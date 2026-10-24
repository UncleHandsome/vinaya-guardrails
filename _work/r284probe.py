# -*- coding: utf-8 -*-
"""284・量：第六章報告十六案之今檔現況（只讀不改）。"""
import io
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, u'_work'))
import _tk  # noqa: E402
import _casedef as CD  # noqa: E402

BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
LINES = io.open(BOOK, encoding=u'utf-8-sig').read().split(u'\n')
T = u'\n'.join(LINES)
i6 = next(i for i, l in enumerate(LINES) if l.startswith(u'# 第六章'))
i7 = next(i for i, l in enumerate(LINES) if l.startswith(u'# 第七章'))

print(u'【A・地標大案之段序連貫】')
for i in range(i6, i7):
    if LINES[i].startswith(u'### 【經典地標深描'):
        j = i + 1
        nums = []
        while j < i7 and not LINES[j].startswith(u'### '):
            m = re.match(u'^#### ([一二三四五六七八九十])、(.{0,18})', LINES[j])
            if m:
                nums.append(m.group(1))
            j += 1
        want = u'一二三四五六'
        seq = u''.join(nums)
        flag = u'' if seq == want[:len(seq)] else u'  ⚠不連'
        print(u'  L%d| %s ➔ %s%s' % (i + 1, LINES[i][:34], seq, flag))

print(u'【B・地標 07 卷四與全書『三十捨墮』之卷引】')
for i, l in enumerate(LINES):
    if u'三十捨墮法之一·長衣' in l or (u'卷四（初分·三十捨墮' in l):
        print(u'  L%d| %s' % (i + 1, l[:220]))
for i, l in enumerate(LINES):
    if u'三十捨墮' in l:
        v = re.findall(u'卷([一二三四五六七八九十]+)', l)
        if v:
            print(u'  [舍墮卷引] L%d %s｜%s' % (i + 1, v, l[:90]))

print(u'【C・無句讀之長串（「」內）今量】')
PU = u'，。；：、？！「」‘’（）《》【】…—·　'


def run(s):
    best = cur = 0
    for ch in s:
        if ch in PU or ch.isspace():
            cur = 0
        else:
            cur += 1
            best = max(best, cur)
    return best


hist = Counter()
worst = []
for i, l in enumerate(LINES):
    for m in re.finditer(u'「([^「」]{12,})」', l):
        r = run(m.group(1))
        if r >= 20:
            hist[r // 5 * 5] += 1
            worst.append((r, i + 1, m.group(1)[:70]))
worst.sort(reverse=True)
print(u'  無句讀長串（≥20 字）：%d 段・分佈 %s' % (len(worst), sorted(hist.items())))
for r, ln, s in worst[:10]:
    print(u'   %d 字 L%d| %s' % (r, ln, s))

print(u'【D・同級嵌套『…『…』』】')
nest = [(i + 1, m.group(0)[:80]) for i, l in enumerate(LINES) for m in re.finditer(u'『[^』]{6,}『', l)]
print(u'  命中 %d 處' % len(nest))
for x in nest[:8]:
    print(u'   L%d| %s' % x)

print(u'【E・斜線台帳代號與『原編』】')
sl = [l for l in LINES if re.search(u'〔案例 ?\\d+ ?/ [^〕]+〕', l)]
print(u'  帶斜線之案號標：%d 行' % len(sl))
pat = Counter()
for l in sl:
    for m in re.finditer(u'〔案例 ?\\d+ ?/ ([^〕]+)〕', l):
        pat[m.group(1)] += 1
print(u'  代號族：%s' % u'・'.join(u'%s%d' % (k[0], v) for k, v in sorted(Counter(k[0] for k in pat).items())))
for k in (u'原編', u'異分支', u'安居段', u'未遂支', u'方便支'):
    print(u'  『%s』全書：%d・第六章：%d' % (k, T.count(k), sum(l.count(k) for l in LINES[i6:i7])))
for i, l in enumerate(LINES):
    if u'台帳' in l and (u'遮' in l or u'僧' in l) or u'舊錄' in l and u'次' in l:
        print(u'  解釋行候選 L%d| %s' % (i + 1, l[:170]))

print(u'【F・同案多名（定義載體間）】')
d = {}
for i in range(i6, len(LINES)):
    for m in re.finditer(u'〔案例 ?0*(\\d+)([^〕0-9][^〕]*)?〕', LINES[i]):
        pass
names = {}
for i in range(i6, len(LINES)):
    l = LINES[i]
    for m in re.finditer(u'〔案例 ?0*(\\d+)〕(?:\\*\\*)?(?:<br>\\*\\*)?([^｜|〕<\\n]{0,40})', l):
        n = int(m.group(1))
        nm = m.group(2).strip(u'*・，，（） ')
        if nm:
            names.setdefault(n, set()).add(nm[:16])
multi = {n: v for n, v in names.items() if len(v) > 1}
print(u'  名異之案：%d 個' % len(multi))
for n in sorted(multi)[:14]:
    print(u'   案%-3d %s' % (n, u'｜'.join(sorted(multi[n]))))

print(u'【G・出佛身血之『第二罪』】')
for i, l in enumerate(LINES):
    if u'出佛身血' in l and (u'逆' in l or u'第二' in l):
        print(u'  L%d| %s' % (i + 1, l[:200]))

print(u'【H・地標 03 案號列・案17・案100・雙螺旋原典欄】')
for i, l in enumerate(LINES):
    if l.startswith(u'* **案號**') and (u'案例 16' in l or u'案例 30' in l or u'案例 37' in l or u'案例 77' in l):
        print(u'  L%d| %s' % (i + 1, l[:220]))
print(u'  『律典原典逐字回查』：全書 %d 見・第六章 %d 見' % (
    T.count(u'律典原典逐字回查'), sum(l.count(u'律典原典逐字回查') for l in LINES[i6:i7])))
for i in range(i6, i7):
    if LINES[i].startswith(u'## ') or LINES[i].startswith(u'### 【雙螺旋') or LINES[i].startswith(u'#### 律典原典'):
        print(u'   L%d| %s' % (i + 1, LINES[i][:56]))
