# -*- coding: utf-8 -*-
# 記錄檔之簡形自掃（第 174 輪立，每輪收尾一跑；待診非閘，報而不挡）
#   主檔之簡形有不變量『引號外無簡體孤立字』守之，而四份長命記錄（SOP・日誌・規画・刪除登記）
#   向無尺——歷輪自查之簡形誤落俱由目測逮得，今歸此器。
#   口徑與主檔同：**引號（「」『』）之內不較**（彼乃如實登載舊形，如『一类』→『一類』之例示）。
#   `_tk.py` 不掃——其 SIMP_ONLY 名單本身即集簡字以校主檔，掃之必滿屏。
#   『诸』一枚第 226 輪補：主檔底冊校勘記落『诸語料頻次』（在『』之內，故主檔之簡形閘向不較，
#   而此器與 `_tk.SIMP_ONLY` 兩名單俱無此字——『名單之外』之又一例，第 61／174／216 輪之教）。
import glob
import io, sys

import _simpmap as _SM          # 簡形↔繁體對照今在 `_simpmap.py`（第 238 輪歸一，勿再各抄一份）
S, T, MAP = _SM.S, _SM.T, _SM.MAP

FILES = ([u'列印SOP.md', u'文意梳理規劃.md', u'_archive/編年工程日誌.md']
         + sorted(glob.glob(u'_archive/DELETED-*.txt')))   # 登記檔逐日另檔，硬寫一日即漏此後諸檔（204 輪察）
# 軸檔之註解不掃：`_work/*.py` 多屬一輪之暫存（旋造旋棄），今制掃之得 874 處全在棄檔——
#   滿屏之噪即無器，故唯校四份長命記錄。
APPLY = len(sys.argv) > 1 and sys.argv[1] == u'apply'
seen, bad = set(), 0
for f in FILES:
    if f in seen:
        continue
    seen.add(f)
    txt = io.open(f, encoding='utf-8').read()
    mask, depth = [], 0
    for ch in txt:
        mask.append(depth == 0)
        if ch in u'「『':
            depth += 1
        elif ch in u'」』' and depth:
            depth -= 1
    hits = [i for i, c in enumerate(txt) if mask[i] and c in MAP]
    if u'DELETED-' in f:
        # 刪除登記檔之『甲→乙』例示行乃如實登載舊形（與引號之內同一口徑，第 175 輪『族內各有其制』）——不較
        spans, st = [], 0
        for ln in txt.split(u'\n'):
            en = st + len(ln) + 1
            if u'→' in ln:
                spans.append((st, en))
            st = en
        hits = [i for i in hits if not any(a <= i < b for a, b in spans)]
    if not hits:
        continue
    bad += len(hits)
    print(u'%s｜%d 處' % (f, len(hits)))
    for i in hits:
        print(u'   L%-5d %s←%s→%s' % (txt.count(u'\n', 0, i) + 1, txt[i],
              txt[max(0, i - 14):i].replace(u'\n', u'⏎'),
              txt[i + 1:i + 15].replace(u'\n', u'⏎')))
    if APPLY:
        lst = list(txt)
        for i in hits:
            lst[i] = MAP[txt[i]]
        io.open(f, 'w', encoding='utf-8', newline=u'\n').write(u''.join(lst))
print(u'合計 %d 處%s' % (bad, u'（已改）' if APPLY else u'（僅報；改須加 apply）'))
