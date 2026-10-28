# -*- coding: utf-8 -*-
r"""287 候裁清單・印面之量（唯讀）：半空頁之今席、名詞之兩冊對照。"""
import io
import os
import re

import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(ROOT, u'_print',
                   u'ver39四分律_起心動念心智分析框架_第三十九版_列印版.pdf')

T39 = io.open(os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md'),
              encoding='utf-8').read()
T38 = io.open(os.path.join(ROOT, u'ver38四分律_起心動念心智分析框架_修正版.md'),
              encoding='utf-8').read()

print(u'【甲・兩冊名詞對照】')
TERMS = [u'台帳', u'綁定', u'稱重', u'壓力測試', u'勞動契約', u'防爆', u'穿透審計', u'行治證明牒',
         u'安全封存', u'假處分', u'提存', u'結界隔離', u'查無對應', u'附錄B', u'附錄F', u'附錄五',
         u'定位行', u'正理欄']
for t in TERMS:
    print(u'  %-8s ver38 %3d｜ver39 %3d' % (t, T38.count(t), T39.count(t)))

print(u'\n【乙・印面之半空頁（内容底緣距版心下界者）】')
doc = pymupdf.open(PDF)
H = doc[10].rect.height
W = doc[10].rect.width
print(u'  頁數 %d｜版心高 %.1fpt・寬 %.1fpt' % (doc.page_count, H, W))
recs = []
for i in range(6, doc.page_count):          # 卷首之後起算
    p = doc[i]
    bl = [b for b in p.get_text('blocks') if b[4].strip()]
    if not bl:
        continue
    bottom = max(b[3] for b in bl if b[3] < H - 30)     # 排頁腳
    fill = (bottom - min(b[1] for b in bl)) / (H - 120)
    recs.append((i + 1, bottom, fill))
sparse = sorted([r for r in recs if r[1] < H - 250], key=lambda r: r[1])
print(u'  全文平均底緣 %.1fpt｜版心下界 %.1fpt' % (sum(r[1] for r in recs) / len(recs), H))
print(u'  底緣距下界 >250pt 之頁（近半空）：%d 頁' % len(sparse))
for pg, bt, fl in sparse[:14]:
    txt = u''.join(b[4] for b in doc[pg - 1].get_text('blocks') if b[4].strip())[:34].replace(u'\n', u' ')
    print(u'    p%-4d 底緣 %6.1fpt｜內容佔 %.0f%%｜%s' % (pg, bt, fl * 100, txt))
doc.close()
