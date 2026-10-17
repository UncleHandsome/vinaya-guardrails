# -*- coding: utf-8 -*-
"""第 96 輪探針七：官樣冗辭與「的／性／化」鏈。"""
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
            return L[j][:22]
    return "卷首"
pats = collections.OrderedDict([
    ("進行V", r"進行[一-鿿]{2,4}"),
    ("通過…來", r"通過[^，。\n]{2,18}來"),
    ("針對", r"針對"),
    ("關於", r"關於"),
    ("之所以", r"之所以"),
    ("以上所述", r"如上所述|綜上|由上可知|上文所稱|前述"),
    ("須知腔", r"此處須知|須知|當知|須辨|應了解|需要指出|值得強調|特別提醒"),
    ("的鏈", r"[^，。\n]{3,12}的[^，。\n]{3,12}的[^，。\n]{3,12}的"),
    ("性鏈", r"[一-鿿]{2,4}性[一-鿿]{2,4}性"),
    ("三重括號", r"（[^（）\n]{2,20}）[^（）\n]{0,10}（[^（）\n]{2,20}）[^（）\n]{0,10}（"),
])
tot = collections.Counter(); ex = collections.defaultdict(list)
for i, l in enumerate(L):
    if i in skip or not l.strip() or l.startswith("|"):
        continue
    for k, p in pats.items():
        for m in re.findall(p, l):
            tot[k] += 1
            if len(ex[k]) < 6:
                ex[k].append("L%d %s: %s" % (i + 1, head_of(i), m[:40]))
for k in pats:
    print("== %-8s %d" % (k, tot[k]))
    for e in ex[k]:
        print("   " + e)
