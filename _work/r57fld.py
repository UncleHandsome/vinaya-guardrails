# -*- coding: utf-8 -*-
import io, os, re
from collections import Counter
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L=io.open(os.path.join(ROOT,u"佛陀的護欄_重構版.md"),encoding="utf-8-sig").read().replace("\r\n","\n").split(u"\n")
inc=False; c=Counter(); per=Counter(); cur=None
for l in L:
    if l.startswith(u"### 案例"):
        if cur: per[tuple(c)]+=0
        cur=l; c=Counter()
    m=re.match(u"^#### (.+)$", l)
    if m and cur: c[m.group(1)]+=1
    if re.match(u"^#{1,3} ", l) and not l.startswith(u"#### ") and not l.startswith(u"### 案例"):
        if cur: per[tuple(sorted(c))]+=1; cur=None; c=Counter()
for k,v in c.items(): pass
print(u"#### 欄名計數：")
for k,v in Counter([x for x in []]).items(): print(k,v)
CC=Counter()
inc=None
for l in L:
    if l.startswith(u"### 案例"): inc=l
    m=re.match(u"^#### (.+)$", l)
    if m and inc: CC[m.group(1)]+=1
for k,v in CC.most_common(30): print(u"%4d｜%s"%(v,k[:44]))
print(u"案數 %d"%sum(1 for l in L if l.startswith(u"### 案例")))
