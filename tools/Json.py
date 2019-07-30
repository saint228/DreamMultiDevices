# -*- coding: utf-8 -*-
__author__ = "无声"

import xlwings as xw
import os
import time
import json

def create_log_json(nowtime,device):
    create_time = time.strftime("%m%d%H%M", nowtime)
    jsonfile = create_time + "_" + device + "_log.json"
    if os.path.exists(jsonfile):
        raise Exception( "FileHasExisted")
    f = open(jsonfile, "w")
    resultData = {
        "FuncMemory": [],
        "FuncCPU": [],
        "FuncFPS": [],
        "ScreencapPNG": [],
        "YList": [],
        "AllocatedMemory": [],
        "UsedMemory": [],
        "FreeMemory": [],
        "TotalCPU": [],
        "AllocatedCPU": [],
        "AllocatedFPS": [],
        "StatisMemory": [],
        "StatisCPU": [],
        "StatisFPS": [],
    }
    resultJson = json.dumps(resultData)
    f.write(resultJson)
    f.close()

def  record_to_json(jsonfilepath,list,png):
    pass

def calculate_by_json(file):
    print("enter calculate_by_json")
    avglist=[]
    maxlist=[]
    minlist=[]
    return  avglist, maxlist, minlist

def EditReport_by_json(filename, jsonfilepath, avglist, maxlist, minlist):
    print("EditReport_by_json")
    pass