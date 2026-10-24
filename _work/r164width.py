# -*- coding: utf-8 -*-
"""r164width.py —— 第 164 輪・表格欄寬之源層診斷（待診，恆退 0）。

問：`build38.retune_tables()` 設欄寬下限 6%，而 CAP=104、PAD=2.4 ⇒ 6% 之欄每行僅
    6/100*104-2.4 ≈ 3.8 個半形單位＝**1.9 個漢字**，標籤欄遂一字一行。
法：讀中介 HTML 之各表（含 colgroup），逐欄算其『每行漢字數』與『欄內最長短格（標籤）之字數』，
    報『每行漢字 < 3 而最長短格 ≥4 字』之欄——即紙上必成碎行者。
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, '_print', 'ver38_列印版.html')
CAP, PAD = 104.0, 2.4


def cw(s):
    s = re.sub(r'(?s)<[^>]+>', '', s)
    s = s.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    return sum(2 if ord(ch) > 0x2E80 else 1 for ch in s)


if not os.path.isfile(HTML):
    # 待診軸自稱恆退 0：中介 HTML 乃建冊腳手，清場即除——無法源時明報未行，不可崩退壞跑批
    print('中介 HTML 未在：%s（建冊方生・清場即除）｜此軸未行' % os.path.relpath(HTML, ROOT))
    sys.exit(0)
h = io.open(HTML, encoding='utf-8').read()
tabs = re.findall(r'(?s)<table[^>]*>(.*?)</table>', h)
bad = []
for ti, tb in enumerate(tabs):
    ws = [float(x) for x in re.findall(r'width:\s*([0-9.]+)%', tb)]
    if not ws:
        continue
    rows = re.findall(r'(?s)<tr>(.*?)</tr>', tb)
    cells = [re.findall(r'(?s)<t[hd][^>]*>(.*?)</t[hd]>', r) for r in rows]
    n = max((len(c) for c in cells), default=0)
    if n < 2 or len(ws) != n:
        continue
    units = [[cw(c) for c in cs] + [0] * (n - len(cs)) for cs in cells]
    for i in range(n):
        per = (ws[i] / 100.0 * CAP - PAD) / 2.0          # 每行可容漢字數
        labs = [u[i] / 2.0 for u in units if 0 < u[i] <= 24]
        if not labs:
            continue
        mx = max(labs)
        if per < 3.0 and mx >= 4.0:
            head = re.sub(r'(?s)<[^>]+>', '', cells[0][i])[:16] if cells and cells[0] else u'?'
            bad.append((ti + 1, i + 1, len(ws), ws[i], per, mx, head))
print(u'冊：%s｜表 %d 張' % (os.path.basename(HTML), len(tabs)))
print(u'碎行之欄（每行漢字 <3 而最長標籤 ≥4 字）：%d 欄' % len(bad))
seen = {}
for ti, ci, n, w, per, mx, head in bad:
    seen.setdefault(ti, []).append((ci, w, per, mx, head))
for ti in sorted(seen):
    print(u'  表 %-3d：' % ti +
          u'；'.join(u'第%d欄 %.1f%%→每行 %.1f 字（標籤 %.0f 字「%s」）' % (c, w, per, mx, hd)
                     for c, w, per, mx, hd in seen[ti]))
sys.exit(0)
