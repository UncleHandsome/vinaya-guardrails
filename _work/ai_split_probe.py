# -*- coding: utf-8 -*-
"""第二探：案號錨形・五層模型之實形・閘門與邊界之落點（只讀）。"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
F1 = (ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt").read_bytes().decode("utf-8").split("\r\n")
F2 = (ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt").read_bytes().decode("utf-8").split("\r\n")


def probe(nm, lines, rx, cap=6):
    hits = [(i + 1, l.strip()) for i, l in enumerate(lines) if re.search(rx, l)]
    print(f"  [{nm}] {rx}  → {len(hits)} 行")
    for i, l in hits[:cap]:
        print(f"        L{i}: {l[:74]}")
    return hits


print("■ 案號錨形（F1）")
for rx in [r"〔案\s*\d", r"\[案\s*\d", r"案卷 ?\d{2}", r"〔案例 ?\d", r"〔案\d{2}〕", r"〔案 \d{2}〕"]:
    probe("F1", F1, rx, 3)
nums = sorted({int(x) for x in re.findall(r"〔案[卷例]?\s*(\d{1,3})", "\n".join(F1))})
print("  F1 去重案號：", nums, f"共 {len(nums)} 個")
g = {1: [1, 2, 5, 16, 27, 28, 30], 8: [7, 19, 37, 38, 49, 55], 9: [21, 42, 96], 10: [10, 12, 13]}
want = sorted({n for v in g.values() for n in v})
print("  指南派 F1 案：", want, f"共 {len(want)}")
print("  書中有而指南未派：", sorted(set(nums) - set(want)), "・指南派而書中無：", sorted(set(want) - set(nums)))

print("\n■ 案號錨形（F2 制度案卷）")
probe("F2", F2, r"〔(?:制度)?案卷?\s*\d", 8)
nums2 = sorted({int(x) for x in re.findall(r"〔(?:制度)?案卷?\s*(\d{1,3})", "\n".join(F2))})
print("  F2 去重案號：", nums2)
print("  指南派 F2 制度案：", sorted([23, 77, 81, 76, 83, 84, 98, 91, 97]), "・缺席：",
      sorted({23, 77, 81, 76, 83, 84, 98, 91, 97} - set(nums2)))

print("\n■ 五層模型之實形")
for nm, lines, rxs in (
    ("F1", F1, [r"現象層", r"解剖層", r"法相層", r"修復層", r"照鏡層", r"五層顯微", r"五層解剖"]),
    ("F2", F2, [r"程序危機", r"法益爭點", r"如法推尋與證據", r"判決主文", r"現代治理會通", r"五層法理", r"法理判例案卷"]),
):
    print(f"  {nm}：", {rx: sum(1 for l in lines if re.search(rx, l)) for rx in rxs})

print("\n■ 六重心智閘門・四大神聖邊界之落點")
probe("F1", F1, r"閘門", 4)
probe("F2", F2, r"閘門", 8)
probe("F1", F1, r"四大神聖邊界|神聖邊界", 6)
probe("F2", F2, r"神聖邊界|四大.*邊界", 4)

print("\n■ 案 91・98・97 之名今在何冊")
for k in ["高勝", "泉水", "金布"]:
    for nm, lines in (("F1", F1), ("F2", F2)):
        hits = [(i + 1, l.strip()) for i, l in enumerate(lines) if k in l]
        print(f"  {k} {nm}: {len(hits)} 行", *(f" | L{i}: {l[:52]}" for i, l in hits[:2]))

print("\n■ F1 第二章第三節（指南派 F2 之管轄素材）之跨度")
idx = [i for i, l in enumerate(F1) if re.match(r"^### 第[一二三四五六七八九十]節", l.strip())]
for i in idx[:8]:
    nxt = next((j for j in idx if j > i), len(F1))
    print(f"   L{i+1}: {F1[i].strip()[:46]}  → 至 L{nxt}（{nxt - i} 行）")
