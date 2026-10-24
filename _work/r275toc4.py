# -*- coding: utf-8 -*-
"""275 輪・目錄同步（定版）：先自備份一步還原，再**只在卷首目錄之內**作最小易字。

前車：① v1 誤取他章同序列；② v2 整行覆寫丟括注；③ v3 意圖全書替『心理學』三字，量得全書 17 見——**即止**（多數為正文常用語）。
今定：範圈先切『# 第一章』之前；再限定在目錄內『第五章』至『第六章』兩條章題之間；
      且只替舊題之異字，括注摘語一概不動；改後斷言該條含新題、全書他處一字未動。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r275toc4.py
"""
import difflib
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, u'_work')
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'\u5217\u5370' not in q][0]
SRC = os.path.join(ROOT, NAME)
BAK = os.path.join(WORK, u'r275toc.bak')
OLD, NEW = u'\u5fc3\u7406\u5b78', u'\u5fc3\u6027'            # 心理學 → 心性
C5, C6, CH4 = u'\u7b2c\u4e94\u7ae0', u'\u7b2c\u516d\u7ae0', u'\u7b2c\u56db\u7bc0'

pristine = io.open(BAK, encoding=u'utf-8').read()            # ① 先還原（v1/v2 之改一筆抹平）
cur = io.open(SRC, encoding=u'utf-8').read()
io.open(SRC, 'w', encoding=u'utf-8').write(pristine)
L = pristine.split(u'\n')
BODY0 = next(i for i, l in enumerate(L) if l.startswith(u'# \u7b2c\u4e00\u7ae0'))
c5 = next(i for i, l in enumerate(L[:BODY0]) if l.lstrip().startswith(u'* **' + C5))
c6 = next(i for i, l in enumerate(L[:BODY0]) if i > c5 and l.lstrip().startswith(u'* **' + C6))
hits = [i for i in range(c5, c6) if L[i].lstrip().startswith(u'* ' + CH4) and OLD in L[i]]
assert len(hits) == 1, u'\u76ee\u9304\u4e94\u7ae0\u7b2c\u56db\u7bc0\u689d\u542b\u65e7\u5b57\u8005 %d \u7b46' % len(hits)
i = hits[0]
L[i] = L[i].replace(OLD, NEW)
out = u'\n'.join(L)
assert out.count(OLD) == pristine.count(OLD) - 1, u'\u5168\u66f8\u8f03\u5b57\u6578\u4e0d\u5c0d'
io.open(SRC, 'w', encoding=u'utf-8').write(out)
sm = difflib.SequenceMatcher(None, cur.split(u'\n'), L).get_opcodes()
print(u'\u76ee\u9304 L%d \u5b9a\uff5c%s' % (i + 1, L[i].strip()[:76]))
print(u'\u8207\u4e0a\u4e00\u6b65\u76f8\u8f03\uff1a\u66f4\u65b0 %d \u884c\u3001\u586b\u5165 %d \u884c\u3001\u522a\u9664 %d \u884c' % (
    sum(1 for o in sm if o[0] == u'replace'), sum(o[2] - o[1] for o in sm if o[0] == u'insert'),
    sum(o[2] - o[1] for o in sm if o[0] == u'delete')))
print(u'\u5168\u66f8\u300e\u5fc3\u7406\u5b78\u300f\uff1a%d \u2192 %d\uff5c\u300e\u5fc3\u6027\u300f\uff1a%d \u2192 %d' % (
    pristine.count(OLD), out.count(OLD), pristine.count(NEW), out.count(NEW)))
