# -*- coding: utf-8 -*-
# The earlier bulk replace also rewrote the guard string itself; restore it to test the
# SIMPLIFIED form (via escapes), so it guards instead of firing.
import io
p = '_work/r253three.py'
s = io.open(p, encoding='utf-8').read()
old = "if u'\u60e1\u610f' in l or u'Hide' in l:"
new = "if u'\\u6076\\u610f' in l or u'Hide' in l:"
print('guard hits:', s.count(old))
if s.count(old) != 1:
    raise SystemExit('unexpected guard form')
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
print('guard restored to simplified probe')
