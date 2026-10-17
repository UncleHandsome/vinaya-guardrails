# -*- coding: utf-8 -*-
"""諸篇戒條之因緣摘證：按 gen_appendix 之條界取條，再回溯該條宣說之前之因緣段（起於最近之「爾時／時有」）。
   用途：補案前先量哪幾條真有故事、哪幾條律文但云「如上」「義如上」——勿憑印象虛構因緣。
   法源同於附錄（rules_of），故此處所見之條號即附錄所標之條號。
用法：python -X utf8 _work/niyuan.py [--篇 篇名] [號|起-迄]…｜寬度可加 --w 260
     篇名須為 gen_appendix.PLAN 之 stem（預設『一百七十八單提法』，即舊行為）。
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import gen_appendix as G  # noqa: E402  條界與取條之唯一法源

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
W = 200
if "--w" in sys.argv:
    W = int(sys.argv[sys.argv.index("--w") + 1])
STEM = u"一百七十八單提法"
if "--篇" in sys.argv:
    STEM = sys.argv[sys.argv.index(u"--篇") + 1]
    ARGS = [a for a in ARGS if a != STEM]
# 「尼三十捨墮法」之類：篇名兩部相同者（三十捨墮法）以部辨之，故先試全名，再退到「部＋名」
PLAN = None
for p in G.PLAN:
    if p[1] == STEM:
        PLAN = p
        break
if PLAN is None and STEM[0] in u"比尼":
    fam, stem = STEM[0], STEM[1:]
    cand = [p for p in G.PLAN if p[1] == stem and ((u"尼" in p[0]) == (fam == u"尼"))]
    assert len(cand) == 1, u"篇名不可定：%s｜候選 %d" % (STEM, len(cand))
    PLAN = cand[0]
assert PLAN, u"PLAN 無此篇：%s（須為 gen_appendix.PLAN 之 stem，或以『尼／比』前置辨部）" % STEM
_, stem, _title, cat, exp, tag = PLAN
s = G.corpus(tag)
rs = dict(G.rules_of(s, stem, cat, exp))
todo = ARGS or [u"1-%d" % exp]
print(u"篇＝%s｜檔＝%s｜戒本 %d 條｜別宣 %d 條" % (stem, tag, exp, len(rs)))
for arg in todo:
    a, _, b = arg.partition(u"-")
    for n in range(int(a), int(b or a) + 1):
        txt = rs.get(n)
        if not txt:
            continue
        j = s.find(txt)                  # 戒文乃自宣說句所截，必在全文現形
        if j < 0:
            print(u"%3d｜（戒文不可定址）" % n)
            continue
        seg = s[max(0, j - 1800):j]
        m = list(re.finditer(u"爾時|時有|後有", seg))
        head = (seg[m[-1].start():] if m else seg[-260:]).replace(u"\n", u"")
        print(u"%3d｜%s" % (n, head[:W]))
