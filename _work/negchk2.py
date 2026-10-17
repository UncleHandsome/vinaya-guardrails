# -*- coding: utf-8 -*-
"""否定式宣稱覆核（精確版）：只取本書慣用句式——
   『X』...（0 見／查無／律無／無此逐字句／未見／通卷 0 見／檢索為 0 見）
   或 （查無／律無／本律無）『X』
   逐條回語料實查；範圍詞（調部／本律／全語料／他典）決定檢索域。"""
import io, os, re, sys, glob
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk

ROOT, norm = _tk.ROOT, _tk.norm
VIN = _tk.VINAYA
OTHER = u''.join(_tk.OTHER.values())
p = [f for f in glob.glob(os.path.join(ROOT, u'原文', u'50-60*.txt'))][0]
TIAO = u''.join(norm(l) for l in io.open(p, encoding='utf-8-sig'))
import _tk as _t
rows = [norm(l) for l in io.open(p, encoding='utf-8-sig')]
TIAO = u''.join(rows[582:1280])

AFTER = re.compile(u'[』」][^」』。；！？]{0,14}(0\\s*見|未見|查無|律無|無此|檢索為\\s*0|通卷[^。]{0,4}0\\s*見|俱?無從)')
BEFORE = re.compile(u'(查無|律無|本律無|全無|未見|不見)[^「『」』]{0,10}[『「]')
Q = re.compile(u'[『「]([^』」]{2,30})[』」]')

out, tested, bad = [], 0, 0
for i, line in enumerate(_tk.LINES):
    for m in Q.finditer(line):
        term = m.group(1).strip(u'：: 、')
        if u'**' in term or len(norm(term)) < 2 or len(norm(term)) > 20:
            continue
        tail = line[m.end():m.end() + 34]
        head = line[max(0, m.start() - 22):m.start()]
        neg = AFTER.search(u'』' + tail) or bool(BEFORE.search(head))
        if not neg:
            continue
        seg = head + term + tail
        if u'調部' in tail or u'調部' in head:
            scope, pool = u'調部', TIAO
        elif re.search(u'他典|論典|成唯識|俱舍', tail + head):
            scope, pool = u'他典', OTHER
        else:
            scope, pool = u'本律全書', VIN
        nt = norm(term)
        tested += 1
        if nt in pool:
            bad += 1
            out.append(u'FALSE L%d [%s]『%s』稱無而實有 :: %s' % (i + 1, scope, term, seg[:120]))
out.insert(0, u'精確句式檢得 %d 條；稱無而實有 %d 條' % (tested, bad))
io.open(os.path.join(ROOT, u'_work', u'neg2.txt'), 'w', encoding='utf-8').write(u'\n'.join(out))
print(tested, bad)
