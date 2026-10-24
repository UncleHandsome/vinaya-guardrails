# -*- coding: utf-8 -*-
"""通器・換章三段式（274 立、275 汎用化）：新章段**先試跑、後入冊、可一步回退**。

用法：
  PYTHONIOENCODING=utf-8 python -X utf8 _work/v39swap.py tryrun <新章段> <起章> <迄章>
  PYTHONIOENCODING=utf-8 python -X utf8 _work/v39swap.py apply   <新章段> <起章> <迄章>
  PYTHONIOENCODING=utf-8 python -X utf8 _work/v39swap.py undo    <起章> <迄章>
口徑：① 起章之行必為『# 起章…』、迄章之行必為『# 迄章…』，新章段之末行不得含迄章；
      ② 組裝後以**五尺試跑通道**量之（v39chk・v39quote2・v39volchk・v39volrange・v39secref），紅者不換；
      ③ apply 先寫 `_work/swap.<起章>.bak` 並記舊 SHA；undo 即以該檔還原（再校 SHA 貼合）。
"""
import hashlib
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_work')
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'\u5217\u5370' not in q][0]
SRC = os.path.join(ROOT, NAME)
RULERS = (u'v39chk.py', u'v39quote2.py', u'v39volchk.py', u'v39volrange.py', u'v39secref.py')
env = dict(os.environ, PYTHONIOENCODING=u'utf-8')
MODE, ARG = sys.argv[1], sys.argv[2:]
if MODE == u'undo':
    a = ARG[0]
    bak = os.path.join(WORK, u'swap.%s.bak' % a)
    raw0 = io.open(bak, 'rb').read()
    io.open(SRC, 'wb').write(raw0)
    print(u'\u56de\u9000\u5b8c\u6210\uff5c%s\uff5cSHA %s' % (os.path.basename(bak),
                                                        hashlib.sha256(io.open(SRC, 'rb').read()).hexdigest()[:12]))
    raise SystemExit(0)

DRAFT, A0, Z0 = ARG[0], ARG[1], ARG[2]
nl = io.open(DRAFT, encoding=u'utf-8-sig').read().replace(u'\r\n', u'\n').rstrip(u'\n').split(u'\n')
cl = io.open(SRC, encoding=u'utf-8-sig').read().split(u'\n')
A = next(i for i, l in enumerate(cl) if l.startswith(u'# ' + A0))
Z = next(i for i, l in enumerate(cl) if l.startswith(u'# ' + Z0))
assert nl[0].startswith(u'# ' + A0), u'\u65b0\u7a3f\u9996\u884c\u975e\u8d77\u7ae0\uff1a%s' % nl[0][:20]
assert not any(l.startswith(u'# ' + Z0) for l in nl), u'\u65b0\u7a3f\u63c0\u5f9e\u9032\u4e86\u903e\u518a\u4e4b\u7ae0'
nH1 = [l for l in nl if l.startswith('# ')]
print(u'\u65b0\u7a3f %d \u884c\uff5cH1 %d \u679e\uff1a%s' % (len(nl), len(nH1), u'\u3001'.join(h[2:12] for h in nH1)))
TRIAL = cl[:A] + nl + cl[Z:]
tp = os.path.join(WORK, u'swap.trial.md')
io.open(tp, 'w', encoding=u'utf-8').write(u'\n'.join(TRIAL) + u'\n')
print(u'\u7d44\u88dd\uff5c\u6b63\u672c %d \u884c \u2212 \u65e7\u6bb5 %d \u884c\uff08L%d〜L%d\uff09\uff0b \u65b0\u6bb5 %d \u884c = %d \u884c' % (
    len(cl), Z - A, A + 1, Z, len(nl), len(TRIAL)))
assert TRIAL[:A] == cl[:A] and TRIAL[A + len(nl):] == cl[Z:], u'\u524d\u5f8c\u7db4\u4e0d\u7b49'
print(u'\u524d\u5f8c\u7db4\u9010\u5b57\u76f8\u7b49\u2014\u2014\u8d77\u7ae0\u4e4b\u524d\u8207\u903e\u518a\u4e4b\u5f8c\u4e00\u5b57\u672a\u52d5')
bad = 0
for tool in RULERS:
    q = subprocess.run([sys.executable, u'-X', u'utf8', os.path.join(WORK, tool), tp],
                       capture_output=True, text=True, encoding=u'utf-8', env=env, cwd=ROOT)
    out = (q.stdout or u'').rstrip().split(u'\n')
    err = (q.stderr or u'').strip()
    if q.returncode or err:
        bad += 1
        print(u'\u2717 %-14s rc=%d\uff5c%s' % (tool, q.returncode, out[-1][:88] if out else u''))
        for l in out:
            if u'\u2717' in l or u'FAIL' in l or u'\u4e0d\u5408' in l:
                print(u'     ' + l.strip()[:120])
        if err:
            print(u'     stderr\uff5c%s' % err[:150])
    else:
        print(u'\u2713 %-14s %s' % (tool, out[-1][:92] if out else u''))
if bad and MODE == u'apply':
    print(u'\u2014\u2014 \u8a66\u8dd1\u6709\u7d05 %d \u652f\uff0c\u4e0d\u5f97\u5165\u518a' % bad)
    raise SystemExit(1)
if MODE == u'apply':
    raw = io.open(SRC, 'rb').read()
    io.open(os.path.join(WORK, u'swap.%s.bak' % A0), 'wb').write(raw)
    io.open(SRC, 'w', encoding=u'utf-8').write(u'\n'.join(TRIAL) + u'\n')
    b2 = io.open(SRC, 'rb').read()
    print(u'\u5165\u518a\uff5cSHA %s \u2192 %s\uff5c%d \u884c\uff5c%s B\uff5c\u56de\u9000\uff1apy _work/v39swap.py undo %s %s' % (
        hashlib.sha256(raw).hexdigest()[:12], hashlib.sha256(b2).hexdigest()[:12],
        b2.decode(u'utf-8').count(u'\n') + 1, len(b2), A0, Z0))
else:
    print(u'\u2014\u2014 \u8a66\u8dd1%s\uff5c\u6b63\u672c\u672a\u52d5' % (u'\u5168\u7da0' if not bad else u'\u6709\u7d05'))
