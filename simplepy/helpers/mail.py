# -*-coding:UTF-8-*-
import datetime
import imaplib
import poplib
from datetime import timedelta

import pytz
from imap_tools import MailBox, OR

from simplepy import logger
from simplepy.config import EMAIL_USER, EMAIL_PWD

"""
POP3/SMTP协议
接收邮件服务器：pop.exmail.qq.com ，使用SSL，端口号995
发送邮件服务器：smtp.exmail.qq.com ，使用SSL，端口号465
海外用户可使用以下服务器
接收邮件服务器：hwpop.exmail.qq.com ，使用SSL，端口号995
发送邮件服务器：hwsmtp.exmail.qq.com ，使用SSL，端口号465

IMAP协议
接收邮件服务器：imap.exmail.qq.com ，使用SSL，端口号993
发送邮件服务器：smtp.exmail.qq.com ，使用SSL，端口号465
海外用户可使用以下服务器
接收邮件服务器：hwimap.exmail.qq.com ，使用SSL，端口号993
发送邮件服务器：hwsmtp.exmail.qq.com ，使用SSL，端口号465
"""

"""
POP3服务器: pop.126.com
SMTP服务器: smtp.126.com
IMAP服务器: imap.126.com
"""


def pop_client():
    # 输入邮件地址、口令和POP3服务器地址
    email = EMAIL_USER
    password = EMAIL_PWD
    pop3_server = 'pop.exmail.qq.com'

    # 连接到POP3 服务器
    server = poplib.POP3(pop3_server)
    # 可以打开或关闭调试信息
    # server.set_debuglevel(1)
    # 可选：输出POP3服务器的欢迎文字
    print(server.getwelcome().decode('utf-8'))

    # 身份认证
    server.user(email)
    server.pass_(password)
    # stat()返回邮件数量和占用空间
    print('Messages: %s. Size: %s' % server.stat())
    # list()返回所有邮件的编号
    resp, mails, octets = server.list()
    # server.retr()
    # 可以查看返回的列表，类似[b'1 82923', b'2 2184', ...]
    print(mails)

    # 获取最新一封邮件, 注意索引号从1 开始
    index = len(mails)
    resp, lines, octets = server.retr(index)
    print(lines[0])

    server.quit()


def imap_client():
    conn = imaplib.IMAP4_SSL(host='imap.exmail.qq.com', port=993)
    conn.login('gaozhe@gaozhe.net', '416798Gao!')
    conn.select()
    # '(OR (TO "tech163@fusionswift.com") (FROM "tech163@fusionswift.com"))'
    #             '(SUBJECT "Example message 2")',
    type_, data = conn.search(None, '(SUBJECT "608913 is your Instagram code ")')
    print(data)

    mail_list = data[0].split()[::-1]
    for num in mail_list:
        type_, data = conn.fetch(num, '(RFC822)')
        print(type_, data)
    conn.close()


def imap_tools_test():
    # Get date, subject and body len of all emails from INBOX folder
    q4 = OR(from_=["@exmail.weixin.qq.com"])
    with MailBox('imap.exmail.qq.com').login(EMAIL_USER, EMAIL_PWD) as mailbox:
        for msg in mailbox.fetch(reverse=True):
            if msg.subject.find('your Instagram code') > -1:
                logger.info(msg.subject, timedelta(hours=15) + msg.date)
                start = timedelta(hours=15) + msg.date
                end = datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC'))
                logger.info(start.minute, end.minute)


if __name__ == '__main__':
    imap_tools_test()
