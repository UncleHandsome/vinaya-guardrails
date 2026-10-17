# -*- coding: utf-8 -*-
"""第 89 輪丙批：印面之長段與成語式重覆片語（≥14 字、見於三行以上）。

引號內之逐字律文（本律語料）不入列——那是引用，不是回音。
"""
import io, os, re, sys
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk

LINES = _tk.DOC.split("\n")
BOTTOM = _tk.bottom_lines()

prose = []
for i, l in enumerate(LINES):
    if i in BOTTOM:
        continue
    if l.startswith("|") or l.startswith("> ---") or not l.strip():
        continue
    if re.search(r"[│┌└├┤━═▼▲►◄]", l):        # 框圖之行不入列
        continue
    prose.append((i + 1, l))

# 一、長段
out = [u"##### 一、印面最長之散文段（去記號後字數）#####"]
longs = sorted(((len(re.sub(r"[#*`>\-\s|]", "", l)), n, l) for n, l in prose), reverse=True)
for c, n, l in longs[:14]:
    out.append(u"  L%-6d %4d 字｜%s" % (n, c, l[:60]))

# 二、片語回音：以 14 字滑窗統計（只算散文行，且先剔除「」與『』之內容）
out.append(u"\n##### 二、剔除引文後之 14 字滑窗重覆 #####")
strip_q = lambda s: re.sub(u"[「『][^」』]*[」』]", u"□", s)
cnt = defaultdict(set)
for n, l in prose:
    s = re.sub(r"(?s)<[^>]+>", "", strip_q(l))
    s = re.sub(r"[#*>`|\-\s]", "", s)
    for k in range(0, max(0, len(s) - 13)):
        cnt[s[k:k + 14]].add(n)
# 合併相疊之窗（取每組最長代表）
hot = {w: ls for w, ls in cnt.items() if len(ls) >= 3}
groups = []
for w in sorted(hot, key=lambda x: (-len(hot[x]), x)):
    hit = next((g for g in groups if any(w[j:j + 6] in g[0] for j in range(0, max(1, len(w) - 5)))), None)
    if hit:
        if len(w) > len(hit[0]) and set(hot[w]) != set(hit[1]):
            hit[0], hit[1] = w, sorted(hot[w])
    else:
        groups.append([w, sorted(hot[w])])
groups = [g for g in groups if len(g[1]) >= 3]
groups.sort(key=lambda g: (-len(g[1]), -len(g[0])))
for w, ls in groups[:30]:
    out.append(u"  %2d 行｜%s｜L%s" % (len(ls), w, ",".join(str(x) for x in ls[:8])))
out.append(u"  —— 共 %d 組 ——" % len(groups))

io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "phrase89.txt"),
        "w", encoding="utf-8").write(u"\n".join(out) + u"\n")
sys.stdout.write(u"longs %d groups %d\n" % (len(longs), len(groups)))
