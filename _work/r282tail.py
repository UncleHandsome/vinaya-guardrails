# -*- coding: utf-8 -*-
"""282・補刀：案69 處斷欄之命題以『教令』收尾，觸第 26 目『印面命題不作行政令』之禁
   （律語雖非官文书之令，形制之尺不許破例）→ 改叢林原生之『學處』。"""
import hashlib
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
APPLY = u'--apply' in sys.argv
TXT = io.open(BOOK, encoding=u'utf-8-sig').read()
OLD = u'別制看門相之教令'
NEW = u'別制看門相之學處'
print(u'命中：%d 處' % TXT.count(OLD))
assert TXT.count(OLD) == 1, TXT.count(OLD)
out = TXT.replace(OLD, NEW, 1)
print(u'改後 %d 行－sha %s' % (len(out.split(u'\n')),
      hashlib.sha256(out.encode(u'utf-8')).hexdigest()[:12]))
if not APPLY:
    print(u'（乾跑・未落盤）')
    sys.exit(0)
io.open(BOOK, 'w', encoding=u'utf-8').write(out)
back = io.open(BOOK, encoding=u'utf-8-sig').read()
print(u'落盤訖・同=%s・sha %s' % (back == out, hashlib.sha256(back.encode(u'utf-8')).hexdigest()[:12]))
