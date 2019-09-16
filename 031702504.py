#!/usr/bin/python
# -*- coding: UTF-8 -*-

line = input()
'''提取姓名，电话，地址'''
import re
name = re.search(r'^[\u4e00-\u9fa5]{2,5}', line)
'''print(name.group())'''
phone = re.search('(\d{11})', line)
'''print(phone.group())'''
address = re.sub(name.group(), '', line)
address = re.sub(',', '', address)
address = re.sub('\.', '', address)
address = re.sub(phone.group(), '', address)
'''print(address)'''

'''省市区三级xml文件解析'''

from xml.dom.minidom import parse
import xml.dom.minidom
DOMTree  = xml.dom.minidom.parse("LocList.xml")
CountryRegion = DOMTree.documentElement


'''1级省市匹配'''
province = re.search('[\u4e00-\u9fa5]{2,7}?(?:省|自治区)', address)
if (province != None):
    '''print(province.group())'''
    length = len(province.group())
    loc = address.find(province.group())
    address2 = address[loc+length:]
    province = province.group()
    '''print(address2)'''
else:
    States = CountryRegion.getElementsByTagName("State")
    for State in States:
        if State.hasAttribute("Name"):
            State_name = State.getAttribute("Name")
            province = re.search(State_name, address)
            if (province != None):
                break
    '''print(province.group())'''
    length = len(province.group())
    loc = address.find(province.group())
    address2 = address[loc + length:]
    province = province.group()
    if((province!="北京") & (province!="天津") & (province!="上海") & (province!="重庆")):
        province = province+"省"
    else:
        address2 = address
    '''print(address2)'''

'''2级市匹配'''
c_city = re.search('([\u4e00-\u9fa5]{2,7}?(?:市))', address2)
if (c_city != None):
    '''print(c_city.group())'''
    length = len(c_city.group())
    loc = address2.find(c_city.group())
    address3 = address2[loc + length:]
    c_city = c_city.group()
    '''print(address3)'''
else:
    Cities = State.getElementsByTagName("City")
    for City in Cities:
        if City.hasAttribute("Name"):
            City_name = City.getAttribute("Name")
            c_city = re.search(City_name, address2)
            if (c_city != None):
                break
    '''print(c_city.group())'''
    length = len(c_city.group())
    loc = address2.find(c_city.group())
    address3 = address2[loc + length:]
    c_city = c_city.group() + "市"
    '''print(address3)'''

'''3级市区县匹配'''
r_region = re.search('([\u4e00-\u9fa5]{2,7}?(?:市|区|县))', address3)
if (r_region != None):
    '''print(r_region.group())'''
    length = len(r_region.group())
    loc = address3.find(r_region.group())
    address4 = address3[loc + length:]
    r_region = r_region.group()
    '''print(address4)'''
else:
    r_region = ""
    address4 = address3
    '''print(address4)'''


'''4级乡镇街道匹配'''
country = re.search('([\u4e00-\u9fa5]{2,7}?(?:街道|镇|乡))', address4)
if (country != None):
    '''print(country.group())'''
    length = len(country.group())
    loc = address4.find(country.group())
    address5 = address4[loc + length:]
    country = country.group()
    '''print(address5)'''
else:
    address5 = address4
    country = ""
'''导出json格式'''
import json
result = {"姓名": name.group(), "手机": phone.group(), "地址": [province, c_city, r_region, country, address5]}
print(json.dumps(result, ensure_ascii=False, indent=4))
