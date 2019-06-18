# coding: utf-8
import os
import time
import requests
from bs4 import BeautifulSoup
import itchat
import yaml

with open('_config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.load(f, Loader=yaml.Loader)


class SmzdmCrawler:       
    def queryProduct(self, key):
        # resp = self.requestPage(key)
        # if resp != None:
        #     html_page = resp.text
        #     return self.parseList(html_page)
        
        file = open('t.html', 'r')
        html_page = file.read()
        return self.parseList(html_page)

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
                if line.strip() != '':
                    data[var] = line.strip()
                    var = 'store'

            datalist.append(data)  

        return datalist    

class WechatSender:

    def __init__(self):
        itchat.auto_login(enableCmdQR=2, hotReload=True)  

    def sendMessageToUser(self, message, receiver):
        user = itchat.search_friends(name=receiver)
        user.send(message)

def run():
    datalist = SmzdmCrawler().queryProduct(config.get('search_key'))
    receiver = config.get('receiver_name')  

    if datalist: 
        message = ''       
        for data in datalist:
            message = message + ("%s - %s - %s\n%s %s[%s]\n\n" % (data['time'], data['index'], data['title'], data['price'], data['store'], data['link']))
        
        print(message)
        # WechatSender().sendMessageToUser(message, receiver)

if __name__ == '__main__':
    while(True):
        run()
        time.sleep(3)
    