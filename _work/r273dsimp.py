# -*- coding: utf-8 -*-
"""273 輪・日誌之清瘡（逐枚帶左文為錨，不動舊條；全域替換在此類檔即自滅供狀）。

新出之字八枚，逐一判讀：**引用錯字之供狀一概不動**（U+4EA7・U+5355・U+8F2B 三枚乃本條所記之病字，
留在『X→U+XXXX』之式內即是證）；敘事用字之誤（码・读・单・与・两・则）逐枚改之。
又碼位之判必以實測：U+5306 實為『匆』非『匣』（匣＝U+5323）、U+9322 非『鎢』（鎢＝U+93A2）——
故引病字只列碼位不列字形，**不憑記憶為錯字取名**。
"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, u'_archive', u'編年工程日誌.md')
t = io.open(P, encoding=u'utf-8').read()
FIX = [
    (u'\u689d\u4e0e\u5927\u7db1', u'\u689d\u8207\u5927\u7db1', u'①与➔與'),
    (u'\u53cd\u5f15\u865f\u8207\u5355\u5f15\u865f', u'\u53cd\u5f15\u865f\u8207\u55ae\u5f15\u865f', u'②单➔單'),
    (u'\uff1a\u2460 **\u4ee5\u7801\u4f4d', u'\uff1a\u2460 **\u4ee5\u78bc\u4f4d', u'③码➔碼（首）'),
    (u'\u2014\u2014**\u7801\u4f4d\u53ea\u9632', u'\u2014\u2014**\u78bc\u4f4d\u53ea\u9632', u'④码➔碼（次）'),
    (u'\u4e4b\u6e90\u6b63\u5219\u8bfb\u51fa', u'\u4e4b\u6e90\u6b63\u5247\u8b80\u51fa', u'⑤正则读➔正則讀'),
    (u'\u4e24\u5ea6\u7834\u6cd5', u'\u5169\u5ea6\u7834\u6cd5', u'⑥两度➔兩度'),
    (u'\u5668\u2192U+5306\u300e\u5323\u300f', u'\u5668\u2192U+5306', u'⑦去『匣』之誤名'),
    (u'\u9396\u2192U+9322\u300e\u93a2\u300f', u'\u9396\u2192U+9322', u'⑧去『鎢』之誤名'),
]
for old, new, tag in FIX:
    n = t.count(old)
    assert n == 1, u'%s｜錨非一（%d）' % (tag, n)
    t = t.replace(old, new)
    print(u'%s ok' % tag)
io.open(P, 'w', encoding=u'utf-8').write(t)
print(u'清瘡八枚訖')
