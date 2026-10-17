# -*- coding: utf-8 -*-
"""第七章總表之「生活領域」欄 ↔ 第五章三十格矩陣各格所列案例，兩方歸屬是否一致。"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk

ROOT = _tk.ROOT
L = _tk.LINES
TAG = re.compile(u'〔([遮開僧])(\\d{1,2})〕')
DOMS = [u'個人修煉', u'人際互動', u'僧團事務', u'僧團與社會邊界', u'危機與特殊時刻', u'照護與護生專業']

s5, e5 = _tk.sec(u'第五章')
s7, e7 = _tk.sec(u'第七章')
s8, e8 = _tk.sec(u'第八章')

# 1) 第七章總表：行如 | **〔遮25〕** | 標題 | 根本心 | 領域 | 正理 | ...
book_dom = {}
for i in range(s7, e7):
    ln = L[i]
    if not ln.startswith(u'|'):
        continue
    t = TAG.search(ln)
    if not t:
        continue
    key = u'〔%s%s〕' % (t.group(1), t.group(2))
    cells = [c.strip() for c in ln.strip(u'|').split(u'|')]
    hit = [c for c in cells if any(d in c for d in DOMS) and len(c) <= 14]
    if hit and key not in book_dom:
        book_dom[key] = hit[0]

# 2) 第五章三十格矩陣：找含大量案例標籤之表格列，取其行首領域名
mx = {}
for i in range(s5, e5):
    ln = L[i]
    if not ln.startswith(u'|') or len(TAG.findall(ln)) < 3:
        continue
    cells = [c.strip() for c in ln.strip(u'|').split(u'|')]
    head = cells[0]
    dom = None
    for d in DOMS:
        if d in head:
            dom = d
            break
    if not dom:
        continue
    for t in TAG.findall(ln):
        key = u'〔%s%s〕' % (t[0], t[1])
        mx.setdefault(key, set()).add(dom)

out = [u'第七章取得領域 %d 案；第五章矩陣取得歸格 %d 案' % (len(book_dom), len(mx))]
bad = 0
for k in sorted(set(book_dom) & set(mx)):
    d = book_dom[k]
    dd = min(mx[k], key=lambda x: len(x))
    a = d[:4].replace(u'財', u'責')
    b = dd[:4].replace(u'財', u'責')
    if a not in d or b not in dd:
        pass
    if not (d[:3] in u''.join(mx[k]) or any(m[:3] in d for m in mx[k])):
        bad += 1
        out.append(u'差異 %s：總表「%s」 vs 矩陣「%s」' % (k, d, u'/'.join(sorted(mx[k]))))
out.append(u'兩方俱有之案 %d；歸屬不一致 %d' % (len(set(book_dom) & set(mx)), bad))
missing = sorted(set(book_dom) - set(mx))
out.append(u'矩陣中未見（或該格未以六大領域命名）之案數：%d' % len(missing))
io.open(os.path.join(ROOT, u'_work', u'dom.txt'), 'w', encoding=u'utf-8').write(u'\n'.join(out))
print(len(book_dom), len(mx), bad)
