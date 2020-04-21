#!/usr/bin/env python

# -*- coding: utf-8 -*-

import requests
import time
from pyquery import PyQuery as pq

import re

startIndex = 12345712
endIndex = 12347837
# endIndex = 12345715

#  url ='https://www.boquge.com/book/21281/12345712.html'

fd =open('/Users/bm/Desktop/仙逆.txt', 'w', encoding ='utf-8')

for index in range(startIndex,endIndex+1) :
    html = pq(requests.get('https://www.boquge.com/book/21281/%s.html' % index).text)
    html.remove('.gad2')
    title = html('#h1 h1').text()
    print('下载 -> %s' % title)
    content = html('#txtContent').text()
    fd.write(title)
    fd.write('\n')
    fd.write(content)
    fd.write('\n\n')
    time.sleep(0.1)

fd.flush()
fd.close()

exit()
