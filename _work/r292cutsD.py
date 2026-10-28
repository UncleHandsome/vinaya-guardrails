# -*- coding: utf-8 -*-
"""292・丁組刀（『憲綱』之名全退，還三十二字於『略戒心印』；平等憲綱歸平等正理）。

外路第七報刀口一之『建議一』：憲綱二字太像法典之名，遂與八大正理相打。
今全書『憲綱』字面歸零，『略戒心印』為體之名；泛指治理原則之『平等憲綱』改稱『平等正理』。
口徑：逐形斷言命中數；先長後短，短形須在長形退盡之後；改畢印殘存之『憲[綱章]』行，目視其義。
"""
import hashlib
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
APPLY = u'--apply' in sys.argv

RAW = io.open(SRC, 'rb').read()
SHA0 = hashlib.sha256(RAW.replace(b'\r\n', b'\n')).hexdigest()[:12]
T = RAW.decode('utf-8').replace(u'\r\n', u'\n')
L = T.split(u'\n')
LOG = []


def rep(old, new, label, expect=1):
    n = sum(x.count(old) for x in L)
    assert n == expect, u'%s：命中 %d 枚（須 %d）➔ %s' % (label, n, expect, old[:20])
    for i, x in enumerate(L):
        if old in x:
            L[i] = x.replace(old, new)
            LOG.append(u'%-26s L%-5d ×%d ➔ %s' % (label, i + 1, x.count(old), new[:28]))


XG = u'憲' + chr(0x7DB1)                                   # 綱（防傳遞層歸簡）
IN = u'心' + chr(0x5370)                                   # 印
RULES = [
    (u'三十二字略戒' + XG + u'（諸佛教' + IN + u'）', u'三十二字略戒' + IN, u'題目・心印去重', 2),
    (u'三十二字略戒' + XG + u'（諸佛教' + IN + u'·體）', u'三十二字略戒' + IN + u'（體）',
     u'種子圖・心印去重', 1),
    (u'三十二字略戒' + XG, u'三十二字略戒' + IN, u'全書・三十二字略戒心印', 9),
    (u'略戒' + XG, u'略戒' + IN, u'全書・略戒心印', 6),
    (u'32字' + XG, u'32字' + IN, u'動線・32字心印', 1),
    (u'三十二字' + XG, u'三十二字' + IN, u'結語・三十二字心印', 1),
    (u'卷首' + XG, u'卷首' + IN, u'一章・卷首心印', 3),
    (XG + u'體', IN + u'體', u'表題・心印體', 1),
    (u'大綱座右銘（' + XG + IN + u'）', u'大綱座右銘（' + IN + u'）', u'卷首・座右銘去重', 1),
    (u'大綱座右銘（憲章' + IN + u'）', u'大綱座右銘（' + IN + u'）', u'法位宣告・座右銘去重', 1),
    (XG + u'之「自淨其意」', IN + u'之「自淨其意」', u'七佛略戒・心印之句', 1),
    (u'為' + XG + u'之歸', u'為' + IN + u'之歸', u'一章・心印之歸', 1),
    (u'卷首之' + XG + u'既立', u'卷首' + IN + u'既立', u'一章・卷首心印既立', 1),
    (u'平等' + XG, u'平等正理', u'六章・平等正理', 2),
]
for old, new, label, expect in RULES:
    rep(old, new, label, expect)

rest = [(i + 1, x) for i, x in enumerate(L) if XG in x]
print(u'殘存『憲綱』：%d 行' % len(rest))
for i, x in rest:
    print(u'  L%d｜%s' % (i, x[:120]))
for i, x in enumerate(L):
    for m in re.finditer(u'憲' + chr(0x7AE0), x):            # 憲章（泛指，保留）
        print(u'  〔憲章・留〕L%d｜%s' % (i + 1, x[max(0, m.start() - 18):m.start() + 14]))

OUT = u'\n'.join(L)
sys.path.insert(0, os.path.join(ROOT, u'_work'))
import _simpmap as SM                                   # noqa: E402
import _simpdict as SD                                   # noqa: E402
SIMPS = set(getattr(SM, 'MAP', {})) | set(getattr(SD, 'MAP', {}))
newbad = sorted(({c for c in OUT if c in SIMPS} - {c for c in T if c in SIMPS}))
print(u'簡形新增：%s' % (u''.join(newbad) or u'無'))
for c in newbad:
    j = OUT.find(c)
    print(u'   %s U+%04X｜…%s…' % (c, ord(c), OUT[max(0, j - 22):j + 12].replace(u'\n', u' ')))
print(u'刀數 %d｜行數 %d ➔ %d' % (len(LOG), len(L), len(L)))
for x in LOG:
    print(u'  ' + x)
if not APPLY:
    print(u'（乾跑・未寫檔。）')
    sys.exit(0)
assert not newbad, u'簡形未淨'
B = OUT.replace(u'\n', u'\r\n').encode('utf-8')
io.open(SRC, 'wb').write(B)
print(u'寫畢：%dB｜CRLF %d｜bareCR %d｜sha %s ➔ %s' % (
    len(B), B.count(b'\r\n'), B.count(b'\r') - B.count(b'\r\n'), SHA0,
    hashlib.sha256(OUT.encode('utf-8')).hexdigest()[:12]))
