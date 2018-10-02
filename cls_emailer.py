# -*- coding:utf-8 -*-
from smtplib import SMTP_SSL   # SMTPException


class Sender:
    def __init__(self, recipient=None, subject=None, message=None,
                 login=None, word=None, server='smtp.yandex.ru', port=465):
        self.recipients = recipient
        self.subject = subject
        self.message = message
        self.login = login
        self.word = word
        self.server = server
        self.port = port
        self.msg = None

    def check_server_data(self):
        def none_check(data):
            if data[1] is None:
                print(f'Error: no {data[0]} is specified')
                return True
            return False
        error, warning = False, False
        if none_check(['server', self.server]):
            error = True
        if none_check(['port', self.port]):
            error = True
        if none_check(['login', self.login]):
            error = True
        if none_check(['password', self.word]):
            error = True
        return error, warning

    def send(self, rcpt):
        status = 1
        try:
            sender = self.login
            recepient = rcpt
            subject = self.subject
            self.msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s" % (sender, recepient, subject, self.message))
            # sending data
            s = SMTP_SSL(self.server, self.port)
            s.login(self.login, self.word)
            s.sendmail(sender, recepient, self.msg)
            s.quit()
            status = 0
        finally:
            return status

    def notify(self, recipients=None, subject=None, message=None):
        error, warning = self.check_server_data()
        if recipients and len(recipients) > 0:
            if len(recipients[0]) > 1:
                self.recipients = recipients
            else:
                self.recipients = [recipients, ]
        elif self.recipients and len(self.recipients) > 0:
            if len(self.recipients[0]) == 1:
                self.recipients = [self.recipients, ]
        else:
            print(f'Error: something wrong with recipients, got {self.recipients}')
            error = True
        if not subject and not self.subject:
            print('Warning: no subject')
            # warning = True
            self.subject = ''
        if not message and not self.message:
            print('Warning: no message')
            # warning = True
            self.message = ''
        if error:
            return 1
        # warning is suppressed
        # if warning:  # at this moment warning behaves same as error
        #    return 1
        for recipient in self.recipients:
            res = self.send(recipient)
            if not res:
                print(f'The message was send to {recipient}')
            else:
                print(f'Error: the message was lost on the way to {recipient}')
            # self.sql_write(res)  # should write result in DB, before and after sending
        return 0
