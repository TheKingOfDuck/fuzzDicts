# -*- coding: utf-8 -*-
# @Author: kingkk
# @Date:   2018-08-12 10:50:51
# @Last Modified by:   kingkk
# @Last Modified time: 2018-08-12 11:14:39
'''
字典去重
'''
import os

for i in os.walk('./'):
	files = i[2]

files.remove(os.path.basename(__file__))

for file in files:
	os.rename(file, file+'.bak')

t = {}
for file in files:
	f = open(file, 'w+')
	fbak = open(file+'.bak', 'r')
	t = {i for i in fbak.readlines()}
	for i in t:
		f.write(i)
	f.close()
	fbak.close()
	os.remove(file+'.bak')