# -*- coding: utf-8 -*-
"""265 輪・刀一：術語與撮述判語自「」歸位『』（凡例第二律），靶在附錄六法理欄三十二枚。

法源：【全書出版凡例】一之二——「……」唯給大正藏逐字原文；作者白話改寫・撮述經義・法式標題作『……』。
口徑（`_work/r265probe.py` 之量）：附錄六・「」norm ≤14 字・無句末標點・語料無據。分三桶：
      桶一 純編者語 ➔ 『』；（『與狂癡羯磨』三見同治——律本作「心亂狂癡羯磨」，此乃撮述名）
      桶二 律語攙括注 ➔ 引號唯留律語，今譯移到引號外之括號；
      桶三 律語本形（調部・作意）留「」不較。
用法：python -X utf8 _work/r265style.py         # 乾跑
      python -X utf8 _work/r265style.py apply
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')

ONE = [u'法定保證人義務', u'治病雙修、密意方便', u'最初違犯之因緣人', u'法官自創罪名',
       u'事後追溯', u'入住出三時受樂', u'一剎那之貪愛迎合（相應心所受樂）', u'非自願',
       u'自願接納', u'依其原本之指示實行', u'教唆未遂之方便偷蘭遮',
       u'賦能型治理（Enabling Governance）', u'非自由意志行為',
       u'無責任能力人行為不罰', u'清醒故作', u'手弄排精', u'程序瑕疵一票否決',
       u'親厚意取無犯', u'自認為親厚', u'私人關係好', u'為懺悔和合故無犯',
       u'預備階段自主中止', u'承諾應允 ➔ 反悔退出 ➔ 拒絕受贓', u'方便突吉羅輕罪',
       u'心差自主中止']
WANT = [(u'與狂癡羯磨', 3)]
TWO = [(u'其「明知、生疑、放任（不作為）」之態度', u'其「明知、生疑」而復『放任（不作為）』之態度', 1),
       (u'前方便結「偷蘭遮（重罪未遂中罪）」', u'前方便結「偷蘭遮」（今譯：重罪未遂中罪）', 1),
       (u'破壞「現前、自白、法定人數」等法定五如法要件', u'破壞「現前、自白」與『法定人數』等法定五如法要件', 1),
       (u'法律評價為「不成就（自始無效）」', u'法律評價為「不成就」（意即自始無效）', 1)]

t = io.open(BOOK, encoding=u'utf-8-sig').read()
plan = [(u'「%s」' % q, u'『%s』' % q, 1) for q in ONE]
plan += [(u'「%s」' % q, u'『%s』' % q, w) for q, w in WANT]
plan += [(o, n, w) for o, n, w in TWO]

bad = [(o, t.count(o), w) for o, _n, w in plan if t.count(o) != w]
print(u'合 %d 項（桶一 %d・多見者 %d・桶二 %d）' % (len(plan), len(ONE), len(WANT), len(TWO)))
if bad:
    print(u'!! 命中數不符：%s' % bad)
    sys.exit(2)
if u'apply' not in sys.argv:
    for o, n, w in plan:
        print(u'   ×%d｜%s ➔ %s' % (w, o[:34], n[:34]))
    print(u'乾跑，未寫入。')
    sys.exit(0)
for o, n, w in plan:
    assert t.count(o) == w, o
    t = t.replace(o, n)
io.open(BOOK, 'w', encoding=u'utf-8', newline=u'').write(t)
chk = io.open(BOOK, encoding=u'utf-8-sig').read()
for o, n, w in plan:
    assert chk.count(o) == 0 and chk.count(n) == w, (o, n)
print(u'已寫入 %d 項，回讀相符。' % len(plan))
