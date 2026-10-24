# -*- coding: utf-8 -*-
"""270 輪・帳二：SOP（今制＋本輪案內）與記憶層現況。一錨一斷言；附加式之期望值＝new.count(old)。
錨皆自實檔讀得（不憑憶），故先印命中數再改。
用法：python -X utf8 _work/r270sop.py [apply]
"""
import hashlib
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
raw = open(os.path.join(ROOT, NAME), 'rb').read()
SHA = hashlib.sha256(raw).hexdigest()[:12]
NL = raw.decode(u'utf-8-sig').count(u'\n') + 1
NLS = format(NL, u',d')
NBS = format(len(raw), u',d')
MEM = os.path.join(os.path.expanduser(u'~'), u'.qoder', u'projects',
                   u'C--Users-lionc-OneDrive-----------------', u'memory')
SOP = os.path.join(ROOT, u'列印SOP.md')
ST = os.path.join(MEM, u'project-round31-state.md')
IX = os.path.join(MEM, u'MEMORY.md')

ENTRY = (u'\n  **第 270 輪・自查自除：量而未刀者二軸，改約以從實者一軸**——269 改凡例第六節時新添一句'
         u'『凡用之處須自註分界』，**立約而未自量**：`_work/r270probe.py` 量得前七章以凡例自舉之鑰詞'
         u'（證據能力・管轄・迴避）為骨之節 **31 段，22 段無註**；`_work/r270narrow.py` 收窄口徑'
         u'（改取實定法專名十八詞）仍得 41 段而**偽陽過半**（『警』中於『警策』・『判決』中於『佛判』・'
         u'『稅』中於案例51『私度關逃稅』之律藏本事）⇒ **無可分別之口徑即無此約**（與 267『幽靈名與描述語同形』同科）。'
         u'另試『例示之詞須見於冊』（`_work/r270exem.py`）：可判 129 項・47 項唯此一見，覆核俱是偽陽'
         u'（『如市井頑童般』・『作如是言』・『如來主幹垂問』・『過急則掉』）——『如』一字多義，**此軸不可立尺，記而不立**。'
         u'**治＝約不可驗即改約**（`_work/r270fix.py` 1 項）：凡例作『此類語彙乃全書公堂喻之骨架，不逐處標記；'
         u'凡涉世俗實定法之具體制度（法條、時效、報告之義務、管轄之歸屬），其本域在第八章』，並如實記'
         u'『『詳見第八章』之自註今四見，俱在第四章』。刀後該約 0 見。**器**：第 10 目加網『**蒙上省寫**』'
         u'（『第八章第二節與第四節』省其章名乃中文常形，舊鑰只認全形，後項向在網外）；不以節為序之章（三・六）'
         u'如實報『節制不合』，不強判落空亦不默過；目名自報『蒙上省寫 5 處』・今 5 處 0 落空'
         u'（報行之序值經 `_ord`，漢字序數按 codepoint 排會成『一・三・二・四』——**排序亦是宣稱**）。'
         u'負測 `_work/r270neg.py` 兩道各證一枝：植『與第九節』→『省寫落空：第八章 無第九節（今有 一・二・三・四）』退 1・'
         u'植『詳見第三章第二節與第五節』→『不以節為序（節制不合）』退 1・正本 29/29；**兩枝皆須能響，只驗其一即該枝未證**。'
         u'自犯四則：① **立約未自量**（舊誡『立約須當場自量全書』自己踩之；新誡入檔：**凡立『凡…須…』式之約，'
         u'同日必以一口徑量其守得幾何，未量不准入凡例**）；② 偽陽過半之軸**棄其尺**而非降其閾；'
         u'③ 器身註自落英字『iform』一枚（覆讀現形，拉丁與簡形同罪）；④ 新文自落簡形六枚（处・当・场・变・须・写）'
         u'由廣單現形，逐枚帶錨改（`_work/r270simp.py`，並捎清 v39chk 舊註之须・最长・字体三枚）。'
         u'**今量：%s 行・%s B・SHA `%s`｜八尺全綠・不變量 29/29｜負測十一支俱中**。'
         u'⚠ 本輪動印面（凡例一句重寫），**積輪 20**。呈裁三項如 269，未動。' % (NLS, NBS, SHA))

