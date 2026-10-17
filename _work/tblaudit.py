# -*- coding: utf-8 -*-
"""表圖全面產物層健檢（第 111 輪立）。

只量交付物（PDF）與其所自之 HTML，五類病各立一口徑：
  甲 表結構：表頭欄數與每一列欄數是否齊（HTML 端，格線之外另須欄數對）；
     另查表頭空欄——欄數齊不等於表頭齊，漏一名（如三十格表之「癡」欄）欄數檢全綠而印面残缺。
  乙 印面格線：沿用 tblgrid.check()（find_tables 為第一證據）。
  丙 版心外溢：任一詞之右緣逾「物理邊界減最小邊距」，或左緣逾左界——含表格長詞、
              ASCII 圖、案號 .nb 不可折行所撐出者。
  丁 圖段行內完整：凡含框線字符（─│┌┐└┘═╔╚→←↑↓╳├┤）之 pre 源碼行，須整行落在
              印面同一條行內；散落兩行者＝折行，圖必散架。
  戊 鎖頁屬實：凡掛 class="keep" 之 pre／blockquote／table，其首尾須同在一頁。
用法：python _work/tblaudit.py            # 四式全檢
      python _work/tblaudit.py 列印版     # 只檢一式
"""
import io, os, re, sys
import html as H
import pymupdf as fitz

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PRINT = os.path.join(ROOT, '_print')
MIN_MARGIN = 24.0          # 影印版外側 10mm≈28.3pt，留 4pt 容誤差
BOX = u'─│┌┐┘├┤┴┼═║╔╗╚╝╠╣╬╭╮╰╯→←↑↓╳▶◀▼▲'
EDS = [
    ('列印版', 'final38.html', 'ver38四分律_起心動念心智分析框架_第三十八版_列印版.pdf'),
    ('螢幕版', 'final38_screen.html',
     'ver38四分律_起心動念心智分析框架_第三十八版_螢幕版.pdf'),
    ('精簡本', 'final38_精簡本.html',
     'ver38四分律_起心動念心智分析框架_第三十八版_列印版_精簡本.pdf'),
    ('精簡本螢幕', 'final38_精簡本_screen.html',
     'ver38四分律_起心動念心智分析框架_第三十八版_螢幕版_精簡本.pdf'),
]


def norm(s):
    s = H.unescape(re.sub(r'(?s)<[^>]+>', '', s))
    return re.sub(r'\s+', '', s)


def strip_keep_tags(block, tag):
    return re.findall(r'(?s)<%s[^>]*class="[^"]*keep[^"]*"[^>]*>(.*?)</%s>' % (tag, tag), block)


def axis_a(html):
    """甲軸：表欄數與表頭空欄。只讀 HTML，不需 PDF，故可單測（見 negtest_axisa.py）。"""
    bad_n, bad_h = [], []
    tbls = re.findall(r'(?s)<table[^>]*>.*?</table>', html)
    for ti, tb in enumerate(tbls):
        ths = re.findall(r'(?s)<th[^>]*>(.*?)</th>', tb)
        rows = re.findall(r'(?s)<tr[^>]*>(.*?)</tr>', tb)
        ncols = len(ths) if ths else None
        for hi, h in enumerate(ths):                      # 欄數齊不等於表頭齊：空表頭＝漏名
            if not H.unescape(re.sub(r'(?s)<[^>]+>', '', h)).strip():
                bad_h.append(u'表%02d 表頭第%d格空白' % (ti + 1, hi + 1))
        for ri, r in enumerate(rows):
            tds = re.findall(r'(?s)<td[^>]*>(.*?)</td>', r)
            if not tds:
                continue
            if ncols and len(tds) != ncols:
                bad_n.append(u'表%02d 第%d列 %d 欄≠表頭 %d 欄' % (ti + 1, ri + 1, len(tds), ncols))
    return tbls, bad_n, bad_h


