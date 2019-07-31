# -*- coding: utf-8 -*-
__author__ = "无声"

import xlwings as xw
import os
import time
import json

resultData = {
    "Time_series": [],
    "TotalMemory": [],
    "AllocatedMemory": [],
    "UsedMemory": [],
    "FreeMemory": [],
    "TotalCPU": [],
    "AllocatedCPU": [],
    "FPS": [],
    "PNGAddress": [],
    "data_count": [],
}

def create_log_json(nowtime,device):
    create_time = time.strftime("%m%d%H%M", nowtime)
    jsonfile = create_time + "_" + device + "_log.json"
    if os.path.exists(jsonfile):
        raise Exception( "FileHasExisted")
    f = open(jsonfile, "w")
    f.close()
    return jsonfile

def  record_to_json(jsonfilepath,list):
    print("json=",jsonfilepath)
    print(list)
    for i in range(len(list)):
        if list[i] =="N/a":
            list[i] = "0"
    list[1]=float(list[1])
    list[2]=float(list[2])
    list[3]=float(list[3])
    list[4]=float(list[4])
    list[5]=float(list[5])*100
    list[6]=float(list[6].split("%")[0])
    list[7]=float(list[7])
    resultData["Time_series"].append(list[0])
    resultData["TotalMemory"].append(list[1])
    resultData["AllocatedMemory"].append(list[2])
    resultData["UsedMemory"].append(list[3])
    resultData["FreeMemory"].append(list[4])
    resultData["TotalCPU"].append(list[5])
    resultData["AllocatedCPU"].append(list[6])
    resultData["FPS"].append(list[7])
    resultData["PNGAddress"].append(list[8])

def calculate_by_json(jsonfile):
    print("enter calculate_by_json")
    avglist=[1234,123,653]
    maxlist=[5643,654,654]
    minlist=[589,65,321]
    data_count={"avg":avglist,"max":maxlist,"min":minlist}
    resultData["data_count"].append(data_count)
    resultJson = json.dumps(resultData)
    f = open(jsonfile, "w")
    f.write(resultJson)
    f.close()

