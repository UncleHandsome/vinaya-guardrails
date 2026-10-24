# -*- coding: utf-8 -*-
"""第 256 輪・ver39 逐字口徑（债⑤之清）：卡身【律典原典】之 「」 引文，逐段對本地語料。

口徑一仍 `_tk` 之舊約：（甲）**出處閘門**——引號段而其前未見《…》・卷N・犍度等出處者，
      屬術語標注，不作逐字宣稱；（乙）**刪節號切段**＋**norm 折異體與拆字**；
      （丙）段長四字以下不校（避「五錢」一類術語誤中）。
範圍＝`_CD.src_blocks` 所定之宣稱區（原典欄・及自標『◎原典』或卷段之段）——276 續改按**句式**劃，
      因第六章改製後一案一卡之形已廢，而補遺十五則之引律文者向在兩張名單之縫外。只報不改（改須另刀）。

用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/v39quote.py [-v]
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import _casedef as CD                                              # 276・原典欄之共器
import _tk                                                     # noqa: E402  語料・norm・classify 之法源

SRC_PATH = next((a for a in sys.argv[1:] if not a.startswith(u'-')), None)   # 276 續・試跑通道：量假冊而不動正本
if SRC_PATH:
    LINES = io.open(SRC_PATH, encoding=u"utf-8-sig").read().replace(u"\r\n", u"\n").split(u"\n")
else:
    LINES = _tk.MAIN_LINES

verbose = u'-v' in sys.argv
rows = []            # (隸屬, 行, 引文, verdict, bad, 依)
skipped = 0          # 同線左側冠出處者——尺三之職，此不重校
for a, b, lab, dep in CD.src_blocks(LINES):
    txt = u'\n'.join(LINES[a:b])                # 併區而校：一「……」可跨數行（276 大黑牛之盲處即在此）
    for m in _tk.Q_RE.finditer(txt):
        ln = a + txt[:m.start()].count(u'\n')
        col = m.start() - (txt.rfind(u'\n', 0, m.start()) + 1)
        if _tk.SRC_STRICT.search(LINES[ln][:col]):
            skipped += 1
            continue
        if dep == u'段' and not CD.is_quote_line(LINES[ln]):
            continue                                 # 攝述清單內之術語，不作逐字宣稱
        v, bad = _tk.classify(m.group(1))
        rows.append((lab, ln + 1, m.group(1), v, bad, dep))

tally = {}
for _c, _l, _q, v, _b, _d in rows:
    k = v if not v.startswith(u'other') else u'other'
    tally[k] = tally.get(k, 0) + 1
BLK = CD.src_blocks(LINES)
nb = {}
for _a, _b, _l, dep in BLK:
    nb[dep] = nb.get(dep, 0) + 1
print(u'語料：%d 檔・norm 後 %s 字｜宣稱區 %d（原典欄 %d・自標出處之段 %d）｜逐字宣稱 %d 段・他典 %d・讓於尺三（同線冠出處）%d' % (
    len([1 for f in os.listdir(os.path.join(ROOT, u'原文')) if f.endswith(u'.txt')]),
    format(len(_tk.VINAYA), u','), len(BLK), nb.get(u'欄', 0), nb.get(u'段', 0),
    len(rows), tally.get(u'other', 0), skipped))
print(u'判定分布：%s' % u'・'.join(u'%s %d' % (k, v) for k, v in sorted(tally.items())))
miss = [r for r in rows if r[3] == u'miss']
print(u'———— 非逐字 %d 段（犯之者 %d 區）' % (len(miss), len({r[0] for r in miss})))
for c, l, q, v, bad, dep in miss:
    print(u'  ✗ %-4s %-14s L%-6d %s' % (dep, c, l, q[:34].replace(u'\n', u'')))
    for p, lp in bad[:2] if not verbose else bad:
        print(u'        段%d字・前綴合 %d｜%s' % (len(p), lp, p[:44]))
print(u'———— 他典（OTHER）命中之段：%s' % (u'・'.join(
    sorted({r[3][6:] for r in rows if r[3].startswith(u'other')})) or u'無'))
sys.exit(1 if miss else 0)
