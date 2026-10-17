# -*- coding: utf-8 -*-
# 第 190 輪·負測：同位易一書名（改成本地未收且 F-3 未列之僎名），甲目須由 0 起 1。
# 只寫副本、不動主檔；行數全同。
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
MASTER = u'ver38四分律_起心動念心智分析框架_修正版.md'
COP = u'_work/r190neg.md'
env = dict(os.environ)
env['PYTHONIOENCODING'] = 'utf-8'
env['PYTHONPATH'] = '.'

GOOD = u'（該典本地語料未收，其逐字無從覆核，已列附錄F-3'
BAD = u'（《陘山別錄》本地語料未收，其逐字無從覆核'
PAT = re.compile(u'甲·宣稱本地未收而未列 F-3 (\\d+) 筆')


def run(path):
    q = subprocess.run([sys.executable, u'-X', u'utf8', u'_work/r190f3.py', path, u'require-hit'],
                       capture_output=True, text=True, encoding=u'utf-8', env=env)
    m = PAT.search(q.stdout)
    assert m, q.stdout[:400] + q.stderr[:300]
    return int(m.group(1)), q.returncode


lines = io.open(MASTER, encoding=u'utf-8').read().split(u'\n')
idx = [k for k, l in enumerate(lines) if GOOD in l]
assert len(idx) >= 1, u'植病錨零見'
n0 = len(lines)
for k in idx:
    lines[k] = lines[k].replace(GOOD, BAD, 1)
assert len(lines) == n0

a0, rc0 = run(MASTER)
io.open(COP, 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(lines))
try:
    a1, rc1 = run(COP)
finally:
    if os.path.exists(COP):
        os.remove(COP)

t = io.open(MASTER, encoding=u'utf-8').read()
print(u'正路：甲 %d（須 0，揭露無漏）｜退 %d（須 1）' % (a0, rc0))
print(u'植病：%d 處易為僎名《陘山別錄》→ 甲 %d（須 ≥1）｜退 %d（須 0）' % (len(idx), a1, rc1))
print(u'主檔：%s' % (u'如舊' if GOOD in t and BAD not in t else u'已臟！'))
ok = (a0 == 0 and rc0 == 1 and a1 >= 1 and rc1 == 0 and GOOD in t and BAD not in t)
print(u'結果斷：%s' % (u'甲目有牙：未收而未列 F-3 即報' if ok else u'負測不合——器或無牙'))
sys.exit(0 if ok else 1)
