def get_baidu_citycode(city):
    # 从百度城市编码文件中加载城市编码，转换为dict
    citycode = {}
    f = open('utils/baidu_citycode.txt', encoding="utf-8")
    text = f.read()
    context = text.strip("").split(",")
    for c in context:
        ctx = c.split("|")
        citycode[ctx[0]] = ctx[1]
    f.close()

    # 根据传入的城市返回对应的城市编码
    code = citycode[city]
    return code
