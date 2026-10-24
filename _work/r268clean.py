# -*- coding: utf-8 -*-
"""268 輪・清場：一支性記帳器（帳修・帳改號・索引更新）用畢即除，**逐名列檔不用前綴通配**。
保留：第八尺 `v39secref.py`・負測 `r268neg.py`・網界 `r268net.py`・掃描 `r268scan.py`・267 之刀與尺。
末段跑一次『記憶名冊每檔是否存在』（第十八度之自我版）。
用法：python -X utf8 _work/r268clean.py [apply]
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, u'_work')
DROP = [u'r268sop.py', u'r268fix2.py', u'r268mem.py', u'r268mem2.py', u'r268num.py',
        u'r268note.py', u'r268idx.py']
MEM = os.path.join(os.path.expanduser(u'~'), u'.qoder', u'projects',
                   u'C--Users-lionc-OneDrive-----------------', u'memory',
                   u'project-round31-state.md')

for f in DROP:
    p = os.path.join(WORK, f)
    print(u'  %s｜存在=%s・大小 %s' % (f, os.path.exists(p),
                                     os.path.getsize(p) if os.path.exists(p) else u'—'))
missing = [f for f in DROP if not os.path.exists(os.path.join(WORK, f))]
if missing:
    print(u'!! 名單與實物不合（缺 %s），未刪任何檔' % missing)
    raise SystemExit(2)
if u'apply' not in __import__(u'sys').argv:
    print(u'乾跑：擬除 %d 檔' % len(DROP))
    raise SystemExit(0)
for f in DROP:
    os.remove(os.path.join(WORK, f))
print(u'已除 %d 檔。' % len(DROP))

t = io.open(MEM, encoding=u'utf-8').read()
names = sorted(set(re.findall(u'`(r\\d+\\w*\\.py|v39\\w+\\.py|_simp\\w+\\.py)`', t)))
absent = [n for n in names if not os.path.exists(os.path.join(WORK, n))]
print(u'記憶名冊 %d 檔・查無此檔：%s' % (len(names), absent or u'無'))
