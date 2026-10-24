# -*- coding: utf-8 -*-
"""274 輪・量①：新稿（附件之第一〜三章）入冊前之六面差分——只量不改，產出待治清單。

六面：甲 交付殘跡（第 6 目）・乙 黑話與代號（29）＋命題作『令』（26）＋無號指針（28）・
      丙 簡形（5）・丁 案例指針之號↔名（27 口徑）・戊 掛出處之逐字宣稱（23＋v39quote2 口徑）・
      己 章與節之形（合章後節次可達否，第 10 目）。
口徑名單**不兩抄**：黑話・代號・禁詞皆自 `_work/v39chk.py` 之源以 ast 取字面；引文判定逕用 `_tk.classify`。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r274probe.py
"""
import ast
import glob
import io
import os
import re
import sys
import contextlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, '_work'))
AP = os.path.join(os.path.expanduser(u'~'), u'.qoder', u'tmp',
                  u'C--Users-lionc-OneDrive-----------------', u'attachments',
                  u'e11d207e-a4f7-4a0e-9edb-3124ac9d8a4a',
                  u'fa89e70f-39b1-4bde-9002-a0548ff0653d.txt')
AL = io.open(AP, encoding=u'utf-8', errors=u'replace').read().split(u'\n')
A = u'\n'.join(AL)
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
BL = io.open(os.path.join(ROOT, NAME), encoding=u'utf-8').read().split(u'\n')
print(u'新稿 %d 行・%d 字（去空白）｜今冊 ch1-3 = L436〜1985（%d 行）' % (
    len(AL), len(re.sub(u'\\s', u'', A)), 1985 - 436 + 1))

CHK = io.open(os.path.join(ROOT, u'_work', u'v39chk.py'), encoding=u'utf-8').read()


def lit(name):
    m = re.search(u'%s = \\[((?:.|\\n)*?)\\n?\\]' % name, CHK)
    return ast.literal_eval(u'[' + m.group(1) + u']') if m else []


PROMPT, JARGON, CODES = lit('PROMPT'), lit('JARGON'), lit('CODES')
assert PROMPT and len(JARGON) >= 20 and len(CODES) >= 8, u'名單不可空'

# ── 甲・交付殘跡
print(u'\n甲・交付殘跡（第 6 目之詞 %d 枚）' % len(PROMPT))
for k in PROMPT:
    ln = [i + 1 for i, l in enumerate(AL) if k in l]
    if ln:
        print(u'   %-12s %2d 見  L%s' % (k, len(ln), u','.join(map(str, ln[:9]))))
BATCH = [(i + 1, l) for i, l in enumerate(AL)
         if l.startswith(u'# ') and (u'\u4ea4\u4ed8' in l or u'\u5b9a\u672c' in l)]
NARR = [(i + 1, l) for i, l in enumerate(AL) if l.startswith(u'### ') and any(
    k in l for k in (u'\u4ea4\u4ed8', u'\u5713\u6eff', u'\u5448\u8fad', u'\u9a57\u6536'))]
print(u'   批次 H1 %d 枚 %s' % (len(BATCH), [i for i, _ in BATCH]))
print(u'   交付型 H3 %d 枚 %s' % (len(NARR), [i for i, _ in NARR]))

# ── 乙・黑話／代號／命題作令／無號指針
print(u'\n乙・黑話與代號（29）・命題作令（26）・無號指針（28）')
for w in JARGON + CODES:
    ln = [i + 1 for i, l in enumerate(AL) if w in l]
    if ln:
        print(u'   %-10s %d 見 L%s' % (w, len(ln), u','.join(map(str, ln[:6]))))
LING = re.compile(u'(?:\\*\\*|\u3010)[^*\u3010\u3011\\n]{2,18}\u4ee4(?:\\*\\*|\u3011|\uff1a)')
print(u'   命題作『某某令』：%d 見 %s' % (sum(1 for l in AL if LING.search(l)),
      [i + 1 for i, l in enumerate(AL) if LING.search(l)][:6]))
NOREF = re.compile(u'\u3014(?:案例|補遺)·|\u3014(?:案例|補遺)\u3015|\u3014(?:案例|補遺)\\s+\u3014')
print(u'   無號〔案例·名〕形制：%d 見' % len(NOREF.findall(A)))

# ── 丙・簡形
with contextlib.redirect_stdout(io.StringIO()):
    import recordsimp
from _simpdict import MAP as SD
CORP = set()
for f in glob.glob(os.path.join(ROOT, u'原文', u'*.txt')):
    CORP |= set(io.open(f, encoding=u'utf-8', errors=u'ignore').read())
SIMP = (set(recordsimp.S) | set(u'\u4e24\u5f53\u5f3a\u968f\u65e7\u603b')
        | (set(SD) - {c for c in SD if c in CORP}))
