# -*- coding: utf-8 -*-
"""第 42 輪補刀二：另兩處「歸語於佛／祖而語料無據」之偽逐字（皆在案例區外，故戊、辛兩閘向所未見）。
   ①L856 娑伽陀之問——本律所記者別見第九章案例二十七，此句乃他傳之問，須去自稱逐字
   ②L1169「毘尼住者，正法亦住」——本律無此文（『正法住』『毘尼住』俱 0 見），乃律家常談
用法：python -X utf8 _work/r9fix2.py [--go]"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
GO = u"--go" in sys.argv
BOOK = HP.SRC
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
L = raw.split(u"\r\n")
V, NV = _tk.VINAYA, _tk.norm(_tk.VINAYA)

assert _tk.norm(u"如今不能降伏小龍，況能降伏大龍") in NV, u"引路之句今不成連写"
for k in [u"恭敬心", u"毘尼住", u"正法亦住"]:
    assert V.count(k) in (0, 6), u"『%s』計數走樣：%d" % (k, V.count(k))

PAIRS = [
    (u"> 佛陀又問：**「娑伽陀向來恭敬如來，如今他躺在地上，還能對如來生起恭敬心嗎？」**",
     u"> 佛陀又問（此句非本律之文，乃他傳所記之問，今譯如次）：「娑伽陀向來恭敬如來，如今他躺在地上，還能對如來生起恭敬心嗎？」——本律所記的問答別見第九章案例二十七，佛告阿難：「如今不能降伏小龍，況能降伏大龍。」"),
    (u"* **「毘尼（戒律）住者，正法亦住；毘尼若亡，正法亦亡。」**",
     u"* 律家常談：「毘尼住者，正法亦住；毘尼若亡，正法亦亡。」——此八字本律無文（『正法住』『毘尼住』俱不見於六十卷），乃後世護律者替第十句義下的註腳，本書取其意、不稱其逐字。"),
]
for old, new in PAIRS:
    hits = [i for i, s in enumerate(L) if old in s]
    assert sum(L[i].count(old) for i in hits) == 1, u"命中 %d（應 1）：%s" % (len(hits), old[:34])
    for i in hits:
        L[i] = L[i].replace(old, new)
        print(u"  ✓ L%-5d｜%s…" % (i + 1, old[:30]))

txt = u"\r\n".join(L)
assert txt.count(u"\r\n") == len(L) - 1, u"CRLF 變形"
print(u"行數 %d→%d｜%s" % (len(raw.split(u"\r\n")), len(L), u"寫檔" if GO else u"覆核模式（未寫檔）"))
if GO:
    io.open(BOOK, u"w", encoding="utf-8", newline=u"").write(txt)
