# -*- coding: utf-8 -*-
"""r177term.py —— 術語異形族之分布計數（第 177 輪立，待診軸：只報稀形，不判成病）。

為什麼要有：177 輪掃『兩部僧／第〔10〕問』即由此器逮得——異形之害不止美觀，
**凡以『形』取鑰之檢（如 `qindex` 取半形 [N]），形制一亂即驗器之盲**。
為什麼只是待診：某形是『異名』還是『別物』，須讀文意方能判——
『隨身三鏡』（第三章隨身尺）與『隨身三印卡』（結語體·用·息）二物也；
『二百五十條』之『條』是『二百五十條繩索』之量詞；『六閘門』『六領域』屬有據之略式。
故本器只列『印面稀形而正形大成』之可疑者，**判否由人**，永不升為閘（升即滿屏假陽性）。

已讀而留（存照，免後人重議）：『八正理』與同句『六閘門』成偶句之略式；『三十二字憲綱』與
『三十二字略戒』二名各有所指（憲綱言其為全書之綱，略戒言其出七佛略戒之文）；『二諦』・
『真俗二諦』・『勝義諦』・『二諦法域』乃異稱非異名；『五十一法』之『法』係『心所六位
共五十一法』之正稱；『二百五十條』之『條』是『二百五十條繩索』之量詞；『四重／四根本／
四波羅夷／四根本重戒／四根本重罪』義各有側；『隨身三鏡』（第三章隨身尺）與『隨身三印卡』
（結語體·用·息）**二物也**；『六閘門』『六領域』『三十格矩陣』俱屬有據之概念略稱
（130 輪已裁：強改反生名相之擾，故留）。

另附『四制括號』之自查（此條已升不變量 82，此處僅供逐處明細）：
問序須半形 [N]、案號須六角〔遮N〕、通道須【…】、圖內切片須［…］。

用法：PYTHONPATH=. python -X utf8 _work/r177term.py [主檔副本]
退出碼：恆 0（待診）。
"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as t

ARGS = [a for a in sys.argv[1:] if not a.startswith('-')]
SRC = ARGS[0] if ARGS else u'ver38四分律_起心動念心智分析框架_修正版.md'
L = io.open(SRC, encoding='utf-8').read().split('\n')
BOT = t.bottom_lines()
FEN, op = set(), False
for i, l in enumerate(L):
    if l.lstrip().startswith(u'```'):
        op = not op
        FEN.add(i)
    elif op:
        FEN.add(i)
印面 = u'\n'.join(l for i, l in enumerate(L) if i not in BOT and i not in FEN)
全檔 = u'\n'.join(L)

FAMS = [
    [u'六重閘門', u'六閘門', u'六重心智閘門', u'六道閘門'],
    [u'八大正理', u'八正理'],
    [u'三十二字憲綱', u'三十二字略戒', u'略戒三十二字', u'三十二字'],
    [u'十六觀心問', u'十六問', u'夜半四問'],
    [u'五十一心所', u'五十一法'],
    [u'三十格矩陣', u'三十格檢索總表', u'三十格'],
    [u'四種諍', u'四諍', u'七滅諍法', u'七滅諍'],
    [u'白四羯磨', u'白二羯磨'],
    [u'二百五十戒', u'二百五十條'],
    [u'二部僧', u'兩部僧'],
    [u'四重', u'四根本', u'四波羅夷', u'四根本重戒', u'四根本重罪'],
    [u'隨身三鏡', u'三鏡', u'隨身三印', u'三印', u'隨身三印卡'],
    [u'舉罪五德', u'五德'],
    [u'三環自省', u'三環模型'],
    [u'二諦', u'真俗二諦', u'二諦法域', u'勝義諦'],
    [u'六大領域', u'六領域'],
]
print(u'── 術語族（印面／全檔）──')
rare = 0
for fam in FAMS:
    cnt = [(f, 印面.count(f), 全檔.count(f)) for f in fam]
    cnt = [c for c in cnt if c[2]]
    if not cnt:
        continue
    main = max(c[1] for c in cnt)
    line = u' ｜ '.join(u'%s %d/%d' % c for c in cnt)
    flag = u''
    for f, a, b in cnt:
        if a and a <= 3 and main >= 20:
            flag = u'   ← 稀形待讀'
            rare += 1
            break
    print(u'  %s%s' % (line, flag))

print(u'── 四制括號之形（已升不變量 82，此列明細）──')
for nm, rx in ((u'問序掛六角／全形／方頭', u'[〔［【]\\d+[〕］】]問'),
               (u'案號掛半形或全形', u'[\\[［【](?:遮|開|僧)\\d+[\\]］】]'),
               (u'通道掛純數字', u'【\\d+】')):
    hits = [(i + 1, m.group(0)) for i, l in enumerate(L)
            if i not in BOT and i not in FEN for m in re.finditer(rx, l)]
    print(u'  %-14s %d 處｜%s' % (nm, len(hits), hits[:4]))
print(u'稀形族計 %d（恆退 0——判否由人）' % rare)
