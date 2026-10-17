# -*- coding: utf-8 -*-
r"""r243long　印面長句清冊（第 243 輪立，待診・專軸，恆退 0）

   所以立之：作者命『其他章節依卷首與第一章兩範例重新調整』。兩範例之實質唯**以標點拆長句**
   （外加個別『的／是』級補字），故本軸只量一事：**印面逐行切句後，句逾 80 字者幾處**——
   此即兩範例自報成效所用之同一口徑（卷首 >80 由 3 減為 1；第一章由 11 減為 7、>100 歸零）。
   口徑：剔底冊四篇、剔圍欄、剔表列與標題行；**引言塊（> ）與列表項俱收**（第一章八處中五處在列表項內）。
   報而不挡：長句之拆與否涉文意，唯清冊可恃，故退 0。
"""
import re, sys
sys.path.insert(0, '.')
import _tk as t

L = t.LINES
BOT = t.bottom_lines()
CJK = re.compile(u'[一-鿿]')
FENCE = set()
run = False
for i in range(len(L)):
    if L[i].startswith(u'```'):
        run = not run
        FENCE.add(i)
        continue
    if run:
        FENCE.add(i)

CH, cur = {}, u'卷首'
for i, l in enumerate(L):
    m = re.match(u'^# (第[一二三四五六七八九]章|結語|終卷|附錄\\S+)', l)
    if m:
        cur = m.group(1)
    CH.setdefault(cur, []).append(i)
ORDER = [u'卷首'] + [u'第%s章' % x for x in u'一二三四五六七八九'] + [u'結語']
rows = []
for c in ORDER + [k for k in CH if k.startswith(u'附錄')]:
    n80 = n100 = mx = 0
    for i in CH.get(c, []):
        if i in BOT or i in FENCE:
            continue
        s = L[i].strip()
        if not s or s[0] in u'#|':      # 表列非句：三十格矩陣以 <br> 堆格，計之必假陽性（第 210 輪同誡）
            continue
        s = re.sub(u'^([*\\-] |\\d+\\. )+', u'', s)
        for seg in re.split(u'[。；！？]', s):
            n = len(CJK.findall(seg))
            if n > 80:
                n80 += 1
                rows.append((c, i + 1, n))
            if n > 100:
                n100 += 1
            mx = max(mx, n)
    print(u'%-8s >80：%3d｜>100：%3d｜最長：%3d' % (c, n80, n100, mx))
print(u'合计 >80 字之句：%d' % len(rows))
if len(sys.argv) > 1 and sys.argv[1] == u'--list':
    for c, ln, n in sorted(rows, key=lambda x: -x[2])[:40]:
        print(u'   %-6s L%-6d %3d 字' % (c, ln, n))
sys.exit(0)
