# -*- coding: utf-8 -*-
# @Time    : 2022/8/23 15:30
# @Author  : Python超人
# @FileName: mail.py

import smtplib, email, sys, datetime
from email import encoders
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import os


class Mail(object):
    def __init__(self, account):
        self.from_account = account

    @staticmethod
    def build_mail(mail_addr, password, smtp_server, display_name=None):
        """
        创建一个发送帐号
        :param mail_addr: 不能为空，邮件发送者的邮箱地址
        :param password: 发送者邮箱的密码
        :param smtp_server: 发送者邮箱SMTP服务器地址
        :param display_name: 邮件发送者名称，可以为空，如果为空，则显示 mail_from
        :return:
        """

        mail_from_account = {
            "display_name": display_name,  # 可以为空，邮件显示名称，如果为空，则显示 mail_addr
            "mail_addr": mail_addr,  # 不能为空，发送者的邮箱地址
            "password": password,  # 不能为空，发送者的邮箱密码，如果不是你设定的密码，在该邮箱的官网上面咨询
            "smtp_server": smtp_server  # 不能为空，发送者的邮箱SMTP服务器地址，在该邮箱的官网上面咨询
        }
        return Mail(mail_from_account)

    def zhuanma(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def writelog(self, proname, errcont):
        now = datetime.datetime.now()
        today = now.strftime('%Y-%m-%d')
        now = now.strftime('%Y-%m-%d %H:%M:%S')
        errfile = open(proname + today + '.log', 'a')
        errfile.write(now + ' ' + str(errcont) + '\n')
        errfile.close()

    def build_attachment(self, file_path, filename=None, content_type='application/octet-stream'):
        # 添加附件
        if filename is None:
            filename = os.path.basename(file_path)

        # 解决办法： 将 att1[‘Content-Disposition’] = 'attachment;filename = “星测试附件.txt”'
        # 替换成 att1.add_header(‘Content-Disposition’, ‘attachment’, filename=‘星测试附件.txt’)，即可完美解决

        att = MIMEText(open(file_path, 'rb').read(), 'base64', 'utf-8')
        att["Content-Type"] = content_type
        # att["Content-Disposition"] = 'attachment; filename="' + filename + '"'
        att.add_header('Content-Disposition', 'attachment', filename=filename)
        return att

    def send_text(self, mail_to, subject, text, attachment_paths=[]):
        if len(attachment_paths) == 0:
            msg = MIMEText(text, 'plain', 'utf-8')
        else:
            msg = MIMEMultipart('alternative')
            msg.attach(MIMEText(text, 'plain', 'utf-8'))

        self.send(mail_to, subject, msg, attachment_paths)

    def send_html(self, mail_to, subject, html, attachment_paths=[]):
        msg = MIMEMultipart('alternative')
        msg.attach(MIMEText(html, 'html'))
        self.send(mail_to, subject, msg, attachment_paths)

    def send(self, mail_to, subject, msg, attachment_paths=[]):
        from_name = None
        if self.from_account.__contains__('display_name'):
            from_name = self.from_account["display_name"]
        from_addr = self.from_account["mail_addr"]
        password = self.from_account["password"]
        smtp_server = self.from_account["smtp_server"]

        if from_name is None or from_name == '':
            msg['From'] = self.zhuanma(from_addr)
        else:
            msg['From'] = self.zhuanma('%s<%s>' % (from_name, from_addr))

        msg['To'] = mail_to
        msg['Subject'] = Header(subject, 'utf-8').encode()

        for attachment_path in attachment_paths:
            attachment = self.build_attachment(attachment_path)
            msg.attach(attachment)

        try:
            print("SMTP服务器%s连接中..." % smtp_server)
            # server = smtplib.SMTP(smtp_server, 25)

            # 阿里云建议使用SSL，如果WindowServer2008发送失败，建议安装 libs/Win64OpenSSL_Light-1_1_1i.msi
            # from: http://slproweb.com/products/Win32OpenSSL.html
            server = smtplib.SMTP_SSL(smtp_server, 465)

            print("SMTP服务器登录中....")
            server.login(from_addr, password)
            print("邮件发送中....")
            server.sendmail(from_addr, mail_to, msg.as_string())
            server.quit()
            print("邮件发送成功")
        except:
            info = sys.exc_info()
            errcont = info[1]
            self.writelog('mailerror', errcont)
            print('邮件发送失败')