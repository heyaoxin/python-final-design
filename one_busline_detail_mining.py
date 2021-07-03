import requests
import json
import pandas as pd
from lxml import etree
import time


def get_busline_detail(city, line):
    url = "https://restapi.amap.com/v3/bus/linename?s=rsv3&extensions=all&key=afa5c6aa403924178d79dee916785b87&output=json&city={}&offset=1&keywords={}&platform=JS".format(
        city, line)
    r = requests.get(url).text
    rt = json.loads(r)
    if rt["count"] != "0":
        return rt
    else:
        return "查询不到此公交信息，请输入正确信息......"
    # try:
    #     if rt['buslines']:
    #         print('data available..')
    #         if len(rt['buslines']) == 0:  # 有名称没数据
    #             print('no data in list..')
    #         else:
    #             dt = {}
    #             dt['line_name'] = rt['buslines'][0]['name']
    #             dt['polyname'] = rt['buslines'][0]['polyline']
    #             dt['total_price'] = rt['buslines'][0]['total_price']
    #
    #             st_name = []
    #             st_coords = []
    #             for st in rt['buslines'][0]['busstops']:
    #                 st_name.append(st['name'])
    #                 st_coords.append(st['location'])
    #
    #             dt['station_name'] = st_name
    #             dt['station_coords'] = st_coords
    #             dm = pd.DataFrame([dt])
    #             # print(dm)
    #     else:
    #         pass
    # except:
    #     print('error..try it again..')
    #     time.sleep(2)
    #     get_dt(city, line)
