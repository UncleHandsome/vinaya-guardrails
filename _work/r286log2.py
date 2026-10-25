# -*- coding: utf-8 -*-
"""286・帳（純文字稿拼接版）：日誌加節・SOP 改印面條並立新條。"""
import hashlib
import io
import re
import sys

J = u'_archive/編年工程日誌.md'
O = u'列印SOP.md'
P = u'_work/r286para.txt'
APPLY = u'--apply' in sys.argv

raw = io.open(u'ver39四分律_起心動念心智分析框架_修正版.md', encoding=u'utf-8').read()
T = raw.replace(u'\r\n', u'\n')
SHA = hashlib.sha256(T.encode(u'utf-8')).hexdigest()[:12]
NROW = len(T.split(u'\n'))

para = io.open(P, encoding=u'utf-8').read().strip()
for a, b in [(chr(0x4E24), chr(0x5169)), (chr(0x4E2A), chr(0x500B))]:
    para = para.replace(a, b)
para = para.replace(u'NROW', u'{:,}'.format(NROW)).replace(u'SHA', SHA)
assert u'NROW' not in para and u'SHA' not in para

DJ = io.open(J, encoding=u'utf-8').read()
assert u'286・外路第十四報告' not in DJ
DJ2 = DJ.rstrip(u'\n') + u'\n\n' + para + u'\n'

sop_line = (u'- **印面**：**積輪 0**（286 重建：完整版影印與螢幕**各 261 頁**・大綱 146＝目錄印出 146・定位失敗 0；'
            u'冊 ' + u'{:,}'.format(NROW) + u' 行・sha256（LF 形）`' + SHA + u'`；五量全中：圍欄 75 段同頁 75・超閾 0、'
            u'最細 9.33pt・9pt 以下 0 段、目錄縮字警語仍無）。**終卷自 286 起隨冊印**：`build39.DROP_H1` 今為空，'
            u'故冊與目錄多其一條（大綱 143➔146）。奉令方重建：`python _print/build39.py full`（＋ `full screen`），'
            u'覆核 `_work/r273face.py 列印`。')
sop_bullet = (u'- **第 286 輪・印面與編輯痕跡之清創（產器四刀）**：① 表前標籤歸表為 `caption.tbl-lbl`'
              u'（鎖框一途於 Chromium 無效——框高一頁即不行 `break-inside: avoid`）；② 具名頁 `.fm` 之錨前移至卷首'
              u'之第一個 H2，卷前頁碼自此一律羅馬；③ `retune_tables` 短格之門 24➔30，出處欄不再一字一行；'
              u'④ 六十二行之流程圖於冊身折為兩段，圍欄超閾不鎖者自此為 0。**改產器之律：只以唯一錨點逐條替換、'
              u'不取區間，改畢即以 ast 與『相鄰諸函數俱在』自校；寫檔之換行只在一處換（內容或 newline 參數，'
              u'不可兩地俱動），寫訖即以二進位數 CR／CRLF／LF 自證。**')

DO = io.open(O, encoding=u'utf-8').read()
m = re.search(u'(?m)^- \\*\\*印面\\*\\*：.*$', DO)
assert m, u'SOP 印面條不可求'
DO2 = DO.replace(m.group(0), sop_line, 1)
DO3 = DO2.replace(u'\n- **第 285 輪・', u'\n' + sop_bullet + u'\n- **第 285 輪・', 1)
assert DO3 != DO2, u'SOP 新條未入'
para2 = para.replace(chr(0x7B2C) + u'一' + chr(0x4E2A), u'第一個')
print(u'冊 %s 行・sha %s・日誌 %d➔%d・SOP %d➔%d' % (
    u'{:,}'.format(NROW), SHA, len(DJ), len(DJ2), len(DO), len(DO3)))
if APPLY:
    io.open(J, 'w', encoding=u'utf-8', newline=u'\n').write(DJ2)
    io.open(O, 'w', encoding=u'utf-8', newline=u'\n').write(DO3)
    print(u'已寫入日誌與 SOP')
else:
    print(u'（試跑・未寫檔）')
