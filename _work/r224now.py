# -*- coding: utf-8 -*-
# r224now　修訂誌自稱「現行」之表列，其所載篇題必與印面實有標題逐字同（第 224 輪立，長駐・專軸）
#
#   所以立之：附錄C『C-3 總綱節名沿革存檔』表有列標曰「現行第三十八版第一章（六節標準定本）」，
#   而三格猶載舊題（『第一節　立法本懷與唯一判準』『第四節　客觀法治與三大校準』『第二節　…母法』），
#   歷二百餘輪諸軸俱綠——『卷首目錄＝實有標題』之檢只查目錄，查不到這張以篇題為字面之表。
#   此即第 208／223 輪『凡以字面為鍵之表，隨動須連宣稱』之又一形，故不靠手檢而立器。
#
#   口徑：① 篇界取附錄C（其職在記今制，他篇之表不預）；② 只取欄名含「現行」之那一列，
#   其餘列乃舊名之存檔，正是該表之職，不較；③ 只校其形作「**第X節　題**」／「**第X章　題**」者
#   （「*（併入第一節）*」之說明格與分隔格不較）；④ 實題取印面 H1／H3 之全串，逐字對，不作近似匹配。
#   源檔隨 `_tk.SRC`（故 TKSRC 之植病副本可測）。
#   用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r224now.py
from __future__ import unicode_literals
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as T

LINES = T.LINES
TITLES = set()
for l in LINES:
    s = l.strip()
    if s.startswith(u'### '):
        TITLES.add(s[4:].strip())
    elif s.startswith(u'# '):
        TITLES.add(s[2:].strip())

lo = [i for i, l in enumerate(LINES) if l.startswith(u'# 附錄C')]
assert len(lo) == 1, u'附錄C 之篇界非恰一：%s' % lo
hi = [i for i in range(lo[0] + 1, len(LINES)) if LINES[i].startswith(u'# ')]
end = hi[0] if hi else len(LINES)
bad = []
cols = 0
cur = -1
for i in range(lo[0], end):
    s = LINES[i].strip()
    if not s.startswith(u'|'):
        cur = -1
        continue
    cells = [c.strip() for c in s.split(u'|')[1:-1]]
    where = [k for k, c in enumerate(cells) if u'現行' in c]
    if where:
        cur = where[0]
        cols += 1
        continue
    if cur < 0 or cur >= len(cells):
        continue
    cell = cells[cur]
    if not cell.startswith(u'**第'):
        continue
    name = cell.strip(u'*').strip()
    if name not in TITLES:
        bad.append((i + 1, name))

print(u'附錄C 自稱「現行」之欄：%d｜篇題不符 %d 處%s' % (cols, len(bad), u' []' if not bad else u''))
for ln, name in bad:
    print(u'   L%-6d 表載『%s』而印面無此標題' % (ln, name))
sys.exit(1 if bad else 0)
