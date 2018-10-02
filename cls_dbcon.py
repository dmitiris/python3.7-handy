# -*- coding: utf-8 -*-

try:
    from cls_readconf import ReadConfig
except ImportError:
    class Dummy:
        def __init__(self):
            pass
    ReadConfig = Dummy()
try:
    from psycopg2 import connect
except ImportError:
    print('ImportError: No module named psycopg2')

    def connect(string):
        assert string
        raise ImportError('ImportError: No module named psycopg2')


class DBConnection:
    def __init__(self, db_name=None, db_user=None, db_word=None, db_host=None, db_port=None, config=False):
        if (config and isinstance(config, ReadConfig)) or isinstance(db_name, ReadConfig):
            if not config:
                config = db_name
            for key in config.attrib:
                if key in ['dbname', 'db_name']:
                    db_name = config.attrib[key]
                if key in ['dbuser', 'db_user']:
                    db_user = config.attrib[key]
                if key in ['dbword', 'db_word']:
                    db_word = config.attrib[key]
                if key in ['dbhost', 'db_host']:
                    db_host = config.attrib[key]
                if key in ['dbport', 'db_port']:
                    db_port = config.attrib[key]
        data = [db_name, db_user, db_word, db_host, db_port]
        keywords = ['dbname', 'user', 'password', 'host', 'port']
        connection_string_parts = ['%s=%s' % (keywords[i], data[i]) for i in range(0, len(data)) if data[i]]
        self.connection_string = ' '.join(connection_string_parts)

    def execute(self, sql_request, sql_data=(), output=True):
        with connect(self.connection_string) as con:
            cur = con.cursor()
            if sql_data:
                cur.execute(sql_request, sql_data)
            else:
                cur.execute(sql_request)
            if output:
                data = cur.fetchall()
            else:
                data = str(cur.statusmessage)
            con.commit()
        return data

    def bulk_upsert(self, table, columns, unique, data, schema='public'):
        """ data = [{}, {}, {}] """
        # print 'DATA:', data
        if len(data) == 0:
            return None      # Just in case data is empty
        pcolumns = ', '.join(columns)
        value_plc = ','.join(['(%s)' % ','.join(['%s' for _ in item]) for item in data])
        punique = ', '.join(unique)
        update = ', '.join(['%s=EXCLUDED.%s' % (column, column) for column in columns])
        sql_query = """
            INSERT INTO %(schema)s.%(table)s (%(columns)s) VALUES %(value_placeholder)s
            ON CONFLICT (%(unique)s) DO UPDATE SET %(update)s;
            """ % {
            'schema': schema, 'table': table, 'columns': pcolumns,
            'value_placeholder': value_plc, 'unique': punique, 'update': update
        }
        """"""
        sql_data = []
        if isinstance(data[0], dict):
            sql_data = [sublist[item] for sublist in data for item in columns]
        elif isinstance(data[0], list):
            sql_data = [item for sublist in data for item in sublist]
        result = self.execute(sql_query, sql_data, output=False)
        return result

    def bulk_delete(self, table, data, data_key, column_key=False, schema='public'):
        if len(data) == 0:
            return 0
        if not column_key:
            column_key = data_key
        keys = ', '.join(["'%s'::text" % item[data_key] for item in data])
        sql_query = """ 
            DELETE FROM %(schema)s.%(table)s WHERE ARRAY[%(unique)s::text] <@ ARRAY[%(keys)s] 
            """ % {'schema': schema, 'table': table, 'unique': column_key, 'keys': keys}
        """"""
        result = self.execute(sql_query, output=False)
        return result
