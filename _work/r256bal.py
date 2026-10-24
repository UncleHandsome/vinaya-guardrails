# -*- coding: utf-8 -*-
"""第 256 輪・引號調平器：回填之後，內層 『…』 常只餘单边（候選不帶語料之引號），
本器於【律典原典】欄內逐行調平——孤現之 』 先削，行末仍無對者再削 『。行數不動。"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
P = os.path.join(ROOT, NAME)
L = io.open(P, encoding=u'utf-8').read().split(u'\n')
APPLY = u'apply' in sys.argv


def balance(s):
    out, open_at = [], []
    for i, c in enumerate(s):
        if c == u'\u300e':
            open_at.append(len(out))
        elif c == u'\u300f':
            if open_at:
                open_at.pop()
            else:
                continue                     # 孤現之 』 不收
        out.append(c)
    for pos in open_at:                      # 未閉之 『 亦不收
        out[pos] = u''
    return u''.join(out)


n = 0
for i, l in enumerate(L):
    if not l.strip():
        continue
    if l.count(u'\u300e') == l.count(u'\u300f'):
        continue
    j = i
    while j >= 0 and not L[j].startswith(u'#### 【律典原典】') and not L[j].startswith(u'#'):
        j -= 1
    if j < 0 or not L[j].startswith(u'#### 【律典原典】'):
        continue                             # 唯治原典欄，他處之跨行引對不妄動
    b = balance(l)
    if b != l:
        n += 1
        print(u'L%d 削 %d 符｜%s' % (i + 1, len(l) - len(b), l[:70]))
        print(u'      → %s' % b[:70])
        if APPLY:
            L[i] = b
if APPLY:
    assert n
    io.open(P, 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(L))
    back = io.open(P, encoding=u'utf-8').read().split(u'\n')
    assert len(back) == len(L)
    print(u'———— 調平落檔 %d 行（%d 行 → %d 行）' % (n, len(L), len(back)))
else:
    print(u'———— 待調平 %d 行（只報；apply 方改）' % n)
