#!/bin/env python

import re
import sys

fname = sys.argv[1]
f = open(fname)

while True:
    line = f.readline()
    title = re.findall('title: \"(.*?)\"', line)
    if len(title) > 0:
        title = re.sub(' ', '-', title[0].lower())
        break

while True:
    line = f.readline()
    postdate = re.findall('date: (\d\d\d\d-\d\d-\d\d)', line)
    if len(postdate) > 0:
        postdate = re.sub(' ', '-', postdate[0].lower())
        break
    
fullfilename = postdate+'-'+title+'.md'
print(fullfilename)
f.close()
