# -*- coding: utf-8 -*-
"""272 輪・SOP 今制之改帳（積輪 22・第九尺入列・目數三十有一・兩目之說補入）。

何以走腳本不走手：本檔以漢字為錨之 Edit 嘗而不中（我打的『殘』到器中已是簡形，錨永不中）。
      故**錨一律以 \\uXXXX 寫（純 ASCII，傳遞層無從更動）**，插入之長句仍以漢字寫，
      寫畢另次呼叫以 codepoint 掃之（簡形名單為鑰），有則逐枚帶錨改——**改字之器不靠目驗**。
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, u'\u5217\u5370SOP.md')                       # 列印SOP.md
T = io.open(P, encoding=u'utf-8').read()
L = T.split(u'\n')
log = []


def must1(txt, plain, tag):
    assert txt.count(plain) == 1, u'%s｜錨非一（%d 中）' % (tag, txt.count(plain))
    return txt


# ══ ① 今制行：積輪 21➔22・272 之 clause 補入（插在『…））**而 PDF 未重建**’之括前）
i0 = next(i for i, l in enumerate(L) if l.startswith(u'- **\u4e09\u5341\u4e5d\u7248\u4eca\u5236'))
s = must1(L[i0], u'21**', u'\u2460')
s = s.replace(u'21**', u'22**')
j = s.rfind(u'\uff09', 0, s.index('PDF'))
assert j > 0, u'\u2460 \u62ec\u865f\u4e0d\u53ef\u6c42'
CLAUSE = (u'\u3001' + u'272 之立第 31 目『目數自對合』'
          u'並添第九尺『牙列矩陣』（三十二針逐目植病・俱逮・冊身一字未動）')
L[i0] = s[:j] + CLAUSE + s[j:]
log.append(u'\u2460 \u7a4d\u8f2a 22 / 272 clause')

# ══ ② 公約行：輪號・三十一目・近六目・一行跑九尺・30 與 31 兩目之說・r272teeth 入列
i1 = next(i for i, l in enumerate(L) if l.startswith(u'- **') and
          u'\u67e5\u6838\u516c\u7d04' in l and l is not L[i0])     # 『查核公約』行，非『今制』行
s = L[i1]
cand = [p for p in range(len(s)) if s.startswith(u'271', p) and u'255' in s[max(0, p - 10):p]]
assert len(cand) == 1, u'\u2461a\uff08%d \u5019\u9078\uff09' % len(cand)
p = cand[0]
s = s[:p] + u'272' + s[p + 3:]
for plain, new, tag in [(u'\u4e8c\u5341\u4e5d\u76ee', u'\u4e09\u5341\u4e00\u76ee', u'\u2461b'),
                        (u'\u8fd1\u56db\u76ee', u'\u8fd1\u516d\u76ee', u'\u2461c'),
                        (u'\u4e00\u884c\u8dd1\u516b\u5c3a', u'\u4e00\u884c\u8dd1\u4e5d\u5c3a', u'\u2461d')]:
    s = must1(s, plain, tag)
    s = s.replace(plain, new)
m1 = s.index(u'26\uff0f28\uff0f29')
DESC = (u'\u300130\u300e\u66f8\u540d\u865f\u5167\u4e4b\u672c\u5f8b\u7bc7\u540d\u9808\u898b\u65bc\u8a9e\u6599\u300f'
        u'\uff08271 \u8f2b\uff1a\u53ea\u8a8d\u542b\u300e\u72b5\u5ea6\u300f\u4e4b\u300aX\u300b\uff0c'
        u'\u524d\u7de8\u3001\u6298\u90b5\u3001\u64f2\u7e3d\u6578\u7a31\uff09'
        u'\u300131\u300e\u76ee\u6578\u81ea\u5c0d\u5408\u300f\uff08272 \u8f2b\uff1a\u9012\u8b80 `__file__`\uff0c'
        u'\u76ee\u540d\u9808\u5e38\u91cf\u3001try/except \u540c\u540d\u3001'
        u'\u6e90\u552f\u4e00\u540d\u6578\uff1d\u5be6\u5370\u76ee\u6578\uff0c'
        u'\u65a5\u300e\u4e0d\u8b8a\u91cf N/N\u300f\u4e4b N \u4e0d\u518d\u5b8c\u5168\u9760\u5c3a\u81ea\u5831\uff09')
s = s[:m1] + DESC + s[m1:]
last = s.rindex('v39apx4chk') + len('v39apx4chk')
assert s[last] == u'\uff09', u'\u2461e \u5217\u672a\u9589'
L[i1] = s[:last] + u'\u3001**r272teeth**' + s[last:]
log.append(u'\u2461 \u76ee\u6578 / \u4e5d\u5c3a / \u5169\u76ee\u4e4b\u8aaa')

io.open(P, 'w', encoding=u'utf-8').write(u'\n'.join(L))
t2 = io.open(P, encoding=u'utf-8').read()
assert t2.count(u'22**') >= 1 and u'\u4e09\u5341\u4e00\u76ee' in t2 and u'**r272teeth**' in t2
print(u'\u5df2\u843d\u5730\uff1a' + u' | '.join(log))
print(u'\u884c\u6578 %d\u2192%d\uff08\u672c\u5668\u4e0d\u589e\u884c\uff09' % (len(L), len(t2.split(u'\n'))))
