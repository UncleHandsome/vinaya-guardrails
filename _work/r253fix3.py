# -*- coding: utf-8 -*-
# The law text says ZHI-ZEI-BAN (no shi); correct the quote to the corpus form.
import io
p = '_work/r253three.py'
s = io.open(p, encoding='utf-8').read()
old = u'\u82e5\u6bd4\u4e18\u77e5\u662f\u8cca\u4f34'
new = u'\u82e5\u6bd4\u4e18\u77e5\u8cca\u4f34'
n = s.count(old)
print('hits', n)
if n != 1:
    raise SystemExit('unexpected')
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
