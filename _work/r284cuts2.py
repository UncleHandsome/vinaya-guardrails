# -*- coding: utf-8 -*-
"""284・補刀：凡例新立之『三層界定』句內掛了裸的單層角引號，被尺三逮為『未標界之非逐字』——
   改以名詞述之（單層／雙層角引號），不落形於冊。"""
import hashlib
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
APPLY = u'--apply' in sys.argv
T = io.open(BOOK, encoding=u'utf-8-sig').read()
sha = lambda x: hashlib.sha256(x.encode(u'utf-8')).hexdigest()[:12]
OLD = (u'又一：**逐字之文內遇引中之引，一概作『……』——雖涉三層亦仍作『』，不復迴「」**；'
       u'蓋全書逐字之抽取以 「」 為界，三層若再掛「」，逐字之尺必誤截其段，反傷校勘。')
NEW = (u'又一：**逐字之文內遇引中之引，一概作雙層角引號（『……』）——雖涉三層亦仍作雙層，不復迴用單層角引號**；'
       u'蓋全書逐字之抽取以單層角引號為界，三層若再掛單層，逐字之尺必誤截其段，反傷校勘。')
print(u'命中：%d' % T.count(OLD))
assert T.count(OLD) == 1
T2 = T.replace(OLD, NEW, 1)
print(u'改後 %d 行・sha %s' % (len(T2.split(u'\n')), sha(T2)))
if not APPLY:
    print(u'（乾跑）')
    sys.exit(0)
io.open(BOOK, 'w', encoding=u'utf-8').write(T2)
back = io.open(BOOK, encoding=u'utf-8-sig').read()
print(u'落盤訖・同=%s・sha %s' % (back == T2, sha(back)))
