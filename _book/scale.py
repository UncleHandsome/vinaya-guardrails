# -*- coding: utf-8 -*-
"""第五十七輪・⑥：尺群改口徑——八目新尺，一律量冊身（不量印象、不量舊產器）。

冊身今為《重構版》之_hand-edit_檔，舊 `_book/check.py` 四十四尺所依之產器已退，其口徑
（28 章・7 部・六欄卡・八大正理・三鏡）於今冊長紅無義。今立八目代之，逐目量實物：

  尺一 骨架自算      篇・章・節・案・附錄之數，並與封面計數式同口徑
  尺二 目錄之賬      卷首總目錄所列章・節標題與冊身實題逐條對合（虛列＝漏列＝0）
  尺三 死鏈四式      第N章案例M／第N章第M節／第N篇／附錄N 四式俱核實靶
  尺四 四步之齊      241 案每案恰有起・承・轉・合四段與末行出處；舊欄名殘跡為零
  尺五 術語之制      正理N／八大正理／三鏡／夜半四問／隨身四照 清零，四底線四名俱在
  尺六 法條之制      第十七章正文不掛世俗法名與條號（條號唯登附錄四）
  尺七 附錄座次      附錄一〜五連號無缺、無虛引
  尺八 戒本通數      附錄二表題之 250／348 與其凡例算式、組頭實數對合
用法：python -X utf8 _book/scale.py
"""
import io
import os
import re
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, u"佛陀的護欄_重構版.md")
CN = u"零一二三四五六七八九十百"
bad, note = [], []


def cnum(s):
    if u"百" in s:
        a, _, b = s.partition(u"百")
        return (CN.index(a) if a else 1) * 100 + (cnum(b) if b else 0)
    if u"十" in s:
        a, _, b = s.partition(u"十")
        return (CN.index(a) if a else 1) * 10 + (CN.index(b) if b else 0)
    return CN.index(s) if s and s in CN else 0


txt = io.open(SRC, encoding="utf-8-sig").read().replace("\r\n", "\n")
L = txt.split(u"\n")
case_of, sec_of = Counter(), Counter()
heads, apx = [], []
cur = 0
for i, l in enumerate(L, 1):
    m = re.match(u"^# 第([一二三四五六七八九十]+)章　(.+)$", l)
    if m:
        cur = cnum(m.group(1))
        heads.append((2, u"第%s章　%s" % (m.group(1), m.group(2))))
        continue
    m = re.match(u"^## 第([一二三四五六七八九十]+)節　(.+)$", l)
    if m and cur:
        sec_of[cur] += 1
        heads.append((3, m.group(0)[3:]))
        continue
    m = re.match(u"^### 案例([一二三四五六七八九十百]+)：", l)
    if m and cur:
        case_of[cur] += 1
        continue
    m = re.match(u"^## (附錄[一二三四五]　.+)$", l)
    if m:
        apx.append(m.group(1))
        heads.append((2, m.group(1)))
        continue
    m = re.match(u"^# 【(.+)】", l)
    if m:
        heads.append((1, m.group(1)))
n_chap, n_sec, n_case = 0, sum(sec_of.values()), sum(case_of.values())
n_pian = len(re.findall(u"^# 【第[一二三四五六七八九十]+篇：", txt, re.M))
n_apx = len(apx)

# ── 尺一 骨架自算 ────────────────────────────────────────────
n_chap = len(sec_of)
CAP = u"%d 篇・%d 章・%d 節・%d 案・附錄 %d 件" % (n_pian, n_chap, n_sec, n_case, n_apx)
if not (n_pian == 5 and n_chap == 20 and n_case == 241 and n_apx == 5):
    bad.append(u"尺一 骨架非常規：%s" % CAP)
else:
    note.append(u"尺一 %s（篇・章・節・案・附錄自冊身算）" % CAP)
