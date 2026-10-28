# -*- coding: utf-8 -*-
"""『102 案三層落位』方案之可行性量測（只讀）。

量：ver39 第六章與附錄四之體積・兩冊案號形制・搬入後之印面增頁推算。
用法：python -X utf8 _work/pair102.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V39 = sorted(ROOT.glob("ver39*.md"))[0].read_bytes().decode("utf-8").split("\r\n")
F1 = (ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt").read_bytes().decode("utf-8").split("\r\n")
F2 = (ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt").read_bytes().decode("utf-8").split("\r\n")


def cjk(s):
    return sum(1 for c in s if "\u4e00" <= c <= "\u9fff")


def h1idx(lines, pat):
    return [i for i, l in enumerate(lines) if re.match(r"^#\s+" + pat, l.strip())]


print("■ ver39 之章界（H1）")
h1 = [(i + 1, l.strip()[:40]) for i, l in enumerate(V39) if re.match(r"^#\s+\S", l.strip())]
for a, b in h1:
    print(f"   L{a}: {b}")

print("\n■ 第六章之體積與內部結構")
c6 = [i for i, l in enumerate(V39) if re.match(r"^#\s+第六章", l.strip())]
c7 = [i for i, l in enumerate(V39) if re.match(r"^#\s+第七章", l.strip())]
if c6 and c7:
    a, b = c6[0], c7[0]
    seg = V39[a:b]
    print(f"   第六章＝L{a+1}〜L{b}・{b-a} 行・漢字 {cjk(chr(10).join(seg)):,}")
    for lv in (2, 3, 4):
        n = sum(1 for l in seg if re.match(r"^#{%d}\s" % lv, l.strip()))
        print(f"     H{lv} 小節 {n} 枚")
    地標 = sum(1 for l in seg if re.search(r"地標", l) and l.strip().startswith("#"))
    卡 = sum(1 for l in seg if re.match(r"^#{4,5}\s*[【\[]?", l.strip()) and "案例" in l)
    print(f"     含『地標』之標題 {地標} 枚・含『案例』之卡片標題 {卡} 枚")
    for l in seg:
        if re.match(r"^#{2,3}\s", l.strip()):
            print("       ·", l.strip()[:56])

print("\n■ 附錄四（判例原典逐條回查索引）之體積")
a4 = h1idx(V39, r"附錄四")
a5 = h1idx(V39, r"附錄五")
if a4 and a5:
    seg = V39[a4[0]:a5[0]]
    rows = [l for l in seg if l.strip().startswith("|")]
    print(f"   附錄四＝L{a4[0]+1}〜L{a5[0]}・{len(seg)} 行・漢字 {cjk(chr(10).join(seg)):,}・表行 {len(rows)}（含表頭與分隔）")
    print("   表頭：", next((l.strip()[:110] for l in seg if l.strip().startswith("|")), ""))

print("\n■ 兩冊現行之案號形制（若要『唯一通用座標』須先歸一）")
for nm, L in (("F1", F1), ("F2", F2)):
    forms = {
        "〔案NN〕": r"〔案\d{1,3}〕",
        "〔案例 NN〕": r"〔案例 ?\d{1,3}〕",
        "【案卷 NN】": r"【案卷 [^】]{1,12}】",
        "【制度案卷 NN】": r"【制度案卷[^】]{1,12}】",
        "〔調部專題 NN〕": r"〔調部專題 ?\d{1,2}〕",
        "〔案例 現NN〕": r"〔案例 ?現\d{2}〕",
    }
    print(f"  {nm}：", "・".join(f"{k} {sum(1 for l in L if re.search(v, l))}" for k, v in forms.items()))
    nums = sorted({int(x) for l in L for x in re.findall(r"〔案(?:例)?\s*(\d{1,3})", l)})
    print(f"      行內引用之案號去重 {len(nums)} 個：{nums}")

print("\n■ 印面增頁之推算（以今兩冊之實測字/頁為率）")
import pymupdf as pm
for nm, f in (("F1", "起心動念_四分律的心智顯微鏡與唯識解剖_螢幕版.pdf"),
              ("F2", "如法推尋_僧伽憲政法權審理與修復正義_螢幕版.pdf")):
    d = pm.open(str(ROOT / "_print" / f))
    ch = sum(cjk(d[i].get_text()) for i in range(d.page_count))
    print(f"   {nm}：{d.page_count} 頁・印面漢字 {ch:,}・每頁均 {ch // d.page_count:,} 字")
    cpo = ch // d.page_count
    d.close()
    if nm == "F2":
        print(f"      → 若搬入第六章 {b-a} 行之正文（漢字另計）與附錄四，須先算其印面字數")
if c6 and c7:
    seg6 = chr(10).join(V39[c6[0]:c7[0]])
    seg4 = chr(10).join(V39[a4[0]:a5[0]])
    print(f"   第六章漢字 {cjk(seg6):,}・附錄四漢字 {cjk(seg4):,}")

print("\n■ ver39 第六章是否已非『102 張平鋪卡片』（報告假設之驗證）")
for i, l in enumerate(V39, 1):
    if "不再採用 102" in l or "五大戰場" in l or "集群矩陣" in l:
        print(f"   L{i}: {l.strip()[:96]}")
