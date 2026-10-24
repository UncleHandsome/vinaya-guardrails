# -*- coding: utf-8 -*-
"""259 輪・語料直取器：正文【律典原典】內只剩『律意：』而全無逐字可證之卡，逐句回語料求其真文。

與 `_work/v39qback.py`（供體＝ver38 完卡）相補：此器之供體是**語料本身**。
法（六道閘，缺一不候）：
  一・唯取【律典原典】欄・其內**全無已證 「」 段**之卡（已證者不復動，免生兩重宣稱）；
  二・以『律意』之文按句（。！？……）切段，段長十字以上者方求；
  三・對齊器 `_work/v39align`（探點四路・覆蓋閘預設 0.70・跨度相似閘 0.72），候選須 `_tk.classify` 自證；
  四・候選須**印面可用**（無合字『[x*y]』・無套引號・『』成對・無 `*`）；
  五・候選之長不得逾原句 2.2 倍（防吞他文），且須含原句之稀有長錨（≥8 字連語）——防錯拾套語；
  六・諸句候選依原序綴以『……』成一行，**只報並落 `_work/_qcorpus.json` 待人裁**；apply 讀此檔，改其所載者從其改。
落檔之法與迎回器同：真逐字另立一行掛「」，原『律意：』攝述仍留（一字不刪）。

用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/v39qcorpus.py            # 求候選・寫賬
      （目視 `_work/_qcorpus.json`，删其不可者、改其可改者）
      PYTHONIOENCODING=utf-8 python -X utf8 _work/v39qcorpus.py apply      # 按賬落檔
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (ROOT, os.path.join(ROOT, u'_work')):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import _tk                                                     # noqa: E402
import v39align                                                # noqa: E402

APPLY = u'apply' in sys.argv
MINCOV = float(os.environ.get(u'MINCOV', u'0.70'))
ACC = os.path.join(ROOT, u'_work', u'_qcorpus.json')
LINES = _tk.MAIN_LINES
CARD = re.compile(u'^### 〔(案例|補遺) (\\d+)〕')
HEAD = re.compile(u'^#### 【律典原典】\\s*$')
STOP = re.compile(u'^(#{1,6} |---\\s*$)')
Q = re.compile(u'\u300c([^\\u300c\\u300d]+)\\u300d')
SENT = re.compile(u'[^。！？\\u2026]+')

cards = []
i = 0
cur = None
while i < len(LINES):
    m = CARD.match(LINES[i])
    if m:
        cur = u'%s%s' % (m.group(1), m.group(2))
    if not HEAD.match(LINES[i]):
        i += 1
        continue
    j = i + 1
    quotes, lvline = [], None
    while j < len(LINES) and not STOP.match(LINES[j]):
        if u'律意：' in LINES[j] and lvline is None:
            lvline = j
        for q in Q.findall(LINES[j]):
            quotes.append(q)
        j += 1
    if cur and lvline is not None and not any(_tk.classify(q)[0] in (u'hit', u'skip') for q in quotes):
        cards.append((cur, i, lvline, LINES[lvline].split(u'律意：', 1)[1]))
    i = j

print(u'待求之卡：%d（其【律典原典】全無已證之 「」 段）' % len(cards))
book = {}
for card, sec, lv, body in cards:
    props = []
    for s in SENT.findall(body):
        n = _tk.norm(s)
        if len(n) < 10:
            continue
        r = v39align.realign(n, mincov=MINCOV)
        if not r:
            continue
        cand = r[2]
        if (_tk.classify(cand)[0] not in (u'hit', u'skip') or u'[' in cand or u'*' in cand
                or u'\u300c' in cand or cand.count(u'\u300e') != cand.count(u'\u300f')
                or len(_tk.norm(cand)) > len(n) * 2.2):
            continue
        shared = [n[k:k + 8] for k in range(0, max(1, len(n) - 7))
                  if len(n[k:k + 8]) >= 8 and k + 8 <= len(n) and n[k:k + 8] in _tk.norm(cand)]
        if not shared:
            continue
        rarest = min(shared, key=lambda g: _tk.VINAYA.count(g))
        if _tk.VINAYA.count(rarest) > 3:                    # 所共者唯套語（遍處皆是）即為錯拾
            continue
        props.append({u'sent': s.strip(), u'quote': cand, u'cov': round(r[0], 3)})
    book[card] = {u'line': lv + 1, u'body': body, u'props': props}
    print(u'◈ %-8s L%-5d 得 %d/%d 句' % (card, lv + 1, len(props), len(SENT.findall(body))))
    for p in props:
        print(u'      句｜%s' % p[u'sent'][:34])
        print(u'      候｜%s（cov%.2f）' % (p[u'quote'][:66], p[u'cov']))

if not APPLY:
    json.dump(book, io.open(ACC, 'w', encoding=u'utf-8'), ensure_ascii=False, indent=1)
    print(u'———— 賬落 %s（目視删改後再加 apply）' % os.path.relpath(ACC, ROOT))
    sys.exit(0)
assert os.path.exists(ACC), u'無賬可落'
acc = json.load(io.open(ACC, encoding=u'utf-8'))
INSERTS, skip = [], []
for card, sec, lv, body in cards:
    ent = acc.get(card)
    if not ent or not ent.get(u'props'):
        skip.append((card, u'賬內無候選'))
        continue
    assert lv == ent[u'line'] - 1, u'落點已位移（賬 %s・今 %d）' % (ent[u'line'], lv + 1)
    quotes = list(dict.fromkeys(p[u'quote'] for p in ent[u'props']))   # 同句重出者只留一次
    bad = [q for q in quotes
           if _tk.classify(q)[0] not in (u'hit', u'skip') or u'[' in q or u'\u300c' in q]
    if bad:
        skip.append((card, u'賬內之候今已不可證'))
        continue
    INSERTS.append((lv, u'> \u300c%s\u300d' % u'……'.join(quotes)))
for c, why in skip:
    print(u'  ! %-8s %s' % (c, why))
n2 = list(LINES)
for pos, line in sorted(INSERTS, reverse=True):
    n2.insert(pos, line)
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
io.open(os.path.join(ROOT, NAME), 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(n2))
back = io.open(os.path.join(ROOT, NAME), encoding=u'utf-8').read().split(u'\n')
assert len(back) == len(LINES) + len(INSERTS), u'行數等式不合（%d＋%d≠%d）' % (
    len(LINES), len(INSERTS), len(back))
bset = set(back)
for pos, line in INSERTS:
    assert line in bset, u'回讀缺行'
print(u'———— 已落檔：添 %d 行・舍 %d 卡（%d → %d 行）・回讀相符' % (
    len(INSERTS), len(skip), len(LINES), len(back)))
