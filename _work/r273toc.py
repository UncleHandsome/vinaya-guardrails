# -*- coding: utf-8 -*-
"""273 輪・印面之量①：目錄 221 條 對 內嵌大綱 212 條——九條之差不由『未定位』，由**同名重出**。

`build_outline` 於 `disp in seen` 時**靜默跳過**（不計入 miss），故『定位失敗未入者 0』與『大綱少九條』
可以同時為真——**此即『自驗之數不.cover 跳過之數』**：宣稱只敘其判式之所判，未敘其未判。
本器只量，不改：列出全書目錄條中**同名重出**者及其層級與源行，供裁『是否須如實加別（續／上・下／之幾）』。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r273toc.py
"""
import collections
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, '_print'))
import build39 as B

src = B.read_source()
hs0 = B.collect_all_headings(src)
lines = B.drop_appendices(B.drop_blocks(src, hs0), hs0)
lines = B.strip_ch6_yuandian(lines, B.collect_all_headings(lines))
lines = B.apply_slim_markers(lines)
lines = B.apply_slim_cuts(lines, B.collect_all_headings(lines))
lines = B.ensure_blank(lines)
hs = B.collect_headings(lines)
entries = B.prepare_toc_entries(hs)
kept = [(lv, dp, ky) for (lv, dp, ky) in entries if dp != u'\u76ee\u5f55' and not B.skip_in_toc(lv, dp)]
print(u'\u76ee\u9304\u689d\uff1a\u5168\u9ad4 %d \u30fb\u5217\u5167\u5370\u51fa %d \u30fb\u5927\u7d17\u53ef\u5165\uff08\u53bb\u91cd\uff09%d' % (
    len(entries), len(kept), len({dp for _l, dp, _k in kept})))
cnt = collections.Counter(dp for _l, dp, _k in kept)
dups = {t: c for t, c in cnt.items() if c > 1}
print(u'\u540c\u540d\u91cd\u51fa\uff1a%d \u7a2e\uff0c\u5171\u6d6a\u8cbb %d \u689d\u5927\u7d17\u4e4b\u4f4d' % (
    len(dups), sum(c - 1 for c in dups.values())))
for t in sorted(dups, key=lambda x: (-dups[x], x)):
    where = [(lv, ky) for (lv, _d, ky) in kept if _d == t]
    print(u'  %d \u898b\u3000%s\u3000\u5c64\u7d1a %s' % (dups[t], t[:52], sorted({lv for lv, _k in where})))
    for lv, ky in where:
        print(u'        \u932f %s' % (str(ky)[:44],))
