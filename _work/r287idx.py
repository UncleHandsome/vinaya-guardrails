# -*- coding: utf-8 -*-
"""287・MEMORY.md 指標行改帳（一行・唯讀式替換，寫檔只在一處）。"""
import io

P = u'C:/Users/lionc/.qoder/projects/C--Users-lionc-OneDrive-----------------/memory/MEMORY.md'
raw = io.open(P, encoding='utf-8').read()
OLD = u'**第 286 輪止（2026-10-26）**：ver39 正本 **8,272 行・sha256 `ab8d6c6149a5`**・'
NEW = u'**第 287 輪止（2026-10-26）**：ver39 正本 **8,272 行・sha256 `83e7a32a2f31`**・'
assert raw.count(OLD) == 1, raw.count(OLD)
raw = raw.replace(OLD, NEW)

A = u'核卷 133/0/18・節級 38/38'
assert raw.count(A) == 1
raw = raw.replace(A, u'核卷 134/0/18・節級 39/39・逐字段 152（命中 115）')

B = u'**積輪 0**（286 重建：影印・螢幕各 **261 頁**'
assert raw.count(B) == 1
raw = raw.replace(B, u'**積輪 0**（287 重建：影印・螢幕各 **261 頁**')

C = u'286 收外路第十四報告兩批'
assert raw.count(C) == 1
tail = (u'287 收外路第十五報告兩批（廿六事：真病廿三・偽病灶六・須裁三）——冊身卅一刀：'
        u'自指尾語八枚除・指針四歸位・說戒小界引文歸真（標『說戒犍度』乃外來篇題）・'
        u'案 25 存外來卷三十八之說（核合 133➔134）案 69 記不相容故不取・僧物兩套四分各標其界・'
        u'白二遞歸改程序裁・四署降為本冊自律・微過分麁輕・前七章去世俗法專名；'
        u'偽病灶六俱以量駁（四軸 24 枚宣稱全合・果葉實屬第四分・全書無『第九章』）；'
        u'須裁：ver38 五件迎回（133 台帳・29 稱重・附錄B・五大 SOP・F-2）與矩陣升至 102 行之議。')
raw = raw.replace(C, tail + C)

io.open(P, 'w', encoding='utf-8', newline='\n').write(raw)
print(u'指標行已改｜檔長 %d 字' % len(raw))
