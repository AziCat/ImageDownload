# -*- coding: UTF-8 -*-
import os
import sys
import threading
from time import sleep
import time
import urllib2
import Queue
import config
import util.Controler

#重载Utf-8编码
reload(sys)
sys.setdefaultencoding('utf-8')

#下载队列
downloadQueue = Queue.Queue()
    
def getImageName(position,url):  
    urlArr = url.split(".")
    return  position+"."+urlArr[len(urlArr)-1]
    
def saveImage(url,name,threadName):
    path = config.downloadPath
    if os.path.exists(path) == False:
        os.mkdir(path)
        print "创建目录"+path
    try:
        print threadName+"开始下载"+name
        headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        #设置请求头，防止403错误
        req = urllib2.Request(url = url,headers = headers)
        #设置响应超时时间为10s，防止阻塞卡死
        feeddata = urllib2.urlopen(req,timeout=10).read()  
        f = open(path+"\\"+name,'wb')  
        
        #图片写入
        f.write(feeddata)  
        f.close()   
    except BaseException:
        print name+"下载异常，暂停5秒"
        sleep(5)
        saveImage(url,name,threadName);
    
    print "下载完成-->"+path+"\\"+name

def downloadThread(threadName,downloadQueue,maxsize):
    print threadName+"启动"
    while downloadQueue.empty() == False:
        url = downloadQueue.get()
        name = getImageName(str(maxsize-downloadQueue.qsize()), url)
        saveImage(url, name,threadName)
    print threadName+"执行完毕"
    
if __name__ == '__main__':
    startTime = time.time()
    #线程池  
    threads = []
    threadCount = 0
    
    #获取下载列表
    downloadList = util.Controler.getDownlowdList()
    
    #构建队列
    for downloadUrl in downloadList:
        downloadQueue.put(downloadUrl)
    size = len(downloadList)
     
    while threadCount<=config.threadNums:
        #创建下载线程
        threadCount = threadCount+1
        threadName = "线程"+str(threadCount)
        t = threading.Thread(target=downloadThread, name=threadName,args=((threadName,downloadQueue,size)))
         
        t.start()
        threads.append(t)
        #t.join()
         
    # 等待线程运行完毕  
    for th in threads:  
        th.join() 
     
    endTime = time.time()
    print 'Done %s ' % (endTime-startTime)
    