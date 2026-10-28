# -*- coding: utf-8 -*-
"""第 57 輪・戊：新第十一章內兩枚『粗體＋引號』之本書自製名（停權清單／親友七法）去式樣。
凡例款①：引號與粗體相合之文必是律文原句；自製名只作強調，故留粗體、去引號（與 57 輪甲之五枚同案）。
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
FIX = [(u"**「停權清單」**", u"**停權清單**"),
       (u"**「親友七法」**", u"**親友七法**")]
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert raw.count(u"\r") == raw.count(u"\n"), u"入口 CRLF 已傷"
for old, new in FIX:
    c = raw.count(old)
    assert c == 1, u"錨命中 %d：%s" % (c, old)
    raw = raw.replace(old, new)
    print(u"  去式樣：%s → %s" % (old, new))
assert raw.count(u"\r") == raw.count(u"\n"), u"出口 CRLF 變形"
if u"--go" in sys.argv:
    io.open(BOOK, "w", encoding="utf-8", newline=u"").write(raw)
    print(u"已寫檔")
else:
    print(u"（乾跑：加 --go 始寫）")
