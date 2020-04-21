#!/usr/bin/env python

# -*- coding: utf-8 -*-

import requests
import time
from pyquery import PyQuery as pq

import re

startIndex = 17036832
# endIndex = 153157174
endIndex = 17036835

#  url ='http://www.paoshu8.com/44_44420/17036832.html'

fd =open('C:/Users/bm/Desktop/阴阳鬼术.txt', 'w', encoding ='utf-8')

for index in range(startIndex,endIndex+1) :
    html = pq(requests.get('http://www.paoshu8.com/44_44420/%s.html' % index).text)
    title = html('.bookname h1').text()
    print('下载 -> %s' % title)
    content = html('#content')
    content.remove(':last-child')
    fd.write(title)
    fd.write('\n')
    fd.write(content.text())
    fd.write('\n\n')
    time.sleep(0.1)

fd.flush()
fd.close()

exit()
