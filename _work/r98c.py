# -*- coding: utf-8 -*-
"""第 96 輪探針三：考據補丁與工程自述是否洩入印面。"""
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
            return L[j][:30]
    return "卷首"
pats = collections.OrderedDict([
    ("舊版/舊載", r"舊版|舊載|舊稿|本版"),
    ("輪次自述", r"第[一二三四五六七八九十百零〇\d]+輪"),
    ("校勘用語", r"校勘|勘誤|三校|覆核|校讎|校改|訂補"),
    ("工程用語", r"管線|批次|腳本|自算器|驗收器|探針|迴歸|部署|渲染|解析"),
    ("版本號", r"v3[0-9]|ver3[0-9]|第三[十]?[一二三四五六七八九]?版"),
    ("工具名", r"_tk|build38|verify38|pandoc|Typst|typst"),
])
tot = collections.Counter()
for i, l in enumerate(L):
    if i in skip:
        continue
    for k, p in pats.items():
        m = re.findall(p, l)
        if m:
            tot[k] += len(m)
            print("L%-6d %-8s %-22s %s" % (i + 1, k, head_of(i), " ".join(m[:4])))
print("== 總計 ==", dict(tot))
