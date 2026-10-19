# -*- coding: utf-8 -*-
"""第六十四輪・附錄二台帳之重算（以案例標題自列之條號為法源）。

病：附錄二『書中』欄有 32 行錯章——如十三僧殘第1條（故弄陰失精）系於『第五章案例一』，
   而第五章是四波羅夷；正靶當是第六章案例一（其題自列『第一至第四僧殘』）。
法源：各案標題自己寫明所摄之條（『第16、17條』『第一至第四僧殘』『第84、85條』），
   章之篇聚亦由章次定（五波羅夷・六僧殘與二不定・七捨墮・八單提・九提舍尼與眾學・
   十至十三尼篇）。據此反推每條之正靶，與表所載對核；不合者改表，不改案。
用法：python -X utf8 _work/r64fix.py [--go]
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, u"佛陀的護欄_重構版.md")
GO = u"--go" in sys.argv
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
    a, b = divmod(n, 10)
    return CN[a] + u"十" + (CN[b] if b else u"")


L = io.open(P, encoding="utf-8-sig").read().replace("\r\n", "\n").split(u"\n")
ch = 0
CASE = re.compile(u"^### 案例([一二三四五六七八九十百]+)：(.*)$")
# 章 → 其所摄篇聚之組名关键词
GRP = {u"四波羅夷": 5, u"十三僧殘": 6, u"二不定法": 6, u"三十捨墮": 7, u"九十單提": 8,
       u"四提舍尼": 9, u"百眾學法": 9, u"七滅諍": 9,
       u"八波羅夷": 10, u"十七僧殘": 10, u"三十捨墮（比丘尼": 11,
       u"一百七十八波逸提": 12, u"八悔過": 13, u"百眾學法（比丘尼": 13, u"七滅諍（比丘尼": 13}
NUM = re.compile(u"第([0-9]+)(?:、([0-9]+))*(?:、([0-9]+))?(?:、([0-9]+))?")
HANR = re.compile(u"第([一二三四五六七八九十]+)至第?([一二三四五六七八九十]+)(?:僧殘|波羅夷|捨墮|單提)")
HAN1 = re.compile(u"第([一二三四五六七八九十]+)(僧殘|波羅夷|捨墮)")
HANL = re.compile(u"第([一二三四五六七八九十]+)、第?([一二三四五六七八九十]+)(?:僧殘|波羅夷|捨墮|單提)?")

plan = {}                                     # (組名, 條序) → (章, 案序)
cur = 0
for l in L:
    m = re.match(u"^# 第([一二三四五六七八九十]+)章", l)
    if m:
        cur = cnum(m.group(1))
        continue
    m = CASE.match(l)
    if not m or not cur:
        continue
    k = cnum(m.group(1))
    t = m.group(2)
    got = set()
    for x in re.findall(u"第([0-9]+)條", t):
        got.add(int(x))
    for mm in re.finditer(u"第([0-9]+)、([0-9]+)(?:、([0-9]+))?(?:、([0-9]+))?條", t):
        for g in mm.groups():
            if g:
                got.add(int(g))
    for x in re.findall(u"第([0-9]+)～([0-9]+)條", t):
        got.update(range(int(x[0]), int(x[1]) + 1))
    for mm in HANR.finditer(t):
        a, b = cnum(mm.group(1)), cnum(mm.group(2))
        if a and b:
            got.update(range(a, b + 1))
    for mm in HAN1.finditer(t):
        v = cnum(mm.group(1))
        if v:
            got.add(v)
    for mm in HANL.finditer(t):
        for g in mm.groups():
            v = cnum(g) if g else 0
            if v:
                got.add(v)
    if not got:
        continue
    if cur == 6:
        g6 = u"二不定法" if u"不定" in t else u"十三僧殘"
        for n in got:
            plan[(g6, n)] = (6, k)
    elif cur == 5:
        for n in got:
            plan[(u"四波羅夷", n)] = (5, k)
    elif cur == 7:
        for n in got:
            plan[(u"三十捨墮", n)] = (7, k)
    elif cur == 8:
        for n in got:
            plan[(u"九十單提", n)] = (8, k)
    elif cur == 9:
        for n in got:
            plan[(u"四提舍尼", n)] = (9, k)
    elif cur in (10, 11, 12, 13):
        for n in got:
            for gname in [u"八波羅夷", u"十七僧殘", u"三十捨墮（比丘尼", u"一百七十八波逸提"]:
                pass

# 組名匹配：取組頭之關鍵片段
def gkey(head):
    for g in GRP:
        if g in head:
            return g
    return None


grp = None
rows = re.compile(u"^(\d+)\.\s*[「『](.{0,80})")
fix = []
skip = 0
for i, l in enumerate(L, 1):
    if l.startswith(u"### 甲、") or l.startswith(u"### 乙、"):
        grp = gkey(l)
        continue
    if not grp:
        continue
    m = rows.match(l)
    if not m or grp is None:
        continue
    n = int(m.group(1))
    t = l
    mm = re.search(u"｜書中[：:]\\s*第([一二三四五六七八九十]+)章案例([一二三四五六七八九十百]+)", t)
    if not mm:
        continue
    want = plan.get((grp, n))
    if not want:
        skip += 1
        continue
    now = (cnum(mm.group(1)), cnum(mm.group(2)))
    if now == want:
        continue
    fix.append((i, mm.group(0), u"｜書中：第%s章案例%s" % (cn(want[0]), cn(want[1])), grp, n))



print(u"可推之條 %d｜表行與之不合 %d｜無從推而留 %d" % (len(plan), len(fix), skip))
seen = {}
for i, o, nw, g, n in fix:
    print(u"  L%-6d %s｜組%s 條%d → %s" % (i, o[1:22], g[:6], n, nw[1:]))
if GO:
    for i, o, nw, g, n in fix:
        L[i - 1] = L[i - 1].replace(o, nw, 1)
    io.open(P, "w", encoding="utf-8", newline="\n").write(u"\n".join(L))
    print(u"已落盤 %d 行" % len(fix))
