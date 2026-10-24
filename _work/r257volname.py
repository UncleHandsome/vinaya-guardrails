# -*- coding: utf-8 -*-
"""257 輪・引卷正名器：書中『01-10卷段』之類乃本地語料之檔名區間，非讀者語。
一律改為『卷一至十』之漢字卷段；行數不動，錨點自校，寫後回讀。
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
P = os.path.join(ROOT, NAME)
APPLY = u'apply' in sys.argv
CN = u'零一二三四五六七八九'


def cn(n):
    n = int(n)
    if n < 10:
        return CN[n]
    if n < 20:
        return u'十' + (CN[n % 10] if n % 10 else u'')
    return CN[n // 10] + u'十' + (CN[n % 10] if n % 10 else u'')


PAT = re.compile(u'([0-9]{1,2})-([0-9]{1,2})\\s*\u5377\u6bb5')
L = io.open(P, encoding=u'utf-8').read().split(u'\n')
n = 0
for i, l in enumerate(L):
    if PAT.search(l):
        new = PAT.sub(lambda m: u'\u5377%s至%s' % (cn(m.group(1)), cn(m.group(2))), l)
        n += 1
        print(u'L%-5d %s' % (i + 1, PAT.findall(l)))
        print(u'        → %s' % new[max(0, new.find(u'\u5377') - 14):new.find(u'\u5377') + 22])
        if APPLY:
            L[i] = new
if APPLY:
    assert n, u'無可改之行'
    txt = u'\n'.join(L)
    io.open(P, 'w', encoding=u'utf-8', newline=u'\n').write(txt)
    back = io.open(P, encoding=u'utf-8').read()
    assert len(back.split(u'\n')) == len(L), u'行數不合'
    assert not PAT.search(back), u'仍有檔名式引卷未淨'
    print(u'———— 已正名 %d 行・回讀凈盡（檔名式引卷 0 見）' % n)
else:
    print(u'———— 待正名 %d 行（只報；apply 方改）' % n)
