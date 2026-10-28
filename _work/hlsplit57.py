# -*- coding: utf-8 -*-
"""第 57 輪・庚：印面單段過長者分段（>300 字之段，名單與切法見 _work/hlsplit57_data.py）。
自證（寫檔前）：錨於本行唯一・每片 ≥FLOOR 字・每片星號成偶（不計行首之清單符）・
              諸片漢字總數＝原行（不丟一字）・全書漢字總數不變・CRLF 等式。
退回器：_work/hlunjoin57.py（全退後以大哈希覆核＝切分前之 SHA，證兩向無損）。
用法：python -X utf8 _work/hlsplit57.py [--go]
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.abspath(__file__))); _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import hlsplit57_data as D  # noqa: E402
import hashlib  # noqa: E402

BOOK = HP.SRC
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert raw.count(u"\r") == raw.count(u"\n"), u"入口 CRLF 已傷"
L = raw.split(u"\r\n")
N0 = len(L)
PLAN, PROB, used = [], [], set()
for n, anchors in D.SPL:
    line = L[n - 1]
    try:
        parts = D.cut(line, anchors)
    except (AssertionError, StopIteration) as e:
        PROB.append(u"L%d 切點不如期：%s" % (n, e))
        continue
    if D.CN(u"".join(parts)) != D.CN(line):
        PROB.append(u"L%d：分段丟字（%d→%d）" % (n, D.CN(line), D.CN(u"".join(parts))))
        continue
    sliv = [u"%d 字「%s…」" % (D.CN(x), x.strip()[:14]) for x in parts if D.CN(x) < D.FLOOR]
    odd = [x.strip()[:14] for x in parts
           if re.sub(u"^\\s*(?:\\*|\\d+\\.)\\s+", u"", x).count(u"*") % 2]
    if sliv or odd:
        PROB.append(u"L%d：片段過短 %s｜星號成奇 %s" % (n, u"、".join(sliv), u"、".join(odd)))
        continue
    PLAN.append((n, parts, D.indent_of(line)))
    print(u"L%-5d → %d 段（%s）" % (n, len(parts), u"・".join(u"%d 字" % D.CN(x) for x in parts)))
    for x in parts[1:]:
        print(u"        接：%s…" % x.strip()[:34])
for p in PROB:
    print(u"  ✗ %s" % p)
assert not PROB, u"有 %d 處切點不如期，未敢寫檔" % len(PROB)
new = list(L)
for n, parts, ind in sorted(PLAN, key=lambda x: -x[0]):      # 由後向前插，前行號方不失準
    new[n - 1:n] = [parts[0]] + [y for p in parts[1:] for y in (u"", ind + p)]
print(u"分段 %d 處｜新增段落 %d｜行數 %d→%d" % (len(PLAN), sum(len(p) - 1 for _n, p, _i in PLAN), N0, len(new)))
txt = u"\r\n".join(new)
assert txt.count(u"\r") == txt.count(u"\n"), u"出口 CRLF 變形"
assert D.CN(txt) == D.CN(raw), u"全書漢字總數變形"
if u"--go" in sys.argv:
    io.open(BOOK, "w", encoding="utf-8", newline=u"").write(txt)
    print(u"已寫檔｜新 SHA %s" % hashlib.sha256(txt.encode("utf-8")).hexdigest()[:12])
else:
    print(u"（乾跑：加 --go 始寫）")
