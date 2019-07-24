#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = "无声"

import pymysql

db = pymysql.connect("localhost","root","test123456","test" )

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

sql = "SELECT * FROM testtable"
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    for row in results:
        id = row[0]
        name = row[1]
        age = row[2]

        # 打印结果
        print("id={},name={},age={}".format(id,name,age))
except:
    print("Error: unable to fetch data")

# 关闭数据库连接
db.close()