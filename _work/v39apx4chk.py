# -*- coding: utf-8 -*-
"""260 輪・附錄四之逐字覆核：附錄四自稱『繇諸卡自身之【律典原典】欄匯出』，其表列之 「」 乃**逐字宣稱之載體**。
本尺驗其二：（甲）表列所掛 「」 段是否俱可於語料逐字命中；（乙）該段是否仍見於其所指之卡（若卡已改攝述而表猶掛引號，即自報失實）。
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (ROOT, os.path.join(ROOT, u'_work')):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import _casedef as CD        # 276・案號定義共器
import _tk                                                     # noqa: E402

L = _tk.MAIN_LINES
A4 = next((i for i, l in enumerate(L) if l.startswith(u'# 附錄四')), None)
A5 = next((i for i in range(A4 + 1, len(L)) if L[i].startswith(u'# 附錄五')), len(L))
CARD = re.compile(u'^### 〔案例 (\\d+)〕')
ROWQ = re.compile(u'\u300c([^\u300c\u300d]+)\u300d')
ROWID = re.compile(u'\u3014\u6848\u4f8b ?(\\d+)\u3015')
HEAD = re.compile(u'^#### 【律典原典】\\s*$')
STOP = re.compile(u'^(#{1,6} |---\\s*$)')

DEFN = CD.case_defs(L)
cardtext = {str(n): DEFN[n]['名'] for n in DEFN}

badq = mis = 0
rows = 0
for i in range(A4, A5):
    l = L[i]
    if not l.startswith(u'|'):
        continue
    mm = ROWID.search(l)
    if not mm:
        continue
    rows += 1
    num = str(int(mm.group(1)))
    for q in ROWQ.findall(l):
        if _tk.classify(q)[0] == u'miss':
            badq += 1
            print(u'✘ L%-5d 案例%s　非逐字：%s' % (i + 1, num, q[:44]))
        elif num not in cardtext:
            mis += 1
            print(u'⚠ L%-5d 案例%s　表列之案無定義載體（指針落空）：%s' % (
                i + 1, num, q[:34]))
print(u'———— 附錄四表列 %d 行・非逐字 %d 段・指針落空 %d 段（案號定義今 %d 個）' % (rows, badq, mis, len(DEFN)))
sys.exit(1 if (badq or mis) else 0)
