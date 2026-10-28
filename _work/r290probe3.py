# -*- coding: utf-8 -*-
r"""290・三查：難教之本地原文・『大正藏卷段』之數與形・尼波逸提諸案之卷引。"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, u'_work'))
import _tk                                               # noqa: E402
import v39align as VA                                    # noqa: E402

V = _tk.VINAYA
BOOK = io.open(os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md'),
               encoding='utf-8').read()
BL = BOOK.split('\n')

print(u'【難教・本地原文】')
for m in re.finditer(u'難教', V):
    print(u'  …%s…' % V[max(0, m.start() - 70):m.start() + 60])

print(u'\n【大正藏卷段／卷段 標法之量】')
for p in [u'大正藏卷段', u'卷段', u'檔內行', u'L\d+']:
    print(u'  %-12s %d 見' % (p, len(re.findall(p, BOOK))))

print(u'\n【v39linchk 之解析錨（其認何形制）】')
S = io.open(os.path.join(ROOT, u'_work', u'v39linchk.py'), encoding='utf-8').read()
for i, l in enumerate(S.split('\n')):
    if re.search(u'PAT|re\.compile|finditer|口徑|卷段', l):
        print(u'  L%-4d %s' % (i + 1, l.strip()[:130]))

print(u'\n【附錄四諸案之尼波逸提卷引（內部一致性之線索）】')
for i, l in enumerate(BL):
    if l.startswith(u'| **〔案例') and (u'比丘尼波逸提' in l or u'尼波逸提' in l):
        m = re.search(u'卷([一二三四五六七八九十百]{1,6})', l)
        print(u'  L%-5d %s ｜ 卷%s' % (i + 1, l.split(u'|')[1].strip()[:34], m.group(1) if m else u'?'))
for i, l in enumerate(BL):
    if u'卷二十七' in l or u'卷二十八' in l or u'卷二十九' in l or u'卷三十' in l:
        print(u'  冊 L%-5d %s' % (i + 1, l.strip()[:118]))
