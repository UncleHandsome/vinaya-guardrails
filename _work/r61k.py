# -*- coding: utf-8 -*-
"""第六十一輪・款級債之正解：回錨舊冊讀原指針（非以今座標倒查）。

前試之誤：拿今冊之『第十章第一節第二款』去舊冊查（章,節）=（10,1）——
   而今冊之第十章是尼戒總論，舊冊之第十章是單提，同數不同物，故盡皆落空。
今法（與第五十六輪救回 277 條案例指針同一法源）：
   ① 取今冊死指之上下文（前後各 22 歸一字），於舊冊實文中找同一句；
   ② 讀該處舊冊之款級指針——這才是作者落筆時的實數；
   ③ 舊（章,節）→節題→今冊唯一落點；款序則以舊款題對今款題（或今實文含舊款題者）；
   ④ 三关俱過始改；缺關者保留，並把『舊冊原指針＋舊節題＋今候選』寫入債帳，
      使親裁者一眼見全案，不必再從頭查。
用法：python -X utf8 _work/r61k.py [--go]
"""
import io
import os
import re
import sys
import unicodedata
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEW = os.path.join(ROOT, u"佛陀的護欄_重構版.md")
OLD = os.path.join(ROOT, u"佛陀的護欄_四分律行為心理學與現代僧伽治理.md")
TSV = os.path.join(ROOT, u"_book", u"款級待裁.tsv")
GO = u"--go" in sys.argv
CN = u"零一二三四五六七八九十百"
DROP = set(u" \t、，。：:；;（）()「」『』“”‘'\"/／-—─│·・.!?？…*#|【】《》〇")


def key(s):
    return u"".join(c for c in unicodedata.normalize("NFKC", s) if c not in DROP)


def cnum(s):
    s = s.strip()
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


def model(path):
    L = io.open(path, encoding="utf-8-sig").read().replace("\r\n", "\n").split(u"\n")
    ch = sec = 0
    S, order = {}, []
    for i, l in enumerate(L, 1):
        m = re.match(u"^# 第([一二三四五六七八九十]+)章", l)
        if m:
            ch, sec = cnum(m.group(1)), 0
            continue
        m = re.match(u"^## 第([一二三四五六七八九十]+)節　(.*)$", l)
        if m:
            if sec:
                S[order[-1]][1] = i - 1
            sec = cnum(m.group(1))
            order.append((ch, sec))
            S[(ch, sec)] = [i, len(L), m.group(2).strip(), {}, u""]
            continue
        if (l.startswith(u"## ") or l.startswith(u"# ")) and sec:
            S[order[-1]][1] = i - 1
            sec = 0
    for k in S:
        S[k][1] = min(S[k][1], len(L))
        body = L[S[k][0] - 1:S[k][1]]
        S[k][4] = key(u"".join(body))
        for x in body:
            m = re.match(u"^### ([一二三四五六七八九十]+)、(.*)$", x)
            if m:
                S[k][3][cnum(m.group(1))] = m.group(2).strip()
                continue
            m = re.match(u"^### ([0-9]+)\. (.*)$", x)
            if m:
                S[k][3][int(m.group(1))] = m.group(2).strip()
    return L, S


NL, NS = model(NEW)
OL, OS = model(OLD)
okey = key(u"\n".join(OL))
NT = defaultdict(list)
for c, v in NS.items():
    NT[key(v[2])].append(c)
PAT = re.compile(u"第([一二三四五六七八九十]+)章第([一二三四五六七八九十]+)節第([一二三四五六七八九十]+)款")
OPAT = re.compile(u"第([一二三四五六七八九十]+)章第([一二三四五六七八九十]+)節第([一二三四五六七八九十]+)款")


def dead(a, b, k):
    cur = NS.get((a, b))
    if not cur:
        return True
    return k not in cur[3]


def old_anchor(line, m):
    pre = key(line[max(0, m.start() - 46):m.start()])[-22:]
    post = key(line[m.end():m.end() + 46])[:22]
    if len(pre) < 8 and len(post) < 8:
        return []
    pos, found = -1, []
    while True:
        pos = okey.find(pre, pos + 1)
        if pos < 0 or len(found) > 6:
            break
        seg = okey[pos + len(pre):pos + len(pre) + len(post) + 34]
        for mm in OPAT.finditer(seg):
            found.append((cnum(mm.group(1)), cnum(mm.group(2)), cnum(mm.group(3))))
    return list(dict.fromkeys(found))


done, rest = [], []
for i, l in enumerate(NL, 1):
    if l.startswith(u"# "):
        continue
    for m in PAT.finditer(l):
        a, b, k = cnum(m.group(1)), cnum(m.group(2)), cnum(m.group(3))
        if not dead(a, b, k):
            continue
        cands = old_anchor(l, m)
        got = []
        for (oa, ob, ok) in cands:
            o = OS.get((oa, ob))
            if not o:
                continue
            tgt = list(dict.fromkeys(NT.get(key(o[2]), [])))
            if len(tgt) != 1:
                continue
            c2, s2 = tgt[0]
            otitle = o[3].get(ok, u"")
            nk = None
            for n, t in NS[(c2, s2)][3].items():
                if otitle and key(t)[:12] == key(otitle)[:12]:
                    nk = n
            if nk is None and otitle and key(otitle)[:10] in NS[(c2, s2)][4]:
                nk = None                                   # 款題在節內而無明序 → 節級
            got.append((c2, s2, nk, oa, ob, ok, otitle[:16]))
        uniq = list(dict.fromkeys([(x[0], x[1], x[2]) for x in got]))
        if len(got) == 1 or (len(uniq) == 1 and got):
            c2, s2, nk, oa, ob, ok, otitle = got[0]
            new = u"第%s章第%s節" % (cn(c2), cn(s2)) + (u"第%s款" % cn(nk) if nk else u"")
            done.append((i, m.group(0), new, u"舊%s-%s-%s｜舊款題%s" % (cn(oa), cn(ob), cn(ok), otitle or u"—")))
        else:
            rest.append((i, m.group(0), u"／".join(u"舊%s-%s-%s" % (cn(x[3]), cn(x[4]), cn(x[5])) for x in got) or u"無錨",
                         u"／".join(u"第%s章第%s節%s" % (cn(x[0]), cn(x[1]), (u"第%s款" % cn(x[2])) if x[2] else u"") for x in got) or u"—"))
print(u"款級債：回錨可定 %d｜仍候裁 %d" % (len(done), len(rest)))
for i, o, n, w in done:
    print(u"  改 L%-6d %-22s → %-22s %s" % (i, o[:22], n[:22], w[:44]))
for x in rest[:14]:
    print(u"  候 L%-6d %-22s｜%s｜%s" % (x[0], x[1][:22], x[2][:26], x[3][:30]))
if GO:
    t = u"\n".join(NL)
    for i, o, n, w in done:
        t = t.replace(o, n, 1)
    io.open(NEW, "w", encoding="utf-8", newline="\n").write(t)
    io.open(TSV, "w", encoding="utf-8", newline="\n").write(
        u"\t".join([u"行", u"原指針", u"舊冊該處之實指", u"今冊落點", u"款題"]) + u"\n" +
        u"\n".join(u"%d\t%s\t%s\t%s\t%s" % (x[0], x[1], x[2], x[3], u"") for x in rest) + u"\n")
    print(u"已落盤；債帳重生 %s（%d 行）" % (os.path.basename(TSV), len(rest)))
