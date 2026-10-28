# -*- coding: utf-8 -*-
r"""290・續查：難教之詞・附錄六 L 標・結小界兩段・案86 之篇聚線索。"""
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
BOOK = io.open(os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md'),
               encoding='utf-8').read()
BL = BOOK.split('\n')


def where(frag):
    f = re.sub(u'[^\\u4e00-\\u9fff]', u'', frag)
    out = []
    for n, t in CORP:
        p = t.find(f)
        if p >= 0:
            out.append(n)
    return out


print(u'【三・難教】')
for frag in [u'有二法一難教二不受訓導', u'一難教二不受訓導', u'難教二不受訓導', u'不受訓導']:
    print(u'  %-22s 語料 %d｜檔 %s' % (frag, V.count(re.sub(u'[^\u4e00-\u9fff]', u'', frag)), where(frag)))
for i, l in enumerate(BL):
    if u'難教' in l:
        print(u'  冊 L%-5d %s' % (i + 1, l.strip()[:120]))

print(u'\n【四・附錄六 L 標】')
for i, l in enumerate(BL):
    if l.startswith(u'* **原典文獻定位**'):
        print(u'  L%-5d %s' % (i + 1, l.strip()[:120]))

print(u'\n【五・結小界與解界】')
for frag in [u'當下道集一處結小界說戒', u'應解界去不應不解界而去']:
    print(u'  %-22s ➔ %s' % (frag, where(frag)))
print(u'  語料『受戒犍度』%d｜『說戒犍度』%d｜『明尼戒法』%d｜『二分之八』%d' % (
    V.count(u'受戒犍度'), V.count(u'說戒犍度'), V.count(u'明尼戒法'), V.count(u'二分之八')))

print(u'\n【一・案 86 之篇聚與條次線索】')
for frag in [u'數來詣寺住立言語戲笑', u'擅入比丘尼僧', u'罵比丘', u'工師種']:
    print(u'  %-22s ➔ %s' % (frag, where(frag)))
for n, t in CORP:
    if u'工師種' in t:
        p = t.find(u'工師種')
        seg = t[max(0, p - 900):p + 1600]
        print(u'  檔 %s 之『竟』標：%s' % (n, re.findall(u'([一二三四五六七八九十百零]{1,8})竟', seg)))
        print(u'  檔 %s 之『分』標：%s' % (n, re.findall(u'[一二三四五六七八九十]{1,3}分之[一二三四五六七八九十]{1,3}', seg)[:6]))
        print(u'  其制戒句：%s' % re.findall(u'若比丘尼[^]{0,40}?波逸提', seg)[:4])
for i, l in enumerate(BL):
    if u'卷二十七' in l:
        print(u'  冊『卷二十七』L%-5d %s' % (i + 1, l.strip()[:110]))
