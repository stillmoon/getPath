import json
import urllib
from urllib import parse
import hashlib
import requests


def get_urt(address):
    # 以get请求为例http://api.map.baidu.com/geocoder/v2/?address=百度大厦&output=json&ak=yourak
    queryStr = f'/geocoding/v3/?address={address}&output=json&ak=yourak'

    # 对queryStr进行转码，safe内的保留字符不转换
    encodedStr = parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")

    # 在最后直接追加上yoursk
    rawStr = encodedStr + 'Lh3l0RW2dfyenPKKKYLQZ7VY1Hv5ng7e'

    # md5计算出的sn值7de5a22212ffaa9e326444c75a58f9a0
    # 最终合法请求url是http://api.map.baidu.com/geocoder/v2/?address=百度大厦&output=json&ak=yourak&sn=7de5a22212ffaa9e326444c75a58f9a0
    sn = hashlib.md5(parse.quote_plus(rawStr).encode('ISO-8859-1')).hexdigest()
    # 由于URL里面含有中文，所以需要用parse.quote进行处理，然后返回最终可调用的url
    url = parse.quote("http://api.map.baidu.com" + queryStr + "&sn=" + sn, safe="/:=&?#+!$,;'@()*[]")
    return url


def get_ngat(url):
    session = requests.session()
    respond = session.get(url)
    jsons = respond.json().get("result")
    return jsons


if __name__ == "__main__":
    add = input("请输入地址:")
    url = get_urt(add)
    jsons = get_ngat(url).get("location")
    lng = jsons.get("lng")
    lat = jsons.get("lat")
    print("经度：")
    print(lng)
    print("纬度：")
    print(lat)
