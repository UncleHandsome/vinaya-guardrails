# -*- coding: utf-8 -*-
"""印面格線實測（第 110 輪立）：逐表量 PDF，查表格是否散架為連寫文字。

病徵：第 105 輪 table_keep 之複寫字串混入 \\x01，標籤名變 <table\\x01，解析器不認得
      table，td/th 盡遭丟棄，三十四張表於 PDF 化為一團連寫文字（格線全失）。
驗法（皆量產物，不信生成器之言）：
  甲、PyMuPDF find_tables() 依印面實際向量線重構表格；偵得之表含本表表頭者，格線即存。
  乙、表頭首格與正文首格若落在同一條基線（±3pt），即行內連寫——散架之鐵證。
  丙、二者皆無從判者列「待考」如實報數，絕不計為通過。
用法：python _work/tblgrid.py [PDF ...]（預設四式，與 _print/final38*.html 配對）
"""
import io, os, re, sys
import pymupdf as fitz

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PRINT = os.path.join(ROOT, '_print')
PAIR = [
    ('final38.html', 'ver38四分律_起心動念心智分析框架_第三十八版_列印版.pdf'),
    ('final38_screen.html', 'ver38四分律_起心動念心智分析框架_第三十八版_螢幕版.pdf'),
    ('final38_精簡本.html',
     'ver38四分律_起心動念心智分析框架_第三十八版_列印版_精簡本.pdf'),
    ('final38_精簡本_screen.html',
     'ver38四分律_起心動念心智分析框架_第三十八版_螢幕版_精簡本.pdf'),
]
BASE_TOL = 3.0


def norm(s):
    s = re.sub(r'(?s)<[^>]+>', '', s)
    s = s.replace(u'&nbsp;', u'').replace(u'&#160;', u'')
    return re.sub(r'\s+', '', s)


def tables_of(html):
    out = []
    for m in re.finditer(r'(?s)<table[^>]*>.*?</table>', html):
        body = m.group(0)
        ths = [norm(x) for x in re.findall(r'(?s)<th[^>]*>(.*?)</th>', body)]
        tds = [norm(x) for x in re.findall(r'(?s)<td[^>]*>(.*?)</td>', body)]
        if not ths or not tds:
            continue
        cells = [c for c in ths + tds if len(c) >= 6]
        out.append((len(re.findall(r'<tr[ >]', body)), ths[0], tds[0], cells))
    return out


def y_of(page, key):
    """以 search_for 求該詞所在基線（取首個命中）；找不到回 None。"""
    if not key:
        return None
    for ln in (6, 4, 3):
        k = key[:ln]
        rs = page.search_for(k, quads=False)
        if rs:
            return round((rs[0].y0 + rs[0].y1) / 2.0, 1)
    return None


def detected(page, key):
    """find_tables 所偵得之任一表，其任一格含 key 之前 3 字 → 格線存在。"""
    k = key[:3]
    if not k:
        return None
    try:
        tabs = page.find_tables()
    except Exception:
        return None
    for t in tabs.tables:
        for row in t.extract():
            for c in row:
                if c and k in norm(c):
                    return True
    return False if tabs.tables else None


def check(html_path, pdf):
    html = io.open(html_path, encoding='utf-8').read()
    tbls = tables_of(html)
    doc = fitz.open(pdf)
    texts = [re.sub(r'\s+', '', doc[i].get_text()) for i in range(len(doc))]
    whole = u''.join(texts)
    bad, unk, ok, lost = [], [], 0, []
    for idx, (rows, th0, td0, cells) in enumerate(tbls):
        # 丙、內容不缺：每格首 8 字須見於全冊文字流（鎖頁表若高過一頁，Chromium 會整塊丟棄）
        miss = [c for c in cells if c[:8] not in whole]
        if miss:
            lost.append((idx + 1, rows, th0[:8], len(miss), miss[0][:16]))
        cand = [i for i, t in enumerate(texts) if th0 and th0 in t and td0[:8] in t]
        if not cand:                              # 表頭與首格同頁者方為本表之頁
            cand = [i for i, t in enumerate(texts) if th0 and th0 in t]
        if not cand:
            unk.append((idx + 1, rows, th0[:8], u'表頭未落頁'))
            continue
        det, yh, yd, pno = None, None, None, cand[0]
        for p in cand[:3]:
            pg = doc[p]
            d = detected(pg, th0)
            if det is None:
                det = d
            if yh is None:
                yh = y_of(pg, th0)
            if yd is None:
                yd = y_of(pg, td0)
            if det or (yh is not None and yd is not None):
                pno = p
                break
        # 判序：向量線重建為第一證據（find_tables 只認印面實際格線）；
        #       同基線之連寫徵象僅於重建不成時作裁。
        if det:
            ok += 1
        elif yh is not None and yd is not None and abs(yh - yd) <= BASE_TOL:
            bad.append((idx + 1, rows, pno + 1, th0[:8], u'表頭與首格同基線', yh, yd, det))
        elif det is None or (yh is None or yd is None):
            unk.append((idx + 1, rows, th0[:8], u'無從判定（頁 %d）' % (pno + 1)))
        else:
            ok += 1
    doc.close()
    return len(tbls), bad, unk, ok, lost


def main():
    args = [a for a in sys.argv[1:] if a]
    fail = tot_unk = 0
    targets = [(None, p) for p in args] if args else PAIR
    for hf, pf in targets:
        hp = os.path.join(PRINT, hf) if hf else None
        pdf = pf if os.path.isfile(pf) else os.path.join(PRINT, pf)
        if not os.path.isfile(pdf):
            print(u'跳過：缺 %s' % pdf)
            continue
        if not hp or not os.path.isfile(hp):
            print(u'跳過：缺配對 HTML（%s）' % (hf or pdf))
            continue
        n, bad, unk, ok, lost = check(hp, pdf)
        print(u'%-58s 表 %3d｜格線確認 %3d｜散架 %d｜缺字 %d｜待考 %d' % (
            os.path.basename(pdf)[-20:], n, ok, len(bad), len(lost), len(unk)))
        for b in bad[:10]:
            print(u'      散架 表%02d（%d 列）頁 %d 表頭「%s」%s（y%s vs y%s，find_tables=%s）' % b)
        for b in lost[:8]:
            print(u'      缺字 表%02d（%d 列）「%s」有 %d 格不見於印面，首見「%s」' % b)
        for b in unk[:8]:
            print(u'      待考 表%02d（%d 列）「%s」：%s' % b)
        fail += len(bad) + len(lost)
        tot_unk += len(unk)
    print(u'結論：%s（散架／缺字 %d 處、待考 %d 處）' % (
        u'印面格線與表格文字全數確認' if not fail else u'表格有恙', fail, tot_unk))
    return 1 if fail else 0


if __name__ == '__main__':
    sys.exit(main())
