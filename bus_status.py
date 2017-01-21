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
        print('\033[32m'+str(cnt)+'.  '+items['runPathName']+'\033[0m')
        print("    首发站："+items['startName'])
        print("    终点站："+items['endName'])
        cnt += 1
    chosen_item = input("请输入您要查询的编号：")
    return lines[int(chosen_item)-1]['runPathId']

def bus_query(path_id_to_query):
    """
    打印公交车的基本信息，如发车时间，末班车时间，间隔时间
    """
    url = r"http://61.177.44.242:8080/BusSysWebService/common/busQuery"
    content_to_post = {'runPathId': path_id_to_query}
    data = post_data_to_server(url, content_to_post)
    items = data['result']
    print('\033[32m'+items['runPathName']+'\033[0m'+"    发车间隔:"+items['busInterval']+"分钟")
    print("首发站："+items['startStation']+"    终点站："+items['endStation'])
    print("首发时间："+items['startTime']+"    末班时间："+items['endTime'])
    # if items['runFlag'] == '1':
    #     print("正在运营中")
    # else:
    #     print("休息中")

def get_gps_info(path_id_to_query, flag):
    """
    获得线路的gps信息，返回线路上车辆的所有信息，类型为list
    当 flag == 1 时为查询上行信息，flag == 3 时查询下行信息
    """
    url = r"http://61.177.44.242:8080/BusSysWebService/bus/gpsForRPF"
    content_to_post = {'rpId': path_id_to_query, 'flag': flag}
    data = post_data_to_server(url, content_to_post)
    return data['result']['lists']

def get_bus_line(path_id_to_query):
    """
    获得线路的信息，包括线路上的公交信息，无返回值
    """
    url = r"http://61.177.44.242:8080/BusSysWebService/bus/searchSSR"
    content_to_post = {'rpId': path_id_to_query}
    data = post_data_to_server(url, content_to_post)
    shangxing = data['result']['shangxing']
    xiaxing = data['result']['xiaxing']
    shangxing_gps = get_gps_info(path_id_to_query, 1)
    xiaxing_gps = get_gps_info(path_id_to_query, 3)
    flag = False
    gps_flag = False
    print('\033[32m-----上行路线-----\033[0m')
    for items in shangxing:
        if flag:
            print('---', end='')
        flag = True
        for gps_items in shangxing_gps:
            if gps_items['busStationId'] == items['busStationId']:
                gps_flag = True
                out_state = gps_items['outstate']
        if gps_flag:
            if out_state == '1':
                print('\033[32m', end='')
            else:
                print('\033[31m', end='')
        print(items['busStationName'], end='')
        if gps_flag:
            print('\033[0m', end='')
            gps_flag = False
    print()

    flag = False
    print('\033[32m-----下行路线-----\033[0m')
    for items in xiaxing:
        if flag:
            print('---', end='')
        flag = True
        for gps_items in xiaxing_gps:
            if gps_items['busStationId'] == items['busStationId']:
                gps_flag = True
                out_state = gps_items['outstate']
        if gps_flag:
            if out_state == '1':
                print('\033[32m', end='')
            else:
                print('\033[31m', end='')
        print(items['busStationName'], end='')
        if gps_flag:
            print('\033[0m', end='')
            gps_flag = False
    print()
    print('\033[32m绿色\033[0m代表已出站，\033[31m红色\033[0m代表未出站')
    info = input("输入i获得更多信息，输入其他退出")
    if info == 'i':
        for gps_items in shangxing_gps:
            print("\033[32m车载sim卡号\033[0m：\t"+gps_items['simno'])
            print("\033[32m是否出站\033[0m：\t"+('是' if gps_items['outstate']=='1' else '否'))
            print("\033[32m站点名称\033[0m：\t"+gps_items['busStationName'])
            print("\033[32mGPS时间\033[0m：\t"+gps_items['gPSTime'])
            print("\033[32m上下行\033[0m：\t"+('上行' if gps_items['shangxiaxing']=='1' else '下行'))
            print("\033[32m车牌号\033[0m：\t"+gps_items['numberPlate'])
            print()
        for gps_items in xiaxing_gps:
            print("\033[32m车载sim卡号\033[0m：\t"+gps_items['simno'])
            print("\033[32m是否出站\033[0m：\t"+('是' if gps_items['outstate']=='1' else '否'))
            print("\033[32m站点名称\033[0m：\t"+gps_items['busStationName'])
            print("\033[32mGPS时间\033[0m：\t"+gps_items['gPSTime'])
            print("\033[32m上下行\033[0m：\t"+('上行' if gps_items['shangxiaxing']=='1' else '下行'))
            print("\033[32m车牌号\033[0m：\t"+gps_items['numberPlate'])
            print()
    else:
        exit()

def main():
    BUSNO = input("请输入您想查询的公交线路：")
    path_id = search_bus(BUSNO)
    bus_query(path_id)
    get_bus_line(path_id)

main()