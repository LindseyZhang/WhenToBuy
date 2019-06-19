# coding: utf-8
import os
import time
import requests
from bs4 import BeautifulSoup
import itchat
import yaml
import datetime as dt
import re

with open('_config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.load(f, Loader=yaml.Loader)
config['last_query_time'] = dt.datetime.min

time_pattern = re.compile('[0-9]{2}:[0-5][0-9]')    

class SmzdmCrawler:       
    def queryProduct(self, key):
        resp = self.requestPage(key)
        if resp != None:
            html_page = resp.text
            return self.parseList(html_page)
        
        # file = open('t.html', 'r')
        # html_page = file.read()
        # return self.parseList(html_page)

    def requestPage(self, key):
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        }

        url = "http://search.smzdm.com/?v=b&c=faxian&s=%s" % key
        resp = requests.get(url, headers=header)
        if resp.status_code == 200:
            return resp
        else:
            return None

    def parseList(self, html_page):
        soup = BeautifulSoup(html_page, 'html.parser')
        contentlist = soup.find('ul', {'id':'feed-main-list'}).find_all('div', {'class': 'z-feed-content'})

        datalist = []
        count = 0
        for content in contentlist:
            count = count + 1
            data = {}
            data['index'] = count

            titles = content.h5.a.text.splitlines()
            var = 'title'
            for title in titles:
                if title.strip() != '':
                    data[var] = title
                    var = 'price'

            btn = content.find('div', {'class': 'feed-link-btn-inner'})
            data['link'] = btn.a.get('href')
        
            extras = content.find('span', {'class': 'feed-block-extras'}).text
            extraline =  extras.splitlines()
            var = 'time' 
            for line in extraline:
                content = line.strip()
                if content != '':
                    if var == 'time':
                        if time_pattern.match(content):
                            time = dt.datetime.strptime(content, "%H:%M").time()
                            data[var] = dt.datetime.combine(dt.date.today(), time)
                        else:
                            datetime = dt.datetime.strptime(content, "%m-%d %H:%M")
                            data[var] = datetime.replace(year = dt.date.today().year)
                        var = 'store'
                    else:
                        data[var] = content
                    
            datalist.append(data)  

        return datalist    

class WechatSender:

    def __init__(self):
        itchat.auto_login(enableCmdQR=2, hotReload=True)  

    def sendMessageToUser(self, message, receiver):
        user = itchat.search_friends(name=receiver)
        for u in user:
            u.send(message)

def run():
    print(config.get('last_query_time'))
    start_query_time = dt.datetime.now()

    datalist = SmzdmCrawler().queryProduct(config.get('search_key'))
    new_data = filter(datalist, config.get('last_query_time'))
    receiver = config.get('receiver_name')  

    if new_data: 
        message = ''       
        for data in new_data:
            message = message + ("%s - %s - %s\n%s %s[%s]\n\n" % (data['time'], data['index'], data['title'], data['price'], data['store'], data['link']))
        
        print("new :", message)
        WechatSender().sendMessageToUser(message, receiver)

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
    