# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

FROM_ADDRESS = 'lonlylamb@gmail.com'
MY_PASSWORD = 'jiyuJizai62'
TO_ADDRESS = 'WhiteRookNo1@gmail.com'
BCC = 'onlylamb@gmail.com'
SUBJECT = 'Gmail テスト'
BODY = 'mail by python　ホゲホゲ'

def create_message(from_addr, to_addr, bcc_addrs, subject, body):
    #msg = MIMEText(body)
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Bcc'] = bcc_addrs
    msg['Date'] = formatdate()
    return msg


def attach_file(msg):

    # 添付ファイルの設定
    attach_file = {'name': 'CIMG0345.jpg', 'path': '/Users/miracle_super_man/Desktop/cars/CIMG0345.jpg'} # nameは添付ファイル名。pathは添付ファイルの位置を指定
    attachment = MIMEBase('image', 'ipg')
    file = open(attach_file['path'], 'rb+')
    attachment.set_payload(file.read())
    file.close()
    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=attach_file['name'])
    msg.attach(attachment)

    return msg



def send(from_addr, to_addrs, msg):
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(FROM_ADDRESS, MY_PASSWORD)
    smtpobj.sendmail(from_addr, to_addrs, msg.as_string())
    smtpobj.close()


if __name__ == '__main__':

    to_addr = TO_ADDRESS
    subject = SUBJECT
    body = BODY

    msg = create_message(FROM_ADDRESS, to_addr, BCC, subject, body)
    msg = attach_file(msg)
    send(FROM_ADDRESS, to_addr, msg)
