# -*- coding: utf-8 -*-
"""`refnum` 之負測：植入假錯，驗尺須中——不中即尺盲。

用法：python -X utf8 _merge/refnum_negtest.py
由來：第三十七輪校驗器以裸序數查節，把「##### 三、大綱本懷」当成「第三節」，
      139 條死鏈只掛得 80 標，59 條靜靜無形。此測即為守那一刀。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import refnum as RN

BOOK = u"""# 第一部　因聚
# 第一章　總綱
### 第一節　真節
### 第二節　亦真
##### 三、列項非節
內文引第二章第三節為據。
# 第二章　別論
### 第一節　只有此節
引第一章第二節與第一章第七節。
# 第三章　空章
無節之章，卻有人引第三章第四節。
"""

fails = []
n_chk = [0]


def chk(name, got, want):
    n_chk[0] += 1
    print("%-34s %-6s 得 %s／須 %s" % (name, "中" if got == want else "錯", got, want))
    if got != want:
        fails.append(name)


chk("序數十→10", RN.cnum(u"十"), 10)
chk("序數十七→17（昔解為 107）", RN.cnum(u"十七"), 17)
chk("序數二十一→21", RN.cnum(u"二十一"), 21)
chk("序數不可解→0", RN.cnum(u"百"), 0)
chk("章界切得三章", sorted(RN.chapter_blocks(BOOK)), [1, 2, 3])

d = [(m.group(0), tg) for m, tg in RN.dead_refs(BOOK)]
chk("死鏈三條", len(d), 3)
chk("裸序數 H5 不得頂替「第三節」", u"第二章第三節" in [x[0] for x in d], True)
chk("他章之真節指針存活", u"第一章第二節" in [x[0] for x in d], False)
chk("章在而無任何節者亦死", u"第三章第四節" in [x[0] for x in d], True)

tagged, n = RN.tag_dead(BOOK)
chk("掛標數＝死鏈數", n, 3)
chk("標後即死鏈，殭標 0", tagged.count(RN.TAG), n)
chk("重掃即全數已掛", sum(1 for _, tg in RN.dead_refs(tagged) if tg), n)
chk("削標之後尺必察其未掛", sum(1 for _, tg in RN.dead_refs(
    tagged.replace(RN.TAG, u"")) if not tg), n)

print("\n判定：%s" % ("%d 目俱中" % n_chk[0] if not fails else "未中：%s" % "、".join(fails)))
sys.exit(1 if fails else 0)
