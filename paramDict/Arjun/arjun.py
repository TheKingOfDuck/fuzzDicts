#!/usr/bin/env python3

from __future__ import print_function

from core.colors import red, green, white, end, info, bad, good, run

print('''%s    _         
   /_| _ '    
  (  |/ /(//) %sv1.5%s
      _/      %s
''' % (green, white, green, end))

try:
    import concurrent.futures
except ImportError:
    print ('%s Please use Python > 3.2 to run Arjun.' % bad)
    quit()

import re
import sys
import json
import requests
import argparse

from urllib.parse import unquote

import core.config
from core.prompt import prompt
from core.requester import requester
from core.utils import e, d, stabilize, randomString, slicer, joiner, unityExtracter, getParams, flattenParams, removeTags, extractHeaders, log

parser = argparse.ArgumentParser() #defines the parser
#Arguements that can be supplied
parser.add_argument('-u', help='target url', dest='url')
parser.add_argument('-f', help='wordlist path', dest='wordlist')
parser.add_argument('-d', help='request delay', dest='delay', type=int)
parser.add_argument('-t', help='number of threads', dest='threads', type=int)
parser.add_argument('-o', help='path for the output file', dest='output_file')
parser.add_argument('--urls', help='file containing urls', dest='url_file')
parser.add_argument('--get', help='use get method', dest='GET', action='store_true')
parser.add_argument('--post', help='use post method', dest='POST', action='store_true')
parser.add_argument('--include', help='include this data in every request', dest='include')
parser.add_argument('--headers', help='add headers', dest='headers', nargs='?', const=True)
parser.add_argument('--json', help='treat post data as json', dest='jsonData', action='store_true')
args = parser.parse_args() #arguments to be parsed

url = args.url
jsonData = args.jsonData
headers = args.headers
delay = args.delay or 0
url_file = args.url_file
include = args.include or {}
threadCount = args.threads or 2
wordlist = args.wordlist or './db/params.txt'

core.config.globalVariables = vars(args)

if type(headers) == bool:
    headers = extractHeaders(prompt())
elif type(headers) == str:
    headers = extractHeaders(headers)
else:
    headers = {}

if jsonData:
    headers['Content-type'] = 'application/json'

if args.GET:
    GET = True
else:
    GET = False

include = getParams(include)

paramList = []
try:
    with open(wordlist, 'r') as file:
        for line in file:
            paramList.append(line.strip('\n'))
except FileNotFoundError:
    log('%s The specified file for parameters doesn\'t exist' % bad)
    quit()

urls = []

if url_file:
    try:
        with open(url_file, 'r') as file:
            for line in file:
                urls.append(line.strip('\n'))
    except FileNotFoundError:
        log('%s The specified file for URLs doesn\'t exist' % bad)
        quit()

if not url and not url_file:
    log('%s No URL specified.' % bad)
    quit()

def heuristic(response, paramList):
    done = []
    forms = re.findall(r'(?i)(?s)<form.*?</form.*?>', response)
    for form in forms:
        method = re.search(r'(?i)method=[\'"](.*?)[\'"]', form)
        inputs = re.findall(r'(?i)(?s)<input.*?>', response)
        for inp in inputs:
            inpName = re.search(r'(?i)name=[\'"](.*?)[\'"]', inp)
            if inpName:
                inpType = re.search(r'(?i)type=[\'"](.*?)[\'"]', inp)
                inpValue = re.search(r'(?i)value=[\'"](.*?)[\'"]', inp)
                inpName = d(e(inpName.group(1)))
                if inpName not in done:
                    if inpName in paramList:
                        paramList.remove(inpName)
                    done.append(inpName)
                    paramList.insert(0, inpName)
                    log('%s Heuristic found a potential parameter: %s%s%s' % (good, green, inpName, end))
                    log('%s Prioritizing it' % good)

def quickBruter(params, originalResponse, originalCode, reflections, factors, include, delay, headers, url, GET):
    joined = joiner(params, include)
    newResponse = requester(url, joined, headers, GET, delay)
    if newResponse.status_code == 429:
        print ('%s Target has rate limiting in place, please use -t 2 -d 5.' % bad)
        raise ConnectionError
    if newResponse.status_code != originalCode:
        return params
    elif factors['sameHTML'] and len(newResponse.text) != (len(originalResponse)):
        return params
    elif factors['samePlainText'] and len(removeTags(originalResponse)) != len(removeTags(newResponse.text)):
        return params
    elif True:
        for param, value in joined.items():
            if param not in include and newResponse.text.count(value) != reflections:
                return params
    else:
        return False

