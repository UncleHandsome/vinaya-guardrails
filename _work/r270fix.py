# -*- coding: utf-8 -*-
"""270 輪・刀：凡例第六節之**不可驗約**改為可守之形（269 自己種下，本輪自查自除）。

量得（`_work/r270probe.py`・`_work/r270narrow.py`）：
  『凡用之處須自註分界』——前七章以『證據能力／管轄／迴避』為骨之節 **31 段，22 段無註**；
  收窄口徑（改取實定法專名）仍得 41 段，而偽陽過半（『警』中於『警策』・『判決』中於『佛判』）
  ⇒ **無可分別之口徑**（與 267『幽靈名與描述語同形』同科）。
另量『例示之詞須見於冊』一軸：可判 129 項而 47 項唯此一見——逐條覆核俱是比喻句與引文內語
  （『如市井頑童般』・『如來主幹垂問』・『作如是言』），**此軸天生不可立尺**，記而不立。
實態之最 crisp 者：『詳見第八章』之自註全冊 5 見，去凡例自引 1，**餘四見俱在第四章**。
治：**約不可驗即改約**（不是假裝守得到，也不是硬補二十二段重複自註）。
用法：python -X utf8 _work/r270fix.py [apply]
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')

PAIRS = [
    (u'此屬功能對位而非移植法條，**凡用之處須自註分界**——第四章第三節之末即立此例：'
     u'『屬證據能力之會通；其道場層面之調查標準作業與數位資產治理，詳見第八章第二節與第四節』。'
     u'兩者界限分明，互不相犯。',
     u'此屬功能對位而非移植法條。**此類語彙乃全書公堂喻之骨架，不逐處標記**；'
     u'讀者欲辨其界，只消記一句：**凡涉世俗實定法之具體制度（法條、時效、報告之義務、管轄之歸屬），'
     u'其本域在第八章**。冊中遇其樞紐處自註分界，今有『詳見第八章』之自註四見，**俱在第四章**'
     u'（第三節之末云：『屬證據能力之會通；其道場層面之調查標準作業與數位資產治理，'
     u'詳見第八章第二節與第四節』），遇此類處皆作如是觀。兩者界限分明，互不相犯。'),
]

t = io.open(BOOK, encoding=u'utf-8-sig').read()
bad = [(o[:40], t.count(o)) for o, _n in PAIRS if t.count(o) != 1] + \
      [(u'新文已在：' + n[:34], t.count(n)) for _o, n in PAIRS if t.count(n)]
print(u'合 %d 項・錨不合 %d' % (len(PAIRS), len(bad)))
for x in bad:
    print(u'   命中 %d｜%s' % (x[1], x[0]))
if bad:
    sys.exit(2)
if u'apply' not in sys.argv:
    for o, n in PAIRS:
        print(u'  舊：%s\n  新：%s' % (o[:80], n[:80]))
    print(u'乾跑，未寫入。')
    sys.exit(0)
for o, n in PAIRS:
    t = t.replace(o, n, 1)
io.open(BOOK, 'w', encoding=u'utf-8', newline=u'').write(t)
chk = io.open(BOOK, encoding=u'utf-8-sig').read()
for o, n in PAIRS:
    assert chk.count(n) == 1 and chk.count(o) == n.count(o), o[:30]
print(u'已寫入 %d 項，回讀相符。今『凡用之處須自註分界』%d 見（須 0）・『詳見第八章』%d 見。'
      % (len(PAIRS), chk.count(u'凡用之處須自註分界'), chk.count(u'詳見第八章')))
