# -*- coding: utf-8 -*-
import io, os, re
from collections import Counter, defaultdict
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L=io.open(os.path.join(ROOT,u"佛陀的護欄_重構版.md"),encoding="utf-8-sig").read().replace("\r\n","\n").split(u"\n")
CN=u"零一二三四五六七八九十"
def cnum(s):
    if u"十" in s:
        a,_,b=s.partition(u"十"); return (CN.index(a) if a else 1)*10+(CN.index(b) if b else 0)
    return CN.index(s) if s in CN else 0
ch=sec=0; nk=defaultdict(int); names=defaultdict(list)
inpre=False
for i,l in enumerate(L,1):
    if l.startswith("```"): inpre = not inpre
    if inpre: continue
    m=re.match(u"^# 第([一二三四五六七八九十]+)章",l)
    if m: ch=cnum(m.group(1)); sec=0; continue
    m=re.match(u"^## 第([一二三四五六七八九十]+)節",l)
    if m: sec=cnum(m.group(1)); continue
    if sec and not re.match(u"^### ",l):
        m=re.match(u"^#### (\d+)\. ",l) or re.match(u"^### ([一二三四五六七八九十]+)、",l)
        if m: nk[(ch,sec)]+=1
tot=bad=0; ex=[]
for l in L:
    if l.startswith("# "): continue
    for m in re.finditer(u"第([一二三四五六七八九十]+)章第([一二三四五六七八九十]+)節第([一二三四五六七八九十]+)款",l):
        a,b,c=cnum(m.group(1)),cnum(m.group(2)),cnum(m.group(3)); tot+=1
        n=nk.get((a,b),-1)
        if n<0 or c>n:
            bad+=1
            if len(ex)<12: ex.append(u"%s-%s（該節實 %s 款）"%(m.group(0),c,n if n>=0 else u"無此節"))
print(u"款級指針 %d｜越界 %d"%(tot,bad))
for e in ex: print(u"  "+e)
print(u"有款之節數：%d"%len(nk))
