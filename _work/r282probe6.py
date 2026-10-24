# -*- coding: utf-8 -*-
"""282・量（六）：語料篇名標記・附錄四導言全文・雙空行之多寡・第八章搜查插入點。"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, u'_work'))
import _tk  # noqa: E402

BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
LINES = io.open(BOOK, encoding=u'utf-8-sig').read().split(u'\n')
V = _tk.VINAYA

POS = {u'案25': V.find(u'今從僧乞六夜摩那埵'), u'案69': V.find(u'不看門相便入')}
print(u'語料定位：%s' % POS)
ks = [(m.start(), m.group(0)) for m in re.finditer(u'[\\u4e00-\\u9fff]{0,4}犍度[第\\u4e00-\\u9fff]{0,6}', V)]
print(u'語料內『犍度』標記：%d 枚' % len(ks))
for lab, p in POS.items():
    prev = [x for x in ks if x[0] < p]
    nxt = [x for x in ks if x[0] > p]
    print(u'  %s：前 nearest %s｜後 nearest %s' % (lab, prev[-3:], nxt[:2]))
print(u'  滅諍犍度 出現：%s' % [i for i, s in ks if u'滅諍' in s][:12])
print(u'  房舍犍度 出現：%s' % [i for i, s in ks if u'房舍' in s][:6])
print(u'  衣犍度 出現：%s' % [i for i, s in ks if u'衣犍度' in s][:6])
print(u'語料內『卷第』：%s' % [(m.start(), V[m.start():m.start() + 14]) for m in re.finditer(u'卷第', V)])

# 六檔之分界（以檔頭為準）
for name in sorted(x for x in dir(_tk) if x.endswith('SRC') or x.startswith('B')):
    pass
print(u'_tk 之檔路徑：%s' % getattr(_tk, 'BSRC', None))

print(u'\n== 附錄四導言 L7529..7536')
for i in range(7528, 7536):
    print(u'L%d| %s' % (i + 1, LINES[i][:400]))

dbl = [i + 1 for i in range(len(LINES) - 1) if LINES[i].strip() == u'' and LINES[i + 1].strip() == u'']
print(u'\n== 連二空行：%d 處 %s' % (len(dbl), dbl[:30]))

print(u'\n== 第八章第二節 L6721..6770（搜查插入點之前後）')
for i in range(6720, 6770):
    if LINES[i].strip():
        print(u'L%d| %s' % (i + 1, LINES[i][:150]))
