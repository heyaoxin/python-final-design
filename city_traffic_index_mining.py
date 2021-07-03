import requests
import re
import json


def get_page(url):
    try:
        response = requests.get(url)
        if response.content:  # 返回成功
            return response
    except requests.ConnectionError as e:
        print('url出错', e.args)


def write_to_file(content):
    with open('traffic_index.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        # f.close()


# 获取实时拥堵指数内容
def get_detail(page):
    transformData = json.loads(re.findall(r'[(](.*?)[)]', page.text)[0])
    detail = transformData['data']['detail']
    return detail


# 获取实时拥堵指数变化内容
def get_curve(page):
    transformData = json.loads(re.findall(r'[(](.*?)[)]', page.text)[0])
    curve_detail = transformData['data']['list']
    # k = 0
    # for roadrank_list in curve_detail:
    #     # print('---------------分割线---------------')
    #     # print(k)
    #     write_to_file(str(k) + str(roadrank_list))
    #     k += 1
    #     # print(roadrank_list)
    return curve_detail


# 获取实时道路拥堵指数内容
def get_road(page):
    transformData = json.loads(re.findall(r'[(](.*?)[)]', page.text)[0])
    detail = transformData['data']['detail']
    # for i in detail:
    #     write_to_file(str(i) + '：' + str(detail[i]))
    #     # print(str(i) + '：' + str(detail[i]))
    return detail


# 获取实时拥堵里程内容
def get_congestmile(page):
    transformData = json.loads(re.findall(r'[(](.*?)[)]', page.text)[0])
    congest = transformData['data']['congest']
    # for i in congest:
    #     write_to_file(str(i) + '：' + str(congest[i]))
    #     # print(str(i) + '：' + str(congest[i]))
    return congest


# 获取昨日早晚高峰内容
def get_peakCongest(page):
    transformData = json.loads(re.findall(r'[(](.*?)[)]', page.text)[0])
    peak_detail = transformData['data']['peak_detail']
    # for i in peak_detail:
    #     write_to_file(str(i) + '：' + str(peak_detail[i]))
    #     # print(str(i) + '：' + str(peak_detail[i]))
    return peak_detail


# 获取全部道路拥堵情况
def get_roadrank(page):
    transformData = json.loads(re.findall(r'[(](.*?)[)]', page.text)[0])
    roadrank_detail = transformData['data']['list']
    # for roadrank_list in roadrank_detail:
    #     write_to_file('---------------分割线---------------')
    #     # print('---------------分割线---------------')
    #     for element in roadrank_list:
    #         if str(element) != 'links' and str(element) != 'nameadd':
    #             write_to_file(str(element) + ':' + str(roadrank_list[element]))
    #             # print(str(element) + ':' + str(roadrank_list[element]))
    return roadrank_detail


def traffic_index(city_code):
    city_code = str(city_code)
    # 实时拥堵指数内容api
    url_detail = "https://jiaotong.baidu.com/trafficindex/city/details?cityCode=" + city_code + "&callback=jsonp_1570959868686_520859"
    # 实时拥堵指数变化内容api
    url_curve = "https://jiaotong.baidu.com/trafficindex/city/curve?cityCode=" + city_code + "&type=minute&callback=jsonp_1571018819971_8078256"
    # 实时道路拥堵指数内容api
    url_road = "https://jiaotong.baidu.com/trafficindex/city/road?cityCode=" + city_code + "&callback=jsonp_1571014746541_9598712"
    # 实时拥堵里程内容api
    url_congestmile = "https://jiaotong.baidu.com/trafficindex/city/congestmile?cityCode=" + city_code + "&callback=jsonp_1571014746542_5952586"
    # 昨日早晚高峰内容api
    url_peakCongest = "https://jiaotong.baidu.com/trafficindex/city/peakCongest?cityCode=" + city_code + "&callback=jsonp_1571014746543_3489265"
    # 全部道路拥堵情况api
    url_roadrank = "https://jiaotong.baidu.com/trafficindex/city/roadrank?cityCode=" + city_code + "&roadtype=0&callback=jsonp_1571016737139_1914397"
    # 高速/快速路拥堵情况api
    url_highroadrank = "https://jiaotong.baidu.com/trafficindex/city/roadrank?cityCode=" + city_code + "&roadtype=1&callback=jsonp_1571018628002_9539211"

    # 获取实时拥堵指数内容
    congest_index_now = get_detail(get_page(url_detail))

    # 获取实时拥堵指数变化内容
    congest_index_change = get_curve(get_page(url_curve))

    # 获取实时道路拥堵指数内容
    congest_road_index_now = get_road(get_page(url_road))

    # 获取实时拥堵里程内容
    congest_mile_now = get_congestmile(get_page(url_congestmile))

    # 获取昨日早晚高峰内容
    congest_peak = get_peakCongest(get_page(url_peakCongest))

    # 获取全部道路拥堵情况
    congest_allroad = get_roadrank(get_page(url_roadrank))

    # 获取高速/快速路拥堵情况
    congest_highroad = get_roadrank(get_page(url_highroadrank))

    all_detail = {
        "实时拥堵指数内容": congest_index_now,
        "实时拥堵指数变化": congest_index_change,
        "实时道路拥堵指数": congest_road_index_now,
        "实时拥堵里程": congest_mile_now,
        "昨日早晚高峰": congest_peak,
        "全部道路拥堵情况": congest_allroad,
        "高速/快速路拥堵情况": congest_highroad
    }
    return all_detail
