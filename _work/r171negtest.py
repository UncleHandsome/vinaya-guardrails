# -*- coding: utf-8 -*-
"""r171negtest.py —— 第 171 輪負測：證本軸有牙，且歸零非消音。

三測：
  一 回植：於副本以「欲對其進行處分」替「欲處分之」 → 甲必報 +1（器有牙）。
  二 非消音（自動詞豁免）：撤『其後無賓語即豁免』一條再掃主檔 → 甲必增報（『得以進行』一类）。
  三 非消音（法令豁免）：撤 STATUTE 一條再掃主檔 → 乙必報《勞資爭議處理法》之『予以』。
用法：`PYTHONPATH=. python -X utf8 _work/r171negtest.py`
"""
import io, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AXIS = os.path.join(ROOT, '_work', 'r171light.py')
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = [f for f in os.listdir(ROOT) if f.startswith('ver38') and f.endswith('.md')][0]
SRCP = os.path.join(ROOT, SRC)
COPY = os.path.join(HERE, 'r171neg.md')
TMP1 = os.path.join(HERE, '_ax_nointrans.py')
TMP2 = os.path.join(HERE, '_ax_nostat.py')


def run(script, path):
    env = dict(os.environ)
    env['PYTHONPATH'] = ROOT
    env['PYTHONIOENCODING'] = 'utf-8'
    out = subprocess.run([sys.executable, '-X', 'utf8', script, path],
                         capture_output=True, text=True, encoding='utf-8', env=env)
    tail = [l for l in out.stdout.splitlines() if l.startswith(u'== 合計')]
    assert tail, out.stdout[-300:] + out.stderr[-300:]
    return tail[0]


def num(line, tag):
    return int(re.search(u'%s (\\d+)' % tag, line).group(1))


s = io.open(SRCP, encoding='utf-8').read()
r0 = run(AXIS, SRCP)
print(u'〇 今制：%s' % r0)

# 一 回植
assert s.count(u'僧團大眾欲處分之') == 1
io.open(COPY, 'w', encoding='utf-8', newline='').write(
    s.replace(u'僧團大眾欲處分之', u'僧團大眾欲對其進行處分', 1))
r1 = run(AXIS, COPY)
print(u'一 回植『進行處分』：%s' % r1)
assert num(r1, u'甲') == num(r0, u'甲') + 1, u'回植未報，器無牙'
print(u'   PASS：甲 +1（器有牙）')

# 二 撤自動詞豁免
ax = io.open(AXIS, encoding='utf-8').read()
io.open(TMP1, 'w', encoding='utf-8').write(ax.replace(u'if not OBJ.match(tail):', u'if False:'))
r2 = run(TMP1, SRCP)
print(u'二 撤自動詞豁免：%s' % r2)
assert num(r2, u'甲') > num(r0, u'甲'), u'撤豁免仍零——此測無效或豁免非因'
print(u'   PASS：甲 %d→%d（歸零確賴此豁免，故須如實記其理）' % (num(r0, u'甲'), num(r2, u'甲')))

# 三 撤法令豁免
io.open(TMP2, 'w', encoding='utf-8').write(
    ax.replace(u"if w == u'予以' and STATUTE.search", u"if False and STATUTE.search"))
r3 = run(TMP2, SRCP)
print(u'三 撤法令豁免：%s' % r3)
assert num(r3, u'乙') > num(r0, u'乙'), u'撤法令豁免仍零'
print(u'   PASS：乙 %d→%d' % (num(r0, u'乙'), num(r3, u'乙')))

for p in (TMP1, TMP2):
    os.remove(p)
print(u'\n三測俱 PASS。')
