# -*- coding: utf-8 -*-
"""第 127 輪探針：跨行配對之孤立星號（markdown 段內兩枚單星會悄悄變成斜體而吃掉字面星號）

病緣（實測）：第三章境想表下註解四行「⁽*²⁾…⁽*⁵⁾」，md 層星號俱在，印面卻作「⁽²⁾…」——
    四行同屬一個 blockquote 段落，第一、二枚單星結為斜體對，第三、四枚亦然，
    於是字面星號盡消。故本軸以**段**為單位數單星，凡配對之兩枚分屬不同行者報病。
"""
import io
import re
import sys

BS = chr(0x5C)
md = sys.argv[1] if len(sys.argv) > 1 else u'ver38四分律_起心動念心智分析框架_修正版.md'
L = io.open(md, encoding='utf-8').read().split('\n')
TSTART = next((i for i, l in enumerate(L) if l.startswith(u'# 終卷')), len(L))

blocks, cur = [], []
incode = False
for i, l in enumerate(L):
    if l.startswith('```'):
        incode = not incode
        if cur:
            blocks.append(cur)
            cur = []
        continue
    if incode:
        continue
    if l.strip() == u'':
        if cur:
            blocks.append(cur)
            cur = []
        continue
    if l.startswith('#'):
        if cur:
            blocks.append(cur)
            cur = []
        continue
    if l.lstrip().startswith('|'):      # 表列各自成段（pandoc 逐格解析，不跨列配對）
        if cur:
            blocks.append(cur)
            cur = []
        blocks.append([(i, l)])
        continue
    cur.append((i, l))
if cur:
    blocks.append(cur)

bad = 0
odd = 0
FOOT = re.compile(u'⁽\\\\?\\*[^⁾]*⁾')      # 腳注標記 ⁽*¹⁾／⁽\*²⁾——字面星號，不入斜體之計
BRK = re.compile(u'\\[[^\\]\\n]{0,8}\\*[^\\]\\n]{0,8}\\]')   # [月*冓] 之類拆字形， likewise 字面
OPENER = re.compile(u'^\\s*(?:>\\s*)*\\*[^*\\s]')        # 行首單星緊接字＝斜體起符（『* 』乃列表標記）
for b in blocks:
    if b[0][0] >= TSTART:            # 終卷不印，不入本軸（底冊四篇已另檔，第 250 輪）
        continue
    stars = []                     # (行 index, 欄位)
    for i, l in b:
        t = re.sub(r'^\s*(?:>\s*)+', '', l)     # 引標先削，否則「> * 條列」之星號乃列表標記
        t = re.sub(r'`[^`]*`', ' ' * 8, t)
        t = re.sub(r'^\s*[*+-]\s', '  ', t, count=1)
        t = t.replace(u'**', '  ')
        for j, ch in enumerate(t):
            if ch == u'*' and (j == 0 or t[j - 1] != BS):
                stars.append((i, j))
    if len(stars) >= 2:
        cross = [(stars[k], stars[k + 1]) for k in range(0, len(stars) - 1, 2)]
        acc = [(p, q) for p, q in cross if p[0] != q[0]]
        if acc:
            bad += 1
            i0 = acc[0][0][0]
            print(u'  病 @行%s 單星 %d 枚、跨行配對 %d 組｜%s' % (
                i0 + 1, len(stars), len(acc), L[i0][:56]))
    # ── 軸二（第 158 輪立）：行首斜體起符而全段無閉合 ──
    #    pandoc 遇不配對之起符不作斜體，逕以字面「*」印出，冊頁遂見游星。
    plain = FOOT.sub('', BRK.sub('', u'\n'.join(x[1] for x in b)))
    plain = re.sub(r'`[^`]*`', ' ', plain)
    plain = plain.replace(u'**', u'')
    n = plain.count(u'*')
    if n % 2 == 1 and OPENER.match(b[0][1]):
        odd += 1
        print(u'  游星 @行%s 單星奇數(%d 枚)且行首起符無閉｜%s' % (b[0][0] + 1, n, b[0][1][:56]))
print(u'==== 跨行吞字之段 %d 處＋行首游星之段 %d 處（印面範圍內始計）====' % (bad, odd))
sys.exit(1 if (bad or odd) else 0)
