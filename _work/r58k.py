# -*- coding: utf-8 -*-
import io, os, re
from collections import Counter, defaultdict
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L=io.open(os.path.join(ROOT,u"佛陀的護欄_重構版.md"),encoding="utf-8-sig").read().replace("\r\n","\n").split(u"\n")
ST=[(u"甲 H3漢字、", u"^### ([一二三四五六七八九十]+)、"),
    (u"乙 H4阿拉伯.", u"^#### ([0-9]+)\. "),
    (u"丙 H4漢字、", u"^#### ([一二三四五六七八九十]+)、"),
    (u"丁 H3阿拉伯.", u"^### ([0-9]+)\. "),
    (u"戊 粗體第一款", u"^\*\s*\*\*第([一二三四五六七八九十]+)款"),
    (u"己 粗體漢字、", u"^\*\s*\*\*([一二三四五六七八九十]+)、"),
    (u"庚 列表『（甲）』", u"^\s*\*?\s*\*?【?第?([甲乙丙丁戊己庚辛壬癸]+)】?")]
cnt=Counter()
for l in L:
    for tag,p in ST:
        if re.match(p,l): cnt[tag]+=1
print(u"標記總數：", dict(cnt))
# 每節之款數（依節內所見最多之一式）
CN=u"零一二三四五六七八九十"
def cnum(s):
    if u"十" in s:
        a,_,b=s.partition(u"十"); return (CN.index(a) if a else 1)*10+(CN.index(b) if b else 0)
    return CN.index(s) if s in CN else 0
ch=sec=0; ku=defaultdict(Counter); mix=defaultdict(set)
for l in L:
    m=re.match(u"^# 第([一二三四五六七八九十]+)章",l)
    if m: ch=cnum(m.group(1)); sec=0; continue
    m=re.match(u"^## 第([一二三四五六七八九十]+)節",l)
    if m: sec=cnum(m.group(1)); continue
    if not sec: continue
    for tag,p in ST:
        mm=re.match(p,l)
        if mm:
            v=mm.group(1)
            n=int(v) if v.isdigit() else cnum(v)
            if n: ku[(ch,sec)][tag]+=1; mix[(ch,sec)].add(tag)
multi=[k for k,v in mix.items() if len(v)>1]
print(u"有款之節 %d｜兩式以上者 %d"%(len(ku),len(multi)))
for k in sorted(multi)[:10]: print(u"  混式 %s｜%s"%(k,dict(ku[k])))
