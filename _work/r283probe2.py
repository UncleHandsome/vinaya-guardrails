# -*- coding: utf-8 -*-
"""283・量（二）：重複段之字數與明橋・第四章之『第八章』自註・四法緣僧・舊本之 J・語料之有根無根。"""
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
T = u'\n'.join(LINES)


def block(start_marker, stop=re.compile(u'^#{1,5} ')):
    i = next(k for k, l in enumerate(LINES) if start_marker in l)
    j = i + 1
    while j < len(LINES) and not LINES[j].startswith(u'#'):
        j += 1
    return i, j, u'\n'.join(LINES[i:j])


a1, e1, B1 = block(u'#### 二、程序終結之消磁宣告（出堂洗心三事）')
a2, e2, B2 = block(u'#### 一、出堂洗心三事（結案當日強制消磁儀軌')
print(u'【丁】第四章 L%d..%d（%d 字）｜第七章 L%d..%d（%d 字）' % (
    a1 + 1, e1, len(B1), a2 + 1, e2, len(B2)))


def common_runs(s1, s2, n=40):
    out, i = [], 0
    while True:
        j = i
        best = 0
        while j < len(s1):
            k = s2.find(s1[i:j + 1])
            if k < 0:
                break
            best = j - i + 1
            j += 1
        if best >= n:
            out.append((i, best, s1[i:i + best]))
            i += best
        else:
            i += 1
        if i >= len(s1):
            break
    return out


runs = common_runs(B1, B2, 25)
print(u'  兩段之公共長串（≥25 字）：%d 條・共 %d 字' % (len(runs), sum(r[1] for r in runs)))
for r in runs[:6]:
    print(u'   %d 字｜%s…' % (r[1], r[2][:60]))
print(u'  明橋之搜：『同一制』%d・『橋』於兩段附近：%s' % (
    T.count(u'同一制'), [i + 1 for i, l in enumerate(LINES) if u'明橋' in l][:6]))
for i in range(a1, min(a1 + 6, e1)):
    print(u'   四章 L%d| %s' % (i + 1, LINES[i][:130]))
for i in range(a2, min(a2 + 6, e2)):
    print(u'   七章 L%d| %s' % (i + 1, LINES[i][:130]))

print(u'【辛】第四章之『第八章』指稱：%s' % [i + 1 for i, l in enumerate(LINES) if u'第八章' in l][:20])
i4 = next(i for i, l in enumerate(LINES) if l.startswith(u'# 第四章'))
i5 = next(i for i, l in enumerate(LINES) if l.startswith(u'# 第五章'))
for i in range(i4, i5):
    if u'第八章' in LINES[i]:
        print(u'   L%d| %s' % (i + 1, LINES[i][:150]))
print(u'  第四章第三節之節末（『### 第三節』起之最後六個非空行）：')
s3 = next(i for i in range(i4, i5) if LINES[i].startswith(u'### 第三節'))
n3 = next(i for i in range(s3 + 1, i5) if LINES[i].startswith(u'### '))
tails = [i for i in range(s3, n3) if LINES[i].strip()]
for i in tails[-6:]:
    print(u'   L%d| %s' % (i + 1, LINES[i][:190]))

print(u'【丙附】四法緣僧之上下文：')
for i, l in enumerate(LINES):
    if u'四法緣僧' in l or u'四法僧' in l:
        print(u'   L%d| %s' % (i + 1, l[:200]))

print(u'【戊】舊本之 J：')
for rel in (u'_archive/舊本', u'_archive'):
    d = os.path.join(ROOT, rel)
    if os.path.isdir(d):
        for f in sorted(os.listdir(d))[:24]:
            print(u'   %s/%s' % (rel, f))
V38 = None
for cand in (u'ver38四分律_起心動念心智分析框架.md',):
    for root_, _, fs in os.walk(ROOT):
        if cand in fs:
            V38 = os.path.join(root_, cand)
print(u'  ver38 之徑：%s' % V38)
if V38:
    S38 = io.open(V38, encoding=u'utf-8-sig').read()
    print(u'  ver38『J-1』：%d・『附錄J』：%d・『附錄 J』：%d・『現代深水』：%d' % (
        S38.count(u'J-1'), S38.count(u'附錄J'), S38.count(u'附錄 J'), S38.count(u'現代深水')))
    for m in re.finditer(u'.{0,60}附錄 ?J.{0,80}', S38):
        print(u'     %s' % m.group(0).replace(u'\n', u'\\n')[:150])

print(u'【癸】語料之有根／無根不犯句：')
V = _tk.VINAYA
for m in re.finditer(u'[^。]{0,50}(?:有根|無根)[^。]{0,80}', V):
    s = m.group(0)
    if u'不犯' in s or u'聽' in s:
        print(u'   %s' % s[:150])
