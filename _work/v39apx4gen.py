# -*- coding: utf-8 -*-
"""260 輪・附錄四重生成器：其凡例自稱『繇諸卡自身之【律典原典】欄匯出（一卡一行）』——今依此言**實作之**。

二病同治：（甲）30 行之原句欄仍掛 「」 而實非逐字（卡身已改攝述而表未隨動）；
          （乙）表中缺三行（案例51・60・102——254 輪新立之卡未匯入），凡例卻自稱 102 案一行一卡。
法：卷引・原句一律取之卡身。有已證 「」 段者取其首段（逾 210 字則截於句末而綴『……』）；
    全無已證者作『律意：…』（不掛引號，與卡身同一口徑）。缺行插入其所屬之組表末。
只報；apply 方改。改後須 `_work/v39apx4chk.py` 報 0／0 且行數＝卡數。
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (ROOT, os.path.join(ROOT, u'_work')):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import _tk                                                     # noqa: E402

APPLY = u'apply' in sys.argv
L = _tk.MAIN_LINES
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'\u5217\u5370' not in q][0]
CARD = re.compile(u'^### 〔案例 (\\d+)〕(.*)$')
HEAD = re.compile(u'^#### 【律典原典】\\s*$')
GRP = re.compile(u'^## (.+)$')
STOP = re.compile(u'^(#{1,6} |---\\s*$)')
Q = re.compile(u'\u300c([^\u300c\u300d]+)\u300d')
VOL = re.compile(u'卷\\s*(\\[?)([0-9]+\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e]+)\\]?\uff08([^\uff09]+)\uff09')

c6 = next(i for i, l in enumerate(L) if l.startswith(u'# \u7b2c\u516d\u7ae0'))
e6 = next(i for i in range(c6 + 1, len(L)) if L[i].startswith(u'# '))
grps, cards = [], {}
gname = u''
for i in range(c6, e6):
    m = GRP.match(L[i])
    if m:
        gname = m.group(1).strip()
        if u'\u5c0e\u8a00' not in gname:
            grps.append(gname)
        continue
    m = CARD.match(L[i])
    if not m:
        continue
    num = m.group(1)
    j = i + 1
    while j < e6 and not HEAD.match(L[j]):
        j += 1
    k = j + 1
    cite = lv = u''
    quotes = []
    while k < e6 and not STOP.match(L[k]):
        if u'\u5f8b\u610f\uff1a' in L[k] and not lv:
            lv = L[k].split(u'\u5f8b\u610f\uff1a', 1)[1].strip()
        for q in Q.findall(L[k]):
            if _tk.classify(q)[0] in (u'hit', u'skip'):
                quotes.append(q)
        if not cite:
            mv = VOL.search(L[k])
            if mv:
                cite = mv.group(2) + u'\u00b7' + mv.group(3)
        k += 1
    cards[num] = {u'title': m.group(2).split(u'\u2014\u2014')[0].strip(), u'grp': gname,
                  u'cite': cite, u'q': quotes, u'lv': lv, u'line': i}


def cell3(num):
    d = cards[num]
    if d[u'q']:
        s = d[u'q'][0]                                   # 全段照錄，不截——截則破句、且生 『』 單邊之險
        return u' \u300c%s\u300d ' % s
    s = d[u'lv'] or u'（原典欄無文）'
    return u' 律意：%s ' % s                                       # 攝述亦全錄：截之必破 『』 之對


a4 = next(i for i, l in enumerate(L) if l.startswith(u'# 附錄四'))
a5 = next(i for i in range(a4 + 1, len(L)) if L[i].startswith(u'# 附錄五'))
RID = re.compile(u'\u3014\u6848\u4f8b ?(\\d+)\u3015')
seen, edits, tail = set(), {}, {}
for i in range(a4, a5):
    l = L[i]
    if not l.startswith(u'|'):
        continue
    ms = RID.findall(l)
    if not ms:
        continue
    num = ms[0]
    seen.add(num)
    cells = l.split(u'|')
    assert len(cells) == 5, u'附錄四行欄數異常 L%d（欄 %d）' % (i + 1, l.count(u'|'))
    new = u'|'.join(cells[:3] + [cell3(num)] + [cells[4]]) if num in cards else l
    if new != l:
        edits[i] = new
    g = cards.get(num, {}).get(u'grp', u'')
    if g:
        tail[g] = i
missing = [n for n in cards if n not in seen]
print(u'卡 %d・表行 %d・缺 %s・須改 %d 行' % (len(cards), len(seen), missing, len(edits)))
for i, new in sorted(edits.items()):
    old = L[i]
    print(u'  L%-5d %s' % (i + 1, RID.findall(old)[0]))
    print(u'      舊｜%s' % old.split(u'|')[3].strip()[:66])
    print(u'      新｜%s' % new.split(u'|')[3].strip()[:66])
adds = []
for num in missing:
    g = cards[num][u'grp']
    at = tail.get(g)
    if at is None:
        print(u'  ! 案例%s 所屬組未詳（%s），暫不插入' % (num, g[:16]))
        continue
    row = u'| **\u3014\u6848\u4f8b %s\u3015%s** | %s |%s|' % (
        num, cards[num][u'title'], cards[num][u'cite'] or u'\u5377\u6b20', cell3(num))
    adds.append((at, row))
    print(u'  ＋組『%s』末添：案例%s %s' % (g[:14], num, cards[num][u'title'][:18]))
if not APPLY:
    sys.exit(0)
n2 = []
emap = dict(edits)
addmap = {}
for at, row in adds:
    addmap.setdefault(at, []).append(row)
for i, l in enumerate(L):
    n2.append(emap.get(i, l))
    if i in addmap:
        n2.extend(addmap[i])
io.open(os.path.join(ROOT, NAME), 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(n2))
back = io.open(os.path.join(ROOT, NAME), encoding=u'utf-8').read().split(u'\n')
assert len(back) == len(L) + len(adds), u'行數等式不合（%d＋%d≠%d）' % (len(L), len(adds), len(back))
for _at, row in adds:
    assert row in set(back), u'回讀缺新行'
for i, new in edits.items():
    assert new in set(back), u'回讀缺改行 L%d' % (i + 1)
print(u'———— 已改 %d 行・添 %d 行・%d → %d 行・回讀相符' % (
    len(edits), len(adds), len(L), len(back)))
