# -*- coding: utf-8 -*-
# @Author: kingkk
# @Date:   2018-08-11 19:32:38
# @Last Modified by:   kingkk
# @Last Modified time: 2018-08-28 11:36:19
import sys
import requests
from config import * 
from lib.log import Log
from lib.scan import Scan
from lib.generatedict import GenerateDcit


class Init:
	def __init__(self, args):	
		self.url = self.init_url(str(args.url))
		self.keywords = args.key_words


	def help(self):
		help = 'Useage : python ctf-wscan.py [website url]\n'
		help+= 'Example: python ctf-wscan.py http://ctf.test.com'
		print(help)
		exit()

	# def args(self):

	def init_url(self, url):
		'''
		处理成标准的url格式
		'''
		if not url.startswith('http'):
			url = 'http://'+url

		if not url.endswith('/'):
			url = url + '/'

		return url

	def detect(self):
		import uuid
		import random
		import string

		rand1 = ''.join(random.sample(string.ascii_letters, 8))
		rand2 = uuid.uuid4()
		rand3 = random.randint(1000000,99999999)
		r1 = requests.get(self.url+str(rand1))
		r2 = requests.get(self.url+str(rand2))
		r3 = requests.get(self.url+str(rand3))
		if r1.status_code == r2.status_code == r3.status_code == 200 and len(r1.text) == len(r2.text) == len(r3.text):
			req = requests.get
			return len(r1.text),req
		else:
			if REQUEST_METHOD == 1:
				req = requests.head
			elif REQUEST_METHOD == 2:
				req = requests.get
			return -1,req


	def get_files(self):
		# 获取默认扫描列表
		with open('dict/default.txt') as f:
			files = f.readlines()
		

		#生成关键字字典
		if KEY_WORDS or args.KEY_WORDS:
			g = GenerateDcit(self.keywords)
			for i in g.generate():
				files.append(i)


		files = (file.strip() for file in files)
		return files

	def start(self):
		threadlist = []
		loglist = {}
		files = self.get_files()
		req = self.detect()
		# print(req)
		# for i in files:
		# 	print(i)
		for i in range(NUMBER_OF_THREAD):
			threadlist.append(Scan(self.url, loglist, files, req))
		for t in threadlist:
			t.start()
		for t in threadlist:
			t.join()

		if CACHE_LOG:
			log = Log(self.url, loglist)
			log.save()
