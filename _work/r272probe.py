# -*- coding: utf-8 -*-
"""272 輪・量一：目數之自對合＋『哪幾目從未負測』。

法源：檔上之誡——**每立一目必先植其病證其能紅，方准計入綠數**；又『目數即宣稱，宣稱須有尺』。
今以此為尺：① 印出之 N 須等於 `chk()` 實際註冊之條數（含 except 分支之同名保底，去重）；
   ② 目名不得重複（重名即兩目共號，FAIL 時不知誰紅）；
   ③ 每一目名須在**至少一支負測器**（`_work/r*neg*.py`）中露面，否則該目『無牙』——列入欠測帳。
用法：python -X utf8 _work/r272probe.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, u'_work')
SRC = io.open(os.path.join(WORK, u'v39chk.py'), encoding=u'utf-8-sig').read()
LINES = SRC.split(u'\n')

names = re.findall(u"chk\\(u'([^']+)'", SRC) + re.findall(u'chk\\(u"([^"]+)"', SRC)
print(u'chk() 呼叫 %d 次・去重後目名 %d 個' % (len(names), len(set(names))))
dup = sorted({n for n in names if names.count(n) > 1})
print(u'重名：%s' % (u'・'.join(dup) or u'無'))
for d in dup:
    print(u'   重名目：%s（%d 次）' % (d, names.count(d)))

print(u'\n── 逐目（去重後之順序）──')
uniq = []
for n in names:
    if n not in uniq:
        uniq.append(n)
NEG = []
for f in sorted(os.listdir(WORK)):
    if (f.startswith(u'r') and u'neg' in f and f.endswith(u'.py')) or f == u'r255neg.py':
        NEG.append((f, io.open(os.path.join(WORK, f), encoding=u'utf-8-sig').read()))
print(u'負測器 %d 支：%s' % (len(NEG), u' '.join(f for f, _ in NEG)))
print()
toothless = []
for n in uniq:
    key = re.sub(u'（.*?）', u'', n).strip()
    hits = [f for f, t in NEG if key and (key in t or key[:8] in t)]
    if not hits:
        toothless.append(n)
    print(u'  %-46s %s' % (n[:46], u'・'.join(hits) or u'⚠ 無負測'))
print(u'\n——— 目 %d・無牙 %d：%s' % (len(uniq), len(toothless), u'、'.join(x[:14] for x in toothless)))
