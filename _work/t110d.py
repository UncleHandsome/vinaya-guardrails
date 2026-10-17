# -*- coding: utf-8 -*-
"""全書普查：48 張表逐張定位到 PDF 頁，數該頁之「格線級」繪圖，與 class=keep 對照。"""
import io, re, fitz
from collections import Counter

OUT = io.open(u'_work/t110d.txt', 'w', encoding='utf-8')
def say(s): OUT.write(s + u'\n')

src = io.open(u'_print/final38.html', encoding='utf-8').read()
tbls = re.findall(u'(?s)<table([^>]*)>(.*?)</table>', src)
say(u'表數 %d；帶 keep %d' % (len(tbls), sum(1 for a, _ in tbls if 'keep' in a)))

doc = fitz.open(u'_print/ver38四分律_起心動念心智分析框架_第三十八版_列印版.pdf')
pagetext = [doc[i].get_text() for i in range(len(doc))]
pagetag = {}
def gridcount(pno):
    if pno in pagetag:
        return pagetag[pno]
    d = doc[pno - 1].get_drawings()
    n = sum(1 for x in d if x['rect'].width < 2.5 or x['rect'].height < 2.5)
    big = sum(1 for x in d if x['rect'].width > 400)
    pagetag[pno] = (n, big, len(d))
    return pagetag[pno]

def norm(s):
    return re.sub(u'\\s+', u'', re.sub(u'<[^>]+>', u'', s))

bad, good, unk = [], [], []
for idx, (attrs, body) in enumerate(tbls):
    ths = re.findall(u'(?s)<th[^>]*>(.*?)</th>', body)
    key = norm(ths[0]) if ths else norm(body)[:12]
    key2 = norm(ths[1]) if len(ths) > 1 else u''
    pages = [i + 1 for i, t in enumerate(pagetext) if key and key in t.replace(u' ', u'')]
    if not pages:
        unk.append((idx + 1, key[:10]))
        continue
    n, big, tot = gridcount(pages[0])
    rec = (idx + 1, u'keep' if 'keep' in attrs else u'-   ', key[:10], pages[0], n, big, tot)
    (good if n >= 6 else bad).append(rec)

say(u'—— 疑無格線（格線級繪圖 <6）——')
for r in bad:
    say(u'  表%02d %s 「%s」 頁%s 細線%d 寬條%d 總%d' % r)
say(u'—— 有格線 ——')
for r in good:
    say(u'  表%02d %s 「%s」 頁%s 細線%d 寬條%d 總%d' % r)
say(u'未定位：%s' % (unk,))
say(u'統計 無格線 %d／有格線 %d；其中 keep 於無格線者 %d，keep 於有格線者 %d' % (
    len(bad), len(good), sum(1 for r in bad if r[1] == u'keep'),
    sum(1 for r in good if r[1] == u'keep')))
doc.close(); OUT.close()
