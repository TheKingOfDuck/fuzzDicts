# -*- coding: utf-8 -*-
# @Author: King kaki
# @Date:   2018-07-30 12:37:36
# @Last Modified by:   kingkk
# @Last Modified time: 2018-08-18 15:33:01

# url = 'http://localhost:80/'
# url = 'http://ctf5.shiyanbar.com/web/'
import sys
import argparse
from lib.init import Init


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('url', help="The website to be scanned", type=str)
	parser.add_argument('-k', '--keys', dest="key_words", nargs='+', help="Keys words to extend scan", type=str, default="")
	args = parser.parse_args()
	
	scan = Init(args)
	scan.start()

if __name__ == '__main__':
	main()

