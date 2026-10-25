# -*- coding: utf-8 -*-
r"""287・第七章四維矩陣之「N 案」宣稱與實數對量（唯讀，不改冊）。

法：只量「第二節　判例四維極速檢索矩陣」，整段併成一字符串取絕對偏移。
每枚宣稱（「共 N 案」或「（N 案）」）之管轄段＝宣稱尾，至
【其後第一個標題行首】與【下一枚宣稱首】之較近者；段內〔案例NN〕去重計數。
"""
import io
import re
import sys

PATH = sys.argv[1] if len(sys.argv) > 1 else u'../ver39四分律_起心動念心智分析框架_修正版.md'
TEXT = io.open(PATH, encoding='utf-8').read()
L = TEXT.split('\n')

i7 = next(i for i, l in enumerate(L) if l.startswith(u'# 第七章'))
i8 = next(i for i, l in enumerate(L) if l.startswith(u'# 第') and i > i7)
SEC = L[i7:i8]
j2 = next(i for i, l in enumerate(SEC) if l.startswith(u'### 第二節'))
j3 = next(i for i, l in enumerate(SEC) if l.startswith(u'### 第三節'))
B = SEC[j2:j3]
base = i7 + j2 + 1
body = u'\n'.join(B)

# 行首偏移表
starts, off = [], 0
for l in B:
    starts.append(off)
    off += len(l) + 1
starts.append(off)


def line_of(p):
    lo, hi = 0, len(starts) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if starts[mid] <= p:
            lo = mid
        else:
            hi = mid - 1
    return lo


claims = [(m.start(), m.end(), int(m.group(1)))
          for m in re.finditer(u'(?:共 |\uff08)(\d+) 案', body)]
heads = [starts[i] for i, l in enumerate(B) if re.match(u'^#{3,6} ', l)]
CID = re.compile(u'〔案例(\d{1,3})〕')

print(u'第二節 L%d〜L%d｜宣稱 %d 枚｜標題 %d 行' % (base, base + len(B) - 1, len(claims), len(heads)))
bad = []
for k, (s, e, n) in enumerate(claims):
    nxt_claim = claims[k + 1][0] if k + 1 < len(claims) else len(body)
    nxt_head = min([h for h in heads if h > e] or [len(body)])
    stop = min(nxt_claim, nxt_head)
    seg = body[e:stop]
    ids = [int(x) for x in CID.findall(seg)]
    uniq = sorted(set(ids))
    ok = len(uniq) == n
    li = line_of(s)
    print(u'%s L%-5d 稱 %-4d 得 %-4d %s｜%s' % (
        u'✔' if ok else u'✘', base + li, n, len(uniq),
        (u'' if ok else u'差%+d（列舉%d・行內重出%d）' % (len(uniq) - n, len(ids), len(ids) - len(uniq))),
        B[li].strip().replace(u'**', u'')[:44]))
    if not ok:
        bad.append(base + li)
        print(u'      名單：%s' % u' '.join(u'%02d' % x for x in uniq))
print(u'不合 %d 枚：%s' % (len(bad), bad))
