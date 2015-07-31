#!/usr/bin/env python
#coding:utf-8

import urllib
import urllib2
import re
import tool
import os
    
class Spider:
    def __init__(self):
        self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'
        self.tool = tool.Tool()
        
    def getPage(self,pageIndex):
        url = self.siteURL + "?page=" +str(pageIndex)
        print url
        request = urllib2.Request(url)
        reponse = urllib2.urlopen(request)
        return reponse.read().decode('gbk')
    def getContents(self,pageIndex):
        page = self.getPage(pageIndex)
        pattern = re.compile('<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',re.S)
        items = re.findall(pattern,page)
        contents = []
        for item in items:
            contents.append(["http:"+item[0],"http:"+item[1],item[2],item[3],item[4]])
        return contents
    def getDetailPage(self,infoURL):
        reponse = urllib2.urlopen(infoURL)
        return reponse.read().decode('gbk')
    def getBrief(self,page):
        pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
        result = re.search(pattern,page)
        if result:
            return self.tool.replace(result.group(1))
        else:
            return
    def getAllimg(self,page):
        pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
        content = re.search(pattern, page)
        patternImg = re.compile('<img.*?src="(.*?)"',re.S)
        if content:
            images = re.findall(patternImg,content.group(1))
            return images
        else:
            return
    
    def saveImgs(self,images,name):
        number = 1
        #print u"发现",name,u"共有",len(images),u"张照片"
        if images:
            for imageURL in images:
                splitPath = imageURL.split('.')
                fTail = splitPath.pop()
                if len(fTail) > 3:
                    fTail = "jpg"
                    fileName = name + "/" + str(number) + "." +fTail
                    self.saveImgs(imageURL, fileName)
                    number += 1
    def saveIcon(self,iconURL,name):
        splitPath = iconURL.split('.')
        fTail = splitPath.pop()
        fileName = name + "/icon." + fTail 
        self.saveImg(iconURL, fileName)
    def saveBrief(self,content,name):
        if content:
            fileName = name + "/" +name+".txt"
            f = open(fileName,"w+")
            print u"正在保存她的个人信息为",fileName
            f.write(content.encode('utf-8'))
    def saveImg(self,imageURL,fileName):
        u = urllib.urlopen(imageURL)
        data = u.read()
        f = open(fileName,'wb')
        f.write(data)
        print u"正在保存她的一张图片为",fileName
        f.close()
    def mkdir(self,path):
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print u"新建了",path,u"文件夹"
            os.makedirs(path)
            return True
        else:
            print u"名为",path,'的文件夹已经创建成功'
            return False
                
    def savePageInfo(self,pageIndex):
        contents = self.getContents(pageIndex)
        for item in contents:
            print u"名字",item[2],u"年龄",item[3],u"地址",item[4]
            detailURL = item[0]
            print "detailURL:"+ detailURL
            #detailURL = "http:" + detailURL
            detailPage = self.getDetailPage(detailURL)
            brief = self.getBrief(detailPage)
            images = self.getAllimg(detailPage)
            self.mkdir(item[2])
            self.saveBrief(brief,item[2])
            self.saveIcon(item[1],item[2])
            self.saveImgs(images, item[2])
                    
    def savePagesInfo(self,start,end):
        for i in range(start,end+1):
            self.savePageInfo(i)
                    
if __name__ == "__main__":        
    spider = Spider()
    spider.savePagesInfo(2, 10)
