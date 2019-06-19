# coding: utf-8
import os
import time
import requests
import yaml
import datetime as dt
import re
from SmzdmCrawler import SmzdmCrawler
from WechatSender import WechatSender

with open('_config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.load(f, Loader=yaml.Loader)

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
        
        print("new :", message)
        wechatSender.sendMessageToUser(message, receiver)

    config['last_query_time'] = start_query_time    

def filter(datalist, query_time):
    new_data = []
    for data in datalist:
        if data['time'] > query_time:
            new_data.append(data)
    return new_data

if __name__ == '__main__':
    while(True):
        run()
        time.sleep(3)
    