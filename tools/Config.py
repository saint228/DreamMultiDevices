    # -*- coding: utf-8 -*-
__author__ = "无声"
import configparser

config = configparser.ConfigParser()

#解析config文件并将其结果转成一个list，对单个的value，到时候可以用[0]来取到。
def getValue(path,section):
    config.read(path)
    result = config.get("config",section)
    list=result.split(",")
    return list



