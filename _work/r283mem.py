# -*- coding: utf-8 -*-
"""283・帳（三）：把『多行隱式相連字串須加外括號』與『碼位補字必印原文行』補入 user 記憶。"""
import hashlib
import io
import os

P = os.path.join(u'C:', u'\\', u'Users', u'lionc', u'.qoder', u'memory',
                 u'feedback-tool-write-then-run-partial-file.md')
S = io.open(P, encoding=u'utf-8').read().rstrip(u'\n') + u'\n'
Q = u'\u3002'
ADD = (u'\n**變體（2026-10-25・戒律分析 283 輪）**：同一家族的另一型幽靈 IndentationError——不是寫入層壞檔，'
       u'而是我把多行隱式相連之字串直接賦值（`X = u\u2018…\u2019 換行 `u\u2018…\u2019`）而未加外層括號。'
       u'教：ast.parse 之復核能一眼分別『半檔』與『自寫錯』（前者錯在隨機行，後者錯在我新添那段），'
       u'故**必讀 e.msg 與 e.lineno 再決定改哪裡**，不可預設是工具故障。'
       u'又一行：以碼位補字時要替換成**字元本身**，不可替換成「U+53C8」之類**字面文字**——'
       u'落盤後須印**原文行**覆讀，不可只看命中數（本輪『三軌之外U+53c8一閘』即靠覆讀現形）' + Q)
S = S + ADD
io.open(P, 'w', encoding='utf-8').write(S)
back = io.open(P, encoding=u'utf-8-sig').read()
print(u'今 %d 行・sha %s・含變體：%s' % (len(back.split(u'\n')),
      hashlib.sha256(back.encode(u'utf-8')).hexdigest()[:12], u'變體（2026-10-25' in back))
