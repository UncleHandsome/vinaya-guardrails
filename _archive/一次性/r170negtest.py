# -*- coding: utf-8 -*-
"""第 170 輪負測（改以『文』為鑰）：於副本回植三類病各一，驗 `r170flow.py` 逐目報出。"""
import io
import os
import re
import subprocess

src = 'ver38四分律_起心動念心智分析框架_修正版.md'
lines = io.open(src, encoding='utf-8').read().split('\n')

A_TXT = u'此三則乃治理通則（各附其本有之律據案例，不別立案號、不占百則之數、不充空白格）：'
B_TXT = u'此為「設一長語以測引文淹句之目其字數須逾十四而主幹只留四字」。'
C_TXT = u'如此設問而竟無答，讀者懸於半空，是否亦成疑？'

i = next(k for k, l in enumerate(lines) if u'此三則乃治理通則，各附其本有' in l)
lines[i] = A_TXT                                        # 甲：改回括注淹主幹
j = next(k for k, l in enumerate(lines) if l.startswith(u'##### '))
lines[j:j] = [B_TXT, u'']                               # 乙：引文淹句
# 丙目已撤（『作答之形』無自動之解），故此測唯驗甲乙兩目
io.open('_work/r170neg.md', 'w', encoding='utf-8').write('\n'.join(lines))
r = subprocess.run(['python', '-X', 'utf8', '_work/r170flow.py', '_work/r170neg.md'],
                   capture_output=True, text=True, encoding='utf-8',
                   env=dict(os.environ, PYTHONPATH='.', PYTHONIOENCODING='utf-8'))
out = r.stdout
res = dict(re.findall(r'── ([甲乙丙])[^：]*：(\d+) 處', out))
print('基準（主檔）：甲 0、乙 0')
print('副本回植後：甲 %s、乙 %s' % (res.get(u'甲'), res.get(u'乙')))
for tag, key in ((u'甲', u'此三則乃治理通則'), (u'乙', u'設一長語以測引文')):
    print('  %s 植病「%s…」→ 報出：%s' % (tag, key[:10], u'是' if key in out else u'否'))
