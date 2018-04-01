# -*- coding: UTF-8 -*-
import os
import threading
from time import sleep
import time
import urllib.request
import queue
import config
import util.Controler
import random
# 重载Utf-8编码
import importlib, sys

importlib.reload(sys)
# sys.setdefaultencoding('utf-8')

# 下载队列
downloadQueue = queue.Queue()

my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"

]


def getImageName(position, url):
    urlArr = url.split(".")
    return position + "." + urlArr[len(urlArr) - 1]


def saveImage(url, name, threadName):
    path = config.downloadPath
    if os.path.exists(path) == False:
        os.mkdir(path)
        print("创建目录" + path)
    try:
        print(threadName + "开始下载" + name)
        randdom_header = random.choice(my_headers)
        headers = {
            'User-Agent': randdom_header}
        # 设置请求头，防止403错误
        req = urllib.request.Request(url=url, headers=headers)
        # 设置响应超时时间为10s，防止阻塞卡死
        feeddata = urllib.request.urlopen(req, timeout=10).read()
        f = open(path + "\\" + name, 'wb')

        # 图片写入
        f.write(feeddata)
        f.close()
        print("下载完成-->" + path + "\\" + name)
    except BaseException:
        print(name + "下载异常，暂停5秒")
        sleep(5)
        saveImage(url, name, threadName)


def downloadThread(threadName, downloadQueue, maxsize):
    print(threadName + "启动")
    while downloadQueue.empty() == False:
        url = downloadQueue.get()
        name = getImageName(str(maxsize - downloadQueue.qsize()), url)
        saveImage(url, name, threadName)
    print(threadName + "执行完毕")


class myThread(threading.Thread):
    def __init__(self, threadID, name, downloadQueue, size):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.downloadQueue = downloadQueue
        self.size = size

    def run(self):
        downloadThread(self.name, self.downloadQueue, self.size)


if __name__ == '__main__':
    startTime = time.time()
    # 线程池
    threads = []
    threadCount = 0

    # 获取下载列表
    downloadList = util.Controler.getDownlowdList()

    # 构建队列
    for downloadUrl in downloadList:
        downloadQueue.put(downloadUrl)
    size = len(downloadList)

    while threadCount <= config.threadNums:
        # 创建下载线程
        threadCount = threadCount + 1
        threadName = "线程" + str(threadCount)
        # t = threading.Thread(target=downloadThread, name=threadName, args=((threadName, downloadQueue, size)))
        t = myThread(threadCount, threadName, downloadQueue, size)
        t.start()
        threads.append(t)
        # t.join()

    # 等待线程运行完毕
    for th in threads:
        th.join()

    endTime = time.time()
    print('Done %s ' % (endTime - startTime))
