# -*- coding: utf-8 -*-
# 第 204 輪·負測：新軸 `r204chart` 須有牙——八植分擊甲・乙・丙・丁・戊・己・庚・辛八目，
# 另以主檔現形為陰性對照（退 0），並自證主檔末段未動。
# 植病只在 `_work/_r204neg.md` 之副本上動手，**主檔一字不觸**；副本用畢即刪。
import io
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

MD = u'ver38四分律_起心動念心智分析框架_修正版.md'
PRE = u'_work/_r204base.md'
NEG = u'_work/_r204neg.md'
BASE = io.open(MD, encoding=u'utf-8').read()
io.open(PRE, 'w', encoding=u'utf-8', newline=u'\n').write(BASE)   # 自建基準，故本測可獨立重跑（不倚他輪之副本）
L = BASE.split(u'\n')

# 以「圖內之行號」定位（1 基，主檔今制 9393–9459），植病各以其原文為錨、斷言恰一
ROW_BAR1, ROW_V1, ROW_LB1, ROW_SP1 = 9403, 9404, 9405, 9407
ROW_SP2 = 9408


def plant(name, fn):
    lines = list(L)
    lines = fn(lines)
    io.open(NEG, 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(lines))
    q = subprocess.run([sys.executable, u'-X', u'utf8', u'_work/r204chart.py',
                        u'--file=' + NEG, u'--ref=' + PRE, LIMIT],
                       capture_output=True, text=True, encoding=u'utf-8', errors='replace')
    hit = (u'  %s ' % name) in q.stdout
    print(u'  %s·%s：%s｜退 %d' % (name, EXPECT[name], u'中' if hit else u'不中', q.returncode))
    if not hit or q.returncode != 1:
        print(u'     └ 輸出：%s' % q.stdout.strip().split(u'\n')[-3:])
    return hit and q.returncode == 1


def shift_last(s, ch, k):
    i = s.rindex(ch)
    return s[:i] + u' ' * k + ch + s[i + 1:]


CASES = [
    (u'甲', u'孤箭', lambda ls: [(shift_last(x, u'▼', 2) if i == ROW_V1 - 1 else x)
                              for i, x in enumerate(ls)]),
    (u'乙', u'空落', lambda ls: [(x.replace(u'【道岔一：前端阻卻】', u'  【道岔一：前端阻卻】', 1)
                              if i == ROW_LB1 - 1 else x) for i, x in enumerate(ls)]),
    (u'丁', u'歪角', lambda ls: [(x[:-1] + u'┌' if i == ROW_BAR1 - 1 else x) for i, x in enumerate(ls)]),
    (u'戊', u'歪扅', lambda ls: [(x.replace(u'┌', u'┴', 1) if i == ROW_BAR1 - 1 else x)
                             for i, x in enumerate(ls)]),
    (u'丙', u'斷柱', lambda ls: [(x.replace(u'│', u' ', 1) if i == ROW_SP1 - 1 else x)
                             for i, x in enumerate(ls)]),
    (u'辛', u'骨架', lambda ls: [(x.replace(u'│', u' ', 1) if i == ROW_SP2 - 1 else x)
                             for i, x in enumerate(ls)]),
    (u'庚', u'改字', lambda ls: [(x.replace(u'見罪自肯', u'見罪自言', 1) if i == 9441 - 1 else x)
                             for i, x in enumerate(ls)]),
]
EXPECT = {u'甲': u'▼ 上無導線', u'乙': u'▼ 下無所指', u'丙': u'│ 上無來處', u'丁': u'臂缺',
          u'戊': u'┴ 上無來線', u'辛': u'導線骨架異', u'庚': u'文字簽名異', u'己': u'最寬逾限'}

fails = []
LIMIT = u'100'
for name, _d, fn in CASES:
    if not plant(name, fn):
        fails.append(name)

# 己·逾寬：以寬限 90 校主檔現形（今 95 半形）⇒ 須報己；以 100 校則須淨（陰性對照在下一行）
LIMIT = u'90'
if not plant(u'己', lambda ls: list(ls)):
    fails.append(u'己')
LIMIT = u'100'

q0 = subprocess.run([sys.executable, u'-X', u'utf8', u'_work/r204chart.py',
                     u'--ref=' + PRE, u'100'],
                    capture_output=True, text=True, encoding=u'utf-8', errors='replace')
ctl = (q0.returncode == 0)
print(u'  陰性對照·主檔現形退 0：%s（%d）' % (u'中' if ctl else u'不中', q0.returncode))
print(u'  主檔末段自證：%s' % (u'如舊' if io.open(MD, encoding=u'utf-8').read() == BASE else u'已臟！'))

for _p in (NEG, PRE):
    if os.path.exists(_p):
        os.remove(_p)
ok = not fails and ctl and io.open(MD, encoding=u'utf-8').read() == BASE
print(u'結果斷：%s' % (u'r204chart 八目俱有牙，主檔未動，副本已除' if ok else u'負測不合：%s' % fails))
sys.exit(0 if ok else 1)
