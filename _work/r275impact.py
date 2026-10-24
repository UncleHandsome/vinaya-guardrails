# -*- coding: utf-8 -*-
"""275 輪・換章之損益（量產物，不量宣稱）：對換冊前後兩冊逐面計數，並列舊段／新段之差。

口徑：凡『印在紙上之數』皆以整冊為單位；案例卡・圍欄・引卷另計。
退碼：此尺不判成敗，只供報告——其中『掛出處之逐字』若減，須在日誌寫明減者何據。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r275impact.py
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import _tk                                                        # noqa: E402

NEW = os.path.join(ROOT, [q for q in os.listdir(ROOT) if q.startswith(u'ver39')
                          and q.endswith(u'.md') and u'列印' not in q][0])
OLD = os.path.join(ROOT, u'_work', u'swap.第四章.bak')

CARD = re.compile(u'^### 〔案例 (\\d+)〕')
SUPP = re.compile(u'^### 〔補遺 ')
FENCE = re.compile(u'^```', re.M)
VERB = re.compile(u'「[^」]{6,}」')
CITE = re.compile(u'《[^》]{1,12}》')
TERM = re.compile(u'『[^』]{2,14}』')
LONG = 120


def ptr_from_ruler():
    """指針之形不自造——自第八尺 v39secref 之源取 PTR 之式（名單不兩抄）。"""
    import ast
    src = io.open(os.path.join(ROOT, u'_work', u'v39secref.py'), encoding=u'utf-8').read()
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', None) == 'PTR':
            return re.compile(ast.literal_eval(n.value.args[0]))
    raise AssertionError(u'v39secref 之 PTR 不可求')


POINTER = ptr_from_ruler()


def stat(lines):
    s = u'\n'.join(lines)
    return {
        u'行': len(lines),
        u'字元': len(s),
        u'案例卡': sum(1 for x in lines if CARD.match(x)),
        u'補遺': sum(1 for x in lines if SUPP.match(x)),
        u'圍欄': len(FENCE.findall(s)) // 2,
        u'「」段': len(VERB.findall(s)),
        u'掛出處行': sum(1 for x in lines if CITE.search(x) and VERB.search(x)),
        u'《》段': len(CITE.findall(s)),
        u'『』段': len(TERM.findall(s)),
        u'指針': len(POINTER.findall(s)),
        u'長行': sum(1 for x in lines if len(x) > LONG),
    }


a = stat(io.open(OLD, encoding=u'utf-8').read().split(u'\n'))
b = stat(io.open(NEW, encoding=u'utf-8-sig').read().split(u'\n'))
print(u'%-12s %10s %10s %9s' % (u'面', u'舊冊', u'新冊', u'差'))
for k in sorted(a, key=lambda z: -abs(b[z] - a[z])):
    print(u'%-12s %10d %10d %+9d' % (k, a[k], b[k], b[k] - a[k]))

Lo = io.open(OLD, encoding=u'utf-8').read().split(u'\n')
Ln = io.open(NEW, encoding=u'utf-8-sig').read().split(u'\n')
i0 = next(i for i, l in enumerate(Lo) if l.startswith(u'# 第四章'))
j0 = next(i for i, l in enumerate(Lo) if l.startswith(u'# 第六章'))
i1 = next(i for i, l in enumerate(Ln) if l.startswith(u'# 第四章'))
j1 = next(i for i, l in enumerate(Ln) if l.startswith(u'# 第六章'))
sa, sb = Lo[i0:j0], Ln[i1:j1]
print(u'\n第四〜五章之段：舊 %d 行・%d 字｜新 %d 行・%d 字' % (
    len(sa), len(u'\n'.join(sa)), len(sb), len(u'\n'.join(sb))))
na, nb = stat(sa), stat(sb)
for k in na:
    if k in (u'行', u'字元'):
        continue
    print(u'  %-10s 舊 %6d｜新 %6d｜%+d' % (k, na[k], nb[k], nb[k] - na[k]))

kept = set(Ln)
lost = [x for x in sa if CITE.search(x) and VERB.search(x) and x not in kept]
surv = sum(1 for x in sa if CITE.search(x) and VERB.search(x) and x in kept)
print(u'舊段掛出處之行：存 %d｜失 %d' % (surv, len(lost)))
for x in lost[:3]:
    print(u'    …%s' % x.strip()[:60])
