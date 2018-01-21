#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import time
import re
# new_url= "http://news.sina.com.cn/c/gat/2017-06-14/doc-ifyfzfyz4058260.shtml"
# m = re.search('doc-i(.+).shtml',new_url)
# print(m.group(0),m.group(1))


# import string
# s= 'abababab'
#
# print s.count('a')
#
# s = '1999'
# print s.isdigit()

s = '2011-10-13'
now = datetime.datetime.now()
otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
print otherStyleTime

timeArray = time.strptime(s, "%Y-%m-%d")
timeStamp = int(time.mktime(timeArray))
print timeStamp

a = datetime.datetime.fromtimestamp(timeStamp)
print a















