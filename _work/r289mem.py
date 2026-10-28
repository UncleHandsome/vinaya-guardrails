# -*- coding: utf-8 -*-
r"""289・記憶層入帳（狀態檔＋索引檔），寫畢掃簡形。"""
import io
import os
import sys

MEM = u'C:/Users/lionc/.qoder/projects/C--Users-lionc-OneDrive-----------------/memory'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, u'_work'))
import _simpmap as SM                                   # noqa: E402
import _simpdict as SD                                   # noqa: E402

SIMPS = set(getattr(SM, 'MAP', {})) | set(getattr(SD, 'MAP', {}))
BOOK = io.open(os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md'),
               encoding='utf-8').read()

P = os.path.join(MEM, u'project-round31-state.md')
raw = io.open(P, encoding='utf-8').read()

A = u'description: 戒律分析專案現況（第 288 輪・奉第四次親裁）'
assert raw.count(A) == 1
raw = raw.replace(A, u'description: 戒律分析專案現況（第 289 輪・外路第十六報告 CBETA 逐字比對）')

A2 = u'**8,272 行・sha256 7ce1dbbd806f**・**積輪 0（288 重建'
assert raw.count(A2) == 1, raw.count(A2)
raw = raw.replace(A2, u'**8,272 行・sha256 152486628736**・**積輪 1（289 八刀未出冊，奉令方建；'
                      u'288 重建')

H = u'# 現況快照（截至 2026-10-26・第 288 輪）'
assert raw.count(H) == 1
raw = raw.replace(H, u'# 現況快照（截至 2026-10-26・第 289 輪）')

ANCHOR = u'**第 288 輪・奉第四次親裁（甲乙丙丁四組）之收斂、立尺、重建與入帳**'
assert raw.count(ANCHOR) == 1
NEW = (u'**第 289 輪・外路第十六報告（CBETA 逐字比對六事）之文獻歸真**（起點 `7ce1dbbd806f`・'
       u'今 **8,272 行・`152486628736`**）：六事**俱真**（不同歷輪之偽病灶報告），八刀俱中（`r289cuts.py`）。'
       u'① **目連牽臂引文係混合**——『怪哉目連』『何乃造次』『我更不說戒』『汝等自共說戒』四語本地六十卷分段檔'
       u'**全無一文**，而報告所擬卷三十六原文四句（『汝今不應為後亦不應為』等）**俱各 1 見於 31-37 檔**'
       u'➔改引真逐字，混入四語如實記削（『前一句或出他部之律，後三語無從指實』），卷次依 287 約作存其說、'
       u'說戒犍度仍標外來篇題；② **波逸提第六十六條 卷十九➔卷十七**——本地只證至檔段 11-21（兩說俱相容），'
       u'治據乃**本冊自家之內部衝突**（L4770 第六十四條・L7740 第六十七條俱作卷十七，三條同群而 66 獨異）；'
       u'③ 閘門六『（原典卷次未標）』➔『卷五十七・毘尼增一』（五句俱見 50-60 檔，篇題『毘尼增一』本地語料實有 7 見）；'
       u'④⑤ 案 25・案 69 之『未細核』各**存其說而不升為主位卷號**（案 25 記卷三十八與卷四十五・人犍度二說俱與檔段相容；'
       u'案 69 前說不相容故不取、今說卷四十九・法犍度相容故存之），正文 L4767 羯磨段頭同步補界；'
       u'⑥ **《五支物主經》末句降為義撮『』＋引首自標『本地未收・照錄未覆核・次第依本書義理之便』**'
       u'（量得《中阿含》確不在本地收錄之列——`佛經/` 目錄無一檔含之）。'
       u'**今量**：逐字段 152➔**153**（命中 116）・核卷 **134➔136**／不合 0・未證 18 如舊・一案兩說 0・'
       u'不變量 38/38・牙列 40 針俱逮➔**十尺全綠**。**積輪 1**。'
       u'**自犯**：錨內分隔符第二犯（L4767 兩處俱 U+00B7『·』，我以 U+30FB『・』打字而 0 命中，乾跑現形）'
       u'——**凡帶『・／·』之錨須先印碼位或逕以 chr() 構造**；又：本帳先立備份 `_archive/備份/ver39.pre289.md` 而後落刀，'
       u'288 所立『先備份後落刀』之約今守。\n\n')
