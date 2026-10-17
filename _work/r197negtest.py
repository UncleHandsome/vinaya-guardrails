# -*- coding: utf-8 -*-
# 第 197 輪·負測：判例卡片軸須能報『缺欄』『欄序倒置』『主卡片非百則』，且不誤傷正常卡片。
# 只寫副本、不動主檔；植病同位換字、不增不刪行；陽性與陰性對照俱給（192 之誡）。
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

MASTER = u'ver38四分律_起心動念心智分析框架_修正版.md'
COP = u'_work/r197neg.md'
env = dict(os.environ)
env['PYTHONIOENCODING'] = 'utf-8'
env['PYTHONPATH'] = '.'

PAT = re.compile(u'主 (\\d+) 則・補遺 (\\d+) 則｜甲·四欄有缺 (\\d+)｜乙·欄序倒置或重出 (\\d+)｜丙·主卡片非百則 (\\d+)')


def run(path):
    q = subprocess.run([sys.executable, u'-X', u'utf8', u'_work/r197card.py', path, u'require-hit'],
                       capture_output=True, text=True, encoding=u'utf-8', env=env)
    m = PAT.search(q.stdout)
    assert m, q.stdout[:400]
    return (int(m.group(3)), int(m.group(4)), int(m.group(5))), q.returncode


def card_block(text, head):
    """取某一則卡片之區塊（自其 H4 起至下一張卡片前），回傳 (起, 迄)。"""
    a = text.index(head)
    b = text.index(u'#### 〔', a + 5)
    return a, b


got0, rc0 = run(MASTER)
print(u'正路：甲 %d｜乙 %d｜丙 %d（須全 0）｜退 %d（須 1）' % (got0[0], got0[1], got0[2], rc0))
assert got0 == (0, 0, 0) and rc0 == 1

base = io.open(MASTER, encoding=u'utf-8').read()
n0 = base.count(u'\n')

# ── 四植：各造一段改後全文，再交軸判 ─────────────────────────
pops = {}

a, b = card_block(base, u'#### 〔遮1〕')
blk = base[a:b]
assert blk.count(u'##### 人間智慧\n') == 1
pops[u'缺欄→甲'] = base[:a] + blk.replace(u'##### 人間智慧\n', u'##### 現代啟示\n', 1) + base[b:], (1, 0, 0)

a, b = card_block(base, u'#### 〔遮2〕')
blk = base[a:b]
assert blk.count(u'##### 事相經過\n') == 1 and blk.count(u'##### 人間智慧\n') == 1
blk2 = blk.replace(u'##### 事相經過\n', u'##### @TMP@\n', 1)
blk2 = blk2.replace(u'##### 人間智慧\n', u'##### 事相經過\n', 1).replace(u'##### @TMP@\n', u'##### 人間智慧\n', 1)
pops[u'欄序倒置→乙'] = base[:a] + blk2 + base[b:], (0, 1, 0)

pops[u'主數非百→丙'] = (base.replace(u'#### 〔遮1〕', u'#### 〔遺1〕', 1), (0, 0, 1))
pops[u'正常卡片→俱零'] = (base.replace(u'#### 〔遮3〕', u'#### 〔遮3〕 ', 1), (0, 0, 0))

fails = []
for name, (txt, want) in pops.items():
    assert txt.count(u'\n') == n0, u'植病改動行數：%s' % name
    io.open(COP, 'w', encoding=u'utf-8', newline=u'\n').write(txt)
    try:
        got, rc = run(COP)
    finally:
        if os.path.exists(COP):
            os.remove(COP)
    ok = got == want
    if not ok:
        fails.append(u'%s（得 %s）' % (name, got))
    print(u'%-16s 甲%d 乙%d 丙%d（須 %s）｜%s' % (name, got[0], got[1], got[2], want, u'中' if ok else u'不中'))

mt = io.open(MASTER, encoding=u'utf-8').read()
# 淨檢之標須取『必不存在之語』：〔遺N〕乃附錄B 本有之編號（實測 3 見），不可作髒跡之用
dirty = [s for s in (u'現代啟示', u'@TMP@') if s in mt]
print(u'主檔：%s' % (u'如舊' if not dirty else u'已臟！%s' % dirty))
ok = not fails and not dirty
print(u'結果斷：%s' % (u'卡片軸有牙——缺欄、倒序、失數俱報，正常卡片不誤傷' if ok else u'負測不合：%s' % fails))
sys.exit(0 if ok else 1)
