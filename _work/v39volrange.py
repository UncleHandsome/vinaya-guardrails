# -*- coding: utf-8 -*-
"""第 264 輪・範圍引卷尺：凡以『卷X至Y』形制引卷者（非單一『卷N』），驗其所引之文確在該卷段。

緣起：`v39volchk.py` 只識單一『卷N』（語料六檔＝六個卷區間，故可判『所引之卷在其文所在之卷段』）；
      而書中另有 **23 處作『卷X至Y』**（附錄三辭典之「……」（卷一至十）式・卷首七佛略戒之雙卷段・
      第六章與附錄六之『《四分律》卷五十五至五十七（第四分調部…）：』式・附錄四表列之卷段欄），
      此形制向在核卷尺之外——**新形制必回頭校舊尺**（261 輪『兼引』之教同科）。
口徑：
  （一）形制二式：① 引號之後近處有（卷A至B）或，卷A至B；② 行首作『《四分律》卷A至B（…）：』者，
        其下【律典原典】塊內之 「」 段悉歸此宣稱。
  （二）卷段之落地：A..B 與本地六檔之卷區間**相交**者即為該宣稱之許用檔；引文（按刪節號切段・norm 折形）
        須見於其中**一檔**。
  （三）判語三態：合（在其許用檔見）／不合（全書他檔見而此卷段不見）／未證（語料無此文，如他部之典）。
退碼：『不合』≥1 即退 1（未證者不充自稱之據，如實列數而不挡）。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/v39volrange.py [-v]
"""
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import _tk                                                     # noqa: E402

SRC_PATH = next((a for a in sys.argv[1:] if not a.startswith(u"-")), None)          # 274 輪・試跑通道：量假冊而不動正本
if SRC_PATH:
    LINES = io.open(SRC_PATH, encoding=u"utf-8-sig").read().split(u"\n")
else:
    LINES = _tk.MAIN_LINES
Q = _tk.Q_RE
RNG = re.compile(u'卷\\s*([一二三四五六七八九十百0-9]{1,6})\\s*至\\s*([一二三四五六七八九十百0-9]{1,6})')
HEAD = re.compile(u'^>\\s*(?:《[^》]{1,16}》\\s*)?(?:又|兼)?卷')   # 亦收續引之形（『> 又卷二十二至三十（…）：』）
VERB = re.compile(u'^#### 【律典原典】\\s*$')
ANYHEAD = re.compile(u'^(#{1,6} |---\\s*$)')
END = next((k for k, l in enumerate(LINES) if l.startswith(u'# 終卷')), len(LINES))
ENDN = next((k for k in range(END + 1, len(LINES)) if LINES[k].startswith(u'# ')), len(LINES))


def num(s):
    s = s.strip()
    if s.isdigit():
        return int(s)
    v = _tk.cn_num(s)
    return v


# ── 語料六檔：檔名即卷區間（01-10 … 50-60）。 loading 一依 `v39align.CORPUS`（單一法源，
#    不另起爐灶——原文/*.txt 之編碼向有前車之鑒）
RANGE = {u'01-10': (1, 10), u'11-21': (11, 21), u'22-30': (22, 30),
         u'31-37': (31, 37), u'38-49': (38, 49), u'50-60': (50, 60)}
import v39align                                                # noqa: E402
FILES = []
for fn, raw, nt, nm in v39align.CORPUS:
    key = next((k for k in RANGE if k in fn), None)
    if key:
        lo, hi = RANGE[key]
        FILES.append((fn, lo, hi, nt))
assert len(FILES) == 6, u'語料六檔未齊（今 %d）' % len(FILES)


def parts_of(q):
    out = []
    for seg in re.split(_tk.ELL, q):
        nq = _tk.norm(seg)
        if len(nq) >= 4:
            out.append(nq)
    return out


def find_files(ps):
    """回傳『含全部片段』之檔名集合（空集合＝全書未見）。"""
    if not ps:
        return set()
    keep = set(name for name, _a, _b, _t in FILES)
    for name, lo, hi, t in FILES:
        if not all(p in t for p in ps):
            keep.discard(name)
    return keep


