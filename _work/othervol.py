# -*- coding: utf-8 -*-
"""他典引文之卷次對檔：凡《X》卷N ＋ 「」 引文，且 X 於 佛經/ 有分卷檔者，
檢该引文是否見於對應卷號之檔案。"""
import io, os, re, sys, glob
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk

ROOT, norm = _tk.ROOT, _tk.norm
Q = re.compile(u'「(.+?)」', re.S)
ELL = re.compile(u'…+|\\.{3,}')
CN = {u'一': 1, u'二': 2, u'三': 3, u'四': 4, u'五': 5, u'六': 6, u'七': 7, u'八': 8, u'九': 9, u'十': 10}

def cn2int(s):
    s = s.strip()
    if s.isdigit():
        return int(s)
    if s in CN:
        return CN[s]
    if s.startswith(u'十') and len(s) > 1:
        return 10 + CN.get(s[1:], 0)
    return None

DIRS = {}
for d in glob.glob(os.path.join(ROOT, u'佛經', u'*')):
    if not os.path.isdir(d):
        continue
    name = os.path.basename(d)
    vols = {}
    for f in glob.glob(os.path.join(d, u'*.txt')):
        stem = os.path.basename(f)[:-4]
        if u'-' in stem:
            a, b = stem.split(u'-')
            for k in range(int(a), int(b) + 1):
                vols[k] = norm(io.open(f, encoding='utf-8-sig').read())
        elif stem.isdigit():
            vols[int(stem)] = norm(io.open(f, encoding='utf-8-sig').read())
    if vols:
        DIRS[name] = vols
# 單檔者
for f in glob.glob(os.path.join(ROOT, u'佛經', u'*.txt')):
    DIRS[os.path.basename(f)[:-4]] = {0: norm(io.open(f, encoding='utf-8-sig').read())}

ALIAS = {u'成唯識論': u'成唯識論', u'楞嚴經': u'楞嚴經', u'大佛頂首楞嚴經': u'楞嚴經',
         u'寶性論': u'寶性論', u'解深密經': u'解深密經', u'大乘入楞伽經': u'大乘入楞伽經',
         u'楞伽阿跋多羅寶經': u'楞伽阿跋多羅寶經', u'月燈三昧經': u'月燈三昧經',
         u'菩薩地論': u'菩薩地_戒品', u'瑜伽師地論': u'菩薩地_戒品', u'梵網經': u'梵網經心地戒品上'}

PAT = re.compile(u'《([^》]{2,12})》[^「」]{0,24}?卷\\s*([0-9]{1,2}|[一二三四五六七八九十]{1,3})')
L = _tk.LINES
out = []
tested = wrong = 0
for i, line in enumerate(L):
    for m in PAT.finditer(line):
        nm, vn = m.group(1), cn2int(m.group(2))
        key = None
        for a, b in ALIAS.items():
            if a in nm and b in DIRS:
                key = b
                break
        if not key or vn is None:
            continue
        vols = DIRS[key]
        if 0 in vols:
            continue
        tail = line[m.end():m.end() + 400]
        frags = [norm(f) for q in Q.findall(tail) for f in ELL.split(q) if len(norm(f)) >= 8]
        if not frags:
            pre = line[max(0, m.start() - 400):m.start()]
            frags = [norm(f) for q in Q.findall(pre) for f in ELL.split(q) if len(norm(f)) >= 8]
        if not frags:
            continue
        where = {v for v in vols for f in frags if f in vols[v]}
        found_any = any(f in ''.join(vols.values()) for f in frags)
        if not found_any:
            continue
        tested += 1
        if vn not in where:
            wrong += 1
            out.append(u'L%d 《%s》卷%d 宣稱；引文實見卷%s :: %s' % (
                i + 1, key, vn, sorted(where), line[max(0, m.start() - 20):m.start() + 90]))
out.insert(0, u'可測 %d 處（引文於該典他檔查得而不於所稱卷者）；卷次不合 %d 處' % (tested, wrong))
io.open(os.path.join(ROOT, u'_work', u'other_vol.txt'), 'w', encoding=u'utf-8').write(u'\n'.join(out))
print(tested, wrong)
