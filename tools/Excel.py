# -*- coding: utf-8 -*-
__author__ = "无声"

import xlwings as xw
import os
import time
import json
import matplotlib.pyplot as plot

#创建一个log_excel用以记录性能数据
def create_log_excel(nowtime,device):
    create_time=time.strftime("%m%d%H%M", nowtime)
    exclefile = create_time+ "_"+ device + "_log.xlsx"
    app = xw.App(visible=True, add_book=False)
    wb = app.books.add()
    sheet=wb.sheets("Sheet1")
    sheet.range('A1').value = ["Time","TotalMemory(MB)", "AllocatedMemory(MB)","UsedMemory(MB)","FreeMemory(MB)","TotalCPU","AllocatedCPU","FPS","JankCount"]
    sheet.range('A1:I1').color=205, 197, 191
    wb.save(exclefile)
    print("创建Excel文件：{}".format(exclefile))
    return exclefile,sheet,wb

#计算一个sheet里已存在的所有数据，然后返回该sheet里的各项的平均、最大、最小值。
def calculate(sheet):
    rng = sheet.range('A1').expand()
    nrow = rng.last_cell.row
    AllocatedMemory=sheet.range("C2:C{}".format(nrow)).value
    sum_UsedMemory=sheet.range("D2:D{}".format(nrow)).value
    sum_FreeMemory=sheet.range("E2:E{}".format(nrow)).value
    TotalCPU=sheet.range("F2:F{}".format(nrow)).value
    AllocatedCPU=sheet.range("G2:G{}".format(nrow)).value
    FPS=sheet.range("H2:H{}".format(nrow)).value
    JankCount=sheet.range("I2:I{}".format(nrow)).value
    sum_TotalCPU=[]
    while "N/a" in AllocatedMemory:
        AllocatedMemory.remove("N/a")
    while "N/a" in AllocatedCPU:
        AllocatedCPU.remove("N/a")
    while "N/a" in FPS:
        FPS.remove("N/a")
    while "N/a" in JankCount:
        JankCount.remove("N/a")
    for i in range(len(TotalCPU)):
        tmp=float(TotalCPU[i].split("%")[0])
        sum_TotalCPU.append(tmp)
    avg_am,max_am,min_am=getcount(AllocatedMemory)
    avg_um,max_um,min_um=getcount(sum_UsedMemory)
    avg_fm,max_fm,min_fm=getcount(sum_FreeMemory)
    avg_tc,max_tc,min_tc=getcount(sum_TotalCPU)
    avg_ac,max_ac,min_ac=getcount(AllocatedCPU)
    avg_fps,max_fps,min_fps=getcount(FPS)
    avg_jc, max_jc, min_jc = getcount(JankCount)
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
    avglist = ["平均值","",avg_am,avg_um,avg_fm,avg_tc,avg_ac,avg_fps,avg_jc]
    maxlist = ["最大值：","",max_am,max_um,max_fm,max_tc,max_ac,max_fps,max_jc]
    minlist = ["最小值：","",min_am,min_um,min_fm,min_tc,min_ac,min_fps,min_jc]
    return avglist,maxlist,minlist

#统计一个list的平均、最大、最小值
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

#读取传过来的list和excel，将list写入excel的下一行
def record_to_excel(sheet,list,**kwargs):
    rng = sheet.range('A1').expand()
    nrow = rng.last_cell.row
    currentcell="A"+str(nrow+1)
    currentcellpng="J"+str(nrow+1)
    currentcellrange=currentcell+":"+"I"+str(nrow+1)
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

#在excel里查找指定键名的列，将该列所有数值（不算最后3行统计行）返回成一个serieslist
def get_series(sheet,Key):
    rng = sheet.range('A1').expand()
    nrow = rng.last_cell.row-3
    rng2=sheet.range('A1:G1')
    serieslist = []
    for key in rng2:
        if key.value==Key:
            cum=key.address
            cum=cum.split("$")[1]
            tmp=cum+"2:"+cum+str(nrow)
            serieslist=sheet.range(tmp).value
            break
    return  serieslist

#在序列表里查询指定键值对，转成json返回
def get_json(sheet,Key):
    series = get_series(sheet, Key)
    series_json=json.dumps({Key:series})
    return series_json




if __name__ == "__main__":
    '''
    file,sheet, wb = create_log_excel(time.localtime(), "7429")
    nowtime = time.localtime()
    inputtime = str(time.strftime("%H:%M:%S", nowtime))
    list=[inputtime,"2","3","4","5","6","7"]
    record_to_excel(sheet,list)
    record_to_excel(sheet, list)
    record_to_excel(sheet, list)
    record_to_excel(sheet, list)
    record_to_excel(sheet, list)
    record_to_excel(sheet, list)
    record_to_excel(sheet, list)
    record_to_excel(sheet, list)
    record_to_excel(sheet, list)
    #get_series(sheet,"AllocatedMemory(MB)")
    rng=sheet.range("A2")
    print(rng.number_format)

    print(rng.value)
    '''
    app = xw.App(visible=True, add_book=False)
    filepath="D:\\Python3.7\\Lib\\site-packages\\DreamMultiDevices\\06241127_7401_log.xlsx"
    wb = app.books.open(filepath)
    sheet=wb.sheets['sheet1']
    time_series=get_series(sheet,"Time")
    am_series=get_series(sheet,"AllocatedCPU")
    tm_series=get_series(sheet,"TotalCPU")
    for i in range(len(tm_series)):
        tm_series[i]=tm_series[i].split("/")[0]

    for i in range(len(am_series)):
        if am_series[i]=="N/a":
            am_series[i]=0
    plot.figure()
    plot.yticks(tm_series)
    plot.plot(time_series)
    plot.show()




