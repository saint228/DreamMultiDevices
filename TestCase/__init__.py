# -*- coding: utf-8 -*-
__author__ = "无声"
import  os

#自动引入当前文件夹下所有py文件
from tools import File
pyList = File.GetPyList("./TestCase")

__all__ = pyList