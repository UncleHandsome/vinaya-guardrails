# -*- coding: utf-8 -*-
"""第 224 輪新軸 r224now 之負測（留檔）：五路分擊其口徑，各中其目。
   主檔唯讀——以 TKSRC 指副本，副本用完即除，並斷主檔哈希前後相同（第 223 輪之誡）。"""
from __future__ import unicode_literals
import hashlib
import io
import os
import subprocess
import sys

NL = chr(10)
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MD = u'ver38四分律_起心動念心智分析框架_修正版.md'
NEW = u'_work/_r224neg.md'
raw = io.open(MD, encoding=u'utf-8').read()
H0 = hashlib.sha256(raw.encode(u'utf-8')).hexdigest()
BASE = raw.split(NL)
CELL = 10987          # 0 基：L10988 之表行
ROW11145 = 11144      # 0 基：L11145（第二張現行列之資料行）


def run(lines, want_rc, want_in, tag):
    io.open(NEW, u'w', encoding=u'utf-8', newline=NL).write(NL.join(lines))
    env = dict(os.environ)
    env[u'TKSRC'] = NEW
    env[u'PYTHONIOENCODING'] = u'utf-8'
    p = subprocess.Popen([sys.executable, u'-X', u'utf8', u'_work/r224now.py'],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    out = p.communicate()[0].decode(u'utf-8', u'replace')
    rc = p.returncode
    ok = (rc == want_rc) and (want_in is None or want_in in out)
    print(u'%-34s rc=%d（期 %d）%s｜%s' % (tag, rc, want_rc, u'中' if ok else u'不中',
                                          out.strip().split(NL)[-1][:78]))
    return ok


cases = []
cases.append(run(list(BASE), 0, None, u'⓪ 自建淨本（陰性基準）'))

a = list(BASE)
a[CELL] = a[CELL].replace(u'**第一節　歷史現場與立法本懷**', u'**第一節　立法本懷與唯一判準**')
assert a[CELL] != BASE[CELL]
cases.append(run(a, 1, u'立法本懷與唯一判準', u'① 植一格舊題（當報・中其目）'))

b = list(BASE)
cols = [c.strip() for c in b[ROW11145].strip().strip(u'|').split(u'|')]
cols[1] = u'*（併入第一節）*'
b[ROW11145] = u'| ' + u' | '.join(cols) + u' |'
cases.append(run(b, 0, None, u'② 現行列植說明格（形不校・勿報）'))

c = list(BASE)
cols = [x.strip() for x in c[ROW11145].strip().strip(u'|').split(u'|')]
cols[1] = u'**第二章　樹根與枝幹：根本心與六大領域**'
c[ROW11145] = u'| ' + u' | '.join(cols) + u' |'
cases.append(run(c, 0, None, u'③ 現行列植合法今題（對者勿報）'))

d = list(BASE)
cols = [x.strip() for x in d[ROW11145].strip().strip(u'|').split(u'|')]
cols[1] = u'**第玖玖節　憑空之題**'
d[ROW11145] = u'| ' + u' | '.join(cols) + u' |'
cases.append(run(d, 1, u'憑空之題', u'④ 現行列植憑空題（當報）'))

if os.path.exists(NEW):
    os.remove(NEW)
H1 = hashlib.sha256(io.open(MD, encoding=u'utf-8').read().encode(u'utf-8')).hexdigest()
print(u'主檔哈希前後相同：%s（副本已除：%s）' % (u'是' if H0 == H1 else u'否（大害！）',
                                                 u'是' if not os.path.exists(NEW) else u'否'))
print(u'負測：%s' % (u'五路俱中' if all(cases) and H0 == H1 else u'有路不中——器無牙'))
sys.exit(0 if (all(cases) and H0 == H1) else 1)
