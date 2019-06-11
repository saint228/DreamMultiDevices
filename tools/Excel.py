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
        print(exclefile)
    return exclefile, sheet,wb

def record_to_excel(sheet,nowtime,*,TotalMemory,AllocatedMemory,UsedMemory,FreeMemory,TotalCPU,AllocatedCPU):
    sheet.range("A2").value =time.strftime("%Y-%m-%d %H:%M:%S",nowtime)
    sheet.range("B2").value=TotalMemory
    sheet.range("C2").value=AllocatedMemory
    sheet.range("D2").value=UsedMemory
    sheet.range("E2").value=FreeMemory
    sheet.range("F2").value=TotalCPU
    sheet.range("G2").value=AllocatedCPU

if __name__ == "__main__":
    nowtime=time.localtime()
    print(nowtime)
    filepath,sheet,wb=create_log_excel(nowtime,"62001")
    record_to_excel(sheet,nowtime,TotalMemory="1024MB",AllocatedMemory="100MB",UsedMemory="500MB",FreeMemory="300MB",TotalCPU="50%",AllocatedCPU="25%")
    wb.save()