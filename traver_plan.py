import requests
import utils.loc2coordinate as l2c


def walk(origin, destination, city):
    origin = l2c.loc2coordinate(city + origin)
    destination = l2c.loc2coordinate(city + destination)
    url = 'https://restapi.amap.com/v3/direction/walking?key=8935b17a6a9791ec62415e2e7a185c96&origin={}&destination={}'.format(
        origin, destination)
    result = requests.get(url).json()
    # 起点终点距离（米）
    distance = result['route']['paths'][0]['distance']
    # 预计花费时间（秒）
    duration = result['route']['paths'][0]['duration']
    duration = round(int(duration) / 60, 1)
    steps = result['route']['paths'][0]['steps']
    route_plan = []
    for step in steps:
        route_plan.append(step['instruction'])
    res = {
        'type': 'walk',
        'distance': str(distance) + '米',
        'duration': str(duration) + '分钟',
        'route_plan': '->'.join(route_plan)
    }
    return res


def drive(origin, destination, city):
    origin = l2c.loc2coordinate(city + origin)
    destination = l2c.loc2coordinate(city + destination)
    url = 'https://restapi.amap.com/v3/direction/driving?origin={}&destination={}&extensions=json&key=8935b17a6a9791ec62415e2e7a185c96'.format(
        origin, destination)
    result = requests.get(url).json()
    # 起点终点距离（米）
    distance = result['route']['paths'][0]['distance']
    # 车费
    taxi_cost = result['route']['taxi_cost']
    # 预计花费时间（秒）
    duration = result['route']['paths'][0]['duration']
    duration = round(int(duration) / 60, 1)
    steps = result['route']['paths'][0]['steps']
    route_plan = []
    for step in steps:
        route_plan.append(step['instruction'])
    res = {
        'type': 'drive',
        'distance': str(distance) + '米',
        'duration': str(duration) + '分钟',
        'taxi_cost': str(taxi_cost) + '元',
        'route_plan': '->'.join(route_plan)
    }
    return res


def bus(origin, destination, city):
    origin = l2c.loc2coordinate(city + origin)
    destination = l2c.loc2coordinate(city + destination)
    url = 'https://restapi.amap.com/v3/direction/transit/integrated?key=8935b17a6a9791ec62415e2e7a185c96&origin={}&destination={}&city={}'.format(
        origin, destination, city)
    result = requests.get(url).json()
    transits = result['route']['transits']
    res = []
    for transit in transits:
        segments = transit['segments']
        for segment in segments:
            buslines = segment['bus']['buslines']
            if len(buslines) > 0:
                # 公交线路
                name = buslines[0]['name']
                # 上车站点
                departure_stop_name = buslines[0]['departure_stop']['name']
                # 下车站点
                arrival_stop_name = buslines[0]['arrival_stop']['name']
                # 途径站点
                via_stops = buslines[0]['via_stops']
                stops = []
                for via_stop in via_stops:
                    stops.append(via_stop['name'])
                pass_stops = '->'.join(stops)
                res.append({
                    'name': name,
                    'departure_stop_name': departure_stop_name,
                    'arrival_stop_name': arrival_stop_name,
                    'pass_stops': pass_stops
                })
    return res
