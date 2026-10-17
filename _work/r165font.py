"""第 165 輪探針：印面之『字』——字号分佈、字型清單、極小字、缺字與異形。

用法：python _work/r165font.py [pdf] [--min 7.5]
      無參數則掃完整版列印 PDF。
"""
import sys, re, collections
import fitz

CJK = re.compile(r'[一-鿿㐀-䶿]')

def main():
    pdf = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else r'_print/ver38_列印版.pdf'
    args = sys.argv[2:]
    lo = 7.5
    for i, a in enumerate(args):
        if a == '--min':
            lo = float(args[i + 1])
    doc = fitz.open(pdf)
    sizes = collections.Counter()          # (round(size,1)) -> span count
    charsz = collections.Counter()         # size -> CJK char count（以字計，非以 span 計）
    fonts = collections.Counter()
    tiny = collections.Counter()           # page -> count of chars below lo
    fontsz = collections.Counter()         # (font, size bucket) -> chars
    repl = []
    for pno in range(doc.page_count):
        dd = doc.load_page(pno).get_text('dict')
        for b in dd.get('blocks', []):
            if b.get('type') != 0:
                continue
            for l in b.get('lines', []):
                for s in l.get('spans', []):
                    t = s.get('text', '')
                    if not t.strip():
                        continue
                    sz = round(s['size'], 1)
                    fn = s['font']
                    nc = len(CJK.findall(t))
                    sizes[sz] += 1
                    charsz[sz] += max(nc, len(t.strip()))
                    fonts[fn] += max(nc, 1)
                    fontsz[(fn, sz)] += nc
                    if sz < lo:
                        tiny[pno + 1] += max(nc, len(t.strip()))
                    if '\ufffd' in t or '□' in t or '𘚞' in t:
                        repl.append((pno + 1, t[:40]))
    doc.close()
    tot = sum(charsz.values())
    body = max(charsz, key=lambda k: charsz[k])
    print('== %s ==' % pdf)
    print('字量總計（以字計）：%d，主字号 %.1f pt 佔 %.1f%%' % (tot, body, 100.0 * charsz[body] / tot))
    print('\n-- 字号分佈（字數 ≥ 0.02%% 者）--')
    for sz in sorted(charsz):
        pc = 100.0 * charsz[sz] / tot
        if pc >= 0.02:
            print('  %6.1f pt  %8d 字  %5.2f%%' % (sz, charsz[sz], pc))
    print('\n-- 小字（< %.1f pt）--' % lo)
    if not tiny:
        print('  零見')
    else:
        for p, c in sorted(tiny.items(), key=lambda kv: -kv[1])[:25]:
            print('  p%-5d %d 字' % (p, c))
        print('  共 %d 頁、%d 字' % (len(tiny), sum(tiny.values())))
    print('\n-- 字型 --')
    for fn, c in fonts.most_common():
        print('  %-34s %8d' % (fn, c))
    print('\n-- 替補／缺字符號 --')
    print('  無' if not repl else '  %s' % repl[:20])
    print('\n-- 主字号之外之異形組合（字型×字号，字數 ≥ 300）--')
    for (fn, sz), c in sorted(fontsz.items(), key=lambda kv: -kv[1]):
        if sz != body and c >= 300:
            print('  %-30s %6.1f pt  %7d 字' % (fn, sz, c))

main()
