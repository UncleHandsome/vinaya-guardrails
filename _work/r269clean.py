# -*- coding: utf-8 -*-
"""269 輪・清場：一支性記帳器用畢即除（**逐名列檔，不用前綴通配**），末段驗名冊配實物。
保留：刀 `r269fix.py`／`r269apx.py`・負測 `r269neg.py`・四支量尺 `r269probe/site/mark/jarg`・自查 `r269chk.py`・帳修 `r269simp.py`。
用法：python -X utf8 _work/r269clean.py [apply]
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, u'_work')
MEM = os.path.join(os.path.expanduser(u'~'), u'.qoder', u'projects',
                   u'C--Users-lionc-OneDrive-----------------', u'memory',
                   u'project-round31-state.md')
KEEP = [u'v39secref.py', u'r269fix.py', u'r269apx.py', u'r269neg.py', u'r269probe.py',
        u'r269site.py', u'r269mark.py', u'r269jarg.py', u'r269chk.py', u'r269simp.py',
        u'r268neg.py', u'r268net.py', u'r268scan.py', u'r267fix.py', u'r267neg.py',
        u'r267sec.py', u'r267simp.py', u'r267count.py']
DROP = [u'r269sop.py', u'r269mem.py', u'r269mem3.py', u'r269peek.py']

print(u'── 擬除 ──')
for f in DROP:
    p = os.path.join(WORK, f)
    print(u'   %-14s 存在=%s・在保留單=%s' % (f, os.path.exists(p), f in KEEP))
miss = [f for f in DROP if not os.path.exists(os.path.join(WORK, f))]
inkeep = [f for f in DROP if f in KEEP]
if miss or inkeep:
    print(u'!! 名單有誤（缺 %s／與保留單撞 %s），未刪' % (miss, inkeep))
    sys.exit(2)
if u'apply' not in sys.argv:
    print(u'乾跑：擬除 %d 檔' % len(DROP))
    sys.exit(0)
for f in DROP:
    os.remove(os.path.join(WORK, f))
print(u'已除 %d 檔。' % len(DROP))

t = io.open(MEM, encoding=u'utf-8').read()
names = sorted(set(re.findall(u'`(r\d+\w*\.py|v39\w+\.py|_simp\w*\.py)`', t)))
absent = [n for n in names if not os.path.exists(os.path.join(WORK, n))]
print(u'記憶名冊 %d 檔・查無此檔：%s' % (len(names), absent or u'無'))
for f in KEEP:
    if not os.path.exists(os.path.join(WORK, f)):
        print(u'!! 保留單落空：%s' % f)
