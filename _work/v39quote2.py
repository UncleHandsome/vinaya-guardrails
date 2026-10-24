# -*- coding: utf-8 -*-
"""第 263 輪・卡外逐字尺（`v39quote` 之盲處）：卡身【律典原典】以外，凡引號之前同線有出處標記者，
皆係『掛出處之逐字宣稱』，須對語料（本律六十卷＋本地所收之他部經論）命中。

口徑三則：
  （一）**引號前須先見出處**——《…》・卷N・犍度・大正藏等標記之起點必在該 「 之左，
        故現代案例中人物之說話（其內偶引《金剛經》）不充宣稱、不入此尺；
  （二）判定一依 `_tk.classify`（norm 折異體拆字・段長四字以下不校・他部經論命中作 other）；
  （三）**未收者須有界**——本地語料未收之典籍（《六祖壇經》《中阿含經》）所引，
        其所在附錄必自標『照錄未覆核／本地語料未收』之界，界在則如實列數，界亡即紅。

退碼：非逐字而未標界者 ≥1 即退 1。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/v39quote2.py [-v]
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, u'_work'))
import _tk                                                     # noqa: E402

SRC_PATH = next((a for a in sys.argv[1:] if not a.startswith(u"-")), None)          # 274 輪・試跑通道：量假冊而不動正本
if SRC_PATH:
    LINES = io.open(SRC_PATH, encoding=u"utf-8-sig").read().split(u"\n")
else:
    LINES = _tk.MAIN_LINES
Q = _tk.Q_RE
GATE = _tk.SRC_STRICT

# ── 與尺二之分工（276 續）：兩尺各按**引號同線之左有無出處**判，天然互斥，故不再按區擯除——
#     舊制擯『#### 【律典原典】』一形，該形今廢；若仍按區擯之，則區內同線冠出處者兩尺皆不校，反開新縫。
import _casedef as CD                                              # noqa: E402  只取區數以實報

# ── 印面範圍（終卷一块不入）
END = next((k for k, l in enumerate(LINES) if l.startswith(u'# 終卷')), len(LINES))
ENDN = next((k for k in range(END + 1, len(LINES)) if LINES[k].startswith(u'# ')), len(LINES))

# ── 區域名（最近之 H1）
H1 = [(k, l.strip()[:22]) for k, l in enumerate(LINES) if l.startswith(u'# ')]


def region_of(idx):
    cur2 = u'卷首'
    for k, h in H1:
        if k <= idx:
            cur2 = h
        else:
            break
    return cur2


def block_text(name_prefix):
    ks = [k for k, l in enumerate(LINES) if l.startswith(u'# ' + name_prefix)]
    if not ks:
        return u''
    a = ks[0]
    b = next((k for k in range(a + 1, len(LINES)) if LINES[k].startswith(u'# ')), len(LINES))
    return u'\n'.join(LINES[a:b])


# ── 未收之典・其界須在（界亡即紅）
BOUND = [(u'《六祖壇經》開示無相心地戒', u'附錄一', u'照錄未覆核'),
         (u'《中阿含經》第 179 經', u'附錄五', u'本地語料未收'),
         (u'《梵網經菩薩戒》', u'第五章', u'本地語料未收')]
declared = []
for anchor, blk, word in BOUND:
    ok = anchor in u'\n'.join(LINES) and word in block_text(blk)
    declared.append((anchor, blk, word, ok))
    if not ok:
        print(u'✘ 標界之宣稱不在：錨『%s』須見『%s』於%s' % (anchor[:20], word, blk))

verbose = u'-v' in sys.argv
rows = []
tally = {}
for idx, l in enumerate(LINES):
    if END <= idx < ENDN:
        continue
    gates = [m.start() for m in GATE.finditer(l)]
    if not gates:
        continue
    for m in Q.finditer(l):
        if not any(g < m.start(1) for g in gates):
            continue
        q = m.group(1)
        v, _bad = _tk.classify(q)
        k = v if not v.startswith(u'other') else u'other'
        tally[k] = tally.get(k, 0) + 1
        rows.append((idx + 1, region_of(idx), q, v))

undb = [r for r in rows if r[3] == u'miss'
        and not any(ok and anchor in LINES[r[0] - 1]
                    for anchor, _blk, _word, ok in declared)]
print(u'———— 同線冠出處之逐字宣稱 %d 段（宣稱區 %d 段之跨行引文由 v39quote 校）：'
      u'命中 %d・他典 %d・不校 %d・未標界之非逐字 %d' % (
          len(rows), len(CD.src_blocks(LINES)), tally.get(u'hit', 0), tally.get(u'other', 0),
          tally.get(u'skip', 0), len(undb)))
for c, (anchor, blk, word, ok) in enumerate(declared, 1):
    print(u'   界%d・%s（%s：%s）' % (c, anchor[:18], blk, u'在' if ok else u'亡！'))
if verbose:
    for ln, reg, q, v in rows:
        print(u'  %s L%-6d %-22s %-6s %s' % (u'✗' if (ln, q, v) in undb else u'·',
                                             ln, reg, v, q[:38].replace(u'\n', u'')))
elif undb:
    for ln, reg, q, v in undb:
        print(u'  ✗ L%-6d %-22s %s' % (ln, reg, q[:44].replace(u'\n', u'')))
sys.exit(1 if (undb or not all(d[3] for d in declared)) else 0)
