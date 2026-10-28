# -*- coding: utf-8 -*-
"""第 82 輪・外路第三十一報之真病（五刀，皆以今册量得）：
   甲、卷首自制語邏輯倒反：『凡不可指認今人者，一概不寫』——前句方云『全書無一例出於今人今事』，
       此句字面卻成『只寫能指認出現代人的』。改『凡涉可指認之今人者，一概不寫』。
   乙、凡例孤標『（款①）』——全書款②③④俱 0，是編寫大綱之殘留，削之。
   丙、名形分裂：偷蘭難陀 22 見（全在引號外之散文），而第十二・十三章與語料俱作偷羅難陀
       （語料 172:32）——散文處一律歸『偷羅難陀』；引號內不動（律文之形以語料為準）。
   丁、目錄之第十四・十五章副題仍是舊稿（『身體純化…』／『度人考核…』），正文已換為
       『身軀、空間與共住心理學』／『生計、准入風控與二部僧法治』——副題自正文 H2 現取，不重打。
   戊、『四大生活防禦模組』『四大法治重鎮』——同節之題與圖俱作『五大』，導言首句漏改，二處歸五。
"""
import hashlib
import io
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import hulan_path as HP                                        # noqa: E402

GO = u"--go" in sys.argv
raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
L = raw.split(u"\r\n")
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
errs = []
QUOTE = re.compile(u"「[^」]*」")


def one(pred, what):
    got = [i for i, s in enumerate(L) if pred(s)]
    if len(got) != 1:
        errs.append(u"%s 命中 %d（宜 1）" % (what, len(got)))
        return None
    return got[0]


# 甲
i = one(lambda s: u"凡不可指認今人者，一概不寫" in s, u"甲之句")
if i is not None:
    L[i] = L[i].replace(u"凡不可指認今人者，一概不寫", u"凡涉可指認之今人者，一概不寫")

# 乙
i = one(lambda s: u"（款①）" in s, u"乙之孤標")
if i is not None:
    L[i] = L[i].replace(u"（款①）", u"")

# 丙：引號外之偷蘭難陀 → 偷羅難陀
n_c = 0
for k, s in enumerate(L):
    if u"偷蘭難陀" not in s:
        continue
    out, pos = [], 0
    for m in QUOTE.finditer(s):
        out.append(s[pos:m.start()].replace(u"偷蘭難陀", u"偷羅難陀"))
        out.append(m.group(0))
        pos = m.end()
    out.append(s[pos:].replace(u"偷蘭難陀", u"偷羅難陀"))
    ns = u"".join(out)
    if ns != s:
        n_c += s.count(u"偷蘭難陀") - ns.count(u"偷蘭難陀")
        L[k] = ns
print(u"丙｜改 %d 處（引號內不動）" % n_c)
left = sum(s.count(u"偷蘭難陀") for s in L)
print(u"   餘『偷蘭難陀』%d 處（宜 0 或皆在引內）" % left)

# 丁：目錄副題自正文取（唯目錄區之內，免誤逮章末回顧之『* **第十四章：**』）
T0 = next(i for i, s in enumerate(L) if s.startswith(u"# ") and u"全書詳細目錄" in s)
T1 = next(i for i in range(T0 + 1, len(L)) if L[i].startswith(u"# "))
for num in (u"十四", u"十五"):
    h = one(lambda s, n=num: s.startswith(u"# 第" + n + u"章"), u"第%s章 H1" % num)
    if h is None:
        continue
    if not L[h + 1].startswith(u"## "):
        errs.append(u"第%s章無副題" % num)
        continue
    title = L[h][2:].strip()
    sub = L[h + 1][3:].strip()
    new = u"* **" + title + sub + u"**"
    t = one(lambda s, n=num: s.strip().startswith(u"* **第" + n + u"章") and T0 < L.index(s) < T1, u"目錄第%s章條" % num)
    if t is None:
        continue
    print(u"丁｜L%-5d 舊：%s" % (t + 1, L[t].strip()[:70]))
    print(u"       新：%s" % new[:70])
    L[t] = new

# 戊
for a, b in ((u"四大生活防禦模組", u"五大生活防禦模組"), (u"四大法治重鎮", u"五大法治重鎮")):
    i = one(lambda s, x=a: x in s, a)
    if i is not None:
        L[i] = L[i].replace(a, b)

if errs:
    for e in errs:
        print(u"✗ " + e)
    sys.exit(1)
print(u"行數 %d → %d" % (len(raw.split(u"\r\n")), len(L)))
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
BK = HP.bakpath(u"82a")
io.open(BK, "wb").write(raw.encode("utf-8"))
out = u"\r\n".join(L)
for k in range(3):
    try:
        io.open(HP.SRC, "wb").write(out.encode("utf-8"))
        break
    except OSError as e:
        print(u"  寫檔重試 %d：%s" % (k + 1, e))
        time.sleep(2)
chk = io.open(HP.SRC, "rb").read().decode("utf-8")
print(u"已寫檔｜sha %s→%s｜回讀%s｜備份 %s" % (
    sha0, hashlib.sha256(chk.encode("utf-8")).hexdigest()[:12],
    u"全等" if chk == out else u"不等!", os.path.relpath(BK, ROOT)))
