import re
import json
import random
import requests

import core.config
from core.colors import bad

def log(data, mode='', show=False):
    suffix = '\n'
    if mode == 'run':
        suffix = '\r'
    if not core.config.globalVariables['url_file']:
        print (data, end=suffix)
    else:
        if show:
            print (data, end=suffix)

def extractHeaders(headers):
    headers = headers.replace('\\n', '\n')
    sorted_headers = {}
    matches = re.findall(r'(.*):\s(.*)', headers)
    for match in matches:
        header = match[0]
        value = match[1]
        try:
            if value[-1] == ',':
                value = value[:-1]
            sorted_headers[header] = value
        except IndexError:
            pass
    return sorted_headers

def unityExtracter(arrayOfArrays, usable):
    "extracts the value from single valued list from a list of lists"
    remainingArray = []
    for array in arrayOfArrays:
        if len(array) == 1:
            usable.append(array[0])
        else:
            remainingArray.append(array)
    return remainingArray

def slicer(array, n=2):
    "divides a list into n parts"
    k, m = divmod(len(array), n)
    return list(array[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

def joiner(array, include):
    "converts a list of parameters into parameter and value pair"
    params = {}
    for element in array:
        params[element] = randomString(6)
    params.update(include)
    return params

def stabilize(url):
    "picks up the best suiting protocol if not present already"
    if 'http' not in url:
        try:
            requests.get('http://%s' % url) # Makes request to the target with http schema
            url = 'http://%s' % url
        except: # if it fails, maybe the target uses https schema
            url = 'https://%s' % url

    try:
        requests.get(url) # Makes request to the target
    except Exception as e: # if it fails, the target is unreachable
        if 'ssl' in str(e).lower():
            pass
        else:
            print ('%s Unable to connect to the target.' % bad)
            quit()
    return url

def removeTags(html):
    "removes all the html from a webpage source"
    return re.sub(r'(?s)<.*?>', '', html)

def lineComparer(response1, response2):
    "compares two webpage and finds the non-matching lines"
    response1 = response1.split('\n')
    response2 = response2.split('\n')
    num = 0
    dynamicLines = []
    for line1, line2 in zip(response1, response2):
        if line1 != line2:
            dynamicLines.append(num)
        num += 1
    return dynamicLines

def randomString(n):
    "generates a random string of length n"
    return ''.join(str(random.choice(range(10))) for i in range(n))

def e(string):
    "utf encodes a string"
    return string.encode('utf-8')

def d(string):
    "utf decodes a string"
    return string.decode('utf-8')

def flattenParams(params):
    flatted = []
    for name, value in params.items():
        flatted.append(name + '=' + value)
    return '?' + '&'.join(flatted)

def getParams(data):
    params = {}
    try:
        params = json.loads(str(data).replace('\'', '"'))
        return params
    except json.decoder.JSONDecodeError:
        if data.startswith('?'):
            data = data[1:]
        parts = data.split('&')
        for part in parts:
            each = part.split('=')
            try:
                params[each[0]] = each[1]
            except IndexError:
                params = None
    return params
