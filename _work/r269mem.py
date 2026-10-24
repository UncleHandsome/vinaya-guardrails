# -*- coding: utf-8 -*-
"""269 輪・帳二：記憶層現況隨本輪更新（二十九年？非也——第 269 輪・二十九目・八尺・積輪 19）。

判式之正（268 自犯之落地）：附加式 patch 後 count(old) 之期望＝new 內所含 old 的次數，
   故斷言寫 `count(new)==1 且 count(old)==new.count(old)`——不誤報『未套』，也不放過『真未套』。
用法：python -X utf8 _work/r269mem.py [apply]
"""
import io
import os
import sys

MEM = os.path.join(os.path.expanduser(u'~'), u'.qoder', u'projects',
                   u'C--Users-lionc-OneDrive-----------------', u'memory')
P1 = os.path.join(MEM, u'project-round31-state.md')
P2 = os.path.join(MEM, u'MEMORY.md')

PAIRS = [
    (P1, u'description: 戒律分析專案現況（第 268 輪）', u'description: 戒律分析專案現況（第 269 輪）'),
    (P1, u'**9,338 行・966,940 B・SHA `02ac8be6433f`**', u'**9,340 行・968,278 B・SHA `06fba4dd5fa6`**'),
    (P1, u'（v39chk 28 尺／v39quote 卡身逐字', u'（v39chk **29 目**／v39quote 卡身逐字'),
    (P1, u'**今量：28/28・卡身 116/116', u'**今量：29/29・卡身 116/116'),
    (P1, u'・27 目 457 可判 0 報・28 目無號形制 0。**',
         u'・27 目 457 可判 0 報・28 目無號形制 0・**29 目黑話與官僚代號 40 詞 0 見**；'
         u'26／28／29 三禁今掃 `in_page`（凡印得出者，**含圍欄 562 行**），以 markdown 記號為鑰者仍用 `in_print`。**'),
    (P1, u'`v39chk.py`（形制與數目 28 目，', u'`v39chk.py`（形制與數目 29 目，'),
    (P1, u'（記錄檔簡形之逐枚改正與掃描，排除「」『』反引號之供狀）**、',
         u'（記錄檔簡形之逐枚改正與掃描，排除「」『』反引號之供狀）**、'
         u'**`r269fix.py`（25 項改名：解耦➔分立・模組➔範疇／對治功能・甲乙丙➔三層之名・存檔卡➔僧事日誌）、'
         u'`r269apx.py`（凡例兩處歸實態 5 項）、`r269neg.py`（三道植詞負測）、`r269probe.py`＋`r269site.py`'
         u'＋`r269mark.py`＋`r269jarg.py`（外路第四報告逐條對兩版之量）、`r269simp.py`・`r269chk.py`（帳修與刀後自查）**、'),
    (P1, u'**積輪 18・候令出冊**', u'**積輪 19・候令出冊**'),
    (P2, u'**第 268 輪止（2026-10-20）**', u'**第 269 輪止（2026-10-20）**'),
    (P2, u'不變量 28/28・卡身逐字 116/116', u'不變量 29/29・卡身逐字 116/116'),
    (P2, u'・案號↔案名 457/0・無號指針 0・**節級指針 31／錯靶 0／未證 2**',
         u'・案號↔案名 457/0・無號指針 0・**節級指針 31／錯靶 0／未證 2・黑話與官僚代號 40 詞 0**'),
    (P2, u'・六度補尺之盲（263 卡外逐字・264 範圍引卷・265 行號・266 案號與案名・267 名不可辨故禁其形＋27 目放寬容空格與卷首・'
         u'**268 第 10 目只問節號可達而不問靶對不對，遂立第八尺**）・積輪 18 候令重建',
         u'・六度補尺之盲（263 卡外逐字・264 範圍引卷・265 行號・266 案號與案名・267 名不可辨故禁其形＋27 目放寬容空格與卷首・'
         u'**268 第 10 目只問節號可達而不問靶對不對，遂立第八尺**）・'
         u'**269 外路第四報告八項：四屬 ver38 幽靈、四屬今冊實病（➔第 29 目『黑話與官僚代號』之禁，'
         u'並把形制三禁改掃含圍欄之紙面）；又挖出凡例兩處宣稱與實態不合**・積輪 19 候令重建'),
]
t = {}
for p, _o, _n in PAIRS:
    if p not in t:
        t[p] = io.open(p, encoding=u'utf-8').read()
bad = [(os.path.basename(p), old[:38], t[p].count(old)) for p, old, _n in PAIRS if t[p].count(old) != 1]
print(u'合 %d 項・錨不合 %d' % (len(PAIRS), len(bad)))
for x in bad[:8]:
    print(u'   %s｜命中 %d｜%s' % (x[0], x[2], x[1]))
if bad:
    sys.exit(2)
if u'apply' not in sys.argv:
    for p, old, new in PAIRS:
        print(u'  %-26s 舊:%s' % (os.path.basename(p), old[:52]))
    print(u'乾跑，未寫入。')
    sys.exit(0)
for p, old, new in PAIRS:
    t[p] = t[p].replace(old, new, 1)
for p in t:
    io.open(p, 'w', encoding=u'utf-8', newline=u'').write(t[p])
back = {p: io.open(p, encoding=u'utf-8').read() for p in t}
nok = []
for p, old, new in PAIRS:
    exp = new.count(old)
    if not (back[p].count(new) == 1 and back[p].count(old) == exp):
        nok.append((os.path.basename(p), old[:28], back[p].count(old), exp))
print(u'已寫入 %d 項・回讀不符 %d' % (len(PAIRS), len(nok)))
for x in nok[:6]:
    print(u'   %s｜舊實 %d／期望 %d｜%s' % x)
sys.exit(1 if nok else 0)
