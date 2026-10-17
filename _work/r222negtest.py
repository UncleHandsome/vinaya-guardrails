# -*- coding: utf-8 -*-
# 第 222 輪・負測器（留檔）：新閘 92『印面漢字並列不作半形斜線』之牙與四側豁免
#   ⓪ 現形（須綠・全閘綠）
#   ① 表列植『漢/漢』→ 須報
#   ② 散文植『漢/漢』→ 須報（證兩容器俱有牙）
#   ③ 半形方括號之內植『漢/漢』→ 須不報（本輪新開之豁免側：字構拆描之職，同級植病證其界）
#   ④ 圍欄行植『漢/漢』→ 須不報（221 之容器法沿用）
#   ⑤ 既有引號之內植『漢/漢』→ 須不報（照錄側）
#   ⑥ 表列植『漢／漢』（全形）→ 須不報（陰性對照，證尺不誤傷通例）
#   ⑦甲 表列植『拉/拉』、⑦乙 表列植『數/數』→ 須不報（證尺取漢漢，不誤傷外語名與比值）
#   每路俱斷『中其目』（216 之誡）；自建基準、副本用完即除，他日可獨立重跑；末以主檔哈希自證一字未損。
#   宿主之辨一律手扫（find）不用正則——方括號與引號之字類式表屢因轉義走樣而空轉（206 之誡、本輪兩度自蹈）。
from __future__ import unicode_literals
import hashlib
import io
import os
import subprocess
import sys

NL = chr(10)
TICK = chr(0x60)
FENCE = TICK * 3
LB = u'['
RB = u']'
LQ = u'「'
RQ = u'」'
SL = chr(0x2F)
FW = chr(0xFF0F)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, u'ver38四分律_起心動念心智分析框架_修正版.md')
WORK = os.path.join(ROOT, u'_r222neg.md')
GATE = u'漢字並列不作半形斜線'
BASE = io.open(MD, encoding=u'utf-8').read()
H0 = hashlib.sha256(io.open(MD, u'rb').read()).hexdigest()
L = BASE.split(NL)
os.chdir(ROOT)
sys.path.insert(0, ROOT)
import _tk
BOT = set(_tk.bottom_lines())


def fences(lines):
    fl, inside = [False] * len(lines), False
    for i in range(len(lines)):
        if lines[i].startswith(FENCE):
            inside = not inside
            fl[i] = True
            continue
        fl[i] = inside
    return fl


FL = fences(L)


def han(c):
    return 0x4E00 <= ord(c) <= 0x9FFF


def bar_free(s):
    return SL not in s and FW not in s


def brk_span(s):
    """求『[ … 漢字 … ]』括內末漢字之位（無則 None）——括內本無斜線者方堪植字。"""
    k = s.find(LB)
    while k >= 0:
        e = s.find(RB, k)
        if e < 0:
            return None
        inner = s[k + 1:e]
        if inner and any(han(c) for c in inner) and SL not in inner:
            return k + 1 + max(j for j, c in enumerate(inner) if han(c))
        k = s.find(LB, e)
    return None


def quote_span(s):
    """求『「 … 」』閉號之位（行內成對且其間無斜線者）。"""
    k = s.find(LQ)
    while k >= 0:
        e = s.find(RQ, k)
        if e < 0:
            return None
        if SL not in s[k + 1:e] and FW not in s[k + 1:e]:
            return e
        k = s.find(LQ, e)
    return None


def t_tbl(i):
    s = L[i]
    return (i not in BOT and not FL[i] and s.strip().startswith(u'|') and s.count(u'|') >= 4
            and s.rstrip().endswith(u'|') and u'--' not in s and bar_free(s) and LQ not in s)


def t_prse(i):
    s = L[i].strip()
    return (i not in BOT and not FL[i] and 40 <= len(s) <= 150 and s.endswith(u'。')
            and not s.startswith((u'#', u'|', u'>', u'*', u'-')) and bar_free(s)
            and LQ not in s and u'『' not in s and LB not in s)


def t_brack(i):
    s = L[i]
    return (i not in BOT and not FL[i] and s.count(LB) == s.count(RB) and brk_span(s) is not None)


def t_fence(i):
    return (FL[i] and i not in BOT and not L[i].startswith(FENCE) and bar_free(L[i])
            and sum(1 for c in L[i] if c in u'│─▼►') >= 1 and len(L[i].rstrip()) > 8)


def t_quote(i):
    return (i not in BOT and not FL[i] and quote_span(L[i]) is not None)


def pick(pred, lo=0):
    for i in range(lo, len(L)):
        if pred(i):
            return i
    raise AssertionError(u'無宿主')


