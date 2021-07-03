import requests
from bs4 import BeautifulSoup
import models.bus_net_model as bnm
import utils.zh2pinying
from concurrent.futures import ProcessPoolExecutor

# 创建进程池
pool = ProcessPoolExecutor(max_workers=4)


# 最终页面收集公交线路信息
def get_final_detail(url, city):
    final_page = requests.get(url).text
    final_page_soup = BeautifulSoup(final_page, 'lxml')

    # 获取公交详细信息
    title = final_page_soup.find('div', class_='info').find('h1').get_text()
    bus_name = str(title).split('[')[0]  # 广州1路公交车路线
    bus_type = str(title).split('[')[1].split(']')[0]  # 市区编码线路
    detail = final_page_soup.find('div', class_='info').find('ul').find_all('li')
    bus_runtime = detail[0].get_text()  # 运行时间：东山总站(署前路) 06:00--22:30|芳村花园南门总站 06:00--22:30
    bus_price = detail[1].get_text()  # 参考票价：票价2元
    bus_company = detail[2].get_text()  # 公交公司：第一巴士
    bus_update = detail[3].get_text().split('免')[0]  # 最后更新：2021-03-06

    # 获取公交站点信息
    line = final_page_soup.find_all('div', class_='trip')
    bus_station = final_page_soup.find_all('div', class_='bus-lzlist mb15')
    index = 0
    route_detail = {}
    for l in line:
        # 线路名
        line_name = l.get_text()
        # 途径站点
        station_name_list = bus_station[index].find_all('li')
        line_arrive = ''
        for one in station_name_list:
            station = one.get_text()
            line_arrive += "->" + str(station)
        index += 1
        route_detail[line_name] = line_arrive

    bus_info = {
        'bus_name': bus_name,
        'bus_type': bus_type,
        'bus_runtime': bus_runtime,
        'bus_price': bus_price,
        'bus_company': bus_company,
        'bus_update': bus_update,
        'route_detail': route_detail,
        'city': city
    }
    # model实例化
    busnet_db_model = bnm.BusNet()
    # 存库操作
    busnet_db_model.add_bus_detail(bus_info=bus_info)
    pass


# 获取list、line等等的最终url
def get_final_url(url, source_url, city):
    # 分别去请求对应的url 获取公交信息
    type_page = requests.get(url).text
    type_page_soup = BeautifulSoup(type_page, 'lxml')
    try:
        all_line = type_page_soup.find('div', class_="list clearfix").find_all('a')
        # 找到list、line对应的url
        for one in all_line:
            num_and_line_url = one['href']
            final_url = source_url + num_and_line_url
            # get_final_detail(final_url, city)
            pool.submit(get_final_detail, final_url, city)
    except:
        pass


def traffic_net_mining(city):
    city_pinying = utils.zh2pinying.Zh2pinying(city)
    main_url = "https://{}.8684.cn/".format(city_pinying)
    # 进入主页
    main_page = requests.get(main_url).text
    # 爬取以数字开头列表 <a href="/list1">1</a>
    soup = BeautifulSoup(main_page, 'lxml')
    all_type = soup.find('div', class_='bus-layer depth w120').find_all('a')

    # 遍历所有线路类别，找出其对应的url后缀,补全所有url
    for one in all_type:
        rest_url = one['href']
        if main_url in rest_url:
            # 这一类是已经有最终需要获取信息的页面的url的，直接请求去获取信息
            full_url = rest_url
            # get_final_detail(full_url, city)
            try:
                pool.submit(get_final_detail, full_url, city)
            except:
                pass
        else:
            # 这一类是最终页面url还没获取到，需要在请求一遍后的页面才有
            full_url = main_url + rest_url
            get_final_url(full_url, main_url, city)
    pass
