# -*- coding: utf-8 -*-
"""案例盤點：逐章列出『#### 案例』標題、該案所引條次（第N條／第N～M條／第N、M條），
並匯出全書已用條次之多重集，供「還欠哪些條」之對照。只讀不改。
用法：python -X utf8 _work/case_inventory.py [章序]
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
lines = io.open(BOOK, encoding="utf-8", newline="").read().split("\r\n")

NUM = re.compile(u"第([0-9一二三四五六七八九十百～、，及]{1,12})條")
CHAPTER = re.compile(u"^# 第(.+?)章\\s*(.*)$")
CASE = re.compile(u"^#### +案例")
SEC = re.compile(u"^## +")

chs, cur = [], None
for i, s in enumerate(lines, 1):
    m = CHAPTER.match(s)
    if m and u"章" in s[:8] and not s.startswith("##"):
        cur = {"no": m.group(1), "title": m.group(2)[:22], "cases": [], "sec": ""}
        chs.append(cur)
    elif cur is not None:
        if SEC.match(s):
            cur["sec"] = s[3:26]
        if CASE.match(s):
            cur["cases"].append((i, s.strip(), cur["sec"]))

only = sys.argv[1] if len(sys.argv) > 1 else None
tot = 0
for c in chs:
    tot += len(c["cases"])
    if only and c["no"] != only:
        continue
    print("=== 第%s章｜%s｜案例 %d 則（末節：%s）" % (c["no"], c["title"], len(c["cases"]), c["sec"]))
    for ln, t, sec in c["cases"]:
        nums = NUM.findall(t)
        print("   L%-5d %-46s｜條次：%s" % (ln, t[:46], "、".join(nums) if nums else "—"))
if not only:
    used = sorted({n for c in chs for ln, t, sec in c["cases"] for n in NUM.findall(t)})
    print("\n案例標題中出現之條次（去重）：%d 筆" % len(used))
    print("案例總則數：%d｜章數：%d" % (tot, len(chs)))
