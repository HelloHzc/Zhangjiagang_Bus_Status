import requests

HEADERS = {
    'User-Agent': r'%E9%98%B3%E5%85%89%E5%A5%BD%E8%BF%90/2.0.5 CFNetwork/808.2.16 Darwin/16.3.0',
    'Connection': 'keep-alive',
    'Cookie': 'JSESSIONID=04CD2BDFC1374417F24A7C8E0663B407',
    'Accept-Language': 'zh-cn',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': r'application/x-www-form-urlencoded'
}


def request_api(url, params):
    for _ in range(3):
        try:
            r = requests.get(url, params=params, headers=HEADERS)
        except (ConnectionError, requests.exceptions.Timeout) as e:
            continue
        else:
            res = eval(r.text)
            if res['status'] != 'SUCCESS':
                raise Exception('Fail to fetch', url, params)
            return res['result']
    raise e


def search_bus(bus_no):
    """
    Searching for bus.

    搜索公交线路

    Args:
        bus_no: bus number to search

    Returns:
        A list of dicts containing 'endId', 'endName', 'runPathId', 'runPathName', 'startId', 'startName'. For example:

            [{'endId': '40981036',
              'endName': '第一人民医院南门',
              'runPathId': '40983214',
              'runPathName': '11路西线',
              'startId': '40981274',
              'startName': '港城汽车站'},
             {'endId': '40981035',
              'endName': '第一人民医院南门',
              'runPathId': '40983213',
              'runPathName': '11路东线',
              'startId': '40981274',
              'startName': '港城汽车站'}]
    """
    url = r'http://61.177.44.242:8080/BusSysWebService/bus/allStationOfRPName'
    params = {'name': bus_no}
    data = request_api(url, params)
    return data['lines']


def get_line_info(path_id):
    """
    Get basic information of bus line like start time, end time, etc.

    获得公交线路的基本信息，如发车时间，末班车时间，间隔时间

    Args:
        path_id: runPathId got in search_bus(bus_no)

    Returns:
        A dict containing 'busInterval', 'endStation', 'endTime', 'endTime1', 'runFlag', 'runPathId', 'runPathName',
        'startStation', 'StartTime', 'startTime1'. For example:

        {'busInterval': '13~20',
         'endStation': '第一人民医院南门',
         'endTime': '17:40',
         'endTime1': '17:40',
         'runFlag': '0',
         'runPathId': '40983214',
         'runPathName': '11路西线',
         'startStation': '港城汽车站',
         'startTime': '06:06',
         'startTime1': '06:06'}
    """
    url = r'http://61.177.44.242:8080/BusSysWebService/common/busQuery'
    params = {'runPathId': path_id}
    data = request_api(url, params)
    return data


def get_gps_info(path_id):
    """
    Get the bus line's buses' GPS info.

    获得线路的gps信息，返回线路上车辆的所有信息

    Args:
        path_id: runPathId got in search_bus(bus_no)

    Return:
        A dict has keys of 'up_going' and 'down_going'. Each key contains a list of dicts containing 'busStationId',
        'busStationName', 'gPSTime', 'numberPlate', 'outstate', 'shangxiaxing', 'simno', 'voiceSn'. For example:

        [{'busStationId': '40982581',
          'busStationName': '万红三村',
          'gPSTime': '2017-10-19 14:36:30.0',
          'numberPlate': '苏E6M838',
          'outstate': '0',
          'shangxiaxing': '1',
          'simno': '13401473182',
          'voiceSn': '7'},
         {'busStationId': '40981274',
          'busStationName': '港城汽车站',
          'gPSTime': '2017-10-19 14:33:17.0',
          'numberPlate': '苏E6M809',
          'outstate': '1',
          'shangxiaxing': '1',
          'simno': '13401473089',
          'voiceSn': '1'}]
    """
    result = dict()
    url = r'http://61.177.44.242:8080/BusSysWebService/bus/gpsForRPF'
    result['up_going'] = request_api(url, {'rpId': path_id, 'flag': 1})['lists']
    result['down_going'] = request_api(url, {'rpId': path_id, 'flag': 3})['lists']
    return result


