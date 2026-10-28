# -*- coding: utf-8 -*-
"""第 65 輪・己：圍欄兩段之對齊與一處脫字（我自己鑄圖時的帳）。

 一・「│      」六空格令續行之文落在第 8 格，而節點之文起於第 5 格——差三格，視覺上像多縮一層。
 二・「└─」下之續行七空格，同病。
 三・我以 chr() 補『徹』時掉了『底』字，遂成「徹銷毀」——simp_sweep 只掃簡形，逮不到脫字；
    此即『形制之尺不為成語破例』之反面：自造之文須自讀一遍。
用法：python -X utf8 _work/hlfix65f.py [--go]
"""
import hashlib
import io
import os
import re
import shutil
import sys

GO = u"--go" in sys.argv
BOOK = u"佛陀的護欄 四分律比丘與比丘尼戒的行為心理學解析.txt"
BAK = BOOK + u".bak65f"
raw = io.open(BOOK, "rb").read()
sha0 = hashlib.sha256(raw).hexdigest()
L = raw.decode("utf-8").split(u"\r\n")
N0 = len(L)

IND = re.compile(u"^(│)( {3,6})(?=\\S)")
ONLY = re.compile(u"^( {6,8})(?=\\S)")
cnt = cnt2 = 0
for k in range(1753, 2212):
    m = IND.match(L[k])
    if m:
        L[k] = u"│   " + L[k][m.end():]
        cnt += 1
        continue
    m = ONLY.match(L[k])
    if m:
        L[k] = u"     " + L[k][m.end():]
        cnt2 += 1
print(u"對齊：│ 續行 %d 行｜└ 續行 %d 行" % (cnt, cnt2))
assert (cnt, cnt2) == (10, 2), u"圍欄內之縮排行數與預期不合（%d／%d）" % (cnt, cnt2)

FIX = [(u"│   徹銷毀，不許任何人復用", u"│   " + chr(0x5FB9) + chr(0x5E95) + u"銷毀，不許任何人復用")]
for old, new in FIX:
    hits = [k for k, t in enumerate(L) if t == old]
    assert len(hits) == 1, u"脫字之錨命中 %d" % len(hits)
    L[hits[0]] = new
    print(u"  補字｜L%d→%s" % (hits[0] + 1, new))

txt = u"\r\n".join(L)
assert txt.count(u"\r") == txt.count(u"\n") == len(L) - 1, u"CRLF 變形"
print(u"行數 %d→%d" % (N0, len(L)))
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
assert not os.path.exists(BAK), u"備份已存在：%s" % BAK
shutil.copy2(BOOK, BAK)
io.open(BOOK, "w", encoding="utf-8", newline=u"").write(txt)
chk = io.open(BOOK, "rb").read()
print(u"已寫檔｜sha %s→%s｜備份 %s" % (
    sha0[:12], hashlib.sha256(chk).hexdigest()[:12], os.path.basename(BAK)))
