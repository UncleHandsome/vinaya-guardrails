# -*- coding: utf-8 -*-
"""273 輪・器病之刀：`build39.build_outline` 去重改鑰之後，呼出口須接三值並**把帳印出**。

只用 ASCII 錨定行（本檔之 CJK 作錨三度不中，故一律以 ASCII 片段求行、新句直打漢字，打完以 ast 覆核）。
"""
import ast
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, '_print', 'build39.py')
L = io.open(P, encoding=u'utf-8').read().split(u'\n')

# ① 呼出口：三值
i = next(k for k, l in enumerate(L) if 'outline, miss = build_outline' in l)
L[i] = '    outline, miss, dup = build_outline(_d, entries, pages)'
# ② ntoc 之算（緊接呼出口之後）
j = next(k for k, l in enumerate(L) if 'miss[:6]' in l)          # 『未入大綱』之印行
# ③ 印帳兩行：加在 miss 印行之後；帳不平另報
block = [u'        print(u"    帳：目錄印出 %d 條・大綱入 %d 條・定位失敗 %d・同級重出跳過 %d（前兩數須齊）"',
         u'              % (ntoc, len(outline), len(miss), len(dup)))',
         u'        if dup:',
         u'            print(u"    跳過之名：%s" % u\'、\'.join(dup[:8]))',
         u'        if ntoc - len(outline) != len(miss) + len(dup):',
         u'            print(u"    ⚠ 大綱之帳不平：印出－入＝%d 而 miss＋dup＝%d（有條目無故而擲）"',
         u'                  % (ntoc - len(outline), len(miss) + len(dup)))']
L[j + 1:j + 1] = block
# ④ ntoc 之定義：放在 `if outline:` 之前
h = next(k for k, l in enumerate(L) if l.strip() == 'if outline:' and 'stamp_pdf' in L[k + 1])
L[h:h] = [u'    ntoc = sum(1 for lv, dp, _ in entries if dp != u"\\u76ee\\u9304" and not skip_in_toc(lv, dp))']
T = u'\n'.join(L)
ast.parse(T)
io.open(P, 'w', encoding=u'utf-8').write(T)
print(u'刀落：%d 行插入・呼出口改三值・ntoc 定義 %d 行' % (len(block), 1))
print(u'驗：ast OK｜三值呼出 %d・ntoc %d・帳印 %d' % (
    T.count('outline, miss, dup = build_outline'), T.count('ntoc = sum('), T.count(u'帳：目錄印出')))
