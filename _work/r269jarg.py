# -*- coding: utf-8 -*-
"""269 輪・量四：『工程／行政黑話』之名單今量——供新不變量『印面不作工程黑話』定靶。

口徑：只列**可逐字判定**之詞（黑話以詞為單位，不以義為單位，否則又墮『描述語同形』之盲）；
      並標其落點之章，及是否已在『不印底冊／圍欄』之外。
用法：python -X utf8 _work/r269jarg.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
L = io.open(os.path.join(ROOT, NAME), encoding=u'utf-8-sig').read().split(u'\n')
B = u'\n'.join(L)


def chap_of(i):
    ch = u'卷首'
    for k in range(i + 1):
        m = re.match(u'^# (第.{1,3}章|結語|終卷|附錄[一二三四五六])', L[k])
        if m:
            ch = m.group(1)
    return ch


WORDS = [u'解耦', u'模組', u'參數', u'代碼', u'流水號', u'工單', u'工單號', u'票據', u'測試集',
         u'接口', u'串列', u'陣列', u'資料庫', u'索引檔', u'腳本', u'管線', u'pipeline',
         u'SOP', u'KPI', u'OKR', u'迭代', u'版本控管', u'緩存', u'快取', u'正規化',
         u'去耦合', u'微服務', u'面向', u'顆粒度', u'回呼', u'登入欄位', u'表單',
         u'核取方塊', u'三聯單', u'編號格式', u'格式：', u'序列化', u'對帳', u'台帳']
print(u'── 黑話候選之名單今量 ──')
for w in WORDS:
    n = B.count(w)
    if n:
        chs = {}
        for i, l in enumerate(L):
            if w in l:
                chs[chap_of(i)] = chs.get(chap_of(i), 0) + 1
        print(u'  %-8s %3d 見　%s' % (w, n, u'・'.join(u'%s%d' % (k, v) for k, v in sorted(chs.items()))))
print(u'\n── 「格式：○○○」式之編碼宣稱（報告所指之『編號格式』）──')
for i, l in enumerate(L):
    if re.search(u'格式[:：]', l):
        print(u'  L%-5d %-8s %s' % (i + 1, chap_of(i), l.strip()[:120]))
print(u'\n── 印面之勾選框（- [ ]）與『一式／三份／執存』式 ──')
box = [(i + 1) for i, l in enumerate(L) if re.match(u'^\\s*- \\[ \\]', l)]
print(u'  「- [ ]」開頭之行：%d（附錄/第八章自檢表之形制）' % len(box))
for w in [u'一式', u'三份', u'執存', u'存檔備查', u'歸檔']:
    print(u'  「%s」%d 見' % (w, B.count(w)))
    for i, l in enumerate(L):
        if w in l:
            print(u'      L%-5d %-8s %s' % (i + 1, chap_of(i), l.strip()[:96]))
