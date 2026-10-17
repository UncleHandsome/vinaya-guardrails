# -*- coding: utf-8 -*-
"""後三十卷之揵度地圖：列出語料中所有「X揵度／X犍度」之標題行（原檔標題行無縮排），
   報其檔、起訖偏移與字數——補案前先量哪一揵度有多長、書中用過與否。
   （語料作「揵度」，書中通行作「犍度」，此尺兩者俱收，勿只查其一而誤判書中未用。）
用法：python -X utf8 _work/khandha_map.py [詞…]　　詞＝只報含此詞之揵度（並報其內含次數）
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import glob
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = HP.SRC
bk = io.open(BOOK, encoding="utf-8", newline="").read()

HEAD = re.compile(u"^([^ \\n，。：；【】]{2,12}[揵犍]度[^\\n，。：；]{0,6})$", re.M)
files = sorted(glob.glob(os.path.join(ROOT, u"原文", u"*.txt")))
rows = []
for f in files:
    t = io.open(f, encoding="utf-8", errors="ignore").read().replace(u"\r\n", u"\n")
    hits = [(m.start(), m.group(1)) for m in HEAD.finditer(t)]
    for i, (pos, name) in enumerate(hits):
        end = hits[i + 1][0] if i + 1 < len(hits) else len(t)
        core = re.sub(u"[揵犍]度.*$", u"", name)
        rows.append((os.path.basename(f)[:-4], name, pos, end - pos, core))
KEYS = [a for a in sys.argv[1:] if not a.startswith("--")]
if KEYS:
    rows = [r for r in rows if any(k in r[1] or k in r[4] for k in KEYS)]
tot = sum(r[3] for r in rows)
print(u"揵度標題 %d 段｜計 %s 字" % (len(rows), format(tot, ",")))
for fn, name, pos, size, core in rows:
    tag = u"書中既用" if core and core in bk else u"書中未見"
    kw = u"｜含詞 %d" % sum(1 for k in KEYS if k in core) if KEYS else u""
    print(u"  %-8s｜%-14s｜%7s 字｜%s%s" % (fn, name, format(size, ","), tag, kw))
