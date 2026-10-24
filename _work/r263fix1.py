# -*- coding: utf-8 -*-
"""第 263 輪・刀一：第三章 L1924 之拼接引文改為語料原位之真逐字（一字不重打）。

病灶：書中作《四分律》明文將「見罪能如法懺，而彼不受」——此乃律文相鄰兩句之**拼接**，
      語料無此連綴（`v39quote` 之口徑會判 miss）。
正解：自語料原位**複製**兩句（『有二法不得解脫』節與『有二法自得解脫』節），
      卷次不可細標者依全書既有形制作『（原典卷次未標）』。
用法：python -X utf8 _work/r263fix1.py         # 乾跑（只印）
      python -X utf8 _work/r263fix1.py apply
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39%E5%9B%9B%E5%88%86%E5%BE%8B' if False else
                    u'ver39四分律_起心動念心智分析框架_修正版.md')
CORPUS = os.path.join(ROOT, u'原文', u'50-60 原文.txt')

raw = io.open(CORPUS, encoding='utf-8', errors='replace').read()
ANCH = u'若如法懺而彼不受'
REPV = u'如法懺悔，?而彼不受'


def grab(start_key, end_key):
    i = raw.find(start_key)
    assert i >= 0, start_key
    j = raw.find(end_key, i)
    assert j >= 0, end_key
    seg = raw[i:j + len(end_key)]
    assert u'\n' not in seg and len(seg) < 90, (len(seg), seg[:40])
    return seg


s1 = grab(u'有二法不得解脫：一見罪不如法懺悔', u'而彼不受。')
s2 = grab(u'有二法自得解脫：一見罪能如法懺', u'如法受。')
assert raw.count(s1) == 1 and raw.count(s2) == 1, (raw.count(s1), raw.count(s2))
print(u'語料複製：%r ｜ %r' % (s1, s2))

old = (u'《四分律》明文將「見罪能如法懺，而彼不受」定性為**受者之過失**（受者得罪）；'
       u'僧團負有如法受懺之法定受懺義務，不得異化為派系私刑。')
new = (u'《四分律》（原典卷次未標）列『不受』於不得解脫之法：「' + s1 + u'」復明自得解脫之法：「'
       + s2 + u'」——是故**受不受之過在受者而不在懺者**；'
       u'僧團負有如法受懺之法定受懺義務，不得異化為派系私刑。')

txt = io.open(BOOK, encoding='utf-8-sig').read()
n = txt.count(old)
print(u'命中數：%d（須恰 1）' % n)
if n != 1:
    sys.exit(2)
if u'apply' not in sys.argv:
    print(u'乾跑，未寫入。')
    print(u'新句：%s' % new)
    sys.exit(0)
io.open(BOOK, 'w', encoding='utf-8', newline='').write(txt.replace(old, new))
chk = io.open(BOOK, encoding='utf-8-sig').read()
assert chk.count(new) == 1 and chk.count(old) == 0, u'回讀不符'
print(u'已寫入並回讀相符。')
