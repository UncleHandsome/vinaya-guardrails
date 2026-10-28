# -*- coding: utf-8 -*-
"""292・戊組刀（刀口四方案B：附錄六自『十五則深描』轉為『法理專題十五則』，六支器同靶）。

裁語：不採『擴編 112 案』——其十則乃法理推演（共犯・未遂・受樂時序・越權代理），
      納入判例庫即混『既證』與『推演』，正犯本書自制；亦不廢其編序——編序正是
      『專題指針可達』『L行號』『核卷』三尺之靶。故只去其『第二套案號』之相：
      名曰『調部專題』，導言明文『01〜15 唯檢索之序，非案號，不與 102 案爭數』。
器改之律：只以唯一錨點逐條替換（命中數當場斷言），改畢 ast 復核並數其相鄰語句之存在；
          『經典地標深描』四字不入此刀（第六章之制，非附錄六之名）。
"""
import ast
import hashlib
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
WORK = os.path.join(ROOT, u'_work')
PRINTD = os.path.join(ROOT, u'_print')
APPLY = u'--apply' in sys.argv
LOG = []

SM = chr(0x6DF1) + chr(0x63CF)                  # 深描
ZT = chr(0x5C08) + chr(0x984C)                  # 專題
TIAO = chr(0x615F)                              # 慟（本輪所除之錯字）
DB = chr(0x8ABF) + chr(0x90E8)                  # 調部

RAW = io.open(SRC, 'rb').read()
SHA0 = hashlib.sha256(RAW.replace(b'\r\n', b'\n')).hexdigest()[:12]
T = RAW.decode('utf-8').replace(u'\r\n', u'\n')
L = T.split(u'\n')


def rep(old, new, label, expect=1):
    n = sum(x.count(old) for x in L)
    assert n == expect, u'冊・%s：命中 %d 枚（須 %d）➔ %s' % (label, n, expect, old[:22])
    for i, x in enumerate(L):
        if old in x:
            L[i] = x.replace(old, new)
            LOG.append(u'冊 L%-5d %-16s ×%d' % (i + 1, label, x.count(old)))


# ── 冊身：名制・導言・錯字 ────────────────────────────────────────
rep(DB + u'邊緣疑難判例法十五則' + SM, DB + u'疑難判例法理' + ZT + u'十五則', u'附錄六標題', 4)
rep(DB + u'邊緣疑難判例十五則' + SM, DB + u'疑難判例法理' + ZT + u'十五則', u'凡例・附錄收編', 1)
rep(DB + SM, DB + ZT, u'全書・調部專題', 24)
rep(u'**案例與' + SM + u'之編號**', u'**案例與' + ZT + u'之編號**', u'凡例・括號之義', 1)
rep(u'至此，**「' + DB + u'疑難判例法理' + ZT + u'十五則（〔' + DB + ZT + u' 01〕〜〔15〕）」**'
    u'已全數完整歸位！',
    u'十五則既竟，此篇與第六章表裡相成之職亦盡。', u'附錄六・交付殘跡之除')
rep(u'將這套調部精華重新納入《四分律：起心動念心智分析框架》新修訂定本的基座之中，'
    u'這座法相大廈的所有縫隙與拼圖已徹底焊死、圓融無礙。',
    u'調部之精華既具於此篇，第六章之判例法典乃無剩義——法相大廈之縫隙，於此得補；'
    u'補已，遂忘其補。', u'附錄六・定本自指之除')
rep(u'十五則之編次止於『' + SM + u'』之序，不另立案號，亦不與 102 案爭數。',
    u'十五則之編次止於『' + ZT + u'』之序——**『01〜15』唯檢索之序，非第二套案號**，'
    u'不另立案號，亦不與 102 案爭數；判例總帳一以第六章 102 案為準。',
    u'附錄六・編次之義')
rep(u'為編者就地覆核逐字之所' + TIAO, u'為編者就地覆核逐字之所據', u'附錄六・錯字之除', 1)

