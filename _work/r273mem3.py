# -*- coding: utf-8 -*-
"""273 輪・記憶收尾（快照之頭兩行・索引之一行・器戒一段）。

改以**行號定位**而非漢字為錨（前器三度以漢字構錨不中：『輪』之码位錯兩枚、長句有全半形之差）。
插入之文直打漢字，落盤後以『新出之字 vs 前檔』認明。
"""
import io
import os

PRJ = os.path.join(os.path.expanduser(u'~'), '.qoder', 'projects',
                   u'C--Users-lionc-OneDrive-----------------', 'memory')
USR = os.path.join(os.path.expanduser(u'~'), '.qoder', 'memory')

# ── ① 快照之 description 與標題行（行 3・行 8）
P1 = os.path.join(PRJ, 'project-round31-state.md')
L = io.open(P1, encoding=u'utf-8').read().split(u'\n')
assert L[2].startswith('description:') and '272' in L[2], L[2][:40]
assert L[7].startswith('# ') and '272' in L[7], L[7][:40]
L[2] = (u'description: 戒律分析專案現況（第 273 輪）：ver39 正本 9,340 行／案例 102 卡・'
        u'九尺合跑全綠（31 目＋牙列矩陣 32 針俱逮）・**四式已重建，影印與螢幕各 302 頁，'
        u'印面五量俱中（大綱 221＝目錄 221）・積輪 0**')
L[7] = u'# 現況快照（截至 2026-10-20・第 273 輪）'
io.open(P1, 'w', encoding=u'utf-8').write(u'\n'.join(L))
print(u'① 快照頭兩行已改')

# ── ② 索引：現況快照那一行補 273 之節並改積輪
P2 = os.path.join(PRJ, 'MEMORY.md')
t = io.open(P2, encoding=u'utf-8').read()
assert t.count(u'**第 272 輪止（2026-10-20）**') == 1
t = t.replace(u'**第 272 輪止（2026-10-20）**', u'**第 273 輪止（2026-10-20）**')
assert t.count(u'・積輪 22 候令重建') == 1
t = t.replace(u'・積輪 22 候令重建',
              u'・**273 奉令重建四式（影印・螢幕各 302 頁）：器病一枚——大綱去重之鍵只用 `disp`，'
              u'漏同名跨級九條（第六章九組題之 H2 與附錄四如鏡其題之 H3）而自報『定位失敗 0』，'
              u'改鍵為 `(lvl,disp)`、呼出三值、每式必印『帳』並校 `印出－入＝miss＋dup`；'
              u'新器 `_work/r273face.py` 立印面五量（甲・大綱其頁確見其題 221/221、乙・頁腳＝物理頁 301/0、'
              u'丙・圍欄 43 段同頁 42＋超閾如實不鎖 1、丁・附錄 7 篇俱在、戊・字級最細 9.33pt 無細字）俱中，'
              u'負測 `_work/r273faceneg.py` 兩道如所期（移靶→甲點名其題・冊首插空白頁→乙報不合 301）**・積輪 0（四式已出）')
io.open(P2, 'w', encoding=u'utf-8').write(t)
print(u'② 索引已補 273')

# ── ③ 器戒第四十六度
P3 = os.path.join(USR, 'feedback-self-checkers-must-measure-reality.md')
t3 = io.open(P3, encoding=u'utf-8').read()
assert u'\u7b2c\u56db\u5341\u516d\u5ea6' not in t3
TAIL = (u'\n\n**第四十六度・自驗之數不覆跳過之數（2026-10-20・戒律分析第 273 輪）**：'
        u'建冊器自報『目錄條目 221』與『定位失敗未入者 0』，兩數各自皆真，合看卻瞞人——'
        u'`build_outline` 在去重時 `continue` **不計數**，故大綱實入 212 條而歷輪日誌全無痕。'
        u'**凡器中有跳過（continue／豁免／去重／篩後丟棄）者，其數必当场印出，並校一恒等式**'
        u'（本輪立：`印出－入 ＝ miss＋dup`，不平即印 ⚠）——只印各段之數而不校其合，仍等於無帳。'
        u'又：以 `disp` 單鍵去重，把**同名跨級**者（第六章九個組題之 H2 與附錄四如鏡其題之 H3）視作重出——'
        u'此即『尺之單位須與文之單位同寬』之印面版：**去重之鍵的寬度亦是口徑**，須含層級。'
        u'治則承 272 而推及印面：**印面亦須有独立之器**（`_work/r273face.py` 五量：大綱之頁確見其題・頁腳號＝物理頁・'
        u'圍欄起訖同頁・附錄俱在・字級下限），其閾**逕取產器之源**（版寬・字級・行高・鎖頁上限自 `build39.py` 讀出，'
        u'改閾即隨動，不兩抄），且新器之第一跑即負測（移靶→甲點名其題・插空白頁→乙報不合 301），未負測不入帳。'
        u'**再證 236 之別**：圍欄一段跨頁，初判為冊病，查產器方知是『超閾如實不鎖』之裁（鎖之即生大塊空白）——'
        u'**先查器則，再判冊病**。')
io.open(P3, 'w', encoding=u'utf-8').write(t3 + TAIL)
print(u'③ 器戒第四十六度已附')
