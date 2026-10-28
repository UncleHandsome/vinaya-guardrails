# -*- coding: utf-8 -*-
"""第 68 輪・乙：全書『第十一章案例N』之指針歸位（舊27案➔新28案）＋案例總數自報改約。
法：單次正則＋映射函數（絕不逐號輪替，免二次命中）；改前印本數、改後逐處列印；
    附錄不碰（其『書中』欄由產生器重算）；CRLF 等式・備份・SHA・回讀。
用法：python -X utf8 _work/hlfix68b.py [--go]
"""
import os as _hp_os, sys as _hp_sys
_hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__))))
import hulan_path as HP
import hashlib
import io
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
BAK = BOOK + ".bak68b"
GO = "--go" in sys.argv

U = u"零一二三四五六七八九十百"


def i2cn(n):
    if n < 10:
        return U[n]
    if n == 10:
        return u"十"
    if n < 20:
        return u"十" + U[n - 10]
    return U[n // 10] + u"十" + (U[n % 10] if n % 10 else u"")


def cn2int(s):
    if s == u"十":
        return 10
    if s.startswith(u"十"):
        return 10 + U.index(s[1])
    if len(s) == 3 and s[1] == u"十":
        return U.index(s[0]) * 10 + U.index(s[2])
    if s.endswith(u"十"):
        return U.index(s[0]) * 10
    return U.index(s)


MAP = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10,
       11: 12, 12: 13, 13: 14, 14: 15, 15: 16, 16: 17, 17: 18, 18: 19, 19: 20,
       20: 21, 21: 23, 22: 24, 23: 25, 24: 26, 25: 27, 26: 22, 27: 28}
PAT = re.compile(u"第十一章案例([〇零一二三四五六七八九十百]{1,3})")

raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert raw.count(u"\r") == raw.count(u"\n") == raw.count(u"\r\n"), u"入口 CRLF 已傷"
L = raw.split(u"\r\n")
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()
apx = next(i for i, l in enumerate(L) if l.startswith(u"# 附錄"))
assert u"#### 案例" not in u"\r\n".join(L[apx:]), u"附錄內有案例標題，指針區之劃分須重估"

nfix = 0
for i in range(apx):
    l = L[i]
    if u"第十一章案例" not in l:
        continue

    def rep(m):
        global nfix
        old = cn2int(m.group(1))
        assert old in MAP, u"稿L%d 未知之舊案例號 %d" % (i + 1, old)
        nfix += 1
        return u"第十一章案例" + i2cn(MAP[old])

    new = PAT.sub(rep, l)
    if new != l:
        print(u"  L%-5d %s" % (i + 1, l.strip()[:58]))
        print(u"     ➤ %s" % new.strip()[:58])
        L[i] = new

nrep = 0
for i, l in enumerate(L):
    if u"把全書一百三十三則案例" in l:
        L[i] = l.replace(u"一百三十三則", u"一百三十四則")
        nrep += 1
assert nrep == 1, u"自報句命中 %d（欲 1）" % nrep
print(u"  自報句：一百三十三則➔一百三十四則 ✓×1")

# 十線地圖之篇聚欄：『中途遇賊』一案出於比丘尼犍度（旧標『受戒犍度』乃錯標其目）
npk = 0
for i, l in enumerate(L):
    if u"第十一章案例十四 | 受戒犍度 | 中途遇賊" in l:
        L[i] = l.replace(u"案例十四 | 受戒犍度", u"案例十四 | 比丘尼犍度")
        npk += 1
assert npk == 1, u"篇聚欄命中 %d（欲 1）" % npk
print(u"  篇聚欄：中途遇賊一案 受戒犍度➔比丘尼犍度 ✓×1")

txt = u"\r\n".join(L)
assert txt.count(u"\r") == txt.count(u"\n") == len(L) - 1, u"CRLF 變形"
print(u"指針歸位 %d 處｜自報 %d 處" % (nfix, nrep))
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
assert not os.path.exists(BAK) or io.open(BAK, encoding="utf-8", newline=u"").read() == raw, u"備份不同本"
if not os.path.exists(BAK):
    shutil.copy2(BOOK, BAK)
with open(BOOK, "wb") as fh:
    fh.write(txt.encode("utf-8"))
chk = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert chk == txt, u"回讀不符"
print(u"已寫檔｜sha %s→%s｜備份 %s" % (
    sha0[:12], hashlib.sha256(chk.encode("utf-8")).hexdigest()[:12], os.path.basename(BAK)))