def audit(ed, hp, pdf):
    html = io.open(hp, encoding='utf-8').read()
    doc = fitz.open(pdf)
    n = len(doc)
    lines = []                                   # 每頁之「行」清單（已去空白）
    for i in range(n):
        lines.append([re.sub(r'\s+', '', x) for x in doc[i].get_text().split('\n') if x.strip()])
    flat = [u''.join(l) for l in lines]
    # 全冊「一條印面行」之_sentinel_串：某源碼行若被折為兩行，必不存於此串
    big = u'\x00'.join(x for l in lines for x in l)
    rep = {k: [] for k in (u'甲欄數', u'甲表頭空格', u'乙散架', u'丙越界', u'丁折行', u'戊鎖頁')}

    # ── 甲：表欄數與表頭空欄（函式化以便單測）──
    tbls, rep[u'甲欄數'], rep[u'甲表頭空格'] = axis_a(html)

    # ── 乙：印面格線（沿用 tblgrid）──
    spec = os.path.join(HERE, 'tblgrid.py')
    import importlib.util
    sg = importlib.util.spec_from_file_location('tblgrid', spec)
    tg = importlib.util.module_from_spec(sg)
    sg.loader.exec_module(tg)
    _tot, bad, unkg, _ok, lost = tg.check(hp, pdf)
    for b in bad:
        rep[u'乙散架'].append(u'表%02d 頁 %d「%s」%s' % (b[0], b[2], b[3], b[4]))
    for b in lost:
        rep[u'乙散架'].append(u'表%02d「%s」缺 %d 格（疑整塊遭丟棄）' % (b[0], b[2], b[3]))

    # ── 丙：真越界（貼到物理邊界者才算破版；影印版鏡像邊距，最小邊距 10mm≈28.3pt）──
    #     註：Chromium 對過寬之表係**縮排而非溢出**，故「掛出欄外」之病必落於物理邊界內側
    #     以外方可見；逐頁百分比之法在目錄頁（兩欄式）與整頁縮排頁必誤報，不採。
    for i in range(n):
        w = doc[i].rect.width
        for word in doc[i].get_text('words'):
            if word[2] > w - MIN_MARGIN or word[0] < MIN_MARGIN - 6:
                rep[u'丙越界'].append(u'頁 %d x[%.1f,%.1f]（頁寬 %.1f）「%s」' % (
                    i + 1, word[0], word[2], w, word[4][:18]))
                break
    # ── 丙′：表欄寬之合理性（retune_tables 所配 colgroup）──
    for ti, tb in enumerate(tbls):
        cols = [float(x) for x in re.findall(r'<col style="width: ([0-9.]+)%"', tb)]
        if not cols:
            continue
        if sum(cols) > 100.6:
            rep[u'丙越界'].append(u'表%02d 欄寬和 %.1f%% >100%%' % (ti + 1, sum(cols)))
        narrow = [c for c in cols if c < 6.0]
        if narrow:
            rep[u'丙越界'].append(u'表%02d 有 %d 欄寬 <6%%（%s）→ 欄內一字一行' % (
                ti + 1, len(narrow), u'、'.join(u'%.1f%%' % c for c in narrow)))

    # ── 丁：ASCII 圖段折行（源碼行須整條落在某一印面行內）──
    pres = re.findall(r'(?s)<pre[^>]*>(.*?)</pre>', html)
    nfig = nmatch = 0
    for pi, body in enumerate(pres):
        txt = H.unescape(re.sub(r'(?s)<[^>]+>', '', body))
        src = [l for l in txt.split('\n') if l.strip()]
        fig = [l for l in src if any(c in BOX for c in l)]
        nfig += len(fig)
        for l in fig:
            s = re.sub(r'\s+', '', l)
            if not s:
                continue
            if s in big:
                nmatch += 1
            else:
                rep[u'丁折行'].append(u'圖%02d 段（%d 行）「%s」' % (pi + 1, len(fig), l.strip()[:34]))

    # ── 戊：keep 須同頁（頁之歸屬以全頁文字流判，容忍欄內折行）──
    def pgs(s):
        return [i for i, f in enumerate(flat) if s and s in f]

    for pi, body in enumerate(strip_keep_tags(html, 'pre')):
        txt = H.unescape(re.sub(r'(?s)<[^>]+>', '', body))
        src = [re.sub(r'\s+', '', l) for l in txt.split('\n') if l.strip()]
        if len(src) < 2:
            continue
        pg_h, pg_t = pgs(src[0]), pgs(src[-1])
        if pg_h and pg_t and not (set(pg_h) & set(pg_t)):
            rep[u'戊鎖頁'].append(u'pre.keep #%d 跨頁（首 %s／尾 %s）' % (
                pi + 1, [x + 1 for x in pg_h[:3]], [x + 1 for x in pg_t[:3]]))
    for qi, body in enumerate(strip_keep_tags(html, 'blockquote')):
        s = norm(body)
        if len(s) < 16:
            continue
        a, b = pgs(s[:14]), pgs(s[-14:])
        if a and b and not (set(a) & set(b)):
            rep[u'戊鎖頁'].append(u'blockquote.keep #%d 跨頁（首 %d／尾 %d）' % (qi + 1, a[0] + 1, b[0] + 1))
    for ti, tb in enumerate(re.findall(r'(?s)<table[^>]*class="[^"]*keep[^"]*"[^>]*>.*?</table>', html)):
        rows = re.findall(r'(?s)<tr[^>]*>(.*?)</tr>', tb)
        if len(rows) < 2:
            continue
        first = re.findall(r'(?s)<t[hd][^>]*>(.*?)</t[hd]>', rows[0])
        cells = re.findall(r'(?s)<td[^>]*>(.*?)</td>', rows[-1])
        if not first or not cells:
            continue
        f0, l0 = norm(first[0]), norm(cells[0])
        if len(f0) < 4 or len(l0) < 4:
            continue
        a, b = pgs(f0[:10]), pgs(l0[:10])
        if a and b and not (set(a) & set(b)):
            rep[u'戊鎖頁'].append(u'table.keep #%d 跨頁（表頭 %s／末列 %s）' % (
                ti + 1, [x + 1 for x in a[:3]], [x + 1 for x in b[:3]]))
    doc.close()
    return len(tbls), len(pres), (nfig, nmatch, len(unkg), len(bad) + len(lost)), rep


def main():
    want = sys.argv[1:]
    eds = [e for e in EDS if not want or e[0] in want or any(w in e[0] for w in want)]
    total = 0
    for ed, hf, pf in eds:
        hp, pdf = os.path.join(PRINT, hf), os.path.join(PRINT, pf)
        if not (os.path.isfile(hp) and os.path.isfile(pdf)):
            print(u'%s 檔不齊，跳過' % ed)
            continue
        ntbl, npre, figstat, rep = audit(ed, hp, pdf)
        cnt = sum(len(v) for v in rep.values())
        total += cnt
        print(u'【%s】表 %d 張、pre %d 段、圖行 %d 條（整行可核 %d）、格線待核 %d → 恙 %d 處' % (
            ed, ntbl, npre, figstat[0], figstat[1], figstat[2], cnt))
        for k, v in rep.items():                     # 軸名不另列名單：以 rep 之鍵為唯一法源
            print(u'   %s：%d' % (k, len(v)))
            for x in v[:8]:
                print(u'        %s' % x)
    print(u'==== 合計 %d 處 ====' % total)
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main())
