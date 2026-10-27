# -*- coding: utf-8 -*-
"""第十五波・F1 之刀（甲2①・甲2②・乙3）。

奉終審裁決令：
  甲2① F1 第十一章第三節 → 第一人稱自救觀心版（作者給定之文，式樣依凡例歸真）
  甲2② F1 第一章第三節 → 改題『問心之兩徑：心事相應之自察與表業顯影之印證』
  乙3  三段式樣待查 → 逐字者補齊出處（並就地歸真）、撮述與異譯者降『』

四閘前置：唯一錨・重入之護・簡形之掃・逐字之驗（「…」須見形於本地語料且出處在同線左側）。
試跑印名，`--write` 始落盤；落盤前備 `.pre_a15a` 於 `_archive/備份/AI清理前/`。
"""
import hashlib
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "_work"))
import _tk                                            # noqa: E402
import pairsimp                                       # noqa: E402

BOOK = next(os.path.join(ROOT, x) for x in os.listdir(ROOT)
            if x.startswith(u"起心動念") and x.endswith(u".txt"))
BK = os.path.join(ROOT, "_archive", u"備份", u"AI清理前", os.path.basename(BOOK) + ".pre_a15a")
LF = chr(10)
CRLF = chr(13) + LF
QUOTE = chr(0x300C)          # 「
ENDQ = chr(0x300D)           # 」
SRC = u"本地|卷段|之檔|《|大正藏|律作|原典|本律"


def raw():
    """位元組直讀：文字模式之 `io.open` 會把 CRLF 折成 LF（幽靈改檔之源），故取 bytes。"""
    return io.open(BOOK, "rb").read().decode("utf-8-sig")


CORPUS = _tk.norm(_tk.VINAYA) + u"".join(_tk.norm(v) for v in _tk.OTHER.values())


def verbatim_chk(text, tag):
    """「…」＝逐字之宣稱：須 ① 見形於本地語料 ② 同線左側四十六字內帶出處。違者擲。"""
    bad = []
    for line in text.split(LF):
        for m in re.finditer(QUOTE + u"[^" + ENDQ + u"]{4,}" + ENDQ, line):
            body = _tk.norm(m.group(0)[1:-1])
            left = line[max(0, m.start() - 46):m.start()]
            where = []
            if body not in CORPUS:
                where.append(u"語料無形")
            if not re.search(SRC, left):
                where.append(u"左無出處")
            if where:
                bad.append(u"%s｜%s｜%s" % (tag, m.group(0)[:34], u"・".join(where)))
    if bad:
        raise SystemExit(u"逐字之閘未過（不掛逐字之式樣）：\n      " + (LF + u"      ").join(bad))
    return len(re.findall(QUOTE + u"[^" + ENDQ + u"]{4,}" + ENDQ, text))


def simp_chk(lines, tag):
    for i, l in enumerate(lines, 1):
        h = pairsimp.hits(l)
        if h:
            raise SystemExit(u"簡形之閘未過：%s 第 %d 行「%s」➔%s" % (tag, i, h, l[:44]))


def latin_chk(lines, tag, allow=("text",)):
    for i, l in enumerate(lines, 1):
        for m in re.finditer(r"[A-Za-z]{2,}", l):
            if m.group(0) not in allow:
                raise SystemExit(u"夾英文之閘未過：%s L%d ➔%s" % (tag, i, m.group(0)))


# ── 刀目 ────────────────────────────────────────────────────────────────
def k_jia2b(L):
    """甲2②：第一章第三節改題。"""
    old = (u"### 第三節" + u"　審理主幹的二分法相：言詞問與證據問的二諦統一")
    new = (u"### 第三節　問心之兩徑：心事相應之自察與表業顯影之印證")
    if new in L:
        print(u"  甲2② 已在帳（重入之護）")
        return L, 0
    n = sum(1 for l in L if l.strip() == old)
    if n != 1:
        raise SystemExit(u"甲2② 之錨非唯一（%d 見）" % n)
    out = [new if l.strip() == old else l for l in L]
    print(u"  甲2② 改題 1 處：%s" % new[:40])
    return out, 1


