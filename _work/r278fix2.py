# -*- coding: utf-8 -*-
"""278・收口第二刀：第七章審計表之代碼式 0 號索引＋結語三處尾部金句撞車（易喻・不動終卷）。"""
import hashlib
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
BAK = os.path.join(ROOT, u'_work', u'ver39.pre278b.md')
APPLY = u'--apply' in sys.argv

TXT = io.open(BOOK, encoding=u'utf-8-sig').read()
LINES = TXT.split(u'\n')


def sha(s):
    return hashlib.sha256(s.encode(u'utf-8')).hexdigest()[:12]


print(u'正本 %d 行・sha %s' % (len(LINES), sha(TXT)))

CUTS = [
    (6529, u'**0. 公訴排除**', u'**【前置排除】公訴重罪檢核**', u'甲・審計表 0 號索引'),
    (7145, u'健康的身體，感覺不到內臟的存在；', u'調好的琴，不覺弦之緩急；', u'乙・結語三句之首'),
    (7181, u'**一年用不上一次本框架的僧團，才是佛陀最放心的僧團。**',
            u'**最會開庭的僧團，未必是最和合的僧團。**', u'丙・結語之收語'),
    (7194, u'〔心法〕健康的身體感覺不到內臟的存在，無事的僧團不需要日日開庭。',
            u'〔心法〕身安不覺息之出入，僧和不須日對公堂。', u'丁・三印卡心法行'),
]

for ln, old, new, tag in CUTS:
    assert LINES[ln - 1].count(old) == 1, u'%s｜錨非恰一（L%d）：%s' % (tag, ln, LINES[ln - 1][:70])
    LINES[ln - 1] = LINES[ln - 1].replace(old, new)
    print(u'%s｜L%-5d ➔ %s' % (tag[:1], ln, new[:34]))

out = u'\n'.join(LINES)
for phrase in [u'0. 公訴排除']:
    assert phrase not in out, u'%s 猶在冊' % phrase
print(u'改後 %d 行・sha %s' % (len(LINES), sha(out)))
if not APPLY:
    print(u'（乾跑・未落盤）')
    sys.exit(0)
if not os.path.exists(BAK):
    io.open(BAK, 'w', encoding=u'utf-8').write(TXT)
io.open(BOOK, 'w', encoding=u'utf-8').write(out)
back = io.open(BOOK, encoding=u'utf-8-sig').read()
print(u'落盤訖・讀回 %d 行・sha %s・同 out=%s' % (len(back.split(chr(10))), sha(back), back == out))
