# -*- coding: utf-8 -*-
"""負測：甲軸（表欄數＋表頭空欄）究竟逮不逮到病。

第 119 輪之起因：精簡本三十格小表之表頭漏寫『癡』一字，欄數檢全綠而印面殘缺——
故新立『表頭空格』一目，並依例先負測（沒逮過的軸等於沒有軸）。全程在記憶體中
做字串手術，不印暫存 PDF、不落盤。
用法：python _work/negtest_axisa.py
"""
import importlib.util, os, re, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
spec = importlib.util.spec_from_file_location('tblaudit', os.path.join(HERE, 'tblaudit.py'))
ta = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ta)

src = os.path.join(ROOT, '_print', 'final38_精簡本.html')
html = open(src, encoding='utf-8').read()

tbls, n0, h0 = ta.axis_a(html)
print(u'基準：%d 張表｜欄數不合 %d｜表頭空格 %d' % (len(tbls), len(n0), len(h0)))
for x in (n0 + h0)[:5]:
    print(u'   基準即有恙：%s' % x)

# ── 病一：把某表之第三個表頭掏空（本輪『癡』欄之病，欄數不變故舊檢全綠）──
tb = next(t for t in tbls if len(re.findall(r'(?s)<th\b[^>]*>.*?</th>', t)) >= 3)
heads = list(re.finditer(r'(?s)(<th\b[^>]*>)(.*?)(</th>)', tb))
h = heads[2]
tb1 = tb[:h.start(2)] + tb[h.end(2):]                   # 內容挖空，標籤與欄數俱在
neg1 = html.replace(tb, tb1, 1)
assert neg1 != html, u'病一未注入'
_t, _n1, h1 = ta.axis_a(neg1)

# ── 病二：同一表之正文某列少寫一格（欄數軸之舊能力，一并驗其未壞）──
row = next(r for r in re.findall(r'(?s)<tr[^>]*>(.*?)</tr>', tb1)
           if r.count(u'<td') >= 2)
c = list(re.finditer(r'(?s)<td\b[^>]*>.*?</td>', row))[-1]
row2 = row[:c.start()] + row[c.end():]
tb2 = tb1.replace(row, row2, 1)
neg2 = neg1.replace(tb1, tb2, 1)
assert neg2 != neg1, u'病二未注入'
_t, n2, _h2 = ta.axis_a(neg2)

print(u'負測一（掏空表頭第 3 格）：表頭空格 %d 處 → %s' % (
    len(h1), h1[0] if h1 else u'逮不到'))
print(u'負測二（正文列少一格）：欄數不合 %d 處 → %s' % (
    len(n2), n2[0] if n2 else u'逮不到'))

ok = (not n0 and not h0) and len(h1) == 1 and len(n2) == 1
print(u'判定：%s' % (u'甲軸兩目皆有效（基準零誤報、兩病皆逮）' if ok else u'甲軸不可信——須改驗法'))
sys.exit(0 if ok else 1)
