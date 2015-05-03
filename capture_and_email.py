#!/usr/bin/python3
__author__ = 'avi'

"""
captures an image from the camera and emails it to the specfied email address

"""


import subprocess, shlex
import logging
import base64

import smtplib
from os.path import basename
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from datetime import datetime


class CaptureException(Exception):
    def __init__(self, message):
        super(CaptureException, self).__init__('Image capturing error: {}'.format(message))


class Base:
    def __init__(self):
        self.datestamp = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')


class Capture(Base):
    def __init__(self, config):
        super(Capture, self).__init__()
        self.command = config['command']
        self.file_name = config['filename_template'].format(self.datestamp)
        self.arguments = config['arguments_template'].format(self.file_name)

    def capture_image(self):
        exit_code = subprocess.call([self.command] + shlex.split(self.arguments))
        if exit_code != 0:
            raise CaptureException('Subprocess {0} returned non-zero status {1}; arguments: "{2}"'.format(self.command, exit_code, self.arguments))
        return self.file_name


class CaptureAndEmail(Capture):
    def __init__(self, config):
        super(CaptureAndEmail, self).__init__(config.snapshot_command)
        self.server = config.email_config['server']
        self.username = config.email_config['username']
        self.password = base64.b64decode(config.email_config['password'].encode()).decode()
        self.addressee = config.email_config['addressee']

    @staticmethod
    def get_attachmnet(filename):
        with open(filename, "rb") as file:
            return MIMEImage(
                file.read(),
                Content_Disposition='attachment; filename="%s"' % basename(filename),
            )

    def send_mail(self):
        attachment = self.capture_image()

        msg = MIMEMultipart(
            From=self.username,
            To=self.addressee,
            Date=formatdate(localtime=True),
            Subject='Login attempt detected'
        )

        msg.attach(MIMEText('Camera capture image attached'))
        msg.attach(self.get_attachmnet(attachment))

        server = smtplib.SMTP(self.server)
        server.set_debuglevel(False)
        server.ehlo()

        server.starttls()
        server.login(self.username, self.password)

        server.sendmail(self.username, self.addressee, msg.as_string())
        server.quit()
        server.close()


def main():
    try:
        import capture_and_email_config as config
        capture = CaptureAndEmail(config)
        capture.send_mail()
    except Exception as ex:
        logging.error(ex)


if __name__ == '__main__':
    main()
