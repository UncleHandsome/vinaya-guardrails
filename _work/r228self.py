# -*- coding: utf-8 -*-
# r228self　指針不得指其自身所在之節（第 228 輪立，長駐・專軸）
#
#   所以立之：第四章第一節第二款數位延伸條舊云『依本章第一節「經三次合法傳喚不到」之缺席例』——
#   該句本身即在第一章第一節之內，**指針指回自己**，讀者循鏈而行原地打轉；第九章第四節亦有同病
#   （『依本章第四節第八至十款』）。歷輪之針檢（`r195ref` 校章級之有所至、`krefstrict` 與附錄K 校款級之確存、
#   `anchorref` 校版面承接）**只問其所指存否，不問所指是否即其自身**——存而自指，鏈雖合而義已虛。
#   第 228 輪外路報『法源循環虛懸』，親量得二處，俱改從『本節』或款級。
#
#   口徑：① 章界取 H1『# 第N章』、節界取 H3『### 第N節』；遇非此式之 H1／H3（如第六章案例題）則擲其所屬為空，
#      空則不校（無從判自指）；② 兩式俱校：『本章第X節』與『第N章第X節』（後者乃以他稱行自指之形）；
#      ③ 底冊不校（記錄轉述舊形，218／226 之裁）；④ 圍欄內不校（圖中欄寬之文非指針，221『容器』之誡）；
#      ⑤ 指至『本章第N款／本節』之自稱不在此限（自稱本節乃正格）；⑥ 表列（行首『|』）不校——
#         三十格矩陣等表之指針須就單格自足，通例全帶章名（『說在第二章第五節治理通則』），非原地打轉之病。
#   升閘：自指一處即退 1。負測四路見 `_work/r228negtest.py`。
#   用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r228self.py
from __future__ import unicode_literals
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as T

LINES = T.LINES
BOT = T.bottom_lines()
CN = {u'一': 1, u'二': 2, u'三': 3, u'四': 4, u'五': 5, u'六': 6, u'七': 7, u'八': 8, u'九': 9}
H1CH = re.compile(u'^# 第([一二三四五六七八九])章')
H3SE = re.compile(u'^### 第([一二三四五六七八九])節')
P_SELF = re.compile(u'本章第([一二三四五六七八九])節')
P_EXPL = re.compile(u'第([一二三四五六七八九])章第([一二三四五六七八九])節')

fence, inf = [], False
for l in LINES:
    if l.strip().startswith(u'```'):
        inf = not inf
    fence.append(inf)

bad = []
n = 0
ch = se = None
for i, l in enumerate(LINES):
    if i in BOT or fence[i]:
        continue
    if l.lstrip().startswith(u'|'):
        continue                      # 表列之指針須就單格自足（三十格矩陣通例作『說在第X章第X節』），不校
    m = H1CH.match(l)
    if m:
        ch, se = CN[m.group(1)], None
        continue
    if l.startswith(u'# '):
        ch, se = None, None
        continue
    m = H3SE.match(l)
    if m:
        se = CN[m.group(1)]
        continue
    if l.startswith(u'### ') and not m:
        se = None                     # 非『第N節』式之 H3（如第六章案例題）：其內無節可自指
    if se is None or ch is None:
        continue
    n += 1
    for mm in P_SELF.finditer(l):
        if CN[mm.group(1)] == se:
            bad.append((i + 1, u'本章第%s節' % mm.group(1), ch, se, l.strip()[:64]))
    for mm in P_EXPL.finditer(l):
        if CN[mm.group(1)] == ch and CN[mm.group(2)] == se:
            bad.append((i + 1, u'第%s章第%s節' % (mm.group(1), mm.group(2)), ch, se, l.strip()[:64]))

print(u'印面可校之頁 %d 行｜自指之針 %d 處%s' % (n, len(bad), u' []' if not bad else u''))
for ln, txt, c, s, frag in bad[:12]:
    print(u'   L%-6d 身處第%s章第%s節而云『%s』｜%s…' % (ln, c, s, txt, frag))
sys.exit(1 if bad else 0)
