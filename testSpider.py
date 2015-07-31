#!/usr/bin/env python
#coding:utf-8

import urllib
import urllib2
import re
class Spider:
    def __init__(self):
        self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'
    def getPage(self,pageIndex):
        url = self.siteURL + "?page=" + str(pageIndex)
        print url
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().decode('gbk')
    def getContents(self,pageIndex):
        page = self.getPage(pageIndex)
        pattern = re.compile('<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',re.S)
        items = re.findall(pattern,page)
        for item in items:
            print "item[0]"+"http:"+item[0]
            print "item[1]"+"http:"+item[1]
            print "item[2]"+item[2]
            print "item[3]"+item[3]
            print "item[4]"+item[4]

if __name__ == '__main__':
    spider = Spider()
    spider.getContents(2)