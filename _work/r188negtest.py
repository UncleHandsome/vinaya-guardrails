# -*- coding: utf-8 -*-
# 第 188 輪·負測：分植兩病，證丁·羅項末項未收句號 與 戊·項末誤頓號 俱有牙。
# 只寫副本、不動主檔；每次植病俱『同位換字、不增不刪行』。
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
MASTER = u'ver38四分律_起心動念心智分析框架_修正版.md'
env = dict(os.environ)
env['PYTHONIOENCODING'] = 'utf-8'
env['PYTHONPATH'] = '.'

LINES = io.open(MASTER, encoding=u'utf-8').read().split(u'\n')
N0 = len(LINES)
ITEM = re.compile(u'^\\s*([-*]|\\d+[.)、])\\s+\\S.*。\\s*$')
MARK = re.compile(u'^\\s*([-*]|\\d+[.)、])\\s+')
TAIL = re.compile(u'。\\s*$')


def swap(line, ch):
    return TAIL.sub(ch, line.rstrip()) + (line[len(line.rstrip()):])


def find_pair():
    """取一『群之末即 block 之末』的兄弟對：其後除空行外不再是列項（否則乃巢未盡之正格，丁本不報）。"""
    for i in range(1, len(LINES) - 2):
        if not (ITEM.match(LINES[i]) and ITEM.match(LINES[i - 1])):
            continue
        ind = len(LINES[i]) - len(LINES[i].lstrip())
        ind2 = len(LINES[i - 1]) - len(LINES[i - 1].lstrip())
        if ind != ind2:
            continue
        j = i + 1
        while j < len(LINES) and not LINES[j].strip():
            j += 1
        if j >= len(LINES):
            continue
        if MARK.match(LINES[j]) or LINES[j].strip().startswith(u'#'):
            continue
        if LINES[j].strip().startswith(u'|'):
            continue
        return i
    return None


def find_single():
    for i in range(1, len(LINES) - 1):
        if not ITEM.match(LINES[i]):
            continue
        ind = len(LINES[i]) - len(LINES[i].lstrip())
        prev = LINES[i - 1]
        if ITEM.match(prev) and len(prev) - len(prev.lstrip()) == ind:
            return i
    return None


def run(path):
    q = subprocess.run([sys.executable, u'-X', u'utf8', u'_work/r188tail.py', path, u'require-hit'],
                       capture_output=True, text=True, encoding=u'utf-8', env=env)
    d = re.search(u'丁·羅項末項未收句號 (\\d+) 巢', q.stdout)
    e = re.search(u'戊·項末誤頓號 (\\d+) 項', q.stdout)
    assert d and e, q.stdout[:400] + q.stderr[:400]
    return int(d.group(1)), int(e.group(1)), q.returncode


pair, single = find_pair(), find_single()
assert pair and single, u'無處可植（取樣先失效）：pair=%s single=%s' % (pair, single)
d0, e0, rc0 = run(MASTER)
print(u'正路：丁 %d｜戊 %d（俱須 0）｜退 %d（須 1＝無報即不過）' % (d0, e0, rc0))

dW, dR, rcW = run_pair = None, None, None
lines = list(LINES)
lines[pair - 1] = swap(lines[pair - 1], u'；')
lines[pair] = swap(lines[pair], u'；')
assert len(lines) == N0 and lines[pair].rstrip().endswith(u'；')
cop = u'_work/r188neg_丁.md'
io.open(cop, 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(lines))
try:
    rW = run(cop)
finally:
    os.remove(cop)

lines = list(LINES)
lines[single] = swap(lines[single], u'、')
assert len(lines) == N0 and lines[single].rstrip().endswith(u'、')
cop = u'_work/r188neg_戊.md'
io.open(cop, 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(lines))
try:
    rE = run(cop)
finally:
    os.remove(cop)

t = io.open(MASTER, encoding=u'utf-8').read()
print(u'植丁（L%d＋L%d 末標易『；』）：丁 %d（須 ≥1）｜戊 %d｜退 %d（須 0）' % (pair - 1, pair, rW[0], rW[1], rW[2]))
print(u'植戊（L%d 末標易『、』）：丁 %d｜戊 %d（須 ≥1）｜退 %d（須 0）' % (single, rE[0], rE[1], rE[2]))
print(u'主檔：%s｜行數=%d' % (u'未動' if len(t.split(u'\n')) == N0 else u'已變！', len(t.split(u'\n'))))
ok = (d0 == 0 and e0 == 0 and rc0 == 1 and rW[0] >= 1 and rW[2] == 0
      and rE[1] >= 1 and rE[2] == 0 and len(t.split(u'\n')) == N0)
print(u'結果斷：%s' % (u'丁戊俱有牙：末標一改即報' if ok else u'負測不合——器或無牙'))
sys.exit(0 if ok else 1)
