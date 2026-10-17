# -*- coding: utf-8 -*-
# 第 220 輪・負測器（留檔）：簡形名單八字之擴到，與『巢套豁免』口徑之兩側
#   ⓪ 現形——簡形閘須綠
#   ① 印面散文植『并』（裸字，引號外）→ 須報
#   ② 印面散文植『届』→ 須報（第二形，證非只對一字有牙）
#   ③ 同線引號內植『并』→ 須不報（舊尺亦守，豁免側之對稱）
#   ④ 跨行巢套引文內植『并』→ 新口徑須不報，而舊同線剝法須報（差證隨附）
#       ——此路專驗本輪口徑升級所扩之那一段碼；不露差即未測到
#   每路俱斷『中其目』：FAIL 者須為簡形閘，且報數須含所植之字。
import hashlib
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, u'ver38四分律_起心動念心智分析框架_修正版.md')
WORK = os.path.join(ROOT, u'_r220work.md')
GATE = u'引號外無簡體孤立字'
JP = chr(0x5E76)                        # 并（本輪新入名單之字）
RX = u'「[^」]*」|『[^』]*』'
BASE = io.open(MD, encoding=u'utf-8').read()
H0 = hashlib.sha256(io.open(MD, u'rb').read()).hexdigest()   # 與 H1 同法（取原位元組，免 BOM/換行演繹之差）
L = BASE.split(u'\n')


def state_out(s):
    o = []
    a = b = 0
    for c in s:
        if c == u'「':
            a += 1
        elif c == u'」':
            a = max(0, a - 1)
        elif c == u'『':
            b += 1
        elif c == u'』':
            b = max(0, b - 1)
        elif a == 0 and b == 0:
            o.append(c)
    return u''.join(o)


def once_out(s):
    return re.sub(RX, u'', s)


def prose_host():
    for i, l in enumerate(L):
        s = l.strip()
        if 60 <= len(s) <= 200 and s.endswith(u'。') \
                and not s.startswith((u'#', u'|', u'>', u'*', u'-')) \
                and u'「' not in s and u'」' not in s and u'『' not in s and u'』' not in s:
            return i
    raise AssertionError(u'無散文宿主')


def seam():
    """尋一『巢套之縫』：狀態機判在引號內、而同線配對之舊剝法判在引號外的位置。
       本書之實例即 L5671（外層「」領起而內層『』『』重疊，配對錯位）——植字於此縫，
       舊尺必報（露差）、新尺不報（口徑之擴到由實例證，不靠推理）。"""
    ins = []
    a = b = 0
    nq = []
    idx = None
    for i, c in enumerate(BASE):
        if c == u'「':
            a += 1
        elif c == u'」':
            a = max(0, a - 1)
        elif c == u'『':
            b += 1
        elif c == u'』':
            b = max(0, b - 1)
        ins.append((a == 0 and b == 0))
    cov = [False] * len(BASE)
    for m in re.finditer(RX, BASE):
        for k in range(m.start(), m.end()):
            cov[k] = True
    for i, c in enumerate(BASE):
        if c == JP and ins[i] is False and cov[i] is False:
            return i, BASE[:i].count(chr(10)) + 1
    raise AssertionError(u'無巢套之縫——舊尺之錯位在本檔未現，擴到須另證')


I1 = prose_host()
I2 = I1   # 各路自成副本，同宿主亦可兩植
SEAM, SEAM_LN = seam()


def add(ln, txt):
    t = BASE.split(u'\n')
    assert txt not in t[ln], u'宿主已含植字'
    t[ln] = t[ln].rstrip() + txt
    return u'\n'.join(t)


P1 = add(I1, u'（此處植一枚并字，以驗名單！）  ')
P2 = add(I2, u'（此處植一枚届字，以驗名單！）  ')
P3 = add(I1, u'（引「并」之式）  ')
P4 = BASE[:SEAM] + JP + BASE[SEAM:]          # 巢套之縫內插一枚裸『并』（不增不減他字）
d_old = once_out(P4).count(JP) - once_out(BASE).count(JP)
d_new = state_out(P4).count(JP) - state_out(BASE).count(JP)
print(u'宿主｜散文 L%d｜巢套之縫 L%d（其『并』舊剝露於引外、狀態機斂於引內）' % (I1 + 1, SEAM_LN))
print(u'現形之差｜并 舊剝餘 %d｜新机餘 %d（須 舊>0 且 新=0——此即本輪修尺之所由）'
      % (once_out(BASE).count(JP), state_out(BASE).count(JP)))
print(u'④ 差證｜縫中植字後：舊剝新增 %d（須 >0）｜新機新增 %d（須 0）' % (d_old, d_new))
assert once_out(BASE).count(JP) > 0 and state_out(BASE).count(JP) == 0, u'現形之差不露，尺無可證'
assert d_old > 0 and d_new == 0, u'④ 未練到新口徑那段碼——此路無效'

CASES = [
    (u'⓪ 現形（須綠）', None, None),
    (u'① 散文植并（須報）', P1, u'并'),
    (u'② 散文植届（須報）', P2, u'届'),
    (u'③ 同線引號內植并（須不報）', P3, None),
    (u'④ 跨行巢套內植并（須不報）', P4, None),
]


def run(txt):
    io.open(WORK, u'w', encoding=u'utf-8', newline=u'\n').write(txt)
    env = dict(os.environ)
    env[u'TKSRC'] = WORK
    env[u'PYTHONPATH'] = ROOT
    p = subprocess.Popen([sys.executable, u'-X', u'utf8', os.path.join(ROOT, u'_tk.py'), u'check'],
                         cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.communicate()[0].decode(u'utf-8', u'replace')
    rep = os.path.join(ROOT, u'_work', u'check.txt')
    body = io.open(rep, encoding=u'utf-8').read() if os.path.exists(rep) else out
    row = [x for x in body.split(u'\n') if GATE in x]
    return p.returncode, (row[0] if row else u''), out


ok = True
for name, txt, want in CASES:
    rc, row, out = run(BASE if txt is None else txt)
    st = row.split(u' ')[0] if row else u'無行'
    others = [x for x in out.split(u'\n') if x.startswith(u'FAIL') and GATE not in x]
    if want is None:
        good = (st == u'PASS')
        print(u'%-30s｜簡形閘 %-4s｜他閘 FAIL %d 條｜%s' % (name, st, len(others), u'中' if good else u'不中'))
    else:
        good = (st == u'FAIL' and want in row and rc != 0)
        print(u'%-30s｜簡形閘 %-4s｜報數含『%s』：%s｜退出碼 %d｜%s'
              % (name, st, want, want in row, rc, u'中' if good else u'不中'))
    if not good:
        print(u'      %s' % ((row[:150] if row else u'') or u'；'.join(others[:2])))
    ok = ok and good

if os.path.exists(WORK):
    os.remove(WORK)
H1 = hashlib.sha256(io.open(MD, u'rb').read()).hexdigest()
print(u'哈希自證｜主檔 %s…｜%s' % (H1[:12], u'未損' if H1 == H0 else u'已損！'))
assert H1 == H0
print(u'結論｜五路%s' % (u'俱中' if ok else u'有不中'))
sys.exit(0 if ok else 1)
