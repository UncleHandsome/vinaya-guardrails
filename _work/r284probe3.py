# -*- coding: utf-8 -*-
"""284・量（三）：疑字之上下文（樞・輍・闊・抖），並列全書只一見之可疑字供目視。"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = io.open(os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md'),
            encoding=u'utf-8-sig').read()
L = S.split(u'\n')
for ch in (u'樞', u'輍', u'闊', u'抖', u'諉', u'標點'):
    print(u'=== %s（U+%04X）' % (ch, ord(ch)) if len(ch) == 1 else u'=== %s' % ch)
    for i, l in enumerate(L):
        k = l.find(ch)
        while k >= 0:
            print(u'  L%d …%s…' % (i + 1, l[max(0, k - 26):k + 26].replace(u'\n', u' ')))
            k = l.find(ch, k + 1)
            if ch == u'樞':
                break
