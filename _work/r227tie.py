# -*- coding: utf-8 -*-
# r227tie　制辭式引文與其條次之全書配對唯一性（第 227 輪立，長駐・專軸）
#
#   所以立之：第三章閘門二第三款舊文『依《波逸提法》第五十四條……律文原句作「若比丘妄作異語惱他者波逸提」』——
#   第五十四條乃『不受諫』之次（第一章引其隨語，卷十六），『妄作異語惱他』在本書他處三處俱標**第十二條**（卷十二，
#   一戒二制）；一條原句掛兩種條次，讀者依條次求戒必得錯戒。歷二百餘輪無一器校『同一引文之條次須唯一』：
#   `r185orphan` 校引號串在語料之存在性（此串去標點後確可查得，故甲目無感）、`r216loc` 校語料行號、
#   `caseref` 校案號——條次與引文之配對，全無守者。
#
#   口徑：① 唯校**制辭式**之引號串（剝標點後 ≥10 漢字，且含 波羅夷／僧伽婆尸沙／偷蘭遮／波逸提／突吉羅 之一），
#      名目短標（『不受諫』『無根僧殘謗戒』）不較——彼乃本書歸名，非逐字宣稱（第 26 輪之界）；
#   ② 引號形「」與『』俱取（本書兩式並存，一刀切即漏其一）；③ 條次取同行之『第N條』，
#      一章之『第N條』屬他篇者以（篇名＋條次）連記（波羅提提舍尼法第三條 不與 波逸提第三條 相混）；
#   ④ 底冊不較（修訂誌與附錄乃轉述，非宣稱——218 輪之裁、226 輪之誡）；⑤ 圍欄內之圖不較（欄寬所縛，從圖不從文）。
#   升閘：同一制辭串掛兩條次即退 1。負測見 `_work/r227negtest.py`。
#   用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r227tie.py
from __future__ import unicode_literals
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as T

LINES = T.LINES
BOT = T.bottom_lines()
TITLES = re.compile(u'波羅夷|僧伽婆尸沙|偷蘭遮|波逸提|突吉羅')
Q = re.compile(u'[「『]([^」』]{6,80})[」』]')
N = re.compile(u'(第[一二三四五六七八九十]+條)')
PIN = re.compile(u'(波羅提提舍尼法|僧殘|波逸提法|眾法|滅法)')
PUN = re.compile(u'[，。、：；！？「」『』“”()（）\\s*·…]')

pairs = {}
for i, l in enumerate(LINES):
    if i in BOT:                     # 底冊乃轉述，非宣稱（218 輪之裁、226 輪之誡）
        continue
    if not N.findall(l):
        continue
    for q in Q.findall(l):
        core = PUN.sub(u'', q)
        if len(core) < 10 or not TITLES.search(core):
            continue
        sec = u'・'.join(PIN.findall(l))
        for n in N.findall(l):
            pairs.setdefault(core, {}).setdefault((sec, n), []).append(i + 1)

bad = []
for core, d in sorted(pairs.items()):
    if len(d) > 1:
        bad.append((core, d))

print(u'制辭式引文 %d 串｜條次衝突 %d 處%s' % (len(pairs), len(bad), u' []' if not bad else u''))
for core, d in bad[:8]:
    print(u'   『%s…』掛 %s' % (core[:18], u'｜'.join(
        u'%s%s（L%s）' % (s, n, u'、'.join(str(x) for x in ls[:4])) for (s, n), ls in d.items())))
sys.exit(1 if bad else 0)
