# -*- coding: utf-8 -*-
"""第 96 輪探針四：同義堆疊與語氣疊床。"""
import io, os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "ver38四分律_起心動念心智分析框架_修正版.md")
L = io.open(MD, encoding="utf-8").read().split("\n")
skip = set()
for i, l in enumerate(L):
    if l.startswith(("# 附錄C", "# 附錄K", "# 附錄L", "# 附錄M")):
        j = i + 1
        while j < len(L) and not L[j].startswith("# "):
            j += 1
        skip.update(range(i, j))
def head_of(i):
    for j in range(i, -1, -1):
        if L[j].startswith("# "):
            return L[j][:26]
    return "卷首"

pats = collections.OrderedDict([
    ("命令三疊", r"(?:一律|必須|嚴禁|不得|不可|禁止).{0,12}(?:一律|必須|嚴禁|不得|不可|禁止).{0,12}(?:一律|必須|嚴禁|不得|不可|禁止)"),
    ("堅硬疊", r"(?:剛性|硬性|鐵|絕對|不可逆){1}.{0,8}(?:剛性|硬性|鐵|絕對|不可逆)"),
    ("全然疊", r"(?:完全|徹底|全然|百分之百|毫無|一無){1}.{0,6}(?:完全|徹底|全然|百分之百|毫無|一無)"),
    ("如實疊", r"(?:如實|客觀|全面|逐一|逐條){1}.{0,6}(?:如實|客觀|全面|逐一|逐條)"),
    ("双重括號", r"）[^，。\n]{0,10}（"),
    ("分號列三", r"；[^。\n]{0,14}；[^。\n]{0,14}；[^。\n]{0,14}；"),
    ("阿拉伯括保", r"（\d+/\d+）"),
    ("現代語", r"白名單|黑名單|背調|KPI|流程圖|機制化|項目|團隊|溝通|Feedback|反饋"),
])
tot = collections.Counter()
for i, l in enumerate(L):
    if i in skip or not l.strip():
        continue
    for k, p in pats.items():
        for m in re.findall(p, l):
            tot[k] += 1
            print("L%-6d %-8s %-24s %s" % (i + 1, k, head_of(i), m[:70]))
print("== 總計 ==", dict(tot))
