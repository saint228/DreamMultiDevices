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
    f.close()

def collect_data_by_json(madb, jsonfilepath, flag):
    print("enter collect_data_by_json")
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