# -*- coding: utf-8 -*-
# 第 180 輪·簡形新單之負測：以『貼』之行替為簡形『贴』植入印面，書閘須報；還原後雜湊須同。
# 全段包於 try/finally——**植入主檔之任何腳本，須使『還原』在異常路徑下也必執行**
#   （本器初版即因 `dict(..., PYTHONIOENCODING=utf-8)` 之語法錯死在植入之後、復原之前，
#    主檔遂留一枚植入字，賴人工覆核始清——此即『植病之器自傷最重』之實據）。
import hashlib
import io
import os
import re
import subprocess
import sys

sys.path.insert(0, u'.')
import _tk

MASTER = u'ver38四分律_起心動念心智分析框架_修正版.md'
raw = io.open(MASTER, 'rb').read()
h0 = hashlib.sha256(raw).hexdigest()
t = raw.decode(u'utf-8')
B = _tk.bottom_lines()
lines = t.split(u'\n')

target = None
for i, l in enumerate(lines):
    if i in B or not l.strip():
        continue
    plain = re.sub(u'「[^」]*」|『[^』]*』', u'', l)
    if u'貼' in plain:
        target = (i, plain)
        break
assert target, u'印面引號外查無『貼』——負測須改用他法'
i = target[0]
lines2 = list(lines)
lines2[i] = lines[i].replace(u'貼', u'贴', 1)
io.open(MASTER, 'wb').write(u'\n'.join(lines2).encode(u'utf-8'))

rc_plant = nfail = 0
hit = []
try:
    env = dict(os.environ)
    env[u'PYTHONIOENCODING'] = u'utf-8'
    p = subprocess.run([sys.executable, u'-X', u'utf8', u'_tk.py', u'check'],
                       capture_output=True, text=True, encoding=u'utf-8', env=env)
    rc_plant = p.returncode
    rep = io.open(u'_work/check.txt', encoding=u'utf-8').read()
    nfail = sum(1 for x in rep.split(u'\n') if x.startswith(u'FAIL'))
    hit = [x for x in rep.split(u'\n') if x.startswith(u'FAIL') and u'簡體孤立字' in x]
finally:
    io.open(MASTER, 'wb').write(raw)

h1 = hashlib.sha256(io.open(MASTER, 'rb').read()).hexdigest()


def pair(path):
    s = io.open(path, encoding=u'utf-8').read()
    m = re.search(u'S = \\((.*?)\\)\\n', s, re.S)
    n = re.search(u'T = \\((.*?)\\)\\n', s, re.S)
    S = u''.join(re.findall(u"u?'([^']*)'", m.group(1))) if m else u''
    T = u''.join(re.findall(u"u?'([^']*)'", n.group(1))) if n else u''
    return len(S), len(T), (u'贴' in S), (u'貼' in T)


ok_scan = True
for path in (u'_work/recordsimp.py', u'_work/memsimp.py'):
    a, b, c, d = pair(path)
    print(u'%-22s S %d｜T %d（須等長）｜收 贴 %d｜收 貼 %d' % (path, a, b, c, d))
    ok_scan = ok_scan and (a == b) and c and d

print(u'植貼→贴：check rc=%d｜FAIL 總數 %d｜簡形一條報 %d（俱須 ≥1）｜其報 %s' % (
    rc_plant, nfail, len(hit), hit[:1]))
print(u'還原：雜湊%s（須同）' % (u'相同' if h0 == h1 else u'不同！'))
ok = (rc_plant == 1 and nfail >= 1 and hit and h0 == h1 and ok_scan)
print(u'結果斷：%s' % (u'書閘能逮新形、記錄器名單俱齊、主檔無損'
                       if ok else u'負測不合——器仍無牙或檔未復'))
sys.exit(0 if ok else 1)
