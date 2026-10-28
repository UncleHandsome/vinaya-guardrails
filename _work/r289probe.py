# -*- coding: utf-8 -*-
r"""289・外路第十六報告六事之語料考證（唯讀）。

一、逐句查本地《四分律》語料（去標點）與檔段；
二、查他部經論（中阿含等）是否在本地收錄之列；
三、查條末『N竟』之尾標能否定條次（波逸提六十六）。
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, u'_work'))
import v39align as VA                                    # noqa: E402
import _tk                                               # noqa: E402


def strip(s):
    return re.sub(u'[^\\u4e00-\\u9fff]', u'', s)


CORP = [(n, t) for n, r, t, i in VA.CORPUS]

print(u'【一・目連牽臂公案（L2098）】')
for q in [u'怪哉目連', u'何乃造次', u'自今已去我更不說戒', u'汝等自共說戒',
          u'自今已去聽作自言治', u'若不自言不應治', u'汝今不應為後亦不應為',
          u'汝等自作羯磨說戒', u'牽臂', u'不淨比丘']:
    sq = strip(q)
    files = [n for n, t in CORP if sq in t]
    print(u'  %-14s VINAYA %d｜檔：%s' % (q, _tk.VINAYA.count(sq), files))

print(u'\n【二・不受與自得解脫（L2041）】')
for q in [u'有二法不得解脫', u'見罪不如法懺悔', u'若如法懺而彼不受', u'有二法自得解脫',
          u'如法懺者彼能如法受']:
    sq = strip(q)
    print(u'  %-14s 檔：%s' % (q, [n for n, t in CORP if sq in t]))

print(u'\n【三・波逸提第六十六條（L2723）】')
for q in [u'若比丘鬪諍如法滅已後更發起者波逸提', u'知諍事如法懺悔已']:
    sq = strip(q)
    print(u'  %-28s 檔：%s' % (q[:26], [n for n, t in CORP if sq in t]))
raw = dict((n, r) for n, r, t, i in VA.CORPUS)
for n, t in CORP:
    if strip(u'若比丘鬪諍如法滅已') in t:
        p = t.find(strip(u'若比丘鬪諍如法滅已'))
        seg = t[max(0, p - 300):p + 120]
        print(u'  檔 %s 前後文：%s' % (n, seg[-260:]))
        print(u'  其內『竟』尾標：%s' % re.findall(u'[（(]?([一二三四五六七八九十百]{1,6})竟[)）]?',
                                                  t[max(0, p - 1200):p + 400]))

print(u'\n【四・他部經論是否本地收錄】')
DIRS = [u'原文', u'_tk', u'_corpus', u'語料']
for d in DIRS:
    fp = os.path.join(ROOT, d)
    if os.path.isdir(fp):
        print(u'  目錄 %s：%s' % (d, sorted(os.listdir(fp))[:14]))
print(u'  _tk 之語料彙：%s' % [x for x in dir(_tk) if x.isupper()][:24])
for key in [u'中阿含', u'成唯識', u'勝鬘', u'瑜伽師地', u'中論']:
    found = []
    for d in DIRS:
        fp = os.path.join(ROOT, d)
        if not os.path.isdir(fp):
            continue
        for f in os.listdir(fp):
            if key in f:
                found.append(os.path.join(d, f))
    print(u'  檔名含『%s』：%s' % (key, found))
