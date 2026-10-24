# -*- coding: utf-8 -*-
# Repair mangled CJK in _work/r253three.py using escapes only (ASCII-safe).
import io
p = '_work/r253three.py'
s = io.open(p, encoding='utf-8').read()
rep = [
    (u'\u6076\u610f', u'\u60e1\u610f'),                  # simp e-yi -> trad e-yi
    (u'Hide\u4ed6\u8cc7\u5177', u'\u85cf\u4ed6\u8cc7\u5177'),   # Hide ta-zi-ju -> cang ta-zi-ju
    (u'\u4f60\u4ee5\u4e3a\u540c\u884c', u'\u4f60\u4ee5\u70ba\u540c\u884c'),
    (u'\u4e00\u6bb5\u8def\u53ea\u662f\u987a\u6c34', u'\u4e00\u6bb5\u8def\u53ea\u662f\u9806\u6c34'),
    (u'\u4e09\u5bf6\u7684\u95e8\u9762', u'\u4e09\u5bf6\u7684\u9580\u9762'),
]
for a, b in rep:
    n = s.count(a)
    print('hit %d : %s' % (n, repr(a)))
    if n == 0:
        raise SystemExit('miss: %r' % a)
    s = s.replace(a, b)
io.open(p, 'w', encoding='utf-8').write(s)
bad = [c for c in set(s) if c in u'\u6076\u4e71\u7b80\u5173\u4e2a\u56fd\u4e3a\u8bf4\u5bf9\u7ecf\u89c6\u89c1\u8fd0\u8fd8\u8fd9\u91cf\u95e8\u95f4\u5e94']
print('left suspicious simp:', bad)
