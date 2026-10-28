# -*- coding: utf-8 -*-
r"""292・補量：三鏡之第三章與結語卡、附錄六導言、凡例 L260 之 J 段與次碼段、_casedef 之形。"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = io.open(os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md'),
            encoding='utf-8').read().split('\n')
for a, b in [(1576, 1584), (7299, 7312), (7856, 7860)]:
    print(u'===== L%d〜%d =====' % (a, b))
    for i in range(a - 1, b):
        print(u'L%-5d %s' % (i + 1, L[i][:170]))

s = L[259]
i = s.find(u'〔案例 J-1〕')
j = s.find(u'斜線次碼')
print(u'\n--- 凡例 L260・J 段 ---\n%s' % s[max(0, i - 8):i + 300])
print(u'\n--- 凡例 L260・次碼段 ---\n%s' % s[j - 12:j + 320])

print(u'\n===== _casedef.py 之形 =====')
S = io.open(os.path.join(ROOT, u'_work', u'_casedef.py'), encoding='utf-8').read()
for k, l in enumerate(S.split('\n')):
    if 'compile' in l or 'ROW' in l or 'H2' in l:
        print(u'L%-4d %s' % (k + 1, l.strip()[:160]))
