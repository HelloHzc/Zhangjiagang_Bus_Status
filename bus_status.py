#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.parse
import urllib.request
import json

HEADERS = {
    'User-Agent': r'%E9%98%B3%E5%85%89%E5%A5%BD%E8%BF%90/2.0.5 CFNetwork/808.2.16 Darwin/16.3.0',
    'Connection': 'keep-alive',
    'Cookie': 'JSESSIONID=04CD2BDFC1374417F24A7C8E0663B407',
    'Accept-Language': 'zh-cn',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': r'application/x-www-form-urlencoded'
}

def post_data_to_server(url_to_post, content_to_post):
    """
    输入发送POST的URL和内容，返回结果，类型为dict
    """
    data = urllib.parse.urlencode(content_to_post)
    binary_data = data.encode(encoding='utf_8')
    HEADERS['Content-Length'] = str(len(data))
    req = urllib.request.Request(url_to_post, binary_data, HEADERS)
    response = urllib.request.urlopen(req)
    the_page = response.read()
    response_data = json.loads(the_page.decode("utf8"))
    return response_data

def bus_query(path_id_to_query):
    """
    打印公交车的基本信息，如发车时间，末班车时间，间隔时间
    """
    url = r"http://61.177.44.242:8080/BusSysWebService/common/busQuery"
    content_to_post = {'runPathId': path_id_to_query}

    data = post_data_to_server(url, content_to_post)
    items = data['result']
    print(items['runPathName']+"    发车间隔:"+items['busInterval']+"分钟")
    print("首发站："+items['startStation']+"    终点站："+items['endStation'])
    print("首发时间："+items['startTime']+"    末班时间："+items['endTime'])
    if items['runFlag'] == '1':
        print("正在运营中")
    else:
        print("休息中")


def search_bus(bus_to_search):
    """
    搜索公交车，打印搜索列表，返回Path_ID，类型为str
    """
    url = r"http://61.177.44.242:8080/BusSysWebService/bus/allStationOfRPName"
    content_to_post = {'name': bus_to_search}
    data = post_data_to_server(url, content_to_post)
    lines = data['result']['lines']
    cnt = 1
    for items in lines:
        print(str(cnt)+'.  '+items['runPathName'])
        print("    首发站："+items['startName'])
        print("    终点站："+items['endName'])
        cnt += 1
    chosen_item = input("请输入您要查询的编号：")
    return lines[int(chosen_item)-1]['runPathId']

BUSNO = input("请输入您想查询的公交线路：")
path_id = search_bus(BUSNO)
bus_query(path_id)
