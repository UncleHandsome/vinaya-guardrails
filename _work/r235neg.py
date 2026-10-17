# -*- coding: utf-8 -*-
"""第 235 輪負測：丙桶擭緊之後，真候選仍須抓得到（陽性一枚），兩枚陰性不得復報。
   陽性·行內自陳未收而有八字以上「」逐字形貌｜陰性一·引的是篇目職分｜陰性二·已以〔案〕就地標界。"""
import io
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER = os.path.join(ROOT, u'ver38四分律_起心動念心智分析框架_修正版.md')
COP = os.path.join(ROOT, u'_work', u'_r235neg.md')

POS = u'問：本地未收之典所載如「一切眾生皆為宿世本師故今為之故不惜身命」者，讀者宜逕查原書。'
NEG1 = u'又例：第三節「查無對應清單」與「F-3 無從覆核之典籍與版本」兩節分職，本地未收者彙列於後。'
NEG2 = u'又例：『此事出禪宗語錄』之說，其長句「五百世中墮野狐身未曾解脫」〔案：該典未入本書比對用語料，逐字無從覆核。〕'

src = io.open(MASTER, encoding='utf-8').read().split(u'\n')
s3, e3 = None, None
for i, l in enumerate(src):
    if l.startswith(u'# ') and u'第三章' in l:
        s3 = i
    elif s3 is not None and l.startswith(u'# '):
        e3 = i
        break
assert s3 is not None and e3 is not None
# 取章內第一枚散文行之後插入三例
k = next(i for i in range(s3, e3) if src[i].strip() and not src[i].startswith((u'#', u'|', u'>')))
cut = src[:k + 1] + [u''] + [POS, NEG1, NEG2] + src[k + 1:]
io.open(COP, 'w', encoding='utf-8', newline=u'\n').write(u'\n'.join(cut))

env = dict(os.environ, PYTHONPATH=ROOT, PYTHONIOENCODING='utf-8')
r = subprocess.run([sys.executable, u'-X', u'utf8', os.path.join(u'_work', u'r190f3.py'),
                    os.path.join(u'_work', u'_r235neg.md')],
                   cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf-8')
head = u''
for line in (r.stdout or u'').split(u'\n'):
    if line.startswith(u'F-3 兩向'):
        head = line
        break
print(head)
n = int(head.split(u'丙·宣稱而配對無書名 ')[1].split(u' 筆')[0]) if head else -1
print(u'陽性被抓？%s（丙=%d，須恰 1）' % (u'✓' if n == 1 else u'✗', n))
os.remove(COP)
sys.exit(0 if n == 1 else 1)
