# -*- coding: utf-8 -*-
# @Author: King kaki
# @Date:   2018-07-30 13:18:58
# @Last Modified by:   King kaki
# @Last Modified time: 2018-08-21 21:56:55

import sys
import re
import threading
from config import *

import requests


class Scan(threading.Thread):
	def __init__(self, url, log, files, req):
		threading.Thread.__init__(self)
		self.url = url
		self.log = log
		self.len, self.req = req
		self.files = files



	def run(self):
		for file in self.files:
			try:
				r = self.req(self.url+file, timeout=TIME_OUT)
			except:
				continue
			with threading.Lock():
				self.display(r, file)

	# def setting(self):
	# 	# 获取请求方式
	# 	if REQUEST_METHOD == 1:
	# 		req = requests.head
	# 	elif REQUEST_METHOD == 2:
	# 		req = requests.get
	# 	return req


				
	def display(self, r, file):
		if self.len == -1:
			if r.status_code not in INVALID_CODE: 
				print('[{}] => {}{}'.format(r.status_code, file, '\t'*5))
				self.log[file] = r.status_code
			else:
				print('[{}] => {}{}'.format(r.status_code, file, '\t'*5))
		else:
			if len(r.text) != self.len:
				print('[{}] => {}{}'.format(r.status_code, file, '\t'*5))
				self.log[file] = r.status_code
			else:
				print('[{}] => {}{}'.format(r.status_code, file, '\t'*5), end='\r')




