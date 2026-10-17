# -*- coding: utf-8 -*-
"""第 44 輪・歸正印面之日式中黑『・』（verify_hulan 戊2 所報之應無形）。
十見全為历輪手打：目錄與正文之案例題・節題・靶點・散文指針。
書中慣例用全形頓號『、』；散文內『案例三・第18條』一類改作『案例三、案例一（第18條、第1條）』。
用法：python -X utf8 _work/r11zhonghei.py [--go]"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
ZH = u"\u30fb"                                     # ・
DUN = u"\u3001"                                    # 、
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
L = raw.split(u"\r\n")
assert u"".join(L).count(ZH) == 10, u"今有 『・』 %d 見（應 10）" % u"".join(L).count(ZH)

# 一、散文一處須重排（外層已是括號，不便再套）
p1 = (u"\u7b2c\u4e03\u7ae0\u6848\u4f8b\u4e09" + ZH + u"\u7b2c18\u689d\uff0c\u8207"
      u"\u7b2c\u4e03\u7ae0\u6848\u4f8b\u4e00" + ZH + u"\u7b2c1\u689d")
r1 = (u"\u7b2c\u4e03\u7ae0\u6848\u4f8b\u4e09" + DUN + u"\u6848\u4f8b\u4e00"
      u"\uff08\u7b2c18\u689d" + DUN + u"\u7b2c1\u689d\uff09")
n = 0


def sub(old, new, want=1, only=None):
    global n
    rng = only if only is not None else range(len(L))
    hits = [i for i in rng if old in L[i]]
    tot = sum(L[i].count(old) for i in hits)
    assert tot == want, u"命中 %d（應 %d）：%s" % (tot, want, old[:40])
    for i in hits:
        L[i] = L[i].replace(old, new)
        print(u"  \u2713 L%d" % (i + 1))
    n += tot


sub(p1, r1, 1)
sub(ZH, DUN, 8)                                     # 其餘八處逕改頓號
txt = u"\r\n".join(L)
assert txt.count(ZH) == 0, u"猶存 『・』 %d 見" % txt.count(ZH)
assert txt.count(u"\r\n") == len(L) - 1, u"CRLF 變形"
assert len(L) == raw.count(u"\r\n") + 1, u"行數變形"
print(u"共改 %d 處｜全檔 %d 行" % (n, len(L)))
if u"--go" in sys.argv:
    io.open(BOOK, "w", encoding="utf-8", newline=u"").write(txt)
    print(u"已改檔")
else:
    print(u"未改（加 --go）")
