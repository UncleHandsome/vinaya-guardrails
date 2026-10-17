"""第 165 輪探針三：指定頁之指定字符，截其周邊高倍圖以便親目。

用法：python _work/r165shot.py 頁:字串 [頁:字串 ...]
"""
import sys, re
import pymupdf as fitz

PDF = r'_print/ver38_列印版.pdf'
CJK = re.compile(r'[一-鿿]')

def main():
    doc = fitz.open(PDF)
    for spec in sys.argv[1:]:
        pno, needle = spec.split(':', 1)
        pg = doc.load_page(int(pno) - 1)
        hits = pg.search_for(needle)
        if not hits:
            print('%s：查無' % spec)
            continue
        r = hits[0]
        clip = fitz.Rect(max(0, r.x0 - 130), max(0, r.y0 - 46),
                         min(pg.rect.x1, r.x1 + 300), min(pg.rect.y1, r.y1 + 46))
        out = r'_work/r165_%sp%s.png' % (needle[:3].replace('/', '-'), pno)
        pix = pg.get_pixmap(matrix=fitz.Matrix(4.2, 4.2), clip=clip)
        pix.save(out)
        print('%s → %s（%dx%d，命中 %d 處）' % (spec, out, pix.width, pix.height, len(hits)))
    doc.close()

main()
