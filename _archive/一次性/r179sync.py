# -*- coding: utf-8 -*-
# 第 179 輪「無待建之動」之實測：主檔之印面逐行須俱見於建置當輪之中介檔
# （中介檔由 build38 自主檔生成，若主檔印面其後有改而行行仍在中介檔，即證未動；
#  底冊（附錄C/K/L/M/終卷）與卷首目錄區塊乃管線整段取代者，不預。）
import io
import re
import sys

sys.path.insert(0, u'.')
import _tk

MD = u'_print/ver38_列印版.md'
lines = _tk.LINES
bottom = set(_tk.bottom_lines())

# 卷首標準目錄區塊：自 TOC_H2 之 H2 起，至下一個 H1/H2 前（build38.write_md 同式）
s = None
for i, l in enumerate(lines):
    if l.startswith(u'## ') and u'全書開卷標準目錄' in l:
        s = i
        break
assert s is not None, u'目錄區塊起點不中——法源已改，本器須同步'
e = None
for i in range(s + 1, len(lines)):
    if re.match(u'^#{1,2}\\s', lines[i]):
        e = i
        break
assert e is not None and e > s, u'目錄區塊終點不中'
toc = set(range(s, e))
print(u'範圍斷：目錄區塊 %d–%d 行（%d 行整段取代）｜底冊 %d 行不預' % (s + 1, e, len(toc), len(bottom)))

# 管線就地改形者（非內容之動），逐條對形豁免
EXEMPT = (u'## 【開卷總提撕】',)

def norm(x):
    return re.sub(u'\\s+', u'', x).strip()

tgt = norm(io.open(MD, encoding=u'utf-8').read())
miss = []
kept = 0
for i, l in enumerate(lines):
    if (i + 1) in bottom or i in toc or not norm(l):
        continue
    if any(l.startswith(k) for k in EXEMPT):
        continue
    kept += 1
    if norm(l) not in tgt:
        miss.append((i + 1, l[:60]))

print(u'印面逐行入中介檔：可核 %d 行｜查無 %d 行' % (kept, len(miss)))
for n, t in miss[:12]:
    print(u'   L%d %s' % (n, t))
print(u'結果斷：%s' % (u'無待建之動（印面與建冊當輪所出中介檔全同）' if not miss
                       else u'有待建之動——印面 %d 行未入中介檔' % len(miss)))
