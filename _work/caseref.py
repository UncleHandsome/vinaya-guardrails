# -*- coding: utf-8 -*-
"""第 133 輪軸：『第六章案例：…』之所指須真在第六章——編號與案名兩式皆查

病緣：附錄I-3 一行舊作「第六章案例：〔遮24〕、〔開12〕、伊羅鉢羅龍王案」，而伊羅鉢羅龍王案
    實出第一章第四節第三款，第六章百則無此目——索引死鏈之『名相式』者，舊檢但查〔X n〕編號，
    於裸案名全無感，故立本軸。
"""
import io
import re
import sys

MD = sys.argv[1] if len(sys.argv) > 1 else u'ver38四分律_起心動念心智分析框架_修正版.md'
T = io.open(MD, encoding='utf-8').read()
L = T.split('\n')
# 第 250 輪：底冊四篇已另檔，主檔之印面尾今為「# 終卷」（不隨冊），故界標隨之
MSTART = next((i for i, l in enumerate(L) if l.startswith(u'# 終卷')), len(L))

# 第六章百則之編號與案名
nums = set()
titles = []
in6 = False
for l in L:
    if l.startswith(u'# '):
        in6 = l.startswith(u'# 第六章')
    if in6 and l.startswith(u'#### '):
        m = re.match(u'^#### 〔(遮|開|僧)(\\d{1,3})〕(.{2,28})', l)
        if m:
            nums.add(u'〔%s%s〕' % (m.group(1), m.group(2)))
            titles.append(m.group(3))
print(u'第六章編號 %d 個｜案名 %d 條' % (len(nums), len(titles)))

bad = []
seen = 0
for i, l in enumerate(L[:MSTART]):
    if u'第六章案例' not in l and u'第六章定位行' not in l:
        continue
    seg = l[l.find(u'第六章案例'):] if u'第六章案例' in l else l
    for m in re.finditer(u'〔(遮|開|僧)(\\d{1,3})〕', seg):
        seen += 1
        tok = u'〔%s%s〕' % (m.group(1), m.group(2))
        if tok not in nums:
            bad.append(u'  行 %d 無此編號：%s' % (i + 1, tok))
    for m in re.finditer(u'([\\u4e00-\\u9fff]{2,8}案)(?![\\u4e00-\\u9fff])', seg):
        nm = m.group(1)
        if nm in (u'第六章案例', u'百則案例', u'案例'):
            continue
        # 「…案」兩字之前若為虛字或類名（檔、統、攝、入、方、本、例、是、不、無、此、斯），乃詞組非案名
        if nm[-2] in u'檔統攝入方本例是不無此斯為亦即該諸':
            continue
        if not any(nm.rstrip(u'案') in t for t in titles):
            bad.append(u'  行 %d 裸案名而第六章無其目：%s' % (i + 1, nm))
print(u'查編號 %d 枚、裸案名若干' % seen)
for x in bad[:20]:
    print(x)
print(u'==== 第六章所指之實：%d 處 ====' % len(bad))
sys.exit(1 if bad else 0)
