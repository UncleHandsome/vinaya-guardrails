# -*- coding: utf-8 -*-
"""第 71 輪・宣稱之字樣歸一（承 71d 之新句）。
71d 以 `%d` 植入「的 54 條（條號錯落於第 70 至 178 條之間，其餘 55 條…）」，
而本書散文之數自以漢字為常（同句已有「一百零九條」），條號則用阿拉伯而不空一格（L4402「第70條至第178條」即成例）。
本刀只改字樣，不改其數。"""
import hashlib
import io
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "_work"))
import hulan_path as HP  # noqa: E402

GO = u"--go" in sys.argv
PAIR = [(u"的 54 條（條號錯落於第 70 至 178 條之間，其餘 55 條另入第十五章）",
         u"的五十四條（條號錯落於第70至178條之間，其餘五十五條另入第十五章）")]

raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
L = raw.split(u"\r\n")
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
n = 0
for a, b in PAIR:
    hit = [i for i, s in enumerate(L) if a in s]
    print(u"锚命中 %d 行：%s" % (len(hit), [i + 1 for i in hit]))
    for i in hit:
        print(u"  L%d|%s" % (i + 1, L[i][max(0, L[i].index(a) - 40):L[i].index(a) + len(a) + 30]))
        L[i] = L[i].replace(a, b)
        n += 1
assert n == 1, u"命中數非 1，先查再改（今 %d）" % n
out = u"\r\n".join(L)
if not GO:
    print(u"（乾跑：加 --go 始寫檔）｜改 %d 處" % n)
    sys.exit(0)
BK = HP.bakpath("71f")
io.open(BK, "wb").write(raw.encode("utf-8"))
for k in range(3):
    try:
        io.open(HP.SRC, "wb").write(out.encode("utf-8"))
        break
    except OSError as e:
        print(u"  寫檔重試 %d：%s" % (k + 1, e))
        time.sleep(2)
chk = io.open(HP.SRC, "rb").read().decode("utf-8")
print(u"已寫檔｜行數 %d｜sha %s→%s｜回讀%s｜備份 %s"
      % (len(L), sha0, hashlib.sha256(chk.encode("utf-8")).hexdigest()[:12],
         u"全等" if chk == out else u"不等!", os.path.relpath(BK, ROOT)))
