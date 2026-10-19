# -*- coding: utf-8 -*-
"""第五十九輪・款級死指之定讞與債帳。

證有三層，取最上者而落筆；不足者入表候裁，不以『可能』代『已證』：
  甲【定讞】指針自帶〔〕（…）之款題標籤，且今冊某節實有该款題・其序相合 → 逕改座標。
  乙【定讞】指針無標籤，然其『舊合編本節題』於今冊唯一落點，且本句之名相見於該節實文 → 改至節級。
  丙【候裁】二者俱不足者，列 `_book/款級待裁.tsv`：原指針・本句主題・舊節題・今冊候選・
       候選節內有無本句名相・擬議——作者一望可裁，不再從頭查。
用法：python -X utf8 _work/r59k.py [--go]
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
LED = os.path.join(ROOT, u"_book", u"款級待裁.txt")
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
NT = defaultdict(list)
for c, v in NS.items():
    NT[key(v[2])].append(c)
PAT = re.compile(u"第([一二三四五六七八九十]+)章第([一二三四五六七八九十]+)節第([一二三四五六七八九十]+)款")
LBL = re.compile(u"[〔（]([^〕）]{4,26})[〕）]")


def topics(line):
    out = []
    for g in re.findall(u"『([^』]{2,14})』|「([^」]{2,14})』|\\*\\*([^*]{2,14})\\*\\*", line):
        out += [x for x in g if x and len(key(x)) >= 3]
    return out


fix, pend = [], []
for i, l in enumerate(NL, 1):
    if l.startswith(u"# "):
        continue
    for m in PAT.finditer(l):
        a, b, k = cnum(m.group(1)), cnum(m.group(2)), cnum(m.group(3))
        cur = NS.get((a, b))
        if cur and k in cur[3]:
            continue
        new, way = None, u""
        lab = LBL.search(l, m.end(), min(len(l), m.end() + 30)) or \
            LBL.search(l[max(0, m.start() - 46):m.start()])
        if lab:
            lk = key(lab.group(1))
            c1 = [(c, s, n) for (c, s), v in NS.items() for n, t in v[3].items()
                  if lk and (lk in key(t) or key(t) in lk)]
            c2 = [x for x in c1 if x[2] == k]
            if len(set(x[:2] for x in c2)) == 1:
                new = u"第%s章第%s節第%s款" % (cn(c2[0][0]), cn(c2[0][1]), cn(k))
                way = u"甲・標籤『%s』對款題且序合" % lab.group(1)[:12]
            elif len(set(c1)) == 1:
                new = u"第%s章第%s節第%s款" % (cn(c1[0][0]), cn(c1[0][1]), cn(c1[0][2]))
                way = u"甲・標籤對款題（序改 %s）" % cn(c1[0][2])
        if new is None:
            o = OS.get((a, b))
            tgt = list(dict.fromkeys(NT.get(key(o[2]), []))) if o else []
            tp = topics(l)
            if len(tgt) == 1:
                hit = [t for t in tp if key(t) in NS[tgt[0]][4]]
                if hit:
                    new = u"第%s章第%s節" % (cn(tgt[0][0]), cn(tgt[0][1]))
                    way = u"乙・舊節題對號，靶含『%s』" % hit[0][:10]
        if new:
            fix.append((i, m.group(0), new, way))
        else:
            o = OS.get((a, b))
            tgt = list(dict.fromkeys(NT.get(key(o[2]), []))) if o else []
            cand = u"／".join(u"第%s章第%s節" % (cn(c), cn(s)) for c, s in tgt) or u"（無候選）"
            has = u"／".join(u"%s" % (u"有" if any(key(t) in NS[x][4] for t in topics(l)) else u"無")
                             for x in tgt) or u"-"
            pend.append((i, m.group(0), u"「%s」" % (o[2][:18] if o else u"舊冊無此節"),
                         cand, has, u"；".join(topics(l)[:3])[:34]))
print(u"款級死指 %d｜定讞 %d｜候裁 %d" % (len(fix) + len(pend), len(fix), len(pend)))
for i, o, n, w in fix:
    print(u"  改 L%-6d %-20s → %-20s %s" % (i, o[:20], n[:20], w[:34]))

if GO:
    t = u"\n".join(NL)
    for i, o, n, w in fix:
        t = t.replace(o, n, 1)
    io.open(NEW, "w", encoding="utf-8", newline="\n").write(t)
    io.open(TSV, "w", encoding="utf-8", newline="\n").write(
        u"\t".join([u"行", u"原指針", u"舊冊該節之題", u"今冊候選靶", u"靶內含本句名相", u"本句主題"]) + u"\n" +
        u"\n".join(u"\t".join(str(x) for x in r) for r in pend) + u"\n")
    io.open(LED, "w", encoding="utf-8", newline="\n").write(
        u"# 款級死指之債帳（第五十九輪重立）\n\n"
        u"定讞 %d 條已落筆（甲＝指針自帶〔〕款題標籤且今冊實有其款其序；乙＝舊合編本節題於今冊唯一落點，"
        u"且本句之名相見於該節實文）。\n"
        u"候裁 %d 條列於 `款級待裁.tsv`——每行附：舊冊該節之題・今冊候選靶・靶內有無本句名相・本句主題，"
        u"逐行可一望而裁。\n" % (len(fix), len(pend)) +
        u"".join(u"L%-6d %s｜%s\n" % (i, o, w) for i, o, n, w in fix))
    print(u"已落盤：定讞 %d・債帳 %s（%d 行）" % (len(fix), os.path.basename(TSV), len(pend)))
