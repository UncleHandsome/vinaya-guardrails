# -*- coding: utf-8 -*-
import io, os, re, unicodedata
from collections import defaultdict
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GO=u"--go" in os.sys.argv
L=io.open(os.path.join(ROOT,u"佛陀的護欄_重構版.md"),encoding="utf-8-sig").read().replace("\r\n","\n").split(u"\n")
CN=u"零一二三四五六七八九十百"
DROP=set(u" \t、，。：:；;（）()「」『』“”‘'\"/／-—─│·・.!?？…*#|【】《》")
def key(s): return u"".join(c for c in unicodedata.normalize("NFKC",s) if c not in DROP)
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
# 節模型：(章,節) -> (起,迄,款序集合,節題)
ch=sec=0; secinfo={}; order=[]
for i,l in enumerate(L,1):
    m=re.match(u"^# 第([一二三四五六七八九十]+)章",l)
    if m: ch=cnum(m.group(1)); sec=0; continue
    m=re.match(u"^## 第([一二三四五六七八九十]+)節　(.*)$",l)
    if m:
        if secinfo and order: secinfo[order[-1]][1]=i-1
        sec=cnum(m.group(1)); order.append((ch,sec)); secinfo[(ch,sec)]=[i,len(L),m.group(2)]
        continue
    if l.startswith(u"## ") and secinfo and order:
        secinfo[order[-1]][1]=i-1; sec=0
for k in order: secinfo[k][1]=min(secinfo[k][1], len(L))
def ku(s,e):
    ks=set()
    for x in L[s-1:e]:
        m=re.match(u"^### ([一二三四五六七八九十]+)、",x)
        if m: ks.add(cnum(m.group(1)))
        m=re.match(u"^### ([0-9]+)\. ",x)
        if m: ks.add(int(m.group(1)))
    return ks
for k in order: secinfo[k].append(ku(secinfo[k][0],secinfo[k][1]))
PAT=re.compile(u"第([一二三四五六七八九十]+)章第([一二三四五六七八九十]+)節第([一二三四五六七八九十]+)款(?:〔[^〕]*〕)?")
def locate(term, chh):
    tk=key(term)[:14]
    if len(tk)<5: return []
    hits=[]
    for (c,s),(st,en,tt,ks) in secinfo.items():
        if st and key(u"".join(L[st-1:en])).find(tk)>=0: hits.append((c,s))
    return hits
fix=[]; down=[]
for i,l in enumerate(L,1):
    if l.startswith(u"# "): continue
    for m in PAT.finditer(l):
        a,b,k=cnum(m.group(1)),cnum(m.group(2)),cnum(m.group(3))
        inf=secinfo.get((a,b))
        if inf and k in inf[3]:
            continue
        ctx=key(l[max(0,m.start()-40):m.start()])[-18:]
        pre=key(l[max(0,m.start()-30):m.end()+40])
        term=None
        g=re.search(u"[（(]([^）)]{4,16})[）)]",l[max(0,m.start()-70):m.start()])
        if g: term=g.group(1)
        else:
            g2=re.findall(u"\*\*([^*]{4,14})\*\*",l)
            term=g2[0] if g2 else None
        cand=locate(term, a) if term else []
        cand=[x for x in cand if x!=(a,b)]
        if len(set(cand))==1:
            c2,s2=cand[0]
            k2=k if k in secinfo[(c2,s2)][3] else None
            new=u"第%s章第%s節"%(cn(c2),cn(s2))+(u"第%s款"%cn(k2) if k2 else u"")
            fix.append((i,m.group(0),new,u"內容錨：%s"%term))
        else:
            down.append((i,m.group(0),u"第%s章第%s節"%(cn(a),cn(b)),u"%d 候"%len(set(cand)),term or u"-"))
print(u"款級重定向 %d｜降為節級 %d"%(len(fix),len(down)))
for i,o,nn,w in fix: print(u"  L%-6d %-20s → %-20s %s"%(i,o,nn,w))
for i,o,nn,w,t in down: print(u"  降 L%-6d %-20s → %-16s %s｜錨 %s"%(i,o,nn,w,t))
if GO:
    txt=u"\n".join(L)
    for i,o,nn,w in fix: txt=txt.replace(o,nn,1)
    for i,o,nn,w,t in down: txt=txt.replace(o,nn,1)
    io.open(os.path.join(ROOT,u"佛陀的護欄_重構版.md"),"w",encoding="utf-8",newline="\n").write(txt)
    print(u"已落盤")
