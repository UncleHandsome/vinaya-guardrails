# -*- coding: utf-8 -*-
# LIANG (U+91CF) is a legitimate traditional character (measure/quantity); drop it from
# the simplified probe set so it stops firing on real prose.
import io
p = '_work/r253three.py'
s = io.open(p, encoding='utf-8').read()
old = "SIMP = set(u'\u4e24\u5f53\u5f3a\u968f\u5173\u4e2a\u56fd\u4e3a\u8bf4\u5bf9\u7ecf\u89c6\u89c1\u8fd0\u8fd8\u8fd9\u91cf')"
new = "SIMP = set(u'\u4e24\u5f53\u5f3a\u968f\u5173\u4e2a\u56fd\u4e3a\u8bf4\u5bf9\u7ecf\u89c6\u89c1\u8fd0\u8fd8\u8fd9')"
n = s.count(old)
print('hits', n)
if n != 1:
    raise SystemExit('unexpected SIMP line')
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
