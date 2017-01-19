# 图片下载
## 如何使用？

* 在ImageDownload/config/\__init__.py目录下修改相关配置参数

```c
#下载根目录
downloadPath="D:\\Download"

#选择器
selector="test"

#线程数
threadNums=10
```
* 根据上步配置的selector，修改ImageDownload/util/Controler.py

```c
def getDownlowdList():
    if config.selector == "test":
        return TestFilter.getDownloadList()
```

* ImageDownload/util/TestFilter.getDownloadList()返回了一个装载图片url的List
* 执行 ImageDownload/main/main.py