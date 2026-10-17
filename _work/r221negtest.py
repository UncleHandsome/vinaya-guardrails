# -*- coding: utf-8 -*-
"""第 221 輪・負測七路（留檔）：新閘 91『印面引號外且圍欄外不作半形圓括號』之牙與兩側豁免。
   ⓪ 現形須綠
   ① 表列（圍欄外）植半形括拉丁 → 須報（陽性，證閘有牙）
   ② 散文（圍欄外）植半形括漢字 → 須報（證本閘以容器為界，不以字形為界）
   ③ 圍欄行植半形括漢字 → 須不報（本輪新開之豁免側，同級植病證其界）
   ④ 既有引號之內植半形 → 須不報（照錄側）
   ⑤ 底冊行植半形 → 須不報（記錄從寬側）
   ⑥ 表列植全形括拉丁 → 須不報（陰性對照，證尺不誤傷通例）
   末以主檔哈希自證未損（取原位元組）。"""
from __future__ import unicode_literals
import hashlib
import io
import os
import re
import subprocess
import sys

NL = chr(10)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, u'ver38四分律_起心動念心智分析框架_修正版.md')
WORK = os.path.join(ROOT, u'_r221neg.md')
GATE = u'圍欄外不作半形圓括號'
BASE = io.open(MD, encoding=u'utf-8').read()
H0 = hashlib.sha256(io.open(MD, u'rb').read()).hexdigest()
L0 = BASE.split(NL)
os.chdir(ROOT)
sys.path.insert(0, ROOT)
import _tk
BOT = set(_tk.bottom_lines())          # 0 基


def fences(lines):
    fl, inside = [False] * len(lines), False
    for i in range(len(lines)):
        if lines[i].strip().startswith(u'```'):
            inside = not inside
            fl[i] = True
            continue
        fl[i] = inside
    return fl


FL = fences(L0)


def prose(i):
    s = L0[i].strip()
    return (i not in BOT and not FL[i] and not s.startswith((u'#', u'|', u'>', u'*', u'-'))
            and 30 <= len(s) <= 120 and u'(' not in s and u')' not in s)


def tabl(i):
    l = L0[i]
    return (i not in BOT and not FL[i] and l.strip().startswith(u'|') and l.count(u'|') >= 3
            and l.rstrip().endswith(u'|') and u'(' not in l and u'--' not in l)


def fences_ns(lines):
    """_tk 之制：行首直指 ```（不 strip）。兩式取交集，豁免側方無歧義。"""
    fl, inside = [False] * len(lines), False
    for i in range(len(lines)):
        if lines[i].startswith(u'```'):
            inside = not inside
            fl[i] = True
            continue
        fl[i] = inside
    return fl


FL2 = fences_ns(L0)


def fence_line(i):
    return (FL[i] and FL2[i] and i not in BOT and not L0[i].strip().startswith(u'```')
            and u'(' not in L0[i] and u')' not in L0[i] and len(L0[i].rstrip()) > 6
            and sum(1 for c in L0[i] if c in u'\u2502\u2500\u25bc\u25ba') >= 1)


def quoted(i):
    return (i not in BOT and not FL[i] and re.search(u'「[^」()]*」', L0[i]) is not None)


def bottom(i):
    return (i in BOT and not FL[i] and u'(' not in L0[i] and len(L0[i].strip()) > 20)


def pick(pred, lo=0):
    for i in range(lo, len(L0)):
        if pred(i):
            return i
    raise AssertionError(u'無宿主')


I_PROSE = pick(prose)
I_TBL = pick(tabl, I_PROSE + 1)
I_FENCE = pick(fence_line)
I_QUOT = pick(quoted, I_TBL + 1)
I_BOT = pick(bottom)
print(u'宿主｜散文 L%d｜表列 L%d｜圍欄 L%d｜引號 L%d｜底冊 L%d' %
      (I_PROSE + 1, I_TBL + 1, I_FENCE + 1, I_QUOT + 1, I_BOT + 1))


