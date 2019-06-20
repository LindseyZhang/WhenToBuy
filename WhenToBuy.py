# coding: utf-8
import sys, getopt
import time
import yaml
import datetime as dt
from SmzdmCrawler import SmzdmCrawler
from WechatSender import WechatSender

usage = "python WhenToBuy.py -h -k [key to serarch]"


config = {}
config['receiver_name'] = "文件传输助手"
config['search_key'] = "switch"
config['last_query_time'] = dt.datetime.min

crawler = SmzdmCrawler()
wechatSender = WechatSender()

def run():
    print(config.get('last_query_time'))
    start_query_time = dt.datetime.now()

    datalist = crawler.queryProduct(config.get('search_key'))
    new_data = filter(datalist, config.get('last_query_time'))
    receiver = config.get('receiver_name')  

    if new_data: 
        message = ''       
        for data in new_data:
            message = message + ("%s - %s - %s\n%s %s[%s]\n\n" % (data['time'], data['index'], data['title'], data['price'], data['store'], data['link']))
        
        print(message)
        wechatSender.sendMessageToUser(message, receiver)

    config['last_query_time'] = start_query_time    

def filter(datalist, query_time):
    new_data = []
    for data in datalist:
        if data['time'] > query_time:
            new_data.append(data)
    return new_data

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:k:", ["help", "key="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(usage)
            sys.exit()
        elif opt in ('-k' , '--key'):
            print("search key:", arg)
            config['search_key'] = arg

    while(True):
        run()
        time.sleep(3)