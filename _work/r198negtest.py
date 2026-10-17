# -*- coding: utf-8 -*-
# 第 198 輪·負測：跑批器須逮『未列之軸』與『軸之退出碼非零』兩路，並如常放行正常態。
# 植病只用一支假軸與名冊之暫改，`finally` 必還原；不動主檔、不動他軸。
import io
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DUMMY = u'_work/r998drift.py'
REG = u'_work/_axes.txt'
env = dict(os.environ)
env['PYTHONIOENCODING'] = 'utf-8'

STUB = (u'# -*- coding: utf-8 -*-\n"""r998drift.py —— 假軸（負測用・待診）。"""\n'
        u'import sys\nsys.exit(1)\n')

reg0 = io.open(REG, encoding='utf-8').read()


def bat(*args):
    q = subprocess.run([sys.executable, u'-X', u'utf8', u'_work/battery.py'] + list(args),
                       capture_output=True, text=True, encoding='utf-8', errors='replace', env=env)
    return q.returncode, q.stdout


fails = []
try:
    io.open(DUMMY, 'w', encoding='utf-8', newline=u'\n').write(STUB)
    rc, out = bat('--list')
    hit = u'r998drift' in out
    print(u'① 未列之軸 → 漂移點名：%s｜退 %d（須 1）' % (u'中' if hit else u'不中', rc))
    if not (hit and rc == 1):
        fails.append(u'漂移未逮')

    io.open(REG, 'w', encoding='utf-8', newline=u'\n').write(reg0 + u'r998drift\n')
    rc, out = bat()
    hit2 = u'BAD r998drift' in out and rc == 1
    print(u'② 入冊而軸自敗 → 列名退 1：%s｜退 %d' % (u'中' if hit2 else u'不中', rc))
    if not hit2:
        fails.append(u'rc 路未逮')
finally:
    io.open(REG, 'w', encoding='utf-8', newline=u'\n').write(reg0)
    if os.path.exists(DUMMY):
        os.remove(DUMMY)

rc, out = bat('--list')
back = (rc == 0 and u'漂移 0' in out)
print(u'③ 還原後 → 冊淨漂移零：%s｜退 %d' % (u'中' if back else u'不中', rc))

# ④ 記號表之牙（第 199 輪擴）：升閘之軸不自稱『待診』，若記號表只認待診／長駐則恰好漏網
GATE = u'_work/r999gate.py'
io.open(GATE, 'w', encoding='utf-8', newline=u'\n').write(
    u'# -*- coding: utf-8 -*-\n"""r999gate.py —— 假升閘軸（負測用・第 999 輪立）。"""\n'
    u'import sys\nsys.exit(0)\n')
try:
    rc4, out4 = bat('--list')
    hit4 = u'r999gate' in out4 and rc4 == 1
    print(u'④ 自稱『某輪所立・升閘』而未列 → 漂移點名：%s｜退 %d（須 1）' % (u'中' if hit4 else u'不中', rc4))
    if not hit4:
        fails.append(u'記號表未擴')
finally:
    if os.path.exists(GATE):
        os.remove(GATE)
rc5, out5 = bat('--list')
back2 = (rc5 == 0 and u'漂移 0' in out5)
print(u'⑤ 除假軸後 → 冊淨漂移零：%s｜退 %d' % (u'中' if back2 else u'不中', rc5))
print(u'名冊還原：%s（假軸已除：%s）' % (u'如舊' if io.open(REG, encoding='utf-8').read() == reg0 else u'已臟！',
                                    u'是' if not os.path.exists(DUMMY) else u'否！'))
ok = not fails and back and back2 and io.open(REG, encoding='utf-8').read() == reg0
print(u'結果斷：%s' % (u'跑批器四路俱有牙（漂移・rc・記號表・還原），且植病已全數還原' if ok else u'負測不合：%s' % fails))
sys.exit(0 if ok else 1)
