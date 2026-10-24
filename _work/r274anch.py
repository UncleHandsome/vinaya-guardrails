# -*- coding: utf-8 -*-
"""274 輪・量③：新稿每一枚〔案例 NN〕指針之**歸屬面**——名對號否，以『該名是否見於本號卡身』判之。

緣由：第 27 目只比『卡題』，遇表列之短描（『糞掃衣想』『病苦服藥』）即成描述語而不判——**盲處在此**。
今以卡身全文為據（真名必見於本卡），三名一判：中（名見本卡）／錯系（名見他卡而不見本卡）／無著（全書卡身無此名）。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r274anch.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
BL = io.open(os.path.join(ROOT, NAME), encoding=u'utf-8').read().split(u'\n')
AP = os.path.join(os.path.expanduser(u'~'), u'.qoder', u'tmp',
                  u'C--Users-lionc-OneDrive-----------------', u'attachments',
                  u'e11d207e-a4f7-4a0e-9edb-3124ac9d8a4a',
                  u'fa89e70f-39b1-4bde-9002-a0548ff0653d.txt')
AL = io.open(AP, encoding=u'utf-8', errors=u'replace').read().split(u'\n')
norm = lambda s: re.sub(u'[\\s\\u3000\\uff0c\\u3001\\uff1b\\uff1a\\uff08\\uff09()\\[\\]'
                        u'\\u3010\\u3011\\u3014\\u3015\\u00b7\\u2014\\-\\u300c\\u300d\\u300e\\u300f]', u'', s)

# ── 卡身區間（題＋文）
heads = [(i, l) for i, l in enumerate(BL) if re.match(u'^### \u3014案例 [0-9]+\u3015', l)]
BODY = {}
TIT = {}
for k, (i, l) in enumerate(heads):
    num = re.match(u'^### \u3014案例 ([0-9]+)\u3015(.*)$', l)
    n, t = num.group(1), num.group(2)
    end = heads[k + 1][0] if k + 1 < len(heads) else len(BL)
    nxt = next((j for j in range(i + 1, end) if BL[j].startswith(u'#')), end)   # 卡身止於下一任何標題
    BODY[n] = norm(u''.join(BL[i:nxt]))
    TIT[n] = t

PAT = re.compile(u'\u3014案例 ?([0-9]{1,3})\u3015\\s*(?:\\*\\*)?([一-\\u9fff]{2,12})')
rows = []
for i, l in enumerate(AL):
    for m in PAT.finditer(l):
        n, nm = m.group(1).zfill(2), norm(m.group(2))
        if n not in BODY:
            rows.append((i + 1, n, m.group(2), u'\u67e5\u7121\u6b64\u865f', u''))
            continue
        own = nm in BODY[n] or TIT[n].startswith(m.group(2)[:2])
        others = [k for k, v in BODY.items() if len(nm) >= 3 and nm in v]
        v = u'\u4e2d' if own else (u'\u932f\u7cfb' if others else u'\u7121\u8457')
        rows.append((i + 1, n, m.group(2), v, u'、'.join(sorted(others))[:22]))
print(u'新稿〔案例 NN〕＋名 之指針共 %d 枚' % len(rows))
for r in rows:
    mark = u'  ' if r[3] == u'\u4e2d' else u'\u26a0'
    print(u'%s L%-5d %s%s『%s』｜卡題『%s』→ %s%s' % (
        mark, r[0], u'\u6848\u4f8b', r[1], r[2][:12], TIT.get(r[1], u'—')[:14], r[3],
        (u'（見 %s）' % r[4]) if r[3] == u'\u932f\u7cfb' else u''))
cnt = {}
for r in rows:
    cnt[r[3]] = cnt.get(r[3], 0) + 1
print(u'\u2014\u2014 \u5224\u8a9e\u6578\uff1a%s' % cnt)
print(u'\u4ec5\u53f7\u7121\u540d\u4e4b\u6307\u91dd\uff1a%d 枚' % len([
    1 for l in AL for _ in re.finditer(u'\u3014案例 ?[0-9]{1,3}\u3015(?!\\s*(?:\\*\\*)?[一-\\u9fff]{2,12})', l)]))
