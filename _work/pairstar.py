# -*- coding: utf-8 -*-
"""星號之兩查：冊上字面 `**` 之成因（散文未閉・圍欄圖文）與 span 切分之盲。

用法：python -X utf8 _work/pairstar.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import pymupdf as pm        # noqa: E402

PAIR = [("起心動念", "pair1_screen.pdf", "起心動念：四分律的心智顯微鏡與唯識解剖.txt"),
        ("如法推尋", "pair2_screen.pdf", "如法推尋：僧伽憲政、法權審理與修復正義.txt")]

for name, pdfn, srcn in PAIR:
    d = pm.open(str(ROOT / "_print" / pdfn))
    raw = (ROOT / srcn).read_bytes().decode("utf-8-sig").replace("\r\n", "\n").split("\n")
    print("=" * 74)
    print("■", name)
    for i in range(d.page_count):
        spans = [sp["text"] for b in d[i].get_text("dict")["blocks"]
                 for ln in b.get("lines", []) for sp in ln["spans"] if sp["text"].strip()]
        joined = [s for s in spans if "**" in s]
        loose = [s for s in spans if s.count("*") and "**" not in s]
        if joined or loose:
            print("  p%-4d 含 ** 之 span %d・單星 span %d｜例：%s"
                  % (i + 1, len(joined), len(loose), (joined or loose)[0][:52].replace("\n", "")))
    d.close()

print("=" * 74)
print("■ 散文未閉之 `**`（源檔逐行數星號之奇偶，奇者為候選）")
for name, _p, srcn in PAIR:
    raw = (ROOT / srcn).read_bytes().decode("utf-8-sig").replace("\r\n", "\n").split("\n")
    inf, odd = False, []
    for i, l in enumerate(raw, 1):
        if re.match(r"^\s*```", l):
            inf = not inf
            continue
        if inf or not l.strip() or l.strip().startswith("#"):
            continue
        if l.count("**") % 2:
            odd.append((i, l.strip()[:66]))
    print(f"  {name}：散文行內 `**` 成對不合者 {len(odd)} 行")
    for i, s in odd[:10]:
        print(f"     L{i} 「{s}」")
