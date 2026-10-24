# -*- coding: utf-8 -*-
import io, re

t = io.open(u'佛陀的護欄_四分律行為心理學與現代僧伽治理.md', encoding='utf-8').read()
L = t.split(u'\n')
print(u'== 世俗條號八行全文 ==')
for ln in (18278, 18423, 18538, 18549, 18551, 18552):
    print(u'--- L%d' % ln)
    print(u'    ' + L[ln - 1][:520])
print(u'\n== 附錄之結構（H1/H2）==')
i = next(k for k, l in enumerate(L, 1) if l.startswith(u'# 【卷末'))
for k in range(i - 1, len(L)):
    if L[k].startswith(u'# ') or L[k].startswith(u'## '):
        print(u'  L%-6d %s' % (k + 1, L[k][:60]))
print(u'\n== 示例法域之自陳 ==')
for m in re.finditer(u'示例法域|某法域|所稱法域|地方化', t):
    print(u'  L%-6d %s' % (t[:m.start()].count(u'\n') + 1, t[max(0, m.start() - 40):m.start() + 40].replace(u'\n', u' ')))
