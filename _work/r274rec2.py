# -*- coding: utf-8 -*-
"""274 輪・立帳②：SOP 今制加積輪之實・記憶三層隨之（插入之文直打漢字，落盤後以碼位掃）。"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRJ = os.path.join(os.path.expanduser(u'~'), '.qoder', 'projects',
                   u'C--Users-lionc-OneDrive-----------------', 'memory')
USR = os.path.expanduser(u'~') + u'/.qoder/memory'


def sub(path, pairs, tag):
    t = io.open(path, encoding=u'utf-8').read()
    for old, new in pairs:
        n = t.count(old)
        assert n == 1, u'%s｜錨非一（%d）：%s' % (tag, n, old[:26])
        t = t.replace(old, new)
    io.open(path, 'w', encoding=u'utf-8').write(t)
    print(u'%s｜改 %d 處' % (tag, len(pairs)))


# ── ① SOP 今制：積輪之實
sub(os.path.join(ROOT, u'列印SOP.md'),
    [(u'**積輪 0**（四式已出）；往後非奉令不出冊，再動冊身則再積。',
      u'往後非奉令不出冊，再動冊身則再積——**第 274 輪換入第一〜三章（+93 行），今積輪 1，四式停在 273 輪之 302 頁，候令重建**（'
      u'重建後須以 `_work/r273face.py` 覆核：新章多兩段圍欄，跨頁與細字之判或有變動）。')], u'①')

# ── ② 快照：正本・九尺通道・積輪・下一軸
P1 = os.path.join(PRJ, 'project-round31-state.md')
L = io.open(P1, encoding=u'utf-8').read().split(u'\n')
i = next(k for k, l in enumerate(L) if l.startswith(u'**正本**'))
L[i] = (u'**正本**：根目錄 `ver39四分律_起心動念心智分析框架_修正版.md`（**9,432 行・986,152 B・SHA `9821c90fb52c`**・'
        u'案例卡 102・補遺 15・圍欄 45 段（274 輪換入第一〜三章後由 43 ➔ 45）・'
        u'ch1-3 = L435〜L2077（1,643 行））；`_tk.SRC` 取最高版號，然 `_tk` 諸閘之錨仍指 ver38 字面 ⇒ **新冊之證唯在下列九尺**。')
j = next(k for k, l in enumerate(L) if l.startswith(u'**一行驗全冊**'))
L[j] = L[j].replace(u'（v39chk **31 目**／', u'（v39chk **31 目**／**274 輪起 v39quote2・v39volchk・v39volrange・v39secref 四尺可帶檔參數＝試跑通道（不帶參與歷輪逐字同）**，未換冊而能量新稿；／')
t = u'\n'.join(L)
assert u'9,432 行' in t and u'試跑通道' in t
io.open(P1, 'w', encoding=u'utf-8').write(t)
print(u'② 快照已改')

# ── ③ 快照末段：積輪與下一軸
sub(P1, [(u'**積輪 0**；往後非奉令不出冊，奉令方 `python _print/build39.py full`（一行驗封面之數：`python _print/build39.py meta`）。',
          u'**積輪 1**（第 274 輪換入 ch1-3・+93 行，四式停在 302 頁）；奉令方 `python _print/build39.py full`'
          u'（一行驗封面之數：`python _print/build39.py meta`），重建後另跑 `_work/r273face.py 列印｜螢幕`。')], u'③')
t = io.open(P1, encoding=u'utf-8').read()
t = t.rstrip(u'\n') + u'\n\n**第 274 輪・換入新稿之第一〜三章**（作者貼上 1,816 行）：' + \
    u'清殘跡 11 段 163 行・第二章三篇合為一・解耦➔分立・『某某禁令』➔禁約 3 處・表列兩枚無著之號改歸本章『檢核案一／二』・' + \
    u'263 之拼接引文換回已證二法全文（自正本 L1926 切片帶入）；四尺加試跑通道，**未換先以假冊跑五尺**（唯一之紅＝目錄不指空兩條，一改題一除目）；' + \
    u'換以 `_work/r274swap.py`（備份＋一步回退）。**九尺全綠**（卡外宣稱 147・未標界 0・節級 32／錯靶 0／未證 3・牙列 32 針俱逮）。' + \
    u'**盈虛如實記**：舊章獨有 386 長行退（其中 137 行含歷輪已證之「」引文）、新獨 408 行、ch1-3 案例指針 70➔41（新稿以白描代外鍵，義理得而導航失）。' + \
    u'**下一軸**：『名須見於本號卡身』之**歸屬面尺**（prototype 在 `_work/r274anch.py`，可立為第 32 目，先定撮述名之寬窄口徑）。\n'
io.open(P1, 'w', encoding=u'utf-8').write(t)
print(u'③b 快照加 274 段')

# ── ④ 索引行
sub(os.path.join(PRJ, 'MEMORY.md'),
    [(u'**第 273 輪止（2026-10-20）**：ver39 正本 9,340 行・968,565 B・SHA `ec1bd4242914`',
      u'**第 274 輪止（2026-10-24）**：ver39 正本 9,432 行・986,152 B・SHA `9821c90fb52c`（第一〜三章已换新稿・圍欄 45）'),
     (u'**・積輪 0（四式已出）',
      u'・**274 奉命換入新稿 ch1–3**：清交付殘跡 11 段（163 行）・第二章三篇合為一・解耦➔分立・某某禁令➔禁約 3・'
      u'表列兩枚無著之號改歸『檢核案』（第 27 目遇短描即盲，今以**卡身**覆核定讞）・263 拼接引文換回已證二法全文；'
      u'**四尺加試跑通道**（可帶檔參數，不帶參與歷輪逐字同）→ 未換先以假冊跑五尺，唯一紅在目錄兩條；'
      u'換器先備份＋SHA 一步回退。九尺全綠（卡外 147・未標界 0・節級 32／錯靶 0／未證 3・牙列 32 針俱逮）・'
      u'**盈虛：舊 386 長行退（含 137 行已證引文）、新獨 408、ch1-3 指針 70➔41**・積輪 1 候令重建')], u'④')

# ── ⑤ 器戒：試跑通道之戒
P3 = os.path.join(USR, 'feedback-self-checkers-must-measure-reality.md')
t3 = io.open(P3, encoding=u'utf-8').read()
assert u'第四十七度' not in t3
TAIL = (u'\n\n**第四十七度・尺要能量『將欲換入之文』，不是只量已入之文（2026-10-24・第 274 輪）**：'
        u'作者貼上第一〜三章新稿命我換入。舊制下四尺（v39quote2／v39volchk／v39volrange／v39secref）硬讀 `_tk.MAIN_LINES`，'
        u'於是我只能**換了才知道紅在哪**——而換是一次性覆蓋 1,550 行的大動作，紅了等於病已入體。'
        u'治：給尺加**可選路徑參數**（試跑通道），把「卷首＋新章＋第四章以後」拼成假冊先跑五尺；'
        u'果然唯一之紅在目錄（新章改題、旧目指空），**在紙上治完才入正本**。'
        u'配套三則：① 通道之負測＝不帶參時輸出與歷輪逐字相同（否則通道本身是新變數）；'
        u'② 換冊器須先立**行序列等長式**與**前後綴相等**雙證（卷首與第四章以後一字未動），並先備份＋記 SHA 作一步回退；'
        u'③ 行界一律以標題**动态求得**——我硬記 436／1985，目錄除目一行即全書位移，器自止而不誤傷（錨不中即停之利）。'
        u'另立一筆帳：**換血必有所失**（舊章獨有 386 長行退，其中 137 行含歷輪逐字回填之已證引文；案例指針 70➔41）——'
        u'如實寫入日誌與 SOP，不假裝無損；作者要的是新稿，代價由帳本承之。')
io.open(P3, 'w', encoding=u'utf-8').write(t3 + TAIL)
print(u'⑤ 器戒第四十七度已附')
