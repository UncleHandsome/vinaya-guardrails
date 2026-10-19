# -*- coding: utf-8 -*-
"""第五十七輪・③：死鏈清冊（量產物，不量印象）。

凡指針三式一律核對實有之靶：
  第A章案例B ／ 第A章第B節（含第K款） ／ 裸第A章・第A篇・附錄A
案例級死鏈另試一法：舊指針之（A,B）作「合編本座標」解，經 重構章表 → 挪移帳 兩重換算，
得今靶者記其法；兩重皆不得者列待裁，附上下文以备親裁。
"""
import io
import os
import re
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, u"佛陀的護欄_重構版.md")
CN = u"零一二三四五六七八九十百"


def cnum(s):
    s = s.strip()
    if u"百" in s:
        a, _, b = s.partition(u"百")
        return (CN.index(a) if a else 1) * 100 + (cnum(b) if b else 0)
    if u"十" in s:
        a, _, b = s.partition(u"十")
        return (CN.index(a) if a else 1) * 10 + (CN.index(b) if b else 0)
    return CN.index(s) if s and s in CN else 0


def cn(n):
    if n < 10:
        return CN[n]
    if n < 20:
        return u"十" + (CN[n % 10] if n % 10 else u"")
    if n < 100:
        a, b = divmod(n, 10)
        return CN[a] + u"十" + (CN[b] if b else u"")
    return u"百"


L = io.open(SRC, encoding="utf-8-sig").read().replace("\r\n", "\n").split(u"\n")
case_of, sec_of, head_of = defaultdict(int), defaultdict(int), {}
cur = 0
for i, l in enumerate(L, 1):
    m = re.match(u"^# 第([一二三四五六七八九十]+)章", l)
    if m:
        cur = cnum(m.group(1))
        head_of[cur] = i
        continue
    if l.startswith(u"### 案例") and cur:
        case_of[cur] += 1
    elif l.startswith(u"## 第") and cur:
        sec_of[cur] += 1
NP = len([1 for l in L if l.startswith(u"## 附錄")])
print(u"章 %d｜節總 %d｜案總 %d｜附錄 %d" % (len(head_of), sum(sec_of.values()),
                                            sum(case_of.values()), NP))

M1 = re.compile(u"第([一二三四五六七八九十]+)章案例([一二三四五六七八九十百]+)")
M2 = re.compile(u"第([一二三四五六七八九十]+)章第([一二三四五六七八九十]+)節")
M3 = re.compile(u"第([一二三四五六七八九十]+)篇")
dead1, dead2, dead3, dead4 = [], [], [], []
for i, l in enumerate(L, 1):
    if l.startswith(u"# "):
        continue
    for m in M1.finditer(l):
        a, b = cnum(m.group(1)), cnum(m.group(2))
        if not (0 < b <= case_of.get(a, -1)):
            dead1.append((i, a, b, m.group(0), l))
    for m in M2.finditer(l):
        a, b = cnum(m.group(1)), cnum(m.group(2))
        if not (0 < b <= sec_of.get(a, -1)):
            dead2.append((i, a, b, m.group(0), l))
    for m in re.finditer(u"第([一二三四五])篇", l):
        if cnum(m.group(1)) > 5:
            dead3.append((i, m.group(0)))
    for m in re.finditer(u"附錄([一二三四五六七八九])", l):
        if cnum(m.group(1)) > NP:
            dead4.append((i, m.group(0)))
print(u"\n死鏈：案例 %d｜節 %d｜篇 %d｜附錄 %d" % (len(dead1), len(dead2), len(dead3), len(dead4)))

# 兩重換算：合編本(A,B) → 重構版前 → 今
R1 = {}
for ln in io.open(os.path.join(ROOT, u"_book", u"重構章表.tsv"), encoding="utf-8-sig").read().split(u"\n"):
    f = ln.split(u"\t")
    if len(f) >= 5 and f[0].strip().lstrip(u"#").strip().isdigit():
        R1[(int(f[0]), int(f[1]))] = (int(f[3]), int(f[4]), f[2].strip()[:24])
R2 = {}
for ln in io.open(os.path.join(ROOT, u"_book", u"挪移帳.tsv"), encoding="utf-8").read().split(u"\n"):
    f = ln.split(u"\t")
    if f and f[0] == u"C":
        R2[(int(f[1]), int(f[2]))] = (int(f[3]), int(f[4]))
hit, miss = [], []
for (i, a, b, s, line) in dead1:
    g = R1.get((a, b))
    tgt = None
    way = u""
    if g:
        k2 = R2.get(g[:2])
        if k2:
            tgt, way = k2, u"合編本座標"
        elif g[:2] in case_of and 0 < g[1] <= case_of[g[0]]:
            tgt, way = g[:2], u"重構版前座標"
    if tgt and 0 < tgt[1] <= case_of.get(tgt[0], -1):
        hit.append((i, s, u"%s→第%s章案例%s" % (way, cn(tgt[0]), cn(tgt[1])), g[2] if g else u""))
    else:
        miss.append((i, s, line.strip()[:150]))
print(u"\n案例死鏈兩重換算：可定 %d／%d" % (len(hit), len(dead1)))
for x in hit[:60]:
    print(u"  L%-6d %-12s %s｜舊題 %s" % (x[0], x[1], x[2], x[3]))
print(u"\n須親裁 %d：" % len(miss))
for i, s, line in miss:
    print(u"  L%-6d %s｜%s" % (i, s, line))
print(u"\n節級死鏈 %d：" % len(dead2))
for i, a, b, s, line in dead2:
    print(u"  L%-6d %s（第%s章實 %d 節）｜%s" % (i, s, cn(a), sec_of.get(a, 0), line.strip()[:130]))
if dead3:
    print(u"\n篇：%s" % dead3)
if dead4:
    print(u"\n附錄：%s" % dead4)
