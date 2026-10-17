# -*- coding: utf-8 -*-
# r225toc　卷首手寫目錄之『歸章』須與印面標題層相符（第 225 輪立，長駐・專軸）
#
#   所以立之：第 225 輪外路報來一案——目錄把【章末指針：從公堂急診，走向自心免疫】列在第四章末，
#   而印面此插片實在第五章末（L4663，第五章起 L3615、第六章起 L4681）。歷輪之檢唯校
#   『列其目→有其題』與『有其題→列其目』（第 142 輪之雙向、不變量 60），**兩向皆不問其目掛於何章**：
#   條目在、標題亦在，故 misplaced 而全綠。此即『以字面為鍵之表』之名冊又漏一格（208／223／224 同族）。
#
#   口徑：① 目錄區塊（起『## 【全書開卷標準目錄】』，至第一個『# 第X章』前）逐條解析為
#        『單元頂條 + 其下縮排子目』；頂條之職=章（H1）或卷首_unit（H2），附錄區塊之職=附錄H1群。
#   ② 單元之『地界』自其標題行起，至下一個同級或更粗之標題止（章→下个 H1；卷首_unit→下个 H2 或 H1）。
#   ③ 子目配對：剝粗體與空白後，若子目與該地界內某標題逐字同、或子目以該標題為前綴（目錄加括註）、
#        或該標題以子目為前綴，皆算相符。正向（目→題）與反向（題→目）俱校，反向唯取該地界之 H3
#        （H4 以下乃款級，目錄不列，強校即生假陽性；第 209 輪『通例常在假設之外』之誡）。
#   ④ 源檔隨 `_tk.SRC`（TKSRC 植病副本可測）。
#   用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r225toc.py [--list]
from __future__ import unicode_literals
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as T

LINES = T.LINES
SP = re.compile(u'[' + chr(32) + chr(9) + u']+')


def norm(s):
    s = s.strip().replace(u'**', u'').replace(u'`', u'')
    while s.startswith(u'*'):
        s = s[1:].strip()
    return SP.sub(u'', s)


def core(s):
    """剝盡尾端之全形括註，取其骨——目錄常於實題之後加括註，印面亦常以括註存目之别。"""
    s = norm(s)
    while s.endswith(u'）'):
        k = s.rfind(u'（')
        if k < 0:
            break
        s = s[:k]
    return s


def head_title(s):
    s = s.strip()
    for pre in (u'##### ', u'#### ', u'### ', u'## ', u'# '):
        if s.startswith(pre):
            return s[len(pre):].strip(), len(pre) - 1
    return None, 0


# 一、目錄區塊之範圍
toc_start = [i for i, l in enumerate(LINES) if l.strip() == u'## 【全書開卷標準目錄】']
assert len(toc_start) == 1, u'目錄之起點非恰一：%s' % toc_start
toc_end = [i for i in range(toc_start[0] + 1, len(LINES)) if LINES[i].startswith(u'# 第')]
assert toc_end, u'目錄之後無章界'
TOC = toc_end[0]

# 二、印面所有標題（含級別與行號）
HEADS = []
for i, l in enumerate(LINES):
    t, lvl = head_title(l)
    if t is not None:
        HEADS.append((i, lvl, t))

# 三、章與卷首單元之地界
REG = []
for i, lvl, t in HEADS:
    if lvl not in (1, 2) or (toc_start[0] <= i < TOC):    # 目錄區塊自身不入围（章界行即 TOC，須入）
        continue
    nxt = len(LINES)
    for j, lvl2, t2 in HEADS:
        if j > i and lvl2 <= lvl:
            nxt = j
            break
    REG.append((core(t), i, nxt, lvl, t))


def find_reg(ntitle):
    c = core(ntitle)
    for r in REG:
        if r[0] == c or c.startswith(r[0]) or r[0].startswith(c):
            return r
    return None


# 附錄區塊之特例：頂條『附錄』之轄境＝自附錄A 起至全檔末
app_start = [i for i, l in enumerate(LINES) if l.startswith(u'# 附錄A')]
assert len(app_start) == 1, u'附錄A 之起點非恰一'
# 第 250 輪：底冊四篇另檔，附錄區之轄境止於主檔末（備檔之篇不復由目錄求其目）
APPENDIX = (u'附錄', app_start[0], T.N_MAIN if hasattr(T, 'N_MAIN') else len(LINES), 1, u'附錄區')

# 四、解析目錄：頂條與子目
blocks = []
cur = None
for i in range(toc_start[0] + 1, TOC):
    s = LINES[i]
    if not s.strip():
        continue
    top = s.startswith(u'* **') or s.startswith(u'* ') and s.strip().startswith(u'**')
    sub = s.startswith(u'  * ') or s.startswith(u'   * ')
    if top and not sub:
        cur = (norm(s), i, [])
        blocks.append(cur)
    elif sub and cur is not None:
        cur[2].append((norm(s[4:]), i + 1))

if u'--list' in sys.argv:
    for nt, ln, ents in blocks:
        r = find_reg(nt) or (APPENDIX if u'附錄' in nt else None)
        print(u'L%-5d 頂條 %-42s → %s｜子目 %d'
              % (ln + 1, nt[:42], (r[1] + 1, r[2]) if r else u'❓未定位', len(ents)))
    sys.exit(0)

def fit(a, b):
    return a == b or a.startswith(b) or b.startswith(a)


def e_head(lines, j):
    t, _lv = head_title(lines[j])
    return t or lines[j].strip()


miss = []
for nt, ln, ents in blocks:
    r = APPENDIX if nt == u'附錄' else find_reg(nt)
    if r is None:
        miss.append((u'頂條無所屬之地界', ln + 1, nt[:40]))
        continue
    lo, hi = r[1], r[2]
    if r is APPENDIX:
        lo -= 1                      # 附錄區塊之子目即各附錄之 H1 本體，首篇亦須入境
    want_lv = 1 if r is APPENDIX else 3   # 附錄區之子目乃各篇 H1；他區之子目乃節級 H3
    got = [(j, core(t)) for j, lv, t in HEADS if lo < j < hi and lv == want_lv]
    for e, eln in ents:
        ce = core(e)
        if not any(fit(ce, g) for _, g in got):
            miss.append((u'目不屬其所掛之單元', eln, e[:44] + u'（單元：' + nt[:22] + u'）'))
    for j, g in got:
        if not any(fit(core(e), g) for e, _ in ents):
            miss.append((u'單元內有題而目錄未列', j + 1, e_head(LINES, j)[:44] + u'（單元：' + nt[:22] + u'）'))

print(u'目錄區塊 L%d–L%d｜單元 %d 個｜子目 %d 條｜病 %d 處%s'
      % (toc_start[0] + 1, TOC, len(blocks), sum(len(b[2]) for b in blocks), len(miss),
         u' []' if not miss else u''))
for kind, ln, info in miss:
    print(u'   %s｜L%-6d %s' % (kind, ln, info))
sys.exit(1 if miss else 0)
