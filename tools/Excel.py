import xlwings as xw
import os
import time


def create_log_excel():
    exclefile = os.getcwd()  + "\log.xlsx"
    app = xw.App(visible=True, add_book=False)
    if not os.path.exists(exclefile):
        wb = app.books.add()
        wb.save(exclefile)
    else:
        wb = app.books.open(exclefile)

def input_log(*kargs):
    pass


def record_allocated_memory(self,timeout=30):
    start_time=time.time()
    while time.time()-start_time<timeout:
        nowmemory=self.get_allocated_memory()
        self.write_excel(nowmemory,"allocated_memory",time.time())
        time.sleep(0.5)


if __name__ == "__main__":
    create_log_excel()