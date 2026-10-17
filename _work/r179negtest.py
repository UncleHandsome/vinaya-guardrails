# -*- coding: utf-8 -*-
# 第 179 輪 `_work/syncchk.py` 之負測：植一行須逮（正向）、削一行須逮（反向）、不改須淨。
# 四份中介檔（full print/screen ＋ slim print/screen）各自比較，故一行之植／削當報 4 次。
import io
import os
import re
import subprocess
import sys

MASTER = u'ver38四分律_起心動念心智分析框架_修正版.md'
ANCH = u'此非苛求，乃二論之分際'          # 167 輪所補之印面橋句（L720；校勘記同語者屬底冊不預）
NEW = u'負測植入之印面新行——第 179 輪 syncchk 之牙，不入正式檔。'
TMP_F = u'_work/_syncneg_fwd.md'
TMP_R = u'_work/_syncneg_rev.md'
N = 4

lines = io.open(MASTER, encoding=u'utf-8').read().split(u'\n')
cand = [l for l in lines if ANCH in l]
assert len(cand) == 2, u'含錨語之行非二（印面一、校勘記一）：%d' % len(cand)
FULL = [l for l in cand if l.startswith(ANCH)][0]        # 印面之橋句以全形取（校勘記之引稱形不同）
hits = [i for i, l in enumerate(lines) if l == FULL]
assert len(hits) == 1, u'全行錨非恰一：%s' % hits
k = hits[0]

io.open(TMP_F, 'w', encoding=u'utf-8', newline=u'\n').write(
    u'\n'.join(lines[:k + 1] + [NEW] + lines[k + 1:]))
io.open(TMP_R, 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(lines[:k] + lines[k + 1:]))

env = dict(os.environ, PYTHONIOENCODING=u'utf-8')
res = {}
for tag, path in [(u'對照', MASTER), (u'植一行', TMP_F), (u'削一行', TMP_R)]:
    p = subprocess.run([sys.executable, u'-X', u'utf8', u'_work/syncchk.py', path],
                       capture_output=True, text=True, encoding=u'utf-8', env=env)
    out = p.stdout
    f = sum(int(x) for x in re.findall(u'正向缺 (\\d+)', out))
    r = sum(int(x) for x in re.findall(u'反向幽 (\\d+)', out))
    res[tag] = (p.returncode, f, r)
    print(u'%-8s rc=%d｜正向缺 %d｜反向幽 %d' % (tag, p.returncode, f, r))

ok = (res[u'對照'] == (0, 0, 0)
      and res[u'植一行'][1] == N and res[u'植一行'][2] == 0
      and res[u'削一行'][2] == N and res[u'削一行'][1] == 0)
for fp in (TMP_F, TMP_R):
    os.remove(fp)
print(u'結果斷：%s（對照 0/0｜植入須正向 %d、反向 0｜削除須反向 %d、正向 0；實際 %s）' % (
    u'器有牙，三測俱中' if ok else u'負測不合——器無牙或口徑過寬', N, N,
    u'；'.join(u'%s=%s' % (t, res[t]) for t in res)))
sys.exit(0 if ok else 1)
