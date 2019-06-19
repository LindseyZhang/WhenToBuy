# coding: utf-8
import os
import requests
from bs4 import BeautifulSoup
import datetime as dt
import re

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