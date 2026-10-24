# -*- coding: utf-8 -*-
"""275 輪・記憶檔簡形之逐枚點名（**不構碼位，只報索引**）：供 r275memfix2 按索引择治。

判式同 `memsimp`（引號內不較），但另標一欄『疑為供狀』：其前後十字之內若見列舉之形（『X・Y・Z』
或『X／Y／Z』且同類相連），即標『？』——此類乃以錯字為證據之引用，治之即滅供狀，一概不動。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r275memfix2.py
"""
import glob
import io
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), u'_work'))
import _simpmap as SM                                               # noqa: E402

U = os.path.expanduser(u'~')
DIRS = [os.path.join(U, u'.qoder', u'memory'),
        os.path.join(U, u'.qoder', u'projects', u'C--Users-lionc-OneDrive-----------------', u'memory')]
ENUM = re.compile(u'[、，・／]\\s*$')

rows = []
for d in DIRS:
    for f in sorted(glob.glob(os.path.join(d, u'*.md'))):
        txt = io.open(f, encoding=u'utf-8').read()
        mask, depth = [], 0
        for ch in txt:
            mask.append(depth == 0)
            if ch in u'「『':
                depth += 1
            elif ch in u'」』' and depth:
                depth -= 1
        for i, c in enumerate(txt):
            if mask[i] and c in SM.MAP:
                prev = txt[max(0, i - 12):i]
                nxt = txt[i + 1:i + 13]
                enumish = bool(ENUM.search(prev)) or bool(re.match(u'^[、・／\\u3000\\s]\\S', nxt))
                rows.append((os.path.basename(f), i, c, SM.MAP[c], txt[:i].count(u'\n') + 1,
                             prev.replace(u'\n', u'/'), nxt.replace(u'\n', u'/'),
                             u'？' if enumish else u'！'))
for k, (fn, i, c, t, ln, prev, nxt, mark) in enumerate(rows):
    print(u'%2d %-44s L%-4d %s→%s %s …%s[%s]%s…' % (k, fn, ln, c, t, mark, prev[-8:], c, nxt[:8]))
print(u'合計 %d 枚｜！=手筆（可治）・？=疑供狀（不動）' % len(rows))

# ── 治：`apply 0,3,7` 僅改所列之索引（同檔自後往前改，索引不亂）
if len(sys.argv) > 2 and sys.argv[1] == u'apply':
    pick = {int(x) for x in sys.argv[2].split(u',') if x.strip().isdigit()}
    byfile = {}
    for k in pick:
        fn, i, c, t = rows[k][0], rows[k][1], rows[k][2], rows[k][3]
        byfile.setdefault(fn, []).append((i, c, t))
    done = 0
    for fn, lst in byfile.items():
        path = next(os.path.join(d, f) for d in DIRS for f in os.listdir(d) if f == fn)
        txt = io.open(path, encoding=u'utf-8').read()
        for i, c, t in sorted(lst, reverse=True):
            assert txt[i] == c, u'索引 %d 移位（期 %s 得 %s）' % (i, c, txt[i])
            txt = txt[:i] + t + txt[i + 1:]
            done += 1
        io.open(path, 'w', encoding=u'utf-8', newline=u'\n').write(txt)
    print(u'已治 %d 枚（依索引點名，不構碼位、不全域替換）' % done)

