import requests


def loc2coordinate(loc):
    url = 'https://restapi.amap.com/v3/geocode/geo?key=8935b17a6a9791ec62415e2e7a185c96&address={}'.format(loc)
    result = requests.get(url).json()
    coordinate = result['geocodes'][0]['location']
    return coordinate
