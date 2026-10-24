# -*- coding: utf-8 -*-
import io, re

book = io.open(u'佛陀的護欄_四分律行為心理學與現代僧伽治理.md', encoding='utf-8').read()
k4 = book.find(u'## 附錄四')
k5 = book.find(u'## 附錄五')
kt = book.find(u'示例法域之條號對照')
print(u'偏移：四=%d 五=%d 表=%d（表在四之後？%s 在五之前？%s）' % (k4, k5, kt, kt > k4, kt < k5))
apx4 = book[k4:k5]
print(u'apx4 內含表題？%s｜apx4 內含『### 附』？%s' % (u'示例法域之條號對照' in apx4, u'### 附' in apx4))
i = apx4.find(u'示例法域之條號對照')
print(u'表題前之十六字：%r' % apx4[max(0, i - 20):i + 8])
for m in re.finditer(u'(?m)^### [^\n]{0,40}', apx4):
    print(u'  H3｜%r' % m.group(0)[:44])
