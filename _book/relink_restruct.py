# -*- coding: utf-8 -*-
"""重構版之指針重鏈（甲案・第一步）：
   案例指針：A 當號即合者不動；其餘以上 22 字＋下 22 字回錨產器冊身，讀舊指針，經章表換算。
   節級指針：舊（章,節）取節題，節題於換算後之新章內找同題之節，易其號。
   多錨者取『案號與原書所載相同』之一；不得者一律不動並列帳。
   用法：python -X utf8 _work/r56fix.py [--go]"""
import io
import os
import re
import sys
import unicodedata
from collections import defaultdict

NEW = u'佛陀的護欄_重構版.md'
OLD = u'佛陀的護欄_四分律行為心理學與現代僧伽治理.md'
MAP = os.path.join(HERE, u'重構章表.tsv')
LOG = os.path.join(HERE, u'重鏈帳一.txt')
BAK = u'_work/重構版.前.bak'
GO = '--go' in sys.argv
CN = u'零一二三四五六七八九十'
DROP = set(u" \t、，。：:；;（）()「」『』“”‘'\"/／-—─│·・.!?？…*" + u'\u3000')


def cnum(s):
    s = s.strip()
    if s == u'十':
        return 10
    if u'十' in s:
        a, _, b = s.partition(u'十')
        return (1 if not a else CN.index(a)) * 10 + (CN.index(b) if b else 0)
    return CN.index(s) if s in CN and s else 0


def cn(n):
    d = CN
    if n < 10:
        return d[n]
    if n == 10:
        return u'十'
    if n < 20:
        return u'十' + (d[n % 10] if n % 10 else u'')
    a, b = divmod(n, 10)
    return d[a] + u'十' + (d[b] if b else u'')


def key(s):
    s = unicodedata.normalize('NFKC', s)
    return u''.join(ch for ch in s if ch not in DROP)


def scan(path):
    """回 (行列表, 章→案號集, 章→節題列, 章起行)"""
    L = io.open(path, encoding='utf-8-sig').read().replace('\r\n', '\n').split('\n')
    cur, cases, secs, head = 0, defaultdict(set), defaultdict(list), {}
    for i, l in enumerate(L):
        m = re.match(u'^# 第([一二三四五六七八九十]+)章', l)
        if m:
            cur = cnum(m.group(1))
            head[cur] = i
            continue
        if cur:
            m = re.match(u'^### 案例([一二三四五六七八九十百]+)[：:](.*)$', l)
            if m:
                cases[cur].add(cnum(m.group(1)))
                continue
            m = re.match(u'^## (第[一二三四五六七八九十]+節　.+)$', l)
            if m:
                secs[cur].append(m.group(1).strip())
    return L, cases, secs, head


NL, NCASES, NSECS, _nh = scan(NEW)
OL, OCASES, OSECS, _oh = scan(OLD)
okey = key(u'\n'.join(OL))
rows = [l.split(u'\t') for l in io.open(MAP, encoding='utf-8').read().split('\n')
        if l.strip() and not l.startswith('#')]
C2N = {(int(r[0]), int(r[1])): (int(r[3]), int(r[4])) for r in rows}
CHof = defaultdict(set)
for (oc, on), (nc, nn_) in C2N.items():
    CHof[oc].add(nc)
CHMAP = {c: next(iter(s)) for c, s in CHof.items() if len(s) == 1}
# 舊節題 → 新（章,序）
SECMAP = {}
for oc, titles in OSECS.items():
    nc = CHMAP.get(oc)
    if not nc:
        continue
    for k, t in enumerate(titles, 1):
        if t in NSECS.get(nc, []):
            SECMAP[(oc, k)] = (nc, NSECS[nc].index(t) + 1)
        else:
            base = key(re.sub(u'^第[一二三四五六七八九十]+節　', u'', t))
            got = [j for j, x in enumerate(NSECS.get(nc, []), 1)
                   if key(re.sub(u'^第[一二三四五六七八九十]+節　', u'', x))[:14] == base[:14]]
            if got:
                SECMAP[(oc, k)] = (nc, got[0])
print(u'章對 %d・節對 %d／舊節 %d' % (len(CHMAP), len(SECMAP),
                                     sum(len(v) for v in OSECS.values())))

