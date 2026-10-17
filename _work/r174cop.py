# -*- coding: utf-8 -*-
"""r174cop.py —— 繫詞『是』之引號層級待診軸（第 174 輪立，恆退 0，不為閘）。

緣起：第 170 輪擴 `quotejudge` 時補入『此為／是為／所謂／謂之…』一族判定語氣，**裸『是』字未入**；
本書慣以「」掛逐字原文、以『』掛書語與自製之式（凡例第一條），故「X 是「楊」」一類
若『楊』非語料逐字，即屬冒充律語。本軸專掃此形，三桶分計：
  甲 語料逐字可查（合法，不判）
  乙 語料查無、且非名相／非卷次／非案例代號 ⇒ **病**（應改掛『』）
  丙 語料查無然屬名相／專名／引文內之引（從寬不判）
用法：`PYTHONPATH=. python -X utf8 _work/r174cop.py [--csv]`
"""
import io, os, re, sys, csv
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as t

L = t.LINES
BOT = t.bottom_lines()
N = len(L)
FEN = [False] * N
_in = False
for i, l in enumerate(L):
    if l.strip().startswith(u'```'):
        _in = not _in
        FEN[i] = True
        continue
    FEN[i] = _in
PRINT = [i for i in range(N) if i not in BOT and not FEN[i]]

QIN = re.compile(u'「([^」]{2,20})」')
COP = re.compile(u'(?:是|為|即|乃|稱|謂|叫)[^「」]{0,6}$')
NAMEY = re.compile(u'[卷經律論論阿毘達摩俱舍品句義戒心魔道閘門正理憲綱]$|^[甲乙丙丁戊己]')
NUM = re.compile(u'[0-9０-９]')
JIA, YI, BING = [], [], []
seen = set()
for i in PRINT:
    line = L[i]
    if not line.strip() or line.strip()[0] in u'|#':
        continue
    for m in QIN.finditer(line):
        term = m.group(1)
        n = t.norm(term)
        if len(n) < 2 or n in seen:
            continue
        head = line[max(0, m.start() - 10):m.start()]
        if not COP.search(head):
            continue
        seen.add(n)
        hit = n in t.VINAYA or any(n in v for v in t.OTHER.values())
        rec = (i + 1, term, re.sub(u'\\s+', u' ', line[max(0, m.start() - 26):m.end() + 16]))
        if hit:
            JIA.append(rec)
        elif NAMEY.search(term) or NUM.search(term) or u'『' in term:
            BING.append(rec)
        else:
            YI.append(rec)

for lab, rows in ((u'甲 語料逐字可查（合法）', JIA), (u'乙 語料查無且非名相（病，應改掛『』）', YI),
                  (u'丙 語料查無然屬名相／專名（從寬不判）', BING)):
    print(u'── %s：%d 處' % (lab, len(rows)))
    for ln, term, ctx in rows[:24]:
        print(u'   L%-6d 『%s』｜…%s…' % (ln, term, ctx))
print(u'\n== 合計：甲 %d、乙 %d、丙 %d ==' % (len(JIA), len(YI), len(BING)))
