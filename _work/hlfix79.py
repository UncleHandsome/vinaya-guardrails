# -*- coding: utf-8 -*-
"""第 79 輪・目錄條目還座：十線地圖自【第一部】之前移回尾部（「尾聲」之下、附錄之上）。

緣由：外路第廿七報稱『目錄序位倒置』（條目在目錄之尾，而靶在書前），76 輪遂提條目至部題之前。
今奉作者令『放後面』——作者原稿（git 30b689f・215d0d8 俱證）本以此條列於目錄之末，
其下括注『（前置於第一部之前，全書之路標）』正是如實交代『目錄列在末、正文排在先』之兩地，
非病也。故還座，並改 toccensus 之尺護此制（見 _work/toccensus.py 之序位目）。

唯動目錄之一行；正文之十線地圖區塊（H1 及其下全表）不動——作者自標『前置於第一部之前』。
"""
import hashlib
import io
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import hulan_path as HP                                        # noqa: E402

GO = u"--go" in sys.argv
MP = u"十線地圖"
raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
L = raw.split(u"\r\n")
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]

ent = [i for i, s in enumerate(L) if s.startswith(u"* **" + MP)]
tail = [i for i, s in enumerate(L) if s.startswith(u"  * 尾聲")]
apx = [i for i, s in enumerate(L) if s.startswith(u"* **附錄")]
toc_end = next(i for i, s in enumerate(L) if s.startswith(u"# ") and i > 80)   # 目錄區塊之末
errs = []
if len(ent) != 1:
    errs.append(u"目錄之十線條目命中 %d（宜 1）" % len(ent))
if len(tail) != 1:
    errs.append(u"『  * 尾聲』錨命中 %d（宜 1）" % len(tail))
if len(apx) != 1:
    errs.append(u"目錄之附錄條目命中 %d（宜 1）" % len(apx))
if errs:
    for e in errs:
        print(u"✗ " + e)
    sys.exit(1)
i_e, i_t, i_a = ent[0], tail[0], apx[0]
print(u"今｜條目 L%d・尾聲 L%d・附錄條 L%d｜條目%s尾聲" % (
    i_e + 1, i_t + 1, i_a + 1, u"在後" if i_e > i_t else u"在前"))
if i_e > i_t:
    print(u"條目已在尾部，無需動刀")
    sys.exit(0)
line = L[i_e]
assert u"前置於第一部之前" in line, u"條目括注形制有變，須先查再移：%s" % line[:60]

# 削原行（連帶其後之空行，免目錄頭生雙空）
del L[i_e]
if i_e < len(L) and L[i_e].strip() == u"" and i_e - 1 >= 0 and L[i_e - 1].strip() == u"":
    del L[i_e]
# 還座：尾聲之下、附錄條之上（原稿之次）
i_t2 = next(i for i, s in enumerate(L) if s.startswith(u"  * 尾聲"))
i_a2 = next(i for i, s in enumerate(L) if s.startswith(u"* **附錄"))
L.insert(i_a2, line)
print(u"移後｜條目 L%d・附錄條 L%d｜目錄區塊末行 L%d" % (i_a2 + 1, i_a2 + 2, toc_end))
print(u"── 目錄之尾（移後）──")
for j in range(i_t2 - 1, min(len(L), i_a2 + 3)):
    print(u"  L%-5d%s %s" % (j + 1, u"▶" if j == i_a2 else u" ", L[j][:76]))

if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
BK = HP.bakpath(u"79a")
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
print(u"已寫檔｜行 %d→%d｜sha %s→%s｜回讀%s｜備份 %s" % (
    len(raw.split(u"\r\n")), len(L), sha0,
    hashlib.sha256(chk.encode("utf-8")).hexdigest()[:12],
    u"全等" if chk == out else u"不等!", os.path.relpath(BK, ROOT)))