def bruter(param, originalResponse, originalCode, factors, include, reflections, delay, headers, url, GET): 
    fuzz = randomString(6)
    data = {param : fuzz}
    data.update(include)
    response = requester(url, data, headers, GET, delay)
    newReflections = response.text.count(fuzz)
    reason = False
    if response.status_code != originalCode:
        reason = 'Different response code'
    elif reflections != newReflections:
        reason = 'Different number of reflections'
    elif factors['sameHTML'] and len(response.text) != (len(originalResponse)):
        reason = 'Different content length'
    elif factors['samePlainText'] and len(removeTags(response.text)) != (len(removeTags(originalResponse))):
        reason = 'Different plain-text content length'
    if reason:
        return {param : reason}
    else:
        return None

def narrower(oldParamList, url, include, headers, GET, delay, originalResponse, originalCode, reflections, factors, threadCount):
    newParamList = []
    threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=threadCount)
    futures = (threadpool.submit(quickBruter, part, originalResponse, originalCode, reflections, factors, include, delay, headers, url, GET) for part in oldParamList)
    for i, result in enumerate(concurrent.futures.as_completed(futures)):
        if result.result():
            newParamList.extend(slicer(result.result()))
        log('%s Processing: %i/%-6i' % (info, i + 1, len(oldParamList)), mode='run')
    return newParamList

def initialize(url, include, headers, GET, delay, paramList, threadCount):
    url = stabilize(url)

    log('%s Analysing the content of the webpage' % run)
    firstResponse = requester(url, include, headers, GET, delay)

    log('%s Analysing behaviour for a non-existent parameter' % run)

    originalFuzz = randomString(6)
    data = {originalFuzz : originalFuzz[::-1]}
    data.update(include)
    response = requester(url, data, headers, GET, delay)
    reflections = response.text.count(originalFuzz[::-1])
    log('%s Reflections: %s%i%s' % (info, green, reflections, end))

    originalResponse = response.text
    originalCode = response.status_code
    log('%s Response Code: %s%i%s' % (info, green, originalCode, end))

    newLength = len(response.text)
    plainText = removeTags(originalResponse)
    plainTextLength = len(plainText)
    log('%s Content Length: %s%i%s' % (info, green, newLength, end))
    log('%s Plain-text Length: %s%i%s' % (info, green, plainTextLength, end))

    factors = {'sameHTML': False, 'samePlainText': False}
    if len(firstResponse.text) == len(originalResponse):
        factors['sameHTML'] = True
    elif len(removeTags(firstResponse.text)) == len(plainText):
        factors['samePlainText'] = True

    log('%s Parsing webpage for potential parameters' % run)
    heuristic(firstResponse.text, paramList)

    fuzz = randomString(8)
    data = {fuzz : fuzz[::-1]}
    data.update(include)

    log('%s Performing heuristic level checks' % run)

    toBeChecked = slicer(paramList, 50)
    foundParams = []
    while True:
        try:
            toBeChecked = narrower(toBeChecked, url, include, headers, GET, delay, originalResponse, originalCode, reflections, factors, threadCount)
            toBeChecked = unityExtracter(toBeChecked, foundParams)
            if not toBeChecked:
                break
        except:
            raise ConnectionError

    if foundParams:
        log('%s Heuristic found %i potential parameters.' % (info, len(foundParams)))
        paramList = foundParams

    currentResult = []
    returnResult = []

    threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=threadCount)
    futures = (threadpool.submit(bruter, param, originalResponse, originalCode, factors, include, reflections, delay, headers, url, GET) for param in foundParams)
    for i, result in enumerate(concurrent.futures.as_completed(futures)):
        if result.result():
            currentResult.append(result.result())
        log('%s Progress: %i/%i' % (info, i + 1, len(paramList)), mode='run')

    log('%s Scan Completed    ' % info)

    for each in currentResult:
        for param, reason in each.items():
            log('%s Valid parameter found: %s%s%s' % (good, green, param, end))
            log('%s Reason: %s' % (info, reason))
            returnResult.append({"param": param, "reason": reason})
    if not returnResult:
        log('%s Unable to verify existence of parameters detected by heuristic' % bad)
    return returnResult

finalResult = {}
if url:
    finalResult[url] = []
    try:
        finalResult[url] = initialize(url, include, headers, GET, delay, paramList, threadCount)
    except ConnectionError:
        print ('%s Target is refusing connections. Consider using -d 5 -t 1.' % bad)
        quit()
elif urls:
    for url in urls:
        finalResult[url] = []
        print('%s Scanning: %s' % (run, url))
        try:
            finalResult[url] = initialize(url, include, headers, GET, delay, list(paramList), threadCount)
            if finalResult[url]:
                print('%s Parameters found: %s' % (good, ', '.join([each['param'] for each in finalResult[url]])))
        except ConnectionError:
            print ('%s Target is refusing connections. Consider using -d 5 -t 1.' % bad)
            pass

# Finally, export to json
if args.output_file and finalResult:
    log('%s Saving output to JSON file in %s' % (info, args.output_file))
    with open(str(args.output_file), 'w+') as json_output:
        json.dump(finalResult, json_output, sort_keys=True, indent=4)
