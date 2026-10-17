# -*- coding: utf-8 -*-
"""決定性檢驗：凡「波逸提法第N條」所在行另有 「」 引文者，取該引文於 11-21 檔之實際行號，
對照 (N竟) 尾標所切出之條次區間，查條次是否相符。"""
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

p = [f for f in glob.glob(os.path.join(ROOT, u'原文', u'11-21*.txt'))][0]
rows = [l.rstrip(u'\n') for l in io.open(p, encoding=u'utf-8-sig')]
NR = [norm(l) for l in rows]
MK = re.compile(u'[(（]([^）()]{1,6})竟[)）]')
marks, exp = [], 1
for i, l in enumerate(rows, 1):
    m = MK.search(l)
    if not m:
        continue
    n = num(m.group(1))
    if n == exp:
        marks.append((i, n))
        exp += 1
        if n == 90:
            break
RANGE = {}
prev = 1
for i, n in marks:
    RANGE[n] = (prev, i)
    prev = i + 1

Q = re.compile(u'「(.+?)」', re.S)
ELL = re.compile(u'…+|\\.{3,}')
CLAIM = re.compile(u'(?:九十)?單提|波逸提法第([0-9]{1,2}|[一二三四五六七八九十]{1,3})條')
out = []
tested = bad = 0
for li, line in enumerate(_tk.LINES):
    for m in re.finditer(u'波逸提法第([0-9]{1,2}|[一二三四五六七八九十]{1,3})條', line):
        N = int(m.group(1)) if m.group(1).isdigit() else num(m.group(1))
        if not N:
            continue
        lo, hi = None, None
        for q in Q.findall(line):
            for f in ELL.split(q):
                nf = norm(f)
                if len(nf) < 10:
                    continue
                for i, r in enumerate(NR, 1):
                    if nf in r:
                        lo = hi = i
                        break
                if lo:
                    break
            if lo:
                break
        if not lo:
            continue
        owner = [k for k, (a, b) in RANGE.items() if a <= lo <= b]
        tested += 1
        if owner != [N]:
            bad += 1
            out.append(u'MISS L%d 宣稱第%s條；引文實在本檔 L%d → 屬第%s條 :: %s' % (
                li + 1, N, lo, owner, line[max(0, m.start() - 20):m.start() + 70]))
out.insert(0, u'條次可判定 %d 項；條次不合 %d 項（索引 %d 條）' % (tested, bad, len(RANGE)))
io.open(os.path.join(ROOT, u'_work', u'tiaochk2.txt'), 'w', encoding=u'utf-8').write(u'\n'.join(out))
print(len(RANGE), tested, bad)
