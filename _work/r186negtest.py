# -*- coding: utf-8 -*-
# 第 186 輪·負測：同位植一枚『本律逐字而掛雙層角引號』之病，甲桶須由 0 起 1。
# 只寫副本、不動主檔；副本行數與正路徑全同（植病須同位換字、不增不刪行）。
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
MASTER = u'ver38四分律_起心動念心智分析框架_修正版.md'
COP = u'_work/r186neg.md'
env = dict(os.environ)
env['PYTHONIOENCODING'] = 'utf-8'
env['PYTHONPATH'] = '.'

GOOD = u'『兩側不得互相打架』'
BAD = u'『諸惡莫作，諸善奉行；自淨其意，是諸佛教』'   # 律本七佛略戒之逐字（50-60 卷段與 11-21 卷段兩見）
PAT = re.compile(u'甲·本律逐字（本軸之的）(\\d+)')


def run(path):
    q = subprocess.run([sys.executable, u'-X', u'utf8', u'_work/r186mirror.py', path, u'require-hit'],
                       capture_output=True, text=True, encoding=u'utf-8', env=env)
    m = PAT.search(q.stdout)
    assert m, q.stdout[:400]
    return int(m.group(1)), q.returncode


lines = io.open(MASTER, encoding=u'utf-8').read().split(u'\n')
idx = [k for k, l in enumerate(lines) if GOOD in l]
assert len(idx) == 1, u'植病錨非恰一：%s' % idx
n0 = len(lines)
lines[idx[0]] = lines[idx[0]].replace(GOOD, BAD, 1)
assert len(lines) == n0, u'植病改動行數——副本行號將移'

a0, rc0 = run(MASTER)
io.open(COP, 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(lines))
try:
    a1, rc1 = run(COP)
finally:
    if os.path.exists(COP):
        os.remove(COP)

t = io.open(MASTER, encoding=u'utf-8').read()
print(u'正路：甲 %d（須 0，本輪已歸位）｜require-hit 退 %d（須 1＝無報即不過）' % (a0, rc0))
print(u'植病：甲 %d（須 1）｜退 %d（須 0＝有報方算過）' % (a1, rc1))
print(u'主檔：%s（錨 %d 處、植字 %d 處，未被本測觸動）'
      % (u'如舊' if GOOD in t and BAD not in t else u'已臟！', t.count(GOOD), t.count(BAD)))
ok = (a0 == 0 and rc0 == 1 and a1 == 1 and rc1 == 0 and GOOD in t and BAD not in t)
print(u'結果斷：%s' % (u'甲目有牙：律本逐字一掛『』即報' if ok else u'負測不合——器或無牙'))
sys.exit(0 if ok else 1)
