# -*- coding: utf-8 -*-
# 第 184 輪·負測：拆去一枚節級導言，戊目『節下即款·真無一字』須 +1。
# 植病探本檔（只寫副本，主檔不動）；副本行數與正路徑全同，故行號不移（180 輪之制）。
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
MASTER = u'ver38四分律_起心動念心智分析框架_修正版.md'
COP = u'_work/r184neg.md'
env = dict(os.environ)
env['PYTHONIOENCODING'] = 'utf-8'
env['PYTHONPATH'] = '.'

LEAD = u'導言既以大樹為喻，此節先立其觀法之器：名相所從出、方法所止際。二者不明，則所照皆成妄執。'

raw = io.open(MASTER, encoding=u'utf-8').read()
lines = raw.split(u'\n')
idx = [k for k, l in enumerate(lines) if l == LEAD]
assert len(idx) == 1, u'導言錨非恰一：%s' % idx
n0 = len(lines)


def run(path):
    q = subprocess.run([sys.executable, u'-X', u'utf8', u'_work/r180voice.py', path],
                       capture_output=True, text=True, encoding=u'utf-8', env=env)
    m = re.search(u'無一句承接）：(\\d+)', q.stdout)
    assert m, q.stdout[:400]
    zhen = re.search(u"真無一字', (\\d+)", q.stdout)
    assert zhen, q.stdout[:400]
    return int(m.group(1)), int(zhen.group(1))


tot0, zhen0 = run(MASTER)
lines[idx[0]] = u''
assert len(lines) == n0, u'植病改動行數——副本行號將移'
io.open(COP, 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(lines))
try:
    tot1, zhen1 = run(COP)
finally:
    os.remove(COP)
h = io.open(MASTER, encoding=u'utf-8').read()
print(u'正路：戊總 %d｜真無一字 %d' % (tot0, zhen0))
print(u'植病：戊總 %d｜真無一字 %d（須各 +1）' % (tot1, zhen1))
print(u'主檔未動：%s' % (u'是' if h == raw else u'否！'))
ok = (zhen1 == zhen0 + 1 and tot1 == tot0 + 1 and h == raw)
print(u'結果斷：%s' % (u'戊目有牙：導言一撤即報' if ok else u'負測不合——器或無牙'))
sys.exit(0 if ok else 1)
