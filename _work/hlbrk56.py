# -*- coding: utf-8 -*-
"""小刀（第 56 輪附五）：題詞之引句與署名行須以『行尾兩空格』硬換行（書中既有之制，
如《四分律》六條題詞皆然）——否則 pandoc 併為一段，短句者署名會黏在引句同一行（印面 p32 實測）。
用法：python -X utf8 _work/hlbrk56.py [--go]
"""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import hulan_path as HP  # noqa: E402

PAIRS = [
    (u"> 「如王邊城七事具足。」" + chr(13),
     u"> 「如王邊城七事具足。」  " + chr(13)),
]
GO = u"--go" in sys.argv[1:]
raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
c0 = raw.count(u"\r\n")
for i, (old, new) in enumerate(PAIRS, 1):
    g = raw.count(old)
    if g != 1:
        raise SystemExit(u"靶 %d 命中 %d（須 1）" % (i, g))
    raw = raw.replace(old, new)
if raw.count(u"\r\n") != c0:
    raise SystemExit(u"CRLF 變形")
print(u"兩處硬換行已補｜字 %+d" % (len(raw) - len(io.open(HP.SRC, encoding='utf-8', newline='').read())))
if GO:
    io.open(HP.SRC, "w", encoding="utf-8", newline="").write(raw)
    print(u"已入刀：SHA %s" % hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16])
else:
    print(u"（覆核模式）")
