# -*- coding: utf-8 -*-
"""269 輪・帳佐：讀記憶層現況檔之尺群段尾，供 append 之錨（不在 shell 帶反引號）。"""
import io
import os

P = os.path.join(os.path.expanduser(u'~'), u'.qoder', u'projects',
                 u'C--Users-lionc-OneDrive-----------------', u'memory',
                 u'project-round31-state.md')
t = io.open(P, encoding=u'utf-8').read()
for k in [u'book_meta', u'r267count.py', u'r268scan.py', u'r268net.py', u'29 目', u'（形制與數目 28 目']:
    print(u'%-18s 命中 %d' % (k, t.count(k)))
i = t.find(u'**尺群')
j = t.find(u'\n\n', i)
print(u'── 尺群段（尾 220 字）──')
print(t[max(i, j - 240):j])
