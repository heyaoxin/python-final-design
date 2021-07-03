from main import db
import json


# 创建数据表模型
class BusNet(db.Model):
    # 定义表名
    __tablename__ = 'bus_net'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bus_name = db.Column(db.String(64), nullable=False)
    bus_type = db.Column(db.String(64), nullable=False)
    bus_runtime = db.Column(db.String(64), nullable=False)
    bus_price = db.Column(db.String(64), nullable=False)
    bus_company = db.Column(db.String(64), nullable=False)
    bus_update = db.Column(db.String(64), nullable=False)
    route_detail = db.Column(db.String(4096), nullable=False)
    city = db.Column(db.String(8))

    # 增加记录
    def add_bus_detail(self, bus_info):
        add_info = BusNet(bus_name=bus_info['bus_name'],
                          bus_type=bus_info['bus_type'],
                          bus_runtime=bus_info['bus_runtime'],
                          bus_price=bus_info['bus_price'],
                          bus_company=bus_info['bus_company'],
                          bus_update=bus_info['bus_update'],
                          route_detail=str(bus_info['route_detail']),
                          city=str(bus_info['city']))
        db.session.add(add_info)
        db.session.commit()
        pass

    # 查询记录
    def search_bus_detail_all(self, **kwargs):
        if kwargs['city'] is not None:
            city = kwargs['city']
        bus_info = BusNet.query.filter_by(city=city).all()
        res_arr = []
        for one in bus_info:
            info = {
                'bus_name': one.bus_name,
                'bus_type': one.bus_type,
                'bus_runtime': one.bus_runtime,
                'bus_price': one.bus_price,
                'bus_company': one.bus_company,
                'bus_update': one.bus_update,
                'route_detail': one.route_detail,
                'city': one.city
            }
            res_arr.append(info)
        return json.dumps({'data': res_arr})
        pass
