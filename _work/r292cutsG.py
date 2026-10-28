# -*- coding: utf-8 -*-
"""292・庚組刀（刀口七之半：第一章之四奪重述退場，全數歸附錄一之矩陣）。

外路第七報刀口七『宗門機鋒全數歸位至附錄一與結語』——第一章乃母法公堂，不宜自點火又潑水。
量得：第一章第六節第二款之『病相⟷四奪』圍欄圖與四條列舉，與附錄一『臨濟四奪行持矩陣』
      （L7423〜7433・四門四省四情境）文義重出，故削此段而留法位辨定與剛性禁令（後者是判準層之防，非機鋒）。
口徑：整段以行號定位切除，先斷言起訖之形；公共之義一句不失（歸附錄一之橋自帶其目）。
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

h = [i for i, x in enumerate(L) if x.startswith(u'#### 二、臨濟四奪之妙用')]
assert len(h) == 1, u'款題錨命中 %d' % len(h)
h = h[0]
a = [i for i, x in enumerate(L) if x.startswith(u'審理者在手握實體閘門與母法正理時')]
assert len(a) == 1, u'起行錨命中 %d' % len(a)
a = a[0]
b = [i for i, x in enumerate(L) if x.startswith(u'* **人境俱不奪（平常無事歸家）**')]
assert len(b) == 1, u'訖行錨命中 %d' % len(b)
b = b[0] + 1                                          # 其下之續行亦屬此條
assert L[b].strip().endswith(u'平常是道。'), u'訖行末不合：%s' % L[b][-20:]
assert L[b + 1].strip() == u'' and L[b + 2].strip() == u'---', u'段外之形不合'
assert a == h + 4, u'起行非款題之第四行（%d≠%d）' % (a, h + 4)
CUT = L[a:b + 1]
NEW = [u'四奪與『法官席上四大心智病相』之逐一對位（病相➔所奪➔臨場自省），'
       u'**全數歸附錄一『臨濟四奪行持矩陣』**——公堂之上稱量唯依六閘門與八大正理，'
       u'宗門活句不入母法之章；退庭之後方堪自照，故其文不列於此。']
L[a:b + 1] = NEW
OUT = u'\n'.join(L)

sys.path.insert(0, os.path.join(ROOT, u'_work'))
import _simpmap as SM                                   # noqa: E402
import _simpdict as SD                                   # noqa: E402
SIMPS = set(getattr(SM, 'MAP', {})) | set(getattr(SD, 'MAP', {}))
newbad = sorted(({c for c in OUT if c in SIMPS} - {c for c in T if c in SIMPS}))
print(u'簡形新增：%s' % (u''.join(newbad) or u'無'))
print(u'削 %d 行・插 %d 行｜行數 %d ➔ %d｜削去之字 %d' % (
    len(CUT), len(NEW), len(T.split(u'\n')), len(L), sum(len(x) for x in CUT)))
print(u'—— 削去之段（供覆核其義果存於附錄一）——')
for x in CUT:
    print(u'  | %s' % x[:110])
print(u'—— 新款之形 ——')
for q in range(h, h + 8):
    print(u'  L%d｜%s' % (q + 1, L[q][:230]))
if not APPLY:
    print(u'（乾跑・未寫檔。）')
    sys.exit(0)
assert not newbad, u'簡形未淨'
B = OUT.replace(u'\n', u'\r\n').encode('utf-8')
io.open(SRC, 'wb').write(B)
print(u'寫畢：%dB｜CRLF %d｜bareCR %d｜sha %s ➔ %s' % (
    len(B), B.count(b'\r\n'), B.count(b'\r') - B.count(b'\r\n'), SHA0,
    hashlib.sha256(OUT.encode('utf-8')).hexdigest()[:12]))
