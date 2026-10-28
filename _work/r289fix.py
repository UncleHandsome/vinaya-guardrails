# -*- coding: utf-8 -*-
r"""289・帳之自清：補回被 shell 反引號吃掉之檔名，並記第三犯之戒。"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, u'_archive', u'編年工程日誌.md')
BN = u'r289clean.py'
raw = io.open(D, 'rb').read().decode('utf-8')

A = u'《菩薩地》諸檔（）——此報告之『無誤』宣稱屬實。'
Bk = u'《菩薩地》諸檔（量尺_' + BN + u'）——此報告之『無誤』宣稱屬實。'
assert raw.count(A) == 1, u'錨 A：%d' % raw.count(A)
raw = raw.replace(A, Bk.replace(u'量尺_', u'量器 '))

C = (u'**自犯一則**：錨點之分隔符又誤記其形')
Dd = (u'**自犯兩則**：① **反引號三犯**——入帳之句內含反引號包檔名，走 shell 時被當命令替換而吃空，'
      u'落盤成『（）』之空括號（此戒 271・283・今 289 三犯，**凡帶反引號之中文一律付腳本檔，不入 `bash -c`**）；'
      u'帳文已補回量器之名。② 錨內分隔符又誤記其形')
assert raw.count(C) == 1, u'錨 C：%d' % raw.count(C)
raw = raw.replace(C, Dd)

E = u'此為『分隔符兩形』之第二犯，下次一律以 `chr(0x00B7)`／`chr(0x30FB)` 構造，不再憑眼看。'
F = u'此為『分隔符兩形』之第二犯，下次一律以 chr(0x00B7)／chr(0x30FB) 構造，不再憑眼看。'
if raw.count(E) == 1:
    raw = raw.replace(E, F)

io.open(D, 'wb').write(raw.encode('utf-8'))
print(u'空括號餘 %d 處（舊帳之他處不動）' % raw.count(u'（）'))
i = raw.find(u'自犯兩則')
print(u'覆讀：%s' % raw[i:i + 90].replace('\r', '').replace('\n', ' '))
