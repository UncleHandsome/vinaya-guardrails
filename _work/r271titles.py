# -*- coding: utf-8 -*-
"""271 輪・量四：全書『《X》』之書名號宣稱——分三類核：
   ① 經論書名（《四分律》《成唯識論》…）→ 對本地語料之『檔名／書名自報』，只須是實有之典；
   ② **篇名**（含『犍度／分／品／集』者）→ 連綴須見於本地語料（折異體 揵→犍）；
   ③ 其他（人名／地名誤掛書名號者）→ 列出人工判。
用法：python -X utf8 _work/r271titles.py
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
L = io.open(os.path.join(ROOT, NAME), encoding=u'utf-8-sig').read().split(u'\n')
B = u'\n'.join(L)
PU = re.compile(u'[\\s\\u3000，、；：？！。\u2014\\-「」『』（）()〔〕\\[\\]·／/]')


def norm(s):
    return PU.sub(u'', s)


NC = norm(_tk.VINAYA).replace(u'揵度', u'犍度')
KNOWN = [u'四分律', u'成唯識論', u'六祖壇經', u'中阿含經', u'清規', u'百丈清規', u'摩訶僧祇律',
         u'十誦律', u'五分律', u'善見律', u'薩婆多論', u'根本說一切有部', u'大智度論',
         u'瑜伽師地論', u'俱舍論', u'大乘義章', u'釋氏要覽', u'禅苑清規', u'敕修百丈清規']
PIAN = re.compile(u'犍度|品$|集$|分$')
forms = {}
for m in re.finditer(u'《([^》\n]{1,26})》', B):
    forms[m.group(1).strip()] = forms.get(m.group(1).strip(), 0) + 1
print(u'《X》共 %d 形・%d 見' % (len(forms), sum(forms.values())))
print(u'\n── ② 篇名類（含犍度／分／品／集）──')
badp = 0
for k in sorted(forms, key=lambda x: -forms[x]):
    if not PIAN.search(k):
        continue
    hit = NC.count(norm(k)) or NC.count(norm(re.sub(u'^第[一-鿿]+', u'', k)))
    if not hit:
        badp += 1
        print(u'  ⚠ 語料無此連綴：《%s》全書 %d 見' % (k, forms[k]))
        for i, l in enumerate(L):
            if u'《%s》' % k in l:
                print(u'      L%-5d %s' % (i + 1, l.strip()[:104]))
                break
print(u'  小計 %d 形無據' % badp)
print(u'\n── ①③ 其餘《X》（書名與雜項）──')
for k in sorted(forms, key=lambda x: -forms[x]):
    if PIAN.search(k):
        continue
    known = next((x for x in KNOWN if x in k), None)
    print(u'  %-22s %3d 見 %s' % (k, forms[k], u'（書名：%s）' % known if known else u'⚠ 未列書名，須目判'))
