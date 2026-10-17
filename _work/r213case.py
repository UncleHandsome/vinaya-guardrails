# -*- coding: utf-8 -*-
"""r213case.py —— 案號各族之『連貫無缺號』軸（第 213 輪立・第 43 軸・**升閘**：缺號即退 1）。

緣起：全書案例以〔遮N〕〔開N〕〔僧N〕〔遺N〕四族編號，歷輪諸器所校者乃**所指之真**（`caseref` 校編號與案名
兩式之所指、`qindex` 校問↔表之對合、`domchk` 校欄歸屬），而**族內之號自 1 至 N 是否無缺**一維向無器——
刪一條目或改一個號即留空穴，讀者依號求案而不得，其害同於『款序跳號』（`h4seq` 已守）而無一器問此族。

口径：
 ① 印面為界（擯底冊四篇與圍欄）——底冊之舉例與編年不入制；
 ② 取〔X N〕之形，X 限 1–2 漢字且屬計量族（遮／開／僧／遺／墮／補／界／變／難／提／捨／殘／例）；
 ③ **唯族內號數 ≥10 方校其連貫**（小族多屬臨時對舉，缺號非病）；
 ④ 缺號＝自該族最小號至最大號之間未見者；**甲目非零即退 1**。
退出碼：**甲 > 0 即退 1**（升閘）。`argv[1]` 給副本路徑即改掃副本（負測之法，底冊界按副本自算）。
用法：`PYTHONPATH=. PYTHONIOENCODING=utf-8 python -X utf8 _work/r213case.py`
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as t

FAMS = u'遮開僧遺墮補界變難提捨殘例'
PAT = re.compile(u'〔([%s]{1,2})\\s*(\\d{1,3})(?:\\s*之\\d+|\\s*、\\d+)*〕' % FAMS)
MIN = 10
COP = sys.argv[1] if len(sys.argv) > 1 else None

if COP:
    L = io.open(COP, encoding=u'utf-8').read().split(u'\n')
    b0 = next((i for i, l in enumerate(L)
               if l.startswith(u'# ') and any(n in l for n in t.BOTTOM_NAMES)), len(L))
    BOT = set(range(b0, len(L)))
    print(u'（掃副本 %s｜底冊自 L%d 起）' % (COP, b0 + 1))
else:
    L = t.LINES
    BOT = set(t.bottom_lines())

fen = [False] * len(L)
ins = False
for i, l in enumerate(L):
    if l.strip().startswith(u'```'):
        ins = not ins
        fen[i] = True
        continue
    fen[i] = ins

use = {}
for i, l in enumerate(L):
    if i in BOT or fen[i]:
        continue
    for m in PAT.finditer(l):
        use.setdefault(m.group(1), set()).add(int(m.group(2)))

gap = []
for fam in sorted(use):
    nums = sorted(use[fam])
    if len(nums) < MIN:
        print(u'   〔%sN〕%d 號（%d–%d）——小族，不校連貫' % (fam, len(nums), nums[0], nums[-1]))
        continue
    miss = [x for x in range(nums[0], nums[-1] + 1) if x not in use[fam]]
    print(u'   〔%sN〕%d 號（%d–%d）｜缺號 %s'
          % (fam, len(nums), nums[0], nums[-1], miss if miss else u'無'))
    gap += [(fam, x) for x in miss]
print(u'== 案號連貫：甲·缺號 %d 處 %s' % (len(gap), gap[:8]))
sys.exit(1 if gap else 0)
