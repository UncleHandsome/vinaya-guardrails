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

# 號段無缺（第 83 輪立・外路第三十二報之線索）：圍欄之題若自宣「第A～B條」，則圖內諸號須覆 A..B。
# 病源：第九章後半部矩陣宣「第46～90條」而漏第54條——摘要圖與案例之戶（案例七正是第54條）不一致。
import re                                                      # noqa: E402
miss_bad = []
for k, (_a, _b, body, _chp) in enumerate(blocks, 1):
    if not body:
        continue
    m = re.search(u"第(\\d{1,3})[～~\\-](\\d{1,3})條", body[0])
    if not m:
        continue
    lo, hi = int(m.group(1)), int(m.group(2))
    nums = set()
    for s in body[1:]:
        for r in re.finditer(u"(?<!\\d)(\\d{1,3})\\s*[～~\\-]\\s*(\\d{1,3})(?!\\d)", s):
            nums.update(range(int(r.group(1)), int(r.group(2)) + 1))
        for x in re.findall(u"(?<!\\d)(\\d{1,3})(?!\\d)", s):
            nums.add(int(x))
    gap = [n for n in range(lo, hi + 1) if n not in nums]
    if gap:
        miss_bad.append((k, lo, hi, gap))
print("號段自宣而圖內缺號：%d 段" % len(miss_bad))
for k, lo, hi, gap in miss_bad:
    print("  ✗ 段%d｜宣第%d～%d條，缺 %s" % (k, lo, hi, u"、".join(str(x) for x in gap)))
_pl = [u"【第1～5條之圖】", u"│  1 甲  2 乙  3 丙  5 戊"]
_m = re.search(u"第(\\d{1,3})[～~\\-](\\d{1,3})條", _pl[0])
_ns = set()
for s in _pl[1:]:
    for r in re.finditer(u"(?<!\\d)(\\d{1,3})\\s*[～~\\-]\\s*(\\d{1,3})(?!\\d)", s):
        _ns.update(range(int(r.group(1)), int(r.group(2)) + 1))
    for x in re.findall(u"(?<!\\d)(\\d{1,3})(?!\\d)", s):
        _ns.add(int(x))
_gap = [n for n in range(int(_m.group(1)), int(_m.group(2)) + 1) if n not in _ns]
print("  號段之負測｜植缺 4 逮 %d（宜 1）" % len(_gap))
sys.exit(1 if (miss_bad or len(_gap) != 1) else 0)
