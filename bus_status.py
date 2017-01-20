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
    'Content-Length': '7',
    'Content-Type': r'application/x-www-form-urlencoded'
}

def post_data_to_server(url_to_post, content_to_post):
    """
    输入发送POST的URL和内容，返回结果，类型为dict
    """
    data = urllib.parse.urlencode(content_to_post)
    binary_data = data.encode(encoding='utf_8')
    req = urllib.request.Request(url_to_post, binary_data, HEADERS)
    response = urllib.request.urlopen(req)
    the_page = response.read()
    response_data = json.loads(the_page.decode("utf8"))
    return response_data


def search_bus(bus_to_search):
    """
    搜索公交车，打印搜索列表
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
