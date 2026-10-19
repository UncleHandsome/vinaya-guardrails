# -*- coding: utf-8 -*-
"""第五十七輪・②：案例大挪移（五篇二十章・依戒次歸位）。

病（實測）：章名與案例錯位——舊第九章「捨墮與犍度」實含 47 犍度案，舊第八章「九十單提」實含
37 提舍尼・眾學・法庭案；且篇內次序為 波羅夷→僧殘→單提→捨墮，與全書自制之戒次
（波羅夷→僧殘→捨墮→單提→提舍尼→眾學→犍度）相左，以致第七章結語「還要守住內城門」
（第三章五重陣地：內城門＝三十捨墮）指空。

治（章譜 declarative，章・節・案三級同一法源）：
  第一篇（理論奠基）1 意志・2 以遮衛性・3 修道要塞與母法中樞・4 心智病理＝舊 4＋舊 5 合一
  第二篇（金剛護欄）5 四波羅夷・6 十三僧殘・7 三十捨墮・8 九十單提・9 提舍尼與眾學法
  第三篇（性別防暴）10～13 如舊
  第四篇（正法久住）14～16 如舊・17 犍度現場與現代道場治理＝舊 9 犍度三節＋舊 17＋舊 9 結語
  第五篇（法架自捨）18～20 如舊（原【終卷】banner 改篇題）
凡節級・案例級指針依（舊章,舊節）→（新章,新節）・（舊章,舊案）→（新章,新案）恒等表換算；
篇級裸指按 舊篇→新篇 一表換算；拆分章（舊 8・舊 9）之裸章指無上下文可判者列帳待③。

用法：python -X utf8 _book/relocate.py [--go]
"""
import io
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, u"佛陀的護欄_重構版.md")
SNAP = os.path.join(HERE, u"挪移前快照.md")
LOG = os.path.join(HERE, u"挪移帳.tsv")
PEND = os.path.join(HERE, u"挪移待裁.txt")
GO = u"--go" in sys.argv
CN = u"零一二三四五六七八九十百"
DROP = set(u" \t、，。：:；;（）()「」『』“”‘'\"/／-—─│·・.!?？…")


def cnum(s):
    s = s.strip()
    if u"百" in s:
        a, _, b = s.partition(u"百")
        return (CN.index(a) if a else 1) * 100 + (cnum(b) if b else 0)
    if u"十" in s:
        a, _, b = s.partition(u"十")
        return (CN.index(a) if a else 1) * 10 + (CN.index(b) if b else 0)
    return CN.index(s) if s and s in CN else 0


def cn(n):
    if n < 10:
        return CN[n]
    if n < 20:
        return u"十" + (CN[n % 10] if n % 10 else u"")
    if n < 100:
        a, b = divmod(n, 10)
        return CN[a] + u"十" + (CN[b] if b else u"")
    a, b = divmod(n, 100)
    out = (CN[a] if a > 1 else u"") + u"百"
    return out + (u"零" if b and b < 10 else u"") + (cn(b) if b else u"")


def key(s):
    return u"".join(ch for ch in s if ch not in DROP)


# ══ 1. 解析 ══════════════════════════════════════════════════
raw = io.open(SRC, encoding="utf-8-sig").read().replace("\r\n", "\n")
L = raw.split(u"\n")
RE_CH = re.compile(u"^# 第([一二三四五六七八九十]+)章　(.+)$")
RE_BAN = re.compile(u"^# 【(.+?)】(.*)$")

