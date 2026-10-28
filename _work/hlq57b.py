# -*- coding: utf-8 -*-
"""第 57 輪・乙佐證二：於《四分律》原檔（帶標點之原文）取語錄上下文，供【律制】歸真時逐字複製。
鍵走命令列第二參數檔（每行一鍵），原檔編碼逐一試（记忆：原文/*.txt 非皆 UTF-8）。
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = sorted(os.path.join(ROOT, u"原文", f)
               for f in os.listdir(os.path.join(ROOT, u"原文")))
SRC = []
for f in FILES:
    raw = io.open(f, "rb").read()
    for enc in (u"utf-8", u"cp950", u"big5hkscs", u"gb18030"):
        try:
            SRC.append((os.path.basename(f), raw.decode(enc)))
            break
        except Exception:
            continue
    else:
        SRC.append((os.path.basename(f), raw.decode("utf-8", "ignore")))
print(u"原檔 %d 支：%s" % (len(SRC), u" ".join(u"%s(%d)" % (n, len(t)) for n, t in SRC)))

keys = [k.strip() for k in io.open(sys.argv[1], encoding="utf-8").read().split(u"\n") if k.strip()]
W = int(sys.argv[2]) if len(sys.argv) > 2 else 90
for k in keys:
    print(u"═══ 鍵：%s" % k)
    hit = 0
    for n, t in SRC:
        p = t.find(k)
        while p >= 0:
            hit += 1
            seg = t[max(0, p - W):p + len(k) + W].replace(u"\r", u"").replace(u"\n", u"⏎")
            print(u"   [%s] …%s…" % (n, seg))
            p = t.find(k, p + 1)
            if hit > 3:
                break
        if hit > 3:
            break
    if not hit:
        print(u"   ✗ 全語料無此鍵")
