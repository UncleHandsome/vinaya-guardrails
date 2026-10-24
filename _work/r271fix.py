# -*- coding: utf-8 -*-
"""271 輪・刀：刪一處**語料所無之篇名**《僧殘犍度》（本地《四分律》六十卷無此連綴，
   而四種治法羯磨之摩那埵確見於『竟覆藏犍度…知我行摩那埵覆藏犍度』）。

量（`_work/r271titles.py`・`_work/r271probe2.py`）：全書《X》35 形 229 見；含『犍度』者三形——
  《四分律·呵責犍度》（呵責犍度 語料 4 見 ✓）・《覆藏犍度》（2 見 ✓）・《僧殘犍度》（**0 見**）。
  另五筆『語料無此連綴』之報俱是口徑之偽缺：未剝『書名·』前綴（四分律·／中論·）與他典品名（本地不儲其檔），
  已如實記於尺身，不誤刀。
用法：python -X utf8 _work/r271fix.py [apply]
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
PAIRS = [
    (u'律典於《僧殘犍度》與《覆藏犍度》中，立四種治法羯磨為其總目',
     u'律典於《覆藏犍度》中，立四種治法羯磨為其總目'),
]
t = io.open(BOOK, encoding=u'utf-8-sig').read()
bad = [(o[:36], t.count(o)) for o, _n in PAIRS if t.count(o) != 1]
print(u'合 %d 項・錨不合 %d' % (len(PAIRS), len(bad)))
for x in bad:
    print(u'   命中 %d｜%s' % (x[1], x[0]))
if bad:
    sys.exit(2)
if u'apply' not in sys.argv:
    for o, n in PAIRS:
        print(u'  舊：%s\n  新：%s' % (o, n))
    print(u'乾跑，未寫入。')
    sys.exit(0)
for o, n in PAIRS:
    t = t.replace(o, n, 1)
io.open(BOOK, 'w', encoding=u'utf-8', newline=u'').write(t)
chk = io.open(BOOK, encoding=u'utf-8-sig').read()
for o, n in PAIRS:
    assert chk.count(n) == 1 and chk.count(o) == n.count(o), o[:24]
print(u'已寫入 %d 項・《僧殘犍度》今 %d 見（須 0）。' % (len(PAIRS), chk.count(u'《僧殘犍度》')))
