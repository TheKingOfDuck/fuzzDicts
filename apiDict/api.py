# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     api
   Description :
   Author :       CoolCat
   date：          2019/5/19
-------------------------------------------------
   Change Activity:
                   2019/5/19:
-------------------------------------------------
"""
__author__ = 'CoolCat'


import requests
import re
import time

allAPI = []

def getApi(res):
    apis = re.findall(r'/api(.+?)"', res.text)
    for api in apis:
        api = "/api" + str(api).replace("\\", "")

        if api not in allAPI \
                and "," not in api \
                and "'" not in api \
                and ";" not in api \
                and "," not in api \
                and "%" not in api \
                and ":" not in api \
                and "<" not in api \
                and ">" not in api \
                and "." not in api:
            allAPI.append(api)
            print(api)


            f = open("api.txt", "a")
            f.write(api + "\n")
            f.close()
        else:
            pass


def page(key,num):
    url = "https://www.zoomeye.org:443/search?q=" + key + "&p=" + str(num)
    cookies = {"__jsluid": "32acd6f720881d472a1c5ac13fe6884f",
               "Hm_lvt_3c8266fabffc08ed4774a252adcb9263": "1555850708,1555855469,1558245244,1558245346",
               "Hm_lvt_d7682ab43891c68a00de46e9ce5b76aa": "1555856656",
               "Hm_lpvt_3c8266fabffc08ed4774a252adcb9263": "1558245346"
               }
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0",
                     "Accept": "application/json, text/plain, */*",
                     "Accept-Language": "en",
                     "Accept-Encoding": "gzip, deflate",
                     "Referer": "https://www.zoomeye.org/searchResult?q=%2Fapi%2Fv1%2F",
                     "Cube-Authorization": "Your-Cube-Authorization",
                     "Connection": "close",
                     "X-Forwarded-For": "127.0.0.1",
                     "If-None-Match": "W/\"5591cbce3ac647856271ec47654da59d0fdcc1cd\""}
    return requests.get(url, headers=burp0_headers, cookies=cookies)

if __name__ == '__main__':
    key = "openapi"
    print("it's too cxk to use...")
    for num in range(1,100):
        print("=" * 20 + str(num) + "=" * 20)
        try:
            getApi(page(key, num))
            time.sleep(5)
        except:
            pass

