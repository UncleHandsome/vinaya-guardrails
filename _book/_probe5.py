# -*- coding: utf-8 -*-
"""跋難陀對與世俗法條號之細量。"""
import io, re

t = io.open(u'佛陀的護欄_四分律行為心理學與現代僧伽治理.md', encoding='utf-8').read()
L = t.split(u'\n')
APX = t.index(u'# 【卷末')

print(u'== 第十二章 案例標題（十四～十九）==')
for i, l in enumerate(L, 1):
    if l.startswith(u'### 案例') and 9250 <= i <= 9400:
        print(u'  L%-6d %s' % (i, l[4:64]))

print(u'\n== 案例十八（跋難陀佛滅已得自在）全文 ==')
a = next(i for i, l in enumerate(L, 1) if l.startswith(u'### 案例十八：跋難陀佛滅已得自在'))
b = next(i for i in range(a + 1, len(L)) if L[i - 1].startswith((u'### ', u'## ')))
print(u'\n'.join(x[:118] for x in L[a - 1:b]))

print(u'\n== 對位表與落點表中涉僧15／跋難陀之條 ==')
for fn in (u'_book/對位表.tsv', u'_book/落點表.tsv'):
    s = io.open(fn, encoding='utf-8').read().split(u'\n')
    for ln in s:
        if u'僧15' in ln or u'波23' in ln or u'案例十八' in ln:
            print(u'  %s｜%s' % (fn.split(u'/')[1][:4], ln[:96]))

print(u'\n== 世俗法條號之窮舉（漢字與阿拉伯數俱收）==')
NUM = u'[0-9０-９〇一二三四五六七八九十百]{1,6}'
pats = [u'[一-鿿]{2,16}法[・§]?第?' + NUM + u'條',
        u'[一-鿿]{2,16}法第' + NUM + u'條',
        u'『[一-鿿]{2,16}法』']
hits = []
for p in pats:
    for m in re.finditer(p, t[:APX]):
        ln = t[:m.start()].count(u'\n') + 1
        hits.append((ln, m.group(0)))
hits.sort()
last = None
for ln, s in hits:
    if s == last:
        continue
    last = s
    print(u'    L%-6d %s' % (ln, s))
print(u'  共 %d 處（去前 %d）' % (len(hits), len(set(s for _, s in hits))))
