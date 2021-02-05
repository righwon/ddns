#!/usr/bin/env python
#coding=utf-8

"""
新增域名解析记录，参数说明如下：
<accessKeyId>：填写自己的accessKey，建议使用RAM角色管理的Key
<accessSecret>：填写自己的accessSecret，建议使用RAM角色管理的Secret

"""

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from hwx_function import *
import os
import time


while True:
    #判断存放IP的文件是否存在，不存在则创建
    if os.path.exists("./ip"):
        pass
    else:
        wirte_to_file("./ip","0.0.0.0")

    client = AcsClient('LTAI4Fe7jf58X2tLNWdAY9Ri', 'DO19eLdhD0sCOpMD9lbzxPK9NUKLdY', 'cn-hangzhou')

    #通过函数获取外网ip
    ip = get_internet_ip()
    #print(ip)

    #下面开始对比ip，如果ip与之前记录的ip一致，则不执行任何操作，如果ip有变化，则会更新本地存储文件和更新域名解析
    with open("./ip", 'r') as f:
        old_ip = f.read()
    if ip == old_ip:
        print("noupdate"+"\nnew_ip:"+ip+"\nold_ip:"+old_ip)
    else:
        #print("update"+"\nnew_ip:"+ip+"\nold_ip:"+old_ip)
        wirte_to_file("./ip",ip)
        des_relsult = Describe_SubDomain_Records(client,"A","sz.yeapl.com")
		#判断子域名解析记录查询结果，TotalCount为0表示不存在这个子域名的解析记录，需要新增一个
        if des_relsult["TotalCount"] == 0:
            add_relsult = add_record(client,"5","600","A",ip,"sz","yeapl.com")
            record_id = add_relsult["RecordId"]
            print("域名解析新增成功！")
        #判断子域名解析记录查询结果，TotalCount为1表示存在这个子域名的解析记录，需要更新解析记录，更新记录需要用到RecordId，这个在查询函数中有返回des_relsult["DomainRecords"]["Record"][0]["RecordId"]
        elif des_relsult["TotalCount"] == 1:
            record_id = des_relsult["DomainRecords"]["Record"][0]["RecordId"]
            update_record(client,"5","600","A",ip,"sz",record_id)
            print("域名解析更新成功！")
        else:
            record_id = 0
            print("存在两个子域名解析记录值，请核查删除后再操作！")
        path = './RecordId'
        wirte_to_file(path,record_id)
    time.sleep(1200)
