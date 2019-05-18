# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     main
   Description :
   Author :       CoolCat
   date：          2019/5/18
-------------------------------------------------
   Change Activity:
                   2019/5/18:
-------------------------------------------------
"""
__author__ = 'CoolCat'

import os
import re

allParams = []

def formatParams(params):
    for param in params:
        param = str(param).replace("'", "").replace("\"", "").replace("$", "").replace("\\", "").replace(" ", "")
        if param not in allParams and ":" not in param and ">" not in param and "." not in param and "[" not in param:
            allParams.append(param)
            print(param)
            f = open("paramDicts.txt", "a")
            f.write(param + "\n")
            f.close()
        else:
            pass

def getParams(filepath):
    for line in open(filepath):
        # print(line)
        getParam = re.findall(r'\$_GET\[(.*?)\]', line)
        formatParams(getParam)
        postParam = re.findall(r'\$_POST\[(.*?)\]', line)
        formatParams(postParam)
        requestParam = re.findall(r'\$_REQUEST\[(.*?)\]', line)
        formatParams(requestParam)


def getFilePath(path):
    for fpathe, dirs, paths in os.walk(path):
        for path in paths:
            filepath = os.path.join(fpathe, path)
            # print(filepath)
            try:
                if ".php" in filepath:
                    getParams(filepath)
                else:
                    pass
            except:
                pass


if __name__ == '__main__':
    try:
        getFilePath("./CMS/")
    except:
        pass
