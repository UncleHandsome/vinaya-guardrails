# -*- coding: utf-8 -*-
"""第 72 輪・自犯之一字：72a 之按語末作「先后」，『后』乃『後』（U+5F8C）之簡形，全檔他處無此形。
本刀只換三字之最小跨度，並自證改後『后』形於全檔 0 見。"""
import hashlib
import io
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import hulan_path as HP  # noqa: E402

GO = u"--go" in sys.argv
OLD = u"\u4e4b\u5148\u540e\u3002"                  # 之<先>后。
NEW = u"\u4e4b\u5148\u5f8c\u3002"                  # 之<先>後。
raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
L = raw.split(u"\r\n")
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
hit = [i for i, s in enumerate(L) if OLD in s]
print(u"锚命中 %d 行：%s｜全檔『后』%d 行" % (len(hit), [i + 1 for i in hit],
                                            sum(1 for s in L if u"\u540e" in s)))
assert len(hit) == 1, u"命中非唯一次"
i = hit[0]
L[i] = L[i].replace(OLD, NEW)
print(u"改後：%s" % L[i][-40:])
print(u"自證：改後全檔『后』%d 見（須 0）" % sum(1 for s in L if u"\u540e" in s))
out = u"\r\n".join(L)
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
BK = HP.bakpath("72b")
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
