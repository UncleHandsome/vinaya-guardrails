# -*- coding: utf-8 -*-
"""273 輪・記憶三層之改帳②③（承 r273mem.py：① 印面今制已換）。

錨一律**直打漢字**（前器以 \\uXXXX 造『輪』字錯兩枚：U+8F2B『輫』與 U+8F2E『轉』——码位只防傳遞，不防我記錯）；
插入之文亦直打，落盤後以『新出之字 vs 前檔』一列認明。
"""
import io
import os

PRJ = os.path.join(os.path.expanduser(u'~'), '.qoder', 'projects',
                   u'C--Users-lionc-OneDrive-----------------', 'memory')
USR = os.path.join(os.path.expanduser(u'~'), '.qoder', 'memory')


def sub(p, pairs, tag):
    t = io.open(p, encoding=u'utf-8').read()
    io.open(p + u'.bak', 'w', encoding=u'utf-8').write(t)
    for old, new in pairs:
        n = t.count(old)
        assert n == 1, u'%s｜錨非一（%d）：%s' % (tag, n, old[:24])
        t = t.replace(old, new)
    io.open(p, 'w', encoding=u'utf-8').write(t)
    print(u'%s 已改 %d 處' % (tag, len(pairs)))


# ── ② 快照之頭與索引
P1 = os.path.join(PRJ, 'project-round31-state.md')
sub(P1, [(u'description: 戒律分析專案現況（第 272 輪）', u'description: 戒律分析專案現況（第 273 輪）'),
         (u'・印面未動、積輪 22 候令出冊', u'・印面四式俱出 302 頁、積輪 0'),
         (u'# 現況快照（截至 2026-10-20・第 272 輪）', u'# 現況快照（截至 2026-10-20・第 273 輪）')], u'②a')
P2 = os.path.join(PRJ, 'MEMORY.md')
sub(P2, [(u'**第 272 輪止（2026-10-20）**', u'**第 273 輪止（2026-10-20）**'),
         (u'・積輪 22 候令重建',
          u'・**273 奉令重建四式（影印・螢幕各 302 頁）：器病一枚——大綱去重之鍵只用 `disp`，'
          u'漏同名跨級九條（第六章 H2 與附錄四 H3）而自報『定位失敗 0』，改鍵為 `(lvl,disp)` 並每式必印『帳』校 `印出－入＝miss＋dup`；'
          u'新器 `_work/r273face.py` 立印面五量（甲・大綱其頁確見其題／乙・頁腳＝物理頁／丙・圍欄起訖同頁／丁・附錄俱在／戊・字級下限）俱中，'
          u'負測 `_work/r273faceneg.py` 兩道如所期（移靶→甲點名其題・冊首插空白頁→乙報不合 301）**・積輪 0（四式已出）')], u'②b')

# ── ③ 器戒：第四十六度
P3 = os.path.join(USR, 'feedback-self-checkers-must-measure-reality.md')
t3 = io.open(P3, encoding=u'utf-8').read()
io.open(P3 + u'.bak', 'w', encoding=u'utf-8').write(t3)
TAIL = (u'\n\n**第四十六度・自驗之數不覆跳過之數（2026-10-20・戒律分析第 273 輪）**：'
        u'建冊器自報『目錄條目 221』與『定位失敗未入者 0』，兩數各自皆真，合看卻瞞人——'
        u'`build_outline` 在去重時 `continue` **不計數**，故大綱實入 212 條而歷輪日誌全無痕。'
        u'**凡器中有跳過（continue／豁免／去重／篩後丟棄）者，其數必当场印出，並校一恒等式**'
        u'（本輪立：`印出－入 ＝ miss＋dup`，不平即印 ⚠）——只印各段之數而不校其合，仍等於無帳。'
        u'又：以 `disp` 單鍵去重，把**同名跨級**者（第六章九個組題之 H2 與附錄四如鏡其題之 H3）視作重出——'
        u'此即『尺之單位須與文之單位同寬』之印面版：**去重之鍵的寬度亦是口徑**，須含層級。'
        u'治則承 272 而推及印面：**印面亦須有独立之器**（`_work/r273face.py` 五量：大綱之頁確見其題・頁腳號＝物理頁・'
        u'圍欄起訖同頁・附錄俱在・字級下限），其閾**逕讀產器之源**（版寬・字級・行高・鎖頁上限自 `build39.py` 正则讀出，'
        u'改閾即隨動，不兩抄），且新器第一跑即負測（移靶→甲點名其題・插空白頁→乙報不合 301），未負測不入帳。'
        u'**再證 236 之別**：圍欄一段跨頁，初判為冊病，查產器方知是『超閾如實不鎖』之裁——**先查器則，再判冊病**。')
io.open(P3, 'w', encoding=u'utf-8').write(t3 + TAIL)
print(u'③ 器戒第四十六度已附')
