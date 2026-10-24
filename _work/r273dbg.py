# -*- coding: utf-8 -*-
"""負測之病：`r273face` 在假冊上崩（traceback 被截），此器先把假冊留住並印全 stderr。"""
import os
import subprocess
import sys

import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, u'_work', u'r273mutant.pdf')
SRC = os.path.join(ROOT, u'_print', max([q for q in os.listdir(os.path.join(ROOT, u'_print'))
                                         if q.startswith(u'ver39') and q.endswith(u'.pdf')
                                         and len(q) > 30], key=len))
d = pymupdf.open(SRC)
toc = d.get_toc()
texts = [u''.join(d[i].get_text().split()) for i in range(d.page_count)]
idx = next(i for i in range(len(toc) - 1, 0, -1) if toc[i][1].replace(u' ', u'')[:12] not in texts[0])
d.set_toc([[lv, ti, (1 if i == idx else pg)] for i, (lv, ti, pg) in enumerate(toc)])
print(u'移靶：第 %d 條『%s』➔p1' % (idx + 1, toc[idx][1][:34]))
d.save(OUT, garbage=3, deflate=True)
d.close()
q = subprocess.run([sys.executable, u'-X', u'utf8', os.path.join(ROOT, u'_work', u'r273face.py'),
                    u'\u5217\u5370', OUT], capture_output=True, text=True, encoding=u'utf-8', cwd=ROOT)
print(u'rc=%d' % q.returncode)
print(u'--- stdout ---\n%s' % (q.stdout or u'')[-1200:])
print(u'--- stderr ---\n%s' % (q.stderr or u'')[-1500:])
