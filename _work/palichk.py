# -*- coding: utf-8 -*-
"""查印面之外文名相（含長音符／下加點者）是否失真。

緣起：目測 p.31 見「Cetan a」「Sam a dhi」「Prajñ a」之類斷字——疑為字型切換所致，
      而字型切換只該多插空白，不該吃掉長音符。故此軸分三級報：
      甲、原詞連空白可核（最宽口径）；
      乙、去盡空白可核（僅屬斷字，印面仍含正確字符）；
      丙、連去空白都核不到（字符真的不見＝印面失真）。
"""
import io, os, re, sys
import pymupdf as fitz

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, 'ver38四分律_起心動念心智分析框架_修正版.md')
P = os.path.join(ROOT, '_print')
DIAC = u'ĀāĪīŪūṚṛḸḷṂṃṄṅÑñṬṭḌḍṆŚśṢṣĀ'
TERM = re.compile(u'[A-Za-z%s\\-\\u00c0-\\u024F]{3,}' % DIAC)

doc_md = io.open(MD, encoding='utf-8').read()
terms = {}
for m in TERM.finditer(doc_md):
    w = m.group(0)
    if any(c in DIAC for c in w):
        terms[w] = terms.get(w, 0) + 1
terms = {k: v for k, v in terms.items() if v >= 2}
print(u'書中（含底冊）之外文名相：%d 目（出現 ≥2 次者），總見 %d 次' % (
    len(terms), sum(terms.values())))

for fn in ['ver38四分律_起心動念心智分析框架_第三十八版_列印版.pdf',
           'ver38四分律_起心動念心智分析框架_第三十八版_列印版_精簡本.pdf']:
    doc = fitz.open(os.path.join(P, fn))
    txt = u''.join(doc[i].get_text() for i in range(len(doc)))
    txt2 = re.sub(u'\\s+', u'', txt)
    printed = {k: v for k, v in terms.items() if k in txt}
    a = [k for k in printed if k in txt]
    c = [k for k in printed if k not in txt and k not in txt2]
    b = [k for k in printed if k not in txt and k in txt2]
    print(u'【%s】印面見此類名相 %d 目' % (fn[-14:], len(printed)))
    print(u'   甲 原形可核 %d｜乙 僅斷字（去空白可核）%d｜丙 字符不見 %d' % (len(a), len(b), len(c)))
    if b:
        print(u'   乙 例：%s' % u'、'.join(b[:12]))
    if c:
        print(u'   丙 例：%s' % u'、'.join(c[:12]))
    # 斷字之實據：抽一詞看印面前後文
    for probe in (u'Cetanā', u'Samādhi', u'Prajñā', u'ā'):
        i = txt.find(probe)
        if i >= 0:
            print(u'   印面「%s」上下文：%s' % (probe, repr(txt[max(0, i - 12):i + 16])))
            break
    doc.close()
