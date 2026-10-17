# -*- coding: utf-8 -*-
"""第 100 輪探針三：指針家族生死檢（修訂版——節號取『第N節／閘門N／（N）』三式）。"""
import io, os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "ver38四分律_起心動念心智分析框架_修正版.md")
L = io.open(MD, encoding="utf-8").read().split("\n")
CN = {c: i for i, c in enumerate("零一二三四五六七八九", 0)}


def c2n(s):
    if not s:
        return None
    s = s.strip()
    if s.isdigit():
        return int(s)
    m = re.fullmatch(r"([一二三四五六七八九])?十([一二三四五六七八九])?", s)
    if m:
        return CN.get(m.group(1), 1) * 10 + CN.get(m.group(2), 0)
    return CN.get(s)


def sec_nums(t):
    for p in (r"^第([一二三四五六七八九十]+)節", r"^閘門([一二三四五六七八九十]+)",
              r"^（([一二三四五六七八九十]+)）", r"^([一二三四五六七八九十]+)、"):
        m = re.match(p, t)
        if m:
            return [c2n(m.group(1))]
    return []


def kua_nums(t):
    m = re.match(r"^([一二三四五六七八九十]+)至([一二三四五六七八九十]+)[、，]", t)
    if m:
        return list(range(c2n(m.group(1)), c2n(m.group(2)) + 1))
    for p in (r"^([一二三四五六七八九十]+)、", r"^（([一二三四五六七八九十]+)）", r"^(\d+)[\.、]",
              r"^【?第?([一二三四五六七八九十]+)款"):
        m = re.match(p, t)
        if m:
            v = c2n(m.group(1))
            return [v] if v else []
    return []


chidx = [i for i, l in enumerate(L) if re.match(r"^# 第[一二三四五六七八九]章", l)]
chidx.append(next(i for i, l in enumerate(L) if l.startswith("# 結語")))
span, tree = {}, {}
for k, nm in enumerate("一二三四五六七八九"):
    a, b = chidx[k], chidx[k + 1]
    name = u"第%s章" % nm
    span[name] = (a, b)
    secs, cur = [], None
    for i in range(a + 1, b):
        l = L[i]
        if l.startswith("### "):
            cur = {"nums": sec_nums(l[4:].strip()), "title": l[4:].strip(), "kuan": [], "i": i}
            secs.append(cur)
        elif l.startswith("#### ") and cur is not None:
            cur["kuan"].append({"nums": kua_nums(l[5:].strip()), "title": l[5:].strip(), "i": i})
    tree[name] = secs

dead = []
stat = collections.Counter()
PTR = re.compile(r"(?:(第[一二三四五六七八九]章)|本章|此章)\s*(?:第([一二三四五六七八九十]+)節|閘門([一二三四五六七八九十]+))?\s*"
                 r"(?:第([一二三四五六七八九十]+)款|之?第?([一二三四五六七八九十]+)款)?")
for i, l in enumerate(L):
    own = next((n for n, (a, b) in span.items() if a <= i < b), None)
    for m in re.finditer(r"(?:第([一二三四五六七八九])章|本章|此章)\s*(?:第([一二三四五六七八九十]+)節|閘門([一二三四五六七八九十]+))?(?:第([一二三四五六七八九十]+)款)?", l):
        name = u"第%s章" % m.group(1) if m.group(1) else own
        if not name or name not in tree:
            continue
        sn = c2n(m.group(2)) if m.group(2) else (c2n(m.group(3)) if m.group(3) else None)
        kn = c2n(m.group(4))
        if sn is None and kn is None:
            continue
        secs = tree[name]
        allsec = sorted({n for s in secs for n in s["nums"]})
        if sn is None:
            stat["款而無節（含糊）"] += 1
            dead.append((i + 1, "款而無節", m.group(0), ""))
            continue
        sec = next((s for s in secs if sn in s["nums"]), None)
        if sec is None:
            stat["節號死鏈"] += 1
            dead.append((i + 1, "節號死鏈", m.group(0), "%s 節號 %s" % (name, allsec)))
            continue
        if kn is None:
            stat["節合"] += 1
            continue
        if any(kn in x["nums"] for x in sec["kuan"]):
            stat["款合"] += 1
        else:
            stat["款號死鏈"] += 1
            dead.append((i + 1, "款號死鏈", m.group(0), "%s『%s』款號 %s" % (
                name, sec["title"][:16], sorted({n for x in sec["kuan"] for n in x["nums"]}))))
print("統計：%s" % dict(stat))
for d in dead:
    if d[1] == "款而無節":
        continue
    print("  L%-6d %-8s ｜%s｜%s" % (d[0], d[1], d[2], str(d[3])[:110]))
print("含糊（款而無節）%d 處，其列於下：" % stat["款而無節（含糊）"])
for d in dead:
    if d[1] == "款而無節":
        print("  L%-6d ｜%s" % (d[0], L[d[0] - 1].strip()[:60]))
