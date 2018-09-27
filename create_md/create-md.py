#-*- coding: utf-8 -*
__author__ = 'geebos'
import datetime
import optparse
import os


split = '---'
time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
options = optparse.OptionParser()

options.add_option('-n', action='store', dest='filename')
options.add_option('--name', action='store', dest='filename')

options.add_option('-t', action='store', dest='tag')
options.add_option('--tag', action='store', dest='tag')


opts, other_args = options.parse_args()
tag = opts.tag
name = opts.filename

if name == None:
    print("please entry a name.")
    raise SystemExit(1)

if tag != None:
    if not os.path.isdir('config'):
        os.mkdir('config')
    with open('config/tags', 'w', encoding='utf-8') as f:
        f.write(opts.tag)
else:
    if os.path.isfile('config/tags'):
        with open('config/tags', 'r', encoding='utf-8') as f:
            tag = f.readline()

if tag == None:
    out = f'''{split}
title: {name}
date: {time}
tags: 
{split}'''
else:
    out = f'''{split}
title: {name}
date: {time}
tags: {tag}
{split}'''


with open(f'{name}.md', 'a', encoding='utf-8') as f:
    f.write(out)