sec_toc = None
items = []                      # ('front',lines) 由 front 表；('ban',t); ('ch',dict); ('tail',lines)
front, cur, tail = [], None, None
for i, l in enumerate(L):
    if l.startswith(u"## 【本書總目錄】"):
        sec_toc = i
    if tail is not None:
        tail.append(l)
        continue
    m = RE_CH.match(l)
    if m:
        cur = {u"n": cnum(m.group(1)), u"title": m.group(2), u"head": [], u"secs": []}
        items.append((u"ch", cur))
        continue
    b = RE_BAN.match(l)
    if b:
        cur = None
        if u"卷末" in b.group(1):
            tail = [l]
            continue
        items.append((u"ban", b.group(1)))
        continue
    if l.startswith(u"# "):
        cur = None
        continue
    if l.startswith(u"## ") and cur is not None:
        t = l[3:].strip()
        mm = re.match(u"^第([一二三四五六七八九十]+)節　(.*)$", t)
        cur[u"secs"].append({u"n": cnum(mm.group(1)) if mm else None, u"t": t, u"body": []})
        continue
    if cur is None:
        front.append(l)
    elif cur[u"secs"]:
        cur[u"secs"][-1][u"body"].append(l)
    else:
        cur[u"head"].append(l)
assert tail is not None, u"未捕到卷末"
CH = {c[u"n"]: c for k, c in items if k == u"ch"}
print(u"解析：章 %d・卷末 %d 行・卷首 %d 行" % (len(CH), len(tail), len(front)))
for n in sorted(CH):
    c = CH[n]
    print(u"  舊%s｜%s｜節%s" % (u"第%s章" % cn(n), c[u"title"][:20],
                                  u",".join(str(s[u"n"]) if s[u"n"] else u"＊" for s in c[u"secs"])))

# ══ 2. 章譜 ══════════════════════════════════════════════════
def whole(n):
    return (n, None, True)


def sub(n, secs, head=False):
    return (n, secs, head)


NEW = [
    (1, None, [whole(1)], False, u"第一篇：理論奠基——懸崖邊的修道要塞"),
    (2, None, [whole(2)], False, None),
    (3, None, [whole(3)], False, None),
    (4, u"心智病理：樹根、面具與六重心智閘門", [whole(4), (5, None, True)], True, None),
    (5, None, [whole(6)], False, u"第二篇：金剛護欄——比丘學處"),
    (6, None, [whole(7)], False, None),
    (7, u"三十捨墮：心理外科與物質極簡", [sub(9, [1, 2, 3, 4, 5], True)], False, None),
    (8, None, [sub(8, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])], False, None),
    (9, u"提舍尼與眾學法：正念前哨", [sub(8, [11, 12, 13]), sub(8, [14, 15, 16])], False, None),
    (10, None, [whole(10)], False, u"第三篇：性別防暴——比丘尼學處"),
    (11, None, [whole(11)], False, None),
    (12, None, [whole(12)], False, None),
    (13, None, [whole(13)], False, None),
    (14, None, [whole(14)], False, u"第四篇：正法久住——司法與治理"),
    (15, None, [whole(15)], False, None),
    (16, None, [whole(16)], False, None),
    (17, u"犍度現場與現代道場治理", [sub(9, [6, 7, 8]), whole(17), sub(9, [9])], False, None),
    (18, None, [whole(18)], False, u"第五篇：法架自捨——狂心自歇的終極歸宿"),
    (19, None, [whole(19)], False, None),
    (20, None, [whole(20)], False, None),
]

# ══ 3. 組裝 ══════════════════════════════════════════════════
SECMAP, CASEMAP, CHMAP = {}, {}, {}
out = []
for nch, newtitle, units, promote, ban in NEW:
    first = CH[units[0][0]]
    tt = newtitle or first[u"title"]
    if ban:
        out += [u"# 【%s】" % ban, u""]
    out += [u"# 第%s章　%s" % (cn(nch), tt), u""]
    sn = case = 0
    for (old_n, keys_, with_head) in units:
        c = CH[old_n]
        CHMAP.setdefault(old_n, set()).add(nch)
        if with_head:
            out += c[u"head"]
        chosen = c[u"secs"] if keys_ is None else [s for s in c[u"secs"] if s[u"n"] in keys_]
        for s in chosen:
            mm = re.match(u"^第[一二三四五六七八九十]+節　(.*)$", s[u"t"])
            base = mm.group(1) if mm else s[u"t"]
            if promote or mm:
                sn += 1
                body = base if mm else base.replace(u"　", u"：", 1)
                out.append(u"## 第%s節　%s" % (cn(sn), body))
                if mm:
                    SECMAP[(old_n, s[u"n"])] = (nch, sn)
            else:
                out.append(u"## %s" % base)
            for line in s[u"body"]:
                cmm = re.match(u"^### 案例([一二三四五六七八九十百]+)：(.*)$", line)
                if cmm:
                    case += 1
                    CASEMAP[(old_n, cnum(cmm.group(1)))] = (nch, case)
                    line = u"### 案例%s：%s" % (cn(case), cmm.group(2))
                out.append(line)
    print(u"新%s｜節 %d・案 %d" % (u"第%s章" % cn(nch), sn, case))

