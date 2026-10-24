# -*- coding: utf-8 -*-
"""274 輪・清理②：新稿歸自制（前器 r274clean.py 之锚多憑記憶構码，錯五處——今**锚皆自檔切片**）。

四步：① 切十一段交付殘跡（起行驗字）；② 第二章三篇合為一；
      ③ 逐行归位：『某某禁令』之**標題形**改『禁約』（第 26 目）・〔管轄雙情境解耦〕改『分立』（第 29 目）・
        表列兩枚錯號改『檢核案一：／二：』（第 27 目之盲處，以卡身覆核定讞）；
      ④ 拼接引文以**今冊 L1926 之已證全文**替換（自正本讀入，不重打一字）。
產 `_work/r274new3.md`，不動正本。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r274clean2.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AP = os.path.join(os.path.expanduser(u'~'), u'.qoder', u'tmp',
                  u'C--Users-lionc-OneDrive-----------------', u'attachments',
                  u'e11d207e-a4f7-4a0e-9edb-3124ac9d8a4a',
                  u'fa89e70f-39b1-4bde-9002-a0548ff0653d.txt')
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
BOOK = io.open(os.path.join(ROOT, NAME), encoding=u'utf-8').read().split(u'\n')
AL = io.open(AP, encoding=u'utf-8', errors=u'replace').read().split(u'\n')
OUT = os.path.join(ROOT, u'_work', u'r274new3.md')
JIU = u'\u6b21\u5c0d\u8a71'                                   # 次對話（實測於附件）

# ── ① 十一段切除（每段起行必含其字，錨不中即止）
SPANS = [(1, 9, u'\u9019\u662f'), (197, 206, JIU), (403, 413, JIU),
         (556, 577, u'\u5ba3\u544a'), (736, 755, u'\u8aaa\u660e'), (1020, 1046, u'\u8aaa\u660e'),
         (1207, 1229, u'\u5448\u8fad'), (1231, 1240, u'\u7b2c\u4e09\u7ae0'), (1473, 1482, u'\u7b2c\u4e09\u7ae0'),
         (1690, 1703, u'\u544a\u4e00\u6bb5\u843d'), (1810, 1816, u'\u9a57\u6536')]
drop = set()
for a, b, key in SPANS:
    got = AL[a - 1]
    assert key in got, u'L%d \u8d77\u884c\u4e0d\u542b\u300e%s\u300f\uff5c\u5be6\u5f97\u300e%s\u300f' % (a, key, got[:30])
    drop.update(range(a, b + 1))
L = [l for i, l in enumerate(AL, 1) if i not in drop]
print(u'\u2460 \u5207\u9664 %d \u6bb5\u3001%d \u884c\uff5c\u5269 %d \u884c' % (len(SPANS), len(drop), len(L)))

# ── ② 第二章三 H1 合為一
dup = [i for i, l in enumerate(L) if l.startswith(u'# \u7b2c\u4e8c\u7ae0')]
assert len(dup) == 3, u'\u7b2c\u4e8c\u7ae0 H1 %d \u679a\uff08\u671f 3\uff09' % len(dup)
for i in dup:
    L[i] = u'# \u7b2c\u4e8c\u7ae0\u3000\u5fc3\u6240\u52d5\u529b\u8207\u751f\u6d3b\u5834\u57df'
kill = set()
for i in dup[1:]:
    j = i
    while j + 1 < len(L) and (L[j + 1].strip() in (u'', u'---')):
        j += 1
    kill.update(range(i, j + 1))
L = [l for k, l in enumerate(L) if k not in kill]
print(u'\u2461 \u7b2c\u4e8c\u7ae0\u5408\u70ba\u4e00\uff5c\u53e6\u9664 %d \u884c' % len(kill))

# ── ③ 逐行歸位
JIEOU = u'\u89e3\u8026'                                       # 解耦（附件實測）
LING = u'\u7981\u4ee4'                                        # 禁令
n = sum(1 for l in L if JIEOU in l)
assert n == 1, u'\u89e3\u8026 %d \u898b\uff08\u671f 1\uff09' % n
for i, l in enumerate(L):
    if JIEOU in l:
        L[i] = l.replace(JIEOU, u'\u5206\u7acb')               # ➔分立
    if re.search(LING + u'(\u3011|\\*\\*)', l):               # 標題形之『某某禁令』➔禁約
        L[i] = re.sub(LING + u'(?=\u3011|\\*\\*)', u'\u7981\u7d04', L[i])
nling = sum(1 for l in L if re.search(LING + u'(?=\u3011|\\*\\*)', l))
print(u'\u2462 \u5206\u7acb 1 \u5904・\u7981\u7d04\u6539 %d \u8655\uff5c\u5269\u300e\u7981\u4ee4\u300f\u6a19\u984c\u5f62 %d' % (
    3 - nling, sum(1 for l in L if LING + u'\u3011' in l or LING + u'**' in l)))
CASE = u'\u3014\u6848\u4f8b '                                  # 〔案例
swap = {u'03': u'\u6aa2\u6838\u6848\u4e00\uff1a', u'02': u'\u6aa2\u6838\u6848\u4e8c\uff1a'}
ncut = 0
for i, l in enumerate(L):
    if not l.startswith(u'| **'):
        continue
    m = re.match(u'^\\| \\*\\*' + CASE + u'([0-9]{2})\u3015', l)
    if m and m.group(1) in swap:
        L[i] = u'| **' + swap[m.group(1)] + l[m.end():]
        ncut += 1
assert ncut == 2, u'\u8868\u5217\u6539\u6b50 %d\uff08\u671f 2\uff09' % ncut
print(u'\u2462 \u8868\u5217\u5169\u679a\u932f\u865f\u2794\u6aa2\u6838\u6848\u4e00\uff1a\uff0f\u4e8c\uff1a')

# ── ④ 拼接引文➔今冊已證全文（自正本 L1926 切片，不重打一字）
FAKE = u'\u898b\u7f6a\u80fd\u5982\u6cd5\u61fa\uff0c\u800c\u5f7c\u4e0d\u53d7'   # 見罪能如法懺，而彼不受
ANCHOR = u'\u50e7\u5718\u8ca0\u6709'                                            # 僧團負有
src = next(l for l in BOOK if FAKE not in l and ANCHOR in l and u'\u61fa\u8005' in l)   # 今冊之已證行
head = src[:src.index(ANCHOR)]
done = 0
for i, l in enumerate(L):
    if FAKE in l and ANCHOR in l:
        L[i] = head + l[l.index(ANCHOR):]
        done += 1
assert done == 1, u'\u62fc\u63a5\u5f15\u6587\u66ff\u63db %d\uff08\u671f 1\uff09' % done
print(u'\u2463 \u62fc\u63a5\u5f15\u6587\u2794\u4eca\u518a\u5df2\u8b49\u5168\u6587\uff08\u53d6\u6b63\u672c L%d\uff09' % (
    [k for k, x in enumerate(BOOK, 1) if x == src][0]))

# ── ⑤ 版式之淨
out = []
for l in L:
    if (len(l) - len(l.rstrip(u' '))) == 1:
        l = l.rstrip(u' ')
    if l.strip() in (u'---', u'***') and out and out[-1].strip():
        out.append(u'')                                        # 分隔線前補空行（防 setext）
    if l.strip() == u'' and len(out) >= 2 and out[-1].strip() == u'' and out[-2].strip() == u'':
        continue                                               # 三連空行斂為二
    out.append(l)
T = u'\n'.join(out)
io.open(OUT, 'w', encoding=u'utf-8').write(T)
t = io.open(OUT, encoding=u'utf-8').read()
H1 = re.findall(u'(?m)^# .*$', t)
assert len(H1) == 3, u'H1 %d \u679e\uff1a%s' % (len(H1), H1)
assert JIEOU not in t and FAKE not in t
print(u'\u2464 \u7522\u51fa %s\uff5c%d \u884c\uff5cH1\uff1a%s' % (
    os.path.basename(OUT), len(t.split(u'\n')), u'・'.join(h[:12] for h in H1)))
