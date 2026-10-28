# -*- coding: utf-8 -*-
"""292・刀後目視：本輪七刀之落點逐段覆讀（構字須向冊內取形，此器只印不寫）。"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
L = io.open(SRC, 'rb').read().decode('utf-8').replace(u'\r\n', u'\n').split(u'\n')
print(u'冊：%d 行｜%d B' % (len(L), len(u'\n'.join(L).encode('utf-8'))))

SEGS = [(u'卷首・鏡尺分軌與八目界說', u'這三十二字是行者', 14),
        (u'卷首・定錨口訣', u'〔定錨口訣〕', 3),
        (u'第一章・去同一性', u'體上之每一句', 3),
        (u'第一章・判準表與明橋', u'| **實體層**', 10),
        (u'第一章・全景表欄名', u'#### 四、八大正理體用源流', 6),
        (u'第三章・腳下三問', u'#### 三、腳下三問', 8),
        (u'第八章・四境之義', u'> **【現代四境演繹判例之義】**', 3),
        (u'第八章・四案之題', u'#### 四、反靈性煤氣燈操縱防護禁約（四境', 3),
        (u'第四章・程序終結', u'#### 二、程序終結之法定宣告', 8),
        (u'附錄六・標題與導言', u'# 附錄六　調部疑難判例法理專題十五則（上篇）', 8),
        (u'附錄四・新舊次碼對照', u'### 〔新舊次碼對照〕', 9),
        (u'附錄六・篇末', u'### 【附錄六全篇大圓滿結語】', 9)]
for title, anchor, n in SEGS:
    hits = [i for i, x in enumerate(L) if x.startswith(anchor)]
    print(u'\n══ %s（錨 %d 處）══' % (title, len(hits)))
    if not hits:
        print(u'  ⚠ 錨不見：%s' % anchor[:28])
        continue
    for q in range(hits[0], min(hits[0] + n, len(L))):
        print(u'  L%-5d｜%s' % (q + 1, L[q][:210]))

print(u'\n══ 名制之殘跡覆量 ══')
T = u'\n'.join(L)
for p in [u'憲' + chr(0x7DB1), u'三鏡', u'J-', u'現-', u'調部' + chr(0x6DF1) + chr(0x63CF),
          u'八重', u'现代', u'专题', u'宪法', u'对应', u'一一']:
    print(u'  %-10s %d' % (p, T.count(p)))
print(u'  現碼：%s' % sorted(set(re.findall(u'現[0-9]{1,2}', T))))
print(u'  四境演繹判例：%d 見｜現代四境演繹判例：%d 見｜腳下三問：%d 見｜夜半四照：%d 見' % (
    T.count(u'四境演繹判例'), T.count(u'現代四境演繹判例'),
    T.count(u'腳下三問'), T.count(u'夜半四照')))
print(u'  次碼形（反引號圖例除外）：%d' % len(re.findall(
    u'〔案例 \\d+ ?/ ?(?:遮|僧|開)', re.sub(u'`[^`]*`', u'', T))))
