# -*- coding: utf-8 -*-
"""寬容版條次索引：尾標缺號時不中斷，並標出界區。三十捨墮（01-10）與九十單提（11-21）皆覆核。"""
import io, os, re, sys, glob
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk

ROOT, norm = _tk.ROOT, _tk.norm
CN = {u'一': 1, u'二': 2, u'三': 3, u'四': 4, u'五': 5, u'六': 6, u'七': 7, u'八': 8, u'九': 9, u'十': 10}

def num(s):
    if s == u'十':
        return 10
    if s.startswith(u'十'):
        return 10 + CN.get(s[1:], 0)
    if u'十' in s:
        a, b = s.split(u'十')
        return CN.get(a, 1) * 10 + (CN.get(b, 0) if b else 0)
    return CN.get(s)

MK = re.compile(u'[(（]([^）()]{1,6})竟[)）]')
Q = re.compile(u'「(.+?)」', re.S)
ELL = re.compile(u'…+|\\.{3,}')

def build(prefix, lo, hi_max):
    p = [f for f in glob.glob(os.path.join(ROOT, u'原文', prefix + u'*.txt'))][0]
    rows = [l.rstrip(u'\n') for l in io.open(p, encoding=u'utf-8-sig')]
    nr = [norm(l) for l in rows]
    marks = []
    for i in range(lo - 1, len(rows)):
        m = MK.search(rows[i])
        if not m:
            continue
        n = num(m.group(1))
        if not n or n > hi_max or (marks and n <= marks[-1][1]):
            continue
        marks.append((i + 1, n))
        if n == hi_max:
            break
    rng, gaps = {}, []
    prev, lastn = lo, None
    for i, n in marks:
        if lastn is not None and n > lastn + 1:
            gaps.append((lastn + 1, n - 1))
            prev = prev  # merged region: keep prev (start of first merged block)
        rng[n] = (prev, i)
        prev, lastn = i + 1, n
    return rng, nr, [n for _, n in marks], gaps

def check(prefix, lo, hi_max, pat, minfrag=12):
    rng, nr, have, gaps = build(prefix, lo, hi_max)
    out = [u'--- %s 自 L%d：得尾標 %d 枚（1..%s，缺 %s）---' % (
        prefix, lo, len(have), have[-1] if have else 0, gaps or u'無')]
    t = b = 0
    ALLNUM = re.compile(u'第([0-9]{1,2}|[一二三四五六七八九十]{1,3})條')
    _bot = _tk.bottom_lines()   # 底冊（校勘記・修訂誌）多引稱舊誤形為反面例子，非今之宣稱，免掃
    for li, line in enumerate(_tk.LINES):
        if li in _bot or not re.search(pat, line):
            continue
        # 一行可並列數條（「波逸提法第八條、第八十四條」），引文又可跨數段——
        # 故取全行宣稱之集合與全數命中之律位，兩集合有交集即合（舊式只取首宣稱＋首命中，遂生虛警）
        claims = set()
        for m in re.finditer(pat, line):
            N = int(m.group(1)) if m.group(1).isdigit() else num(m.group(1))
            if N:
                claims.add(N)
        for m in re.finditer(u'[、，;；兼]第([0-9]{1,2}|[一二三四五六七八九十]{1,3})條', line):
            N = int(m.group(1)) if m.group(1).isdigit() else num(m.group(1))
            if N:
                claims.add(N)
        if not claims:
            continue
        owns = set()
        for q in Q.findall(line):
            for f in ELL.split(q):
                nf = norm(f)
                if len(nf) < minfrag:
                    continue
                for i, r in enumerate(nr, 1):
                    if nf in r:
                        owns.update(k for k, (a, bb) in rng.items() if a <= i <= bb)
                        break
        if not owns:
            continue
        t += 1
        if owns & claims:
            out.append(u'OK   L%d 宣稱第%s條 ← 律文所屬第%s條（合 %s）' % (
                li + 1, u'/'.join(str(x) for x in sorted(claims)),
                u'/'.join(str(x) for x in sorted(owns)), u'/'.join(str(x) for x in sorted(owns & claims))))
        else:
            ambig = [g for g in gaps if any(g[0] <= N <= g[1] for N in claims) or any(g[0] <= o <= g[1] for o in owns)]
            b += 1
            out.append(u'%s L%d 宣稱第%s條；律文實屬第%s條%s' % (
                u'AMB' if ambig else u'MISS', li + 1,
                u'/'.join(str(x) for x in sorted(claims)), u'/'.join(str(x) for x in sorted(owns)),
                u'（該區尾標缺 %s，界區合併故無法定數）' % ambig if ambig else u''))
    return out, t, b

o1, t1, b1 = check(u'01-10', 825, 30, u'尼薩耆波逸提法第([0-9]{1,2}|[一二三四五六七八九十]{1,3})條')
o2, t2, b2 = check(u'11-21', 1, 90, u'(?<!尼薩耆)波逸提法第([0-9]{1,2}|[一二三四五六七八九十]{1,3})條')
res = o1 + o2 + [u'合計可校 %d 項；可疑 %d 項（含尾標缺號之界區）' % (t1 + t2, b1 + b2)]
io.open(os.path.join(ROOT, u'_work', u'tiao4.txt'), 'w', encoding=u'utf-8').write(u'\n'.join(res))
print(t1, b1, t2, b2)
