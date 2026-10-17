"""第 165 輪探針二：非正黑體之替補字形與極小字落點。

用法：python _work/r165font2.py [pdf]
"""
import sys, re, collections
import pymupdf as fitz

CJK = re.compile(r'[一-鿿㐀-䶿]')
MAIN = ('MicrosoftJhengHeiRegular', 'MicrosoftJhengHeiBold')

def main():
    pdf = sys.argv[1] if len(sys.argv) > 1 else r'_print/ver38_列印版.pdf'
    doc = fitz.open(pdf)
    alt = collections.Counter()          # font -> chars
    altc = {}                            # font -> [(page, codepoints, text)]
    tiny = collections.defaultdict(list)  # size -> [(page, text)]
    scale = collections.Counter()        # page size in pt
    for pno in range(doc.page_count):
        pg = doc.load_page(pno)
        scale[(round(pg.rect.width, 1), round(pg.rect.height, 1))] += 1
        for b in pg.get_text('dict').get('blocks', []):
            if b.get('type') != 0:
                continue
            for l in b.get('lines', []):
                for s in l.get('spans', []):
                    t = s.get('text', '').strip()
                    if not t:
                        continue
                    fn, sz = s['font'], round(s['size'], 1)
                    if fn not in MAIN:
                        alt[fn] += len(t)
                        altc.setdefault(fn, []).append((pno + 1, sz, t))
                    if sz < 9.6:
                        tiny[sz].append((pno + 1, t))
    doc.close()
    print('== %s ==' % pdf)
    print('紙面：%s' % list(scale.items()))
    print('\n-- 非正黑體之替補字型 --')
    for fn, c in alt.most_common():
        rows = altc[fn]
        cps = collections.Counter()
        for _, _, t in rows:
            for ch in t:
                if ch.strip():
                    cps[ch] += 1
        print('\n%-28s %5d 字，見 %d 頁' % (fn, c, len(set(p for p, _, _ in rows))))
        print('   字符集：%s' % ''.join(sorted(cps, key=ord))[:180])
        for p, sz, t in rows[:6]:
            print('   p%-4d %4.1fpt  %s' % (p, sz, t[:56]))
    print('\n-- 小字（< 9.6pt）--')
    for sz in sorted(tiny):
        rows = tiny[sz]
        pgs = sorted(set(p for p, _ in rows))
        print('\n  %.1f pt：%d 行、%d 字，頁 %s' % (sz, len(rows), sum(len(t) for _, t in rows), pgs[:14]))
        for p, t in rows[:4]:
            print('     p%-4d %s' % (p, t[:64]))

main()
