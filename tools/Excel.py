# -*- coding: utf-8 -*-
__author__ = "无声"

import xlwings as xw
import os
import time


def create_log_excel(nowtime,device):
    create_time=time.strftime("%m%d%H%M", nowtime)
    exclefile = create_time+ "_"+ device + "_log.xlsx"
    app = xw.App(visible=True, add_book=False)
    if not os.path.exists(exclefile):
        wb = app.books.add()
        sheet=wb.sheets("Sheet1")
        sheet.range('A1').value = ["Time","TotalMemory", "AllocatedMemory","UsedMemory","FreeMemory","TotalCPU","AllocatedCPU"]
        wb.save(exclefile)
        print("创建Excel文件：{}".format(exclefile))
    return exclefile, sheet,wb

def record_to_excel(sheet,list):
    rng = sheet.range('A1').expand()
    nrow = rng.last_cell.row
    #print("nrow=",nrow)
    currentcell="A"+str(nrow+1)
    sheet.range(currentcell).value =list
    sheet.autofit()


if __name__ == "__main__":
    nowtime=time.localtime()
    filepath,sheet,wb=create_log_excel(nowtime,"62001")
    inputtime=time.strftime("%Y-%m-%d %H:%M:%S", nowtime)
    list=[inputtime,"1024MB","100MB","500MB","300MB","50%","25%"]
    for i in range(100):
        record_to_excel(sheet,list)
    wb.save()