PAIRS = [
    (SOP, u'269 之外路第四報告四項歸位並立『黑話與官僚代號』之禁（第 29 目，且把 26／28／29 三禁改掃**含圍欄之紙面**）'
          u'）**而 PDF 未重建**——奉令『修正不即出冊』，**積輪 19** 待令。',
     u'269 之外路第四報告四項歸位並立『黑話與官僚代號』之禁（第 29 目，且把 26／28／29 三禁改掃**含圍欄之紙面**）、'
     u'270 之自查自除（269 新立『凡用之處須自註分界』乃不可驗之約➔改約以從實）與第 10 目加『蒙上省寫』之網）'
     u'）**而 PDF 未重建**——奉令『修正不即出冊』，**積輪 20** 待令。'),
    (SOP, u'三十九版之查核公約今已自立（第 255～269 輪）', u'三十九版之查核公約今已自立（第 255～270 輪）'),
    (SOP, u'〔…〕通道標籤 52 種 55 見之去留・承 266／268 之兩項形制。',
     u'〔…〕通道標籤 52 種 55 見之去留・承 266／268 之兩項形制。' + ENTRY),
    (ST, u'description: 戒律分析專案現況（第 269 輪）', u'description: 戒律分析專案現況（第 270 輪）'),
    (ST, u'**9,340 行・968,278 B・SHA `06fba4dd5fa6`**・案例卡 102',
     u'**%s 行・%s B・SHA `%s`**・案例卡 102' % (NLS, NBS, SHA)),
    (ST, u'**積輪 19・候令出冊**', u'**積輪 20・候令出冊**'),
    (ST, u'**29 目黑話與官僚代號 40 詞 0 見**；',
     u'**29 目黑話與官僚代號 40 詞 0 見・第 10 目今兼護『蒙上省寫』5 處 0 落空**；'),
    (ST, u'、`r269simp.py`・`r269chk.py`（帳修與刀後自查）**',
     u'・`r269simp.py`・`r269chk.py`（帳修與刀後自查）**・'
     u'**`r270probe.py`／`r270narrow.py`（自查 269 之約守得幾何，二寬窄口徑俱不可立尺）・'
     u'`r270exem.py`（例示須見於冊——47 偽陽，記而不立）・`r270fix.py`（凡例改約 1 項）・'
     u'`r270ellip.py`（蒙上省寫之先驅量）・`r270neg.py`（兩枝負測）・`r270simp.py`（本帳之簡形淨）」'),
    (IX, u'**第 269 輪止（2026-10-20）**', u'**第 270 輪止（2026-10-20）**'),
    (IX, u'・積輪 19 候令重建',
     u'・**270 自查自除 269 所立之不可驗約（約不可驗即改約）・第 10 目加蒙上省寫之網**・積輪 20 候令重建'),
]
FILES = {}
for p, _o, _n in PAIRS:
    if p not in FILES:
        FILES[p] = io.open(p, encoding=u'utf-8-sig').read()
bad = [(os.path.basename(p), old[:38], FILES[p].count(old)) for p, old, _n in PAIRS
       if FILES[p].count(old) != 1]
print(u'合 %d 項・錨不合 %d' % (len(PAIRS), len(bad)))
for x in bad:
    print(u'   命中 %d｜%s｜%s' % (x[2], x[0], x[1]))
if bad:
    sys.exit(2)
if u'apply' not in sys.argv:
    print(u'乾跑（冊 %s 行・%s B・%s）。' % (NLS, NBS, SHA))
    sys.exit(0)
for p, old, new in PAIRS:
    FILES[p] = FILES[p].replace(old, new, 1)
for p, txt in FILES.items():
    io.open(p, 'w', encoding=u'utf-8', newline=u'').write(txt)
back = {p: io.open(p, encoding=u'utf-8-sig').read() for p in FILES}
nok = [(os.path.basename(p), old[:24], back[p].count(old), new.count(old))
       for p, old, new in PAIRS
       if not (back[p].count(new) == 1 and back[p].count(old) == new.count(old))]
print(u'已寫入 %d 項・回讀不符 %d' % (len(PAIRS), len(nok)))
for x in nok:
    print(u'   %s｜舊實 %d／期望 %d｜%s' % x)
