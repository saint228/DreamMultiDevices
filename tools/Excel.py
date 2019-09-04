# -*- coding: utf-8 -*-
__author__ = "无声"

import xlwings as xw
import os
import time
import json
import traceback

'''
每次都会生成一个空的sheet1，换了好几种初始化方式都无效，不知道为什么，谁xlwings玩得溜的求告知。
'''
reportpath = os.path.join(os.getcwd(), "Report")
datapath=os.path.join(reportpath, "Data")

#创建一个log_excel用以记录性能数据
def create_log_excel(nowtime,device):
    create_time=time.strftime("%m%d%H%M", nowtime)
    exclefile = datapath+"\\"+create_time+ "_"+ device + "_log.xlsx"
    app = xw.App(visible=True, add_book=False)
    wb = app.books.add()
    sheet = wb.sheets.active
    sheet.range('A1').value = ["Time","TotalMemory(MB)", "AllocatedMemory(MB)","UsedMemory(MB)","FreeMemory(MB)","TotalCPU","AllocatedCPU","FPS","","PNG","PNGAddress"]
    sheet.range('A1:K1').color=205, 197, 191
    if os.path.exists(exclefile):
        raise Exception( "FileHasExisted")
    wb.save(exclefile)
    print("创建Excel文件：{}".format(exclefile))
    return exclefile,sheet,wb

#计算一个sheet里已存在的所有数据，然后返回该sheet里的各项的平均、最大、最小值。
def calculate(sheet):
    #获取excel里的所有已被编辑数据
    rng = sheet.range('A1').expand()
    #获取行号
    nrow = rng.last_cell.row
    #获得对应数据列的数据
    AllocatedMemory=sheet.range("C2:C{}".format(nrow)).value
    sum_UsedMemory=sheet.range("D2:D{}".format(nrow)).value
    sum_FreeMemory=sheet.range("E2:E{}".format(nrow)).value
    sum_TotalCPU=sheet.range("F2:F{}".format(nrow)).value
    AllocatedCPU=sheet.range("G2:G{}".format(nrow)).value
    FPS=sheet.range("H2:H{}".format(nrow)).value
    #sum_TotalCPU=[]
    #为了统计最大最小平均值，需要剔除掉空值的N/a。
    while "N/a"  in AllocatedMemory:
        AllocatedMemory.remove("N/a")
    while "N/a"  in AllocatedCPU:
        AllocatedCPU.remove("N/a")
    for i in range(len(AllocatedCPU)):
        AllocatedCPU[i]=float(AllocatedCPU[i][:-1])
    while "N/a"  in FPS:
        FPS.remove("N/a")
    for i in range(len(sum_TotalCPU)):
        sum_TotalCPU[i]=float(sum_TotalCPU[i][:-1])
    avg_am,max_am,min_am=getcount(AllocatedMemory)
    avg_um,max_um,min_um=getcount(sum_UsedMemory)
    avg_fm,max_fm,min_fm=getcount(sum_FreeMemory)
    avg_tc,max_tc,min_tc=getcount(sum_TotalCPU)
    avg_ac,max_ac,min_ac=getcount(AllocatedCPU)
    avg_fps,max_fps,min_fps=getcount(FPS)
    #CPU的数据需要处理下百分号
    if avg_tc=="N/a":
        pass
    else:
        avg_tc = str(format(avg_tc, ".2f")) + "%"
        max_tc = str(format(max_tc, ".2f")) + "%"
        min_tc = str(format(min_tc, ".2f")) + "%"
    if   avg_ac=="N/a":
         pass
    else:
        avg_ac = str(format(avg_ac  ,".2f")) + "%"
        max_ac = str(format(max_ac  ,".2f")) + "%"
        min_ac = str(format(min_ac  ,".2f")) + "%"
    #填充excel表格的list。每个字段对应excle的一列。
    avglist = ["平均值","",avg_am,avg_um,avg_fm,avg_tc,avg_ac,avg_fps]
    maxlist = ["最大值：","",max_am,max_um,max_fm,max_tc,max_ac,max_fps]
    minlist = ["最小值：","",min_am,min_um,min_fm,min_tc,min_ac,min_fps]
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
        print(traceback.format_exc())
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
    #记录截图的链接和实际地址
    currentcellpng="J"+str(nrow+1)
    currentcellpngvalue="K"+str(nrow+1)
    currentcellrange=currentcell+":"+"H"+str(nrow+1)
    sheet.range(currentcell).value =list
    #分行换色
    if nrow % 2 == 0:
        sheet.range(currentcellrange).color = 173, 216, 230
    else:
        sheet.range(currentcellrange).color = 221, 245, 250
    #单独处理颜色参数以及截图参数
    for  key, value  in kwargs.items():
        if key=="color":
            sheet.range(currentcellrange).color=value
        if key == "png":
            sheet.range(currentcellpng).add_hyperlink(value,"截图","提示：点击打开截图")
            sheet.range(currentcellpngvalue).value=value
    sheet.autofit()

#在excel里查找指定键名的列，将该列所有数值（不算最后3行统计行）返回成一个serieslist
def get_series(sheet,Key):
    rng = sheet.range('A1').expand()
    nrow = rng.last_cell.row-3
    rng2=sheet.range('A1:K1')
    serieslist = []
    for key in rng2:
        if key.value==Key:
            cum=key.address
            cum=cum.split("$")[1]
            tmp=cum+"2:"+cum+str(nrow)
            serieslist=sheet.range(tmp).value
            break
    if Key=="TotalCPU" or Key=="AllocatedCPU" :
        for i in range(len(serieslist)):
            if serieslist[i] == "N/a":
                serieslist[i] = 0
            else:
                stringnum=serieslist[i][:-1]
                serieslist[i] = float(stringnum)
    if Key=="AllocatedMemory(MB)" or Key=="FPS":
        for i in range(len(serieslist)):
            if serieslist[i]=="N/a":
                serieslist[i]=0
    return  serieslist

#在序列表里查询指定键值对，转成json返回
def  get_json(sheet,Key):
    series = get_series(sheet, Key)
    series_json=json.dumps({Key:series})
    return series_json






