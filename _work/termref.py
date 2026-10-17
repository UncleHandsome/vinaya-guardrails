# -*- coding: utf-8 -*-
"""termref.py —— 詞條級指針須有所指（第 149 輪立為長駐軸）。

緣起：附錄E〔開2〕行舊註〔梵 Śiśumāra，恆河鱷，見附錄D-2〕——而附錄D-2『律典原生語釋義』本無『失守摩羅』
條（第 80 輪評議『除名鱷魚油』，故不別立）。既有 invariant 只校『附錄X-N 之子目存否』，於此類
**指向某篇而該篇無其條**者全無感；讀者按圖索驥，撲空而無跡。

口徑：印面凡「見／詳／具載／參／說見＋附錄D-2｜D-3」者，其行須至少含該篇一則詞條名（首欄粗體，去 * 後長 ≥2）；
不含即報。底冊（附錄C／K／L／M／終卷）編年與自述不較。
退出碼：病 > 0 即退 1；指針為 0 時如實報數（不以無樣本充綠燈之證），`argv[1]` 可注副本以供負測。
"""
import io, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import _tk as t
if len(sys.argv) > 1:
    L = io.open(sys.argv[1], encoding='utf-8').read().split(u'\n')
else:
    L = t.LINES
底 = set()
for nm in t.BOTTOM_NAMES:
    if t.sec(nm):
        底.update(range(*t.sec(nm)))

def terms_of(rows):
    """取該篇之詞條首欄名（首欄粗體或表列第一格，去修飾而斷於括號）。"""
    out = set()
    for l in rows:
        if not l.strip().startswith(u'|'):
            continue
        c1 = l.strip().strip(u'|').split(u'|')[0].strip()
        c1 = c1.replace(u'*', u'').replace(u'`', u'').strip()
        c1 = re.split(u'[（(／/、，=]', c1)[0].strip()
        if len(c1) >= 2 and not re.match(u'^:?-', c1) and c1 not in (u'律典原生語', u'律典原生名'):
            out.add(c1)
    return out

def cut(pre, st, stop):
    a = [i for i in range(st, stop) if L[i].startswith(pre)]
    return a[0] if a else None
D2, D3 = set(), set()
_s = t.sec(u'附錄D')
if _s:
    d2 = cut(u'### D-2', _s[0], _s[1])
    d3 = cut(u'### D-3', _s[0], _s[1])
    if d2 is not None and d3 is not None:
        D2 = terms_of(L[d2:d3])
    if d3 is not None:
        D3 = terms_of(L[d3:_s[1]])
INV = {u'2': D2, u'3': D3}
PTR = re.compile(u'(?:見|詳|具載|參|說見)\\s*附錄\\s*D-([23])')
bad, n = [], 0
for i, line in enumerate(L):
    if i in 底:
        continue
    for m in PTR.finditer(line):
        n += 1
        pool = INV.get(m.group(1), set())
        win = line[max(0, m.start() - 80):m.start()]          # 指針前 80 字內須實見其所指之詞條
        if not any(x in win for x in pool):
            bad.append((i + 1, m.group(0), line[max(0, m.start() - 46):m.start() + 12]))
print(u'詞條級指針：%d 處｜詞條庫 D-2 %d 條、D-3 %d 條｜落空 %d 處' % (n, len(D2), len(D3), len(bad)))
for ln, g, ctx in bad:
    print(u'  L%-6d 【%s】…%s…' % (ln, g, ctx))
if n == 0:
    print(u'  （今無此類指針——此軸有牙與否以負測為準，勿以零樣本作無病之證）')
sys.exit(1 if bad else 0)
