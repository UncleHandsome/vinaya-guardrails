# -*- coding: utf-8 -*-
"""第 44 輪补丁（自查・序數族）：四處「序號↔罪名」錯植之歸一。
   ①L3465 第六僧殘→第八僧殘（謗戒族，其落點『第六章案例四』本作第八、九僧殘）
   ②L4853 第八波羅夷→第六波羅夷（「八事成重」乃尼端第六；全書另五處俱作第六，已核）
   ③L5799 第八波羅夷→第四波羅夷（「濫充聖證」＝大妄語，比丘第四・尼第四同）
   ④L5816 「第七波羅夷：以財物成事之尼版」→依律文改其評（尼第七＝知他犯波羅夷不自舉）
用法：python -X utf8 _work/r11fix.py [--go]"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
GO = u"--go" in sys.argv
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
L = raw.split(u"\r\n")
n = 0


def sub(old, new, want=1):
    global n
    hits = [i for i, s in enumerate(L) if old in s]
    tot = sum(L[i].count(old) for i in hits)
    assert tot == want, u"命中 %d（應 %d）：%s" % (tot, want, old[:50])
    for i in hits:
        L[i] = L[i].replace(old, new)
        print(u"  \u2713 L%d" % (i + 1))
    n += tot


sub(u"\u53e6\u6709\u7b2c\u516d\u50e7\u6b98\u8207\u55ae\u63d0\u8af8\u689d\u9023\u74b0\u8655\u7406",          # 另有第六僧殘與單提諸條連環處理
    u"\u53e6\u6709\u7b2c\u516b\u50e7\u6b98\u8207\u55ae\u63d0\u8af8\u689d\u9023\u74b0\u8655\u7406")          # 第八
sub(u"\u3010\u7b2c\u516b\u6ce2\u7f85\u5937\uff1a\u516b\u4e8b\u6210\u91cd\u3011",                      # 【第八波羅夷：八事成重】
    u"\u3010\u7b2c\u516d\u6ce2\u7f85\u5937\uff1a\u516b\u4e8b\u6210\u91cd\u3011")
sub(u"\u3010\u7b2c\u516b\u6ce2\u7f85\u5937\uff1a\u6feb\u5145\u8056\u8b49",                            # 【第八波羅夷：濫充聖證
    u"\u3010\u7b2c\u56db\u6ce2\u7f85\u5937\uff1a\u6feb\u5145\u8056\u8b49")
sub(u"\u3010\u7b2c\u4e03\u6ce2\u7f85\u5937\uff1a\u4ee5\u8ca1\u7269\u6210\u4e8b\u4e4b\u5c3c\u7248\u3011",  # 【第七波羅夷：以財物成事之尼版】
    u"\u3010\u7b2c\u4e03\u6ce2\u7f85\u5937\uff1a\u77e5\u4ed6\u72af\u91cd\u800c\u4e0d\u81ea\u8209\u2014\u2014"
    u"\u88ab\u8a98\u8005\u4e4b\u5516\u53e3\u3011")
print(u"\u5171 %d \u8655" % n)
if GO:
    txt = u"\r\n".join(L)
    assert txt.count(u"\r\n") == len(L) - 1, u"CRLF \u8b8a\u5f62"
    io.open(BOOK, "w", encoding="utf-8", newline=u"").write(txt)
    print(u"\u5df2\u6539\u6a94")
else:
    print(u"\u672a\u6539\uff08\u52a0 --go\uff09")
