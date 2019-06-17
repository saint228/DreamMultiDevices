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
    sheet.range('A1').value = ["Time","TotalMemory(MB)", "AllocatedMemory(MB)","UsedMemory(MB)","FreeMemory(MB)","TotalCPU","AllocatedCPU"]
    sheet.range('A1:G1').color=205, 197, 191
    wb.save(exclefile)
    print("创建Excel文件：{}".format(exclefile))
    return exclefile,sheet,wb

def calculate(sheet):
    rng = sheet.range('A1').expand()
    nrow = rng.last_cell.row
    AllocatedMemory=sheet.range("C2:C{}".format(nrow)).value
    sum_UsedMemory=sheet.range("D2:D{}".format(nrow)).value
    sum_FreeMemory=sheet.range("E2:E{}".format(nrow)).value
    TotalCPU=sheet.range("F2:F{}".format(nrow)).value
    AllocatedCPU=sheet.range("G2:G{}".format(nrow)).value
    sum_TotalCPU=[]
    while "N/a" in AllocatedMemory:
        AllocatedMemory.remove("N/a")
    while "N/a" in AllocatedCPU:
        AllocatedCPU.remove("N/a")
    for i in range(len(TotalCPU)):
        tmp=float(TotalCPU[i].split("%")[0])
        sum_TotalCPU.append(tmp)
    avg_am,max_am,min_am=getcount(AllocatedMemory)
    avg_um,max_um,min_um=getcount(sum_UsedMemory)
    avg_fm,max_fm,min_fm=getcount(sum_FreeMemory)
    avg_tc,max_tc,min_tc=getcount(sum_TotalCPU)
    avg_ac,max_ac,min_ac=getcount(AllocatedCPU)
    if avg_tc=="N/a":
        pass
    else:
        avg_tc = str(format(avg_tc, ".2f")) + "%"
        max_tc = str(format(max_tc, ".2f")) + "%"
        min_tc = str(format(min_tc, ".2f")) + "%"
    if   avg_ac=="N/a":
         pass
    else:
        avg_ac = str(format(avg_ac * 100,".2f")) + "%"
        max_ac = str(format(max_ac * 100,".2f")) + "%"
        min_ac = str(format(min_ac * 100,".2f")) + "%"
    avglist = ["平均值","",avg_am,avg_um,avg_fm,avg_tc,avg_ac]
    maxlist = ["最大值：","",max_am,max_um,max_fm,max_tc,max_ac]
    minlist = ["最小值：","",min_am,min_um,min_fm,min_tc,min_ac]
    return avglist,maxlist,minlist

def getcount(list):
    sum = avg = max = min = 0
    flag = 0
    try:
        for Na in list:
            flag = flag + 1
            if flag == 1:
                sum = float(Na)
                max = float(Na)
                min = float(Na)
            else:
                sum = sum + float(Na)
                if float(Na) > max:
                    max= float(Na)
                elif float(Na) < min:
                    min = float(Na)
    except Exception as e:
        print(e)
    if sum == 0:
        avg = "N/a"
        max = "N/a"
        min = "N/a"
    else:
        avg = float(format(sum / flag,".2f"))
    return avg,max,min

def record_to_excel(sheet,list,**kwargs):
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
    list=['合计：', "", 'N/a', "", "", "", ""]
    file,sheet, wb = create_log_excel(time.localtime(), "7429")
    record_to_excel(sheet,list,color=(230, 230 ,250))