IT, n = [], 0
while len(IT) < 5:
    j = pick(t_tbl, n)
    IT.append(j)
    n = j + 1
I_TBL, I_TBL2, I_TBL3, I_TBL4, I_TBL5 = IT
I_PRSE = pick(t_prse)
I_BRK = pick(t_brack)
I_FNC = pick(t_fence)
I_QUT = pick(t_quote)
print(u'宿主｜表列 %s｜散文 L%d｜方括號 L%d｜圍欄 L%d｜引號 L%d' % (
    SL.join(str(x + 1) for x in IT), I_PRSE + 1, I_BRK + 1, I_FNC + 1, I_QUT + 1))


def cell(idx, txt):
    t = L[:]
    s = t[idx].rstrip()
    k = s.rfind(u'|')
    assert k > 0
    t[idx] = s[:k] + txt + s[k:]
    return NL.join(t)


def end(idx, txt):
    t = L[:]
    assert txt not in t[idx]
    t[idx] = t[idx].rstrip() + txt
    return NL.join(t)


def inbrk(idx):
    t = L[:]
    k = brk_span(t[idx])
    assert k is not None, u'方括號宿主不如期'
    t[idx] = t[idx][:k] + SL + u'乙' + t[idx][k:]
    return NL.join(t)


def inq(idx):
    t = L[:]
    k = quote_span(t[idx])
    assert k is not None, u'引號宿主不如期'
    t[idx] = t[idx][:k] + u'甲' + SL + u'乙' + t[idx][k:]
    return NL.join(t)


P1 = cell(I_TBL, u'甲乙' + SL + u'丙丁')
P2 = end(I_PRSE, u'（植此：甲乙' + SL + u'丙丁）')
P3 = inbrk(I_BRK)
P4 = end(I_FNC, u' 甲' + SL + u'乙')
P5 = inq(I_QUT)
P6 = cell(I_TBL2, u'甲乙' + FW + u'丙丁')
P7 = cell(I_TBL3, u'Abc' + SL + u'Def')
P8 = cell(I_TBL4, u'12' + SL + u'34')
for nm, txt in ((u'①', P1), (u'②', P2), (u'③', P3), (u'④', P4), (u'⑤', P5), (u'⑥', P6),
                (u'⑦甲', P7), (u'⑦乙', P8)):
    assert len(txt.split(NL)) == len(L), u'%s 動了行數' % nm
    assert txt != BASE, u'%s 植字未生效' % nm

CASES = [(u'⓪ 現形（須綠）', None, u'綠'),
         (u'① 表列植漢斜漢（須報）', P1, u'報'),
         (u'② 散文植漢斜漢（須報）', P2, u'報'),
         (u'③ 方括號內植漢斜漢（須不報）', P3, u'不報'),
         (u'④ 圍欄行植漢斜漢（須不報）', P4, u'不報'),
         (u'⑤ 引號之內植漢斜漢（須不報）', P5, u'不報'),
         (u'⑥ 表列植漢全形斜漢（須不報）', P6, u'不報'),
         (u'⑦甲 表列植拉斜拉（須不報）', P7, u'不報'),
         (u'⑦乙 表列植數斜數（須不報）', P8, u'不報')]


def run(txt):
    io.open(WORK, u'w', encoding=u'utf-8', newline=NL).write(txt)
    env = dict(os.environ)
    env[u'TKSRC'] = WORK
    env[u'PYTHONPATH'] = ROOT
    p = subprocess.Popen([sys.executable, u'-X', u'utf8', os.path.join(ROOT, u'_tk.py'), u'check'],
                         cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.communicate()[0].decode(u'utf-8', u'replace')
    rows = [x for x in out.split(NL) if GATE in x and (x.startswith(u'PASS') or x.startswith(u'FAIL'))]
    fails = [x for x in out.split(NL) if x.startswith(u'FAIL')]
    return p.returncode, (rows[0] if rows else u'（無本目之行）'), fails


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
    print(u'%-32s｜本目 %-5s｜退出碼 %d｜他閘 FAIL %d｜%s' % (
        name, st, rc, len(others), u'中' if good else u'不中'))
    if not good or others:
        print(u'      本目行：%s' % row[:190])
        for x in others[:2]:
            print(u'      他閘：%s' % x[:130])
    ok = ok and good

if os.path.exists(WORK):
    os.remove(WORK)
H1 = hashlib.sha256(io.open(MD, u'rb').read()).hexdigest()
print(u'哈希自證｜主檔 %s…｜%s' % (H1[:12], u'未損' if H1 == H0 else u'已損！'))
assert H1 == H0, u'主檔在負測中被動——即停'
print(u'結論｜九路%s' % (u'俱中' if ok else u'有未中'))
sys.exit(0 if ok else 1)
