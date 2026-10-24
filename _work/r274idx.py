# -*- coding: utf-8 -*-
"""274 輪・索引校正：MEMORY.md 現況快照一行去三處之staleness（换➔換・圍欄 43 之重出・148➔147・31／2➔32／3）。
錨皆自檔切片求得，不構码（本輪已三次記錯码位）。"""
import io
import os

P = os.path.join(os.path.expanduser(u'~'), '.qoder', 'projects',
                 u'C--Users-lionc-OneDrive-----------------', 'memory', 'MEMORY.md')
t = io.open(P, encoding=u'utf-8').read()
lines = t.split(u'\n')
k = next(i for i, l in enumerate(lines) if l.startswith(u'- [\u73fe\u6cc1\u5feb\u7167]'))
row = lines[k]
HUA, HUAN = u'\u6362', u'\u63db'                      # 换 → 換
out = row.replace(HUA, HUAN)
seg = u'\u570d\u6b04 43\u30fb'                        # 「圍欄 43・」重出，前句已言 45
out = out.replace(seg, u'', 1) if out.count(seg) == 1 else out
pairs = [(u'\u5361\u5916 148 \u6bb5', u'\u5361\u5916 147 \u6bb5'),
         (u'\u7bc0\u7d1a\u6307\u91dd 31\uff0f\u932f\u9776 0\uff0f\u672a\u8b49 2',
          u'\u7bc0\u7d1a\u6307\u91dd 32\uff0f\u932f\u9776 0\uff0f\u672a\u8b49 3')]
for a, b in pairs:
    assert out.count(a) == 1, u'錨非一：%s -> %d' % (a.encode('unicode_escape').decode(), out.count(a))
    out = out.replace(a, b)
lines[k] = out
io.open(P, 'w', encoding=u'utf-8').write(u'\n'.join(lines))
t2 = io.open(P, encoding=u'utf-8').read()
print(u'\u6821\u6b63\uff5a 换 \u5269 %d\uff5c\u570d\u6b04 43 \u5269 %d\uff5c147 \u898b %d\uff5c32\uff0f\u672a\u8b49 3 \u898b %d' % (
    t2.count(HUA), t2.count(u'\u570d\u6b04 43'), t2.count(u'\u5361\u5916 147'), t2.count(u'\u672a\u8b49 3')))
