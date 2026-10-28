# -*- coding: utf-8 -*-
"""第 57 輪・庚之退刀（單處）：把 L4730『十一條如次』的分段併回一行——h4seq 現形為錯切。
    （連綴式列舉之節奏在『一、二、…十一、』本身；一經換段，散文手寫序號即成 5→7 斷鏈。）
驗：①續行須為『空行＋縮排片段』之形，併回時只取其去縮排之文（縮排是分段所加，非原文所有）
   ②併回後以同錨重切，須得同樣片段（可逆）③漢字總數不變（此段 501 字）④全書行數 -4。
   註：本器不用全檔哈希作驗——其餘 14 處分段係有意保留，檔本不該等於切分前。
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.abspath(__file__))); _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import hlsplit57_data as D  # noqa: E402

BOOK = HP.SRC
PRE = u"十一條如次"
CN_WANT = 501
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert raw.count(u"\r") == raw.count(u"\n"), u"入口 CRLF 已傷"
L = raw.split(u"\r\n")
N0 = len(L)
anchors = dict(D.SPL_ALL)[4730]
i = next(x for x, l in enumerate(L) if l.startswith(PRE))
k = len(anchors)
segs, j = [L[i]], i + 1
for _ in range(k):
    assert j + 1 < len(L) and not L[j].strip(), u"L%d 之後非『空行＋續段』之形" % (j + 1)
    segs.append(L[j + 1])
    j += 2
assert not any(s.startswith(PRE) for s in segs[1:]), u"續段形制不如期"
parts = [segs[0]] + [s.lstrip() for s in segs[1:]]        # 縮排係分段所加，去之
merged = u"".join(parts)
assert D.CN(merged) == CN_WANT, u"併回後 %d 字，應 %d" % (D.CN(merged), CN_WANT)
assert D.cut(merged, anchors) == parts, u"併回後重切不合，未敢寫"
print(u"併回 L%d–L%d（%d 行）→ 1 行｜%d 字｜重切可逆 ✓" % (i + 1, j, k + 1, D.CN(merged)))
new = L[:i] + [merged] + L[j:]
assert len(new) == N0 - 2 * k, u"行數退差不對：%d→%d" % (N0, len(new))
txt = u"\r\n".join(new)
assert txt.count(u"\r") == txt.count(u"\n"), u"出口 CRLF 變形"
assert D.CN(txt) == D.CN(raw), u"全書漢字總數變形"
print(u"全書行數 %d→%d" % (N0, len(new)))
if u"--go" in sys.argv:
    io.open(BOOK, "w", encoding="utf-8", newline=u"").write(txt)
    print(u"已寫檔")
else:
    print(u"（乾跑：加 --go 始寫）")
