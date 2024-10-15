#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import database2text.tool as dbtt
from database2text.tool import *

__all__=["connect","readdata"]

class mssql(object):
    def ana_TABLE(otype):
        dbdata["sql"]["TABLE"]={}
        dbdata["exp"]["TABLE"]=[]
        sql="SELECT table_catalog,table_schema,table_name FROM INFORMATION_SCHEMA.TABLES where table_type='BASE TABLE'"
        if 目录:
            sql=f"{sql} and table_catalog='{目录}'"
        if 集合:
            sql=f"{sql} and table_schema='{集合}'"
        for catalog,schema,表名 in db.exec(sql).fetchall():
            if 检查匹配(otype,表名):
                continue
            表id=db.res1(f"select object_id('{catalog}.{schema}.{表名}')")
            表注释=db.res1(f"select value from sys.extended_properties where major_id={表id} and class=1 and name='MS_Description'") or ""
            原始信息=[]
            md=[]
            for i in db.exec2(f"select * from sys.columns where object_id={表id} order by column_id"):
                原始信息.append(i)
                字段描述=db.res1(f"select value from sys.extended_properties where major_id={i['object_id']} and minor_id={i['column_id']}")
                字段类型=db.res1(f"select name from sys.types where system_type_id={i['system_type_id']} and user_type_id={i['user_type_id']}")
                if i["precision"]==0:    #字符型
                    ts=f"{字段类型}({i['max_length']})"
                elif i['scale']==0: #数值型，小数后精度为0
                    ts=f"{字段类型}({i['precision']})"
                else:
                    ts=f"{字段类型}({i['precision']}.{i['scale']})"
                mddata={"name":i["name"], "desc":字段描述 or "", "type":字段类型, "size":i["max_length"], "null":i["is_nullable"], "default":"", "ts":ts}
                md.append(mddata)
            dbdata["sql"]["TABLE"][表名]=[]   #暂不处理
            dbdata["exp"]["TABLE"].append({"tname":表名,"tdesc":表注释,"ori":原始信息,"c":[],"md":md})

def readdata(arg):
    global 读参数,目录,集合
    目录=arg.get("目录","") or arg.get("catalog","")
    集合=arg.get("集合","") or arg.get("schema","")
    读参数=arg
    dbdata["sql"]={}
    dbdata["exp"]={}
    for i in vars(mssql):
        if i.startswith("ana_"):
            otype=i[4:]
            dbdata["sql"][otype]={}
            dbdata["exp"][otype]=[]
            getattr(mssql,i)(otype)

def connect(arg):
    '连接到mssql数据库'
    if "dbcfg" in stdata:
        db.conn=dbtt.dbc.connect()
        return db.conn
    else:
        return dbtt.connect(arg,"pytds")

def export(stdata,storidata):
    dbtt.export(stdata,storidata,dbdata)
