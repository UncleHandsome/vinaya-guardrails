# -*- coding: utf-8 -*-
"""卷次／卷段宣稱 vs 引文實際所在檔案：視窗式（標頭行＋其下兩行之引文）。
凡宣稱「卷X」或「XY卷段」而引文實在他檔者，列為矛盾候選。"""
import io, os, re, sys, glob
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk

ROOT, norm = _tk.ROOT, _tk.norm
Q = re.compile(u'「(.+?)」', re.S)
ELL = re.compile(u'…+|\\.{3,}')
CN = {u'一': 1, u'二': 2, u'三': 3, u'四': 4, u'五': 5, u'六': 6, u'七': 7, u'八': 8, u'九': 9}
RANGE = {'01-10': (1, 10), '11-21': (11, 21), '22-30': (22, 30),
         '31-37': (31, 37), '38-49': (38, 49), '50-60': (50, 60)}

def cn2int(s):
    s = s.strip()
    if s.isdigit():
        return int(s)
    if s == u'十':
        return 10
    if u'十' in s:
        a, b = s.split(u'十', 1)
        return (CN.get(a, 1) if a else 1) * 10 + (CN.get(b, 0) if b else 0)
    return CN.get(s)

CORP = {}
for p in sorted(glob.glob(os.path.join(ROOT, u'原文', u'*.txt'))):
    key = re.match(r'(\d+-\d+)', os.path.basename(p)).group(1)
    with io.open(p, encoding=u'utf-8-sig') as f:
        CORP[key] = [norm(l) for l in f]

def where(frag):
    return [k for k, rows in CORP.items() if any(frag in r for r in rows)]

VOLPAT = re.compile(u'卷\\s*([0-9]{1,2}|[一二三四五六七八九十]{1,3})')
SEGPAT = re.compile(u'(01-10|11-21|22-30|31-37|38-49|50-60)\\s*卷段')
L = _tk.LINES
s6, e6 = _tk.sec(u'第六章')
sE, eE = _tk.sec(u'附錄E')
out = []
tested = conf = 0
for i in range(len(L)):
    if not (s6 <= i < e6 or sE <= i < eE):
        continue
    win = u'\n'.join(L[i:i + 3])
    segs = set(SEGPAT.findall(L[i]))
    vols = [v for v in (cn2int(m.group(1)) for m in VOLPAT.finditer(L[i])) if v and 1 <= v <= 60]
    if not segs and not vols:
        continue
    own = u'\n'.join(Q.findall(L[i]))
    src = L[i] if len(norm(min(Q.findall(L[i]), key=lambda x: -len(x)) if Q.findall(L[i]) else u'')) >= 14 else u'\n'.join(L[i + 1:i + 3])
    frags = [norm(f) for q in Q.findall(src) for f in ELL.split(q) if len(norm(f)) >= 14]
    if not frags:
        continue
    locs = []
    for fr in frags:
        locs.extend(where(fr))
    if not locs:
        continue
    tested += 1
    located = set(locs)
    seg_hit = bool(segs & located)
    vol_hit = any(RANGE[k][0] <= v <= RANGE[k][1] for v in vols for k in located)
    if (segs or vols) and not (seg_hit or vol_hit):
        conf += 1
        out.append(u'L%d :: 稱%s%s 而引文實見%s\n    %s' % (
            i + 1, sorted(segs) if segs else u'',
            (u' 卷' + u','.join(str(v) for v in vols)) if vols else u'',
            sorted(located), L[i][:110]))

out.insert(0, u'視窗可測 %d 行；矛盾 %d 行' % (tested, conf))
io.open(os.path.join(ROOT, u'_work', u'volchk2.txt'), 'w', encoding=u'utf-8').write(u'\n'.join(out))
print(tested, conf)
