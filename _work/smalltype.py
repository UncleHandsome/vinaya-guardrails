# -*- coding: utf-8 -*-
"""smalltype.py —— 交付冊印面『實測字級』之下限檢（第 249 輪立）。

緣起：第 248 輪一刀在第八章公堂審計表之 ``` 圍欄內加了 43 個漢字，遂令該行成為全塊最寬行；
`build38.fit_pre_blocks()` 依最寬行等比縮字，整張手填表遂由 11pt 跌到 6.46pt——源層諸閘全綠，
紙上卻小如蟻行。圍欄之病不在字数而在塊寬，非量產物不可知，故立此器。

口徑：掃四式 PDF 每一 span 之 size；凡低於 FLOOR 者記其頁與文，退出碼非零。
FLOOR 取 8.1pt，與 `build38.MMD_FLOOR`（圖形之路之同一下限）同尺，不另立第二制。
今日之實測基線：全冊最小 8.99pt（圍欄圖），頁碼 9.40pt，目錄條目 8.4～8.9pt 一族已於第 165 輪消盡。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/smalltype.py [FLOOR]
"""
import io, os, sys
import pymupdf as fitz

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, u'_print')
BOOKS = [(u'完整·影印', u'ver38_列印版.pdf'), (u'完整·螢幕', u'ver38_列印版_screen.pdf'),
         (u'精簡·影印', u'ver38_列印版_精簡本.pdf'), (u'精簡·螢幕', u'ver38_列印版_精簡本_screen.pdf')]
FLOOR = float(sys.argv[1]) if len(sys.argv) > 1 else 8.1
bad = 0
for tag, fn in BOOKS:
    d = fitz.open(os.path.join(P, fn))
    worst, wpage, wtext, n = 99.0, 0, u'', 0
    for i, pg in enumerate(d, 1):
        for b in pg.get_text('dict')['blocks']:
            for l in b.get('lines', []):
                for s in l['spans']:
                    z = round(s['size'], 2)
                    if not s['text'].strip():
                        continue
                    if z < worst:
                        worst, wpage, wtext = z, i, s['text'].strip()[:22]
                    if z < FLOOR:
                        n += 1
    d.close()
    bad += 1 if n else 0
    print(u'%-9s 最小 %.2fpt（p%d『%s』）｜低於 %.1fpt 之 span %d 格%s'
          % (tag, worst, wpage, wtext, FLOOR, n, u'' if not n else u'　★'))
print(u'==== 印面實測字級下限檢（FLOOR=%.1fpt）：不合格 %d 冊 ====' % (FLOOR, bad))
sys.exit(1 if bad else 0)
