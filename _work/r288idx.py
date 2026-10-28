# -*- coding: utf-8 -*-
r"""288・MEMORY.md 索引行改帳。"""
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
P = os.path.join(MEM, u'MEMORY.md')
raw = io.open(P, encoding='utf-8').read()

OLD = u'**第 287 輪止（2026-10-26）**：ver39 正本 **8,272 行・sha256 `83e7a32a2f31`**'
NEW = u'**第 288 輪止（2026-10-26・奉第四次親裁）**：ver39 正本 **8,272 行・sha256 `7ce1dbbd806f`**'
assert raw.count(OLD) == 1, raw.count(OLD)
raw = raw.replace(OLD, NEW)

A = u'牙列 37 目 39 針逮 39'
assert raw.count(A) == 1, u'A：%d' % raw.count(A)
raw = raw.replace(A, u'牙列 38 目 40 針逮 40')

B = u'**積輪 0**（287 重建：影印・螢幕各 **261 頁**'
assert raw.count(B) == 1
raw = raw.replace(B, u'**積輪 0**（288 重建：影印・螢幕各 **261 頁**')

C = u'287 收外路第十五報告兩批'
assert raw.count(C) == 1
HEAD = (u'288 奉第四次親裁收四組：甲組五件俱結（A1 不迎 133 台帳而**落凡例第二宣告**『總帳一以附錄四 102 案為準』、'
        u'A2 29 稱重／A3 附錄B 19 則／A5 F-2 俱不迎、A4 依裁先取證➔ver38 實存而今缺失凡四已列表候裁）；'
        u'乙組維持現狀（矩陣 76 行分工・J 序乃歷版之次・次碼 54 枚）；'
        u'丙組 C1 頁眉暫緩・C2 試 orphans/widows 3➔2 只移一條目錄 1 頁而 p85／p221 底緣未動反添 p216 ➔ 還原而**安受留白**；'
        u'丁組 D6 立尺＝v39chk 新第 37 目『款級指針之名實對合』（管轄：三級 3・二級 37・帶掛名 1；紅時點名該款實題），'
        u'自對合順移 38、牙列新針 37 逮 40 欠 0；二級試校已擲（卷首索引之撮述 2 枚屬偽陽）。'
        u'冊身兩刀：第五章第五節導引盒款號歸實（款一至八／款九至十一）・凡例增二宣告。'
        u'⚠自犯：量過而未刀亦是債（287 查實未入刀）・規則未命中即假試驗（`body.print-copy` 不存在）。')
raw = raw.replace(C, HEAD + C)

bad = sorted({c for c in raw if c in SIMPS and c not in BOOK})
print(u'索引簡形：%s' % (u''.join(bad) or u'無'))
for c in bad:
    j = raw.find(c)
    print(u'   %s｜…%s…' % (c, raw[max(0, j - 22):j + 12].replace('\n', u' ')))
io.open(P, 'wb').write(raw.encode('utf-8'))
print(u'索引已改：%d 行' % len(raw.split('\n')))
