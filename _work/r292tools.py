# -*- coding: utf-8 -*-
"""292・器刀（v39chk 立第 38 目『印面無退位之名』，自對合順移 39；牙列配針 38）。

作器之律（歷輪之誡）：先量禁形今在印面殘幾枚（_work/r292ban.py 已量：俱零，次碼形唯存於反引號圖例），
再立法禁；新目須（一）目名為常量，（二）try／except 兩支同名，（三）管轄自印，（四）有針可逮。
改他檔只以唯一錨點逐條替換，插段以整行錨定位；改畢 ast 復核並數相鄰諸块之存在。
"""
import ast
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, u'_work')
APPLY = os.environ.get(u'R292APPLY') == u'1'

CHK = os.path.join(WORK, u'v39chk.py')
TEETH = os.path.join(WORK, u'r272teeth.py')

NEW = r'''# ── 38：印面無退位之名（第 292 輪・奉外路第七報告『七大刀口』與作者「全做」之令而立）
#   口徑：名制一改，舊名即入禁形。本目所禁者乃本書歷版用過、今已退位之名，非錯字（第 35 目不識）、
#         非簡形（第 21 目不識）、非黑話（第 29 目不識）——後人若把舊名貼回，唯此目能紅。
#         （形制禁令＝把人工覆核換成機器可驗之約，見 267 輪『幽靈名之治在禁形』之例。）
#   所禁：『憲綱』（292 還三十二字於『略戒心印』，全書 30 枚已退）・『三鏡／第一鏡／第二鏡／第三鏡』
#         （292 併入『腳下三問』與『夜半四照』，不另立隨身口訣）・『J-』『現-』（四境演繹判例今作
#         現01〜現04，去連字號之工程遺跡）・『調部深描』（292 改稱『調部專題』；唯禁全串，
#         『經典地標深描』與『病理學深描』乃第六章與第一章之自制，不在禁列）・
#         〔案例 NN ／ 遮MM〕之斜線次碼（292 自正文退入附錄四〔新舊次碼對照〕，正文純號）。
#   唯所不校：反引號內之圖例——凡例與對照節各以舊形示例，是『說明舊形之相』而非『使用舊形』。
#   管轄自印：禁形幾類・印面幾行・命中幾處（管轄歸零即該目自己現形，五十二度）。
try:
    _BAN = [u'憲' + chr(0x7DB1), u'三鏡', u'第一鏡', u'第二鏡', u'第三鏡',
            u'J-', u'現-', u'調部' + chr(0x6DF1) + chr(0x63CF),
            u'〔案例 \\d+ ?/ ?(?:遮|僧|開)']
    _RXS = [re.compile(p) for p in _BAN]
    _b, _nrow = [], 0
    for i, l in enumerate(LINES):
        if not in_page(i):
            continue
        _nrow += 1
        s = re.sub(u'`[^`]*`', u'', l)                  # 圖例不在此禁
        for rx in _RXS:
            for m in rx.finditer(s):
                _b.append((i + 1, u'禁形『%s』' % m.group(0)[:22]))
    chk(u'印面無退位之名（歷版名制之禁形）', sorted(set(_b)),
        u'禁形 %d 類・印面 %d 行・命中 %d' % (len(_RXS), _nrow, len(_b)))
except Exception as e:
    chk(u'印面無退位之名（歷版名制之禁形）', [(u'尺自身出錯：%s' % e,)])

'''

NEEDLE = '''

@plant(38)
def p38name():
    """292・退位名制之植：把已改名之『略戒心印』貼回舊名『略戒憲綱』。
       （舊名非錯字・非簡形・非黑話，歷尺俱不識——唯第 38 目能紅，針尖單軸。）"""
    L = list(BASE)
    old = u'三十二字略戒心印'
    i = find_line(lambda l, idx: old in l)
    assert L[i].count(old) == 1, u'38 植錨非一'
    L[i] = L[i].replace(old, u'三十二字略戒' + chr(0x61B2) + chr(0x7DB1))
    return L, i, u'舊名『憲綱』貼回一行（第 38 目之植）'

'''


def rd(p):
    return io.open(p, encoding='utf-8').read()


def wr(p, s):
    ast.parse(s)
    if APPLY:
        io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
    print(u'  %s：%s（ast 過）' % (u'落盤' if APPLY else u'乾跑未寫', os.path.basename(p)))


# ── v39chk：新目前置，自對合順移 ──────────────────────────────────
s = rd(CHK)
ANCH = u"# ── 38：尺亦須被尺量"
assert s.count(ANCH) == 1, u'自對合之錨命中 %d' % s.count(ANCH)
assert s.count(u'288 順移為 38') == 1, u'順移註非一'
s = s.replace(ANCH, NEW + ANCH)
s = s.replace(u'288 順移為 38', u'288 順移 38、292 立禁形目而順移為 39')
for keep in (u"chk(u'目數自對合", u"chk(u'款級指針之名實對合", u"chk(u'章級 H1 一章一條",
             u"chk(u'印面無退位之名（歷版名制之禁形）", u'_BAN = ['):
    assert s.count(keep) >= 1, u'相鄰諸块走失：%s' % keep
assert s.count(u"chk(u'印面無退位之名（歷版名制之禁形）") == 2, u'兩支不同名'
wr(CHK, s)

# ── r272teeth：針 38 配新目，自對合之針順移至 39 ───────────────────
t = rd(TEETH)
for old, new, lab in [
    (u'PLANTS[38] = p32', u'PLANTS[39] = p32', u'自對合之針順移 39'),
    (u"EXTRA = {38: [(u'32b', p32b)]", u"EXTRA = {39: [(u'32b', p32b)]", u'EXTRA 同順移'),
]:
    assert t.count(old) == 1, u'%s：錨命中 %d' % (lab, t.count(old))
    t = t.replace(old, new)
ANCH2 = u'@plant(36)'
assert t.count(ANCH2) == 1, u'插針錨命中 %d' % t.count(ANCH2)
t = t.replace(ANCH2, NEEDLE.lstrip(u'\n') + u'\n' + ANCH2)
for keep in (u'@plant(38)', u'def p38name', u'@plant(37)', u'def p37name', u'@plant(36)',
             u'def p36h1', u'PLANTS[39] = p32', u'EXTRA = {39:'):
    assert keep in t, u'牙列相鄰走失：%s' % keep
wr(TEETH, t)
print(u'APPLY=%s（以 R292APPLY=1 落盤）' % APPLY)
