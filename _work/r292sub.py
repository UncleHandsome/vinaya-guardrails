# -*- coding: utf-8 -*-
"""292・次碼之全量清點：逐枚抽〔案例 NN / XMM〕並列其所在行形制。"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
T = io.open(SRC, 'rb').read().decode('utf-8').replace(u'\r\n', u'\n')
L = T.split(u'\n')

RX = re.compile(u'〔案例 (\\d+) ?/ ?([^〕]+)〕')
rows = {}
forms = {}
for i, x in enumerate(L):
    for m in RX.finditer(x):
        n, tail = m.group(1), m.group(2).strip()
        rows.setdefault(n, []).append((i + 1, tail))
        forms[tail] = forms.get(tail, 0) + 1
print(u'含次碼之主號數：%d｜枚數：%d' % (len(rows), sum(len(v) for v in rows.values())))
print(u'次碼式樣（前 12）：%s' % sorted(forms.items(), key=lambda kv: -kv[1])[:12])
bad = [k for k, v in rows.items() if len(set(t for _i, t in v)) > 1]
print(u'同號而次碼不一者：%s' % bad)
for k in sorted(rows, key=int):
    print(u'  %s ➔ %s｜行 %s' % (k, rows[k][0][1], u','.join(str(i) for i, _t in rows[k])))
print()
print(u'—— 純數字對（螺旋雙案，非次碼）——')
for i, x in enumerate(L):
    for m in re.finditer(u'〔案例 \\d+ ?/ ?\\d+〕', x):
        print(u'  L%d %s' % (i + 1, m.group(0)))
print(u'—— 其他含斜線之案例形——')
for i, x in enumerate(L):
    for m in re.finditer(u'〔案例 [^〕]*／[^〕]*〕|〔案例 [^〕]*/[^〕]*〕', x):
        if not RX.search(m.group(0)) and not re.match(u'〔案例 \\d+ ?/ ?\\d+〕', m.group(0)):
            print(u'  L%d %s' % (i + 1, m.group(0)))