RE_CS = re.compile(u'第([一二三四五六七八九十]+)章案例([一二三四五六七八九十百]+)')
RE_SC = re.compile(u'第([一二三四五六七八九十]+)章第([一二三四五六七八九十]+)節')
RE_OCS = re.compile(u'第([一二三四五六七八九十]+)章案例([一二三四五六七八九十百]+)')
RE_OSC = re.compile(u'第([一二三四五六七八九十]+)章第([一二三四五六七八九十]+)節')


def anchor(line, m, kind):
    """以上下文在舊冊定位，回該處之舊指針 (章,數) 列表。"""
    pre = key(line[max(0, m.start() - 44):m.start()])[-22:]
    post = key(line[m.end():m.end() + 44])[:22]
    if len(pre) < 8 and len(post) < 8:
        return []
    pat = RE_OCS if kind == u'案' else RE_OSC
    pos, found = -1, []
    while True:
        pos = okey.find(pre, pos + 1)
        if pos < 0 or len(found) > 8:
            break
        seg = okey[pos + len(pre):pos + len(pre) + len(post) + 30]
        mm = pat.search(seg)
        if mm:
            found.append((cnum(mm.group(1)), cnum(mm.group(2))))
    return list(dict.fromkeys(found))


out, log = [], []
nA = nFix = nSec = 0
pend = defaultdict(list)
for i, l in enumerate(NL, 1):
    if l.startswith('# '):
        out.append(l)
        continue

    def cs(m):
        global nA, nFix
        c, n = cnum(m.group(1)), cnum(m.group(2))
        if c in NCASES and n in NCASES[c]:
            nA += 1
            return m.group(0)
        f = anchor(l, m, u'案')
        ok = [(oc, on) for (oc, on) in f if (oc, on) in C2N]
        if len(ok) > 1:
            same = [x for x in ok if C2N[x][1] == n]
            ok = same[:1] or ok[:1]
        if ok:
            nc, nn_ = C2N[ok[0]]
            nFix += 1
            if (nc, nn_) != ok[0] or True:
                log.append(u'L%-6d 案 %s→第%s章案例%s（舊%s-%s）' % (
                    i, m.group(0), cn(nc), cn(nn_), ok[0][0], ok[0][1]))
            return u'第%s章案例%s' % (cn(nc), cn(nn_))
        if f:
            pend[u'所引之案已佚'].append(u'L%d %s（舊%s-%s）' % (i, m.group(0), f[0][0], f[0][1]))
        else:
            pend[u'上下文無錨'].append(u'L%d %s｜…%s…' % (i, m.group(0), key(l[max(0, m.start() - 20):m.start()])[-12:]))
        return m.group(0)

    def sc(m):
        global nSec
        c, s = cnum(m.group(1)), cnum(m.group(2))
        if c in NSECS and s <= len(NSECS[c]):
            return m.group(0)
        hit = SECMAP.get((c, s))
        if not hit:
            f = anchor(l, m, u'節')
            ok = [(oc, os_) for (oc, os_) in f if (oc, os_) in SECMAP]
            hit = SECMAP[ok[0]] if ok else None
        if hit:
            nSec += 1
            log.append(u'L%-6d 節 %s→第%s章第%s節' % (i, m.group(0), cn(hit[0]), cn(hit[1])))
            return u'第%s章第%s節' % (cn(hit[0]), cn(hit[1]))
        pend[u'節級不得其解'].append(u'L%d %s' % (i, m.group(0)))
        return m.group(0)

    l2 = RE_CS.sub(cs, l)
    l2 = RE_SC.sub(sc, l2)
    out.append(l2)

print(u'案例：合 %d・換 %d｜節級：換 %d｜帳 %d 行' % (nA, nFix, nSec, len(log)))
for k, v in pend.items():
    print(u'  待裁【%s】%d 條：%s' % (k, len(v), v[:3]))
if GO:
    io.open(BAK, 'w', encoding='utf-8', newline='\n').write(u'\n'.join(NL))
    io.open(NEW, 'w', encoding='utf-8', newline='\n').write(u'\n'.join(out))
    with io.open(LOG, 'w', encoding='utf-8', newline='\n') as f:
        f.write(u'# 重鏈之帳（每行一換）\n')
        for x in log:
            f.write(x + u'\n')
        for k, v in pend.items():
            f.write(u'\n# 待裁：%s（%d）\n' % (k, len(v)))
            for x in v:
                f.write(u'  ' + x + u'\n')
    print(u'已落盤；原稿存 %s；帳記 %s' % (BAK, LOG))
else:
    print(u'試跑：未改一檔')
