# -*- coding: utf-8 -*-
"""261 輪・語料列句器（以號選取，不落一字 CJK 於參數）：
先自靶卡之『律意』文中取**稀有多字窗**（語料見數 ≤6）為錨，把語料中含錨之整句（依 。！？ 為界）
連同**歸一偏移**逐號列出；人唯以號數選之（PICKS），apply 時自語料原位複製該句 → 自證逐字 → 掛 「」 入卡。

用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r261list.py            # 列句供選
      PYTHONIOENCODING=utf-8 python -X utf8 _work/r261list.py apply      # 落 PICKS 所選之號
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
import v39align                                                # noqa: E402

APPLY = u'apply' in sys.argv
CARDS = (u'25', u'31')
PICKS = {u'25': (8,)}                     # 卡：所選之句號（案例31 無淨候，如實不落）
BOUND = u'。！？'
LINES = _tk.MAIN_LINES
CARD = re.compile(u'^### 〔案例 (\\d+)〕')
HEAD = re.compile(u'^#### 【律典原典】\\s*$')
STOP = re.compile(u'^(#{1,6} |---\\s*$)')
SENT = re.compile(u'[^。！？……]+')
Q = re.compile(u'\u300c([^\u300c\u300d]+)\u300d')


def lv_of(num):
    i = next(k for k, l in enumerate(LINES) if CARD.match(l) and CARD.match(l).group(1) == num)
    j = next(k for k in range(i, len(LINES)) if HEAD.match(LINES[k]))
    k = j + 1
    while k < len(LINES) and not STOP.match(LINES[k]):
        if u'\u5f8b\u610f\uff1a' in LINES[k]:
            return k, LINES[k].split(u'\u5f8b\u610f\uff1a', 1)[1]
        if Q.search(LINES[k]):
            return k, None                                   # 已有引號者不復動
        k += 1
    return None, None


def windows(s):
    n = _tk.norm(s)
    out = []
    for w in (6, 5, 4):
        for i in range(0, max(1, len(n) - w)):
            g = n[i:i + w]
            if len(g) == w and _tk.VINAYA.count(g) <= 6:
                out.append(g)
    return out


sent_no = 0
cands = {}
for num in CARDS:
    lv, body = lv_of(num)
    if body is None:
        print(u'案例%s：原典欄已有已證之 「」 段，不復動' % num)
        continue
    ws = windows(body)
    print(u'◐◐ 案例%s（律意行 L%s・稀窗 %d 枚）' % (num, (lv + 1) if lv else u'-', len(ws)))
    got, seen = [], set()
    for w in ws:
        for fi, (fn, raw, nt, nm) in enumerate(v39align.CORPUS):
            p = nt.find(w)
            while p >= 0:
                a, z = nm[p], nm[p + len(w) - 1]
                lo = max(raw.rfind(b, 0, a) for b in BOUND)
                lo = lo + 1 if lo >= 0 else 0
                hi = min([raw.find(b, z) for b in BOUND if raw.find(b, z) >= 0] or [len(raw) - 1])
                sen = raw[lo:hi + 1].strip().replace(u'\n', u'')
                sen = sen.replace(u'\u300c', u'\u300e').replace(u'\u300d', u'\u300f')
                key = (fi, sen)
                if key not in seen and sen and len(_tk.norm(sen)) >= 12:
                    seen.add(key)
                    got.append((fi, a, hi + 1, sen, w))
                p = nt.find(w, p + 1)
                if len(got) > 40:
                    break
            if len(got) > 40:
                break
    for idx, (fi, a, b, sen, w) in enumerate(got, 1):
        mark = u'■' if (num in PICKS and idx in PICKS[num]) else u'□'
        print(u'   %s [%d] 檔%d・%d–%d・錨%s｜%s' % (mark, idx, fi, a, b, w, sen[:120]))
    cands[num] = (lv, got)

if not APPLY:
    sys.exit(0)
n2 = list(LINES)
ins = 0
for num in CARDS:
    lv, got = cands.get(num, (None, []))
    if lv is None:
        continue
    quotes = []
    for idx in PICKS.get(num, ()):
        if not (1 <= idx <= len(got)):
            raise SystemExit(u'案例%s 句號 %d 越界（1–%d）' % (num, idx, len(got)))
        fi, _a, _b, sen, _w = got[idx - 1]
        if _tk.classify(sen)[0] not in (u'hit', u'skip'):
            raise SystemExit(u'案例%s 第 %d 號今不可證' % (num, idx))
        if u'[' in sen or u'*' in sen or u'\u300c' in sen or sen.count(u'\u300e') != sen.count(u'\u300f'):
            raise SystemExit(u'案例%s 第 %d 號非印面可用' % (num, idx))
        quotes.append(sen)
    if not quotes:
        continue
    line = u'> \u300c%s\u300d' % u'\u2026\u2026'.join(quotes)
    assert u'\u5f8b\u610f\uff1a' in n2[lv], u'落點已非律意行（案例%s）' % num
    n2.insert(lv, line)
    ins += 1
assert ins, u'PICKS 為空，無可落'
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'\u5217\u5370' not in q][0]
io.open(os.path.join(ROOT, NAME), 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(n2))
back = io.open(os.path.join(ROOT, NAME), encoding=u'utf-8').read().split(u'\n')
assert len(back) == len(LINES) + ins, u'行數等式不合'
print(u'———— 已落 %d 卡・添 %d 行・%d → %d 行・回讀相符' % (
    ins, ins, len(LINES), len(back)))