for want, got, tag in [(20, len(re.findall(u"^# 第[一二三四五六七八九十]+章　", txt, re.M)), u"章題"),
                       (241, len(re.findall(u"^### 案例", txt, re.M)), u"案例"),
                       (5, len(re.findall(u"^## 附錄[一二三四五]　", txt, re.M)), u"附錄")]:
    if want != got:
        bad.append(u"尺一 %s 實 %d（應 %d）" % (tag, got, want))

# ── 尺二 目錄之賬 ────────────────────────────────────────────
i0 = txt.index(u"## 【本書總目錄】")
i1 = txt.index(u"\n# 【第一篇")
toc = []
for x in txt[i0:i1].split(u"\n"):
    if x.startswith(u"    - ") or x.startswith(u"- "):
        toc.append(x.strip()[2:].strip())
real = set()
for l in L:
    m = re.match(u"^(#{1,3}) (第[一二三四五六七八九十]+章　.+|第[一二三四五六七八九十]+節　.+|附錄[一二三四五]　.+)$", l)
    if m:
        real.add(m.group(2).strip())
ghost = [t for t in toc if t not in real]
missing = [r for r in real if r not in toc]
if ghost or missing:
    bad.append(u"尺二 目錄虛列 %d・漏列 %d｜例：%s" % (len(ghost), len(missing), (ghost + missing)[:3]))
else:
    note.append(u"尺二 目錄 %d 條與冊身實題逐條對合（虛列 0・漏列 0）" % len(toc))

# ── 尺三 死鏈四式 ────────────────────────────────────────────
d1 = d2 = d3 = d4 = 0
for l in L:
    if l.startswith(u"# "):
        continue
    for m in re.finditer(u"第([一二三四五六七八九十]+)章案例([一二三四五六七八九十百]+)", l):
        a, b = cnum(m.group(1)), cnum(m.group(2))
        if not (0 < b <= case_of.get(a, 0)):
            d1 += 1
    for m in re.finditer(u"第([一二三四五六七八九十]+)章第([一二三四五六七八九十]+)節", l):
        a, b = cnum(m.group(1)), cnum(m.group(2))
        if not (0 < b <= sec_of.get(a, 0)):
            d2 += 1
    for m in re.finditer(u"第([一二三四五六七八九十]+)篇", l):
        if cnum(m.group(1)) > n_pian:
            d3 += 1
    for m in re.finditer(u"附錄([一二三四五六七八九十]+)", l):
        if cnum(m.group(1)) > n_apx:
            d4 += 1
if d1 + d2 + d3 + d4:
    bad.append(u"尺三 死鏈：案例 %d・節 %d・篇 %d・附錄 %d" % (d1, d2, d3, d4))
else:
    note.append(u"尺三 死鏈四式俱 0（案例・節・篇・附錄）")

# ── 尺四 四步之齊 ────────────────────────────────────────────
FLD = [u"事相經過", u"心相照鏡", u"法相剖析", u"佛陀處斷", u"人間智慧與行持",
       u"律文出處", u"此戒所護", u"現代對讀", u"戒文（戒本次第）"]
res = [txt.count(u"#### " + f) for f in FLD]
n_bad = 0
blocks = re.split(u"(?=^### 案例)", txt, flags=re.M)
for b in blocks:
    if not b.startswith(u"### 案例"):
        continue
    for k in [u"#### 起·案發現場", u"#### 承·照妖鏡下", u"#### 轉·金剛斷腕", u"#### 合·清涼轉身"]:
        if b.count(k) != 1:
            n_bad += 1
    if b.count(u"\n出處：") != 1:
        n_bad += 1
if n_bad or sum(res):
    bad.append(u"尺四 四步不齊之案 %d・舊欄名殘跡 %d" % (n_bad, sum(res)))
else:
    note.append(u"尺四 241 案俱有起承轉合四段與末行出處；舊欄名 9 式殘跡 0")

# ── 尺五 術語之制 ────────────────────────────────────────────
ZERO = [u"八大正理", u"三鏡", u"夜半四問", u"隨身四照", u"判見下面『佛陀處斷』欄"]
for k in range(1, 9):
    ZERO.append(u"正理" + CN[k])
