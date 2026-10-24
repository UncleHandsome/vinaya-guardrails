# -*- coding: utf-8 -*-
"""268 輪・量二：新尺之網界——① 有無『』式節名漏收；② 有無圍欄／終卷內之指針被誤掃；
   ③ 無括號之節級指針有幾處（此類只由第 10 目守其可達，本尺不判其文）。"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
L = io.open(os.path.join(ROOT, NAME), encoding=u'utf-8-sig').read().split(u'\n')
FENCE = chr(96) * 3
inside = False
fence = set()
for i, l in enumerate(L):
    if l.startswith(FENCE):
        inside = not inside
        continue
    if inside:
        fence.add(i)
END = next(i for i, l in enumerate(L) if l.startswith(u'# 終卷'))
ENDN = next(i for i in range(END + 1, len(L)) if L[i].startswith(u'# '))

HEAD = re.compile(u'第([一二三四五六七八九十]+)章(?:第([一二三四五六七八九十]+)節|閘門([一二三四五六]))?'
                  u'[^\\n]{0,3}([（『【「])')
tot = dark = 0
forms = {}
for i, l in enumerate(L):
    for m in HEAD.finditer(l):
        tot += 1
        forms[m.group(4)] = forms.get(m.group(4), 0) + 1
        if i in fence or END <= i < ENDN:
            dark += 1
            print(u'  圍欄／終卷內：L%d %s' % (i + 1, l.strip()[:70]))
print(u'章節級指稱＋引式 共 %d・其中圍欄或終卷內 %d・引式分佈 %s' % (tot, dark, forms))

BARE = re.compile(u'第[一二三四五六七八九十]+章第[一二三四五六七八九十]+節(?!\\s*[（【])')
n = sum(len(BARE.findall(l)) for l in L)
print(u'無括號之節級指針 %d 處（第 10 目守其可達，本尺不判其文）' % n)
A = re.compile(u'第[一二三四五六七八九十]+章第[一二三四五六七八九十]+節[（【]')
print(u'有括號（本尺之靶）%d 處' % sum(len(A.findall(l)) for l in L))
