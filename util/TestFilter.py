#coding=utf-8
url = 'https://ss2.baidu.com/6ONYsjip0QIZ8tyhnq/it/u=808236962,3450414267&fm=80&w=179&h=119&img.JPEG'

def getDownloadList():
    count = 0
    downloadList = [];
    while count<200 :
        downloadList.append(url)
        count=count+1
    return downloadList