out += [u"", u"# 【卷末・工具與附錄】（息・隨身法器與考據底冊）", u""]
out += tail[1:]

# ══ 4. 指針換算 ═════════════════════════════════════════════
pend = defaultdict(list)
CHUNI = {o: list(s)[0] for o, s in CHMAP.items() if len(s) == 1}
SPLIT = {o for o, s in CHMAP.items() if len(s) > 1}
RE_CS = re.compile(u"第([一二三四五六七八九十]+)章案例([一二三四五六七八九十百]+)")
RE_SC = re.compile(u"第([一二三四五六七八九十]+)章第([一二三四五六七八九十]+)節")
RE_CHB = re.compile(u"(?<!案例)(?<!各)第([一二三四五六七八九十]+)章(?![第案])")
RE_PI = re.compile(u"第([一二三四五])篇")
PI = {1: 1, 2: 1, 3: 2, 4: 3, 5: 4}
n_cs = n_sc = n_ch = n_pi = 0
log = []


def fcs(m):
    global n_cs
    o = (cnum(m.group(1)), cnum(m.group(2)))
    if o in CASEMAP:
        nc, nn = CASEMAP[o]
        n_cs += 1
        return u"第%s章案例%s" % (cn(nc), cn(nn))
    pend[u"案例級不得其解"].append(m.group(0))
    return m.group(0)


def fsc(m):
    global n_sc
    o = (cnum(m.group(1)), cnum(m.group(2)))
    if o in SECMAP:
        nc, ns = SECMAP[o]
        n_sc += 1
        return u"第%s章第%s節" % (cn(nc), cn(ns))
    pend[u"節級不得其解"].append(m.group(0))
    return m.group(0)


def fch(m, line):
    global n_ch
    o = cnum(m.group(1))
    if o in CHUNI:
        n_ch += 1
        return u"第%s章" % cn(CHUNI[o])
    s = line[max(0, m.start() - 20):m.end() + 20]
    if u"犍度" in s or u"二十犍" in s:
        n_ch += 1
        return u"第%s章" % cn(17)
    if u"捨墮" in s:
        n_ch += 1
        return u"第%s章" % cn(7)
    if u"單提" in s or u"波逸提" in s:
        n_ch += 1
        return u"第%s章" % cn(8)
    if u"眾學" in s or u"提舍尼" in s:
        n_ch += 1
        return u"第%s章" % cn(9)
    pend[u"拆分章之裸指"].append(m.group(0) + u"｜…" + key(s)[-16:])
    return m.group(0)


def fpi(m):
    global n_pi
    n_pi += 1
    return u"第%s篇" % cn(PI[cnum(m.group(1))])


txt = u"\n".join(out)
txt = RE_CS.sub(fcs, txt)
txt = RE_SC.sub(fsc, txt)
lines2 = []
for line in txt.split(u"\n"):
    if line.startswith(u"# "):
        lines2.append(line)
        continue
    lines2.append(RE_CHB.sub(lambda m: fch(m, line), line))
txt = u"\n".join(lines2)
txt = RE_PI.sub(fpi, txt)
txt = txt.replace(u"【終卷：解脫——狂心自歇】", u"【第五篇：法架自捨——狂心自歇的終極歸宿】")

