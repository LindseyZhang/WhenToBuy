# coding: utf-8
import sys, getopt
import time
import datetime as dt
from SmzdmCrawler import SmzdmCrawler
from MailSender import MailSender

usage = "python WhenToBuy.py \n\
-h 帮助 \n\
-k 要查找的内容,默认是 switch \n\
-s [必填] 发送邮件的qq邮箱地址 \n\
-p [必填] 发送邮件的qq邮箱授权码（如何获得授权码请参考：https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256）\n\
-r [必填] 接收邮件的地址，可以与发送邮箱相同"

config = {}
config['search_key'] = "switch"
config['last_query_time'] = dt.datetime.min

crawler = SmzdmCrawler()

def run(sender, receivers):
    print(config.get('last_query_time'))
    start_query_time = dt.datetime.now() + dt.timedelta(hours = 8)

    datalist = crawler.queryProduct(config.get('search_key'))
    new_data = filter(datalist, config.get('last_query_time'))

    if new_data: 
        message = ''       
        for data in new_data:
            message = message + ("%s - %s - %s\n%s %s[%s]\n\n" % (data['time'], data['index'], data['title'], data['price'], data['store'], data['link']))
        
        print(message)
        sender.sendMessageToUser(message, receivers)

    config['last_query_time'] = start_query_time    

def filter(datalist, query_time):
    new_data = []
    for data in datalist:
        if data['time'] > query_time:
            new_data.append(data)
    return new_data

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:k:s:r:p:", ["help", "key="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    
    sender_password = ''
    sender_mail = ''
    receiver_mail = ''

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(usage)
            sys.exit()
        elif opt in ('-k' , '--key'):
            print("search key:", arg)
            config['search_key'] = arg
        elif opt == '-s':
            sender_mail = arg
        elif opt == '-p':
            sender_password = arg
        elif opt == '-r':
            receiver_mail = arg

    if sender_mail == '' or sender_password == '' or receiver_mail == '':
        print(usage)
        sys.exit(1)

    mailSender = MailSender(sender_mail, sender_password)
    while(True):
        run(mailSender, receiver_mail)
        time.sleep(60)