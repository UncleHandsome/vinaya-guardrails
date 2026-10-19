# -*- coding: utf-8 -*-
"""債帳之末：以尺九同一口徑窮舉死指，逐條附『該節實有之款序』與本句主題，令親裁一望可決。"""
import io, os, re, unicodedata
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P=os.path.join(ROOT,u"佛陀的護欄_重構版.md"); T=os.path.join(ROOT,u"_book",u"款級待裁.tsv")
CN=u"零一二三四五六七八九十百"
DROP=set(u" \t、，。：:；;（）()「」『』“”‘'\"/／-—─│·・.!?？…*#|【】《》〇")
def key(s): return u"".join(c for c in unicodedata.normalize("NFKC",s) if c not in DROP)
def cnum(s):
    if u"十" in s:
        a,_,b=s.partition(u"十"); return (CN.index(a) if a else 1)*10+(CN.index(b) if b else 0)
    return CN.index(s) if s in CN else 0
def cn(n):
    if n<10: return CN[n]
    if n<20: return u"十"+(CN[n%10] if n%10 else u"")
    a,b=divmod(n,10); return CN[a]+u"十"+(CN[b] if b else u"")
L=io.open(P,encoding="utf-8-sig").read().replace("\r\n","\n").split(u"\n")
ch=sec=0; ku={}; ttl={}
for l in L:
    m=re.match(u"^# 第([一二三四五六七八九十]+)章",l)
    if m: ch=cnum(m.group(1)); sec=0; continue
    m=re.match(u"^## 第([一二三四五六七八九十]+)節　?(.*)$",l)
    if m: sec=cnum(m.group(1)); ku.setdefault((ch,sec),set()); ttl[(ch,sec)]=m.group(2).strip(); continue
    if l.startswith(u"## ") or l.startswith(u"# "): sec=0; continue
    if not sec: continue
    m=re.match(u"^### ([一二三四五六七八九十]+)、",l)
    if m: ku[(ch,sec)].add(cnum(m.group(1))); continue
    m=re.match(u"^### ([0-9]+)\. ",l)
    if m: ku[(ch,sec)].add(int(m.group(1)))
rows=[]
for i,l in enumerate(L,1):
    if l.startswith(u"# "): continue
    for m in re.finditer(u"第([一二三四五六七八九十]+)章第([一二三四五六七八九十]+)節第([一二三四五六七八九十]+)款",l):
        a,b,k=cnum(m.group(1)),cnum(m.group(2)),cnum(m.group(3))
        ks=ku.get((a,b))
        if ks is not None and k in ks: continue
        seg=l[max(0,m.start()-70):m.start()]
        ts=[x for g in re.findall(u"『([^』]{3,18})』|「([^」]{3,18})」|\*\*([^*]{3,18})\*\*",seg) for x in g if x]
        rows.append((i,u"第%s章第%s節第%s款"%(cn(a),cn(b),cn(k)),
                     u"（該節無明序之款）" if not ks else u"實有：%s"%u"、".join(cn(x) for x in sorted(ks)),
                     ttl.get((a,b),u"（無此節）")[:22],
                     u"／".join(x[:14] for x in ts[:2]) or u"（本句無引號名相，須讀全句）"))
io.open(T,"w",encoding="utf-8",newline="\n").write(u"\t".join(
  [u"行",u"死指",u"該節實有之款序",u"該節今題",u"本句主題（候定之錨）"])+"\n"+
  u"\n".join(u"\t".join(str(x) for x in r) for r in rows)+"\n")
print(u"債帳 %d 行"%len(rows))
