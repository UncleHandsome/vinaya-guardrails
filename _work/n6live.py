# -*- coding: utf-8 -*-
"""第六章敘事層 「」 之現場統計（驗收裁決段所引數字之真相）。"""
import io, os, sys, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk

norm, VIN = _tk.norm, _tk.VINAYA
segs = list(_tk.fragments_c6n()) if hasattr(_tk, 'fragments_c6n') else []
hit = miss = short = 0
longmiss = []
for item in segs:
    case, ln, q = item if len(item) == 3 else (None,) + tuple(item)
    nq = norm(q)
    frags = [norm(x) for x in re.split(u'…+|\\.{3,}', q) if norm(x)]
    ok = all(f in VIN for f in frags)
    if ok:
        hit += 1
    elif max((len(f) for f in frags), default=0) >= 12:
        miss += 1
        longmiss.append(u'%s L%d %d字 :: %s' % (case, ln, max(len(f) for f in frags), q[:40]))
    else:
        short += 1
out = [u'第六章・◎原典以外 「」 段：共 %d；逐字對合 %d；未合且≥12字 %d；短標／過短 %d' % (
    len(segs), hit, miss, short)]
out += longmiss[:12]
out.append(u'附錄F 無從覆核筆數（F-3 所列）：%d' % len(re.findall(u'^\\|', u'\n'.join(
    _tk.LINES[_tk.sec('附錄F')[0]:_tk.sec('附錄F')[1]]))))
io.open(os.path.join(_tk.ROOT, u'_work', u'n6live.txt'), 'w', encoding=u'utf-8').write(u'\n'.join(out))
print(len(segs), hit, miss, short)
