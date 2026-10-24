# -*- coding: utf-8 -*-
"""272 輪立・第九尺『牙列矩陣』之負測：證此矩陣真能報欠，非以 rc=0 自賣。

三針：① 鈍針（把一目之植改为空寫）→ 該目須報『未逮』且退 1；
      ② 失錨（植法找不到落點）→ 須報『未植』且退 1；
      ③ 基線不綠（副本未跑先帶病）→ 須整盤作廢、報『基線不綠』並退 2。
口徑：改的是 `_work/r272tmpneg.py`（矩陣自身之副本），正本之冊一律不碰——跑前跑後較其 SHA。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r272neg.py
"""
import hashlib
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, u'_work')
TEETH = os.path.join(WORK, u'r272teeth.py')
TXT = io.open(TEETH, encoding=u'utf-8').read()
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
SRC = os.path.join(ROOT, NAME)
sha = lambda: hashlib.sha256(io.open(SRC, 'rb').read()).hexdigest()[:12]  # noqa: E731
env = dict(os.environ, PYTHONIOENCODING=u'utf-8')

CASES = [(u'鈍針', u"    L[i] += u'（迭代）'", u"    L[i] += u''", u'未逮', 1),
         (u'失錨', u"    L[i] += u'【安樂令】'", u"    repl(L, i, u'必無此錨_r272', u'X')", u'未植', 1),
         (u'病基', u"io.open(tmp_base, u'w', encoding=u'utf-8').write(u'\\n'.join(BASE))",
          u"io.open(tmp_base, u'w', encoding=u'utf-8').write(u'\\n'.join(BASE) + u'\\n解耦')",
          u'基線不綠', 2)]

h0 = sha()
bad = []
try:
    for tag, old, new, want, wish in CASES:
        assert TXT.count(old) == 1, u'%s｜植錨非一（%d 中）' % (tag, TXT.count(old))
        p = os.path.join(WORK, u'r272tmpneg.py')
        io.open(p, u'w', encoding=u'utf-8').write(TXT.replace(old, new))
        q = subprocess.run([sys.executable, u'-X', u'utf8', p], capture_output=True,
                           text=True, encoding=u'utf-8', env=env, cwd=ROOT)
        out = (q.stdout or u'').rstrip()
        row = [l for l in out.split(u'\n') if want in l]
        ok = (q.returncode == wish and want in out and not (q.stderr or u'').strip())
        bad.append((tag, want, wish, q.returncode, ok, (q.stderr or u'').strip()[:60],
                    (row[0].strip() if row else u'（無此行）')))
finally:
    p = os.path.join(WORK, u'r272tmpneg.py')
    if os.path.exists(p):
        os.remove(p)

for tag, want, wish, got, ok, err, row in bad:
    print(u'%-4s 期『%s』退%-2s｜實退 %-2s・%s・%s' % (tag, want, wish, got, u'✓' if ok else u'✗', row[:60]))
    if err:
        print(u'      stderr｜%s' % err[:120])
h1 = sha()
print(u'———— 負測三針：%s｜正本 SHA %s→%s %s' % (
    u'俱如所期' if not [x for x in bad if not x[4]] else u'有不如期', h1, h0,
    u'（未動）' if h0 == h1 else u'⚠ 正本被改！'))
sys.exit(1 if [x for x in bad if not x[4]] or h0 != h1 else 0)
