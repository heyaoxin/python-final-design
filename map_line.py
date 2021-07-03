import requests


def getMap(locations):
    url = "https://restapi.amap.com/v3/staticmap?zoom=12&size=5000*3000&paths=5,0x0000ff,1,,:{}&key=8935b17a6a9791ec62415e2e7a185c96".format(
        locations)
    # 字节流
    resp_byte = requests.get(url).content
    return resp_byte
