# -*- coding: utf-8 -*-
r"""292・七大刀口之載體清冊（唯讀；先窮舉載體，後動刀）。"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TXT = io.open(os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md'),
              encoding='utf-8').read()
L = TXT.replace('\r\n', '\n').split('\n')

print(u'【甲・三鏡與三印之全部落點】')
for i, l in enumerate(L):
    if u'三鏡' in l or u'三印' in l:
        print(u'  L%-5d｜%s' % (i + 1, l.strip()[:150]))

print(u'\n【乙・八目（L49〜56）現文】')
for i in range(48, 56):
    print(u'  L%-5d｜%s' % (i + 1, L[i][:120]))

print(u'\n【丙・判準層級表之四奪列（第一章第六節）】')
i = [k for k, l in enumerate(L) if u'除偏鏡（不入判準層級）' in l][0]
for k in range(i - 5, i + 2):
    print(u'  L%-5d｜%s' % (k + 1, L[k][:170]))

print(u'\n【丁・J 案全部載體（14 見）】')
for i, l in enumerate(L):
    if re.search(u'J-\d', l):
        print(u'  L%-5d｜%s' % (i + 1, l.strip()[:126]))

print(u'\n【戊・次碼之形（前 12 枚樣本＋總數）】')
m = re.findall(u'〔案例[^〕]*?/[^〕]*?〕', TXT)
print(u'  總 %d 枚｜形之種類：%s' % (len(m), len(set(m))))
for x in m[:12]:
    print(u'   %s' % x)
print(u'  …凡例之說明句在 L260；第六章以外之次碼：%d 枚'
      % len([i + 1 for i, l in enumerate(L) if re.search(u'〔案例[^〕]*?/', l) and i < 4300]))

print(u'\n【己・附錄六之標題與導言（可正名之處）】')
for i, l in enumerate(L):
    if l.startswith(u'# 附錄六') or (l.startswith(u'### 〔調部深描') and i > 7860 and i < 7866) \
       or u'十五則深描' in l or u'15 則深描' in l:
        print(u'  L%-5d｜%s' % (i + 1, l.strip()[:120]))
print(u'  〔調部深描 NN〕H3：%d 條｜卷首目錄括註：%d' % (
    len([l for l in L if l.startswith(u'### 〔調部深描')]),
    len([l for l in L[:400] if u'深描' in l])))
