# -*- coding: utf-8 -*-
"""圍欄圖體檢：列出每段 ``` 圖之序號、所在章、源檔行範圍、格寬（寬字=2）、最長行。
用法：python -X utf8 _work/fence_audit.py [段序 ...]  → 不給段序只出清單，給段序則連內容一併吐出。
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_print"))
from build_hulan import cw_units  # 格寬模型與印面同源，勿另立口徑  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
t = io.open(BOOK, encoding="utf-8", newline="").read()
lines = t.split("\r\n")
cw = cw_units


blocks, i, cur, chapter = [], 0, None, ""
for ln, s in enumerate(lines, 1):
    if s.startswith("# ") and not s.startswith("##"):
        chapter = s[2:24]
    if s.strip().startswith("```"):
        if cur is None:
            cur = [ln, None, [], chapter]
        else:
            cur[1] = ln
            blocks.append(cur)
            cur = None
    elif cur is not None:
        cur[2].append(s)

want = [a for a in sys.argv[1:] if a.isdigit()]
print("源檔行數：%d｜圍欄段：%d" % (len(lines), len(blocks)))
print("%-4s %-6s %-6s %-42s %s" % ("序", "行", "格寬", "章", "最長行首字"))
for k, (a, b, body, chp) in enumerate(blocks, 1):
    w = max(cw(x) for x in body) if body else 0
    wl = [x for x in body if cw(x) == w]
    flag = "★過寬" if w > 95 else ""
    print("%-4d %-6s %-6d %-42s %s %s" % (k, "%d-%d" % (a, b), w, chp, (wl[0][:34] if wl else ""), flag))
    if want and str(k) in want:
        for j, s in enumerate(body):
            print("        | %3d %s（%d）" % (a + 1 + j, s, cw(s)))
        print("        +------------------------")
