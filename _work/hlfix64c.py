# -*- coding: utf-8 -*-
"""第 64 輪・丙：二不定法之附論入目錄。

新稿已將二不定法自「案例六」降為第三節末之【過渡專題／附論】——案例之數不動（六），
然書中實有此節，目錄不可無（第 57 輪『第N樞紐』入目同此口徑）。
錨：目錄之第六章案例六行＋其後須紧跟『四、 殘之治』；正文之附論標題須在冊。
用法：python -X utf8 _work/hlfix64c.py [--go]
"""
import hashlib
import io
import os
import re
import shutil
import sys

GO = u"--go" in sys.argv
BOOK = u"佛陀的護欄 四分律比丘與比丘尼戒的行為心理學解析.txt"
BAK = BOOK + u".bak64c"
raw = io.open(BOOK, "rb").read()
sha0 = hashlib.sha256(raw).hexdigest()
L = raw.decode("utf-8").split(u"\r\n")
N0 = len(L)

BODY = [l for l in L if l.startswith(u"#### 【過渡專題／附論】")]
assert len(BODY) == 1, u"正文附論標題 %d 枚 ≠ 1" % len(BODY)
title = BODY[0][len(u"#### "):].strip()
ROW = u"    * " + title
t0 = next(k for k, l in enumerate(L) if u"【全書詳細目錄】" in l)
t1 = next(k for k in range(t0 + 1, len(L)) if re.match(u"^# ", L[k]))
i = [k for k, l in enumerate(L) if l.startswith(u"    * 案例六：第十二、第十三僧殘")]
assert len(i) == 1, u"目錄案例六行 %d 枚" % len(i)
i = i[0]
assert t0 < i < t1, u"案例六行不在目錄區內"
assert L[i + 1].startswith(u"  * 四、 殘之治"), u"案例六行之後非『四、 殘之治』：%s" % L[i + 1][:24]
assert not any(title in l for l in L[t0:t1]), u"目錄已有附論之目，勿兩抄"
L[i + 1:i + 1] = [ROW]
print(u"目錄入目 L%d｜%s" % (i + 2, title[:56]))
j = [k for k, l in enumerate(L[t0:t1], t0) if l.startswith(u"* **第六章")]
z = next(k for k in range(j[0] + 1, t1) if L[k].startswith(u"* **第七章"))
print(u"第六章目錄之節項 %d｜案例項 %d｜附論 1" % (
    sum(1 for l in L[j[0]:z] if re.match(u"^  \\* [一二三四五]、", l)),
    sum(1 for l in L[j[0]:z] if l.startswith(u"    * 案例"))))

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
CL = chk.decode("utf-8").split(u"\r\n")
assert CL[i + 1] == ROW, u"覆讀之目錄行與所插者不合"
print(u"已寫檔｜sha %s→%s｜備份 %s" % (
    sha0[:12], hashlib.sha256(chk).hexdigest()[:12], os.path.basename(BAK)))
