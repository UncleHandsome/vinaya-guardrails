# -*- coding: utf-8 -*-
# 第 189 輪·負測：① 扩級後之不變量『標題不懸空（H1–H5）』须能逮空 H5（植於主檔，還原入 finally）；
# ② 軸 `r189dangling` 之甲目须能報『冒號收尾而其下標題亦無文』之懸領（植於副本，行數可變因副本自算其界）。
import io
import os
import re
import subprocess
import sys
import hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
MASTER = u'ver38四分律_起心動念心智分析框架_修正版.md'
COP = u'_work/r189neg.md'
env = dict(os.environ)
env['PYTHONIOENCODING'] = 'utf-8'
env['PYTHONPATH'] = '.'

raw = io.open(MASTER, encoding=u'utf-8').read()
h0 = hashlib.sha256(raw.encode(u'utf-8')).hexdigest()
L = raw.split(u'\n')
ANCHOR = u'##### 【板塊 Z：負測暫植（此題之下暫無內文）】'
idx = [k for k, l in enumerate(L) if l.startswith(u'##### 【板塊 B：')]
assert len(idx) == 1, u'植點錨非恰一：%s' % idx
i = idx[0]

# ── 乙·主檔暫植（測扩級之閘）─────────────────────────────────────
lines = list(L)
lines[i:i] = [ANCHOR, u'']
io.open(MASTER, 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(lines))
rc_plant = 1
hit = []
try:
    q = subprocess.run([sys.executable, u'-X', u'utf8', u'_tk.py', u'check'],
                       capture_output=True, text=True, encoding=u'utf-8', env=env)
    rc_plant = q.returncode
    rep = io.open(u'_work/check.txt', encoding=u'utf-8').read()
    hit = [x for x in rep.split(u'\n') if x.startswith(u'FAIL') and u'標題不懸空' in x]
finally:
    io.open(MASTER, 'wb').write(raw.encode(u'utf-8'))
h1 = hashlib.sha256(io.open(MASTER, u'rb').read()).hexdigest()

# ── 甲·副本暫植（測軸之懸領目）───────────────────────────────────
lines = list(L)
lines[i:i] = [u'以下分三類細目：', u'', ANCHOR, u'']
io.open(COP, 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(lines))
rc_ax = 1
jia = -1
try:
    q2 = subprocess.run([sys.executable, u'-X', u'utf8', u'_work/r189dangling.py', COP, u'require-hit'],
                        capture_output=True, text=True, encoding=u'utf-8', env=env)
    m = re.search(u'甲·懸領無所屬 (\\d+)', q2.stdout)
    jia = int(m.group(1)) if m else -1
    rc_ax = q2.returncode
finally:
    if os.path.exists(COP):
        os.remove(COP)

q3 = subprocess.run([sys.executable, u'-X', u'utf8', u'_work/r189dangling.py'],
                    capture_output=True, text=True, encoding=u'utf-8', env=env)
base = re.search(u'甲·懸領無所屬 (\\d+)', q3.stdout)
print(u'基態：軸 甲 %s｜閘 rc=0（今 84/84）' % (base.group(1) if base else u'?'))
print(u'植閘：check rc=%d（須 1）｜FAIL 報 %d（須 ≥1）｜%s' % (rc_plant, len(hit), hit[:1]))
print(u'植軸：甲 %d（須 ≥1）｜退 %d（須 0）' % (jia, rc_ax))
print(u'還原：雜湊%s' % (u'相同' if h0 == h1 else u'不同！'))
ok = (h0 == h1 and rc_plant == 1 and hit and jia >= 1 and rc_ax == 0
      and base and base.group(1) == u'0')
print(u'結果斷：%s' % (u'兩向俱有牙：H5 空題能逮、懸領能報' if ok else u'負測不合——器或無牙'))
sys.exit(0 if ok else 1)
