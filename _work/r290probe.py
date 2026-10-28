# -*- coding: utf-8 -*-
r"""290・外路第十七報告五事之本地考證（唯讀）。

判準：本地六檔之檔段為唯一就地之證；『卷N』須落於該段所在之檔，方為相容。
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, u'_work'))
import v39align as VA                                    # noqa: E402
import _tk                                               # noqa: E402

CORP = [(n, t) for n, r, t, i in VA.CORPUS]
V = _tk.VINAYA
RANGE = {u'01-10原文.txt': u'1-10', u'11-21 原文.txt': u'11-21', u'22-30 原文.txt': u'22-30',
         u'31-37 原文.txt': u'31-37', u'38-49 原文.txt': u'38-49', u'50-60 原文.txt': u'50-60'}
BOOK = io.open(os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md'),
               encoding='utf-8').read()
BL = BOOK.split('\n')


def where(frag):
    f = re.sub(u'[^\\u4e00-\\u9fff]', u'', frag)
    return [(n, RANGE[n]) for n, t in CORP if f in t], V.count(f)


print(u'【一・案 86（持械圍攻）之檔段與條次】')
for frag in [u'執持刀杖瓦石', u'弊惡下賤工師種', u'飛天現神足', u'以刀杖瓦石']:
    print(u'  %-14s ➔ %s' % (frag, where(frag)))
for n, t in CORP:
    f = re.sub(u'[^\\u4e00-\\u9fff]', u'', u'工師種')
    if f in t:
        p = t.find(f)
        print(u'  檔 %s 其後之『竟』標：%s' % (n, re.findall(u'([一二三四五六七八九十百零]{1,7})竟', t[p:p + 3000])[:12]))
print(u'  冊中『卷二十七』%d 見｜『卷二十九』%d 見' % (BOOK.count(u'卷二十七'), BOOK.count(u'卷二十九')))
for i, l in enumerate(BL):
    if u'案例 86' in l and (u'卷二十七' in l or u'卷二十九' in l):
        print(u'  載體 L%-5d %s' % (i + 1, l[:150]))

print(u'\n【二・地標 05 兩段之檔段（冊作卷四十五 ➔ 卷十二／卷四十三？）】')
for frag in [u'我不見罪云何言我有罪', u'聽白已當名作餘語', u'云何僧與作不同住',
             u'僧與作不見犯羯磨', u'惡見不捨羯磨是為僧與作不同住']:
    print(u'  %-24s ➔ %s' % (frag[:22], where(frag)))

print(u'\n【三・『難教』之詞（冊作『有難教』）】')
print(u'  語料『一難教二不受訓導』：%d｜『難教』：%d' % (V.count(u'一難教二不受訓導'), V.count(u'難教')))
print(u'  %s' % where(u'有二法一難教二不受訓導'))
for i, l in enumerate(BL):
    if u'有難教' in l:
        print(u'  冊 L%-5d %s' % (i + 1, l.strip()[:140]))

print(u'\n【四・附錄六之『L 行號』標法】')
pat = re.compile(u'大正藏卷段[^）]*L\d+')
hit = [m.group(0) for m in pat.finditer(BOOK)]
print(u'  『大正藏卷段…L###』式：%d 見｜樣本：%s' % (len(hit), hit[:4]))
pat2 = re.compile(u'(L\d+(?:[–〜\-、，L\d+①-⑳\s]*)?)')
tot = len(re.findall(u'L\d+', BOOK))
print(u'  全書『L\\d+』：%d 見' % tot)
for i, l in enumerate(BL[:1]):
    pass
for i, l in enumerate(BL):
    if u'原典文獻定位' in l and i < 7900:
        print(u'  L%-5d %s' % (i + 1, l.strip()[:130]))
        break

print(u'\n【五・結小界與解界兩段之檔段（報告分作卷三十五／卷三十四）】')
for frag in [u'當下道集一處結小界說戒', u'應解界去不應不解界而去']:
    print(u'  %-22s ➔ %s' % (frag, where(frag)))
print(u'  語料『受戒犍度』：%d｜『說戒犍度』：%d' % (V.count(u'受戒犍度'), V.count(u'說戒犍度')))
