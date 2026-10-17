# -*- coding: utf-8 -*-
"""widow.py —— 印面之孤懸標題與近空頁（第 143 輪立，產物層）。

口徑：以成品 PDF 之文字塊為據（不信源檔）。① 若某頁最後一個文字塊恰為書中某級標題
（H1–H4，去空白後全等或為其前綴），是為『孤懸標題』——標題與其下之文分家，屬真病；
② 若某頁正文不足 130 字（卷首 12 頁後），列『近空頁』如實報而不判死——章末短頁、
篇末結語之自然收尾皆屬此類，唯須讓後輪看得见。
退出碼：孤懸標題 > 0 即退 1。
"""
import io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pymupdf as fitz

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, u'_print')
MD = os.path.join(ROOT, u'ver38四分律_起心動念心智分析框架_修正版.md')
BOOKS = [(u'完整·影印', u'ver38四分律_起心動念心智分析框架_第三十八版_列印版.pdf'),
         (u'完整·螢幕', u'ver38四分律_起心動念心智分析框架_第三十八版_螢幕版.pdf'),
         (u'精簡·影印', u'ver38四分律_起心動念心智分析框架_第三十八版_列印版_精簡本.pdf'),
         (u'精簡·螢幕', u'ver38四分律_起心動念心智分析框架_第三十八版_螢幕版_精簡本.pdf')]
FLAT = lambda s: re.sub(u'\\s+', u'', s)

heads = set()
for l in open(MD, encoding='utf-8').read().split(u'\n'):
    m = re.match(u'^#{1,4} (.*)$', l)
    if m:
        t = FLAT(m.group(1).replace(u'**', u''))
        if len(t) >= 4:
            heads.add(t)
print(u'源檔標題集：%d 條（H1–H4）' % len(heads))
bad = 0
for tag, fn in BOOKS:
    path = os.path.join(P, fn)
    if not os.path.exists(path):
        print(u'缺檔 %s' % tag)
        bad += 1
        continue
    doc = fitz.open(path)
    wid, thin = [], []
    for pi, pg in enumerate(doc):
        blocks = [b for b in pg.get_text('blocks') if FLAT(b[4])]
        if not blocks:
            if pi > 12:
                thin.append((pi + 1, 0))
            continue
        last = FLAT(blocks[-1][4])
        if last in heads or any(h.startswith(last) and len(last) > 8 for h in heads):
            wid.append((pi + 1, blocks[-1][4].strip()[:40]))
        n = sum(len(FLAT(b[4])) for b in blocks)
        if n < 130 and pi > 12:
            thin.append((pi + 1, n))
    npg = doc.page_count
    doc.close()
    bad += len(wid)
    print(u'%-8s 頁 %3d｜孤懸標題 %d %s｜近空頁（待考）%d %s' % (
        tag, npg, len(wid), [p for p, _ in wid][:6],
        len(thin), [(p, n) for p, n in thin][:6]))
print(u'==== 孤懸標題：不合格 %d 處（近空頁只報不判）====' % bad)
sys.exit(1 if bad else 0)
