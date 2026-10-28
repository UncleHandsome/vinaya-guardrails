# -*- coding: utf-8 -*-
"""第 71 輪・甲：新第十四・十五章合稿之預修刀＋入冊（一檔兩章）。

草稿之形：四次對話之交付件——第十四章分兩片（H1 出二次）、第十五章分兩片（H1 出二次），
          每片皆自帶『---』章界與『## 副標題』與『### 三、核心案例深度解碼（上篇／下篇續）』。
本法：①先併片（去重複之 H1・H2・節題，使案例八則同歸一節）；②再逐款①以『去括注則中』之判定
      自動分派——括注去後即連寫者乃『逐字夹今註』➔歸真（削括注、今註降為款②），
      去括注仍不中者乃本書評語➔降式樣（削 `**「」**` 之自稱逐字形）；③律文欄之序號須與附錄
      該號之律文全等（不合者非削括注即豁免，豁免須列名並記其據）；④簡形・U+30FB・斜體・
      半形斜線諸閘俱先過；⑤圍欄溢框者重鑄；⑥最後以行錨一次入兩章。
用法：python -X utf8 _work/hlfix71.py [--go]
"""
import os as _hp_os, sys as _hp_sys
_hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__))))
import hulan_path as HP
import hashlib
import io
import os
import re
import shutil
import sys

sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.abspath(__file__)))
import _tk
import lane
from _simpdict import MAP as SIMP

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
DRAFT = r"C:\Users\lionc\.qoder\tmp\C--Users-lionc-OneDrive-----------------\attachments\bfc14756-f6f1-4240-bfe7-fba2a0d6f592\3d8aff73-3738-44b6-94d3-49bbe0875fc7.txt"
BOOK = HP.SRC
BAK = HP.bakpath("71a")
GO = u"--go" in sys.argv
PUNC = re.compile(u"[，、；：！？「」『』（）()《》〈〉·．。\\-—…﹑＂\"'*＿　\\s]")
PAT1 = re.compile(u"\\*\\*\\s*「([^「」]+?)」\\s*\\*\\*|「\\s*\\*\\*([^「」]+?)\\*\\*\\s*」")
GLOSS = re.compile(u"（[^（）]*）")


def nm(s):
    return _tk.norm(PUNC.sub(u"", s))


def cw(s):
    return sum(2 if ord(c) > 0x2E80 else 1 for c in s)


U = u"零一二三四五六七八九十"


def cn2int(s):
    if len(s) == 1:
        return U.index(s)
    if s == u"十":
        return 10
    if s.startswith(u"十"):
        return 10 + U.index(s[1])
    if s.endswith(u"十"):
        return U.index(s[0]) * 10
    if len(s) == 3 and s[1] == u"十":
        return U.index(s[0]) * 10 + U.index(s[2])
    if len(s) == 2:
        return U.index(s[0]) * 10 + U.index(s[1])
    raise AssertionError(u"漢字數不认得：%r" % s)


