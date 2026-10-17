# -*- coding: utf-8 -*-
# 第 185 輪·負測：同位植一枚『自製要約掛「」而具律文形貌』之病，甲桶須由 0 起 1。
# 只寫副本、不動主檔；副本行數與正路徑全同（180 輪之制：植病須同位換字、不增不刪行）。
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
MASTER = u'ver38四分律_起心動念心智分析框架_修正版.md'
COP = u'_work/r185neg.md'
env = dict(os.environ)
env['PYTHONIOENCODING'] = 'utf-8'
env['PYTHONPATH'] = '.'

GOOD = u'「維護僧譽、顧全大局、學會包容」'
BAD = u'「若比丘以妄語覆藏麁罪，其覆即成波羅夷」'
PAT = re.compile(u'甲·律文形貌（本軸之的）(\\d+)')


def run(path):
    q = subprocess.run([sys.executable, u'-X', u'utf8', u'_work/r185orphan.py', path, u'require-hit'],
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
print(u'主檔：%s（%d 處，未被本測觸動）' % (u'如舊' if GOOD in t and BAD not in t else u'已臟！', t.count(GOOD)))
ok = (a0 == 0 and rc0 == 1 and a1 == 1 and rc1 == 0 and GOOD in t and BAD not in t)
print(u'結果斷：%s' % (u'甲目有牙：律文形貌一掛「」即報' if ok else u'負測不合——器或無牙'))
sys.exit(0 if ok else 1)