def k_jia2a(L):
    """甲2①：第十一章第三節全文換為第一人稱自救觀心版（作者給定・式樣歸真）。"""
    head = (u"### 第三節　正理八自救指針：行者移轉管轄自救備忘")
    tailmark = (u"永遠護念每一個在泥潭中掙扎求生的清白行者")
    if any(u"觀心提撕：法非絕人之路" in l for l in L):
        print(u"  甲2① 已在帳（重入之護）")
        return L, 0
    i0 = [i for i, l in enumerate(L) if l.strip().startswith(head)]
    i1 = [i for i, l in enumerate(L) if tailmark in l]
    if len(i0) != 1 or len(i1) != 1 or i1[0] < i0[0]:
        raise SystemExit(u"甲2① 之界非唯一（起 %d・迄 %d）" % (len(i0), len(i1)))
    seg = [
        head + u"（第一人稱觀心版）",
        u"",
        u"> **【觀心提撕：法非絕人之路】**  ",
        u"> 戒律是救拔慧命之良藥，絕非派系私刑之凶器。  ",
        u"> 我若不幸身處一個失去正見、派系鬥諍熾盛、或掌權執事利用戒律對我實施法規施虐"
        u"與精神霸凌之道場，致使自身行治受阻、道念瀕臨崩潰——"
        u"**我當深信：毘奈耶自始為我留有生路！**  ",
        u"> 我得本於正理八（斷漏為的）賦予之自救生機，不需向對我施虐之原處分寺院乞求通融，"
        u"依三步自救出險：",
        u"",
        u"```text",
        u"【第一步：出界前單向口宣（自我合法凍結）】",
        u"  · 臨行出界前，我當向界內任一位清淨同修當面口宣：",
        u"    『我某甲比丘，今捨別住（或捨摩那埵）。』",
        u"  · 宣畢，我的行法天數在法界即刻合法凍結存檔；我在外避險期間",
        u"    絕不構成失宿，原寺單方作成之歸零重置自始無效。",
        u"            " + chr(0x2502),
        u"            " + chr(0x25BC),
        u"【第二步：奔赴十方清淨僧伽陳情（尋求法統庇護）】",
        u"  · 門徑一：我當向入境巡錫之持律客僧、五德長老當面提交真實事證陳情書；",
        u"  · 門徑二：我當隻身前往鄰近具足法定人數之正信大叢林，",
        u"    申請接管續行未竟行治；",
        u"  · 門徑三：比丘尼若在尼寺內部遭受權威霸凌，",
        u"    依法得逕向大僧比丘僧團陳情求援。",
        u"            " + chr(0x2502),
        u"            " + chr(0x25BC),
        u"【第三步：接收道場接管與終局出罪（圓滿清淨復權）】",
        u"  · 接收道場核實我之冤抑屬實，依白四羯磨正式接管監護，",
        u"    我的行法天數在清淨新界接續計算；",
        u"  · 原施虐寺院之管轄權依法即刻消滅；期滿由新道場二十位清淨大僧",
        u"    為我出罪，其復權效力遍及十方僧伽。",
        u"```",
        u"",
        u"行法不廢，環境轉軌；身受委屈，心不退道。  ",
        u"《四分律》本地卷段三十八至四十九之檔載佛陀親口承諾"
        + QUOTE + u"比丘我共汝作伴，如法非不如法" + ENDQ +
        u"；正法的羽翼，永遠護念每一個在泥潭中掙扎求生的清白行者。",
    ]
    simp_chk(seg, u"甲2①")
    latin_chk(seg, u"甲2①")
    nq = verbatim_chk(LF.join(seg), u"甲2①")
    w = max(sum(2 if ord(c) > 0x2000 else 1 for c in x) for x in seg if x.startswith(u"  · "))
    print(u"  甲2① 換節：%d 行代 %d 行（L%d–L%d）・圍欄內最長 %d 格・逐字引 %d 條俱對證"
          % (len(seg), i1[0] - i0[0] + 1, i0[0] + 1, i1[0] + 1, w, nq))
    return L[:i0[0]] + seg + L[i1[0] + 1:], 1


