# -*- coding: utf-8 -*-
"""款級死指之內容回锚（v2）：不降級保錯章，唯二途——
   甲 指針自帶〔…〕（…）之節題・款題標籤者，於今冊窮舉求其唯一落點；
   乙 無標籤者，取本句之主題語（粗體・引號・『』內文）於諸節求其唯一落點；
   丙 二者皆不得，原樣不動、列帳待裁（絕不寫入未證之座標）。"""
import io, os, re, unicodedata
from collections import defaultdict
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GO=u"--go" in os.sys.argv
P=os.path.join(ROOT,u"佛陀的護欄_重構版.md")
L=io.open(P,encoding="utf-8-sig").read().replace("\r\n","\n").split(u"\n")
CN=u"零一二三四五六七八九十百"
DROP=set(u" \t、，。：:；;（）()「」『』“”‘'\"/／-—─│·・.!?？…*#|【】《》〇")
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
ch=sec=0; S={}
for i,l in enumerate(L,1):
    m=re.match(u"^# 第([一二三四五六七八九十]+)章",l)
    if m: ch=cnum(m.group(1)); sec=0; continue
    m=re.match(u"^## 第([一二三四五六七八九十]+)節　(.*)$",l)
    if m:
        if sec: S[(ch,sec)][1]=i-1
        sec=cnum(m.group(1)); S[(ch,sec)]=[i,len(L),m.group(2).strip(),set()]
        continue
    if (l.startswith(u"## ") or l.startswith(u"# ")) and sec:
        S[(ch,sec)][1]=i-1; sec=0
for k in list(S): S[k][1]=min(S[k][1],len(L))
for (c,s),(st,en,tt,ks) in S.items():
    for x in L[st-1:en]:
        m=re.match(u"^### ([一二三四五六七八九十]+)、(.*)$",x)
        if m: ks.add((cnum(m.group(1)),m.group(2).strip()))
        m=re.match(u"^### ([0-9]+)\. (.*)$",x)
        if m: ks.add((int(m.group(1)),m.group(2).strip()))
SECIDX={key(tt):k for k,(st,en,tt,ks) in S.items()}
KUIDX=defaultdict(list)
for k,(st,en,tt,ks) in S.items():
    for n,name in ks: KUIDX[key(name)[:18]].append((k[0],k[1],n))
def find_label(t):
    tk=key(t)
    r=[v for kk,v in SECIDX.items() if kk==tk or (len(tk)>=10 and kk.startswith(tk[:10]))]
    if not r:
        r=[x for kk,v in KUIDX.items() if tk[:12] and kk.startswith(tk[:12]) for x in v]
    out=[]
    for x in r:
        x=(x[0],x[1]) if len(x)>2 else tuple(x)
        if x not in out: out.append(x)
    return out
PAT=re.compile(u"第([一二三四五六七八九十]+)章第([一二三四五六七八九十]+)節第([一二三四五六七八九十]+)款(?:〔([^〕]+)〕)?")
dec=[]
for i,l in enumerate(L,1):
    if l.startswith(u"# "): continue
    for m in PAT.finditer(l):
        a,b,k,label=cnum(m.group(1)),cnum(m.group(2)),cnum(m.group(3)),m.group(4)
        inf=S.get((a,b))
        if inf and k in [n for n,_ in inf[3]]: continue
        cands=find_label(label) if label else []
        way=u"甲・節款標籤"
        if not cands:
            seg=l[max(0,m.start()-120):m.start()+120]
            for t in re.findall(u"\*\*([^*」』]{5,18})\*\*|『([^』]{5,18})』|「([^」]{5,18})」",seg):
                t=[x for x in t if x][0]
                if key(t) in key(m.group(0)): continue
                c=find_label(t)
                if len(c)==1: cands=c; way=u"乙・本句主題『%s』"%t[:10]; break
        if len(cands)==1:
            c2,s2=cands[0]
            kn=[n for n,_ in S[(c2,s2)][3]]
            new=u"第%s章第%s節"%(cn(c2),cn(s2))+(u"第%s款"%cn(k) if k in kn else u"")
            dec.append((i,m.group(0),new,way))
        else:
            dec.append((i,m.group(0),None,u"丙・候 %d"%len(cands)))
ok=[d for d in dec if d[2]]; no=[d for d in dec if not d[2]]
print(u"款級死指 %d｜可定靶 %d｜待裁 %d"%(len(dec),len(ok),len(no)))
for i,o,n,w in ok: print(u"  改 L%-6d %-26s → %-22s %s"%(i,o[:26],n,w))
for i,o,n,w in no: print(u"  待裁 L%-6d %-26s %s"%(i,o[:26],w))
if GO:
    t=u"\n".join(L)
    for i,o,n,w in ok: t=t.replace(o,n,1)
    io.open(P,"w",encoding="utf-8",newline="\n").write(t)
    io.open(os.path.join(ROOT,u"_book",u"款級待裁.txt"),"w",encoding="utf-8",newline="\n").write(
        u"\n".join(u"L%d｜%s｜%s"%(i,o,w) for i,o,n,w in no)+u"\n")
    print(u"已落盤；待裁帳 款級待裁.txt")
