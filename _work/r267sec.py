# -*- coding: utf-8 -*-
"""267 輪・量二：『第N章第M節（X）』之括號命題，其核字是否見於所靶之節。

口徑（只量不判，供於目逐條裁）：
  ① 章界**合併上・下兩 H1**（第八章分上、下，單取其一必漏其半➔假紅，266 輪之誡）；
  ② 節界：以 H3『### 第M節』起、至下一個 H3 或 H1 止；章內無此節題者標『節不可求』；
  ③ 命題拆核：按『・、與之及』切，留 norm ≥2 之核；逐核查見於『節』與見於『章』兩層；
  ④ 判語四態：節全中／節缺(章中)／節缺(章亦缺)／節不可求(改查章)。
用法：python -X utf8 _work/r267sec.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
t = io.open(BOOK, encoding=u'utf-8-sig').read()
L = t.split(u'\n')

CN = {u'一': 1, u'二': 2, u'三': 3, u'四': 4, u'五': 5, u'六': 6, u'七': 7, u'八': 8}


def cn2n(s):
    if s.isdigit():
        return int(s)
    if s in CN:
        return CN[s]
    if s.startswith(u'十'):
        return 10 + (CN.get(s[1:], 0) if len(s) > 1 else 0)
    if u'十' in s:
        a, b = s.split(u'十')
        return CN.get(a, 1) * 10 + CN.get(b, 0)
    return None


# 章界（合併上・下）
H1 = [(i, l) for i, l in enumerate(L) if re.match(u'^# 第[一二三四五六七八]章', l)]
chap = {}
for k, (i, l) in enumerate(H1):
    j = H1[k + 1][0] if k + 1 < len(H1) else len(L)
    n = cn2n(re.match(u'^# 第(.+)章', l).group(1))
    body = chap.get(n, u'')
    chap[n] = body + u'\n' + u'\n'.join(L[i:j])
print(u'章 %d 個 H1，合併後 %d 章' % (len(H1), len(chap)))

# 節界
sec = {}
for k, (i, l) in enumerate(H1):
    n = cn2n(re.match(u'^# 第(.+)章', l).group(1))
    j = H1[k + 1][0] if k + 1 < len(H1) else len(L)
    cur = None
    for m in range(i, j):
        s = re.match(u'^### 第(.+)節', L[m])
        if s:
            cur = cn2n(s.group(1))
            sec[(n, cur)] = sec.get((n, cur), u'')
        elif re.match(u'^#{1,3} ', L[m]) and not L[m].startswith(u'### 〔'):
            cur = None
        if cur:
            sec[(n, cur)] += L[m] + u'\n'

PTR = re.compile(u'第([一二三四五六七八])章第([一二三四五六七八九十]+)節（([^（）]+)）')
CUT = re.compile(u'[・、；，：／與及之\\s]')
seen = 0
for i, l in enumerate(L):
    for m in PTR.finditer(l):
        seen += 1
        n, sn, name = cn2n(m.group(1)), cn2n(m.group(2)), m.group(3)
        core = [x for x in CUT.split(name) if len(re.sub(u'[\\s　]', u'', x)) >= 2]
        core = [re.sub(u'[\\s　]', u'', x) for x in core]
        sbody = sec.get((n, sn))
        cbody = chap.get(n, u'')
        if sbody is None:
            print(u'L%-5d 第%s章第%s節（%s）\n        節不可求・章內核:%s'
                  % (i + 1, m.group(1), m.group(2), name,
                     u' '.join(u'%s%s' % (x, u'中' if x in cbody else u'缺') for x in core)))
            continue
        insec = [x for x in core if x in sbody]
        inchap = [x for x in core if x in cbody]
        tag = (u'節全中' if len(insec) == len(core) else
               (u'節缺・章中' if len(inchap) == len(core) else u'節缺・章亦缺'))
        miss = [x for x in core if x not in sbody]
        print(u'L%-5d %s %-24s 核%d・節中%d・章中%d  %s%s'
              % (i + 1, tag, u'第%s章第%s節' % (m.group(1), m.group(2)),
                 len(core), len(insec), len(inchap),
                 name[:24], (u'  缺:' + u'、'.join(miss[:6])) if miss else u''))
print(u'合 %d 處' % seen)