def allowed_any(rms):
    """一處宣稱可兼引數個卷段（『卷五十五至五十七…兼卷二十二至三十』），許用檔取其並集。"""
    ok = set()
    for rm in rms:
        a, b = num(rm.group(1)), num(rm.group(2))
        if a is None or b is None:
            continue
        lo, hi = min(a, b), max(a, b)
        for n, a2, b2, _t in FILES:
            if a2 <= hi and lo <= b2:
                ok.add(n)
    return ok


def judge(ps, ok):
    """逐片段判：每一段都須見於許用檔之一。皆見→合；有段見於他檔→不合；全書無此段→未證。"""
    if not ps:
        return u'不校', u'片段過短'
    txt = dict((n, t) for n, _a, _b, t in FILES)
    seen, outside = [], []
    for p in ps:
        inok = [n for n in sorted(ok) if p in txt[n]]
        if inok:
            seen += inok
            continue
        got = [n for n, _a, _b, t in FILES if p in t]
        if got:
            outside += got
        else:
            return u'未證', u'語料未見此段'
    if outside:
        return u'不合', u'有段見 %s 而不在許用 %s' % (
            u'・'.join(sorted(set(outside))), u'・'.join(sorted(ok)))
    return u'合', u'・'.join(sorted(set(seen)))


rows = []
i = 0
while i < len(LINES):
    l = LINES[i]
    if END <= i < ENDN or not l.strip():
        i += 1
        continue
    ms = list(RNG.finditer(l))
    if not ms:
        i += 1
        continue
    # 形制①：引號之後近處有（卷A至B［、卷C至D］）——取至「下一個引號之前」為止，
    #          免把相鄰另一段之卷段混入本段之許用檔（一名一職，尺之靶須與病同寬亦不可過寬）
    qs = [m2.start() for m2 in Q.finditer(l)]
    for m in Q.finditer(l):
        nxt = [x for x in qs if x > m.start(1)]
        cap = min(nxt[0] if nxt else len(l), m.end() + 36)
        tail = l[m.end():cap]
        rms = list(RNG.finditer(tail))
        if not rms:
            continue
        ok = allowed_any(rms)
        v, d = judge(parts_of(m.group(1)), ok)
        rows.append((i + 1, v, m.group(1), u'＋'.join(x.group(0) for x in rms), d))
    # 形制②：行首《四分律》卷A至B（…）［兼卷C至D］：，其下【律典原典】塊之引文歸此宣稱
    if HEAD.match(l):
        rms = list(RNG.finditer(l))
        ok = allowed_any(rms)
        if ok:
            j = i + 1
            if j < len(LINES) and VERB.match(LINES[j]):
                j += 1
            while j < len(LINES) and not ANYHEAD.match(LINES[j]):
                if LINES[j].strip() and not HEAD.match(LINES[j]):
                    for m2 in Q.finditer(LINES[j]):
                        v, d = judge(parts_of(m2.group(1)), ok)
                        rows.append((j + 1, v, m2.group(1),
                                     u'＋'.join(x.group(0) for x in rms), d))
                j += 1
            i = j
            continue
    i += 1

tally = {}
for _ln, v, _q, _r, _d in rows:
    tally[v] = tally.get(v, 0) + 1
print(u'———— 『卷X至Y』式引卷之宣稱 %d 段：合 %d・不合 %d・未證 %d・不校 %d' % (
    len(rows), tally.get(u'合', 0), tally.get(u'不合', 0), tally.get(u'未證', 0), tally.get(u'不校', 0)))
for ln, v, q, r, d in rows:
    if v in (u'不合', u'未證') or u'-v' in sys.argv:
        mark = {u'合': u'·', u'不合': u'✗', u'未證': u'△', u'不校': u'—'}[v]
        print(u'  %s L%-6d %-14s｜%s｜%s' % (mark, ln, r, q[:30].replace(u'\n', u''), d[:56]))
sys.exit(1 if tally.get(u'不合', 0) else 0)
