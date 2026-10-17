"""第 165 輪產物層實證：目錄容量改尺前後，以無頭 Edge 各排一冊目錄小樣，
量其「頁碼是否被裁」與「最小字級」——不信算式，只信印出來的座標。

用法：python _work/r165tocproof.py
"""
import io, os, re, sys, time, tempfile, subprocess
import pymupdf as fitz

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_print'))
import build38 as B   # noqa

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HTML_SRC = os.path.join(ROOT, '_print', 'final38.html')
CSS = open(os.path.join(ROOT, '_print', 'print38.css'), encoding='utf-8').read() + B.PRINT_CSS
BOX_W = B.CONTENT_W_PT

def entries():
    h = io.open(HTML_SRC, encoding='utf-8').read()
    blk = re.search(r'(?s)<div class="toc-lead">(.*?)</div>', h).group(1)
    out = []
    for r in re.finditer(r'(?s)<p class="toc-line toc-l(\d)">\s*<span class="t"([^>]*)>(.*?)</span>'
                         r'<span class="d">(.*?)</span><span class="pg">(\d*)</span></p>', blk):
        title = re.sub(r'<[^>]+>', '', r.group(3)).strip()
        for lab in ('　　　　', '　　'):
            if title.startswith(lab):
                title = title[len(lab):]
                break
        shr = re.search(r'font-size:([\d.]+)pt', r.group(2))
        out.append((int(r.group(1)), title, r.group(5),
                    float(shr.group(1)) if shr else None, r.group(0)))
    return out

def page_of(lines, tag):
    html = ('<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8">'
            '<style>%s</style></head><body><div class="toc-lead"><h2>目錄</h2>%s</div></body></html>'
            % (CSS, '\n'.join(lines)))
    d = tempfile.mkdtemp(prefix='tocproof-')
    hh = os.path.join(d, tag + '.html')
    pp = os.path.join(HERE, 'r165_%s.pdf' % tag)     # 留樣供覆勘（結帳時隨暫存同清）
    io.open(hh, 'w', encoding='utf-8').write(html)
    br = B.find_browser()
    subprocess.run([br, '--headless=new', '--disable-gpu', '--no-first-run',
                    '--no-default-browser-check', '--disable-extensions',
                    '--user-data-dir=' + os.path.join(d, 'prof'),
                    '--no-pdf-header-footer', '--print-to-pdf=' + pp,
                    'file:///' + hh.replace(os.sep, '/')], check=True, timeout=600)
    t0 = time.time()
    last, same = -1, 0
    while time.time() - t0 < 120:
        try:
            sz = os.path.getsize(pp)
        except OSError:
            sz = -1
        if sz == last and sz > 0:
            same += 1
            if same >= 3:
                break
        else:
            same = 0
        last = sz
        time.sleep(0.25)
    return pp

def measure(pp, tag, n_ent):
    doc = fitz.open(pp)
    rows, sizes, clipped, nopg = [], [], 0, 0
    for i in range(doc.page_count):
        pg = doc.load_page(i)
        # 本頁內容右界：鏡像邊距，奇頁內緣 18mm 在右、偶頁在左
        inner = 18 if (i + 1) % 2 == 1 else 10
        rex = pg.rect.width - inner / 25.4 * 72
        for b in pg.get_text('dict').get('blocks', []):
            if b.get('type') != 0:
                continue
            for l in b.get('lines', []):
                sp = [s for s in l.get('spans', []) if s['text'].strip()]
                if not sp:
                    continue
                x1 = max(s['bbox'][2] for s in sp)
                txt = ''.join(s['text'] for s in sp).strip()
                if '.' not in txt:
                    continue                      # 目錄大標與頁腳羅馬字等非條目行
                sizes.append(round(sp[0]['size'], 1))
                if x1 > rex - 1.0:
                    clipped += 1
                    rows.append((i + 1, round(x1, 1), txt[-24:]))
                if not re.search(r'\d$', txt):
                    nopg += 1
    pgs = doc.page_count
    doc.close()
    print('%-6s 頁數 %d｜條目行 %d（應 %d）｜最小字級 %.1fpt｜觸及內容右界 %d｜失頁碼 %d'
          % (tag, pgs, len(sizes), n_ent, min(sizes), clipped, nopg))
    for r in rows[:6]:
        print('    p%-3d x1=%.1f  …%s' % r)
    return min(sizes), clipped + nopg, pgs

def diag(pp, n_show=6):
    """逐行比對『實測寬』與『算式估寬』，取差最大者示之（校 TOC_ADV 用）。"""
    doc = fitz.open(pp)
    rows = []
    for i in range(doc.page_count):
        for b in doc.load_page(i).get_text('dict').get('blocks', []):
            if b.get('type') != 0:
                continue
            for l in b.get('lines', []):
                sp = [s for s in l.get('spans', []) if s['text'].strip()]
                if not sp:
                    continue
                t = sp[0]
                if '.' in t['text']:
                    continue
                meas = t['bbox'][2] - t['bbox'][0]
                pred = B._wpt(t['text'], t['size'], 'Bold' in t['font'])
                rows.append((meas - pred, t['size'], meas, pred, t['text'][-18:]))
    doc.close()
    rows.sort(reverse=True)
    print('\n-- 實測減估算（pt）最大 %d 行 --' % n_show)
    for d, sz, m, p, tail in rows[:n_show]:
        print('   Δ%+5.2f  %4.1fpt  實測 %6.1f  估 %6.1f  …%s' % (d, sz, m, p, tail))
    tot = [r[0] for r in rows]
    print('   全 %d 行：Δ 中位 %+.2f、最大 %+.2f、最小 %+.2f' % (len(tot), sorted(tot)[len(tot)//2], max(tot), min(tot)))


def main():
    ents = entries()
    print('條目：%d｜版寬 %.1fpt（A4 減外 10mm／內 18mm）' % (len(ents), BOX_W))
    old = [e[4] for e in ents]                      # 現冊之目錄行，原樣再排一遍作對照
    new = [B.toc_line(lv, ti, pg) for lv, ti, pg, _, _ in ents]
    print('舊尺縮字條數：%d｜新尺縮字條數：%d'
          % (sum(1 for e in ents if e[3]), sum(1 for l in new if 'font-size' in l)))
    po = measure(page_of(old, 'old'), '舊尺', len(ents))
    pn_path = page_of(new, 'new')
    pn = measure(pn_path, '新尺', len(ents))
    diag(pn_path)
    print('\n斷言：新尺無一行觸及內容右界（頁碼不被裁）→ %s'
          % ('PASS' if pn[1] == 0 else 'FAIL'))
    print('斷言：新尺最小字級 ≥ 10.5pt（舊 %.1fpt）→ %s'
          % (po[0], 'PASS' if pn[0] >= 10.5 else 'FAIL'))

main()
