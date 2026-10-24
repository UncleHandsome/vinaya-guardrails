# -*- coding: utf-8 -*-
"""274 輪・目錄同步：新稿改兩題，卷首目錄隨之（第三節正名・閘門二（續）之目除）。

依『目錄不指空』（第 11 目）而治：新稿之第一章第三節題作「八大正理規範衝突時的五大裁量階梯」，
且「閘門二（續）　四大臨界標尺」一題已降為閘門二之內款（草稿自陳『降格為自然對稱之款』）——
故目錄一條改題、一條除目。**只動目錄之兩行，不動冊身。**
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r274toc.py [--undo]
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_work')
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
SRC = os.path.join(ROOT, NAME)
BAK = os.path.join(WORK, u'r274toc.bak')
NEW = io.open(os.path.join(WORK, u'r274new3.md'), encoding=u'utf-8-sig').read()

if u'--undo' in __import__('sys').argv:
    import shutil
    shutil.copyfile(BAK, SRC)
    print(u'\u56de\u9000\u5b8c\u6210')
    raise SystemExit(0)

L = io.open(SRC, encoding=u'utf-8').read().split(u'\n')
io.open(BAK, 'w', encoding=u'utf-8').write(u'\n'.join(L))
BODY0 = next(i for i, l in enumerate(L) if l.startswith(u'# \u7b2c\u4e00\u7ae0'))   # 目錄只在前文之內求

# 新稿之第一章第三節實題（自檔讀入，不重打）
m = re.search(u'(?m)^### \u7b2c\u4e09\u7bc0\u3000(.+)$', NEW)
assert m, u'\u65b0\u7a3f\u7b2c\u4e09\u7bc0\u984c\u4e0d\u53ef\u6c42'
H3 = m.group(1).strip()
print(u'\u65b0\u7a3f\u7b2c\u4e09\u7bc0\u984c\uff5c\u300e%s\u300f' % H3[:40])

i39 = next(i for i in range(BODY0) if L[i].lstrip().startswith(u'* \u7b2c\u4e09\u7bc0\u3000\u53f8\u6cd5\u5929\u5e73'))
old39 = L[i39]
L[i39] = u'    * \u7b2c\u4e09\u7bc0\u3000' + H3 + u'\uff08\u4e94\u5927\u512a\u5148\u88c1\u91cf\u4f4d\u968e\u3001\u4f46\u66f8\u540c\u7fa9\u53cd\u8986\u4e4b\u6cbb\u3001\u8fce\u56de\u300a\u4e94\u652f\u7269\u4e3b\u7d93\u300b\uff09'
print(u'L%d \u6539\u984c\uff5c\u65e7\u300e%s\u300f' % (i39 + 1, old39.strip()[:38]))
print(u'      \u65b0\u300e%s\u300f' % L[i39].strip()[:56])

k = [i for i in range(BODY0) if L[i].lstrip().startswith(u'* \u9598\u9580\u4e8c\uff08\u7e8c\uff09')]
assert len(k) == 1, u'\u9598\u9580\u4e8c\uff08\u7e8c\uff09\u76ee\u9304\u689d %d \u7b46' % len(k)
print(u'L%d \u9664\u76ee\uff5c\u300e%s\u300f' % (k[0] + 1, L[k[0]].strip()[:44]))
del L[k[0]]

io.open(SRC, 'w', encoding=u'utf-8').write(u'\n'.join(L))
print(u'\u76ee\u9304\u540c\u6b65\u5b8c\u6210\uff5c\u6587\u4ef6\u884c %d \u2192 %d' % (len(L) + 1, len(L)))
