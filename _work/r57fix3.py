# -*- coding: utf-8 -*-
"""第五十七輪・③：指針清零（承 r57ap5fix 之後）。

甲 附錄五回查表 49 列破損之最後五列——指紋不得者，依行內『波逸提第N條』回查今冊實有之案，
   逐條親裁（第22・23條→第八章案例二十一，第5條→第八章案例十六，第14條→第八章案例二十二，
   第53條→第八章案例二十七，皆驗其案題而後落筆）。
乙 正文 35 條「第七章案例N」死鏈——此乃單提章號之舊稱（合編本・護欄冊相沿），
   今冊單提前半為第八章（1～56）、後半與提舍尼眾學為第九章（57→一）；
   換算三例已對案題驗證：二十九→「僧斷事未竟…（第75條）」、六十八→「誤入眠婦屋」、
   七十八→「與漿水洗瘡」，皆相合，故一律照此式換算，越界者列帳不寫。
丙 「第十一章第六／七節」5 處——依所引之事（出罪大典・心識相續轉業）歸第十六章第六／七節。
丁 「附錄六凡例正名令」2 處——正名令實在附錄五，改之。
戊 三張回查表之範圍宣稱（壹・貳・參）與「共五十五個案例」改由列中實號自算。
"""
import io
import os
import re
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u"佛陀的護欄_重構版.md")
CN = u"零一二三四五六七八九十百"
GO = True


def cnum(s):
    s = s.strip()
    if u"十" in s:
        a, _, b = s.partition(u"十")
        return (CN.index(a) if a else 1) * 10 + (CN.index(b) if b else 0)
    return CN.index(s) if s and s in CN else 0


def cn(n):
    if n < 10:
        return CN[n]
    if n < 20:
        return u"十" + (CN[n % 10] if n % 10 else u"")
    a, b = divmod(n, 10)
    return CN[a] + u"十" + (CN[b] if b else u"")


L = io.open(BOOK, encoding="utf-8-sig").read().replace("\r\n", "\n").split(u"\n")
case_of, sec_of = Counter(), Counter()
cur = 0
for l in L:
    m = re.match(u"^# 第([一二三四五六七八九十]+)章", l)
    if m:
        cur = cnum(m.group(1))
        continue
    if l.startswith(u"### 案例") and cur:
        case_of[cur] += 1
    elif l.startswith(u"## 第") and cur:
        sec_of[cur] += 1
nrep = []

# ── 甲：五列親裁（依行內戒條對今冊案題）────────────────────────
MAN = [(21505, u"第八章案例二十一"), (21506, u"第八章案例二十一"), (21553, u"第八章案例十六"),
       (21586, u"第八章案例二十二"), (21597, u"第八章案例二十七")]
for i, tgt in MAN:
    l = L[i - 1]
    if not l.startswith(u"| **第七章案例九**"):
        nrep.append(u"甲 L%d 非破損列，越界不改" % i)
        continue
    a = tgt.split(u"案例")[0]
    if tgt not in u"\n".join(L):
        nrep.append(u"甲靶不存在：%s" % tgt)
        continue
    L[i - 1] = u"| **%s**" % tgt + l[len(u"| **第七章案例九**"):]
    print(u"甲 L%-6d → %s" % (i, tgt))

# ── 乙：死鏈「第七章案例N」（單提章號之舊稱）→ 第八章／第九章
#     只換 N > 第七章實有案數者（定義上必為死鏈）；合法者指之是新第七章（三十捨墮），不得動。
tot = bad = kept = 0
UP8 = case_of.get(8, 0)
for i, l in enumerate(L, 1):
    if l.startswith(u"# "):
        continue

    def f(m):
        global tot, bad, kept
        n = cnum(m.group(1))
        if n <= 0:
            bad += 1
            return m.group(0)
        if n <= case_of.get(7, 0):
            kept += 1
            return m.group(0)
        if n <= UP8:
            tot += 1
            return u"第八章案例%s" % cn(n)
        k = n - UP8
        if k <= case_of.get(9, 0):
            tot += 1
            return u"第九章案例%s" % cn(k)
        bad += 1
        nrep.append(u"乙 L%d 第七章案例%s 越界（捨墮 %d・單提 %d・眾學 %d）"
                    % (i, m.group(1), case_of.get(7, 0), UP8, case_of.get(9, 0)))
        return m.group(0)
    L[i - 1] = re.sub(u"第七章案例([一二三四五六七八九十]+)", f, l)
