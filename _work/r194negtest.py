# -*- coding: utf-8 -*-
# 第 194 輪·負測：轉寫軸之甲目須有牙（音符脫落、連字號之異俱報；唯大小寫異不報）。
# 只寫副本、不動主檔；植病同位換字、不增不刪行。
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

MASTER = u'ver38四分律_起心動念心智分析框架_修正版.md'
COP = u'_work/r194neg.md'
env = dict(os.environ)
env['PYTHONIOENCODING'] = 'utf-8'
env['PYTHONPATH'] = '.'

PAT = re.compile(u'甲·一詞兩拼（本軸之的）(\\d+)')
PATD = re.compile(u'丁·唯大小寫異 (\\d+)')

PLANTS = [
    (u'音符脫落（應報）', u'Upekṣā', u'Upekṣa', 1),
    (u'連字號之異（應報）', u'Upekṣā', u'Upe-kṣā', 1),
    (u'唯大小寫異（應擯）', u'受 Vedanā、想', u'受 vedanā、想', 0),
]


def run(path):
    q = subprocess.run([sys.executable, u'-X', u'utf8', u'_work/r194pali.py', path, u'require-hit'],
                       capture_output=True, text=True, encoding=u'utf-8', env=env)
    m = PAT.search(q.stdout)
    d = PATD.search(q.stdout)
    assert m and d, q.stdout[:400]
    return int(m.group(1)), int(d.group(1)), q.returncode


base_lines = io.open(MASTER, encoding=u'utf-8').read().split(u'\n')
a0, d0, rc0 = run(MASTER)
print(u'正路：甲 %d（須 0）｜丁 %d｜退 %d（須 1）' % (a0, d0, rc0))
assert a0 == 0 and rc0 == 1

n0 = len(base_lines)
fails = []
for name, old, new, want in PLANTS:
    idx = [k for k, l in enumerate(base_lines) if old in l]
    assert idx, u'找不到錨：%s' % old
    lines = list(base_lines)
    lines[idx[0]] = lines[idx[0]].replace(old, new, 1)
    assert len(lines) == n0
    io.open(COP, 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(lines))
    try:
        a1, d1, rc1 = run(COP)
    finally:
        if os.path.exists(COP):
            os.remove(COP)
    ok = a1 == want
    if not ok:
        fails.append(name)
    print(u'%-22s 植於 L%-6d 甲 %d（須 %d）｜丁 %d｜%s' % (name, idx[0] + 1, a1, want, d1, u'中' if ok else u'不中'))

mt = io.open(MASTER, encoding=u'utf-8').read()
print(u'主檔：%s' % (u'如舊' if u'Upekṣa' not in mt and u'Upe-kṣā' not in mt else u'已臟！'))
ok = not fails and u'Upe-kṣā' not in mt
print(u'結果斷：%s' % (u'轉寫軸有牙——音符脫落與連字號之異俱報，唯大小寫不報' if ok else u'負測不合：%s' % fails))
sys.exit(0 if ok else 1)
