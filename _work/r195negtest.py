# -*- coding: utf-8 -*-
# 第 195 輪立・第 196 輪擴：層級指針軸之負測（章缺／節缺／款缺／該章不用節序／合法指針五植）。
# 只寫副本、不動主檔；植病同位換字、不增不刪行。陽性與陰性對照俱給（192 之誡）。
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

MASTER = u'ver38四分律_起心動念心智分析框架_修正版.md'
COP = u'_work/r195neg.md'
env = dict(os.environ)
env['PYTHONIOENCODING'] = 'utf-8'
env['PYTHONPATH'] = '.'

PAT = re.compile(u'甲·章不存在 (\\d+)｜乙·節不存在 (\\d+)｜丙·該章不用節序 (\\d+)｜'
                 u'丁·款不存在 (\\d+)｜戊·該節不用款序 (\\d+)')

PLANTS = [
    (u'章不存在→甲', u'詳見第六章', u'詳見第十章', (1, 0, 0, 0, 0)),
    (u'節不存在→乙', u'詳見第七章第三節', u'詳見第七章第二十節', (0, 1, 0, 0, 0)),
    (u'款不存在→丁', u'依第五章第七節第七款', u'依第五章第七節第二十款', (0, 0, 0, 1, 0)),
    (u'該章不用節序→丙', u'詳見第九章第二節第二款', u'詳見第六章第一節第二款', (0, 0, 1, 0, 0)),
    (u'合法指針→俱零', u'詳見第七章第三節', u'詳見第七章第一節', (0, 0, 0, 0, 0)),
]


def run(path):
    q = subprocess.run([sys.executable, u'-X', u'utf8', u'_work/r195ref.py', path, u'require-hit'],
                       capture_output=True, text=True, encoding=u'utf-8', env=env)
    m = PAT.search(q.stdout)
    assert m, q.stdout[:400]
    return tuple(int(m.group(x)) for x in range(1, 6)), q.returncode


got0, rc0 = run(MASTER)
print(u'正路：%s（須全 0）｜退 %d（須 1）' % (got0, rc0))
assert got0 == (0, 0, 0, 0, 0) and rc0 == 1

base = io.open(MASTER, encoding=u'utf-8').read().split(u'\n')
n0 = len(base)
fails = []
for name, old, new, want in PLANTS:
    idx = [k for k, l in enumerate(base) if old in l]
    assert idx, u'找不到錨：%s' % old
    lines = list(base)
    lines[idx[0]] = lines[idx[0]].replace(old, new, 1)
    assert len(lines) == n0, u'植病改動行數'
    io.open(COP, 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(lines))
    try:
        got, rc = run(COP)
    finally:
        if os.path.exists(COP):
            os.remove(COP)
    ok = got == want
    if not ok:
        fails.append(name)
    print(u'%-18s 甲%d 乙%d 丙%d 丁%d 戊%d（須 %s）｜%s' % (name, got[0], got[1], got[2], got[3], got[4], want,
                                                    u'中' if ok else u'不中'))

mt = io.open(MASTER, encoding=u'utf-8').read()
print(u'主檔：%s' % (u'如舊' if u'第二十款' not in mt and u'第十章' not in mt else u'已臟！'))
ok = not fails and u'第二十款' not in mt
print(u'結果斷：%s' % (u'層級指針軸有牙——三級之死鏈俱報，而不用節序之章與合法指針不誤傷' if ok
                    else u'負測不合：%s' % fails))
sys.exit(0 if ok else 1)
