# -*- coding: utf-8 -*-
"""第 256 輪・逐字債之候補器：ver39 之【律典原典】非逐字段，逐一於 ver38 完卡之◎原典求『 donating 段』。

法：兩側俱以 `_tk.norm` 折異體・拆字・去標點後比最長共同子串；命中率 = 共串長 / 待補段長。
    供體須自證逐字（`_tk.classify` == hit），否則不候。只報不改。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/v39qdonor.py [最低命中率，預設 .55]
"""
import difflib
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import _tk                                                     # noqa: E402

MINR = float(sys.argv[1]) if len(sys.argv) > 1 else 0.55
OLD = [q for q in os.listdir(ROOT) if q.startswith(u'ver38') and q.endswith(u'.md')][0]
ol = io.open(os.path.join(ROOT, OLD), encoding=u'utf-8-sig').read().split(u'\n')

# ── 供體：ver38 第六章◎原典之 「」 段（須自證逐字）
donors = []
case = None
in_o = False
CASE_RE = re.compile(u'^####\\s*〔(遮|開|僧)(\\d+)〕\\s*(.*)$')
for i, l in enumerate(ol):
    m = CASE_RE.match(l)
    if m:
        case = u'%s%s' % (m.group(1), m.group(2))
        in_o = False
        continue
    if l.strip().startswith(u'◎原典'):
        in_o = True
        continue
    if in_o and (l.strip() == u'---' or l.startswith(u'##')):
        in_o = False
    if in_o and l.lstrip().startswith(u'>'):
        for q in _tk.Q_RE.findall(l):
            if _tk.classify(q)[0] == u'hit':
                donors.append((case, i + 1, q, _tk.norm(q)))
print(u'供體：ver38 逐字原典段 %d 枚（卡 %d 枚）' % (len(donors), len({d[0] for d in donors})))

# ── 待補：ver39【律典原典】之非逐字段
nl = _tk.MAIN_LINES
VERB = re.compile(u'^#### 【律典原典】\\s*$')
HEAD = re.compile(u'^(#{1,6} |---\\s*$)')
CARD = re.compile(u'^### 〔(案例|補遺) (\\d+)〕')
todo = []
cur = None
i = 0
while i < len(nl):
    m = CARD.match(nl[i])
    if m:
        cur = u'%s%s' % (m.group(1), m.group(2))
    if VERB.match(nl[i]):
        src = False
        j = i + 1
        while j < len(nl) and not HEAD.match(nl[j]):
            if not src and _tk.SRC_STRICT.search(nl[j]):
                src = True
            for q in _tk.Q_RE.findall(nl[j]):
                v, bad = _tk.classify(q) if src else (u'gate', [])
                if v == u'miss':
                    for p, lp in bad:
                        todo.append((cur, j + 1, q, p, len(p), lp))
            j += 1
        i = j
    else:
        i += 1
print(u'待補：%d 段（卡 %d 枚）\n' % (len(todo), len({t[0] for t in todo})))

hit = 0
for card, ln, q, seg, L, lp in todo:
    best = None
    for dc, dl, dq, dn in donors:
        m = difflib.SequenceMatcher(None, seg, dn, autojunk=False).find_longest_match(0, len(seg), 0, len(dn))
        if m.size >= 8 and (best is None or m.size > best[1]):
            best = (dc, m.size)
        if best and best[1] >= len(seg) * 0.9:
            break
    r = (best[1] / float(L)) if best else 0.0
    if r >= MINR:
        hit += 1
        print(u'◐ %-8s L%-6d 供 %s 共%d/%d=%.2f  待補%s字｜%s' % (
            card, ln, best[0], best[1], L, r, L, seg[:26]))
    else:
        print(u'● %-8s L%-6d 無供（最共 %s）待補%d字・前綴%d｜%s' % (
            card, ln, (u'%s@%d' % (best[0], best[1])) if best else u'-', L, lp, seg[:26]))
print(u'———— 候得供體 %d / 待補 %d（門檻 %.2f）' % (hit, len(todo), MINR))
