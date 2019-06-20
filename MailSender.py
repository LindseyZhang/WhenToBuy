# coding: utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header

encode = 'utf-8'
class MailSender:

    def __init__(self, qq_mail_address, qq_mail_password):
        self.smtp_server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        self.smtp_server.login(qq_mail_address, qq_mail_password)
        self.sender = qq_mail_address

    def sendMessageToUser(self, message, receiver):
        message = MIMEText(message, 'plain', encode)
        message['From'] = Header("林林总总的机器人", encode)
        message['To'] = Header("小仙女", encode)
        message['Subject'] = Header('什么值得买上有新消息了', encode)

        try:
            print("from %s send to %s:" % (self.sender, receiver))
            self.smtp_server.sendmail(self.sender, receiver, message.as_string().encode(encode))
            print("邮件发送成功！")
        except smtplib.SMTPException:
            print("Error: 邮件发送失败：\n%s" % message.as_string())
