# -*- coding: utf-8 -*-
# @Author: King kaki
# @Date:   2018-07-30 16:06:30
# @Last Modified by:   kingkk
# @Last Modified time: 2018-08-12 10:21:18

from datetime import datetime
import re
from config import *
import os
class Log:
	def __init__(self, url, log):
		self.url = url
		self.filename = self._getname(self.url)
		self.log = log


	def save(self):
		print('output at {}'.format(self.filename))
		with open('output/{}'.format(self.filename), 'w+') as f:
			f.write('[TIME] \t\t\t=> {}\n'.format(datetime.now()) )
			f.write('[TARGET] \t\t\t=> {}\n'.format(self.url))
			f.write('[NUMBER_OF_THRED] \t=> {}\n'.format(NUMBER_OF_THREAD))
			f.write('[KEY_WORDS] \t\t=> {}\n'.format(KEY_WORDS))
			f.write('\n')
			# f.write('{}RESULT{}\n'.format('*'*10, '*'*10))

			for file, status_code in self.log.items():
				
				f.write('[{}] => {}\n'.format(status_code, file))
		print('\n' + '='*30)
		os.system('cat output/' + self.filename)
		print('='*30 + '\n' )



	def _getname(self, url):
		r =  re.match(r'http[s]?://([\\\.\w\d:/]+)/', url).group(1)
		r = r.replace(':','.')
		r = r.replace('/','.')
		r = r.replace('\\','.')
		return r+'.txt'











