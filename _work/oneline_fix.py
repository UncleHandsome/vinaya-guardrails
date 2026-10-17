# -*- coding: utf-8 -*-
"""一線修書：以草稿之同行為準，替換書中該行（只依內容定錨，不依行號）。
用法：python -X utf8 _work/oneline_fix.py <草稿檔> <草稿行號 1 起>
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
D, NO = sys.argv[1], int(sys.argv[2])
dline = io.open(D, encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")[NO - 1].rstrip()
raw = io.open(BOOK, encoding="utf-8", newline="").read()
L = raw.split("\r\n")

# 以「同段首 24 字」為錨，找書中待修之行
key = dline[:24]
cand = [i for i, l in enumerate(L) if l.startswith(key) or key in l]
assert len(cand) == 1, "錨點不唯一：%s → %s" % (key, cand)
i = cand[0]
old = L[i]
print("L%d 舊尾：%s" % (i + 1, old[-34:]))
print("     新尾：%s" % dline[-34:])
assert old.strip() != dline.strip(), "兩行已相同，無需修"
L[i] = dline
new = "\r\n".join(L)
assert new.count("\r\n") == raw.count("\r\n"), "CRLF 變形"
assert len(L) == raw.count("\r\n") + 1, "行數變形"
io.open(BOOK, "w", encoding="utf-8", newline="").write(new)
print("已修 L%d｜行數 %d 不變" % (i + 1, len(L)))
