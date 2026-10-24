# -*- coding: utf-8 -*-
"""257 輪・迎回器：把 256 輪降為『律意：』之 24 段，自 ver38 完卡之◎原典（逐字已證）求供體而迎回真逐字。

法：（一）供體須即自證——取 ver38 該案『◎原典』之 「…」 全段，送 `_tk.classify`，非 hit 者不候；
    （二）對位以歸一文本相似度（difflib ratio）定之，並列 ver39 現引之卷次與供體之卷次，兩者不合者標『卷異』；
    （三）落檔須錨點恰中一次、行數不動、寫後回讀；迎回之段仍帶「律意：」於其行首者即斥（不留雙重標記）。
只報；apply 方改（且須經目視此報）。

用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/v39qback.py [min_ratio]
"""
import difflib
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (ROOT, os.path.join(ROOT, u'_work')):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import _tk                                                     # noqa: E402

MINR = float(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].replace('.', '').isdigit() else 0.30
APPLY = u'apply' in sys.argv
_only = os.environ.get(u'ONLY', u'')
ALLOW = None if not _only else set(x.strip() for x in _only.split(u',') if x.strip())
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
OLD = [q for q in os.listdir(ROOT) if q.startswith(u'ver38') and q.endswith(u'.md')][0]
NL = _tk.MAIN_LINES
OL = io.open(os.path.join(ROOT, OLD), encoding=u'utf-8-sig').read().split(u'\n')

CR = re.compile(u'^####\\s*〔(遮|開|僧)(\\d+)〕\\s*(.*)$')
Q = re.compile(u'\u300c([^\\u300c\\u300d]+)\\u300d')
VOL = re.compile(u'卷\\s*([0-9一二三四五六七八九十百]+)')
BRACKET_CODE = re.compile(u'\\[[^\\]\\s]{1,3}[*\\/][^\\]\\s]{1,3}\\]')    # CBETA 合字：不入印面


def printable(q):
    """供體之引文須『可直接上印面』：無合字、無套引號、『』成對、無 markdown 星號。"""
    return (not BRACKET_CODE.search(q) and u'\u300c' not in q and u'\u300d' not in q
            and q.count(u'\u300e') == q.count(u'\u300f') and u'*' not in q)

donors = []          # (案號, 案題, 卷, 引文, 歸一引文)
lab = ttl = None
in_o = False
cite_vol = u''
for i, l in enumerate(OL):
    m = CR.match(l)
    if m:
        lab, ttl, in_o = m.group(1) + m.group(2), m.group(3)[:22], False
        cite_vol = u''
        continue
    if l.strip().startswith(u'◎原典'):
        in_o = True
        continue
    if in_o and (l.strip() == u'---' or l.startswith(u'####')):
        in_o = False
        continue
    if not in_o:
        continue
    v = VOL.search(l)
    if v:
        cite_vol = v.group(1)
    for q in Q.findall(l):
        if printable(q) and _tk.classify(q)[0] in (u'hit', u'skip'):
            donors.append((lab, ttl, cite_vol, q, _tk.norm(q)))
print(u'供體：ver38 已證原典引文 %d 段（案 %d 枚）｜門檻 ratio≥%.2f' % (
    len(donors), len({d[0] for d in donors}), MINR))

HEAD = re.compile(u'^#### 【律典原典】\\s*$')
CARD = re.compile(u'^### 〔(案例|補遺) (\\d+)〕')
targets = []
cur = None
sec = None
for i, l in enumerate(NL):
    m = CARD.match(l)
    if m:
        cur = u'%s%s' % (m.group(1), m.group(2))
    if HEAD.match(l):
        sec = i
    if u'律意：' in l and sec is not None:
        vol = VOL.search(u' '.join(NL[sec:i + 1]))
        body = l.split(u'律意：', 1)[1]
        targets.append((cur, i, vol.group(1) if vol else u'-', body))
print(u'待迎回：%d 段（卡 %d 枚）\n' % (len(targets), len({t[0] for t in targets})))

plan = {}
for card, idx, vol, body in targets:
    bn = _tk.norm(body)
    scored = []
    for lab, ttl, dvol, q, qn in donors:
        r = difflib.SequenceMatcher(None, bn, qn, autojunk=False).ratio()
        if r >= MINR:
            scored.append((r, lab, ttl, dvol, q))
    scored.sort(reverse=True)
    if not scored:
        print(u'● %-8s L%-5d 現卷%s・無合供（below %.2f）' % (card, idx + 1, vol, MINR))
        continue
    top = scored[0]
    flag = u'' if (vol == u'-' or top[3] == vol or not top[3]) else u'⚠卷異(%s≠%s)' % (vol, top[3])
    print(u'◐ %-8s L%-5d 現卷%-4s 供 %-5s%-6s r%.2f 供卷%s｜%s' % (
        card, idx + 1, vol, top[1], top[2], top[0], top[3], flag))
    print(u'      現：%s' % body[:56])
    print(u'      候：%s' % top[4][:56])
    if len(scored) > 1:
        print(u'      次：%s r%.2f' % (scored[1][1], scored[1][0]))
    if not flag and top[0] >= MINR and (ALLOW is None or card in ALLOW):
        plan[idx] = top[4]

print(u'———— 可迎回 %d 段（無卷異者）・涉行 %d' % (len(plan), len(plan)))
if not APPLY:
    sys.exit(0)
# 迎回之法：真逐字另立一行掛「」，原『律意：』之攝述仍留——一字不刪，只添所缺之律文
ins = {}
for k, q in plan.items():
    assert u'律意：' in NL[k], u'落點非律意之行 L%d' % (k + 1)
    assert (u'\u5df7' in NL[k - 1]) or (u'\u300a' in NL[k - 1]), u'落點上一行非卷引 L%d' % (k + 1)
    ins[k] = u'> \u300c%s\u300d' % q
n2 = []
for i, l in enumerate(NL):
    if i in ins:
        n2.append(ins[i])
    n2.append(l)
assert len(n2) == len(NL) + len(ins), u'行數之等式不合'
io.open(os.path.join(ROOT, NAME), 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(n2))
back = io.open(os.path.join(ROOT, NAME), encoding=u'utf-8').read().split(u'\n')
assert len(back) == len(n2), u'回讀行數不合'
bset = set(back)
for k in ins:
    assert ins[k] in bset, u'回讀缺所迎之行（原 L%d）' % (k + 1)
print(u'———— 已迎回落檔 %d 行（添 %d 行・%d 行 → %d 行）・回讀相符' % (
    len(plan), len(ins), len(NL), len(back)))