# ══ 4b. 親裁改寫（拆分章之裸指・篇次既改之過渡語・治理導航之本地節號）══
OVR = [
    # 裸「第九章」九處，逐條依律據判定（捨墮條→第七章，犍度制→第十七章）
    (u"於第九章專敘其制", u"於第十七章專敘其制", 1),
    (u"那些行款的全貌在第九章", u"那些行款的全貌在第十七章", 1),
    (u"與第九章「聽作自言治」", u"與第十七章「聽作自言治」", 1),
    (u"第九章表決諸幕", u"第十七章表決諸幕", 1),
    (u"【第九章「往執事人所過限求衣戒」", u"【第七章「往執事人所過限求衣戒」", 1),
    (u"（此與第九章「往執事人所過限」同一算術", u"（此與第七章「往執事人所過限」同一算術", 1),
    (u"【第九章羊毛氈三戒", u"【第七章羊毛氈三戒", 1),
    (u"【第九章：衣缽坐具針筒之畜與捨】", u"【第七章：衣缽坐具針筒之畜與捨】", 2),
    # 篇次與章次既改，過渡語隨之
    (u"它將在下章展開", u"它將在第四篇之末（第十七章）展開", 1),
    (u"但在推開比丘尼寺院那道緊閉的山門之前，我們還有一站非去不可：**律藏的另一半——二十犍度。**"
     u" 戒相告訴一個人「不可做什麼」；犍度則告訴一個團體「誰說了算、怎麼算、算幾次、犯了之後怎麼辦」。"
     u"下一章，我們將走進僧團的界場、會議室、工房與病房。",
     u"但在推開比丘尼寺院那道緊閉的山門之前，請先記下律藏的另一半：**二十犍度**。"
     u"戒相告訴一個人「不可做什麼」；犍度則告訴一個團體「誰說了算、怎麼算、算幾次、犯了之後怎麼辦」。"
     u"它不在本篇，而在第四篇之末（第十七章）——那里走進僧團的界場、會議室、工房與病房。", 1),
    (u"## 第九節　結語與過渡：從制度現場，走向更脆弱的一群",
     u"## 第九節　結語與過渡：從制度現場，走向歷史深處的追問", 1),
    (u"而當我們把目光從男眾的僧團轉向女眾的僧團時，將看見這套制度被推向更極致的精密——",
     u"而當我們把目光從制度現場收回，還有一層更深的追問：這套制度究竟是誰、在什麼時候、"
     u"出於什麼考慮定下來的？第五篇將走進兩千五百年的歷史爭議——", 1),
    (u"第十五節　篇間總結與過渡", u"第十五節　篇間總結與過渡", 0),
    (u"## 第十五節　第四篇總結與過渡：走向我們當下的生活",
     u"## 第十五節　篇間總結與過渡：走向我們當下的生活", 1),
    # 第十七章導航：治理五節今列第四～八節，其本地裸節指一律加三
    (u"`第一節（三線模型與雙院覆審）`", u"`第四節（三線模型與雙院覆審）`", 1),
    (u"`第四節第二款（寺產信託與繼承防禦）`", u"`第七節第二款（寺產信託與繼承防禦）`", 1),
    (u"`第四節第八至十款（極限法難與司法衝突避險）`", u"`第七節第八至十款（極限法難與司法衝突避險）`", 1),
    (u"`第三節第三款（僧籍勞雇雙軌）`", u"`第六節第三款（僧籍勞雇雙軌）`", 1),
    (u"`第四節第一款（公訴強制通報）`", u"`第七節第一款（公訴強制通報）`", 1),
    (u"`第三節第三款（志工與勞動防爆）`", u"`第六節第三款（志工與勞動防爆）`", 1),
    (u"`第一節第四款（機構長照防線）`", u"`第四節第四款（機構長照防線）`", 1),
    (u"`第二節（五德談話與創傷知情）`", u"`第五節（五德談話與創傷知情）`", 1),
    (u"`第四節第五款（反靈性煤氣燈操縱防護令）`", u"`第七節第五款（反靈性煤氣燈操縱防護令）`", 1),
    (u"利益迴避（第二節）", u"利益迴避（第五節）", 1),
    (u"第十四章第六節夜半四問", u"第十九章第六節夜半四問", 1),
    (u"> ### 開卷導航與法域界碑", u"> ### 治理篇導航與法域界碑", 1),
]
for a, b, w in OVR:
    c = txt.count(a)
    if c != w:
        pend[u"改寫未中"].append(u"%d／%d｜%s" % (c, w, a[:36]))
    txt = txt.replace(a, b)
    log.append(a[:12])

