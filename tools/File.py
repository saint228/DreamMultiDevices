# -*- coding: utf-8 -*-
__author__ = "无声"
import os

def GetPyList(filePath):
    dirList = os.listdir(filePath)
    pyList = []
    for i in range(len(dirList)):
        fileName = dirList[i].split(".")
        if dirList[i] != "__init__.py" and dirList[i] != "__pycache__":
            if fileName[1].lower() == "py":
                pyList.append(fileName[0])
    return pyList

