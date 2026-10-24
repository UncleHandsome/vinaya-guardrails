# -*- coding: utf-8 -*-
"""269 輪・帳三：索引掛鉤之冊態數字補正（本輪只改輪次與計數，未改行数・_bytes_・SHA＝漏項），
   再跑一次『名冊配實物』與『記憶兩檔之數字對照正本』。"""
import hashlib
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEM = os.path.join(os.path.expanduser(u'~'), u'.qoder', u'projects',
                   u'C--Users-lionc-OneDrive-----------------', u'memory')
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
raw = open(os.path.join(ROOT, NAME), 'rb').read()
SHA = hashlib.sha256(raw).hexdigest()[:12]
NL = raw.decode(u'utf-8-sig').count(u'\n') + 1
print(u'冊實測：%d 行・%d B・SHA %s' % (NL, len(raw), SHA))

PAIRS = [
    (os.path.join(MEM, u'MEMORY.md'),
     u'**第 269 輪止（2026-10-20）**：ver39 正本 9,338 行・966,940 B・SHA `02ac8be6433f`',
     u'**第 269 輪止（2026-10-20）**：ver39 正本 %d 行・%d B・SHA `%s`' % (NL, len(raw), SHA)),
]
for p, old, new in PAIRS:
    t = io.open(p, encoding=u'utf-8').read()
    n = t.count(old)
    print(u'  %s｜錨 %d｜%s' % (os.path.basename(p), n, old[:44]))
    if n != 1:
        continue
    t = t.replace(old, new, 1)
    io.open(p, 'w', encoding=u'utf-8', newline=u'').write(t)
    chk = io.open(p, encoding=u'utf-8').read()
    print(u'      ➔ 已正・新串命中 %d・舊串餘 %d（期望 %d）'
          % (chk.count(new), chk.count(old), new.count(old)))

t = io.open(os.path.join(MEM, u'project-round31-state.md'), encoding=u'utf-8').read()
for pat in (u'[0-9],[0-9]{3} 行', u'\\d+ B', u'SHA `?[0-9a-f]{12}'):
    print(u'  現況檔之 %s ➔ %s' % (pat, sorted(set(re.findall(pat, t)))[:6]))
WORK = os.path.join(ROOT, u'_work')
names = sorted(set(re.findall(u'`(r\d+\w*\.py|v39\w+\.py|_simp\w+\.py)`', t)))
absent = [n for n in names if not os.path.exists(os.path.join(WORK, n))]
print(u'名冊 %d 檔・查無此檔：%s' % (len(names), absent or u'無'))
