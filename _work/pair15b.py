# -*- coding: utf-8 -*-
"""第十五波・F2 之刀（丁3・甲3・戊1 之定名）。

丁3：除正文首頁之 H3 副標題（兩冊副標俱存於封面・扉頁・書訊元數據）。
甲3：【制度案卷 104】整卡自第十六章遷入第十五章新立之第四節；十五章章名歸一；
     十六章章名如實呈（今檔已合裁決之文，不改）；凡例第八律之章次同步歸實。
戊1：第二十章第一・二節依裁決算名定名（檢綱與四署宣告俱已在冊——本刀只辦『定名』，
     並補卷首【三級收納】查考級之稱名）。
"""
import hashlib
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "_work"))
import pairsimp                                       # noqa: E402

BOOK = next(os.path.join(ROOT, x) for x in os.listdir(ROOT)
            if x.startswith(u"如法推尋") and x.endswith(u".txt"))
BK = os.path.join(ROOT, "_archive", u"備份", u"AI清理前", os.path.basename(BOOK) + ".pre_a15b")
LF, CRLF = chr(10), chr(13) + chr(10)


def raw():
    return io.open(BOOK, "rb").read().decode("utf-8-sig")


def one(L, pat, tag, want=1):
    idx = [i for i, l in enumerate(L) if pat(l)]
    if len(idx) != want:
        raise SystemExit(u"%s 之錨非 %d 見（實 %d 見）" % (tag, want, len(idx)))
    return idx


def k_d3(L):
    """丁3：除冊首之 H3 副標連同其後一空行。"""
    i = one(L, lambda l: l.startswith(u"### ——出世自治公法"), u"丁3·副標")
    if L[i[0] + 1].strip():
        raise SystemExit(u"丁3：副標之後非空行，形制與料不合，須查")
    print(u"  丁3 除副標 L%d–L%d：%s" % (i[0] + 1, i[0] + 2, L[i[0]][:40]))
    return L[:i[0]] + L[i[0] + 2:], 1


def k_jia3(L):
    """甲3：章名歸一・卡之遷徙・凡例第八律同步。"""
    n = 0
    old15 = u"### 第十五章　分際之護：默擯之界與惡性別眾之正命"
    new15 = u"### 第十五章　分際之護：默擯之界、惡性別眾與淨人作務"
    if any(l.strip() == old15 for l in L):
        i = one(L, lambda l: l.strip() == old15, u"甲3·十五章題")[0]
        L[i] = new15
        print(u"  甲3 十五章改題 L%d：%s" % (i + 1, new15[4:]))
        n += 1
    else:
        print(u"  甲3 十五章題已在帳（或錨已老，須核）")
    t16 = [l for l in L if l.startswith(u"### 第十六章")]
    want16 = u"### 第十六章　十方僧物不可分割與瞻病護念：四種僧物、名實之辨與照護次第"
    print(u"  甲3 十六章題今作『%s』・裁決之文%s現檔 ➔ %s"
          % (t16[0][4:24], u"已合" if t16 and t16[0].strip() == want16 else u"不合",
             u"不改（如實呈）" if t16[0].strip() == want16 else u"須改"))

    # ── 遷 104 卡 ──
    a = one(L, lambda l: l.startswith(u"### 【制度案卷 104】"), u"甲3·104 卡首")[0]
    b = one(L, lambda l: l.startswith(u"### 【制度案卷 105】"), u"甲3·105 卡首")[0]
    if b < a:
        raise SystemExit(u"甲3：105 之座次在 104 之前，與料不合")
    card = L[a:b]
    # 卡尾之空行不帶走（留在原處），遷入處另補空行
    while card and not card[-1].strip():
        card = card[:-1]
    rest = L[:a] + L[b:]
    j = one(rest, lambda l: l.startswith(u"### 第十六章"), u"甲3·十六章題（遷入之界）")[0]
    tail = rest[:j]
    while tail and not tail[-1].strip():
        tail = tail[:-1]
    lead = [
        u"",
        u"### 第四節　出坡作務之界與淨人外護體制",
        u"",
        u"道場之有作務，如人之有四肢：耕畦、刈草、修舍、炊爨，皆色身住世所不可免。"
        u"律制沙門不掘地、不營商、不自營，卻不令人無瓦可覆、無飯可食——"
        u"所立者乃**分際**：僧主法，淨人主事，外護主緣；三者之界一糊，"
        u"常住之物權與沙門之正命俱遭其害。本節以【制度案卷 104】畢陵伽婆蹉受五百守園人之案，"
        u"立淨人外護之制與出坡作務之界——此即『分際之護』一章所以兼收作務之義。",
        u"",
    ]
    out = tail + lead + card + [u""] + rest[j:]
    print(u"  甲3 遷 104 卡：%d 行自十六章 L%d 移入十五章新第四節（十六章之卡 %d ➔ %d）"
          % (len(card), a + 1, 3, 2))
    n += 1

    # ── 凡例第八律：章次歸實 ──
    old8 = u"又本冊第十六章今新立三案"
    i8 = [i for i, l in enumerate(out) if old8 in l]
    if i8:
        k = i8[0]
        pre = u"又本冊第十六章今新立三案——【制度案卷 103】亡僧遺物分流・【104】畢陵伽婆蹉受五百守園人・【105】瞻病次第差"
        pos = u"又本冊第四篇今新立三案——第十五章第四節立【制度案卷 104】畢陵伽婆蹉受五百守園人・第十六章立【制度案卷 103】亡僧遺物分流與【105】瞻病次第差"
        if pre in out[k]:
            out[k] = out[k].replace(pre, pos)
            print(u"  甲3 凡例第八律章次歸實 L%d（十六→十五・四・十六兩章如實分寫）" % (k + 1))
            n += 1
        elif pos in out[k]:
            print(u"  甲3 凡例第八律已在帳")
        else:
            raise SystemExit(u"凡例第八律之句與料不合，須核：%s" % out[k][40:110])
    else:
        print(u"  甲3 凡例第八律無『第十六章今新立三案』之語（他本？須核）")
    return out, n