raw = raw.replace(ANCHOR, NEW + ANCHOR)

A3 = (u'**正本**：根目錄 `ver39…修正版.md`（**8,272 行・sha256 前 12 碼 `7ce1dbbd806f`**；'
      u'288 前（＝287 末）8,272 行／`83e7a32a2f31`')
assert raw.count(A3) == 1
raw = raw.replace(A3, u'**正本**：根目錄 `ver39…修正版.md`（**8,272 行・sha256 前 12 碼 `152486628736`**；'
                      u'289 前（＝288 末）8,272 行／`7ce1dbbd806f`，288 前（＝287 末）8,272 行／`83e7a32a2f31`')

A4 = u'**印面今制（276 建・284〜288 五度重建・積輪 0）**'
assert raw.count(A4) == 1
raw = raw.replace(A4, u'**印面今制（276 建・284〜288 五度重建・今積輪 1＝289 八刀未出冊）**')

bad = sorted({c for c in raw if c in SIMPS and c not in BOOK})
print(u'狀態檔新增簡形：%s' % (u''.join(bad) or u'無'))
io.open(P, 'wb').write(raw.encode('utf-8'))
print(u'狀態檔：%d 行' % len(raw.split('\n')))

Q = os.path.join(MEM, u'MEMORY.md')
s = io.open(Q, encoding='utf-8').read()
B1 = u'**第 288 輪止（2026-10-26・奉第四次親裁）**：ver39 正本 **8,272 行・sha256 `7ce1dbbd806f`**'
assert s.count(B1) == 1
s = s.replace(B1, u'**第 289 輪止（2026-10-26）**：ver39 正本 **8,272 行・sha256 `152486628736`**')
B2 = u'・**積輪 0**（288 重建：影印・螢幕各 **261 頁**'
assert s.count(B2) == 1
s = s.replace(B2, u'・**積輪 1**（289 八刀未出冊；上一次 288 重建：影印・螢幕各 **261 頁**')
B3 = u'核卷 134/0/18・節級 39/39・逐字段 152（命中 115）'
assert s.count(B3) == 1
s = s.replace(B3, u'核卷 136/0/18・節級 39/39・逐字段 153（命中 116）')
B4 = u'288 奉第四次親裁收四組'
assert s.count(B4) == 1
HEAD = (u'289 收外路第十六報告（CBETA 逐字比對六事，**俱真・八刀俱中**）：目連牽臂引文係混合'
        u'（四語本地全無・報告所擬卷三十六四句俱見 31-37 檔）➔歸真並記削語之由；'
        u'波逸提 66 條引卷 卷十九➔卷十七（據本冊 64・67 兩條俱作卷十七之內部衝突，非據外來表炫精確）；'
        u'閘門六『原典卷次未標』➔卷五十七・毘尼增一（篇題本地實有）；'
        u'案 25・案 69 之未細核各**存其說而不升主位卷號**；《五支物主經》末句**降為義撮『』**並自標未覆核'
        u'（《中阿含》本地未收）。今量：逐字 153（命中 116）・核卷 136・未證 18 如舊・十尺全綠。'
        u'⚠自犯：錨內分隔符 U+00B7 誤記為 U+30FB（第二犯，乾跑現形）。')
s = s.replace(B4, HEAD + B4)
bad2 = sorted({c for c in s if c in SIMPS and c not in BOOK})
print(u'索引新增簡形：%s' % (u''.join(bad2) or u'無'))
io.open(Q, 'wb').write(s.encode('utf-8'))
print(u'索引：%d 行' % len(s.split('\n')))