print(u"乙 第七章案例N 換算 %d 處（合法保留 %d・越界 %d）" % (tot, kept, bad))

txt = u"\n".join(L)
txt = txt.replace(u"第七章案例一七度試探", u"第八章案例十四、三十四之訂探")
# ── 丙・丁 ──────────────────────────────────────────────────
for a, b, w in [(u"第十一章第七節第十六款", u"第十六章第七節第十六款", 1),
                (u"第十一章第七節出罪大典", u"第十六章第七節出罪大典", 1),
                (u"第十一章第七節", u"第十六章第七節", 1),
                (u"心識相續轉業見第十一章第六節第五款", u"心識相續轉業見第十六章第六節第五款", 1),
                (u"階次在第十一章第六節第三款、第五款", u"階次在第十六章第六節第三款、第五款", 1),
                (u"附錄六", u"附錄五", 2)]:
    c = txt.count(a)
    if c != w:
        nrep.append(u"丙丁未中：%s 命中 %d（應 %d）" % (a[:18], c, w))
    txt = txt.replace(a, b)

# ── 戊：三表範圍與總數自算 ────────────────────────────────────
SECID = [(u"壹、照破執念：遮止四十五則逐條回查表", u"遮止四十五則", 45),
         (u"貳、開許慈悲：開許二十五則逐條回查表", u"開許二十五則", 25),
         (u"參、群己和合：僧伽三十則逐條回查表", u"僧伽三十則", 30)]
lines = txt.split(u"\n")
idx = {}
for k, l in enumerate(lines):
    for s, _, _ in SECID:
        if l.startswith(u"### " + s):
            idx[s] = k
order = sorted([k for k, l in enumerate(lines) if l.startswith(u"### ")])
bounds, ncount = {}, {}
for s, tag, want in SECID:
    st = idx[s]
    en = min([x for x in order if x > st] + [len(lines)])
    coords = []
    for l in lines[st:en]:
        m = re.match(u"^\| \*\*第([一二三四五六七八九十]+)章案例([一二三四五六七八九十]+)\*\*", l)
        if m:
            coords.append((cnum(m.group(1)), cnum(m.group(2))))
    uniq = sorted(set(coords))
    lo, hi = uniq[0], uniq[-1]
    rng = u"第%s章案例%s～第%s章案例%s" % (cn(lo[0]), cn(lo[1]), cn(hi[0]), cn(hi[1]))
    print(u"戊 %s｜實 %d 列（自稱 %d）｜範圍 %s" % (tag, len(coords), want, rng))
    ncount[s] = len(coords)
    if len(coords) != want:
        nrep.append(u"戊 %s 實 %d 列而自稱 %d" % (tag, len(coords), want))
    bounds[s] = rng
for s, tag, want in SECID:
    j = idx[s]
    head = lines[j]
    new = re.sub(u"（第.+?）$", u"（%s）" % bounds[s], head)
    if new != head:
        print(u"  改題：%s" % new[len(u"### "):][:56])
        lines[j] = new
txt2 = u"\n".join(lines)
m = re.search(u"開許篇（[^）]*）與僧伽篇（[^）]*）共\d+個案例之文獻出處回查表", txt2)
if m:
    n = ncount[SECID[1][0]] + ncount[SECID[2][0]]
    new = u"開許篇（%s）與僧伽篇（%s）共%d則案例之文獻出處回查表" % (
        bounds[SECID[1][0]], bounds[SECID[2][0]], n)
    txt2 = txt2.replace(m.group(0), new)
    print(u"戊 總說 → %s" % new[:88])

print(u"未合帳：%d" % len(nrep))
for x in nrep:
    print(u"  " + x)
io.open(BOOK, "w", encoding="utf-8", newline="\n").write(txt2)
print(u"已落盤")
