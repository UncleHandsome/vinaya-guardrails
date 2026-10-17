# -*- coding: utf-8 -*-
"""krefstrict.py —— 附錄K 台帳『已回指』之嚴口徑覆核（第 140 輪立；第 236 輪併入 `_tk.kref_check_rows` 為唯一法源）。

舊不變量之口徑：目標（精準定位欄）之『第X章第Y節』只要在全書任何一處出現，即算『已回指』——
此口徑近於恆真（各章各節無不被提及），故台帳可登記某落點指向他章，而該落點之內其實全無指針，
查核無聲（第 140 輪外路指出第四章第五節之『假回指』即其例）。
本軸改以**落點為牢**：目標之章·節須實見於該列『正文落點』所指之款（無款則節）範圍之內。
第 236 輪之两口徑修正（器病）：一、指針写作範圍式者（『第八章第二、三節』『第五章第二至四節』）
須展開為章·節之集合再取交集，不得以字面子串求之；二、目標欄尾掛之括註（『（道岔五）』之屬）不礙辨識。
今全書可校之列與查無指針之列俱由 `_tk.kref_check_rows()` 当场生成——本檔唯出清冊，不另立尺。
退出碼：查無指針者零列即退 0（嚴口徑已升為不變量 95，本檔為其 witness）；有則退 1 並列之。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as t

n, bad = t.kref_check_rows()
print(u'嚴口徑：可校 %d 列｜落點之內查無目標指針者 %d 列' % (n, len(bad)))
for ln, loc, tg in bad:
    print(u'  L%-6d %-18s → %s' % (ln, loc, tg))
sys.exit(0 if not bad else 1)
