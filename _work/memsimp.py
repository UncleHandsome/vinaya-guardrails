# -*- coding: utf-8 -*-
# 記憶檔之簡形自掃（記憶在同步盤外，recordsimp 不及——另立此器，口徑同：引號內不較）。
import glob, io, os, sys

import re as _re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = _re.sub(u'[^0-9A-Za-z]', u'-', ROOT)
DIRS = [os.path.expanduser(u'~/.qoder/memory'),
        os.path.expanduser(u'~/.qoder/projects/%s/memory' % SLUG)]
import _simpmap as _SM          # 簡形↔繁體對照今在 `_simpmap.py`（第 238 輪歸一，勿再各抄一份）
S, T, MAP = _SM.S, _SM.T, _SM.MAP
APPLY = len(sys.argv) > 1 and sys.argv[1] == u'apply'

tot = 0
for d in DIRS:
    for f in sorted(glob.glob(os.path.join(os.path.expanduser(d), u'*.md'))):
        txt = io.open(f, encoding='utf-8').read()
        mask, depth = [], 0
        for ch in txt:
            mask.append(depth == 0)
            if ch in u'「『':
                depth += 1
            elif ch in u'」』' and depth:
                depth -= 1
        hits = [i for i, c in enumerate(txt) if mask[i] and c in MAP]
        if not hits:
            continue
        tot += len(hits)
        print(u'%s｜%d 處' % (os.path.basename(f), len(hits)))
        for i in hits:
            print(u'   %s←%s→%s' % (txt[i], txt[max(0, i - 16):i].replace(u'\n', u'⏎'),
                                    txt[i + 1:i + 15].replace(u'\n', u'⏎')))
        if APPLY:
            lst = list(txt)
            for i in hits:
                lst[i] = MAP[txt[i]]
            io.open(f, 'w', encoding='utf-8', newline=u'\n').write(u''.join(lst))
print(u'合計 %d 處%s' % (tot, u'（已改）' if APPLY else u'（僅報）'))
