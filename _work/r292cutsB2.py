# -*- coding: utf-8 -*-
"""292・乙組補刀（共器放寬・對照節之名冊形制歸穩）。

一・_casedef 之 CASE_ROW_RE／CASE_H_RE 今容『〔案例 NN〕（支名）』——此形乃全書舊有之家法
   （第七章清淨軌名單早已用『〔案例05〕（慈心支）』），非本輪新造；放寬共器，諸尺自癒。
二・附錄四〔新舊次碼對照〕三行之『（N 案）』與第十尺之名冊同形（彼校區內〔案例 NN〕之實收），
   此節本不列案例指針，故改作『N 條』；57 之重複舊次兼併一枚。
改他檔只以唯一錨點逐條替換；改畢即以 ast 與相鄰語句之存在自校。
"""
import ast
import hashlib
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, u'_work')
APPLY = u'--apply' in sys.argv
LOG = []
LB = chr(0xFF08)                     # （
RB = chr(0xFF09)                     # ）
TAILPAT = u'(?:%s[^%s]{1,14}%s)?' % (LB, RB, RB)


def patch_cd(old, new, label):
    s = io.open(CD, encoding='utf-8').read()
    assert s.count(old) == 1, u'%s：錨命中 %d 枚（須 1）' % (label, s.count(old))
    s2 = s.replace(old, new)
    ast.parse(s2)
    for keep in (u'CASE_CARD_RE', u'CASE_LANE_RE', u'CASE_ITEM_RE',
                 u'def case_defs', u'def verb_blocks', u'def src_blocks'):
        assert keep in s2, u'%s：相鄰語句走失 %s' % (label, keep)
    LOG.append(u'%s｜插入之形＝%s' % (label, new))
    if APPLY:
        io.open(CD, 'w', encoding='utf-8', newline='\n').write(s2)


CD = os.path.join(WORK, u'_casedef.py')
patch_cd(u"〕\\*\\*<br", u'〕' + TAILPAT + u"\\*\\*<br", u'共器・CASE_ROW_RE 容支名')
patch_cd(u"〕\\s*([^（(：:]", u'〕\\s*' + TAILPAT + u"\\s*([^（(：:]", u'共器・CASE_H_RE 容支名')

SRC = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
RAW = io.open(SRC, 'rb').read()
SHA0 = hashlib.sha256(RAW.replace(b'\r\n', b'\n')).hexdigest()[:12]
T = RAW.decode('utf-8').replace(u'\r\n', u'\n')
L = T.split(u'\n')
NUM = re.compile(u'^(\\d+) 案）')
for lab in (u'遮罪', u'僧殘', u'開許'):
    pfx = u'* **%s舊次%s' % (lab, LB)
    hit = [k for k, x in enumerate(L) if x.startswith(pfx)]
    assert len(hit) == 1, u'%s 行首錨命中 %d 枚' % (lab, len(hit))
    i = hit[0]
    rest = L[i][len(pfx):]
    m = NUM.match(rest)
    assert m, u'%s 行數形不合：%s' % (lab, rest[:12])
    tail = rest[m.end():]
    L[i] = u'* **%s舊次 %s 條%s' % (lab, m.group(1), tail)
    LOG.append(u'L%-5d 對照節・%s舊次 %s 枚（%s 條）' % (i + 1, lab, m.group(1), m.group(1)))
j = [k for k, x in enumerate(L) if u'57↔遮28・遮28' + LB in x]
assert len(j) == 1, u'57 重碼錨命中 %d 枚' % len(j)
L[j[0]] = L[j[0]].replace(u'57↔遮28・遮28' + LB, u'57↔遮28' + LB)
LOG.append(u'L%-5d 57 之重複舊次兼併一枚' % (j[0] + 1))
OUT = u'\n'.join(L)
print(u'行數 %d ➔ %d' % (len(L), len(L)))
for x in LOG:
    print(u'  ' + x)
if APPLY:
    B = OUT.replace(u'\n', u'\r\n').encode('utf-8')
    io.open(SRC, 'wb').write(B)
    print(u'冊寫畢：%dB｜CRLF %d｜bareCR %d｜sha %s ➔ %s' % (
        len(B), B.count(b'\r\n'), B.count(b'\r') - B.count(b'\r\n'), SHA0,
        hashlib.sha256(OUT.encode('utf-8')).hexdigest()[:12]))
else:
    print(u'（乾跑・未寫檔。）')
