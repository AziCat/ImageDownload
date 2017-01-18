#coding=utf-8
import config
from util import TestFilter

def getDownlowdList():
    if config.selector == "test":
        return TestFilter.getDownloadList()
    