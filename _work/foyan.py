# -*- coding: utf-8 -*-
"""佛言／律云 式引導語之後的 「」 引文（即使未冠卷次），是否為語料逐字。
此類句子對讀者即等同逐字宣稱，掛 「」 而查無者屬真缺陷。"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk

ROOT, norm = _tk.ROOT, _tk.norm
VIN = _tk.VINAYA
Q = re.compile(u'「(.+?)」', re.S)
ELL = re.compile(u'…+|\\.{3,}')
LEAD = re.compile(u'(佛言|佛問言|佛告|世尊告|世尊言|律云|律作|律判|律制|律中|本律|經云|制句|結戒)[^「」]{0,12}\Z')
s6, e6 = _tk.sec(u'第六章')
L = _tk.LINES
out, hits, bad = [], 0, 0
for i, line in enumerate(L):
    if line.lstrip().startswith(('#', '|', '>')) and i < s6:
        pass
    for m in Q.finditer(line):
        q = m.group(1)
        pre = line[:m.start()]
        if not LEAD.search(pre[-16:]):
            continue
        frags = [norm(f) for f in ELL.split(q) if len(norm(f)) >= 6]
        if not frags:
            continue
        ok = all(f in VIN for f in frags)
        hits += 1
        if not ok:
            bad += 1
            miss = [f for f in frags if f not in VIN]
            out.append(u'%s L%d :: %s' % (u'第六章' if s6 <= i < e6 else u'其余', i + 1, q[:60]))
            out.append(u'      未合片段：%s' % miss[0][:50])
out.insert(0, u'佛言／律云式引導之引文共 %d 段；未逐字 %d 段' % (hits, bad))
io.open(os.path.join(ROOT, u'_work', u'foyan.txt'), 'w', encoding=u'utf-8').write(u'\n'.join(out))
print(hits, bad)
