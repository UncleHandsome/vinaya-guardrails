# -*- coding: utf-8 -*-
# r233fix　正隔號：本輪新入之三行校勘記誤用日式中黑 U+30FB，書中通例作 U+00B7（先量總數而後改）
import io
import os

NL = chr(10)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
MD = u'ver38四分律_起心動念心智分析框架_修正版.md'
JP, MID = u'・', u'·'

raw = io.open(MD, encoding=u'utf-8').read()
lines = raw.split(NL)
n0 = len(lines)
c_jp = raw.count(JP)
c_mid = raw.count(MID)
who = [i + 1 for i, l in enumerate(lines) if JP in l]
in233 = all(lines[i - 1].startswith((u'**三、採八處', u'**四、案閉', u'233. **', u'**一、所為'))
            or JP in lines[i - 1] for i in who)
print(u'量得：U+30FB %d 枚於 %s 行｜U+00B7 今 %d 見｜母數 %d' % (c_jp, who, c_mid, n0))
assert c_jp == 20 and who == [13706, 13708, 13709] and in233, u'形不如宣——未改'
txt = raw.replace(JP, MID)
io.open(MD, u'w', encoding=u'utf-8', newline=NL).write(txt)
t2 = io.open(MD, encoding=u'utf-8').read()
l2 = t2.split(NL)
assert t2.count(JP) == 0, u'舊形猶在'
assert t2.count(MID) == c_mid + 20, u'新形數不合：%d vs %d' % (t2.count(MID), c_mid + 20)
assert len(l2) == n0, u'行數已動'
assert l2[-1].startswith(u'*歲次丙午'), u'檔尾已動'
for i in who:
    assert l2[i - 1] == lines[i - 1].replace(JP, MID), u'第 %d 行之改不合' % i
print(u'後驗：U+30FB 歸零・U+00B7 加 20・行數 %d 不動・三行俱改 ✓' % len(l2))
