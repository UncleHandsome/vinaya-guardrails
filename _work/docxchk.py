# -*- coding: utf-8 -*-
"""docxchk.py —— 交付冊 Word 文字層之 markdown／HTML 殘相抽驗（第 143 輪立）。

緣起：歷輪產物層只驗 PDF（格線、邊界、鎖頁、字形、書籤、文字抽驗），DOCX 一路四式從未掃過。
本軸取 word/document.xml 去標籤後之純文字，查若干式 markdown／HTML 未轉化之殘相。
『[ ]』（存檔卡之勾選框）與『◈本書法式』（本書自制之法式標記）乃刻意保留，不入黑名單。
退出碼：不合格 > 0 即退 1。
"""
import io, os, re, sys, zipfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pymupdf as fitz  # noqa: F401  （僅為统一依賴入口，本軸不用）

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, u'_print')
BOOKS = [u'ver38四分律_起心動念心智分析框架_第三十八版_列印版',
         u'ver38四分律_起心動念心智分析框架_第三十八版_螢幕版',
         u'ver38四分律_起心動念心智分析框架_第三十八版_列印版_精簡本',
         u'ver38四分律_起心動念心智分析框架_第三十八版_螢幕版_精簡本']
ART = (u'**', u'```', u'<br', u'&nbsp', u'&amp;', u'<!--', u'SLIM-', u'\\(', u'・',
       u'|---', u'~~', u'\\[', u'\\]', u'</', u'<span', u'<div')
bad = 0
for stem in BOOKS:
    f = os.path.join(P, stem + u'.docx')
    if not os.path.exists(f):
        print(u'缺檔：%s' % stem[-14:])
        bad += 1
        continue
    xml = zipfile.ZipFile(f).read('word/document.xml').decode('utf-8', 'replace')
    txt = re.sub(u'<[^>]+>', u'', xml)
    txt = txt.replace(u'&lt;', u'<').replace(u'&gt;', u'>').replace(u'&amp;', u'&')
    hits = [(a, txt.count(a)) for a in ART if txt.count(a)]
    bad += len(hits)
    print(u'%-14s 文字 %6d 字｜殘相 %s' % (stem.split(u'第三十八版')[-1][:12], len(txt),
                                          hits if hits else u'無'))
print(u'==== DOCX 文字層殘相：不合格 %d 處 ====' % bad)
sys.exit(1 if bad else 0)
