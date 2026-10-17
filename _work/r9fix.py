# -*- coding: utf-8 -*-
"""第 42 輪補刀：自造之兩疵——①L714「谓之」之簡形（字典第十三度已補：谓→謂）②L725「可執行的文」脫一「條」字。
用法：python -X utf8 _work/r9fix.py [--go]"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _simpdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
GO = u"--go" in sys.argv
BOOK = HP.SRC
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
L = raw.split(u"\r\n")

PAIRS = [(u"律中谓之「隨犯隨制」。", u"律中謂之「隨犯隨制」。"),
         (u"而每一次撞線都留下一條可執行的文：", u"而每一次撞線都留下一條可執行的條文：")]
for old, new in PAIRS:
    hits = [i for i, s in enumerate(L) if old in s]
    assert sum(L[i].count(old) for i in hits) == 1, u"命中 %d（應 1）：%s" % (len(hits), old[:30])
    for i in hits:
        L[i] = L[i].replace(old, new)
        print(u"  ✓ L%-5d｜%s" % (i + 1, old[:26]))
assert u"谓" in _simpdict.MAP and _simpdict.MAP[u"谓"] == u"謂", u"字典未收 谓，尺仍會漏"
print(u"  （字典已收 谓→謂，今 %d 枚）" % len(_simpdict.MAP))
if GO:
    txt = u"\r\n".join(L)
    assert txt.count(u"\r\n") == len(L) - 1, u"CRLF 變形"
    io.open(BOOK, u"w", encoding="utf-8", newline=u"").write(txt)
    print(u"已寫檔")
else:
    print(u"覆核模式（未寫檔）")
