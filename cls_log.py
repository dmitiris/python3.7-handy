# -*- coding:utf-8 -*-
from datetime import datetime


# from cls_log import LogObj as LOG
class LogClass:
    def __init__(self, log_name='default.log', to_log=False):
        self.log_name = log_name
        self.to_log = to_log

    def if_log_exists(self):
        try:
            with open(self.log_name, 'r'):
                pass
            return True
        except IOError:
            return False

    def show(self, *args):
        data = [str(datetime.now()), ]
        data += [str(item) for item in args]
        if self.to_log:
            if self.if_log_exists():
                with open(self.log_name, 'a') as fp:
                    fp.write('\t'.join(data))
            else:
                with open(self.log_name, 'w') as fp:
                    fp.write('\t'.join(data))
        else:
            print('\t'.join(data))


LogObj = LogClass()
