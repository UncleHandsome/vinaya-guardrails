# -*- coding: utf-8 -*-
"""第 132 輪軸：梵巴轉寫之**字形分裂**（含變音符之詞由兩家以上字體拼成 → 印面字距參差）

教訓：第 127 輪我以『同家字距』量得中位 0.001、最大 0.157 字寬而退外部之議——**錯在把接縫跳過**，
    病正發生在接縫處（粗體拉丁由微軟正黑排、ā/ṃ/ñ 卻 fallback 至別家，其字框寬依 CJK 之advance，
    墨窄而格寬，故紙上見白隙而框位無隙）。今改量**機制**：一詞之字符若出於兩家以上字型，即報病。
    修法見 `build38.pali_span()`（整詞包 `<span class="pali">`，字型堆疊以 Times New Roman 領頭）。
"""
import sys

import pymupdf

PDF = sys.argv[1] if len(sys.argv) > 1 else u'_print/ver38四分律_起心動念心智分析框架_第三十八版_列印版.pdf'
DIAC = set(u'àáâãäåāăąǎǫèéêëēĕėęěìíîïīĭįıòóôõöøōŏőùúûüūŭůųǔũǔýÿñńņňŉŋ'
           u'çćĉčċđðłśŝšşŧžźżřěů'
           u'ṃṭḥṝśṣñ')
d = pymupdf.open(PDF)
nword = 0
bad = []
for pno in range(len(d)):
    for b in d[pno].get_text('rawdict')['blocks']:
        for l in b.get('lines', []):
            chars = [(c, s['font']) for s in l['spans'] for c in s['chars']]
            i = 0
            while i < len(chars):
                if chars[i][0]['c'] in DIAC:
                    lo = hi = i
                    while lo > 0 and (chars[lo - 1][0]['c'].isalpha() or chars[lo - 1][0]['c'] in DIAC):
                        lo -= 1
                    while hi < len(chars) - 1 and (chars[hi + 1][0]['c'].isalpha() or chars[hi + 1][0]['c'] in DIAC):
                        hi += 1
                    fam = sorted({f for _, f in chars[lo:hi + 1]})
                    word = u''.join(c['c'] for c, _ in chars[lo:hi + 1])
                    if len(word) >= 3:
                        nword += 1
                        if len(fam) > 1:
                            bad.append((pno + 1, word[:22], len(fam), u'+'.join(f[:14] for f in fam)))
                    i = hi + 1
                else:
                    i += 1
d.close()
print(u'含變音符之詞 %d｜字形分裂 %d 處' % (nword, len(bad)))
seen = set()
for p, w, n, f in bad:
    if w in seen:
        continue
    seen.add(w)
    print(u'  第%4d頁 %-22s %d 家｜%s' % (p, w, n, f))
print(u'==== 梵巴字形分裂：病 %d 處（去重後 %d 詞）====' % (len(bad), len(seen)))
sys.exit(1 if bad else 0)
