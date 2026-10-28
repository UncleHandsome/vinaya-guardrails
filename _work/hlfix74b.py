# -*- coding: utf-8 -*-
"""第 74 輪・自犯之收：本輪三處新文用了『・』（日式中黑，U+30FB）作頓號，而本书之制『圍欄外之・須為 0』
（`punctchk` 硬檢，第 74 輪當場逮住——尺又一次接住了編輯層之傷）。本刀只換標點，不動一字。"""
import hashlib
import io
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import hulan_path as HP  # noqa: E402

GO = u"--go" in sys.argv
NAK, IDEO = u"\u30fb", u"\u3001"          # ・ ➔ 、


def out_of_fence(lines, upto):
    """回 [(行號, 是否在圍欄外)]：以 ``` 之奇偶判（附錄以前之正文）。"""
    inside, out = False, []
    for i in range(upto):
        if lines[i].startswith(u"```"):
            inside = not inside
            continue
        out.append((i, not inside))
    return out


raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
L = raw.split(u"\r\n")
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
apx0 = next(i for i, s in enumerate(L) if s.startswith(u"# 附錄"))
n = 0
for i, free in out_of_fence(L, apx0):
    if free and NAK in L[i]:
        c = L[i].count(NAK)
        L[i] = L[i].replace(NAK, IDEO)
        n += c
        j = L[i].find(IDEO)
        print(u"  L%-5d 換 %d 枚 ➔ …%s…" % (i + 1, c, L[i][max(0, j - 22):j + 16]))
rest = sum(1 for i, free in out_of_fence(L, apx0) if free and NAK in L[i])
print(u"共換 %d 枚｜改後圍欄外含『・』之行 %d（須 0）" % (n, rest))
out = u"\r\n".join(L)
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
BK = HP.bakpath("74b")
io.open(BK, "wb").write(raw.encode("utf-8"))
for k in range(3):
    try:
        io.open(HP.SRC, "wb").write(out.encode("utf-8"))
        break
    except OSError as e:
        print(u"  寫檔重試 %d：%s" % (k + 1, e))
        time.sleep(2)
chk = io.open(HP.SRC, "rb").read().decode("utf-8")
print(u"已寫檔｜行數 %d｜sha %s→%s｜回讀%s"
      % (len(L), sha0, hashlib.sha256(chk.encode("utf-8")).hexdigest()[:12],
         u"全等" if chk == out else u"不等!"))
