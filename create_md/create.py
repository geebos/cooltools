#-*- coding: utf-8 -*
__author__ = 'geebos'
import datetime
import sys
import os


split = '---'


args = sys.argv
time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


if '-n' not in args:
    print("请输入名字")
    sys.exit(0)


try:
    name = args[args.index('-n')+1].replace('-', ' ')
except:
    print("请输入名字")
    sys.exit(0)

tags = None
if '-t' in args and len(args) > args.index('-t')+1:
    tags = args[args.index('-t')+1]
    if not os.path.isfile('config/tags'):
        if not os.path.isdir('config'):
            os.mkdir('config')
        with open('config/tags', 'w', encoding='utf-8') as f:
            f.write(tags)
else:
    if os.path.isfile('config/tags'):
        with open('config/tags', 'r', encoding='utf-8') as f:
            tags = f.readline()

if tags == None:
    out = f'''{split}
title: {name}
date: {time}
tags: 
{split}'''
else:
    out = f'''{split}
title: {name}
date: {time}
tags: {tags}
{split}'''


with open(f'{name}.md', 'a', encoding='utf-8') as f:
    f.write(out)

