# -*- coding: utf-8 -*-
"""第 44 輪・重建後之產物病二則：印面直呼附錄篇名，精簡版無從索隱。
十線地圖『如何節讀』與卷首凡例第一款各一處，改以「篇末之歷條總表」稱之並標全本始有。
用法：python -X utf8 _work/r11apxref.py [--go]"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
L = io.open(BOOK, encoding="utf-8", newline=u"").read().split(u"\r\n")
n = 0


def sub(old, new, want=1):
    global n
    hits = [i for i, s in enumerate(L) if old in s]
    tot = sum(L[i].count(old) for i in hits)
    assert tot == want, u"命中 %d（應 %d）：%s" % (tot, want, old[:44])
    for i in hits:
        L[i] = L[i].replace(old, new)
        print(u"  \u2713 L%d" % (i + 1))
    n += tot


# 一、十線地圖・如何節讀
sub(u"\u7bc7\u672b\u300a\u5168\u6212\u672c\u6b77\u689d\u7e3d\u8868\u300b",      # 篇末《全戒本歷條總表》
    u"\u7bc7\u672b\u4e4b\u6b77\u689d\u7e3d\u8868\uff08\u552f\u5168\u672c\u6709\u4e4b\uff09")   # 篇末之歷條總表（唯全本有之）
# 二、卷首凡例第一款
sub(u"\u552f\u300a\u9644\u9304\u300b\u6b77\u689d\u4e4b\u6212\u6587\u96d6\u4e0d\u52a0\u7c97\u9ad4\u800c\u4ecd\u662f\u9010\u5b57\uff0c\u5176\u4f8b\u898b\u8a72\u7bc7\u51e1\u4f8b",
    u"\u552f\u7bc7\u672b\u4e4b\u6b77\u689d\u7e3d\u8868\uff08\u552f\u5168\u672c\u6709\u4e4b\uff09\u6240\u6536\u6212\u6587\u4e0d\u52a0\u7c97\u9ad4\u800c\u4ecd\u662f\u9010\u5b57\uff0c\u5176\u4f8b\u898b\u8a72\u7bc7\u51e1\u4f8b")
txt = u"\r\n".join(L)
key = u"\u5168\u6212\u672c\u6b77\u689d\u7e3d\u8868"                       # 全戒本歷條總表
ai = next(i for i, s in enumerate(L) if s.startswith(u"# 附錄"))
assert txt[:txt.index(u"# 附錄")].count(key) == 0, u"印面猶直呼附錄篇名"
assert txt.count(u"\r\n") == len(L) - 1, u"CRLF 變形"
print(u"共改 %d 處｜全檔 %d 行" % (n, len(L)))
if u"--go" in sys.argv:
    io.open(BOOK, "w", encoding="utf-8", newline=u"").write(txt)
    print(u"已改檔")
else:
    print(u"未改（加 --go）")
