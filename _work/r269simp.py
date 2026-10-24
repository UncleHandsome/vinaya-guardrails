# -*- coding: utf-8 -*-
"""269 輪・帳修：編年日誌 269 條敘事區之七枚簡形逐枚歸正（帶左文為錨，引號內之供狀一概不動）。
用法：python -X utf8 _work/r269simp.py [apply]
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, u'_archive', u'編年工程日誌.md')
FIX = [
    (u'ver38 正本為對照之据）', u'ver38 正本為對照之據）'),
    (u'落到实处：**世俗實定法', u'落到實處：**世俗實定法'),
    (u'（不以放宽換假綠）', u'（不以放寬換假綠）'),
    (u'改從計數只留事实之形', u'改從計數只留事實之形'),
    (u'凡例兩段重写', u'凡例兩段重寫'),
    (u'然**全書『保密義務』唯此一见**', u'然**全書『保密義務』唯此一見**'),
]
t = io.open(P, encoding=u'utf-8-sig').read()
bad = [(o, t.count(o)) for o, n in FIX if t.count(o) != 1] + \
      [(u'正形已在：' + n, t.count(n)) for _o, n in FIX if t.count(n)]
print(u'合 %d 枚' % len(FIX))
if bad:
    print(u'!! 錨不合：%s' % bad[:6])
    sys.exit(2)
if u'apply' not in sys.argv:
    for o, n in FIX:
        print(u'  %s ➔ %s' % (o[:34], n[:34]))
    print(u'乾跑，未寫入。')
    sys.exit(0)
for o, n in FIX:
    t = t.replace(o, n, 1)
io.open(P, 'w', encoding=u'utf-8', newline=u'').write(t)
chk = io.open(P, encoding=u'utf-8-sig').read()
for o, n in FIX:
    assert chk.count(o) == 0 and chk.count(n) == 1, o[:24]
print(u'已寫入 %d 枚，回讀相符。' % len(FIX))
