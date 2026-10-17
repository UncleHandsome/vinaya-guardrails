# -*- coding: utf-8 -*-
"""第 129 輪軸：第八章十六觀心問——正文『法度索引』之案號集合 ↔ 清冊表格『對應案例索引』集合之對合

病緣（實測）：問[15] 正文列〔僧1〕〔僧5〕〔僧11〕〔僧25〕，清冊表卻列〔僧1〕〔僧2〕〔僧5〕〔僧25〕——
    〔僧2〕乃問[14] 之案，〔僧11〕在表內失踪。行者持表自省時所照之鏡與正文所指不同。
口徑：兩側皆只取〔遮N〕〔開N〕〔僧N〕〔遺N〕〔補遺N〕案號，去重後作集合比對；
     正文側若另標「第X章／閘門／第五章第X節」等法理指針，非案號，不計。
"""
import io
import re
import sys

MD = u'ver38四分律_起心動念心智分析框架_修正版.md'
L = io.open(sys.argv[1] if len(sys.argv) > 1 else MD, encoding='utf-8').read().split('\n')
CASE = re.compile(u'〔(遮|開|僧|遺|補遺)(\\d{1,3})〕')
QID = re.compile(u'問\\[?(\\d{1,2})\\]?')

body = {}          # 問序 → 正文法度索引之案號集合
table = {}         # 問序 → 清冊表之案號集合
cur = None
for i, l in enumerate(L):
    if l.startswith(u'#'):                     # 入下節即斷，免把後文之法度索引算入末問
        cur = None
    m = re.match(u'^\\* \\*\\*問\\[(\\d{1,2})\\]', l)
    if m:
        cur = int(m.group(1))
        continue
    if cur and u'法度索引' in l:
        body.setdefault(cur, set()).update(x.group(0) for x in CASE.finditer(l))
    if cur and l.startswith(u'> **【道岔'):
        cur = None
r0 = next(k for k, l in enumerate(L) if l.startswith(u'| **[1] '))
for k in range(r0, min(r0 + 40, len(L))):
    m = re.match(u'^\\| \\*\\*\\[(\\d{1,2})\\]', L[k])
    if m:
        n = int(m.group(1))
        cells = [c.strip() for c in L[k].split(u'|')]
        table[n] = set(x.group(0) for x in CASE.finditer(cells[4] if len(cells) > 4 else u''))

bad = 0
warn = 0
for n in sorted(set(body) | set(table)):
    a, b = body.get(n), table.get(n)
    if a is None or b is None:
        print(u'  待考 問[%d] 缺一側：正文 %s／表 %s' % (n, sorted(a or []), sorted(b or [])))
        warn += 1
        continue
    if a - b:                                  # 正文所舉而清冊失載——行者持表自省即少一面鏡，是病
        print(u'  病 問[%d] 清冊失載：%s' % (n, sorted(a - b)))
        bad += 1
    if b - a:                                  # 清冊多載（或別問之案誤掛）——列待考，不逕判死
        print(u'  待考 問[%d] 清冊多載：%s' % (n, sorted(b - a)))
        warn += 1
print(u'==== 觀心問索引對合：%d 問｜病 %d 處｜待考 %d 處 ====' % (len(set(body) | set(table)), bad, warn))
sys.exit(1 if bad else 0)