def get_bus_line(path_id):
    """
    Get the bus line's info.

    获取线路信息

    Args:
        path_id: runPathId got in search_bus(bus_no)

    Return:
        A dict has keys of 'up_going' and 'down_going'. Each key contains a list of dicts containing 'busStationId',
        'busStationName', 'flag', 'sn'. For example:

            {'down_going': [{'busStationId': '40981036',
               'busStationName': '第一人民医院南门',
               'flag': '2',
               'sn': '14'},
              {'busStationId': '40982361',
               'busStationName': '少年宫',
               'flag': '3',
               'sn': '15'},
              {'busStationId': '40983000',
               'busStationName': '云盘小学',
               'flag': '3',
               'sn': '16'}],
             'up_going': [{'busStationId': '40981274',
               'busStationName': '港城汽车站',
               'flag': '0',
               'sn': '1'},
              {'busStationId': '40981377',
               'busStationName': '国际购物中心',
               'flag': '1',
               'sn': '2'},
              {'busStationId': '40983143',
               'busStationName': '朱港巷路',
               'flag': '1',
               'sn': '3'}]}
    """
    url = r'http://61.177.44.242:8080/BusSysWebService/bus/searchSSR'
    params = {'rpId': path_id}
    data = request_api(url, params)
    result = dict()
    result['up_going'] = data['shangxing']
    result['down_going'] = data['xiaxing']
    return result


def main():
    bus_no = input('请输入您想查询的公交线路：')
    path_list = search_bus(bus_no)
    cnt = 1
    for items in path_list:
        print('\033[32m{}.\t{}\033[0m'.format(cnt, items['runPathName']))
        print('\t首发站：' + items['startName'])
        print('\t终点站：' + items['endName'])
        cnt += 1
    chosen_item = input('请输入您要查询的编号：')
    path_id = path_list[int(chosen_item) - 1]['runPathId']
    line_info = get_line_info(path_id)
    print('\033[32m{}\033[0m'.format(line_info['runPathName']))
    print('首发站：{}\t\t终点站：{}'.format(line_info['startStation'], line_info['endStation']))
    print('首发时间：{}\t\t末班时间：{}'.format(line_info['startTime'], line_info['endTime']))
    print('发车间隔:{}分钟'.format(line_info['busInterval']))
    bus_line = get_bus_line(path_id)
    gps_info = get_gps_info(path_id)
    up_going = bus_line['up_going']
    down_going = bus_line['down_going']
    up_going_gps = gps_info['up_going']
    down_going_gps = gps_info['down_going']
    flag = False
    gps_flag = False
    print('\033[32m-----上行路线-----\033[0m')
    for items in up_going:
        if flag:
            print('---', end='')
        flag = True
        for gps_items in up_going_gps:
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
    for items in down_going:
        if flag:
            print('---', end='')
        flag = True
        for gps_items in down_going_gps:
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
    info = input('输入i获得更多信息，输入其他退出')
    if info == 'i':
        for gps_items in up_going_gps, down_going_gps:
            for gps_item in gps_items:
                print('\033[32m车载sim卡号\033[0m：\t{}'.format(gps_item['simno']))
                print('\033[32m是否出站\033[0m：\t{}'.format(('是' if gps_item['outstate'] == '1' else '否')))
                print('\033[32m站点名称\033[0m：\t{}'.format(gps_item['busStationName']))
                print('\033[32mGPS时间\033[0m：\t{}'.format(gps_item['gPSTime']))
                print('\033[32m上下行\033[0m：\t\t{}'.format(('上行' if gps_item['shangxiaxing'] == '1' else '下行')))
                print('\033[32m车牌号\033[0m：\t\t{}'.format(gps_item['numberPlate']))
                print()


if __name__ == '__main__':
    main()