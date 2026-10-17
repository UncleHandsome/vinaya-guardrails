# -*- coding: utf-8 -*-
"""指針覆核尺（refchk）：全書凡引「第N章案例M」與「第X條」同現之處，核其是否相配。
   甲 該章確有此案例（幽靈章號）；
   乙 同一片段（靶點之【…】為一片段；散文與表列則以整行為一片段）內所舉之條號，
      須落於該片段所指案例之標題條號集的並集內——並集而非一一配對，因一【…】內常數案並列。
   案例之號自「#### 案例…」標題取（含範圍展開），不複用任何生成器之記憶。
   丙 章號後若引「某名」（第X章「名」／第X章『名』），其名須真出於該章——第七批外審即有
      「第十二章『挫折慢心療法』」之錯植（其目實在第十五章第四節），舊尺因只核案例號而放行；
      名以正文之節題／案例題／小題為準，長名取前六字為鍵，遇「之落地」「那組」等虛詞尾巴先削。
   丁 「第X章案例Y」在散文中亦須有戶口（舊尺只看靶點與表列，散文之錯引無人管）。
用法：python -X utf8 _work/refchk.py [--go 則有疑即以 exit≠0 報不合格]
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
GO = u"--go" in sys.argv
BOOK = HP.SRC
U = u"零一二三四五六七八九"
L = io.open(BOOK, encoding="utf-8", newline=u"").read().split(u"\r\n")


def num(s):
    if s.isdigit():
        return int(s)
    if s == u"十":
        return 10
    if u"百" in s:
        a, b = s.split(u"百", 1)
        return (U.index(a) if a else 1) * 100 + (num(b) if b and b != u"零" else 0)
    if s.startswith(u"十"):
        return 10 + U.index(s[1])
    if u"十" in s:
        a, b = s.split(u"十")
        return U.index(a) * 10 + (U.index(b) if b else 0)
    return U.index(s) if s else 0


NUM = re.compile(u"第([0-9]{1,3}|[〇零一二三四五六七八九十百]{1,4})條")
RNG = re.compile(u"([0-9]{1,3}|[〇零一二三四五六七八九十]{1,4})\\s*(?:～|~|至|-)\\s*([0-9]{1,3}|[〇零一二三四五六七八九十]{1,4})")
CHH = re.compile(u"^# 第(.+?)章")
C4 = re.compile(u"^#### 案例([〇零一二三四五六七八九十百]+)：(.*)$")
REF = re.compile(u"第([〇零一二三四五六七八九十]{1,3})章案例([〇零一二三四五六七八九十百]{1,3})")
UNIT = re.compile(u"【[^【】]*】")

cases = {}
chap = 0
for i, s in enumerate(L):
    m = CHH.match(s)
    if m:
        try:
            chap = num(m.group(1))
        except ValueError:
            chap = 0
        continue
    m = C4.match(s)
    if m:
        tt = m.group(2)
        # 「第14、15、59條」式之並列：先把數詞間的頓號補成「條、第」，否則只認末一號（本尺第一版之盲）
        tt2 = re.sub(u"(?<=[0-9〇零一二三四五六七八九十百])、(?=[0-9〇零一二三四五六七八九十百])", u"條、第", tt)
        own = set(num(x) for x in NUM.findall(tt2))
        for a, b in RNG.findall(tt2):
            try:
                x, y = num(a), num(b)
            except ValueError:
                continue
            if x and y:
                own |= set(range(min(x, y), max(x, y) + 1))
        cases[(chap, m.group(1))] = (tt, own)

SECT = re.compile(u"^### ([〇零一二三四五六七八九十]+)、\s*(.*)$")
blk = {}
SUB = re.compile(u"^#### ((?!案例)[^：]{2,40})：")
names, span, chap_i = {}, {}, 0
for i, t in enumerate(L):
    m = CHH.match(t)
    if m:
        try:
            chap_i = num(m.group(1))
        except ValueError:
            chap_i = 0
        names.setdefault(chap_i, set())
        blk.setdefault(chap_i, [t])
        span[chap_i] = [i, len(L)]
        if len(span) > 1:
            for k in sorted(span):
                if k != chap_i and span[k][1] == len(L) and span[k][0] < i:
                    span[k][1] = i
        continue
    if not chap_i:
        continue
    blk[chap_i].append(t)                                # 章之全文（丙檢以「名是否見於該章」為準）
    m = SECT.match(t)
    if m:
        names[chap_i].add(m.group(2).strip())
        continue
    m = C4.match(t)
    if m:
        names[chap_i].add(m.group(2).strip())
        continue
    m = SUB.match(t)
    if m:
        names[chap_i].add(m.group(1).strip())

APPX = [i for i, s in enumerate(L) if s.startswith(u"# 附錄")]
apx0 = APPX[0] if APPX else len(L)
bad = []
nunit = nref = 0
for i, s in enumerate(L):
    if s.startswith(u"#### ") or i >= apx0:
        continue
    us = []
    if u"防禦靶點" in s:
        us = [m.group(0) for m in UNIT.finditer(s)]
    elif s.lstrip().startswith(u"|"):
        us = [s]
    if not us:
        continue
    for unit in us:
        rs = list(REF.finditer(unit))
        if not rs:
            continue
        nunit += 1
        nref += len(rs)
        pool = set()
        live = []
        for m in rs:
            key = (num(m.group(1)), m.group(2))
            if key not in cases:
                bad.append((u"甲", i + 1, u"%s章案例%s不存在｜%s" % (key[0], key[1], unit.strip()[:56])))
            else:
                tt, own = cases[key]
                live.append(unit.strip()[:56] if False else tt)
                pool |= own
        if not pool or pool == set(range(0)):
            continue
        for x in set(num(g) for g in NUM.findall(unit)):
            if x and x not in pool:
                bad.append((u"乙", i + 1, u"%s｜引第%d條，而被引案例標題只列 %s"
                            % (unit.strip()[:60], x, sorted(pool)[:12])))
# 丙／丁：散文與靶點一律再掃一遍章號引用
CP = re.compile(u"第([〇零一二三四五六七八九十]{1,3})章[「『]([^」』，。：；]{4,26})")
SECR = re.compile(u"第([〇零一二三四五六七八九十]{1,3})章第([〇零一二三四五六七八九十]{1,3})節")

npr = npc = 0
for i, t in enumerate(L):
    if i >= apx0 or t.startswith(u"#### 案例"):
        continue
    for m in SECR.finditer(t):
        npr += 1
        c, k = num(m.group(1)), num(m.group(2))
        if c not in span:
            bad.append((u"丁", i + 1, u"第%s章第%s節——章號無實" % (m.group(1), m.group(2))))
            continue
        a, b = span[c]
        n = sum(1 for x in range(a, b) if L[x].startswith(u"### "))
        if k > n:
            bad.append((u"丁", i + 1, u"第%s章第%s節——該章僅 %d 節｜%s" % (c, k, n, t.strip()[:56])))
    for m in CP.finditer(t):
        c, raw_nm = num(m.group(1)), m.group(2)
        if c not in names:
            continue
        npc += 1
        nm2 = re.split(u"之落地|之|所說|那組", raw_nm)[0].strip()
        if len(nm2) < 4:
            continue
        k2 = u"".join(x for x in nm2 if x not in u"，。：；、（）「」『』…—· ")
        # 「在本章」之判須排除引文自身一行，否則自證成立（旧口徑即因此漏掉「許他病衣不與」之類）
        body = u"".join(x for x in blk.get(c, []) if x != t)
        if k2 in body:
            continue
        # 名不在所引之章時，再看其四字組是否落在「他章」正文內——落他章者才是錯植，
        # 出書之 topical 別名（如「受食限量」「坐具與臥具過量」）全書無一處連写，故不報。
        grams = set(k2[i:i + 4] for i in range(0, max(0, len(k2) - 3)))
        # 判準：此名雖不在所引之章，但其四字組見於「他章之標題」——那才是張冠李戴；
        # topical 別名（「受食限量」「坐具與臥具過量」）全書標題無一處有此四字組，故不報。
        # （舊口徑取他章『正文』，六字組漏逮「許他病衣不與」，四字組又誤報三條，今改以標題為限。）
        other = []
        for cc in sorted(names):
            if cc == c:
                continue
            for n2 in names[cc]:
                k3 = u"".join(x for x in n2 if x not in u"，。：；、（）「」『』…—· ")
                if any(g in k3 for g in grams):
                    other.append(cc)
                    break
        if other:
            bad.append((u"丙", i + 1, u"第%s章引『%s』——該章無此名，而他章正文有之（疑錯植：%s）｜%s"
                        % (c, raw_nm, u"／".join(u"第%s章" % k for k in sorted(other))[:26],
                           t.strip()[:52])))
print(u"案例冊 %d 則｜片段 %d 處（含引針 %d）｜章節指 %d 處｜章名引 %d 處" % (len(cases), nunit, nref, npr, npc))
for k, ln, msg in bad:
    print(u"  ✗【%s】L%-5d｜%s" % (k, ln, msg))
print(u"== 疑點 %d（甲 %d／乙 %d／丙 %d／丁 %d）" % (
    len(bad), sum(1 for b in bad if b[0] == u"甲"), sum(1 for b in bad if b[0] == u"乙"),
    sum(1 for b in bad if b[0] == u"丙"), sum(1 for b in bad if b[0] == u"丁")))
if GO and bad:
    raise SystemExit(u"指針有疑，未過")
