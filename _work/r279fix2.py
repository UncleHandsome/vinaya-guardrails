# -*- coding: utf-8 -*-
"""279 補・第一刀：第一章第四節『二諦四疆』之末，補一句數位表業管轄之指針。
   措辭全取本書現文（自『未經親臨…遙舉』該行構造），免構碼位之誤；所據即第四章第一節既存條文。"""
import hashlib
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
BAK = os.path.join(ROOT, u'_work', u'ver39.pre279b.md')
APPLY = u'--apply' in sys.argv
TXT = io.open(BOOK, encoding=u'utf-8-sig').read()
LINES = TXT.split(u'\n')


def sha(x):
    return hashlib.sha256(x.encode(u'utf-8')).hexdigest()[:12]


print(u'正本 %d 行・sha %s' % (len(LINES), sha(TXT)))

LN = 772
assert u'身口表業為限' in LINES[LN - 1], LINES[LN - 1][:60]
assert not LINES[LN - 1].rstrip().endswith(u'節。'), u'已落刀，勿重敷'

SI = next(k for k, l in enumerate(LINES) if u'未經親臨' in l)
SRC = LINES[SI]
bold = re.findall(r'\*\*(.+?)\*\*', SRC)
m = re.search(u'未經親臨[^。]{0,10}', SRC)
assert bold and m, (bold, m)
print(u'取詞來源 L%d・『%s』『%s』' % (SI + 1, bold[0], m.group(0)))

ADD = (u'四疆之分，於數位空間尤須如是落實：' + bold[0] + u'、' + m.group(0) + u'——俱見第四章第一節。')
print(u'ADD＝%s（%d 字）' % (ADD, len(ADD)))
LINES[LN - 1] = LINES[LN - 1] + ADD
out = u'\n'.join(LINES)
print(u'改後 %d 行・sha %s' % (len(LINES), sha(out)))
if not APPLY:
    print(u'（乾跑・未落盤）')
    sys.exit(0)
if not os.path.exists(BAK):
    io.open(BAK, 'w', encoding=u'utf-8').write(TXT)
io.open(BOOK, 'w', encoding=u'utf-8').write(out)
back = io.open(BOOK, encoding=u'utf-8-sig').read()
print(u'落盤訖・%d 行・sha %s・同=%s' % (len(back.split(chr(10))), sha(back), back == out))
