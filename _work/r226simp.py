# -*- coding: utf-8 -*-
# r226simp　底冊（修訂誌・款級台帳・驗收卡・校勘記・終卷）引號外之簡形（第 226 輪立，長駐・專軸）
#
#   所以立之：第 69 檢『引號外無簡體孤立字』依第 218 輪在案之裁定**不掃底冊**（底冊自述舊形與異體，
#   依『編年不回改』之例不較）。然簡形與舊形異體不同職：語料乃漢文大正藏、印面乃繁體，
#   **編者手筆一旦落簡，必是誤字而绝非照錄**——第 226 輪即以手製探針量得一枚『诸』落於第 212 輪之校勘記
#   （在『』之內故印面之檢向不較，而 `_tk.SIMP_ONLY` 與 `recordsimp.S` 兩名單亦俱無此字，遂歷十三輪無感）。
#   此即『名單之外』（61／174／216）與『記錄自犯』（180／221）兩族之交：名額兩張而守者只取其各一。
#
#   口徑：① 區唯取底冊（印面已有第 69 檢守之，不duplicate）；② 引號之豁免走**巢套深度**而非同線正則
#   （第 220 輪之誡：同線剝法遇跨行之巢必錯位而露其字）；③ 名單取 `_tk.SIMP_ONLY` ∪ `_simpmap.S` 之**並集**
#   （第 216 輪之誡：兩者不等，取其一是漏）；④ 述舊形須以碼位或圍以引號，此制有第 221 輪之先例。
#   升閘：底冊引號外現一枚即退 1。負測三路見 `_work/r226negtest.py`（⓪ 淨本、⑧ 植一枚、⑨ 圍以『』而勿報）。
#   源檔隨 `_tk.SRC`（故 TKSRC 之植病副本可測）。
#   用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r226simp.py
from __future__ import unicode_literals
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as T

HERE = os.path.dirname(os.path.abspath(__file__))
NL = chr(10)

# 一、名單之並集：`_tk.SIMP_ONLY`（印面之檢所用）∪ `_simpmap.S`（記錄與記憶兩器所用；第 238 輪歸一）
src = open(T.__file__, encoding='utf-8').read().split(NL)


def grab(text, head):
    k = [n for n, l in enumerate(text) if l.strip().startswith(head)][0]
    expr, bal = u'', 0
    for l in text[k:]:
        frag = l.split(u'=', 1)[1] if u'=' in l.split(u'#')[0] else l
        frag = frag.split(u'#')[0].strip().rstrip(u'\\').strip()
        expr += u' ' + frag
        bal += frag.count(u'(') - frag.count(u')')
        if bal <= 0:
            break
    return eval(expr.strip(), {}, {})


SO = grab(src, u'SIMP_ONLY')
RS = None                      # 第 238 輪：名單已歸 `_simpmap`，不再刮 recordsimp 之碼面（刮碼面者，改碼即斷）
import _simpmap as _SM
S = set(_SM.S)
BAN = set(SO) | S
assert len(SO & S) > 100, u'兩名單竟大異：%d 共' % len(SO & S)

# 二、巢套深度：引號之內不較（跨行亦須豁免）
BOT = T.bottom_lines()
hits, q1, q2, row = [], 0, 0, 0
buf = set()
for ch in T.DOC:
    if ch == NL:
        if buf and row in BOT:
            for c in buf:
                hits.append((row + 1, c))
        buf = set()
        row += 1
        continue
    if ch == u'「':
        q1 += 1
    elif ch == u'」':
        q1 = max(0, q1 - 1)
    elif ch == u'『':
        q2 += 1
    elif ch == u'』':
        q2 = max(0, q2 - 1)
    elif q1 == 0 and q2 == 0 and ch in BAN:
        buf.add(ch)
if buf and row in BOT:                       # 主檔末行無換行符，末例須另 flush
    for c in buf:
        hits.append((row + 1, c))

print(u'名單並集 %d（_tk %d｜_simpmap %d）｜底冊 %d 行｜引號外之簡形 %d 處%s'
      % (len(BAN), len(SO), len(S), len(BOT), len(hits), u' []' if not hits else u''))
seen = []
for ln, ch in hits:
    if ch not in seen:
        seen.append(ch)
    print(u'   L%-7d 落『%s』形' % (ln, ch))
sys.exit(1 if hits else 0)
