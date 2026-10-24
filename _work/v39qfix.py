# -*- coding: utf-8 -*-
"""第 256 輪・逐字回填器：把 ver39【律典原典】內掛了引號卻不合語料之段，回語料取真逐字。

法（機械一口徑，不手撰一字）：
  一・對齊器 `_work/v39align.py`：以段之前綴錨於語料歸一串求候點，覆蓋面與跨度相似面俱過閘者方出候選；
      候選即**語料原文**（帶其標點；跨遠者以『……』相綴，合本書刪節號之制；語料自身引號折為『』並調平）。
  二・候選須即送 `_tk.classify` 自證逐字——不自證者不取。
  三・**以一整段引文為裁单位**：段內諸缺句俱得候選者，照候選回填；
      有一缺句無解者，整段不掛引號並冠以「律意：」——自此不充逐字（依第五輪『去引號改撮要』之舊例）。
  四・落檔須錨點恰中一次、行數不動，寫後回讀並重跑 `_work/v39quote.py`＋`_work/v39chk.py`。
範口徑：唯【律典原典】欄・唯已過出處閘門者；段長六字以下不校。

用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/v39qfix.py                 # 只報
      PYTHONIOENCODING=utf-8 python -X utf8 _work/v39qfix.py apply           # 落回填
      PYTHONIOENCODING=utf-8 python -X utf8 _work/v39qfix.py apply deq       # 並去無解段之引號
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (ROOT, os.path.join(ROOT, u'_work')):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import _tk                                                     # noqa: E402
import v39align                                                # noqa: E402

APPLY = u'apply' in sys.argv
DEQ = u'deq' in sys.argv and APPLY
ELL = _tk.ELL
Q = re.compile(u'\u300c([^\u300c\u300d]+)\u300d')               # 單行內之 「…」
VERB = re.compile(u'^#### 【律典原典】\\s*$')
HEAD = re.compile(u'^(#{1,6} |---\\s*$)')
CARD = re.compile(u'^### 〔(案例|補遺) (\\d+)〕')
SPEAK = re.compile(u'\u300f[^\u300c\u300f]{0,12}\u8a00\\s*[\uff1a:]')   # 『…』X言：『…』 內層引語之接放處（換人說話）

nfile, nsize = v39align.corpus_size()
print(u'語料 %d 檔・歸一 %s 字｜閘 cov≥%.2f・ratio≥%.2f｜模式 %s' % (
    nfile, format(nsize, u','), v39align.MINCOV, v39align.MINRATIO,
    (u'回填＋去引號' if DEQ else (u'落回填' if APPLY else u'只報'))))

LINES = _tk.MAIN_LINES
hits, leaves, edits, dq = [], [], {}, []
cur = None
i = 0
while i < len(LINES):
    m = CARD.match(LINES[i])
    if m:
        cur = u'%s%s' % (m.group(1), m.group(2))
    if not VERB.match(LINES[i]):
        i += 1
        continue
    src = False
    j = i + 1
    while j < len(LINES) and not HEAD.match(LINES[j]):
        if not src and _tk.SRC_STRICT.search(LINES[j]):
            src = True
        if src:
            line = LINES[j]
            new = line
            for q in Q.findall(line):
                v, bad = _tk.classify(q)
                if v != u'miss':
                    continue
                fixed, broken = [], []
                for p, lp in bad:
                    anchor = next((x for x in ELL.split(q) if _tk.norm(x) == p), None)
                    r = v39align.realign(p)
                    if r is None:
                        broken.append((p, u'無候點（前綴%d）' % lp))
                    elif _tk.classify(r[2])[0] not in (u'hit', u'skip'):
                        broken.append((p, u'候選不自證 cov%.2f' % r[0]))
                    elif anchor is None:
                        broken.append((p, u'錨不中'))
                    else:
                        fixed.append((p, r[2], r[0]))
                if not broken:
                    nq = q
                    why = None
                    for p, cand, cov in fixed:
                        a = next(x for x in ELL.split(nq) if _tk.norm(x) == p)   # 於引文之內求錨，勿及行首
                        if SPEAK.search(a):
                            why = u'錨跨語頭（『…』X言：…』之類，換人說話處不可代削）'
                            break
                        nq = nq.replace(a, cand, 1)
                    if why is None:
                        nqn = _tk.norm(nq)
                        for p, cand, cov in fixed:
                            if nqn.count(_tk.norm(cand)) > 1:
                                why = u'候選與同段他句重出（恐錯拾語料另一例）'
                                break
                    if why:
                        leaves.append((cur, j + 1, p, why))
                        if DEQ:
                            dq.append((j, q))
                    else:
                        wrapped = u'\u300c%s\u300d' % q
                        assert new.count(wrapped) == 1, u'引號段須恰中一次 L%d' % (j + 1)
                        new = new.replace(wrapped, u'\u300c%s\u300d' % nq, 1)
                        for p, cand, cov in fixed:
                            hits.append((cur, j + 1, p, cand, cov))
                else:
                    for p, why in broken:
                        leaves.append((cur, j + 1, p, why))
                    if DEQ:
                        dq.append((j, q))
            if new != line:
                edits[j] = new
        j += 1
    i = j

print(u'———— 整段回填 %d 段・無解 %d 段・待去引號 %d 段・涉行 %d' % (
    len(hits), len(leaves), len(dq), len(edits)))
for c, ln, p, cand, cov in hits:
    print(u'◐ %-8s L%-5d cov%.2f｜%s' % (c, ln, cov, p[:22]))
    print(u'      → %s' % cand[:110])
for c, ln, p, why in leaves:
    print(u'● %-8s L%-5d %s｜%s' % (c, ln, why, p[:30]))
io.open(os.path.join(ROOT, u'_work', u'_q256res.json'), 'w', encoding=u'utf-8').write(
    json.dumps({u'mincov': v39align.MINCOV, u'mode': (u'deq' if DEQ else (u'apply' if APPLY else u'report')),
                u'hits': [[c, ln, p, cov] for c, ln, p, _cd, cov in hits],
                u'leaves': [[c, ln, p, w] for c, ln, p, w in leaves],
                u'deq': [[ln + 1, q[:40]] for ln, q in dq]},
               ensure_ascii=False, indent=1))

if not APPLY:
    sys.exit(0)
n2 = list(LINES)
for k, v in edits.items():
    assert LINES[k] != v, u'改文須異於原文'
    n2[k] = v
dq_done = 0
for k, q in dq:
    wrapped = u'\u300c%s\u300d' % q
    if wrapped not in n2[k]:
        print(u'  ! 去引號錨不中 L%d，略' % (k + 1))
        continue
    assert n2[k].count(wrapped) == 1, u'引號段須恰中一次 L%d' % (k + 1)
    n2[k] = n2[k].replace(wrapped, u'律意：%s' % q, 1)
    dq_done += 1
assert len(n2) == len(LINES), u'行數不動'
assert edits or dq_done, u'無可改之行'
io.open(_tk.SRC, 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(n2))
back = io.open(_tk.SRC, encoding=u'utf-8').read().split(u'\n')
assert len(back) == len(LINES), u'回讀行數不合'
touched = set(list(edits.keys()) + [x[0] for x in dq])
for k in touched:
    assert back[k] == n2[k], u'回讀不符 L%d' % (k + 1)
print(u'———— 已落檔 %d 行（回填 %d 段・去引號 %d 段）・回讀相符（%d 行 → %d 行）' % (
    len(touched), len(hits), dq_done, len(LINES), len(back)))
