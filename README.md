# fuzzDicts
Web Pentesting Fuzz 字典,一个就够了。

## log 

不定期更新，使用前建议git pull一下，同步更新。


  **分享字典建议直接提交PR** 


20201202:

* 在目录字典下更新了一个[Se7en](https://github.com/r00tSe7en)师傅给的admin目录变种。

20200510:

* 用户名字典下新增了一个百家姓top3000的拼音，去重后188条，Attack!!!.


20200420:

* 合并一个由[lanyi1998](https://github.com/lanyi1998)提交的pr，测试常用手机号码top300+，放在用户名字典里面，瓶颈测试时可以试试；添加一份团队Child师傅提供的某集团的弱口令字典。

20200410:

* 上传了centos和aix的/etc/目录，放在ssrfDict里面，aix和其他系统区别还是蛮大的，实战一下RFI注意区别。

20200406:

* 合并一个由[lewiswu1209](https://github.com/lewiswu1209)提交的pr，密码top19576。

20200410:

* 新增centOS和AIX主机的/etc/目录的文件列表，放在ssrfDict目录，实战中遇到的，aix和其他系统区别还是蛮大的，作用自己琢磨。

20200221:

* 更新由[makoto56](https://github.com/makoto56)师傅加强后的webshell密码字典,离职学习中，毕业前不会有太多的web测试任务（也不想再继续打web了），字典更新频率会降低很多，如果有小伙伴想一起维护可以联系我啊。

20200211:

* 新增一个lot字典，数据来源于tg群里别人发的50w互联网lot设备弱口令，由[sunu11](https://github.com/sunu11)师傅提取，在此基础上添加了国内的数据。遇到不知名的设备时一阵爆怼咯，擅用字典，事半功倍。

20200115:

* xss字典增加burp官方的210条payload，放在easyXssPayload目录下的[burpXssPayload.txt](https://github.com/TheKingOfDuck/fuzzDicts/blob/master/easyXssPayload/burpXssPayload.txt)文件中。

* 用户名字典增加了2018-2020青年安全圈黑阔们的id，数据来源[Security-Data-Analysis-and-Visualization](https://github.com/404notf0und/Security-Data-Analysis-and-Visualization)，分离了id,博客域名,github ID三个字段。放在userNameDict目录下[sec_ID.txt](https://github.com/TheKingOfDuck/fuzzDicts/blob/master/userNameDict/sec_id.txt),遇到shell先去撞一下,自建waf这些id都标记为黑名单关键字就对了。

* 其他优化，更新。


20200106:

* xss字典增加100+条新Payload，并合并到本项目。

20200104:

* 再次优化参数字典，感谢[key师傅](https://github.com/gh0stkey)的修正。

20191219:

* 使用正则`(\W)`过滤了很多无效的参数,如空格(){}等等,并允许-的存在，重新合并去重了一下参数字典，均放在AllParam.txt，感谢奶权师傅的反馈。

20191214:

* 最近在整理各CMS的漏洞，前前后后下载了50多个CMS,顺便重新采集了一下参数，parameter.txt的体积增加到5859条。（原2800+）

20191106:

* 在密码字典下新增加了华为安全产品默认用户名密码速查表.

20191026:

* 使用过程中发现参数字典冗杂了,所以将最近采集的到的以及一些优秀的工具中的字典合并去重复放进了AllParam.txt，共51219条，推荐使用.

20191022:

* 在参数字典下新增了[Arjun](https://github.com/s0md3v/Arjun)的一个工具,比原先的脚本要强大得多,字典在db目录下.

20190928:

* 在passwordDict下新增了从[猪猪侠师傅Github](https://github.com/ring04h)复制的wifi密码top2000字典。

20190819:

* 在directoryDicts下新增了常见漏洞目录，推荐直接使用all.txt

* 在passwodDict下新增了常见安全设备/路由器/中间件/服务弱口令清单。不过还是推荐使用RW_Password这个强弱口令字典，因为等保的强压之下很多单位不得不将密码设置的复杂，为了方便记忆这些密码又基本都是有规律的，从而诞生了强弱口令，真的很好用啊。
* 其他更新，本次更新部分字典采集自[SaiDict](https://github.com/Stardustsky/SaiDict),合并的时候仔细去重了。

20190811：

* 上传了自己平常爆破子域名用的字典(从subDomainsBrute,layer等工具中提取出来合并去重，再和自己生成的部分字典合并)，推荐使用main.txt,另一个比较弟弟。

20190801：

* 合并了一个[r35tart](https://github.com/r35tart/RW_Password)师傅整理的很好的“强弱口令”字典（即看起来很复杂，单但实际上很多人在用的密码）

20190615：

* 合并了一个[国外的字典](https://github.com/emadshanab/WordLists-20111129) 感觉分类有点乱 考完试再重新整理一下咯。

## content

* [参数Fuzz字典](#参数fuzz字典)
* [Xss Fuzz字典](#xss-fuzz字典)
* [用户名字典](#用户名字典)
* [密码字典](#密码字典)
* [目录字典](#目录字典)
* [sql-fuzz字典](#sql-fuzz字典)
* [ssrf-fuzz字典](#ssrf-fuzz字典)
* [XXE字典](#XXE字典)
* [ctf字典](#ctf字典)
* [Api字典](#Api字典)
* [路由器后台字典](#路由器后台字典)
* [文件后缀Fuzz](#文件后缀Fuzz)
* [js文件字典](#js文件字典)
* [子域名字典](https://github.com/TheKingOfDuck/fuzzDicts/tree/master/subdomainDicts)



工具推荐：[burpsuite](https://portswigger.net/burp/),[sqlmap](https://github.com/sqlmapproject/sqlmap),[xssfork](https://github.com/bsmali4/xssfork),[Wfuzz](https://github.com/xmendez/wfuzz/),[webdirscan](https://github.com/TuuuNya/webdirscan)

如果有什么的好字典或是建议欢迎提交issue给我。


## [参数Fuzz字典](https://github.com/TheKingOfDuck/fuzzDicts/blob/master/paramDict)

```
https://github.com/TheKingOfDuck/fuzzDicts/blob/master/paramDict/parameter.txt
```

![CoolCat](https://github.com/TheKingOfDuck/fuzzDicts/blob/master/images/parameter.jpg)



采集自`ThinkPHP`,`yii2`,`phphub`,`Zblog`,`DiscuzX`,`WordPress`等常见PHP框架/CMS。

使用技巧：如http://127.0.0.1/1.php ,视为可疑文件，进行fuzz param 选择GET,POST AND (POST JSON) AND (GET Route) AND cookie param


## [Xss Fuzz字典](https://github.com/TheKingOfDuck/easyXssPayload/blob/master/easyXssPayload.txt)

```
https://github.com/TheKingOfDuck/easyXssPayload/blob/master/easyXssPayload.txt
```

![CoolCat](https://github.com/TheKingOfDuck/fuzzDicts/blob/master/images/xss.jpg)

采集自`github`。

## [用户名字典](https://github.com/TheKingOfDuck/fuzzDicts/tree/master/userNameDict)

```
https://github.com/TheKingOfDuck/fuzzDicts/tree/master/userNameDict
```

![CoolCat](https://github.com/TheKingOfDuck/fuzzDicts/blob/master/images/username.jpg)


## [密码字典](https://github.com/TheKingOfDuck/fuzzDicts/tree/master/passwordDict)

```
https://github.com/TheKingOfDuck/fuzzDicts/tree/master/passwordDict
```

![CoolCat](https://github.com/TheKingOfDuck/fuzzDicts/blob/master/images/password.jpg)

## [目录字典](https://github.com/TheKingOfDuck/fuzzDicts/tree/master/directoryDicts)

```
https://github.com/TheKingOfDuck/fuzzDicts/tree/master/directoryDicts
```

![CoolCat](https://github.com/TheKingOfDuck/fuzzDicts/blob/master/images/directory.jpg)


## [SQL Fuzz字典](https://github.com/TheKingOfDuck/fuzzDicts/blob/master/sqlDict/sql.txt)

```
https://github.com/TheKingOfDuck/fuzzDicts/blob/master/sqlDict/sql.txt
```

![CoolCat](https://github.com/TheKingOfDuck/fuzzDicts/blob/master/images/sql.jpg)


## [ssrf fuzz字典](https://github.com/TheKingOfDuck/fuzzDicts/blob/master/ssrfDicts)

```
https://github.com/TheKingOfDuck/fuzzDicts/blob/master/ssrfDicts
```

![CoolCat](https://github.com/TheKingOfDuck/fuzzDicts/blob/master/images/ssrf.jpg)

由[\xeb\xfe](https://github.com/doge-dog)师傅提供。

## [XXE字典](https://github.com/TheKingOfDuck/fuzzDicts/tree/master/XXEDicts)

```
https://github.com/TheKingOfDuck/fuzzDicts/tree/master/XXEDicts
```

![CoolCat](https://github.com/TheKingOfDuck/fuzzDicts/blob/master/images/xxe.jpg)

收集自百度。

## [ctf字典](https://github.com/TheKingOfDuck/fuzzDicts/tree/master/ctfDict)

```
https://github.com/TheKingOfDuck/fuzzDicts/tree/master/ctfDict
```

![CoolCat](https://github.com/TheKingOfDuck/fuzzDicts/blob/master/ctfDict/ctf-wscan/1.gif)

采集自[kingkaki](https://github.com/kingkaki/ctf-wscan)，原先收集时百度直接下载的压缩包，没看到github链接，所以没标记来源，抱歉抱歉

## [Api字典](https://github.com/TheKingOfDuck/fuzzDicts/tree/master/apiDict)

```
https://github.com/TheKingOfDuck/fuzzDicts/tree/master/apiDict/api.txt
```

![CoolCat](https://github.com/TheKingOfDuck/fuzzDicts/blob/master/images/api.jpg)

钟馗采集的代码写得很cxk 我真弟弟。。。

## [路由器后台字典](https://github.com/TheKingOfDuck/fuzzDicts/tree/master/routerDicts)

```
https://github.com/TheKingOfDuck/fuzzDicts/tree/master/routerDicts/pass.txt
```

![CoolCat](https://github.com/TheKingOfDuck/fuzzDicts/blob/master/images/router.jpg)

## [文件后缀Fuzz](https://github.com/TheKingOfDuck/fuzzDicts/tree/master/uploadFileExtDicts)

```
https://github.com/TheKingOfDuck/fuzzDicts/tree/master/uploadFileExtDicts
```

![CoolCat](https://github.com/TheKingOfDuck/fuzzDicts/blob/master/images/fileExt.png)

采集自https://github.com/c0ny1/upload-fuzz-dic-builder


## [js文件字典](https://github.com/TheKingOfDuck/fuzzDicts/tree/master/js)

采集自:https://github.com/7dog7/bottleneckOsmosis




