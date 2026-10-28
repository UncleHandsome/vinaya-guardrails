# -*- coding: utf-8 -*-
"""第 65 輪・戊：最後一拍黑塊（案例十三之【第20條】欄：211＋179 字併為一段 323 字）。

治法同前：『同條後半』另起一拍（補空行、除硬斷之兩空格），一字不增刪。
用法：python -X utf8 _work/hlfix65e.py [--go]
"""
import hashlib
import io
import os
import shutil
import sys

GO = u"--go" in sys.argv
BOOK = u"佛陀的護欄 四分律比丘與比丘尼戒的行為心理學解析.txt"
BAK = BOOK + u".bak65e"
raw = io.open(BOOK, "rb").read()
sha0 = hashlib.sha256(raw).hexdigest()
L = raw.decode("utf-8").split(u"\r\n")
N0 = len(L)

LEAD = u"  * **第20條（生薑易食與擣新舊衣）：**"
TAIL = u"  同條後半，跋難陀與一外道以物易衣。"
i = [k for k, t in enumerate(L) if t.startswith(LEAD)]
assert len(i) == 1, u"第20條之錨命中 %d" % len(i)
i = i[0]
assert L[i + 1].startswith(TAIL), u"其下非『同條後半』：%s" % L[i + 1][:24]
L[i] = L[i].rstrip()
L[i + 1:i + 1] = [u""]
print(u"補空行｜L%d 之後另起一拍（%d→兩段）" % (i + 1, len(LEAD)))

txt = u"\r\n".join(L)
assert txt.count(u"\r") == txt.count(u"\n") == len(L) - 1, u"CRLF 變形"
assert sum(1 for l in L if l.startswith(u"#### 案例")) == 163, u"案例之數變形"
print(u"行數 %d→%d" % (N0, len(L)))
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
assert not os.path.exists(BAK), u"備份已存在：%s" % BAK
shutil.copy2(BOOK, BAK)
io.open(BOOK, "w", encoding="utf-8", newline=u"").write(txt)
chk = io.open(BOOK, "rb").read()
print(u"已寫檔｜sha %s→%s｜%d B｜備份 %s" % (
    sha0[:12], hashlib.sha256(chk).hexdigest()[:12], len(chk), os.path.basename(BAK)))
