#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
利用高德地图api实现地址和经纬度的转换
'''
import requests


def geocode(address):
    requests.adapters.DEFAULT_RETRIES = 5
    parameters = {'address': address, 'key': 'c240b697ee05e17aa1db185381eb1c41'}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters)
    answer = response.json()
    s = requests.session()
    s.keep_alive = False
    return answer['geocodes'][0]['location'];
    # print(address + "的经纬度：", answer['geocodes'][0]['location'])


def getDistance(address, destination):
    requests.adapters.DEFAULT_RETRIES = 5
    parameters = {'origins': address, 'destination': destination, 'key': 'c240b697ee05e17aa1db185381eb1c41'}
    base = 'https://restapi.amap.com/v3/distance'
    response = requests.get(base, parameters)
    answer = response.json()
    s = requests.session()
    s.keep_alive = False
    # print(answer)
    return answer['results'][0]['distance']
    # print("两地的距离：", answer['results'][0]['distance'])


if __name__ == '__main__':
    # address = input("请输入地址:")
    address = '新疆维吾尔自治区巴音郭楞蒙古自治州库尔勒市'
    destination = '甘肃省定西市岷县'
    addressCode = geocode(address)
    destinationCode = geocode(destination)
    distance = int(getDistance(addressCode, destinationCode)) // 1000
    print(distance)

    # getDistance(addressCode, destinationCode)
    # geocode(address)
    # geocode(destination)
