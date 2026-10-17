# -*- coding: utf-8 -*-
"""第 100 輪探針四：問次、子目（X-N）、案例編號之指針生死。"""
import io, os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "ver38四分律_起心動念心智分析框架_修正版.md")
L = io.open(MD, encoding="utf-8").read().split("\n")
# 一、問次：書中問[NN] 之定義處與引用處
defn = collections.defaultdict(list)
for i, l in enumerate(L):
    for m in re.finditer(r"問\[(\d{1,2})\]\s*(?:（[^）]{0,30}）)?\s*\*\*|^\s*\*\s+\*\*問\[(\d{1,2})\]", l):
        g = m.group(1) or m.group(2)
        defn[int(g)].append(i + 1)
used = collections.Counter()
for l in L:
    for m in re.finditer(r"問\[(\d{1,2})\]", l):
        used[int(m.group(1))] += 1
print("問次：定義見 %s" % sorted(defn))
print("      引用 %s" % dict(sorted(used.items())))
print("      引用而全書無『問[N]　標題』者：%s" % [n for n in used if n not in defn])
# 二、附錄子目 X-N：以附錄內之 heading／粗體列為實有
apps = {}
cur = None
for i, l in enumerate(L):
    m = re.match(r"^# 附錄([A-M])", l)
    if m:
        cur = m.group(1); apps[cur] = []
    elif l.startswith("# ") and cur:
        cur = None
    elif cur and re.match(r"^#{2,5} ", l):
        apps[cur].append((i + 1, l.lstrip("# ").strip()))
have = collections.defaultdict(set)
for a, hs in apps.items():
    for ln, t in hs:
        for m in re.finditer(r"\b([A-M])\s*[-–]\s*(\d{1,2})\b", t):
            have[a].add("%s-%s" % (m.group(1), m.group(2)))
        for m in re.finditer(r"^([A-M])[-–]?(\d{1,2})[　\s]", t):
            have[a].add("%s-%s" % (m.group(1), m.group(2)))
    for m2 in re.finditer(r"### ([A-M])[-–](\d{1,2})", "\n".join(t for _, t in hs)):
        have[None].add("%s-%s" % (m2.group(1), m2.group(2)))
ALL = have[None] | {k for a in have for k in have[a]}
ref = collections.Counter()
bad = []
for i, l in enumerate(L):
    for m in re.finditer(r"附錄\s*([A-M])[-–](\d{1,2})", l):
        key = "%s-%s" % (m.group(1), m.group(2))
        ref[key] += 1
        if key not in ALL:
            bad.append((i + 1, key, l.strip()[:50]))
print("附錄子目：實有 %s" % sorted(ALL))
print("          被引 %s" % dict(sorted(ref.items())))
print("          引而不存在：%s" % bad)
# 三、案例編號範圍
rng = {"遮": 45, "開": 25, "僧": 30, "遺": 99, "補遺": 99}
oor = collections.Counter()
for i, l in enumerate(L):
    for m in re.finditer(r"〔(遮|開|僧|遺|補遺)(\d{1,3})〕", l):
        k, n = m.group(1), int(m.group(2))
        if k in ("遮", "開", "僧") and n > rng[k]:
            oor["%s%d" % (k, n)] += 1
            if sum(oor.values()) < 12:
                print("  越界 L%d %s" % (i + 1, m.group(0)))
print("案例編號越界：%s" % dict(oor))
