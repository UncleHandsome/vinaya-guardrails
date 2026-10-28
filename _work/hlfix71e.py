# -*- coding: utf-8 -*-
"""第 71 輪・hlchk 戊軸之歸真（1 處）。
病：第十五章案例八 L4918 以款①式樣（粗體＋引號）自稱逐字，作「此弊惡下賤之工師種！」，
    而本律（T22 卷五十八・尼犍度・罵比丘戒之因緣）實作「時諸比丘尼見迦毘羅即罵詈言**此弊惡下賤工師種**壞我等塔」——
    多一「之」字即非連寫子串，故戊軸紅。
治：削一「之」字（最小跨度，全句其餘不動）；同章 L4926 本書自引作「下賤工師種」本已合律，歸真後兩處自一。
"""
import hashlib
import io
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "_work"))
import hulan_path as HP  # noqa: E402
import _tk  # noqa: E402

GO = u"--go" in sys.argv
OLD = u"此弊惡下賤之工師種"
NEW = u"此弊惡下賤工師種"

raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
L = raw.split(u"\r\n")
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]

hit = [i for i, s in enumerate(L) if OLD in s]
print(u"锚『%s』命中 %d 行：%s" % (OLD, len(hit), [i + 1 for i in hit]))
assert len(hit) == 1, u"命中非唯一次，先查再改"
i = hit[0]
n = L[i].count(OLD)
print(u"L%d|%s" % (i + 1, L[i][:260]))
print(u"替換 %d 處｜本律連寫證：%s" % (n, _tk.norm(NEW) in _tk.VINAYA))
assert _tk.norm(NEW) in _tk.VINAYA, u"歸真之形仍不在語料，不可寫檔"

L[i] = L[i].replace(OLD, NEW)
out = u"\r\n".join(L)
print(u"改後行：%s" % L[i][max(0, L[i].index(NEW) - 60):L[i].index(NEW) + 60])
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)

BK = HP.bakpath("71e")
io.open(BK, "wb").write(raw.encode("utf-8"))
for k in range(3):
    try:
        io.open(HP.SRC, "wb").write(out.encode("utf-8"))
        break
    except OSError as e:
        print(u"  寫檔重試 %d：%s" % (k + 1, e))
        time.sleep(2)
chk = io.open(HP.SRC, "rb").read().decode("utf-8")
print(u"已寫檔｜行數 %d → %d｜sha %s→%s｜回讀%s｜備份 %s"
      % (len(L), chk.count(u"\r\n") + 1, sha0,
         hashlib.sha256(chk.encode("utf-8")).hexdigest()[:12],
         u"全等" if chk == out else u"不等!", os.path.relpath(BK, ROOT)))
