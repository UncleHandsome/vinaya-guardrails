# -*- coding: utf-8 -*-
# 第 215 輪·負測：不變量 87（印面引號外無『揵度』）須有牙——① 散文植形即 FAIL、
#   ⓪ 同字植於逐字引文內須不報、② 植於圍欄須不報、③ 現形全綠；末以哈希自證主檔未損。
import hashlib
import io
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.stdout.reconfigure(encoding=u'utf-8', errors=u'replace')

MD = u'ver38四分律_起心動念心智分析框架_修正版.md'
orig = io.open(MD, encoding=u'utf-8').read()
h0 = hashlib.sha256(orig.encode(u'utf-8')).hexdigest()
L = orig.split(u'\n')
NM = u'印面引號外無篇題異形'


def write(lines):
    io.open(MD, 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(lines))


def check():
    subprocess.run([sys.executable, u'-X', u'utf8', u'_tk.py', u'check'],
                   capture_output=True, text=True, encoding=u'utf-8', errors=u'replace')
    txt = io.open(u'_work/check.txt', encoding=u'utf-8').read()
    return [l for l in txt.split(u'\n') if l.startswith(u'FAIL')]


def idx(pred, dflt=None):
    for i in range(len(L)):
        if pred(i):
            return i
    return dflt


I_PROSE = idx(lambda i: L[i].startswith(u'**') and len(L[i]) > 40)
I_QUOTE = idx(lambda i: L[i].startswith(u'> ') and u'「' in L[i] and u'」' in L[i])
I_FENCE = idx(lambda i: L[i].strip() == u'```text')
assert None not in (I_PROSE, I_QUOTE, I_FENCE), u'植形之位未得'
res = []
try:
    a = list(L)
    a[I_PROSE] = a[I_PROSE] + u'（呵責揵度）'
    write(a)
    f = check()
    res.append((u'① 散文植『揵度』即報', any(NM in x for x in f), []))

    b = list(L)
    k = b[I_QUOTE].index(u'「') + 1
    b[I_QUOTE] = b[I_QUOTE][:k] + u'揵度' + b[I_QUOTE][k:]
    write(b)
    f = check()
    res.append((u'⓪ 同字植逐字引文內須不報', not any(NM in x for x in f), []))

    c = list(L)
    c[I_FENCE + 1] = c[I_FENCE + 1] + u'  揵度'
    write(c)
    f = check()
    res.append((u'② 同字落圍欄須不報', not any(NM in x for x in f), []))

    write(L)
    f = check()
    res.append((u'③ 現形全綠退 0', not f, f[:2]))
finally:
    write(L)
    h1 = hashlib.sha256(io.open(MD, encoding=u'utf-8').read().encode(u'utf-8')).hexdigest()

for nm, ok, ex in res:
    print(u'  %-28s %s%s' % (nm, u'中' if ok else u'不中', (u'｜' + str(ex)[:56]) if ex else u''))
same = h0 == h1
print(u'復原自證：主檔哈希 %s（%s）' % (u'如舊' if same else u'已臟！', h0[:12]))
ok = len(res) == 4 and all(x[1] for x in res) and same
print(u'結果斷：%s' % (u'閘有牙、引文與圍欄從寬、主檔一字未損' if ok else u'負測不合'))
sys.exit(0 if ok else 1)
