# -*- coding: utf-8 -*-
"""第 263 輪・刀二：凡例第二律之式樣清創（編者語・撮語・拼接句不得掛「逐字」之單層角引號）。

法源＝本書【全書出版凡例】一之二『引號給予標準』：「……」唯給大正藏逐字原文；
      作者白話改寫、撮述經義、古德公案、法式標題一律『……』。
靶＝`_work/r263census.py` 於『出處標記在前＋同線 「」』之口徑下所逮之卡外 miss（除敘事說話之偽紅）。
每項須恰中一次（「十種肉不應食」唯二處同改）；乾跑印數，apply 方寫，寫畢回讀。
用法：python -X utf8 _work/r263style.py [apply]
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')

PAIRS = [
    (u'「大綱座右銘（憲綱心印）」', 1),
    (u'「本律」', 1),
    (u'「原典」', 1),
    (u'「本地語料」', 1),
    (u'「善護三業，但自觀行；蜂採其華，不惱他人；明眼避險，自淨其意；勤學無憂，常樂空閑」', 1),
    (u'「本來無一物、法尚應捨、不要起分別心」', 1),
    (u'「十種肉不應食」', 2),
    (u'「宗教生活扶助金」', 1),
    (u'「力竭陳報」', 1),
    (u'「想差阻卻故意」', 1),
    (u'「生疑者因決意未滿而法定降階結偷蘭遮」', 1),
    (u'「自言治（不自言不應治）」', 1),
    (u'「止犯（當作而不作）」', 1),
    (u'「執非因非道為真因真道」', 1),
    (u'「以心定性」', 1),
]
# 拼接之正：出處標記在引號外，引號唯留律文之逐字（汝以何心＝語料 96 見，逐字無誤）
SPLICE = [(u'「佛問：汝以何心」', u'佛問「汝以何心」', 1)]

txt = io.open(BOOK, encoding='utf-8-sig').read()
plan = []
bad = []
for old, want in PAIRS:
    n = txt.count(old)
    if n != want:
        bad.append((old, n, want))
    plan.append((old, u'『' + old[1:-1] + u'』', want))
for old, new, want in SPLICE:
    n = txt.count(old)
    if n != want:
        bad.append((old, n, want))
    plan.append((old, new, want))

for old, new, want in plan:
    print(u'%d｜%s ➔ %s' % (txt.count(old), old[:38], new[:38]))
if bad:
    print(u'!! 命中數不符：%s' % bad)
    sys.exit(2)
if u'apply' not in sys.argv:
    print(u'乾跑，未寫入。')
    sys.exit(0)
for old, new, want in plan:
    assert txt.count(old) == want, old
    txt = txt.replace(old, new)
io.open(BOOK, 'w', encoding='utf-8', newline='').write(txt)
chk = io.open(BOOK, encoding='utf-8-sig').read()
for old, new, want in plan:
    assert chk.count(old) == 0 and chk.count(new) == want, (old, new)
print(u'已寫入，%d 項回讀相符。' % len(plan))
