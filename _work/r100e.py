# -*- coding: utf-8 -*-
"""第 100 輪探針五：節號與款號之断號、重號、跳號檢。"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "ver38四分律_起心動念心智分析框架_修正版.md")
L = io.open(MD, encoding="utf-8").read().split("\n")
CN = {c: i for i, c in enumerate("零一二三四五六七八九", 0)}


def c2n(s):
    s = s.strip()
    m = re.fullmatch(r"([一二三四五六七八九])?十([一二三四五六七八九])?", s)
    if m:
        return CN.get(m.group(1), 1) * 10 + CN.get(m.group(2), 0)
    return CN.get(s)


def nums(t, pats):
    for p in pats:
        m = re.match(p, t)
        if m:
            if m.lastindex == 2:
                return list(range(c2n(m.group(1)), c2n(m.group(2)) + 1))
            return [c2n(m.group(1))]
    return []


SEC = [r"^第([一二三四五六七八九十]+)節", r"^閘門([一二三四五六七八九十]+)", r"^【?第([一二三四五六七八九十]+)篇"]
KUA = [r"^([一二三四五六七八九十]+)至([一二三四五六七八九十]+)[、，]", r"^([一二三四五六七八九十]+)、",
       r"^(\d+)[\.、]", r"^（([一二三四五六七八九十]+)）"]
blocks = [(i, l) for i, l in enumerate(L) if re.match(r"^# (第[一二三四五六七八九]章|附錄[A-M]|結語|終卷)", l)]
blocks.append((len(L), ""))
for b in range(len(blocks) - 1):
    a, z = blocks[b][0], blocks[b + 1][0]
    title = blocks[b][1].lstrip("# ")[:14]
    # 節序
    seqs = []
    for i in range(a + 1, z):
        if L[i].startswith("### "):
            seqs += [(i + 1, n) for n in nums(L[i][4:].strip(), SEC)]
    raw = [n for _, n in seqs]
    msg = []
    dup = sorted({n for n in raw if raw.count(n) > 1})
    if dup:
        msg.append("重號%s" % dup)
    gap = [n for n in range(1, max(raw) + 1) if raw and n not in raw] if raw else []
    if gap:
        msg.append("斷號%s（僅數號節）" % gap)
    # 款序（逐節）
    cur, ks = None, []
    kmsg = []
    for i in range(a + 1, z):
        if L[i].startswith("### "):
            if cur is not None:
                kmsg.append((cur, ks))
            cur, ks = i + 1, []
        elif L[i].startswith("#### ") and cur is not None:
            ks += nums(L[i][5:].strip(), KUA)
    if cur is not None:
        kmsg.append((cur, ks))
    for ln, ks in kmsg:
        r = [n for n in ks if n]
        if not r:
            continue
        d = sorted({n for n in r if r.count(n) > 1})
        g = [n for n in range(1, max(r) + 1) if n not in r]
        if d or g:
            bad = " ".join(L[ln - 1].strip()[:20] for _ in [0])
            kmsg2 = "節L%d（%s）款列%s%s" % (ln, L[ln - 1].lstrip("# ")[:14], r,
                                            "　重%s" % d if d else "")
            if g:
                kmsg2 += "　缺%s" % g
            print("  %-12s %s" % (title, kmsg2))
    if msg:
        print("%-14s 節序：%s ｜全序 %s" % (title, "、".join(msg), raw))
