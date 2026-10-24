# -*- coding: utf-8 -*-
"""第 253 輪：舊案號〔遮／開／僧 N〕→ 三十九版第六章新案號之候選對照（供逐條親裁）。

法：ver38 之舊卡（####〔遮N〕題＋內文）取「人名與事相關鍵詞」，再於 ver39 百則卡中
求其命中卡；命中者即候選。非一比一——舊號乃**法相分類**（一類可含ver39 數案），
故本表只出候選，不落刀；刀由人裁。

用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r253map.py
"""
import io
import os
import re
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V39 = io.open(os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md'),
              encoding=u'utf-8').read()
V38 = io.open(os.path.join(ROOT, u'ver38四分律_起心動念心智分析框架_修正版.md'),
              encoding=u'utf-8').read()

NAMES = [u'跋難陀', u'須提那', u'檀尼迦', u'闡陀', u'迦留陀夷', u'六群', u'難陀', u'蓮華色',
         u'阿那律', u'羅睺羅', u'舍利弗', u'目連', u'目犍連', u'大迦葉', u'阿難', u'賓頭盧',
         u'提婆達多', u'富羅那', u'優波離', u'娑伽陀', u'婆求', u'沓婆', u'慈地', u'蘇卑',
         u'耶舍', u'難遮', u'滿賢', u'波旬', u'拘睒彌', u'菩提王子', u'琉璃', u'給孤獨',
         u'祇陀', u'毘舍佉', u'波斯匿', u'頻婆娑羅', u'瓶沙', u'阿闍世', u'旃陀', u'喻頻那',
         u'摩訶男', u'那佉梨', u'血頂', u'刀箭', u'象力', u'大黑', u'烏'
         ]


def cards(txt, hpat):
    """回傳 [(號, 題, 內文)]，內文止於下一同級或更粗標題。"""
    ms = list(re.finditer(hpat, txt))
    out = []
    for i, m in enumerate(ms):
        lvl = len(m.group(1))
        body_end = len(txt)
        for m2 in ms[i + 1:]:
            if len(m2.group(1)) <= lvl:
                body_end = m2.start()
                break
        nxt = re.search(u'(?m)^#{1,%d} ' % lvl, txt[m.end():])
        if nxt:
            body_end = min(body_end, m.end() + nxt.start())
        out.append((m.group(2).strip(), m.group(3).strip(), txt[m.end():body_end]))
    return out


def norm(s):
    return re.sub(u'[^一-鿿]', u'', s)


old = cards(V38, u'(?m)^(#{4,5})\\s*〔((?:遮|開|僧|遺)\\d+)〕(.*)$')
new = cards(V39, u'(?m)^(#{3,4})\\s*〔(案例\\s*\\d+)〕(.*)$')
used = set(re.findall(u'〔(遮\\d+|開\\d+|僧\\d+|遺\\d+)〕', V39))
used = set(re.sub(u'\\s', u'', x) for x in used)
print(u'ver38 舊卡 %d 枚｜ver39 新卡 %d 枚｜三十九版書中引用之舊號 %d 個'
      % (len(old), len(new), len(used)))

newn = [(n, t, norm(b), b) for n, t, b in new]
rows = []
for n, t, b in old:
    key = re.sub(u'\\s', u'', n)
    if key not in used:
        continue
    nb = norm(b)
    hits = [x for x in NAMES if x in b]
    sc = []
    for nn2, tt2, ntb2, _rb in newn:
        s = 0
        for h in hits:
            if h in _rb:
                s += 3
        for g in range(0, max(1, len(nb) - 8), 4):        # 八字滑窗（跳步長，求速）
            seg = nb[g:g + 8]
            if len(seg) == 8 and seg in ntb2:
                s += 1
        if s:
            sc.append((s, nn2, tt2))
    sc.sort(reverse=True)
    rows.append((key, t[:26], hits[:4], sc[:3]))
rows.sort(key=lambda r: (r[0][0], int(r[0][1:])))
for key, t, hits, sc in rows:
    print(u'%-6s｜%-28s｜人%s' % (key, t, u','.join(hits) or u'—'))
    for s, nn2, tt2 in sc:
        print(u'        %-4d %s %s' % (s, nn2.replace(u' ', u''), tt2[:34]))
    if not sc:
        print(u'        （無候選——須人工斷）')
