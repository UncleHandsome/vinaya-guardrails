# -*- coding: utf-8 -*-
"""節序之治：一書一制。每章之節標題統為「第N節」，並隨手把指針舊序改寫為新序。

法則：凡章內節號已自一連貫且同制者，一字不動（其指針自亦不變）；
      唯混制・跳號・斷頭之章才重編，重編時立｛舊序→新序｝之映射，指針據此改寫，
      故『第N章第M節』之形永不失指。
"""
import re

CN = {c: i for i, c in enumerate(u"零一二三四五六七八九")}


def cnum(s):
    if s in CN:
        return CN[s]
    if s == u"十":
        return 10
    if u"十" not in s:
        return 0
    a, _, b = s.partition(u"十")
    return (1 if not a else CN.get(a, 0)) * 10 + CN.get(b, 0)


def cn_num(n):
    d = u"零一二三四五六七八九"
    if n < 10:
        return d[n]
    if n == 10:
        return u"十"
    if n < 20:
        return u"十" + (d[n % 10] if n % 10 else u"")
    a, b = divmod(n, 10)
    return d[a] + u"十" + (d[b] if b else u"")


H2J = re.compile(u"^## 第([一二三四五六七八九十]+)節[　 ]*(.*)$")
H2N = re.compile(u"^## ([一二三四五六七八九十]+)、[　 ]*(.*)$")


def plan_chapter(lines):
    """返 [(行序, 式, 舊序, 標題)]。"""
    out = []
    for k, l in enumerate(lines):
        m = H2J.match(l)
        if m:
            out.append((k, u"J", cnum(m.group(1)), m.group(2)))
            continue
        m = H2N.match(l)
        if m:
            out.append((k, u"N", cnum(m.group(1)), m.group(2)))
    return out


def needs_fix(items):
    if len(items) < 2:
        return False
    nums = [n for _, _, n, _ in items]
    kinds = set(k for k, _, _, _ in items)
    if len(kinds) > 1:
        return True
    return nums != list(range(1, len(nums) + 1))


def renumber(text):
    """重編節號並回傳指針映射 {(章名, 舊序, 式) : 新序}。"""
    lines = text.split(u"\n")
    h1 = [i for i, l in enumerate(lines) if l.startswith(u"# ") and not l.startswith(u"# 【")]
    h1 = [i for i in h1 if re.match(u"^# 第[一二三四五六七八九十]+章　", lines[i]) or
          re.match(u"^# 附錄|終卷", lines[i])]
    h1p = h1 + [len(lines)]
    refmap = {}
    fixed = []
    for a, b in zip(h1p[:-1], h1p[1:]):
        title = lines[a]
        m = re.match(u"^# (第[一二三四五六七八九十]+章　?|附錄[一二三四五]|終卷)", title)
        ch = m.group(1).replace(u"　", u"") if m else u""
        if not ch.startswith(u"第"):
            continue
        if not ch.endswith(u"章"):
            ch = ch + u"章"
        items = plan_chapter(lines[a + 1:b])
        if not needs_fix(items):
            continue
        for k, (off, kind, old, name) in enumerate(items, 1):
            lines[a + 1 + off] = u"## 第%s節　%s" % (cn_num(k), name)
            refmap.setdefault((ch, kind, old), k)
        fixed.append(ch)
    return u"\n".join(lines), refmap, fixed


def rewrite_refs(text, refmap):
    """據映射改寫『第N章第M節』——舊序不分式，先取 J 式，次取 N 式。"""
    n = [0]

    def one(m):
        ch = u"第%s章" % m.group(1)
        old = cnum(m.group(2))
        new = refmap.get((ch, u"J", old)) or refmap.get((ch, u"N", old))
        if not new:
            return m.group(0)
        n[0] += 1
        return u"%s第%s節" % (ch, cn_num(new))
    t = re.sub(u"第([一二三四五六七八九十]+)章第([一二三四五六七八九十]+)節", one, text)
    return t, n[0]
