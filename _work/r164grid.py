# -*- coding: utf-8 -*-
"""r164grid.py —— 第 164 輪・產物層之『窄欄碎行』探針（待診，恆退 0）。

病相：`build38.retune_tables()` 以內容加權定 colgroup 欄寬，然設 6% 之下限；
     六欄以上之表若某欄內容極短而表頭極長（如『領域軸 \\ 心智軸』），該欄即被鉗於 6%，
     紙上遂成『領／域／軸／心／智軸』一字一行，是為碎行。
口徑：取 PDF 逐行文字，於同頁內找『相鄰三行以上、行首 x 相差 ≤4pt、每行 CJK ≤2 字』之豎列；
     含制表符（┌┐└┘│─►）之頁為 ASCII 圖，其短行屬圖制，不計。
用法：PYTHONPATH=. python _work/r164grid.py [冊路徑]
"""
import io, os, re, sys
import pymupdf as fitz

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    ROOT, '_print', 'ver38四分律_起心動念心智分析框架_第三十八版_列印版.pdf')
BOX = set(u'┌┐└┘├┤│─═►◄')   # 唯制表符判為圖頁；◆▲ 乃表內符號，不可混入
CJK = re.compile(u'[一-鿿]')
doc = fitz.open(PDF)
runs = []
for pno in range(len(doc)):
    page = doc[pno]
    txt = page.get_text()
    if len([c for c in txt if c in BOX]) > 3:      # 制表符三枚以上乃 ASCII 圖頁，不計
        continue
    d = page.get_text('dict')
    lines = []
    for b in d['blocks']:
        if b['type'] != 0:
            continue
        for l in b['lines']:
            t2 = ''.join(s['text'] for s in l['spans']).strip()
            if t2:
                lines.append((round(l['bbox'][1], 1), round(l['bbox'][0], 1), t2))
    lines.sort()
    cur = []
    for y, x, t2 in lines:
        n = len(CJK.findall(t2))
        if n <= 2 and len(t2) <= 4:
            if cur and abs(x - cur[-1][1]) <= 4 and 0 < y - cur[-1][0] <= 20:
                cur.append((y, x, t2))
            else:
                if len(cur) >= 3:
                    runs.append((pno + 1, cur))
                cur = [(y, x, t2)]
        else:
            if len(cur) >= 3:
                runs.append((pno + 1, cur))
            cur = []
    if len(cur) >= 3:
        runs.append((pno + 1, cur))
doc.close()
print(u'冊：%s｜頁 %d' % (os.path.basename(PDF), len(fitz.open(PDF))) if False else u'冊：%s' % os.path.basename(PDF))
print(u'窄欄碎行（相鄰三行以上、每行 CJK ≤2 字、行首同 x）：%d 處' % len(runs))
for pno, r in runs:
    print(u'  p%-4d x=%-6.1f %d 行｜%s' % (pno, r[0][1], len(r), u''.join(x[2] for x in r)[:34]))
sys.exit(0)