def cn2s(n):
    T = u"〇一二三四五六七八九"
    if n < 10:
        return T[n]
    if n == 10:
        return u"十"
    if n < 20:
        return u"十" + T[n % 10]
    return T[n // 10] + u"十" + (T[n % 10] if n % 10 else u"")


dr_raw = io.open(DRAFT, encoding="utf-8", newline=u"").read()
assert dr_raw.count(u"\r") == dr_raw.count(u"\n") == dr_raw.count(u"\r\n"), u"草稿 CRLF 異常"
D = dr_raw.split(u"\r\n")
assert D[0] == u"---" and D[1] == u"", u"草稿首兩行非『---＋空行』"
N0 = len(D)
print(u"草稿 %d 行・末行『%s』" % (N0, D[-1][:34]))

book_raw0 = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert book_raw0.count(u"\r") == book_raw0.count(u"\n"), u"正本入口 CRLF 已傷"
B0 = book_raw0.split(u"\r\n")
# 附錄：尼一百七十八單提之律文（條文欄序號對勘之法源）
APX, APXLOC = {}, {}
_sec = u""
for l in B0[next(i for i, x in enumerate(B0) if x.startswith(u"# 附錄")):]:
    if l.startswith(u"## "):
        _sec = l[3:]
        continue
    m = re.match(u"^(\\d+)\\. 「(.+?)」　｜書中：(.*)$", l)
    if m and u"一百七十八單提" in _sec:
        APX[int(m.group(1))] = m.group(2)
        APXLOC[int(m.group(1))] = m.group(3)
assert len(APX) == 109, u"附錄尼單提取 %d 行（欲 109）" % len(APX)


def harvest(snip):
    hits = [l for l in B0 if snip in l]
    assert len(hits) == 1, u"迎回錨在正本見 %d 處：%s" % (len(hits), snip[:18])
    return hits[0]


print(u"\n―― 甲・併片與交付殘跡 ――")
TAIL = u"*(全書第14、15章新版重構工程四次對話全數交付完畢！)*"
assert D[-1] == TAIL, u"末行非交付自指尾語：%r" % D[-1][:40]
del D[-4:]                                      # 『空・---・空・尾語』四行（章界另補於入冊處）
print(u"  甲1 削交付自指尾語連其章界（原 L%d..L%d）" % (N0 - 3, N0))
H1 = [i for i, l in enumerate(D) if l.startswith(u"# 第十")]
assert len(H1) == 4 and D[H1[0]].startswith(u"# 第十四章") and D[H1[1]].startswith(u"# 第十四章") \
    and D[H1[2]].startswith(u"# 第十五章") and D[H1[3]].startswith(u"# 第十五章"), \
    u"H1 非兩兩成對：%s" % [D[i][:16] for i in H1]
DUP = [(H1[1], u"第十四章之下片"), (H1[3], u"第十五章之下片")]
for i, who in sorted(DUP, reverse=True):
    assert D[i + 1].startswith(u"## ") and D[i + 2] == u"" and D[i + 3] == u"---", u"%s界甲形異：%r" % (who, D[i + 1:i + 4])
    assert D[i + 5].startswith(u"### 三、 核心案例深度解碼（下篇續）") \
        and D[i + 4] == u"" and D[i + 6] == u"" and D[i + 7] == u"---" and D[i + 8] == u"", \
        u"%s界乙形異：%r" % (who, D[i + 4:i + 9])
    del D[i:i + 9]                              # 去『重題・重副題・界・下篇續節題・界』九行
    print(u"  甲2 併片：%s➔削重複之 H1・H2 與『（下篇續）』節題（原 L%d 起 9 行）" % (who, i + 1))
n = 0
for i, l in enumerate(D):
    if l == u"### 三、 核心案例深度解碼（上篇）":
        D[i] = u"### 三、 核心案例深度解碼"
        n += 1
        print(u"  甲3 去『（上篇）』（L%d，兩片既併，篇名即交付殘跡）" % (i + 1))
assert n == 2, u"上篇節題 %d 枚（欲 2）" % n
sp = [i for i, l in enumerate(D) if re.search(u"第 \\d", l) or re.search(u"\\d 條", l)]
nsp = 0
for i in sp:
    D[i], a = re.subn(u"(第) (\\d)", u"\\1\\2", D[i])
    D[i], b = re.subn(u"(\\d) (條)", u"\\1\\2", D[i])
    nsp += a + b
print(u"  甲4 數字板式歸成例：去空格 %d 枚（涉 %d 行）" % (nsp, len(sp)))
IT = [i for i, l in enumerate(D) if re.search(u"(?<!\\*)\\*[^*\\s][^*]*\\*(?!\\*)", l)
      and not l.startswith(u"* ")]
assert not IT, u"仍有斜體行：%s" % [x + 1 for x in IT]
print(u"  甲5 斜體行：0（交付自指尾語本為全稿唯一斜體，已隨甲1削）")
assert len([i for i, l in enumerate(D) if l.startswith(u"# 第十")]) == 2, u"併片後 H1 非 2"
assert sum(1 for l in D if re.match(u"^## ", l)) == 2, u"H2 非 2（副標題各一）"
print(u"  併片後：H1 2・H2 2・行數 %d→%d" % (N0, len(D)))

print(u"\n―― 乙・案例標題補條目號次（附錄指針與跨章指針皆以條號為法源，標題無號則無錨）――")
CASE = [i for i, l in enumerate(D) if l.startswith(u"#### 案例")]
CHAP15 = next(i for i, l in enumerate(D) if l.startswith(u"# 第十五章"))


def ranges(ns):
    out, s, p = [], None, None
    for n in sorted(ns):
        if p is not None and n == p + 1:
            p = n
            continue
        if s is not None:
            out.append((s, p))
        s = p = n
    if s is not None:
        out.append((s, p))
    return u"、".join(u"%d～%d" % (a, b) if b > a else u"%d" % a for a, b in out)


C2N = {}                                      # (章, 案序) → {條號}
for bi, i in enumerate(CASE):
    z = CASE[bi + 1] if bi + 1 < len(CASE) else len(D)
    ns = set()
    for j in range(i, z):
        m = lane.ROW.match(D[j])
        if m:
            mm = re.search(u"(\\d+)", m.group(1))
            if mm:
                ns.add(int(mm.group(1)))
        for mm in re.finditer(u"\\*\\s*\\*[^*]*（第(\\d{2,3}(?:[、～〜]\\d{2,3})*?)條）：\\*\\*", D[j]):
            for x in re.split(u"[、]", mm.group(1)):
                if u"～" in x or u"〜" in x:
                    a, b = re.split(u"[～〜]", x)
                    ns |= set(range(int(a), int(b) + 1))
                else:
                    ns.add(int(x))
    chp = u"15" if i > CHAP15 else u"14"
    k = cn2int(re.match(u"#### 案例([一二三四五六七八九十]+)：", D[i]).group(1))
    C2N[(chp, k)] = ns
    if u"（第" in D[i]:
        print(u"  L%-4d 標題已帶號次，跳過" % (i + 1))
        continue
    D[i] = re.sub(u"^#### 案例([一二三四五六七八九十]+)：([^—]+)——",
                  lambda m: u"#### 案例%s：%s（第%s條）——" % (m.group(1), m.group(2).rstrip(), ranges(ns)),
                  D[i], count=1)
    assert D[i].startswith(u"#### 案例") and u"（第" in D[i], u"補號失敗 L%d" % (i + 1)
    print(u"  L%-4d %s ➔ %s" % (i + 1, u"第%s章案例%s" % (chp, k), D[i][:86]))

print(u"\n―― 丙・款①之自動分派（去括注即中者歸真・括注移出引號；仍不中者降式樣）――")
RET, DEMO = [], []
for i, l in enumerate(D):
    for m in PAT1.finditer(l):
        s = (m.group(1) or m.group(2))
        frags = [nm(f) for f in re.split(u"……|…", s) if len(nm(f)) >= 4]
        if frags and all(f_ in _tk.VINAYA for f_ in frags):
            continue
        glosses = GLOSS.findall(s)
        stripped = GLOSS.sub(u"", s).strip()
        frags2 = [nm(f) for f in re.split(u"……|…", stripped) if len(nm(f)) >= 4]
        wrapped = [x for x in (u"**「%s」**" % s, u"「**%s**」" % s) if x in D[i]]
        if frags2 and all(f_ in _tk.VINAYA for f_ in frags2) and len(wrapped) == 1:
            w = wrapped[0]
            bold_first = w.startswith(u"**")
            tail = u""
            for g in glosses:
                if g.strip() and nm(g):
                    tail += u"%s" % g
            new = (u"**「%s」**" % stripped if bold_first else u"「**%s**」" % stripped) + tail
            D[i] = D[i].replace(w, new)
            RET.append((i + 1, s[:40], new[:52]))
        else:
            DEMO.append((i + 1, s[:44]))
            D[i] = PAT1.sub(lambda mm: u"「%s」" % (mm.group(1) or mm.group(2)), D[i])
print(u"  歸真（括注移出引號，引號內不留今註）：%d 枚" % len(RET))
for i, a, b in RET:
    print(u"    ◆ L%-4d %s ➔ %s" % (i, a, b))
print(u"  降式樣（本書評語・今語，本非逐字）：%d 枚" % len(DEMO))
for i, a in DEMO:
    print(u"    ◆ L%-4d %s" % (i, a))

def lcp(a, b):
    k = 0
    while k < min(len(a), len(b)) and a[k] == b[k]:
        k += 1
    return k


print(u"\n―― 丁・律文欄之歸真（欄文須即附錄該號之律文・合宣與撮述者一律拆回逐條）――")
# 白名單：正文不用組字碼（全書今 0 處，唯附錄存 2 處），故第156條從通譯作『襯體衣』，並須如實註明。
EXNOTE = {156: u"律文此字作組字碼『[袖-由+宁]髁衣』，正文從通譯作『襯體衣』"}
NRM = {k: nm(v) for k, v in APX.items()}
tiao = lane.rows(D)
lane_rows = sum(1 for i, (lab, b) in tiao.items() if u"條文" in lab and re.search(u"(\\d+)", lab))
assert lane_rows >= 70, u"律文欄僅 %d 行（稿稱 73 行，尺少覆便是空尺）" % lane_rows
fix, ex = [], []
for i in sorted(tiao, reverse=True):
    lab, body = tiao[i]
    mm = re.search(u"(\\d+)", lab)
    if u"條文" not in lab or not mm:
        continue
    n = int(mm.group(1))
    assert n in APX, u"稿L%d 標『第%d條』而附錄無此號" % (i + 1, n)
    cut = GLOSS.sub(u"", body).strip()
    if nm(cut) == NRM[n]:
        if cut != body:                           # 欄內夹今註／釋相者：削出引體，另行为一線
            D[i] = D[i].replace(body, cut)
            for g in GLOSS.findall(body):
                inner = g.strip(u"（）").strip()
                if len(nm(inner)) >= 4:
                    D[i + 1:i + 1] = [u"> （釋：%s）" % inner]
                    print(u"  ◎ L%-4d 第%-3d 欄內之括注削出引體，另行為『（釋：…）』一线" % (i + 1, n))
        continue
    if n in EXNOTE:
        assert u"組字碼" not in cut, u"L%d 已註而仍不合" % (i + 1)
        D[i] = D[i].replace(cut, cut + u"（%s。）" % EXNOTE[n], 1)
        ex.append((i + 1, n))
        continue
    D[i] = re.sub(re.escape(body), APX[n], D[i], count=1)
    fix.append((i + 1, n, body[:42], APX[n][:42]))
print(u"  歸真 %d 行（合宣・撮述者改回本號律文，所攬他號由丁1補行）" % len(fix))
for i, n, a, b in sorted(fix):
    print(u"    ◆ L%-4d 第%-3d｜稿：%s" % (i, n, a))
    print(u"              律：%s" % b)
print(u"  白名單豁免 %d 行（俱列名於 EXNOTE 並加如實註）：%s" % (len(ex), ex))

print(u"\n―― 丁2・每案逐條立欄（標題所攬之號須各有其律文行）――")


def row_no(j):
    m = lane.ROW.match(D[j])
    if not m or u"條文" not in m.group(1):
        return None
    mm = re.search(u"(\\d+)", m.group(1))
    return int(mm.group(1)) if mm else None


CASE2 = [i for i, l in enumerate(D) if l.startswith(u"#### 案例")]
add = 0
for bi in range(len(CASE2) - 1, -1, -1):           # 由末案往前補，插入不動已算之行號
    i, z = CASE2[bi], (CASE2[bi + 1] if bi + 1 < len(CASE2) else len(D))
    mm = re.search(u"（第([0-9～、]+)條）", D[i])
    assert mm, u"L%d 標題無號次" % (i + 1)
    want = set()
    for x in mm.group(1).split(u"、"):
        if u"～" in x:
            a, b = x.split(u"～")
            want |= set(range(int(a), int(b) + 1))
        else:
            want.add(int(x))
    have = {row_no(j) for j in range(i, z) if row_no(j)}
    miss = sorted(want - have)
    if not miss:
        continue
    j = max(x for x in range(i, z) if row_no(x))
    D[j + 1:j + 1] = [u"> **【第%d條 條文】：** %s  " % (k, APX[k]) for k in miss]
    add += len(miss)
    print(u"  L%-4d 補 %d 行：%s" % (i + 1, len(miss), ranges(miss)))
print(u"  共補 %d 行" % add)
tiao = lane.rows(D)
n5 = sum(1 for i, (lab, b) in tiao.items() if u"條文" in lab
         and (lambda mm: bool(mm) and nm(GLOSS.sub(u"", b).strip()) == NRM[int(mm.group(1))])(
             re.search(u"(\\d+)", lab)))
print(u"  律文欄今 %d 行・與附錄該號全等者 %d 行・白名單 %d 行" % (len(tiao), n5, len(ex)))

print(u"\n―― 戊・圍欄之重鑄（舊稿三欄溢框 103／105 格・依八案之號次重排單欄樹）――")
marks = [i for i, l in enumerate(D) if l.startswith(u"```")]
assert len(marks) == 4, u"圍欄標記 %d 枚（欲 4＝兩段）" % len(marks)
for k in (1, 0):
    chp, ttl = ((u"15", u"【第十五章 比丘尼不共單提：生計、風控與法治】") if k
                else (u"14", u"【第十四章 比丘尼不共單提：身軀、空間與共住】"))
    a, b = marks[2 * k], marks[2 * k + 1]
    ks = sorted(x for (c, x) in C2N if c == chp)
    body = [ttl]
    for j, x in enumerate(ks):
        body.append(u"%s 案%s｜第%s條" % (u"└─" if j == len(ks) - 1 else u"├─",
                                          cn2s(x), ranges(C2N[(chp, x)])))
    old_w = max(cw(t) for t in D[a + 1:b])
    new_w = max(cw(t) for t in body)
    assert new_w <= 72, u"第%s章新圍欄仍寬 %d 格" % (chp, new_w)
    D[a + 1:b] = body
    print(u"  第%s章圍欄：%d 行・%d 格 ➔ %d 行・%d 格" % (chp, b - a - 1, old_w, len(body), new_w))

print(u"\n―― 己・八案未及別解之條目（登號於款題，附錄之『書中』指針始有錨）――")
anchored = set()
for ns in C2N.values():
    anchored |= ns
orph = sorted(set(APX) - anchored)
print(u"  新稿八案未及之條目：%d 枚 %s" % (len(orph), orph))
HOME = {}                                       # 條號 → 章（14/15）：以其舊落點之章次定之
for k in orph:
    m = re.match(u"^第十([四五])章", APXLOC[k])
    assert m, u"第%d條舊落點不明：%r" % (k, APXLOC[k])
    HOME[k] = u"14" if m.group(1) == u"四" else u"15"
print(u"  歸章（以舊落點定）：第十四章 %s｜第十五章 %s" % (
    ranges(sorted(k for k in HOME if HOME[k] == u"14")), ranges(sorted(k for k in HOME if HOME[k] == u"15"))))
for chp in (u"15", u"14"):
    ns = sorted(k for k in orph if HOME[k] == chp)
    if not ns:
        continue
    h = next(i for i, l in enumerate(D) if l.startswith(u"# 第十%s章" % (u"四" if chp == u"14" else u"五")))
    z = next(i for i in range(h, len(D)) if D[i].startswith(u"### 二、"))
    zz = next(i for i in range(z + 1, len(D)) if D[i].startswith(u"### "))
    kids = [i for i in range(z, zz) if D[i].startswith(u"#### ")]
    if kids:
        nxt = max(cn2int(re.match(u"#### （([一二三四五六七八九十]+)）", D[i]).group(1)) for i in kids) + 1
        j = kids[-1]
        while j + 1 < zz and not D[j + 1].startswith(u"#### ") and D[j + 1].strip():
            j += 1
    else:                                       # 本節原無款行（新稿之矩陣只有一段圍欄）：加為第一款
        nxt = 1
        j = zz - 1
        while j > z and not D[j].strip():
            j -= 1
    ins = [u"", u"#### （%s） 案外之條目（第%s條）" % (cn2s(nxt), ranges(ns)), u"",
           u"上列諸條，律中各別起結戒、自有因緣，非如第十三章那十八條之連誦無說；唯本書新編以板塊重組，"
           u"此數條未獲別立案例，今但依戒本之次登其號，並錄其結戒之宣說，俾檢閱者得自查焉。", u""]
    for x, k in enumerate(ns):
        ins.insert(4 + 2 * x, u"* %s、**「%s」**" % (cn2s(x + 1), APX[k].rstrip(u'」')))
    D[j + 1:j + 1] = ins
    print(u"  第%s章 §二 添（%s）款：第%s條（插在 L%d 之後，%d 行）" % (
        chp, cn2s(nxt), ranges(ns), j + 1, len(ins)))

print(u"\n―― 庚・自證諸閘（寫檔前必過）――")
tiao = lane.rows(D)                             # 行號須於諸插入・重鑄之後重算（戊己皆動過行）
txt = u"\r\n".join(D)
bad = []
for i, l in enumerate(D):
    cands = [m.group(1) or m.group(2) for m in PAT1.finditer(l)]
    if i in tiao:
        mm = re.search(u"(\\d+)", tiao[i][0])
        if not (mm and int(mm.group(1)) in EXNOTE):        # 白名單之形制已列名於丁，不重核於此
            cands.append(tiao[i][1])
    for s in cands:
        for frag in re.split(u"……|…", s.strip()):
            nb = nm(frag)
            if len(nb) >= 4 and nb not in _tk.VINAYA:
                bad.append((i + 1, frag[:44]))
print(u"  逐字閘：無據 %d 枚" % len(bad))
for i, f in bad:
    print(u"    × L%-4d %s" % (i, f))
assert not bad, u"逐字閘未過"
CORPF = set(_tk.VINAYA)
lsp, lnn = lane.spans(txt)
simp = []
for i, l in enumerate(D):
    ex = [(m.start(), m.end()) for m in re.finditer(u"「[^」]*」", l)]
    ex += [(m.start(), m.end()) for m in re.finditer(u"\\[[^\\]\\n]{1,14}\\]", l)]   # CBETA 組字碼
    if i in tiao and nm(tiao[i][1]) in _tk.VINAYA:
        b = l.index(tiao[i][1])
        ex.append((b, b + len(tiao[i][1])))
    for ch in SIMP:
        for m in re.finditer(re.escape(ch), l):
            if ch in CORPF and any(a_ <= m.start() < b_ for a_, b_ in ex):
                continue
            simp.append((ch, i + 1, l[max(0, m.start() - 10):m.start() + 10]))
print(u"  簡形（律文欄經對勘者得保）：%d 枚・律文欄保護區管 %d 段" % (len(simp), lnn))
for ch, i, ctx in simp:
    print(u"    × L%-4d 『%s』%s" % (i, ch, ctx))
assert not simp, u"簡形殘留"
assert u"・" not in txt, u"稿內有 U+30FB『・』"
sl = [(i + 1, l[:70]) for i, l in enumerate(D) if u"/" in l and not l.startswith(u"```")]
print(u"  半形斜線：%d 行 %s" % (len(sl), sl[:3]))
assert not sl, u"有半形斜線"
NC = {}
for i, l in enumerate(D):
    if l.startswith(u"# 第十四章"):
        NC[u"14"] = 0
    if l.startswith(u"# 第十五章"):
        NC[u"15"] = 0
    if l.startswith(u"#### 案例") and NC:
        NC[max(NC)] += 1
assert sum(1 for l in D if l.startswith(u"# 第十")) == 2 and NC == {u"14": 8, u"15": 8}, u"形制：%r" % NC
print(u"  形制：兩章 H1・案例 8＋8・行數 %d→%d" % (N0, len(D)))
for snip in [u"第七章案例", u"第十三章案例", u"第十二章", u"本律無文", u"失考"]:
    print(u"    指針／考訂『%s』：%s" % (snip, [i + 1 for i, l in enumerate(D) if snip in l][:9]))

if not GO:
    print(u"\n（乾跑：加 --go 始入冊）")
    sys.exit(0)
print(u"\n―― 辛・入冊（一次換兩章）――")
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert raw.count(u"\r") == raw.count(u"\n") == raw.count(u"\r\n"), u"正本入口 CRLF 已傷"
L = raw.split(u"\r\n")
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()
i14 = next(i for i, l in enumerate(L) if l.startswith(u"# 第十四章"))
i15 = next(i for i, l in enumerate(L) if l.startswith(u"# 第十五章"))
i16 = next(i for i, l in enumerate(L) if l.startswith(u"# 第十六章"))
for x, y in ((i14, i15), (i15, i16)):
    assert L[x - 1] == u"" and L[x - 2] == u"---", u"章界非『---＋空行』@L%d" % x
p15 = next(i for i, l in enumerate(D) if l.startswith(u"# 第十五章"))
B14, B15 = D[2:p15], D[p15:]
for b in (B14, B15):
    b += [u"", u"---"]
NEWL = L[:i14] + B14 + L[i15 - 1:i15] + B15 + L[i16 - 1:]
print(u"  舊第十四章 %d 行→%d 行｜舊第十五章 %d 行→%d 行｜全書 %d→%d 行" % (
    i15 - i14, len(B14), i16 - i15, len(B15), len(L), len(NEWL)))
out = u"\r\n".join(NEWL)
assert out.count(u"\r") == out.count(u"\n") == len(NEWL) - 1, u"CRLF 變形"
assert not os.path.exists(BAK) or io.open(BAK, encoding="utf-8", newline=u"").read() == raw, u"備份不同本"
if not os.path.exists(BAK):
    shutil.copy2(BOOK, BAK)
for tries in range(3):
    try:
        with open(BOOK, "wb") as fh:
            fh.write(out.encode("utf-8"))
        break
    except OSError as e:
        print(u"  ! 寫檔失敗（%s）第 %d 次重試" % (e.strerror, tries + 1))
        import time
        time.sleep(2)
else:
    raise SystemExit(u"寫正本三次不成")
chk = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert chk == out, u"回讀不符"
back = chk.split(u"\r\n")
j14 = next(i for i, l in enumerate(back) if l.startswith(u"# 第十四章"))
j15 = next(i for i, l in enumerate(back) if l.startswith(u"# 第十五章"))
j16 = next(i for i, l in enumerate(back) if l.startswith(u"# 第十六章"))
assert back[j14:j14 + len(B14)] == B14 and back[j15:j15 + len(B15)] == B15, u"回讀块體不等"
print(u"  已寫檔｜sha %s→%s｜備份 %s" % (sha0[:12], hashlib.sha256(chk.encode("utf-8")).hexdigest()[:12],
                                        os.path.basename(BAK)))
print(u"  全書 %d 行｜案例 %d 則｜H1 %d 個｜圍欄 %d 段" % (
    len(back), sum(1 for l in back if re.match(u"^#### (?:★ )?案例", l)),
    sum(1 for l in back if re.match(u"^# 第[一二三四五六七八九十]+章", l)),
    sum(1 for l in back if l == u"```") // 2))
