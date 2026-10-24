# -*- coding: utf-8 -*-
"""279・量之二：印出第七報告諸案之『今檔本文』（供逐條定性与落刀，不改檔）。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r279read.py <案碼>（A1 A2 B C D E F G1 G2 G3 G4 G5 H I J K）
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
LINES = io.open(BOOK, encoding=u'utf-8-sig').read().split(u'\n')

SPOT = {
    u'A1': [(u'暫取想', 3)],
    u'A2': [(u'止犯不坐別住', 2), (u'不作為', 2), (u'見死不救', 2)],
    u'B': [(u'俱時', 4)],
    u'C': [(u'年未滿二十', 2), (u'信賴保護', 2), (u'重新如法', 2)],
    u'D': [(u'心淨則開', 4)],
    u'E': [(u'出時', 2), (u'他心智', 2), (u'嚴禁當庭盤詰', 1)],
    u'F': [(u'判準層級', 3), (u'除偏鏡', 3)],
    u'G1': [(u'罪疑唯輕', 2), (u'疑罪唯輕', 1)],
    u'G2': [(u'越濟人', 2), (u'捨戒', 3)],
    u'G3': [(u'第六十九', 2), (u'四瑕疵', 2), (u'五如法', 2)],
    u'G4': [(u'大悲自誓', 3), (u'違心自誣', 2)],
    u'G5': [(u'破法輪僧', 4), (u'賊住', 2)],
    u'H': [(u'法理特權', 2), (u'染污惡作', 3)],
    u'I': [(u'斷彼心', 2), (u'言聲', 3)],
    u'J': [(u'三禁', 3)],
    u'K': [(u'遙舉', 2), (u'跨界聯合', 2), (u'法域', 2)],
}

which = sys.argv[1:] or sorted(SPOT)
for w in which:
    print(u'\n═══════ 案 %s ═══════' % w)
    for key, cap in SPOT[w]:
        hits = [i for i, l in enumerate(LINES) if key in l]
        print(u'── 鍵『%s』%d 見' % (key, len(hits)))
        for i in hits[:cap]:
            seg = LINES[i]
            if len(seg) > 620:
                j = seg.find(key)
                seg = seg[max(0, j - 220):j + 380]
            print(u'  L%-5d %s' % (i + 1, seg.strip()[:600]))
            if i + 1 < len(LINES) and LINES[i + 1].strip() and not LINES[i + 1].startswith(u'#'):
                print(u'        ↳ %s' % LINES[i + 1].strip()[:300])
