# -*- coding: utf-8 -*-
"""第 71 輪・乙刀：『案外之條目』款之號次改列舉（範圍式在產生器中只作弱指針，非案例行即不展開）。
病：入冊刀以 ranges() 生『第99～100條』之簡写，而 `gen_appendix` 之規——範圍所推之號只為弱指針，
    且非案例行遇範圍即 continue——遂使此十二條全無落點（gapcensus 報未展開 12）。
治：款題之內逐枚列號（『第99、100條』），案例標題之範圍式則不動（案例行遇範圍本會展開）。
用法：python -X utf8 _work/hlfix71b.py [--go]
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
BAK = HP.bakpath("71b")
GO = u"--go" in sys.argv
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert raw.count(u"\r") == raw.count(u"\n") == raw.count(u"\r\n"), u"入口 CRLF 已傷"
L = raw.split(u"\r\n")
N0, sha0 = len(L), hashlib.sha256(raw.encode("utf-8")).hexdigest()

hits = [i for i, l in enumerate(L) if l.startswith(u"#### （一） 案外之條目（第")]
assert len(hits) == 2, u"案外之款見 %d 處（欲 2）" % len(hits)
n = 0
for i in hits:
    old = L[i]
    inside = old[old.index(u"（第") + 1: old.index(u"條）")]
    nums = []
    for part in inside[1:].split(u"、"):
        if u"～" in part:
            a, b = part.split(u"～")
            nums += list(range(int(a), int(b) + 1))
        else:
            nums.append(int(part))
    new = u"#### （一） 案外之條目（第%s條）" % u"、".join(str(x) for x in nums)
    L[i] = new
    n += 1
    print(u"  L%-5d ✓ %s" % (i + 1, new[:78]))
    print(u"           舊 %s" % old[:78])
assert len(L) == N0, u"行數變形"
txt = u"\r\n".join(L)
assert txt.count(u"\r") == txt.count(u"\n") == len(L) - 1, u"CRLF 變形"
print(u"改 %d 行" % n)
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
if not os.path.exists(BAK):
    shutil.copy2(BOOK, BAK)
for tries in range(3):
    try:
        with open(BOOK, "wb") as fh:
            fh.write(txt.encode("utf-8"))
        break
    except OSError as e:
        print(u"  ! 寫檔失敗（%s）第 %d 次重試" % (e.strerror, tries + 1))
        import time
        time.sleep(2)
else:
    raise SystemExit(u"寫正本三次不成")
chk = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert chk == txt, u"回讀不符"
print(u"已寫檔｜sha %s→%s｜備份 %s" % (
    sha0[:12], hashlib.sha256(chk.encode("utf-8")).hexdigest()[:12], os.path.relpath(BAK, HP.ROOT)))
