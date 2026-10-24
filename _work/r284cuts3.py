# -*- coding: utf-8 -*-
"""284・補刀（三）：地標 03 案號列分『本案／參引對照』（48・55 自判唯波逸提，恐被讀作同刑），
   並入卷首之約，明『案號並列不謂同刑』。"""
import hashlib
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
APPLY = u'--apply' in sys.argv
T = io.open(BOOK, encoding=u'utf-8-sig').read()
sha = lambda x: hashlib.sha256(x.encode(u'utf-8')).hexdigest()[:12]
print(u'正本 %d 行・sha %s' % (len(T.split(u'\n')), sha(T)))

OLD1 = (u'*   **案號**：〔案例 16〕迦留陀夷七度試探・〔案例 48〕迦留陀夷三度移座・'
        u'〔案例 55〕迦留陀夷射殺群烏')
NEW1 = (u'*   **案號**：〔案例 16〕迦留陀夷七度試探（本案，僧殘）｜參引對照：〔案例 48〕迦留陀夷三度移座、'
        u'〔案例 55〕迦留陀夷射殺群烏（此二案自判唯波逸提，附此取對讀，非與本案同刑）')
assert T.count(OLD1) == 1, T.count(OLD1)
T = T.replace(OLD1, NEW1, 1)
print(u'  刀 一・地標 03 分本案與參引')

OLD2 = u'其易生誤會者已歸一（如案 02 標其支、案 44 齊其名）。）'
NEW2 = (u'其易生誤會者已歸一（如案 02 標其支、案 44 齊其名）。'
        u'三、一則地標並列數案者（如地標 03 以 16 為本案、48 與 55 為參引對照），'
        u'**並列不謂同刑**：刑名各以其處斷與附錄四之引卷為準。）')
assert T.count(OLD2) == 1, T.count(OLD2)
T = T.replace(OLD2, NEW2, 1)
print(u'  刀 二・卷首補『並列不謂同刑』之約')

print(u'改後 %d 行・sha %s' % (len(T.split(u'\n')), sha(T)))
if not APPLY:
    print(u'（乾跑・未落盤）')
    sys.exit(0)
io.open(BOOK, 'w', encoding=u'utf-8').write(T)
back = io.open(BOOK, encoding=u'utf-8-sig').read()
print(u'落盤訖・同=%s・sha %s' % (back == T, sha(back)))
