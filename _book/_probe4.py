# -*- coding: utf-8 -*-
"""第四十八輪・四案之量尺（改shell：案例之界取『次一不高於己之標題』）。"""
import io, re

t = io.open(u'佛陀的護欄_四分律行為心理學與現代僧伽治理.md', encoding='utf-8').read()
L = t.split(u'\n')
APX = next((i for i, l in enumerate(L, 1) if l.startswith(u'# 【卷末')), len(L))

def lvl(l):
    for k in (1, 2, 3, 4):
        if l.startswith(u'#' * k + u' '):
            return k
    return 0

heads = [(i, lvl(l), l) for i, l in enumerate(L, 1) if lvl(l)]
end_of = {}
for k, (i, v, l) in enumerate(heads):
    j = len(L)
    for i2, v2, l2 in heads[k + 1:]:
        if v2 <= v:
            j = i2 - 1
            break
    end_of[i] = j

cases = []
for i, v, l in heads:
    if v == 3 and l.startswith(u'### 案例'):
        labs = set()
        for i2, v2, l2 in heads:
            if i < i2 <= end_of[i] and v2 == 4:
                labs.add(l2[5:].strip())
        cases.append((i, l[4:], labs, end_of[i]))
print(u'案例 %d 個（正文區 %d）' % (len(cases), len([c for c in cases if c[0] < APX])))
dist = {}
for _, _, labs, _ in cases:
    dist[len(labs)] = dist.get(len(labs), 0) + 1
print(u'欄數分佈：%s' % u'、'.join(u'%d欄×%d' % (k, v) for k, v in sorted(dist.items())))

print(u'\n== 一・跋難陀與卷五十四之兩出 ==')
for i, ttl, labs, j in cases:
    seg = u'\n'.join(L[i - 1:j])
    ch = [h[2][2:] for h in heads if h[0] < i and h[1] == 1][-1][:12]
    if u'五十四' in seg or u'54卷' in seg or (u'跋難陀' in ttl):
        print(u'  L%-6d %s｜%s 欄%d' % (i, ch, ttl[:40], len(labs)))
        print(u'        跋難陀見數 %d｜五十四 %d' % (seg.count(u'跋難陀'), seg.count(u'五十四')))

print(u'\n== 二・缺『心相照鏡』之案（按章）==')
no_m = [c for c in cases if u'心相照鏡' not in c[2]]
by = {}
for i, ttl, labs, j in no_m:
    ch = [h[2][2:] for h in heads if h[0] < i and h[1] == 1][-1][:10]
    by[ch[:10]] = by.get(ch[:10], 0) + 1
print(u'  缺鏡 %d 案：%s' % (len(no_m), u'｜'.join(u'%s×%d' % (k, v) for k, v in by.items())))
no_both = [c for c in no_m if u'法相剖析' not in c[2] and u'心相照鏡' not in c[2]]
print(u'  剖析與鏡俱無者 %d 案：%s' % (len(no_both), u'／'.join(c[1][:14] for c in no_both[:8])))

print(u'\n== 四・世俗法條之號（形制窮舉）==')
pats = [u'[一-鿿]{2,14}法\\s*第[0-9]{1,3}\\s*條', u'[一-鿿]{2,14}法§[0-9]{1,3}',
        u'[一-鿿]{2,14}法\\s*[0-9]{1,3}\\s*條', u'第[0-9]{1,3}\\s*條[（(]?[一-鿿]{2,10}法']
seen = []
for p in pats:
    for m in re.finditer(p, t[:t.index(u'# 【卷末')] if u'# 【卷末' in t else t):
        ln = t[:m.start()].count(u'\n') + 1
        if ln < APX:
            seen.append((ln, m.group(0)))
seen.sort()
for ln, s in seen:
    print(u'    L%-6d %s' % (ln, s))
print(u'  共 %d 處' % len(seen))
