# -*- coding: utf-8 -*-
"""282・帳（補三）：記一則自犯（全域換字元又毀供狀一枚），並逐名列檔清本輪之暫存輸出。"""
import hashlib
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, u'_archive', u'編年工程日誌.md')
TXT = io.open(LOG, encoding=u'utf-8-sig').read()
ADD = u'''
**282 補二・自犯（同輪・記帳之時）**：為除一枚我新打的簡形『则』，我以**一字全域替**掃五份記憶檔（`则`➔`則`），遂把 `feedback-tool-param-unicode-escapes.md` 內**以錯字為供狀**的一句毀了——原文是『逮住自己新打的「经・当・处・书・则・该」六枚』，其『则』正是要留的簡形證據，被我改成『則』。幸即時以碼位復原（檔 sha 回到改前之 `601be1f5cc80`）。**此即 262 輪之舊課現形第二次**（見 [[feedback-no-global-char-fix-for-console-encoding]]・[[feedback-self-checkers-must-measure-reality]]）：**記憶檔裡凡引『錯字本身』為證之句，皆須以上下文為錨逐枚處理，不可按字全域替**；掃簡形之器（`_work/r282sweep.py`）只宜**報**而不宜**改**，改必帶錨且先印命中處。定入後工序：**凡改記憶檔之字，先只印上下文，人工分『供狀』與『敘事』兩途，再逐枚改。**
'''
assert u'282 補二・' not in TXT, u'已記過'
io.open(LOG, 'a', encoding=u'utf-8').write(ADD)
back = io.open(LOG, encoding=u'utf-8-sig').read()
print(u'日誌今 %d 行・sha %s' % (len(back.split(u'\n')),
      hashlib.sha256(back.encode(u'utf-8')).hexdigest()[:12]))

CLEAN = [u'r282dump.txt', u'r282rows.txt', u'r282p2.txt', u'r282p3.txt',
         u'r282p4.txt', u'r282p5.txt', u'r282p6.txt', u'r282glyph2.py']
W = os.path.join(ROOT, u'_work')
print(u'── 清場（逐名列檔・先試跑印名）')
for f in CLEAN:
    p = os.path.join(W, f)
    print(u'  %s｜存在=%s・%s B' % (f, os.path.exists(p),
                                   os.path.getsize(p) if os.path.exists(p) else 0))
