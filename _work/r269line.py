# -*- coding: utf-8 -*-
"""269 輪・帳四：凡例加行（9,338➔9,340）使行號全域位移 +2，本輪記錄所引之行號就地歸正，
   並補一誡：**記錄宜以語為錨，不以行為錨**（行號是易碎座標；221／242 輪之誡之再證）。
用法：python -X utf8 _work/r269line.py [apply]
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = {
    u'日誌': os.path.join(ROOT, u'_archive', u'編年工程日誌.md'),
    u'SOP': os.path.join(ROOT, u'列印SOP.md'),
}
FIX = [
    (u'日誌', u'自建分界自註（L2392）', u'自建分界自註（今 L2394）'),
    (u'日誌', u'並逕引 L2392 之原文為範例', u'並逕引該節末之原文為範例（今 L2394）'),
    (u'日誌', u'唯此一見**（L2347）', u'唯此一見**（第四章第三節，今 L2349）'),
    (u'日誌', u'**自犯四則**', u'**自犯五則**'),
    (u'日誌', u'④ 新凡例句先寫『全冊 103 見』',
     u'④ 新凡例句先寫『全冊 103 見』'),
    (u'SOP', u'自建分界自註（L2392）', u'自建分界自註（今 L2394）'),
]
t = {k: io.open(v, encoding=u'utf-8-sig').read() for k, v in FILES.items()}
bad = [(f, o[:34], t[f].count(o)) for f, o, _n in FIX if t[f].count(o) != 1]
print(u'合 %d 枚・錨不合 %d' % (len(FIX), len(bad)))
for x in bad:
    print(u'   %s｜命中 %d｜%s' % x)
if bad:
    sys.exit(2)
if u'apply' not in sys.argv:
    for f, o, n in FIX:
        print(u'  %-4s %s ➔ %s' % (f, o[:36], n[:36]))
    print(u'乾跑，未寫入。')
    sys.exit(0)
for f, o, n in FIX:
    t[f] = t[f].replace(o, n, 1)
ADD = (u'⑤ **記錄以行為錨，於行號位移時同聲失真**——本輪凡例加兩行（9,338➔9,340），'
       u'故帳中所引 L2347／L2392 俱須進位為 L2349／L2394（即本檔之自改）。'
       u'自今而後：**記錄宜以語為錨（引其句之起首數字），行號只作輔助**，'
       u'否則每一度印面增損都要追改一次（『手工帳必腐』之又一形）。')
i = t[u'日誌'].find(u'**終檢**：9,340 行')
if i < 0 or ADD[:6] in t[u'日誌']:
    print(u'!! 找不到終檢錨或已附入')
    sys.exit(2)
t[u'日誌'] = t[u'日誌'][:i] + ADD + t[u'日誌'][i:]
for f, p in FILES.items():
    io.open(p, 'w', encoding=u'utf-8', newline=u'').write(t[f])
back = {f: io.open(p, encoding=u'utf-8-sig').read() for f, p in FILES.items()}
nok = [(f, o[:26], back[f].count(o), n.count(o)) for f, o, n in FIX
       if not (back[f].count(n) == 1 and back[f].count(o) == n.count(o))]
print(u'已寫入 %d 枚＋一則之誡・回讀不符 %d' % (len(FIX), len(nok)))
for x in nok:
    print(u'   %s｜舊實 %d／期望 %d｜%s' % x)
print(u'今冊行數 %d・日誌含『L2347』%d・含『今 L2349』%d'
      % (len(io.open(os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md'),
                     encoding=u'utf-8-sig').read().split(u'\n')),
         back[u'日誌'].count(u'L2347'), back[u'日誌'].count(u'今 L2349')))
