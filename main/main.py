# -*- coding: UTF-8 -*-
import urllib2
import util.Controler
import os
import config
import threading
import time
import sys
from time import sleep
reload(sys)
sys.setdefaultencoding('utf-8')
    
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
        req = urllib2.Request(url = url,headers = headers)
        feeddata = urllib2.urlopen(req,timeout=10).read()  
        f = open(path+"\\"+name,'wb')  
      
        f.write(feeddata)  
        f.close()   
    except BaseException:
        print name+"下载异常，暂停5秒"
        sleep(5)
        saveImage(url,name,threadName);
    
    print "下载完成-->"+path+"\\"+name

def downloadThread(threadName,downLoadList,start,end):
    print threadName+"启动"
    while start<end:
        url = downLoadList[start]
        name = getImageName(str(start), url)
        saveImage(url, name,threadName)
        start=start+1
    print threadName+"执行完毕"
    
if __name__ == '__main__':
    startTime = time.time()
    #线程池  
    threads = []
    threadCount = 0
    downloadList = util.Controler.getDownlowdList()
    size = len(downloadList)
    buffer = size/config.threadNums
    
    while threadCount<config.threadNums:
        start = threadCount*buffer
        end = (threadCount+1)*buffer
        
        threadCount = threadCount+1
        if threadCount == config.threadNums:
            end = size
        threadName = "线程"+str(threadCount)
        t = threading.Thread(target=downloadThread, name=threadName,args=((threadName,downloadList,start,end)))
        
        t.start()
        threads.append(t)
        #t.join()
        
    # 等待线程运行完毕  
    for th in threads:  
        th.join() 
    
    endTime = time.time()
    print 'Done %s ' % (endTime-startTime)
    