def kWu1(L):
    """戊1：二十章兩節之定名・三級收納查考級之稱名補行。"""
    n = 0
    pairs = [
        (u"### 第一節　開庭四階十六項檢綱（軌道甲·公堂對勘之目）",
         u"### 第一節　執事開庭十六項一票否決檢綱（軌道甲·公堂對勘之目）", u"戊1·檢綱定名"),
        (u"### 第二節　自然人心證自律宣告（四署之制）",
         u"### 第二節　四署心證自律宣告式（自然人心證之制）", u"戊1·宣告定名"),
    ]
    for old, new, tag in pairs:
        i = [k for k, l in enumerate(L) if l.strip() == old]
        if len(i) == 1:
            L[i[0]] = new
            print(u"  %s L%d ➔ %s" % (tag, i[0] + 1, new[4:34]))
            n += 1
        elif any(new.strip() == l.strip() for l in L):
            print(u"  %s 已在帳" % tag)
        else:
            raise SystemExit(u"%s 之錨非唯一（%d 見）" % (tag, len(i)))
    # 查考級之稱名補行（圍欄內之等寬行・以本柵之縮排為準）
    key = u"第三級【查考】"
    i = one(L, lambda l: key in l, u"戊1·查考級")
    ind = L[i[0]][:len(L[i[0]]) - len(L[i[0]].lstrip())]
    cont = [k for k in range(i[0], i[0] + 4)
            if L[k].strip().startswith(u"・") and len(L[k]) - len(L[k].lstrip()) > len(ind)]
    if not cont:
        raise SystemExit(u"戊1：查考級之續行求不得，須核")
    line = L[cont[-1]]
    if u"開庭十六項檢綱" in line:
        print(u"  戊1 查考級已載檢綱之稱名")
    else:
        L[cont[-1]] = line + u"・開庭十六項檢綱與四署宣告"
        print(u"  戊1 查考級補稱名 L%d（+%d 格・仍柵內最長者之比較如下）"
              % (cont[-1] + 1, len(u"・開庭十六項檢綱與四署宣告")))
        n += 1
    def cells(x):
        return sum(2 if ord(c) > 0x2000 else 1 for c in x)
    blk = [x for x in L[i[0] - 6:i[0] + 5] if x.strip()]
    print(u"  戊1 三級收納柵內最大格寬 ➔ %d（自量・非宣稱：真閾在 refit 與 pairface）"
          % max(cells(x) for x in blk))
    return L, n


ALLOW = (u"text", u"markdown", u"Vinaya", u"SOP", u"NPO", u"pdf", u"docx")


def gate(L, fresh=None):
    for i, l in enumerate(L, 1):
        h = pairsimp.hits(l)
        if h:
            raise SystemExit(u"簡形之閘未過 L%d「%s」" % (i, h))
    for i, l in enumerate(fresh or L, 1):
        for m in re.finditer(r"[A-Za-z]{4,}", l):
            if m.group(0) not in ALLOW:
                raise SystemExit(u"夾英文之閘未過（新撰之行）➔%s｜%s" % (m.group(0), l[:40]))


def main():
    go = "--write" in sys.argv
    before = raw()
    sha = hashlib.sha256(before.encode("utf-8")).hexdigest()[:12]
    L = before.replace(CRLF, LF).split(LF)
    print(u"F2 %s・%d 行・SHA %s" % (os.path.basename(BOOK)[:14], len(L), sha))
    n0 = len(L)
    L, a = k_d3(L)
    L, b = k_jia3(L)
    L, c = kWu1(L)
    seen = set(before.replace(CRLF, LF).split(LF))
    fresh = [l for l in L if l.strip() and l not in seen]      # 新撰之行（遷卡者舊行不入）
    gate(L, fresh)
    print(u"  合計 %d 刀・行 %d ➔ %d" % (a + b + c, n0, len(L)))
    if not go:
        print(u"（試跑・加 --write 始落盤）")
        return 0
    if not os.path.isdir(os.path.dirname(BK)):
        os.makedirs(os.path.dirname(BK))
    io.open(BK, "wb").write(before.encode("utf-8"))
    nl = CRLF if CRLF in before else LF
    out = nl.join(L).encode("utf-8")
    io.open(BOOK, "wb").write(out)
    chk = io.open(BOOK, "rb").read().decode("utf-8")
    if chk.count(chr(13)) != chk.count(chr(10)):
        raise SystemExit(u"行尾混雜（CR %d ≠ LF %d）——即 286 輪舊案，須修"
                         % (chk.count(chr(13)), chk.count(chr(10))))
    print(u"  落盤：%d 行・%d B・行尾 %s・SHA %s ➔ %s・備 %s"
          % (len(L), len(out), u"CRLF" if nl == CRLF else u"LF", sha,
             hashlib.sha256(out).hexdigest()[:12], os.path.relpath(BK, ROOT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