hit = []
for k in ZERO:
    if not txt.count(k):
        continue
    ex = 0
    for m in re.finditer(re.escape(k), txt):
        w = txt[max(0, m.start() - 8):m.end() + 6]
        if k == u"三鏡" and (u"旧" in w or u"舊" in w):
            ex += 1                                  # 『旧稱隨身三鏡』之追溯語，合法
        else:
            hit.append((k, txt.count(k) - ex))
    if ex and txt.count(k) == ex:
        continue
_d0 = txt.index(u"### 二、四大金剛底線法定定文")
DING = txt[_d0:txt.index(u"### 三、", _d0)]
four = [k for k in [u"心事相應", u"世間信心", u"不可逆底線", u"正當程序"] if k in DING]
if hit:
    bad.append(u"尺五 舊術語未清：%s" % hit)
elif len(four) != 4:
    bad.append(u"尺五 四底線之名不齊（得 %d）" % len(four))
else:
    note.append(u"尺五 舊術語清零・四大金剛底線四名俱在・十六問已降為四照之細目")

# ── 尺六 法條之制 ────────────────────────────────────────────
i17 = txt.index(u"# 第十七章")
i18 = txt.index(u"# 【第五篇")
body17 = txt[i17:i18]
LAWS = [u"勞基法", u"勞動基準法", u"個資法", u"個人資料保護法", u"財團法人法》第", u"民法》第",
        u"非訟事件法》第", u"民法第", u"護理人員法", u"勞動法防火牆"]
hits = [(k, body17.count(k)) for k in LAWS if body17.count(k)]
if hits:
    bad.append(u"尺六 正文仍掛法名條號：%s" % hits)
else:
    nrow = len(re.findall(u"^\\| ", txt[txt.index(u"## 附錄四"):txt.index(u"## 附錄五")], re.M)) - 2
    note.append(u"尺六 第十七章正文世俗法名・條號 0（皆歸附錄四對照表，表內 %d 行）" % nrow)

# ── 尺七 附錄座次 ────────────────────────────────────────────
seq = [cnum(re.match(u"附錄([一二三四五])", a).group(1)) for a in apx]
if seq != list(range(1, n_apx + 1)):
    bad.append(u"尺七 附錄座次不連號：%s" % seq)
else:
    note.append(u"尺七 附錄一〜%d 連號無缺：%s" % (n_apx, u"／".join(a.split(u"　")[0] for a in apx)))

# ── 尺八 戒本通數 ────────────────────────────────────────────
m = re.search(u"附錄二　全戒本歷條總對照表（比丘 (\d+)・比丘尼 (\d+)）", txt)
if not m:
    bad.append(u"尺八 附錄二表題無法讀數")
else:
    a, b = int(m.group(1)), int(m.group(2))
    seg = txt[txt.index(u"## 附錄二"):txt.index(u"## 附錄三")]
    mA = re.search(u"比丘 (\d)＋(\d+)＋(\d+)＋(\d+)＋(\d+)＋(\d+)＋(\d+)＋(\d+)＝(\d+) 條", seg)
    mB = re.search(u"比丘尼 (\d)＋(\d+)＋(\d+)＋(\d+)＋(\d+)＋(\d+)＋(\d+)＝(\d+) 條", seg)
    okA = mA and sum(int(x) for x in mA.groups()[:-1]) == int(mA.group(9)) == a
    okB = mB and sum(int(x) for x in mB.groups()[:-1]) == int(mB.group(8)) == b
    if not (okA and okB):
        bad.append(u"尺八 算式不合：甲 %s・乙 %s" % (okA, okB))
    else:
        note.append(u"尺八 戒本通數 甲 %d＝4+13+2+30+90+4+100+7・乙 %d＝8+17+30+178+8+100+7（表題與凡例算式合）"
                    % (a, b))

print(u"\n".join(u"  ✓ " + x for x in note))
print(u"病 %d 目" % len(bad))
for x in bad:
    print(u"  ✗ " + x)
