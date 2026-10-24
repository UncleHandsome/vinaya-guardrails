# -*- coding: utf-8 -*-
"""284・量（二）：案名三方對位（正口徑）・斜線代號有無圖例・地標 03 缺段・地標 05 生肉・案例 02 兩名・編者語掛「」。"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
LINES = io.open(BOOK, encoding=u'utf-8-sig').read().split(u'\n')
T = u'\n'.join(LINES)
i6 = next(i for i, l in enumerate(LINES) if l.startswith(u'# 第六章'))
i7 = next(i for i, l in enumerate(LINES) if l.startswith(u'# 第七章'))
i4 = next(i for i, l in enumerate(LINES) if l.startswith(u'# 附錄四'))
i5 = next(i for i, l in enumerate(LINES) if l.startswith(u'# 附錄五'))

print(u'【一・三方案名對位（矩陣・地標案號列・附錄四）】')
mat, lane, apx = {}, {}, {}
for i in range(i6, i7):
    l = LINES[i]
    m = re.match(u'^\\| \\*\\*〔案例 ?0*(\\d+)[^〕]*〕\\*\\*<br>\\*\\*([^*]+)\\*\\*', l)
    if m:
        mat.setdefault(int(m.group(1)), set()).add(m.group(2).strip())
    m = re.match(u'^\\* \\*\\*案號\\*\\*：(.*)$', l)
    if m:
        for n, nm in re.findall(u'〔案例 ?0*(\\d+)〕([^〔｜\\n]{1,34})', m.group(1)):
            lane.setdefault(int(n), set()).add(nm.strip(u'・， ')[:24])
for i in range(i4, i5):
    m = re.match(u'^\\| \\*\\*〔案例 ?0*(\\d+)〕([^|]{1,34})\\*\\*', LINES[i])
    if m:
        apx.setdefault(int(m.group(1)), set()).add(m.group(2).strip())
print(u'  載體數：矩陣 %d・地標案號列 %d・附錄四 %d' % (len(mat), len(lane), len(apx)))
bad = []
for n in sorted(set(apx) & (set(mat) | set(lane))):
    a = apx[n]
    b = mat.get(n, set()) | lane.get(n, set())
    if b and not (a & b):
        bad.append((n, sorted(a), sorted(b)))
print(u'  名不相同之案：%d' % len(bad))
for n, a, b in bad[:20]:
    print(u'   案%-3d 附錄四%s ←→ 正文%s' % (n, a, b))

print(u'【二・斜線代號之圖例】')
for k in (u'舊錄', u'台帳', u'代號', u'遮＝', u'對讀之次', u'尼薩耆', u'次序'):
    hs = [i + 1 for i, l in enumerate(LINES) if k in l]
    print(u'  『%s』：%d 見 %s' % (k, len(hs), hs[:10]))

print(u'【三・地標 03 段標題全文】')
for i in range(4325, 4436):
    if LINES[i].startswith(u'#### '):
        print(u'  L%d| %s' % (i + 1, LINES[i][:60]))

print(u'【四・地標 05 之逐字回查（生肉處）】')
for i in range(4542, 4650):
    if u'律典原典逐字回查' in LINES[i] or (LINES[i].startswith(u'> ') and u'卷' in LINES[i][:40]):
        print(u'  L%d| %s' % (i + 1, LINES[i][:240]))
for i in range(4542, 4650):
    if u'自今已去聽白已' in LINES[i] or u'云何僧與作不同住僧與作' in LINES[i]:
        print(u'  【生肉行】L%d| %s' % (i + 1, LINES[i][:400]))

print(u'【五・案例 02 兩名】')
for i, l in enumerate(LINES):
    if re.search(u'〔案例 ?0*2〕', l) or re.search(u'〔案例 ?0*2 ', l):
        print(u'  L%d| %s' % (i + 1, l[:170]))

print(u'【六・編者語掛「」之兩處】')
for n in (6815, 3501):
    print(u'  L%d| %s' % (n, LINES[n - 1][:300]))
