#coding=utf-8
from bs4 import BeautifulSoup
import requests
from time import sleep
import socket
ua = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"]
url = ""
headers = {'user-agent': ua[0]}
pageUrl= []
downloadList = [];

def initMainPage():
    print "开始装载页面链接"
    try:
        mainPage = requests.get(url,headers=headers)
        #转换成beautifulsoup对象
        mainSoul = BeautifulSoup(mainPage.text)
    
        #print mainSoul.find("div",attrs={"class": "entry-content"}).find_all("p")
    
        #初始化页面
        pageList =  mainSoul.find("div",attrs={"id": "single-navi"}).find_all("a")
    
        pageUrl.append(url)
        for i in range(len(pageList)):
            if len(pageList)-1 == i:
                continue
            pageUrl.append(pageList[i]["href"])
        print "页面链接装载完成" 
    except BaseException:
        print "发生异常，停止5秒"
        sleep(5)
        print "重新加载页面链接"
    except socket.error:
        print "发生异常，停止5秒"
        sleep(5)
        print "重新加载页面链接"
            



    
#获取每页的图片连接
def initEachPageImag():
    print "开始装载图片链接"
    for i in range(len(pageUrl)):
        try:
            initPageImagUrl(pageUrl[i],None)
        except BaseException:
            print "发生异常，停止5秒"
            sleep(5)
            print "重新加载图片链接，切换请求头"+ua[i%2]
            initPageImagUrl(pageUrl[i],ua[i%2])
        except socket.error:
            print "发生异常，停止5秒"
            sleep(5)
            print "重新加载图片链接，切换请求头"+ua[i%2]
            initPageImagUrl(pageUrl[i],ua[i%2])
    print "所有图片装载链接完成，数量-->"+str(len(downloadList))
        
def initPageImagUrl(url,newua):
    if ua is not None:
        headers["user-agent"]=newua
    #headers["Upgrade-Insecure-Requests"]=1
    try:
        eachPage =  requests.get(url,headers=headers)
        eachPageSoup = BeautifulSoup(eachPage.text)
        pList = eachPageSoup.find("div",attrs={"class": "entry-content"}).find_all("p")
        for i in range(len(pList)):
            pObj = pList[i].find("img")
            if pObj is not None:
                downloadList.append(pObj["src"])
                print pObj["src"] +"--"+ pObj["alt"]
    except BaseException:
        print "发生异常，停止5秒"
        sleep(5)
        print "重新加载图片链接"
        initPageImagUrl(url,newua)
    except socket.error:
        print "发生异常，停止5秒"
        sleep(5)
        print "重新加载图片链接"
        initPageImagUrl(url,newua)  
    
    
            
            


#print len(downloadList)
    
def getDownloadList():
    initMainPage()
    initEachPageImag()
    return downloadList