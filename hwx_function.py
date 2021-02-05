"""
Priority(5)：解析优先级，非必填
TTL(600)：TTL值，默认600秒，非必填
Value("121.201.65.98")：记录值，必填
request.set_Type("A")：解析类型，A为解析成IPv4，如需解析根域名，填写@，必填
request.set_RR("www")：子域名，必填
request.set_DomainName("xiaoanran.club")：根域名，必填

返回值说明：
RecordId：解析记录ID，修改和查询域名时需要用到
RequestId：请求ID

"""
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeSubDomainRecordsRequest import DescribeSubDomainRecordsRequest
import urllib.request
import json

#写入文件
def wirte_to_file(path,content):
    with open(path,'w') as f:
        f_name = open(path,'w')
        f_name.write(content)

#新增解析记录，返回json格式的数据
def add_record(client,priority,ttl,record_type,value,rr,domainname):
    request = AddDomainRecordRequest()
    request.set_accept_format('json')

    request.set_Priority(priority)
    request.set_TTL(ttl)
    request.set_Value(value)
    request.set_Type(record_type)
    request.set_RR(rr)
    request.set_DomainName(domainname)

    response = client.do_action_with_exception(request)
    response = str(response, encoding='utf-8')
    relsult = json.loads(response)
    return relsult

#更新解析记录
def update_record(client,priority,ttl,record_type,value,rr,record_id):
    request = UpdateDomainRecordRequest()
    request.set_accept_format('json')

    request.set_Priority(priority)
    request.set_TTL(ttl)
    request.set_Value(value)
    request.set_Type(record_type)
    request.set_RR(rr)
    request.set_RecordId(record_id)

    response = client.do_action_with_exception(request)
    response = str(response, encoding='utf-8')
    return response

#查询解析记录
def Describe_SubDomain_Records(client,record_type,subdomain):
    request = DescribeSubDomainRecordsRequest()
    request.set_accept_format('json')

    request.set_Type(record_type)
    request.set_SubDomain(subdomain)

    response = client.do_action_with_exception(request)
    response = str(response, encoding='utf-8')
    relsult = json.loads(response)
    return relsult

#获取外网地址
def get_internet_ip():
    with urllib.request.urlopen('http://www.3322.org/dyndns/getip') as response:
        html = response.read()
        ip = str(html, encoding='utf-8').replace("\n", "")
    return ip