# ══ 4c. 篇 banner 歸位（RE_PI 只該換算舊文，新立之 banner 反被一併降號）══
bc = [0]


def fixban(m):
    bc[0] += 1
    return u"# 【第%s篇：%s】" % (cn(bc[0]), m.group(1))


txt = re.sub(u"^# 【第[一二三四五六]篇：(.+?)】$", fixban, txt, flags=re.M)
print(u"篇 banner 重編：%d 面" % bc[0])
toc = [u"## 【本書總目錄】", u""]
for line in txt.split(u"\n"):
    if line.startswith(u"# 【卷末"):
        toc += [u"**卷末・工具與附錄**", u""]
        continue
    m = re.match(u"^# 【(.+)】$", line)
    if m:
        toc += [u"**%s**" % m.group(1), u""]
        continue
    m = re.match(u"^# (第[一二三四五六七八九十]+章　.+)$", line)
    if m:
        toc.append(u"- %s" % m.group(1))
        continue
    m = re.match(u"^## (第[一二三四五六七八九十]+節　.+)$", line)
    if m:
        toc.append(u"    - %s" % m.group(1))
        continue
    m = re.match(u"^## (附錄[一二三四五]　.+)$", line)
    if m:
        toc.append(u"- %s" % m.group(1))
toc = u"\n".join(toc)
ti = [k for k, x in enumerate(front) if x.startswith(u"## 【本書總目錄】")][0]
prefix = u"\n".join(front[:ti]).rstrip(u"\n")
txt = prefix + u"\n\n---\n\n" + toc + u"\n\n---\n\n" + txt

print(u"換算：案 %d・節 %d・裸章 %d・篇 %d" % (n_cs, n_sc, n_ch, n_pi))
for k, v in pend.items():
    print(u"  待裁【%s】%d：%s" % (k, len(v), v[:4]))
with io.open(LOG, u"w", encoding="utf-8", newline="\n") as f:
    f.write(u"# 節\t舊章\t舊節\t新章\t新節\n")
    for (a, b), (c, d) in sorted(SECMAP.items()):
        f.write(u"S\t%d\t%d\t%d\t%d\n" % (a, b, c, d))
    f.write(u"# 案\t舊章\t舊案\t新章\t新案\n")
    for (a, b), (c, d) in sorted(CASEMAP.items()):
        f.write(u"C\t%d\t%d\t%d\t%d\n" % (a, b, c, d))
with io.open(PEND, u"w", encoding="utf-8", newline="\n") as f:
    for k, v in pend.items():
        f.write(u"## %s（%d）\n" % (k, len(v)))
        for x in v:
            f.write(u"  " + x + u"\n")
tmp = os.path.join(ROOT, u"_work", u"r57_挪移後.md")
io.open(tmp, "w", encoding="utf-8", newline="\n").write(txt)
io.open(SNAP, "w", encoding="utf-8", newline="\n").write(raw)
print(u"暫存 %s｜%d 行（前 %d 行）｜待裁帳 %s"
      % (os.path.relpath(tmp, ROOT), txt.count(u"\n") + 1, len(L), os.path.basename(PEND)))
if GO:
    io.open(SRC, "w", encoding="utf-8", newline="\n").write(txt)
    print(u"已落盤")
else:
    print(u"試跑：未改冊身")
