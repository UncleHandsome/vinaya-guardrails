# -*- coding: utf-8 -*-
# 第 218 輪·負測：不變量 88（考證案語之括號與標籤畫一）須有牙。
#   ① 散文植『（編者按：…）』即報、② 散文植『〔按：…』即報（兩式各路）、
#   ⓪ 植於「」逐字引文內須不報（照錄之形不犯）、②b 植於圍欄須不報、③ 現形全綠退 0；
#   末以哈希自證主檔未損（同 215 輪之器）。
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
NM = u'考證案語不作'


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
I_PROSE2 = idx(lambda i: L[i].startswith(u'* **') and len(L[i]) > 60)
I_QUOTE = idx(lambda i: L[i].startswith(u'> ') and u'「' in L[i] and u'」' in L[i])
I_FENCE = idx(lambda i: L[i].strip() == u'```text')
assert None not in (I_PROSE, I_PROSE2, I_QUOTE, I_FENCE), u'植形之位未得'
res = []
try:
    a = list(L)
    a[I_PROSE] = a[I_PROSE] + u'（編者按：此係植形之測文，非真案語。）'
    write(a)
    f = check()
    res.append((u'① 散文植全形圓括號即報', any(NM in x for x in f), f[:1]))

    b = list(L)
    b[I_PROSE2] = b[I_PROSE2] + u'〔按：此亦植形之測文。〕'
    write(b)
    f = check()
    res.append((u'② 散文植『〔按：』即報', any(NM in x for x in f), f[:1]))

    c = list(L)
    k = c[I_QUOTE].index(u'「') + 1
    c[I_QUOTE] = c[I_QUOTE][:k] + u'（編者按：照錄之內不犯）' + c[I_QUOTE][k:]
    write(c)
    f = check()
    res.append((u'⓪ 植於逐字引文內須不報', not any(NM in x for x in f), f[:2]))

    d = list(L)
    d[I_FENCE + 1] = d[I_FENCE + 1] + u' 〔按：欄內不犯〕'
    write(d)
    f = check()
    res.append((u'②b 落圍欄須不報', not any(NM in x for x in f), f[:2]))

    write(L)
    f = check()
    res.append((u'③ 現形全綠退 0', not f, f[:2]))
finally:
    write(L)
    h1 = hashlib.sha256(io.open(MD, encoding=u'utf-8').read().encode(u'utf-8')).hexdigest()

for nm, ok, ex in res:
    print(u'  %-30s %s%s' % (nm, u'中' if ok else u'不中', (u'｜' + str(ex)[:60]) if ex else u''))
same = h0 == h1
print(u'復原自證：主檔哈希 %s（%s）' % (u'如舊' if same else u'已臟！', h0[:12]))
ok = len(res) == 5 and all(x[1] for x in res) and same
print(u'結果斷：%s' % (u'閘有牙（兩式俱報）、引文與圍欄從寬、現形綠、主檔一字未損'
                     if ok else u'負測不合'))
sys.exit(0 if ok else 1)
