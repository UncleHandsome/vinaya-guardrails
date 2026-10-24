# -*- coding: utf-8 -*-
import io, re

t = io.open(u'佛陀的護欄_四分律行為心理學與現代僧伽治理.md', encoding='utf-8').read()
L = t.split(u'\n')
print(u'表之位置：')
for i, l in enumerate(L, 1):
    if u'示例法域之條號對照' in l:
        print(u'  L%d %s' % (i, l[:60]))
print(u'附錄標題之所有出現（含行內）：')
for pat in (u'## 附錄四', u'## 附錄五'):
    for m in re.finditer(re.escape(pat), t):
        print(u'  %s → L%d｜%s' % (pat, t[:m.start()].count(u'\n') + 1, t[m.start():m.start() + 34].replace(u'\n', u'⏎')))
