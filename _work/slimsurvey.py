# -*- coding: utf-8 -*-
"""精簡本減重之實測盤點：以「實際印出之物」為準，量每一塊之字數與所占頁數，排名以待裁。

口徑：
  一、內容取自 `_print/final38_精簡本.html`（已是 slim 過濾後者，非工作檔），
      故附錄C～M 與第六章 ◎原典 段之省略天然計入。
  二、字數＝去標籤後之純字（含標點）；頁數估＝字數 ÷ 每頁實測均字數（由 PDF 文字層量得）。
  三、標題層級：h1＝篇、h2＝節（卷首之目）、h3＝節、h4＝款、h5＝目；块之範圍＝至下一同級或更高級標題。
用法：python _work/slimsurvey.py [topN]
"""
import io, os, re, sys
import html as H
import pymupdf as fitz

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P = os.path.join(ROOT, '_print')
HTML = os.path.join(P, 'final38_精簡本.html')
PDF = os.path.join(P, 'ver38四分律_起心動念心智分析框架_第三十八版_列印版_精簡本.pdf')

TOPN = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 40

raw = io.open(HTML, encoding='utf-8').read()
# 砍去封面／目錄／CSS，只留正文（自 body-anchor 起）
i = raw.find('<!--BODY-ANCHOR-->')
if i < 0:
    i = raw.find('<h1')
body = raw[i:]

tok = re.compile(r'(?s)<(h[1-5])[^>]*>(.*?)</\1>')
items = []
ms = list(tok.finditer(body))
for k, m in enumerate(ms):
    lvl = int(m.group(1)[1])
    title = H.unescape(re.sub(r'(?s)<[^>]+>', '', m.group(2)))
    title = re.sub(r'\s+', '', title)[:34]
    # 块之範圍：至下一個層級 ≤ 本層級之標題
    end = len(body)
    for n in range(k + 1, len(ms)):
        if int(ms[n].group(1)[1]) <= lvl:
            end = ms[n].start()
            break
    seg = body[m.end():end]
    txt = H.unescape(re.sub(r'(?s)<[^>]+>', '', seg))
    txt = re.sub(r'\s+', '', txt)
    items.append((lvl, title, len(txt), k))

doc = fitz.open(PDF)
npages = len(doc)
alltext = sum(len(re.sub(r'\s+', '', doc[i].get_text())) for i in range(npages))
per_page = alltext / float(npages)
print(u'精簡本：正文標題 %d 則｜全冊文字 %s 字／%d 頁＝每頁均 %.0f 字' % (
    len(items), format(alltext, ','), npages, per_page))

# 各篇（h1）之規模
h1 = [(t, c) for l, t, c, _ in items if l == 1]
print(u'\n—— 各篇字數與估頁 ——')
tot = 0
for t, c in h1:
    tot += c
    print(u'  %-30s %8s 字 ≈ %5.1f 頁' % (t, format(c, ','), c / per_page))
print(u'  %s合計 %s 字 ≈ %.0f 頁（冊身 %d 頁，差者為目錄與封面等前置）' % (
    u'　' * 15, format(tot, ','), tot / per_page, npages))

# 減重候選：h4／h5 之最大塊（附其父級）
def parent(k, lvl_want):
    for m2 in [x for x in items if x[3] < k and x[0] == lvl_want][-1:]:
        return m2[1]
    return u''
cand = [(l, t, c, parent(k, 1), parent(k, 3)) for l, t, c, k in items if l in (2, 3, 4, 5)]
cand.sort(key=lambda x: -x[2])
print(u'\n—— 最大之可削單元（前 %d，按字數）——' % TOPN)
print(u'  %-3s %-26s %8s %6s  %s' % (u'級', u'標題', u'字', u'頁', u'所屬'))
for l, t, c, p1, p3 in cand[:TOPN]:
    if c < per_page * 0.35:
        break
    print(u'  h%-2d %-26s %8s %6.2f  %s／%s' % (l, t[:26], format(c, ','), c / per_page,
                                                p1[:12], p3[:16]))

# 大表（按 <table> 字數）
tbls = re.findall(r'(?s)<table[^>]*>.*?</table>', body)
tl = sorted(((len(re.sub(r'\s+', '', H.unescape(re.sub(r'(?s)<[^>]+>', '', t)))), j)
             for j, t in enumerate(tbls)), reverse=True)
print(u'\n—— 最大之表（前 12）——')
for c, j in tl[:12]:
    head = re.sub(r'\s+', '', H.unescape(re.sub(r'(?s)<[^>]+>', u'', tbls[j])))[:26]
    print(u'  表%02d %8s 字 ≈ %5.2f 頁  「%s」' % (j + 1, format(c, ','), c / per_page, head))

# 第六章逐案之欄位普查（百則佔全冊四分之一，減重之最大槓桿在此）
h1s = [(m.start(), H.unescape(re.sub(r'(?s)<[^>]+>', '', m.group(1))))
       for m in re.finditer(r'(?s)<h1[^>]*>(.*?)</h1>', body)]
i6 = next((s for s, t in h1s if u'第六章' in t), -1)
i7 = next((s for s, t in h1s if u'第七章' in t and s > i6), len(body))
b6 = body[i6:i7]
print(u'\n—— 第六章欄位普查（%s 字 ≈ %.1f 頁，佔全冊 %.0f%%）——' % (
    format(len(re.sub(r'\s+', '', H.unescape(re.sub(r'(?s)<[^>]+>', '', b6)))), ','),
    len(re.sub(r'\s+', '', H.unescape(re.sub(r'(?s)<[^>]+>', '', b6)))) / per_page,
    100.0 * len(re.sub(r'\s+', '', H.unescape(re.sub(r'(?s)<[^>]+>', '', b6)))) / alltext))
FIELDS = [u'定位行', u'事相', u'判', u'行法指引', u'心相', u'治道', u'現行法對照',
          u'所據戒條', u'互見', u'案', u'觀心', u'界碑', u'要旨']
seen = {}
for m in re.finditer(r'(?s)<strong>([^<]{2,14})[：:]</strong>', b6):
    lab = H.unescape(m.group(1)).strip()
    seen[lab] = seen.get(lab, 0) + 1
tops = sorted(seen.items(), key=lambda kv: -kv[1])[:18]
for lab, n in tops:
    # 該欄位之總字數：由標籤起至下一標籤／下一案
    tot = 0
    for m in re.finditer(r'(?s)<strong>%s[：:]?</strong>' % re.escape(lab), b6):
        e = len(b6)
        for m2 in re.finditer(r'(?s)<strong>[^<]{2,14}[：:]</strong>|<h5[ >]', b6[m.end():]):
            e = m.end() + m2.start()
            break
        tot += len(re.sub(r'\s+', '', H.unescape(re.sub(r'(?s)<[^>]+>', '', b6[m.end():e]))))
    print(u'  %-14s %3d 見｜共 %7s 字 ≈ %5.2f 頁' % (lab, n, format(tot, ','), tot / per_page))
doc.close()
