# -*- coding: utf-8 -*-
"""草稿雙閘（與全書通例對齊）：
① 粗體包引號者＝自稱逐字（**「…」** 或 「**…**」），須為語料 `_tk.VINAYA` 之連寫子串（以 …… 分段）；
   未加粗之「…」＝白話轉寫，只計數不較真。
② 雜質掃描：簡形、連續拉丁詞（白名單外）、韓日字。
用法：python -X utf8 _work/gate_draft.py <草稿檔>
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _tk  # noqa: E402
from _simpdict import MAP as _SIMP  # noqa: E402
from starbal import para_odd  # noqa: E402（粗體成對之定義與全書尺同源）

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
DRAFT = sys.argv[1]
t = io.open(DRAFT, encoding="utf-8", newline="").read().replace("\r\n", "\n")
V = _tk.VINAYA if isinstance(_tk.VINAYA, str) else "".join(_tk.VINAYA)

BOLD = [re.compile(u"\\*\\*「(.+?)」\\*\\*", re.S), re.compile(u"「\\*\\*(.+?)\\*\\*」", re.S)]
OK_LAT = {u"pfc", u"bmap", u"map"}
SIM = frozenset(_SIMP)          # 簡形名單單一法源：與全書尺 simp_sweep 同一份，勿兩處各抄
FOREIGN = re.compile(u"[\u3130-\u318f\u3040-\u30ff]")
LAT = re.compile(u"[A-Za-z][A-Za-z'.-]{2,}")


def nk(s):
    return _tk.norm(re.sub(u"\\*\\*", u"", s))


# 逐行口徑：粗體與引號須同在一行內配對，免跨句誤抓
spans = []
off = 0
for line in t.split("\n"):
    for pat in [re.compile(u"\\*\\*「([^」]+)」(\\*\\*)?"), re.compile(u"「\\*\\*([^」]+)\\*\\*」")]:
        for m in pat.finditer(line):
            spans.append((off + m.start(), off + m.end()))
    off += len(line) + 1
spans = sorted(set(spans))
vh = vm = 0
for a, b in spans:
    for raw in re.split(u"…+", t[a:b]):
        piece = nk(raw)
        if len(piece) < 4:
            continue
        vh += 1
        if piece in V:
            continue
        vm += 1
        s = ""
        for k in range(1, len(piece) + 1):
            if piece[:k] in V:
                s = piece[:k]
        print("L%d 無據｜%s" % (t[:a].count("\n") + 1, piece[:44]))
        print("      中到 %d 字｜…%s" % (len(s), s[-26:]))
        print("      斷點後｜%s" % piece[len(s):len(s) + 30])
vv = len(re.findall(u"「[^」]*」", t)) - len(re.findall(u"「[^」]*\\*\\*[^」]*」", t))
print("== 閘一｜逐字段 %d（無據 %d）｜白話引號 %d 段（不閘）" % (vh, vm, vv))

# 閘三：戒文行「> **【…】：…」須為語料連寫（與 hlchk『戒文省寫』同口徑）
rt = rm = 0
for i, ln in enumerate(t.split("\n"), 1):
    if not ln.startswith(u"> **【"):
        continue
    for raw in re.split(u"…+", re.sub(u"^> \\*\\*【[^】]*】：\\*\\*\\s*", u"", ln)):
        piece = nk(raw)
        if len(piece) < 4:
            continue
        rt += 1
        if piece in V:
            continue
        rm += 1
        s = ""
        for k in range(1, len(piece) + 1):
            if piece[:k] in V:
                s = piece[:k]
        print("L%d 戒文無據｜%s" % (i, piece[:44]))
        print("      中到 %d 字｜…%s" % (len(s), s[-26:]))
        print("      斷點後｜%s" % piece[len(s):len(s) + 30])
print("== 閘三｜戒文行 %d 段（無據 %d）" % (rt, rm))

nb = 0
# 口徑須與全書尺 simp_sweep 全等：語料自有之形（猪・并・宁・谷…）只在引號外追，
# 語料無此形者（历・师・断…）引號內外一律追；CBETA 組字碼括號同列保護區。
import glob  # noqa: E402
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORP = set()
for _f in glob.glob(os.path.join(ROOT, "原文", "*.txt")):
    CORP |= set(io.open(_f, encoding="utf-8", errors="ignore").read())
RISKY = {c for c in SIM if c in CORP}
qsp = [(m.start(), m.end()) for m in re.finditer(u"「[^」]*」|『[^』]*』|\\[[^\\]\\n]{1,14}\\]", t)]
inq = lambda k: any(a <= k < b for a, b in qsp)
pos = 0
for i, ln in enumerate(t.split("\n"), 1):
    pos += len(ln) + 1
    if ln.startswith("#CH "):
        continue
    hits = sorted(set(u"簡『%s』" % c for j, c in enumerate(ln)
                      if c in SIM and not (c in RISKY and inq(pos - len(ln) - 1 + j))))
    hits += [u"拉丁『%s』" % m.group(0)[:20] for m in LAT.finditer(ln)
             if m.group(0).strip(" .-").lower() not in OK_LAT]
    if FOREIGN.search(ln):
        hits.append(u"外文")
    if hits:
        nb += 1
        print("L%-4d %s｜%s" % (i, "、".join(sorted(hits)), ln.strip()[:54]))
print("== 閘二｜雜質行 %d（0 即純净）" % nb)

po = para_odd([x for x in t.split("\n") if not x.startswith("#CH ")])
print("== 閘四｜粗體不配對之段 %d（0 即平衡；落單之 * 會字面洩入印面）" % len(po))
for a, h in po[:8]:
    print("      段起 L%-5d｜%s" % (a, h))
