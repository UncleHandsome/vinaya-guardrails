# -*- coding: utf-8 -*-
"""第十五波・落後之覆核：十五案逐條以今檔與今印面對帳（宣稱須實測）。"""
import io
import os
import re
import sys

import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import _tk                                            # noqa: E402

F1 = next(os.path.join(ROOT, x) for x in os.listdir(ROOT) if x.startswith(u"起心動念") and x.endswith(u".txt"))
F2 = next(os.path.join(ROOT, x) for x in os.listdir(ROOT) if x.startswith(u"如法推尋") and x.endswith(u".txt"))
P = os.path.join(ROOT, "_print")


def rd(p):
    return io.open(p, "rb").read().decode("utf-8-sig").replace("\r\n", "\n").split("\n")


A, B = rd(F1), rd(F2)
print("=" * 72)
print("十五案・逐條對帳（今檔）")
CK = [
    (u"甲2① 第一人稱自救節", lambda: [l for l in A if u"觀心提撕：法非絕人之路" in l],
     u"卷一 第十一章第三節"),
    (u"甲2② 問心之兩徑", lambda: [l for l in A if u"問心之兩徑" in l], u"第一章第三節題"),
    (u"甲3 十五章名", lambda: [l for l in B if l.startswith(u"### 第十五章")], u"含『淨人作務』"),
    (u"甲3 十六章名", lambda: [l for l in B if l.startswith(u"### 第十六章")], u"純化為裁決之文"),
    (u"甲3 十五章之第四節", lambda: [l for l in B if l.startswith(u"### 第四節　出坡作務")], u"新立"),
    (u"甲3 凡例第八律章次", lambda: [l for l in B if u"第十五章第四節立【制度案卷 104】" in l], u"章次歸實"),
    (u"丁3 副標之除", lambda: [l for i, l in enumerate(B[:6]) if l.startswith(u"### ——")], u"應為空"),
    (u"戊1 檢綱定名", lambda: [l for l in B if u"執事開庭十六項一票否決檢綱" in l], u"二十章第一節"),
    (u"戊1 宣告定名", lambda: [l for l in B if u"四署心證自律宣告式" in l], u"二十章第二節"),
    (u"戊1 查考級稱名", lambda: [l for l in B if u"開庭十六項檢綱與四署宣告" in l], u"卷首附說二"),
    (u"丁2 對照圖之雙卡", lambda: [l for l in A if re.search(u"發動鏈對照】･[上下]卡", l)], u"四張卡"),
]
for tag, f, note in CK:
    got = f()
    want_empty = tag.startswith(u"丁3")
    ok = (not got) if want_empty else bool(got)
    print("  %-22s %s・%d 見｜%s" % (tag, u"✓" if ok else u"✗", len(got), note))
    if got and not want_empty:
        print("        " + got[0].strip()[:88])

print("=" * 72)
print("乙1・乙2｜企業專名之落後計數（裁決列名者須歸零）")
BAN = (u"董事會", u"監事會", u"三線模型", u"IIA", u"非營利", u"穿透審計", u"實質受益人",
       u"SOP", u"KPI", u"理事會")
KEEP = (u"安全閥", u"防火牆", u"護網", u"落日", u"減量原則", u"避風港")
for nm, L in ((u"F1", A), (u"F2", B)):
    bad = [(w, sum(1 for l in L if w in l)) for w in BAN if any(w in l for l in L)]
    good = [(w, sum(1 for l in L if w in l)) for w in KEEP if any(w in l for l in L)]
    print("  %s｜列名之未盡 %s ＝ %s" % (nm, u"0 項" if not bad else u"有", bad or u"（俱歸零）"))
    print("        准留之通喻：%s" % u"、".join(u"%s %d" % (w, n) for w, n in good))
    未 = [(w, sum(1 for l in L if w in l)) for w in (u"合規", u"稽核", u"法人", u"機構化")
          if any(w in l for l in L)]
    print("        裁決未列名・如實不動：%s" % u"、".join(u"%s %d" % (w, n) for w, n in 未))

print("=" * 72)
print("式樣｜『「』之逐字宣稱須在語料見形且左側有出處（兩冊全掃）")
print("     口徑：語料＝《四分律》本律＋本地所收他典（《成唯識論》《楞嚴》等）——他典之豁免先入尺")
BAD = _tk.norm(_tk.VINAYA) + u"".join(_tk.norm(v) for v in _tk.OTHER.values())
VL = _tk.norm(_tk.VINAYA)
bad, only_other = [], []
for nm, L in ((u"F1", A), (u"F2", B)):
    for i, l in enumerate(L, 1):
        for m in re.finditer(u"「[^」]{6,}」", l):
            body = _tk.norm(m.group(0)[1:-1])
            left = l[max(0, m.start() - 46):m.start()]
            if re.search(u"《|本地|卷段|之檔|大正藏|律作|原典", left):
                if body not in BAD:
                    bad.append(u"%s L%d 語料全無其形｜%s" % (nm, i, m.group(0)[:30]))
                elif body not in VL:
                    only_other.append(u"%s L%d｜%s" % (nm, i, m.group(0)[:24]))
print(u"  自稱逐字而**兩語料俱無形**者（真待清之類）：%d 條" % len(bad))
for x in bad[:10]:
    print("    " + x)
print(u"  本律無形而他典有形（他典之引・屬正）：%d 條" % len(only_other))

print("=" * 72)
print("印面｜四檔之頁數・細字・圍欄同頁")
for stem, short in ((u"起心動念_四分律的心智顯微鏡與唯識解剖_", u"F1"),
                    (u"如法推尋_僧伽憲政法權審理與修復正義_", u"F2")):
    for ed in (u"螢幕版", u"影印版"):
        d = pymupdf.open(os.path.join(P, stem + ed + u".pdf"))
        lo, n9 = 99, 0
        for p in range(d.page_count):
            for b in d[p].get_text("dict")["blocks"]:
                for ln in b.get("lines", []):
                    for s in ln["spans"]:
                        if s["text"].strip() and not s["text"].strip().isdigit():
                            lo = min(lo, s["size"])
                            n9 += s["size"] < 9
        print("  %s｜%s・%d 頁・最小 %.2fpt・9pt 以下 %d span"
              % (short, ed, d.page_count, lo, n9))
        d.close()
for ed in (u"螢幕版", u"影印版"):
    d = pymupdf.open(os.path.join(P, u"雙子星合冊_起心動念＋如法推尋_" + ed + u".pdf"))
    print(u"  合冊｜%s・%d 頁・書籤 %d 條" % (ed, d.page_count, len(d.get_toc())))
    d.close()
