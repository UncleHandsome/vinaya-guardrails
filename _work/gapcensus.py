# -*- coding: utf-8 -*-
"""未展開之帳：凡「有別宣戒文」而「書中指針為『－』」之號，逐篇列出戒文起句。
   口徑全取 gen_appendix（rules_of／book_hit／disp），勿另立第二套——它即是附錄之產生器。
用法：python -X utf8 _work/gapcensus.py [篇名关键字]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import gen_appendix as G  # noqa: E402  匯入即算好 rows／指針

KEY = sys.argv[1] if len(sys.argv) > 1 else u""
tot = 0
for bu, stem, title, cat, exp, rs in G.rows:
    fam = u"尼" if u"尼" in bu else u"比"
    if KEY and KEY not in stem + cat + fam:
        continue
    got = dict(rs)
    first = min(got) if got else 1
    gaps = []
    for n in range(1, exp + 1):
        txt = got.get(n)
        if not txt:
            continue                      # 無別宣者非「未展開」，乃律文合宣／共戒
        if G.book_hit(fam, cat, n, txt):
            continue
        gaps.append((n, txt))
    if not gaps:
        print(u"── %s｜%s：0（別宣 %d，俱有落點）" % (fam, stem, len(got)))
        continue
    tot += len(gaps)
    print(u"══ %s｜%s｜未展開 %d／別宣 %d（共戒段 1～%d）"
          % (fam, stem, len(gaps), len(got), first - 1))
    for n, txt in gaps:
        print(u"  %3d. %s" % (n, G.disp(txt)[:56]))
print(u"合計未展開：%d 號" % tot)