def repl(i, fn):
    t = L0[:]
    t[i] = fn(t[i])
    return NL.join(t)


def app(s, x):
    return s + x


def cell(s, x):
    """插入表列最後一格之前，欄數不動、行末無空白。"""
    k = s.rstrip().rfind(u'|')
    return s.rstrip()[:k] + x + s.rstrip()[k:]


def inquote(s, x):
    m = re.search(u'「([^」()]*)」', s)
    return s[:m.end(1)] + x + s[m.end(1):]


T1 = repl(I_TBL, lambda s: cell(s, u'(TimingX) '))
T2 = repl(I_PROSE, lambda s: app(s, u'（植此 (測試) 以驗牙）'))
T3 = repl(I_FENCE, lambda s: app(s, u'(邊標)'))
T4 = repl(I_QUOT, lambda s: inquote(s, u' (引內)'))
T5 = repl(I_BOT, lambda s: app(s, u'（記此 (底記) 舊形）'))
T6 = repl(I_TBL, lambda s: cell(s, u'（LatinX） '))
for nm, txt in ((u'①', T1), (u'②', T2), (u'③', T3), (u'④', T4), (u'⑤', T5), (u'⑥', T6)):
    assert len(txt.split(NL)) == len(L0), u'%s 動了行數' % nm
    assert txt != BASE, u'%s 植字未生效' % nm

CASES = [(u'⓪ 現形（須綠）', None, u'綠'),
         (u'① 表列植半形拉丁（須報）', T1, u'報'),
         (u'② 散文植半形漢字（須報）', T2, u'報'),
         (u'③ 圍欄植半形漢字（須不報）', T3, u'不報'),
         (u'④ 引號之內植半形（須不報）', T4, u'不報'),
         (u'⑤ 底冊植半形（須不報）', T5, u'不報'),
         (u'⑥ 表列植全形拉丁（須不報）', T6, u'不報')]


def run(txt):
    io.open(WORK, u'w', encoding=u'utf-8', newline=NL).write(txt)
    env = dict(os.environ)
    env[u'TKSRC'] = WORK
    env[u'PYTHONPATH'] = ROOT
    p = subprocess.Popen([sys.executable, u'-X', u'utf8', os.path.join(ROOT, u'_tk.py'), u'check'],
                         cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.communicate()[0].decode(u'utf-8', u'replace')
    row = [x for x in out.split(NL) if GATE in x and (x.startswith(u'PASS') or x.startswith(u'FAIL'))]
    fails = [x for x in out.split(NL) if x.startswith(u'FAIL')]
    return p.returncode, (row[0] if row else u'（無本目之行）'), fails


ok = True
for name, txt, want in CASES:
    rc, row, fails = run(BASE if txt is None else txt)
    st = row.split(u' ')[0]
    others = [x for x in fails if GATE not in x]
    if want == u'綠':
        good = (st == u'PASS' and rc == 0)
    elif want == u'報':
        good = (st == u'FAIL' and rc != 0)
    else:
        good = (st == u'PASS')
    print(u'%-30s｜本目 %-5s｜退出碼 %d｜他閘 FAIL %d｜%s' % (name, st, rc, len(others), u'中' if good else u'不中'))
    if not good or others:
        print(u'      本目行：%s' % row[:170])
        for x in others[:3]:
            print(u'      他閘：%s' % x[:130])
    ok = ok and good

if os.path.exists(WORK):
    os.remove(WORK)
H1 = hashlib.sha256(io.open(MD, u'rb').read()).hexdigest()
print(u'哈希自證｜主檔 %s…｜%s' % (H1[:12], u'未損' if H1 == H0 else u'已損！'))
assert H1 == H0, u'主檔在負測中被動——即停'
print(u'結論｜七路%s' % (u'俱中' if ok else u'有未中'))
sys.exit(0 if ok else 1)