OUT = u'\n'.join(L)
sys.path.insert(0, WORK)
import _simpmap as SMAP                                 # noqa: E402
import _simpdict as SDP                                  # noqa: E402
SIMPS = set(getattr(SMAP, 'MAP', {})) | set(getattr(SDP, 'MAP', {}))
newbad = sorted(({c for c in OUT if c in SIMPS} - {c for c in T if c in SIMPS}))
print(u'冊・簡形新增：%s' % (u''.join(newbad) or u'無'))
print(u'冊・殘『深描』%d 枚（地標 %d 枚除外，應歸零於此刀之轄）' % (
    OUT.count(SM), OUT.count(chr(0x5730) + chr(0x6A19) + SM)))
for m in re.finditer(u'.{0,16}' + SM + u'.{0,8}', OUT):
    print(u'   …%s…' % m.group(0).replace(u'\n', u' '))

# ── 六支器同靶（錨＋命中數逐一斷言）─────────────────────────────
PATCH = [
    (u'v39chk.py', DB + SM, DB + ZT, 8),
    (u'v39chk.py', u'案號與' + SM + u'之編序', u'案號與' + ZT + u'之編序', 1),
    (u'v39chk.py', SM + u'編序', ZT + u'編序', 1),
    (u'v39chk.py', SM + u'指針可達', ZT + u'指針可達', 1),
    (u'v39chk.py', SM + u'則數', ZT + u'則數', 1),
    (u'v39chk.py', u'連貫無缺號）', u'連貫無缺號；292 奉第七報刀口四，此名自『' + SM + u'』改『' + ZT + u'』）', 1),
    (u'v39linchk.py', DB + SM, DB + ZT, 1),
    (u'v39volchk.py', DB + SM, DB + ZT, 1),
    (u'r272teeth.py', DB + SM, DB + ZT, 5),
    (u'r272teeth.py', SM + u' 15→16', ZT + u' 15→16', 1),
    (u'r272teeth.py', u'降一則' + SM + u'為四級題', u'降一則' + ZT + u'為四級題', 1),
    (u'_casedef.py', DB + SM, DB + ZT, 1),
    (u'build39.py', DB + SM, DB + ZT, 2),
    (u'build39.py', u'(u"' + SM + u'", buyi)', u'(u"' + ZT + u'", buyi)', 1),
    (u'build39.py', u'則' + SM + u'·', u'則' + ZT + u'·', 1),
    (u'build39.py', u'十五則' + SM, u'十五則' + ZT, 1),
]
FAIL = []
for name, old, new, expect in PATCH:
    path = os.path.join(PRINTD if name == u'build39.py' else WORK, name)
    s = io.open(path, encoding='utf-8').read()
    n = s.count(old)
    if n != expect:
        FAIL.append(u'%s・錨『%s』命中 %d（須 %d）' % (name, old[:20], n, expect))
        continue
    s2 = s.replace(old, new)
    ast.parse(s2)
    LOG.append(u'器 %-14s ×%d ➔ %s' % (name, n, new[:22]))
    if APPLY:
        io.open(path, 'w', encoding='utf-8', newline='\n').write(s2)
for name in (u'v39chk.py', u'v39linchk.py', u'v39volchk.py', u'r272teeth.py',
             u'_casedef.py', u'build39.py'):
    p = os.path.join(PRINTD if name == u'build39.py' else WORK, name)
    s = io.open(p, encoding='utf-8').read()
    print(u'器・%-14s 今『深描』%d｜『專題』%d｜地標深描%d' % (
        name, s.count(SM), s.count(ZT), s.count(chr(0x5730) + chr(0x6A19) + SM)))
print(u'刀數 %d' % len(LOG))
for x in LOG:
    print(u'  ' + x)
if FAIL:
    print(u'⚠ 錨不合（俱未改）：')
    for x in FAIL:
        print(u'   ' + x)
    sys.exit(1)
if not APPLY:
    print(u'（乾跑・未寫檔。）')
    sys.exit(0)
assert not newbad, u'簡形未淨'
B = OUT.replace(u'\n', u'\r\n').encode('utf-8')
io.open(SRC, 'wb').write(B)
print(u'冊寫畢：%dB｜CRLF %d｜bareCR %d｜sha %s ➔ %s' % (
    len(B), B.count(b'\r\n'), B.count(b'\r') - B.count(b'\r\n'), SHA0,
    hashlib.sha256(OUT.encode('utf-8')).hexdigest()[:12]))
