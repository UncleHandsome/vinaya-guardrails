# -*- coding: utf-8 -*-
"""第 74 輪・74c 之過：折重引號時把附錄 L6074 的『』嵌套收束（『…『…。』』）亦折了一枚，
   而『』之雙收乃律文引中之引，合法。本刀只還原此行（自 74c 之備份取原句，全行等式覆讀）。
   教：同一字符之『重』有正誤兩解——「「必誤（此書以「」為外層），』』可正（嵌套之收）。尺只當管前者。"""
import hashlib
import io
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import hulan_path as HP  # noqa: E402

GO = u"--go" in sys.argv
BK = HP.bakpath("74c")
old = io.open(BK, encoding="utf-8", newline="").read().split(u"\r\n")
raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
L = raw.split(u"\r\n")
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
KEY = u"16. \u300c\u82e5\u6bd4\u4e18\u5c3c\u8da3\u4ee5\u4e00\u5c0f\u4e8b"
i = [k for k, s in enumerate(L) if s.startswith(KEY)]
assert len(i) == 1, u"锚 %d 次" % len(i)
i = i[0]
j = [k for k, s in enumerate(old) if s.startswith(KEY)]
assert len(j) == 1 and i == j[0], u"備份同鍵之行不同位（%s vs %s）" % (j, i)
print(u"L%-5d 今:%s" % (i + 1, L[i][-34:]))
print(u"      原:%s" % old[i][-34:])
assert L[i] != old[i], u"已等於備份，無需還原"
L[i] = old[i]
t = u"\r\n".join(L)
print(u"還原後：『%d 』%d 差%d｜「%d 」%d 差%d"
      % (t.count(u"\u300e"), t.count(u"\u300f"),
         t.count(u"\u300e") - t.count(u"\u300f"),
         t.count(u"\u300c"), t.count(u"\u300d"),
         t.count(u"\u300c") - t.count(u"\u300d")))
assert t.count(u"\u300c\u300c") == 0 and t.count(u"\u300d\u300d") == 0, u"重「」仍在"
out = t
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
NB = HP.bakpath("74d")
io.open(NB, "wb").write(raw.encode("utf-8"))
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
