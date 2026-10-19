# -*- coding: utf-8 -*-
import io, os, re
from collections import defaultdict
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L=io.open(os.path.join(ROOT,u"佛陀的護欄_重構版.md"),encoding="utf-8-sig").read().replace("\r\n","\n").split(u"\n")
CN=u"零一二三四五六七八九十百"
def cnum(s):
    if u"百" in s:
        a,_,b=s.partition(u"百"); return (CN.index(a) if a else 1)*100+(cnum(b) if b else 0)
    if u"十" in s:
        a,_,b=s.partition(u"十"); return (CN.index(a) if a else 1)*10+(CN.index(b) if b else 0)
    return CN.index(s) if s and s in CN else 0
def cn(n):
    if n<10: return CN[n]
    if n<20: return u"十"+(CN[n%10] if n%10 else u"")
    a,b=divmod(n,10); return CN[a]+u"十"+(CN[b] if b else u"")
A=defaultdict(int); B=defaultdict(int); names=defaultdict(dict)
ch=sec=0
for l in L:
    m=re.match(u"^# 第([一二三四五六七八九十]+)章　(.+)$",l)
    if m: ch=cnum(m.group(1)); sec=0; continue
    m=re.match(u"^## 第([一二三四五六七八九十]+)節　(.*)$",l)
    if m: sec=cnum(m.group(1)); continue
    if l.startswith(u"## ") or l.startswith(u"### 案例") or l.startswith(u"# ") or not sec: continue
    m=re.match(u"^### ([一二三四五六七八九十]+)、(.*)$",l)
    if m:
        n=cnum(m.group(1)); A[(ch,sec)]=max(A[(ch,sec)],n); names[(ch,sec)][n]=m.group(2).strip()[:34]; continue
    m=re.match(u"^### ([0-9]+)\. (.*)$",l)
    if m:
        n=int(m.group(2) and m.group(1)); B[(ch,sec)]=max(B[(ch,sec)],n); names[(ch,sec)].setdefault(n,m.group(2).strip()[:34])
tot=over=amb=0; rows=[]
for i,l in enumerate(L,1):
    if l.startswith(u"# "): continue
    for m in re.finditer(u"第([一二三四五六七八九十]+)章第([一二三四五六七八九十]+)節第([一二三四五六七八九十]+)款",l):
        a,b,k=cnum(m.group(1)),cnum(m.group(2)),cnum(m.group(3)); tot+=1
        hi=max(A.get((a,b),0),B.get((a,b),0)); nm=names.get((a,b),{}).get(k,u"")
        if k>hi:
            over+=1
            if A.get((a,b)) and B.get((a,b)): amb+=1
            rows.append((i,m.group(0),hi,nm,l.strip()[:90]))
print(u"款級指針 %d｜越界 %d（其中混式節 %d）｜款目總數 甲 %d 節・乙 %d 節"%(tot,over,amb,len(A),len(B)))
for i,s,hi,nm,line in rows[:24]:
    print(u"L%-6d %-22s 該節最大 %2d｜目：%s"%(i,s,hi,nm or u"（無）"))
    print(u"        %s"%line)
