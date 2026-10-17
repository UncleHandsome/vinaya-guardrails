# -*- coding: utf-8 -*-
"""後三十卷之「未用場」名冊：合硬斷行 → 以「爾時／時有／我曾聞／後有」切場 →
   逐場取其內足長之整句（剔去通用套語）查其是否已入書。一句入書即算此場已用——
   比「以段首十字求字面」穩：書中引文多為段中一句，非自段首引起。
   正規化唯取 _tk.norm（與逐字閘同一法源）。未用者報其揵度・字數・首句，供選場。
用法：python -X utf8 _work/kh_unused.py [篇关键字] [--top N] [--min 字數] [--all]
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import glob
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = HP.SRC
bn = _tk.norm(io.open(BOOK, encoding="utf-8", newline="").read())

TAG = ["31-37", "38-49", "50-60"]
VAL = {u"--top", u"--min"}
KEY = [a for i, a in enumerate(sys.argv[1:])
       if not a.startswith("--") and not (i and sys.argv[1:][i - 1] in VAL)]
TOP = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 30
MIN = int(sys.argv[sys.argv.index("--min") + 1]) if "--min" in sys.argv else 200
HEAD = re.compile(u"(?:^|\\n)\\s*[(（]?([^\\n，。：；、()（）「」『』\\s]{2,10}[揵犍]度[^\\n，。：；()（）]{0,6})", re.M)
MARK = re.compile(u"(?=(?:爾時|時有|我曾聞|後有|時諸|爾時佛))")

# 套語不自人手 blacklist：凡該句在後三十卷出現 ≥3 次者即為公式語（「非威儀、非沙門法」之類），
# 不充當「已入書」之憑——否則一句套語誤認，全場皆誤。稀有度由語料自算。
FREQ = {}
DOCS = []
for tag in TAG:
    f = [p for p in glob.glob(os.path.join(ROOT, u"原文", u"*.txt")) if tag in os.path.basename(p)][0]
    raw = io.open(f, encoding="utf-8", errors="ignore").read().replace("\r\n", "\n")
    # 標題須於『未合行』之原文上取（合行後行首錨失效），其序再於合行文中逐個前向定址
    names = [re.sub(u"[揵犍]度.*$", u"", m.group(1)).strip(u"(（ ") for m in HEAD.finditer(raw)]
    t = re.sub(u"\\s*\\n\\s*", u"", raw)                     # 合硬斷行（原檔每三十餘字一斷）
    heads, cur = [], 0
    for nmh in names:
        k = t.find(nmh + u"揵度", cur)
        k2 = t.find(nmh + u"犍度", cur)
        k = k2 if k < 0 else (k2 if 0 <= k2 < k else k)
        if k >= 0:
            heads.append((k, nmh))
            cur = k + 1
    DOCS.append((tag, t, heads or [(0, u"（無標題之卷首段）")]))
    for seg in MARK.split(t):
        for s in re.split(u"[。！]", seg):
            if len(s) >= 22:
                FREQ[s] = FREQ.get(s, 0) + 1

rows, used = [], 0
for tag, t, heads in DOCS:
    for seg in MARK.split(t):
        if len(seg) < MIN:
            continue
        pos = t.find(seg[:40])
        nm = next((h for s, h in reversed(heads) if s <= pos), heads[0][1])
        if KEY and not any(k in nm for k in KEY):
            continue
        sents = [x for x in re.split(u"[。！]", seg) if len(x) >= 22 and FREQ[x] <= 2]
        if not sents:
            continue                                   # 全場唯套語，無從判已用與否
        if any(_tk.norm(s) in bn for s in sents):
            used += 1
            continue
        rows.append((nm, len(seg), seg, len(sents)))
print(u"後三十卷｜敘事場（≥%d 字・具特有句）%d 處已入書｜未入書 %d 處" % (MIN, used, len(rows)))
by = {}
for nm, n, txt, ns in rows:
    by.setdefault(nm, []).append((n, txt, ns))
for nm in sorted(by, key=lambda k: -sum(x[0] for x in by[k])):
    print(u"── %-14s｜未用 %2d 場｜合 %6s 字" % (nm, len(by[nm]), format(sum(x[0] for x in by[nm]), ",")))
    for n, txt, ns in sorted(by[nm], reverse=True)[:3 if not KEY else TOP]:
        print(u"     %6d字｜可引句 %d｜%s" % (n, ns, txt[:64].replace(u"\n", u"")))