REPL = [
    # (tag, old_sub, new_sub)  ── 行內之替換，逐條唯一錨
    (u"乙3·閉溫室", QUOTE + u"閉溫室、分惡房、動員冷漠" + ENDQ,
     chr(0x300E) + u"閉溫室、分惡房、動員冷漠" + chr(0x300F)),
    (u"乙3·分惡房事相", u"而" + QUOTE + u"分惡房、生瞋恚" + ENDQ + u"之事相",
     u"而" + chr(0x300E) + u"分惡房、生瞋恚" + chr(0x300F) + u"之事相"),
    (u"乙3·嫉相本律",
     u"唯其心相（不耐他榮、以利養故生嫉）則本律有明文，今引為證。",
     u"唯其嫉相有本律之明文（見本地卷段一至十之檔），今引為證。"),
    (u"乙3·主觀惡意出處",
     u"1. **主觀惡意之勘**：既查其所為純出" + QUOTE + u"以利養故生嫉妬心" + ENDQ +
     u"（本律自有此心相之判）",
     u"1. **主觀惡意之勘**：本地卷段一至十之檔記" + QUOTE +
     u"以利養故生嫉妬心" + ENDQ + u"，既查其所為純出此心"),
    (u"乙3·論釋嫉", QUOTE + u"徇自名利，不耐他榮，妒忌為性" + ENDQ,
     chr(0x300E) + u"徇自名利，不耐他榮，妒忌為性" + chr(0x300F)),
    (u"乙3·佛呵", QUOTE + u"不耐他榮、心懷弊惡" + ENDQ,
     chr(0x300E) + u"不耐他榮、心懷弊惡" + chr(0x300F)),
    (u"乙3·公事公辦", u"不得以" + QUOTE + u"公事公辦" + ENDQ + u"解免",
     u"不得以" + chr(0x300E) + u"公事公辦" + chr(0x300F) + u"解免"),
]

GZ = (u"乙3·染污心歸真",
      u"本地所記偷羅難陀比丘尼之實事，別在" + QUOTE + u"染污心共染污心男子身相觸" + ENDQ + u"一案",
      u"本地所記偷羅難陀比丘尼之實事，即在本地卷段二十二至三十之檔" + QUOTE +
      u"若比丘尼染污心，共染污心男子，從腋已下膝已上身相觸" + ENDQ + u"一案")


def k_yi3(L):
    """乙3：式樣之刀・逐條唯一錨・落後以**終態**之改行再過一次逐字之閘。
    （中途之快照會把尚未改完之行誤報為病，故只記行號，落刀畢方取 L[i]。）"""
    hits, rows = 0, set()
    for tag, old, new in REPL + [GZ]:
        cnt = [i for i, l in enumerate(L) if old in l]
        if not cnt:
            if any(new in l for l in L):
                print(u"  %-18s 已在帳（重入之護）" % tag)
                continue
            raise SystemExit(u"乙3 之錨未中（不敢假稱已治）：%s" % tag)
        if len(cnt) > 1:
            raise SystemExit(u"乙3 之錨非唯一：%s（%d 見）" % (tag, len(cnt)))
        i = cnt[0]
        L[i] = L[i].replace(old, new)
        rows.add(i)
        print(u"  %-18s 落 1 處（L%d）" % (tag, i + 1))
        hits += 1
    simp_chk(L, u"乙3·落後全檔")
    verbatim_chk(LF.join([L[i] for i in sorted(rows)]), u"乙3·落後之逐字宣稱")
    return L, hits


def main():
    go = "--write" in sys.argv
    before = raw()
    sha = hashlib.sha256(before.encode("utf-8")).hexdigest()[:12]
    L = before.replace("\r\n", LF).split(LF)
    print(u"F1 %s・%d 行・SHA %s" % (os.path.basename(BOOK)[:14], len(L), sha))
    n_before = len(L)
    L, a = k_jia2b(L)
    L, b = k_jia2a(L)
    L, c = k_yi3(L)
    if a + b + c == 0:
        print(u"  ・三刀俱已在帳，不落盤")
        return 0
    print(u"  合計 %d 目・行 %d ➔ %d（甲2① 換節為主要之變）" % (a + b + c, n_before, len(L)))
    if not go:
        print(u"（試跑・加 --write 始落盤）")
        return 0
    if not os.path.isdir(os.path.dirname(BK)):
        os.makedirs(os.path.dirname(BK))
    io.open(BK, "wb").write(before.encode("utf-8"))
    nl = CRLF if CRLF in before else LF               # 行尾須隨原檔：翻成 LF 即全檔盡改（假改動）
    io.open(BOOK, "wb").write(nl.join(L).encode("utf-8"))
    after = io.open(BOOK, "rb").read()
    print(u"  落盤：%d 行・%d B・行尾 %s・SHA %s ➔ %s・備 %s"
          % (after.decode("utf-8").count(CRLF) + 1, len(after),
             u"CRLF" if nl == CRLF else u"LF", sha,
             hashlib.sha256(after).hexdigest()[:12], os.path.relpath(BK, ROOT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
