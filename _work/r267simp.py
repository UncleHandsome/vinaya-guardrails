# -*- coding: utf-8 -*-
"""267 輪・刀三：記錄檔之簡形漏字，**逐枚 positional 改正**（絕不全域字替——引號內之舊形乃供狀）。

法源：263 輪之誡（全域掃滅曾滅掉六行以錯字為供狀之引用）。故每枚皆帶足左文為錨，斷言恰一。
用法：python -X utf8 _work/r267simp.py [apply]
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = {
    u'日誌': os.path.join(ROOT, u'_archive', u'編年工程日誌.md'),
    u'SOP': os.path.join(ROOT, u'列印SOP.md'),
}
# (檔, 左文錨＋簡形, 改正形)
FIX = [
    (u'日誌', u'口径＝行首', u'口徑＝行首'),
    (u'日誌', u'**正拼接**一处：', u'**正拼接**一處：'),
    (u'日誌', u'四重奏』（4 处）', u'四重奏』（4 處）'),
    (u'日誌', u'447 处——**絕', u'447 處——**絕'),
    (u'SOP', u'逮 4 处真病', u'逮 4 處真病'),
]

t = {k: io.open(v, encoding=u'utf-8-sig').read() for k, v in FILES.items()}
bad = []
for f, old, new in FIX:
    if t[f].count(old) != 1:
        bad.append((f, old, t[f].count(old)))
    if t[f].count(new) != 0:
        bad.append((f, u'正形已在：' + new, t[f].count(new)))
print(u'合 %d 枚' % len(FIX))
if bad:
    print(u'!! 錨不合：%s' % bad[:6])
    sys.exit(2)
if u'apply' not in sys.argv:
    for f, old, new in FIX:
        print(u'  %s  %s ➔ %s' % (f, old, new))
    print(u'乾跑，未寫入。')
    sys.exit(0)
for f, old, new in FIX:
    t[f] = t[f].replace(old, new, 1)
for f, path in FILES.items():
    io.open(path, 'w', encoding=u'utf-8', newline=u'').write(t[f])
back = {k: io.open(v, encoding=u'utf-8-sig').read() for k, v in FILES.items()}
for f, old, new in FIX:
    assert back[f].count(old) == 0 and back[f].count(new) == 1, (f, old)
print(u'已寫入 %d 枚，回讀相符（引號內之舊形供狀一概未動）。' % len(FIX))
