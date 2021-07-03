from flask import Flask, request, render_template
from flask_cors import CORS
import city_traffic_index_mining
import utils.baidu_citycode
import utils.zh2pinying
import one_busline_detail_mining
import city_traffic_net_mining
import traver_plan
import map_line
import all_cities_index
import json

import pymysql
from flask_sqlalchemy import SQLAlchemy

import models.bus_net_model
from multiprocessing import Process

pymysql.install_as_MySQLdb()
app = Flask(__name__)
# 自动在报文头部加入相应内容
CORS(app, resources=r'/*')


class Config(object):
    """配置参数"""
    # 设置连接数据库的URL
    user = 'heyaoxin'
    password = '123456'
    database = 'course_design'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@192.168.126.132:3306/{}'.format(user, password, database)

    # 连接池
    # app.config['pool_size'] = 100
    # app.config['max_overflow'] = 0

    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 查询时会显示原始SQL语句以及mysql执行过程
    app.config['SQLALCHEMY_ECHO'] = False

    # 禁止自动提交数据处理
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False


# 读取配置
app.config.from_object(Config)

# 创建数据库sqlalchemy工具对象
db = SQLAlchemy(app)


# apis
@app.route('/trafficIndex')
def traffic_index():
    city = request.args.get("city")
    if city is not None and city != "":
        # 城市转换为城市编码
        city_code = utils.baidu_citycode.get_baidu_citycode(city)
        # 爬该城市交通数据
        detail = city_traffic_index_mining.traffic_index(city_code)
        return detail
    else:
        return "参数不符合规范，请选择查询城市"


@app.route('/buslineDetail')
def busline_detail():
    city = request.args.get("city")
    line = request.args.get("line")
    line_detail = one_busline_detail_mining.get_busline_detail(city, line)
    return line_detail


@app.route('/busNetDetail')
def busstation_detail():
    city = request.args.get('city')
    city_traffic_net_mining.traffic_net_mining(city)
    return 'ok'


@app.route('/busNetDetailSearch')
def busnet_city_search():
    city_get = request.args.get('city')
    busNet = models.bus_net_model.BusNet()
    result = busNet.search_bus_detail_all(city=city_get)
    if len(result) > 0:
        return str(result)
    else:
        # 查不到数据，创建新的进程去后台挖掘数据，然后返回信息
        p = Process(target=city_traffic_net_mining.traffic_net_mining, args=(city_get,))
        p.start()
        return '数据库暂时没有该城市数据，挖掘中。。。。。请稍后再查看'


@app.route('/routePlanBus')
def route_plan_bus():
    city = request.args.get('city')
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    res = traver_plan.bus(origin, destination, city)
    return json.dumps(res)


@app.route('/route_plan_drive')
def route_plan_drive():
    city = request.args.get('city')
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    res = traver_plan.drive(origin, destination, city)
    return json.dumps(res)
    pass


@app.route('/route_plan_walk')
def route_plan_walk():
    city = request.args.get('city')
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    res = traver_plan.walk(origin, destination, city)
    return json.dumps(res)
    pass


@app.route('/line_map')
def line_map():
    loc = request.args.get('locations')
    resp = map_line.getMap(loc)
    return resp
    pass


@app.route("/all_index")
def all_index():
    geo = all_cities_index.get_geo()
    return render_template('geo.html',
                           mygeo=geo.render_embed())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
