# -*- coding: utf-8 -*-
"""270 輪・帳修：本輪新文之六枚簡形逐枚歸正（日誌 5・器身 1），並掃盡本輪所有 r270* 與 v39chk。
   引號內之舊形例示（供狀）一概不動。
用法：python -X utf8 _work/r270simp.py [apply]
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIARY = os.path.join(ROOT, u'_archive', u'編年工程日誌.md')
FIX = [
    (DIARY, u'**当场自量之果**', u'**當場自量之果**'),
    (DIARY, u'**蒙上省寫 5 处**', u'**蒙上省寫 5 處**'),
    (DIARY, u'今 5 处 0 落空', u'今 5 處 0 落空'),
    (DIARY, u'行號未動（9,340 行不变）', u'行號未動（9,340 行不變）'),
    (DIARY, u'未動即须如實', u'未動即須如實'),
    (DIARY, u'凡例第六節一句重写', u'凡例第六節一句重寫'),
    (os.path.join(ROOT, u'_work', u'v39chk.py'), u'蒙上省寫 %d 处', u'蒙上省寫 %d 處'),
]
FILES = {}
for p, old, new in FIX:
    if p not in FILES:
        FILES[p] = io.open(p, encoding=u'utf-8-sig').read()
bad = []
for p, old, new in FIX:
    if FILES[p].count(old) != 1:
        bad.append((os.path.basename(p), old[:30], FILES[p].count(old)))
print(u'合 %d 枚・錨不合 %d' % (len(FIX), len(bad)))
for x in bad:
    print(u'   %s｜%s｜命中 %d' % (x[0], x[1], x[2]))
if bad:
    sys.exit(2)
if u'apply' not in sys.argv:
    for p, old, new in FIX:
        print(u'  %-14s %s ➔ %s' % (os.path.basename(p), old[:32], new[:32]))
    print(u'乾跑，未寫入。')
    sys.exit(0)
for p, old, new in FIX:
    FILES[p] = FILES[p].replace(old, new, 1)
for p, txt in FILES.items():
    io.open(p, 'w', encoding=u'utf-8', newline=u'').write(txt)
back = {p: io.open(p, encoding=u'utf-8-sig').read() for p in FILES}
nok = [(os.path.basename(p), o[:24], back[p].count(o), n.count(o))
       for p, o, n in FIX if not (back[p].count(n) == 1 and back[p].count(o) == n.count(o))]
print(u'已寫入 %d 枚・回讀不符 %d' % (len(FIX), len(nok)))
for x in nok:
    print(u'   %s｜舊實 %d／期望 %d｜%s' % (x[0], x[1], x[2], x[3]))

# 掃本輪一切新檔（排除「」『』與反引號之例示）
sys.path.insert(0, os.path.join(ROOT, u'_work'))
import _simpmap
import _simpdict
K = set(_simpmap.S) | set(_simpdict.MAP.keys()) | set(u'写变场处当须号')
SKIP = re.compile(u'「[^」]*」|『[^』]*』|`[^`]*`')
WORK = os.path.join(ROOT, u'_work')
tot = 0
for f in sorted(os.listdir(WORK)):
    if not (f.startswith(u'r270') or f in (u'v39chk.py', u'v39secref.py')) or not f.endswith(u'.py'):
        continue
    for i, l in enumerate(io.open(os.path.join(WORK, f), encoding=u'utf-8-sig').read().split(u'\n')):
        seg = SKIP.sub(u'', l)
        cs = sorted(set(x for x in seg if x in K))
        if cs:
            tot += len(cs)
            print(u'   %s L%-4d %s｜%s' % (f, i + 1, u''.join(cs), seg.strip()[:64]))
for i, l in enumerate(io.open(DIARY, encoding=u'utf-8-sig').read().split(u'\n')[707:], 708):
    seg = SKIP.sub(u'', l)
    cs = sorted(set(x for x in seg if x in K))
    if cs:
        tot += len(cs)
        print(u'   日誌 L%-4d %s｜%s' % (i, u''.join(cs), seg.strip()[:60]))
print(u'——— 本輪新檔與新條之敘事簡形合計 %d（須 0）' % tot)
