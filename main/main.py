# -*- coding: UTF-8 -*-
import urllib2
import util.Controler
import os
import config
import threading
import time


    
def getImageName(position,url):  
    urlArr = url.split(".")
    return  position+"."+urlArr[len(urlArr)-1]
    
def saveImage(url,name):
    path = config.downloadPath
    if os.path.exists(path) == False:
        os.mkdir(path)
        print "创建目录"+path
         
    conn = urllib2.urlopen(url)  
    f = open(path+"\\"+name,'wb')  
      
    f.write(conn.read())  
    f.close()
    print "下载完成-->"+path+"\\"+name

def downloadThread(threadName,downLoadList,start,end):
    print threadName+"启动"
    while start<end:
        url = downLoadList[start]
        name = getImageName(str(start), url)
        saveImage(url, name)
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
    