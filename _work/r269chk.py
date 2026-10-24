# -*- coding: utf-8 -*-
"""269 輪・帳檢：刀後之七詞复查・新改行之可疑符號・冊態之數。"""
import hashlib
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
P = os.path.join(ROOT, NAME)
raw = open(P, 'rb').read()
B = raw.decode(u'utf-8-sig')
L = B.split(u'\n')
print(u'冊 %d 行・%d B・SHA %s' % (len(L), len(raw), hashlib.sha256(raw).hexdigest()[:12]))

LINES_TOUCHED = [401, 1457, 7871, 8009, 8020, 8022, 8230, 198, 2558, 2560, 7675, 7676, 7677,
                 7745, 800, 804, 805, 806, 807, 811, 813, 832, 833, 834, 8521, 8908, 340,
                 254, 255, 256, 257, 258, 259, 260, 261, 262, 296, 297, 298]
print(u'── 新改行之可疑符號（半形引號・反引號・簡形）──')
SIMPLE = set(u'该当强随旧总续证宽样号码乙丙甲')
for n in LINES_TOUCHED:
    if n > len(L):
        continue
    l = L[n - 1]
    odd = re.findall(u"[\"'`]", l)
    sim = [c for c in set(l) if c in SIMPLE]
    if odd or sim:
        print(u'  L%-5d 符%r 簡%r｜%s' % (n, odd[:4], sim[:4], l.strip()[:66]))

print(u'── 刀後七詞＋報告所列之制 ──')
for w in [u'解耦', u'模組', u'甲級', u'乙級', u'丙級', u'存檔卡', u'甲乙丙', u'分流碼',
          u'一式三份', u'三級判準', u'括號之四制', u'〔案例·', u'Ultimate Beneficial']:
    print(u'  %-12s %d' % (w, B.count(w)))
print(u'── 今冊之新名（分立／三層／對治功能／僧事日誌）──')
for w in [u'雙軌分立', u'實體閘門層', u'母法總綱層', u'舉報自察層', u'對治功能', u'僧事日誌',
          u'前三層', u'四大範疇']:
    print(u'  %-12s %d 見' % (w, B.count(w)))
print(u'── 〔…〕標籤之實數（候裁之量）──')
pat = re.compile(u'〔([^〕]{1,24})〕')
tags = [m.group(1).strip() for m in pat.finditer(B) if not re.match(u'^(案例|補遺|[0-9]{2})', m.group(1).strip())]
print(u'  非編號之〔…〕：%d 見・%d 種' % (len(tags), len(set(tags))))
