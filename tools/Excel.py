# -*- coding: utf-8 -*-
__author__ = "无声"

import xlwings as xw
import os
import time


def create_log_excel(nowtime,device):
    create_time=time.strftime("%m%d%H%M", nowtime)
    exclefile = create_time+ "_"+ device + "_log.xlsx"
    app = xw.App(visible=True, add_book=False)
    wb = app.books.add()
    sheet=wb.sheets("Sheet1")
    sheet.range('A1').value = ["Time","TotalMemory", "AllocatedMemory","UsedMemory","FreeMemory","TotalCPU","AllocatedCPU"]
    sheet.range('A1:G1').color=205, 197, 191
    wb.save(exclefile)
    print("创建Excel文件：{}".format(exclefile))
    return exclefile,sheet,wb

def calculate_avg(sheet):
    rng = sheet.range('A1').expand()

    avglist=["合计："]
    return avglist

def calculate_max(sheet):
    maxlist=["最大值："]
    return maxlist
def calculate_min(sheet):
    minlist=["最小值："]
    return minlist

def record_to_excel(sheet,list,**kwargs):
    print("list=",list)
    print("kw=",kwargs)
    rng = sheet.range('A1').expand()
    nrow = rng.last_cell.row
    currentcell="A"+str(nrow+1)
    currentcellpng="H"+str(nrow+1)
    currentcellrange=currentcell+":"+"G"+str(nrow+1)
    sheet.range(currentcell).value =list
    if nrow % 2 == 0:
        sheet.range(currentcellrange).color = 173, 216, 230
    else:
        sheet.range(currentcellrange).color = 221, 245, 250
    for  key, value  in kwargs.items():
        if key=="color":
            sheet.range(currentcellrange).color=value
        if key == "png":
            sheet.range(currentcellpng).add_hyperlink(value,"截图","提示：点击打开截图")
    sheet.autofit()

if __name__ == "__main__":
    nowtime=time.localtime()
    filepath,sheet,wb=create_log_excel(nowtime,"62001")
    inputtime=time.strftime("%Y-%m-%d %H:%M:%S", nowtime)
    list=[inputtime,"1024MB","100MB","500MB","300MB","50%","25%"]
    for i in range(100):
        record_to_excel(sheet,list)
    wb.save()