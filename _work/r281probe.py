# -*- coding: utf-8 -*-
"""281・外路第九報告（論第七章下〜附錄六）之量：標點生肉段・案號形・凡例條文・法域條號・目錄與 H1。"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
TXT = io.open(BOOK, encoding=u'utf-8-sig').read()
LINES = TXT.split(u'\n')
Q = re.compile(u'「([^「」]+)」')
PUNCT = u'，。；：、！？「」‘’（）《》【】…—‧'


def longest_run(s):
    best = cur = 0
    for ch in s:
        if ch in PUNCT or ch.isspace():
            cur = 0
        else:
            cur += 1
            if cur > best:
                best = cur
    return best


print(u'══ 一・無標點長段（逐字引號內最長無標點串 >= 40 字者）')
hits = []
for i, l in enumerate(LINES):
    for m in Q.finditer(l):
        n = longest_run(m.group(1))
        if n >= 40:
            hits.append((i + 1, n, len(m.group(1))))
for ln, n, ql in hits[:40]:
    s = LINES[ln - 1]
    j = s.find(u'〔案例')
    lab = s[j:j + 16] if j >= 0 else s[:16]
    print(u'   L%-5d 無標點 %3d 字・引文 %4d 字｜%s' % (ln, n, ql, lab.strip()))
print(u'   共 %d 段' % len(hits))

print(u'\n══ 二・案號之形（副支／跨界參照）')
for k in [u'未遂支', u'延伸法相', u'跨界參照', u'參照引證', u'副支', u'對照支', u'既遂支']:
    print(u'   %-8s %d 見' % (k, TXT.count(k)))
odd = set()
for i, l in enumerate(LINES):
    for m in re.finditer(u'〔案例 \\d+[^〕]*〕', l):
        t = m.group(0)
        if not re.match(u'〔案例 \\d+〕$', t) and u'/' not in t:
            odd.add((i + 1, t))
for ln, t in sorted(odd)[:20]:
    print(u'   奇形 L%-5d %s' % (ln, t))
print(u'   奇形共 %d 枚' % len(odd))

print(u'\n══ 三・凡例條文（章／節／款／目）')
for k in [u'章直轄節', u'款下為目', u'節下為款']:
    for i, l in enumerate(LINES):
        if k in l:
            print(u'   %-6s L%-5d %s' % (k, i + 1, l.strip()[:160]))

print(u'\n══ 四・H1 之（上）（下）與目錄條')
for i, l in enumerate(LINES):
    if re.match(u'^# 第[七八]章', l):
        print(u'   H1  L%-5d %s' % (i + 1, l.strip()[:60]))
for i in range(0, 480):
    s = LINES[i]
    if (u'第七章' in s or u'第八章' in s) and (u'（上）' in s or u'（下）' in s):
        print(u'   目錄? L%-5d %s' % (i + 1, s.strip()[:90]))

print(u'\n══ 五・法域條號與除斥期間')
for k in [u'三十日', u'除斥', u'勞基法', u'勞動基準', u'三個月']:
    print(u'   %-6s %d 見' % (k, TXT.count(k)))
for i, l in enumerate(LINES):
    if u'除斥期間' in l or (u'三十日' in l and u'解僱' in l):
        print(u'   L%-5d %s' % (i + 1, l.strip()[:190]))

print(u'\n══ 六・附錄五楞嚴異文註・附錄六導言之缺號註')
for k in [u'狂性自歇', u'狂心若歇', u'編次虛一', u'非漏印', u'虛置']:
    for i, l in enumerate(LINES):
        if k in l:
            print(u'   %-6s L%-5d %s' % (k, i + 1, l.strip()[:150]))
