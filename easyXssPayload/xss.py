# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     xss
   Description :
   Author :       CoolCat
   date：          2019/4/27
-------------------------------------------------
   Change Activity:
                   2019/4/27:
-------------------------------------------------
"""
__author__ = 'CoolCat'

import re
n = 0
for xss in open("easyXssPayload.txt"):
    n += 1
    try:
        alert = re.findall(r"alert\((.+?)\)", xss)
        print(alert[0])
        xss = xss.replace(alert[0],str(n))
        print(xss)
        f = open("neweasyXssPayload.txt","a")
        f.write(xss)
        f.close()
    except:
        pass