hits = sorted({c for c in A if c in SIMP})
print(u'\n丙・簡形：%d 枚 ｜ %s' % (len(hits), u' '.join(
    u'U+%04X×%d' % (ord(c), A.count(c)) for c in hits)))
for c in hits[:12]:
    ln = [i + 1 for i, l in enumerate(AL) if c in l][:4]
    print(u'   U+%04X L%s' % (ord(c), ln))

# ── 丁・案例指針之號↔名（27 目口徑）
from difflib import SequenceMatcher
PUNC = re.compile(u'[\\s\u3000\uff0c\u3001\uff1b\uff1a\uff1f\uff01\u3002\u2014\\-\u300c\u300d\u300e\u300f'
                  u'\uff08\uff09\u3010\u3011\u3014\u3015\\[\\]\u00b7]')
_pl = lambda s: PUNC.sub(u'', s)


def _lcs(a, b):
    return SequenceMatcher(None, a, b, autojunk=False).find_longest_match(0, len(a), 0, len(b)).size


TIT = {}
for l in BL:
    m = re.match(u'^### 〔(案例|補遺) ([0-9]+)〕(.*)$', l)
    if m:
        TIT[(m.group(1), m.group(2))] = re.split(u'\u2014|--|\uff1a', m.group(3))[0]
PAT = re.compile(u'〔(案例|補遺) ?([0-9]+)〕([一-鿿]{3,14})')
ok = bad = soft = 0
print(u'\n丁・案例指針（對今冊卡題 %d 枚）' % len(TIT))
for i, l in enumerate(AL):
    for m in PAT.finditer(l):
        key = (m.group(1), m.group(2).zfill(2))
        nm = _pl(m.group(3))
        if key not in TIT:
            bad += 1
            print(u'   L%-5d 查無此卡：%s%s｜引名『%s』' % (i + 1, key[0], key[1], m.group(3)[:14]))
            continue
        own = _lcs(nm, _pl(TIT[key]))
        bo, bk = max((_lcs(nm, _pl(h)), k2) for k2, h in TIT.items() if k2 != key)
        if own >= 2:
            ok += 1
        elif bo >= 5:
            bad += 1
            print(u'   L%-5d 錯系：%s%s『%s』不合本卡『%s』而合 %s%s『%s』' % (
                i + 1, key[0], key[1], m.group(3)[:12], TIT[key][:12], bk[0], bk[1], TIT[bk][:12]))
        else:
            soft += 1
print(u'   中 %d・錯系／查無 %d・描述語不判 %d' % (ok, bad, soft))

# ── 戊・掛出處之逐字宣稱（v39quote2 之口徑）
with contextlib.redirect_stdout(io.StringIO()):
    import _tk
GATE, Q = _tk.SRC_STRICT, _tk.Q_RE
tally = {}
rows = []
for i, l in enumerate(AL):
    gates = [m.start() for m in GATE.finditer(l)]
    if not gates:
        continue
    for m in Q.finditer(l):
        if not any(g < m.start(1) for g in gates):
            continue
        v, _b = _tk.classify(m.group(1))
        k = v if not v.startswith(u'other') else u'other'
        tally[k] = tally.get(k, 0) + 1
        rows.append((i + 1, m.group(1), v))
print(u'\n戊・掛出處之逐字宣稱 %d 段｜命中 %d・他典 %d・不校 %d・未中 %d' % (
    len(rows), tally.get(u'hit', 0), tally.get(u'other', 0), tally.get(u'short', 0), tally.get(u'miss', 0)))
for r in rows:
    if r[2] == u'miss':
        print(u'   L%-5d 未中｜%s' % (r[0], r[1][:52]))

# ── 己・章與節之形
print(u'\n己・新稿 H1 %d 枚' % len([l for l in AL if l.startswith(u'# ')]))
for i, l in enumerate(AL):
    if l.startswith(u'# '):
        print(u'   L%-5d %s' % (i + 1, l[:44]))
seq = {}
for i, l in enumerate(AL):
    m = re.match(u'^### 第([一二三四五六七八九十]+)節', l)
    if m:
        seq.setdefault(m.group(1), []).append(i + 1)
print(u'   新稿『第N節』題：%s' % {k: [v[0]] and v for k, v in sorted(seq.items())})
cur = sorted({re.match(u'^### 第([一二三四五六七八九十]+)節', l).group(1)
              for l in BL[435:1985] if re.match(u'^### 第([一二三四五六七八九十]+)節', l)})
print(u'   今冊 ch1-3 之節序：%s' % cur)
print(u'   新稿非節題之 H3（提撕／總覽／宣告型）：%d 枚' % len([
    l for l in AL if l.startswith(u'### ') and not re.match(u'^### (第[一二三四五六七八九十]+節|閘門|導言)', l)]))
