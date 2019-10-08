#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : me7dog7
import requests
import urlparse
import thread
import time
import Queue
import sys

targetList = Queue.Queue()
targetListCount = 0
progressLock = thread.allocate()
lenUrl = {}


class fuzz():
    def __init__(self, target, lenUrl, timeOut,  targetList):
        self.target = target
        self.targetList = targetList
        self.start(lenUrl, timeOut)

    def start(self, lenUrl, timeOut=10):
        try:
            urlData = None
            if self.target['method'] == 'GET':
                if self.target.has_key('cookie'):
                    urlData = requests.get(url=self.target['url'], timeout=timeOut, cookies=self.target['cookie'])
                else:
                    urlData = requests.get(url=self.target['url'], timeout=timeOut)
            if self.target['method'] == 'POST':
                urlData = requests.post(url=self.target['url'], data=self.target['data'], timeout=timeOut)
            if urlData.status_code == 200:
                if len(urlData.text) != lenUrl['normalUrl'] and len(urlData.text) != lenUrl['url404'] and len(urlData.text) != lenUrl['homeUrl'] and len(urlData.text) != lenUrl['postUrl']:
                    with open('fuzz.txt', mode='a') as filename:
                        filename.write('url : {} , method : {} , data : {}'.format(self.target['url'], self.target['method'], self.target['data']))
                        filename.write('\n')
                    return True
            elif urlData.status_code == 503:
                self.targetList.put(self.target)
        except Exception, e:
            print e
            pass
        return False


def init(url):
    urlParse = urlparse.urlparse(url)
    urlParse = urlParse.scheme + '://' + urlParse.netloc
    randomstr = 'dddjskjdksjkdj21331dasdad'
    homelUrl = urlParse
    lenUrl['homeUrl'] = len(requests.get(url=homelUrl, timeout=timeOut).text)
    url404 = urlParse + '/' + randomstr
    lenUrl['url404'] = len(requests.get(url=url404, timeout=timeOut).text)
    lenUrl['normalUrl'] = len(requests.get(url=url, timeout=timeOut).text)
    lenUrl['postUrl'] = len(requests.post(url=url, data='a=a', timeout=timeOut).text)

def getprocess():
    time.sleep(5)
    while True:
        progressLock.acquire()
        if targetList.qsize() > 0:
            processnum = 100 - round(float(targetList.qsize()) / targetListCount, 2) * 100
            if processnum != 100:
                print 'process:' + str(processnum) + '%'
            else:
                if thread._count() > 1:
                    print 'scanthreadnum:' + str(thread._count()) + ' wait for DogScan'
                else:
                    print 'process done'
                    break
        else:
            if thread._count() <= 1:
                print 'process done'
                exit()

        print 'scanthreadnum:' + str(thread._count())
        progressLock.release()
        time.sleep(10)


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('fuzzParam.py param.txt http://127.0.0.1/1.php or http://127.0.0.1/1/2/3/ ')
        sys.exit()
    threadCount = 50  # 线程 10
    timeOut = 10  # 延迟10秒
    init(sys.argv[2])
    thread.start_new_thread(getprocess, ())
    data = open(sys.argv[1], 'r').read()
    data = data.split('\n')
    for i in data:
        targetList.put({'url': '{}?{}=1'.format(sys.argv[2], i), 'method': 'GET', 'data': ''})
        targetList.put({'url': '{}/{}/1/'.format(sys.argv[2], i), 'method': 'GET', 'data': ''})
        targetList.put({'url': '{}'.format(sys.argv[2]), 'method': 'POST', 'data': '{}=1'.format(i)})
        targetList.put({'url': '{}'.format(sys.argv[2]), 'method': 'POST', 'data': str({i: '1'})})
        targetList.put({'url': sys.argv[2], 'method': 'GET', 'data': '', 'cookie': {i: '1'}})
    targetListCount = targetList.qsize()
    while True:
        try:
            scan_data = []
            if not targetList.empty():
                target = targetList.get()
            elif int(thread._count()) < 1:
                print "Fuzz Param Done"
                break
            else:
                continue
            while True:
                if int(thread._count()) < threadCount:
                    thread.start_new_thread(
                        fuzz, (target, lenUrl, timeOut, targetList))
                    break
                else:
                    time.sleep(2)
        except Exception as e:
            print e
