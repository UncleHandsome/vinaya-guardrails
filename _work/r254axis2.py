# -*- coding: utf-8 -*-
"""第 254 輪・刀十四b：八處『舊漏』補入心所病相軸與生活場域軸，再如實重計各群案數。

（此八案非本次迎回者，乃四軸向來未盡之漏：33・34・40・63 之於病相軸，8・9・40・53 之於場域軸。）
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
       and u'列印' not in q][0]
PATH = os.path.join(ROOT, SRC)
SHORT = {33: u'棄金銀羯磨', 34: u'功德衣五月日落', 40: u'羅睺羅廁夜救幼', 63: u'學家受食可呵',
         8: u'誘殺與嚴拒', 9: u'洗瘡雙判', 53: u'水中嬉戲'}
AX1 = {1: [33, 34, 63], 9: [40]}                       # 群號 → 案號
AX2 = {1: [53], 2: [8], 5: [40], 6: [9]}               # 領域序 → 案號


def nums(line):
    return [int(x) for x in re.findall(u'〔案例 ?(\\d{1,3})〕', line)]


def main():
    apply = u'apply' in sys.argv[1:]
    lines = io.open(PATH, encoding=u'utf-8').read().split(u'\n')
    i7 = next(i for i, l in enumerate(lines) if l.startswith(u'# 第七章'))
    s2 = next(i for i in range(i7, len(lines)) if lines[i].startswith(u'### 第二節'))
    s3 = next(i for i in range(s2 + 1, len(lines))
              if lines[i].startswith(u'### 第三節') or lines[i].startswith(u'# 第七章　'))
    seg = lines[s2:s3]
    # 一、病相軸：入該群之『迎回與新立之案』行（無則新建一行）
    n1 = 0
    heads = [(i, int(re.match(u'^##### (\\d+)\\.', seg[i]).group(1)))
             for i in range(len(seg)) if re.match(u'^##### \\d+\\.', seg[i])]
    for gi, g in sorted(heads, key=lambda x: -x[0]):
        if g not in AX1:
            continue
        end = next((i for i, _x in heads if i > gi), len(seg))
        row = next((i for i in range(gi + 1, end) if u'迎回與新立之案' in seg[i]), None)
        add = u'、'.join(u'〔案例%02d〕%s' % (n, SHORT[n]) for n in AX1[g])
        if row is None:
            seg[end:end] = [u'* **迎回與新立之案（重整後補入）**：  ', u'  ' + add + u'。', u'']
        else:
            tgt = row + 1
            seg[tgt] = re.sub(u'[；。]\\s*$', u'', seg[tgt].rstrip()) + u'、' + add + u'。'
        n1 += len(AX1[g])
    # 二、場域軸：入該領域行末
    n2 = 0
    dom = {u'一': 1, u'二': 2, u'三': 3, u'四': 4, u'五': 5, u'六': 6}
    for i, l in enumerate(seg):
        m = re.match(u'^\\* \\*\\*([一二三四五六])、', l)
        if not m or dom[m.group(1)] not in AX2:
            continue
        g = dom[m.group(1)]
        body = i + 1
        add = u'、'.join(u'〔案例%02d〕%s' % (n, SHORT.get(n, u'')) for n in AX2[g])
        seg[body] = re.sub(u'[；。]\\s*$', u'', seg[body].rstrip()) + u'；' + add + u'。'
        n2 += len(AX2[g])
    print(u'補入：病相軸 %d 案次｜場域軸 %d 案次' % (n1, n2))

    # 三、重計各群『共 N 案』/『（N 案）』
    heads2 = [i for i, l in enumerate(seg)
              if re.match(u'^##### \\d+\\.|^\\* \\*\\*[一二三四五六]、|^\\* \\*\\*第[一二三四五六]階', l)]
    n_cnt = 0
    for k, h in enumerate(heads2):
        end = heads2[k + 1] if k + 1 < len(heads2) else len(seg)
        got = set()
        for l in seg[h + 1:end]:
            got |= set(nums(l))
        l0 = seg[h]
        old = None
        new = None
        m = re.search(u'共 (\\d+) 案（實際）', l0) or re.search(u'共 (\\d+) 案', l0)
        if m:
            old = m.group(0)
            core = u'共 %d 案（實際）' % len(got)
            new = core
        else:
            m2 = re.search(u'（(\\d+) 案', l0)
            if m2:
                old = m2.group(0)
                new = u'（%d 案' % len(got)
        if old and old != new:
            seg[h] = l0.replace(old, new)
            n_cnt += 1
    print(u'重計各群案數：%d 處' % n_cnt)
    text = u'\n'.join(lines[:s2] + seg + lines[s3:])
    for nm, rng in [(u'一、心所病相軸', range(1, 103)), (u'二、生活場域軸', range(1, 103))]:
        pass
    j4 = next(i for i, l in enumerate(seg) if l.startswith('#### ') and u'四、' in l)
    for nm, lo, hi in [(u'一、心所病相軸', 0, next(i for i,l in enumerate(seg) if l.startswith(u'#### 二、'))),
                       (u'二、生活場域軸', next(i for i,l in enumerate(seg) if l.startswith(u'#### 二、')), next(i for i,l in enumerate(seg) if l.startswith(u'#### 三、'))),
                       (u'四、處分階梯軸', j4, len(seg))]:
        got = sorted(set().union(*[set(nums(l)) for l in seg[lo:hi]])) if hi > lo else []
        miss = sorted(set(range(1, 103)) - set(got))
        print(u'  %s：涵蓖 %d/102｜缺 %s' % (nm, len(got), miss or u'無'))
    print(u'行數 %d' % len(text.split(u'\n')))
    if apply:
        io.open(PATH, 'w', encoding=u'utf-8').write(text)
        print(u'已落檔')
    else:
        print(u'（dry-run）')


main()
