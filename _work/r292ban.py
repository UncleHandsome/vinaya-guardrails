# -*- coding: utf-8 -*-
"""292・禁形之量：新目前先驗『退位之名』今在印面殘幾枚（須俱零，除反引號之圖例）。"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
T = io.open(SRC, 'rb').read().decode('utf-8').replace(u'\r\n', u'\n')
NOB = re.sub(u'`[^`]*`', u'', T)                       # 去反引號之圖例
PATS = [u'憲' + chr(0x7DB1), u'三鏡', u'一鏡', u'二鏡', u'J-', u'現-',
        u'調部' + chr(0x6DF1) + chr(0x63CF),
        u'〔案例 05 / 遮44〕']
for p in PATS:
    print(u'%-14s 全文 %2d｜去圖例 %2d' % (p, T.count(p), NOB.count(p)))
print(u'次碼形 regex：全文 %d｜去圖例 %d' % (
    len(re.findall(u'〔案例 \\d+ ?/ ?(?:遮|僧|開)', T)),
    len(re.findall(u'〔案例 \\d+ ?/ ?(?:遮|僧|開)', NOB))))
print(u'反引號段：%d' % len(re.findall(u'`[^`]+`', T)))
for i, x in enumerate(T.split(u'\n')):
    if re.search(u'憲' + chr(0x7DB1) + u'|三鏡|一鏡|二鏡|J-|現-', x):
        print(u'  L%d｜%s' % (i + 1, x[:120]))
