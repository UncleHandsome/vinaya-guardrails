# -*- coding: utf-8 -*-
"""第五十七輪・③甲：附錄五回查表『新編號』欄之恢復。

病（量出，非印象）：冊身附錄五之逐條回查表 154 資料列中，有 49 列首欄一律作「第七章案例九」——
重構時之誤替；舊合編本同表 173 列首欄 172 值各異，可為左證。

治：不臆推。以『卷次＋關鍵核心語句』為指紋，回舊合編本取其實編號，再經
   重構章表（合編本→重構版前）＋挪移帳（重構版前→今）兩重換算，得今靶並驗其存在；
   三关俱過者方落筆，一关不過即列帳不改。表內『開許篇～僧伽篇』之範圍宣稱改由列中實號自算。
"""
import io
import os
import re
import sys
import unicodedata
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
    if n < 100:
        a, b = divmod(n, 10)
        return CN[a] + u"十" + (CN[b] if b else u"")
    return u"百"


DROP = set(u" \t、，。：:；;（）()「」『』“”‘'\"/／-—─│·・.!?？…|*#")


def key(s):
    return u"".join(c for c in unicodedata.normalize("NFKC", s) if c not in DROP)


BOOK = os.path.join(ROOT, u"佛陀的護欄_重構版.md")
OLDB = os.path.join(ROOT, u"佛陀的護欄_四分律行為心理學與現代僧伽治理.md")
L = io.open(BOOK, encoding="utf-8-sig").read().replace("\r\n", "\n").split(u"\n")
O = io.open(OLDB, encoding="utf-8-sig").read().replace("\r\n", "\n").split(u"\n")

# 今靶存在性
case_of, sec_of = Counter(), Counter()
cur = 0
for l in L:
    m = re.match(u"^# 第([一二三四五六七八九十]+)章", l)
    if m:
        cur = cnum(m.group(1))
        continue
    if l.startswith(u"### 案例") and cur:
        case_of[cur] += 1
    elif l.startswith(u"## 第") and cur:
        sec_of[cur] += 1

R1, R2S, R2C = {}, {}, {}
for ln in io.open(os.path.join(ROOT, u"_book", u"重構章表.tsv"), encoding="utf-8-sig").read().split(u"\n"):
    f = ln.split(u"\t")
    if len(f) >= 5 and f[0].strip().lstrip(u"#").strip().isdigit():
        R1[(int(f[0]), int(f[1]))] = (int(f[3]), int(f[4]))
for ln in io.open(os.path.join(ROOT, u"_book", u"挪移帳.tsv"), encoding="utf-8").read().split(u"\n"):
    f = ln.split(u"\t")
    if f[0] == u"C":
        R2C[(int(f[1]), int(f[2]))] = (int(f[3]), int(f[4]))
    elif f[0] == u"S":
        R2S[(int(f[1]), int(f[2]))] = (int(f[3]), int(f[4]))


def to_now(a, b):
    g = R1.get((a, b))
    if not g:
        return None
    return R2C.get(g, g)


# 舊合編本指紋表
IDX = {}
for l in O:
    if l.startswith(u"| **第") and u"案例" in l:
        cs = [c.strip().strip(u"*").strip() for c in l.strip(u"|").split(u"|")]
        m = re.match(u"^第([一二三四五六七八九十]+)章案例([一二三四五六七八九十百]+)$", cs[0])
        if not m or len(cs) < 3:
            continue
        fp = key(cs[2])[:48]
        IDX.setdefault(fp, []).append((cnum(m.group(1)), cnum(m.group(2))))
print(u"舊表指紋 %d 條" % len(IDX))

RE_CELL = re.compile(u"^\\| \\*\\*第([一二三四五六七八九十]+)章案例([一二三四五六七八九十百]+)\\*\\*")
fixed, ambig, norow = [], [], []
for i, l in enumerate(L, 1):
    m = RE_CELL.match(l)
    if not m:
        continue
    a, b = cnum(m.group(1)), cnum(m.group(2))
    if 0 < b <= case_of.get(a, 0) and (a, b) != (7, 9):
        continue
    cs = [c.strip() for c in l.strip(u"|").split(u"|")]
    fp = key(cs[2])[:48] if len(cs) >= 3 else u""
    cands = IDX.get(fp, [])
    if not cands:
        pre = key(cs[2])[:30]
        cands = [v for k, vs in IDX.items() if k.startswith(pre) for v in vs]
    if not cands:
        norow.append((i, l[:70]))
        continue
    if len(set(cands)) > 1:
        ambig.append((i, cands, l[:60]))
        continue
    oa, ob = cands[0]
    tgt = to_now(oa, ob)
    if not tgt or not (0 < tgt[1] <= case_of.get(tgt[0], 0)):
        norow.append((i, u"靶不存在 %s-%s→%s" % (oa, ob, tgt)))
        continue
    new = u"| **第%s章案例%s**" % (cn(tgt[0]), cn(tgt[1]))
    fixed.append((i, l, m.group(0), new, oa, ob))
print(u"可復 %d｜指紋不明 %d｜多候 %d" % (len(fixed), len(norow), len(ambig)))
for i, l, old, new, oa, ob in fixed:
    print(u"  L%-6d %s → %s（合編本%s-%s）" % (i, old[2:20], new[2:], cn(oa), cn(ob)))
for x in norow:
    print(u"  未得 L%-6d %s" % (x[0], str(x[1])[:80]))
for x in ambig[:8]:
    print(u"  多候 L%-6d %s" % (x[0], x[1]))
if GO and fixed:
    for i, l, old, new, _, _ in fixed:
        L[i - 1] = new + l[len(old):]
    io.open(BOOK, "w", encoding="utf-8", newline="\n").write(u"\n".join(L))
    print(u"已落盤 %d 列" % len(fixed))
