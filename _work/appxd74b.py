# -*- coding: utf-8 -*-
"""第七十四輪新軸（定稿）：附錄A／D／I／J 引文逐字覆核。

附錄C 為修訂誌，其 「」 悉屬校勘引述（凡例明定另列豁免，與附錄L／M 同），故不入此軸；
未合者依既定口徑先作兩類豁免：① 同行或次行已標界之「無從覆核／本地語料未收」；② 名相有據。
"""
import io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import _tk  # noqa

NAMES = [u'\u9644\u9304A', u'\u9644\u9304D', u'\u9644\u9304I', u'\u9644\u9304J']
idx, ranges = set(), []
for nm in NAMES:
    rng = _tk.sec(nm)
    if not rng:
        raise SystemExit(u'查無篇：%s' % nm.encode('unicode_escape').decode())
    a, b = rng
    idx.update(range(a, b))
    ranges.append((nm, a, b))


def which(i):
    for nm, a, b in ranges:
        if a <= i < b:
            return nm
    return u'?'


stat = {'vin': 0, 'other': 0, 'term': 0, 'short': 0, 'adj': 0}
misses = []
tot = 0
for i in sorted(idx):
    l = _tk.LINES[i]
    for q in _tk.Q_RE.findall(l):
        if not _tk.has_source_strict(i):
            continue
        n = _tk.norm(q)
        tot += 1
        if len(n) < 6:
            stat['short'] += 1
            continue
        if n in _tk.VINAYA:
            stat['vin'] += 1
            continue
        hit = [k for k, v in _tk.OTHER.items() if n in v]
        if hit:
            stat['other'] += 1
            continue
        st = _tk.st_adjust('miss', i, q)
        if not st.startswith('miss'):
            stat[st if st in stat else 'adj'] += 1
            continue
        if _tk.term_ok(q):
            stat['term'] += 1
            continue
        misses.append((i + 1, which(i), n, len(n)))

out = [u'=== 附錄A／D／I／J 冠出處之引文宣稱：%d 段 ===' % tot,
       u'  四分律逐字 %d｜他典逐字 %d｜已標界豁免 %d｜名相有據 %d｜過短 %d｜未合 %d'
       % (stat['vin'], stat['other'], stat['adj'], stat['term'], stat['short'], len(misses)), '']
for ln, nm, n, k in misses:
    out.append(u'  [%s] %s L%-6d (%d字) %s' % (u'實病級' if k >= 12 else u'短段', nm, ln, k, n[:70]))
open(os.path.join(HERE, 'appxd74.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print('claims', tot, 'miss', len(misses))
