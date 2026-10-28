# -*- coding: utf-8 -*-
"""第 74 輪・自犯之收：74a 降式樣時只該剝 `**`，卻在外層又包了一次「」，
   遂成「「…」」之重引號（18 处）；另搜得一处同型之舊傷（L1921）。
   本刀只折重引號（「「➔「、」」➔」、『『➔『、』』➔』），一字不換。"""
import hashlib
import io
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import hulan_path as HP  # noqa: E402

GO = u"--go" in sys.argv
PAIRS = [(u"\u300c\u300c", u"\u300c"), (u"\u300d\u300d", u"\u300d")]
# 『『／』』不折：律文引中之引之雙收（『…『…。』』）乃合法——74c 曾誤折附錄一行，由 74d 自備份還原。
#   今 punctchk 已立『重引號須 0』之目（只管「「／」」），本刀遂成一次性之历史记录，重跑亦無事。
if any(p[0] in s for s in io.open(HP.SRC, encoding="utf-8", newline="").read().split(u"\r\n")
       for p in PAIRS):
    print(u"（尚有重引號可折）")
else:
    print(u"（今檔已無「「／」」可折——本刀為 74 輪一次性之历史记录，不重覆動檔）")
raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
L = raw.split(u"\r\n")
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
tot = 0
for i, s in enumerate(L):
    for a, b in PAIRS:
        while a in L[i]:
            c = L[i].count(a)
            L[i] = L[i].replace(a, b)
            tot += c
            print(u"  L%-5d 折 %s×%d" % (i + 1, a, c))
            break
print(u"共折 %d 處" % tot)
left = sum(L[i].count(a) for a, _ in PAIRS for i in range(len(L)))
print(u"自證：改後重引號餘 %d（須 0）" % left)
assert left == 0, u"仍有重引號，未寫"
out = u"\r\n".join(L)
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
BK = HP.bakpath("74c")
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
