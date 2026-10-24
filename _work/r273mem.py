# -*- coding: utf-8 -*-
"""273 輪・記憶三層之改帳（快照・索引・器戒）。錨以 escape 構者皆經碼位實測（積 U+7A4D・輪 U+8F2A）。"""
import io
import os

PRJ = os.path.join(os.path.expanduser(u'~'), '.qoder', 'projects',
                   u'C--Users-lionc-OneDrive-----------------', 'memory')
USR = os.path.join(os.path.expanduser(u'~'), '.qoder', 'memory')


def sub(p, pairs, tag):
    t = io.open(p, encoding=u'utf-8').read()
    for old, new in pairs:
        n = t.count(old)
        assert n == 1, u'%s｜錨非一（%d）：%s' % (tag, n, old[:30])
        t = t.replace(old, new)
    io.open(p, 'w', encoding=u'utf-8').write(t)
    print(u'%s 已改 %d 處' % (tag, len(pairs)))


# ── ① 快照：印面今制整行重寫
P1 = os.path.join(PRJ, 'project-round31-state.md')
t = io.open(P1, encoding=u'utf-8').read()
L = t.split(u'\n')
i = next(k for k, l in enumerate(L) if l.startswith(u'**\u7a4d\u8f2a 22'))
NEW = (u'**印面今制（第 273 輪奉令重建，四式俱出）**：影印版與螢幕版各 **302 頁**（PDF 7,418／7,421 KB・DOCX 各 521 KB，在 `_print/`）；'
       u'**大綱 221 條＝目錄印出 221 條・未定位 0**——舊器 `build39.build_outline` 以 `disp` 單鑰去重，'
       u'曾把**同名跨級**者（第六章九個組題之 H2 與附錄四如鏡其題之 H3）靜默擲去而自報『定位失敗 0』，'
       u'273 改鑰為 `(lvl, disp)`、呼出三值、每式必印『帳』且校 `印出－入＝miss＋dup`（`_work/r273fix.py`）。'
       u'**重建後另跑 `_work/r273face.py 列印｜螢幕`（印面五量，獨立於 builder）**：甲・大綱其頁確見其題 221/221、'
       u'乙・頁腳號＝物理頁 相符 301／不合 0／無頁號 1（封面）、丙・圍欄 43 段同頁 42＋**超鎖頁閾如實不鎖 1**'
       u'（L2693・62 行；判式逕讀產器之源，改閾即隨動）、丁・附錄 H1 七篇俱在（附錄六分上・下兩篇）、'
       u'戊・圍欄字級最細 9.33pt／9pt 以下 0 段；負測 `_work/r273faceneg.py` 兩道俱中（移靶→甲點名其題・插空白頁→乙報不合 301）。'
       u'**積輪 0**；往後非奉令不出冊，奉令方 `python _print/build39.py full`（一行驗封面之數：`python _print/build39.py meta`）。')
L[i] = NEW
assert not any(l.startswith(u'**\u7a4d\u8f2a ') for l in L)
t = u'\n'.join(L)
io.open(P1, 'w', encoding=u'utf-8').write(t)
print(u'① 快照之印面今制已換｜行 %d' % (i + 1))

# ── ② 索引行
P2 = os.path.join(PRJ, 'MEMORY.md')
sub(P2, [(u'\u7b2c 272 \u8f2b\u6b62\uff082026-10-20\uff09', u'\u7b2c 273 \u8f2b\u6b62\uff082026-10-20\uff09'),
         (u'\u7a4d\u8f2a 22 \u5019\u4ee4\u91cd\u5efa',
          u'**273 奉令重建四式（影印・螢幕各 302 頁）：器病一枚——大綱去重之鑰漏同名跨級九條而自報『定位失敗 0』，'
          u'改鑰 `(lvl,disp)` 並必印『帳』校其平；新器 `_work/r273face.py` 立印面五量（甲大綱・乙頁腳・丙圍欄同頁・丁附錄・戊字級）俱中，'
          u'負測 `_work/r273faceneg.py` 兩道如所期**・積輪 0（四式已出）')], u'②')

# ── ③ 器戒：第四十六度
P3 = os.path.join(USR, 'feedback-self-checkers-must-measure-reality.md')
t3 = io.open(P3, encoding=u'utf-8').read()
assert t3.count(u'\u7b2c\u56db\u5341\u4e94\u5ea6') == 1
TAIL = (u'\n\n**第四十六度・自驗之數不覆跳過之數（2026-10-20・戒律分析第 273 輪）**：'
        u'建冊器自報『目錄條目 221・定位失敗未入者 0』，兩數各自皆真，合看卻瞞人——'
        u'`build_outline` 在去重時 `continue` **不計數**，故大綱實入 212 條而日誌全無痕。'
        u'**凡器中有跳過（continue／豁免／去重／篩後丟棄）者，其數必当场印出，並校一恒等式**'
        u'（本輪立：`印出－入 ＝ miss＋dup`，不平即印 ⚠）——只印各分段之數而不校其合，仍等於無帳。'
        u'又：`disp` 單鑰之去重把**同名跨級**（第六章 H2 與附錄四 H3）視作重出，'
        u'此即『尺之單位須與文之單位同寬』之印面版——**去重之鍵的寬度亦是口徑**，須含層級。'
        u'治則同 272：**印面亦須有独立之器**（`_work/r273face.py` 五量：大綱之頁確見其題・頁腳號＝物理頁・'
        u'圍欄起訖同頁・附錄俱在・字級下限），且**其閾逕讀產器之源**（改閾即隨動，不兩抄），'
        u'新器第一跑即負測（移靶→甲點名、插空白頁→乙報不合），未負測不入帳。')
io.open(P3, 'w', encoding=u'utf-8').write(t3 + TAIL)
print(u'③ 器戒第四十六度已附')
