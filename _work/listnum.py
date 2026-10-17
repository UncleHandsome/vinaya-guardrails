# -*- coding: utf-8 -*-
"""第 132 輪軸：行首「(N)」之逃逸——pandoc 會把它讀成有序清單標記而改印成「1.」

病（印面實測）：第五章『非法足數十五類』正文原一律作 (1)…(15)，印出來 A 組三項卻成
    「1. 2. 3.」，與 B／C 組之 (4)…(15) 參差——md 層看不出，須以本軸守『未逃逸之行首 (N)』。
"""
import io, re, sys
MD = sys.argv[1] if len(sys.argv) > 1 else u'ver38四分律_起心動念心智分析框架_修正版.md'
L = io.open(MD, encoding='utf-8').read().split('\n')
incode = False
bad = []
for i, l in enumerate(L):
    if l.startswith('```'):
        incode = not incode
        continue
    if incode:
        continue
    if re.match(r'^\s*\(\d{1,2}\)\s', l):
        bad.append(i + 1)
print(u'==== 行首 (N) 未逃逸 %d 行%s ====' % (len(bad), (u'｜' + str(bad[:8])) if bad else u''))
sys.exit(1 if bad else 0)
