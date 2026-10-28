# -*- coding: utf-8 -*-
"""292・己組補刀（刀口一之『建議二』落盡：解除八對八之死扣）。

欄名『卷首心印對應句』易讀作一一对位，今改『義近句』；正文之枚序列舉改標『氣脈之所近』，
並明文『不標一二之同項』。口徑：逐錨斷言命中數，簡形新增須零，改畢即跑十尺。
"""
import hashlib
import io
import os
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
    assert n == expect, u'%s：命中 %d 枚（須 %d）➔ %s' % (label, n, expect, old[:26])
    for i, x in enumerate(L):
        if old in x:
            L[i] = x.replace(old, new)
            LOG.append(u'L%-5d %-20s ×%d' % (i + 1, label, x.count(old)))


rep(u'卷首心印對應句', u'卷首心印義近句', u'表欄名・義近', 2)
rep(u'：善護三業對正理一、明眼避險對正理二、蜂採其華對正理三、但自觀行對正理四、'
    u'自淨其意對正理五、不惱他人對正理六、勤學無憂對正理七、常樂空閑對正理八。',
    u'：八句之於八尺，此欄只標氣脈之所近（善護三業近正理一、明眼避險近正理二……'
    u'常樂空閑近正理八），**不標一二之同項——義近非號同，讀表者勿合讀為十六條**。',
    u'一章・解八對八之死扣')
rep(u'#### 四、八大正理體用源流全景表（心印體 ╳ 十句義母源 ╳ 裁判之尺 ╳ 自省之鏡）',
    u'#### 四、八大正理體用源流全景表（心印之義近 ╳ 十句義母源 ╳ 裁判之尺 ╳ 自省之鏡）',
    u'一章・表題歸今制')

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
print(u'刀數 %d｜行數 %d ➔ %d' % (len(LOG), len(T.split(u'\n')), len(L)))
for x in LOG:
    print(u'  ' + x)
k = [i for i, x in enumerate(L) if x.startswith(u'#### 四、八大正理體用源流')]
for q in range(k[0], k[0] + 6):
    print(u'  L%d｜%s' % (q + 1, L[q][:400]))
if not APPLY:
    print(u'（乾跑・未寫檔。）')
    sys.exit(0)
assert not newbad, u'簡形未淨'
B = OUT.replace(u'\n', u'\r\n').encode('utf-8')
io.open(SRC, 'wb').write(B)
print(u'寫畢：%dB｜CRLF %d｜bareCR %d｜sha %s ➔ %s' % (
    len(B), B.count(b'\r\n'), B.count(b'\r') - B.count(b'\r\n'), SHA0,
    hashlib.sha256(OUT.encode('utf-8')).hexdigest()[:12]))
