# -*- coding: utf-8 -*-
"""第六波・法制卷之詳細總目錄（外路第八報告・第一項之二，量得屬真：今印面唯結構全貌圖，無逐節之目）。

由正文自算（篇 H2・章 H3・節 H4・附錄 H2・終卷），名單不兩抄；舊『今冊附錄之目』隨之退場。
插於【出版凡例與引文承諾】之後、第一篇之前（與心法卷『凡例→目錄』同次）。
再跑即整塊重建（先削舊塊，故可重入）。
用法：python -X utf8 _work/pairf2toc.py [--write]
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import pairsimp as PS  # noqa: E402

F2 = "如法推尋：僧伽憲政、法權審理與修復正義.txt"
BAK = ROOT / "_archive/備份/AI清理前"
W = "--write" in sys.argv
PIAN = re.compile(r"^##\s*(第[一二三四五六七八九十]+篇[:：].*)$")
ZHANG = re.compile(r"^###\s*(第[一二三四五六七八九十]+章[　 ].*)$")
JIE = re.compile(r"^#{3,4}\s*(第[一二三四五六七八九十]+節[　 ].*)$")
APX = re.compile(r"^##\s*(附錄[一二三四]　.*)$")
ZHONG = re.compile(r"^##\s*(【終卷[　 :：].*)$")
ANCHOR = "## 第一篇：憲政基石"
HEAD = "## 【全書標準總目錄】"
OLDLBL = "**【今冊附錄之目】**"


def cnum(n):
    return {5: "五", 20: "二十", 4: "四"}.get(n, str(n))


def build(L):
    out, np_, nz, nj, na = [], 0, 0, 0, 0
    for l in L:
        s = l.strip()
        m = PIAN.match(s)
        if m:
            np_ += 1
            out += ["", "* **【%s】**" % m.group(1)]
            continue
        m = ZHANG.match(s)
        if m:
            nz += 1
            out.append("  * **%s**" % m.group(1))
            continue
        m = JIE.match(s)
        if m:
            nj += 1
            out.append("    * %s" % m.group(1))
            continue
        m = APX.match(s)
        if m:
            na += 1
            out.append("  * **%s**" % m.group(1))
            continue
        m = ZHONG.match(s)
        if m:
            out.append("  * **%s**" % m.group(1))
    head = ["", "* **【卷首】**",
            "  * 自序・開卷總綱（五大基石宣言）・兩則附說（正理對位與記憶分級）・全書結構全貌圖・出版凡例與引文承諾"]
    seg = [HEAD + "（%s篇%s章・%d節・附錄%s篇）" % (cnum(np_), cnum(nz), nj, cnum(na)),
           "", "### 目錄", ""] + head + out
    return seg, (np_, nz, nj, na)


def purge_old_list(L):
    """退『今冊附錄之目』一塊：自其前最近之『***』起，至其後最近之分隔止。"""
    i = next((k for k, l in enumerate(L) if l.strip() == OLDLBL), None)
    if i is None:
        return 0
    a = next(k for k in range(i, -1, -1) if L[k].strip() == "***")
    b = next(k for k in range(i, len(L)) if L[k].strip() in ("---", "***"))
    del L[a:b + 1]
    return b - a + 1


def main():
    raise SystemExit(
        u"退役（第十四波）：目錄今由 _print/build_pair.py 之點線目錄生成器印出並載頁碼，"
        u"正本之 markdown 目錄塊已由 _work/pair14.py 除盡；再跑本器會生出不印之幽靈目錄。"
        u"覆核改走 _work/pairtocnum.py（逐條驗目錄號＝印面頁）。")
    p = ROOT / F2
    raw = p.read_bytes()
    L = raw.decode("utf-8").split("\r\n")
    if any(l.startswith(HEAD) for l in L):
        i0 = next(i for i, l in enumerate(L) if l.startswith(HEAD))
        i1 = next(i for i in range(i0, len(L)) if L[i].strip().startswith(ANCHOR))
        del L[i0:i1]
        print("  ・削舊總目錄塊 %d 行（整塊重建）" % (i1 - i0))
    nd = purge_old_list(L)
    if nd:
        print("  ・退『今冊附錄之目』%d 行（歸一入總目錄）" % nd)
    seg, cnt = build(L)
    for nm in ("【自序", "【開卷總綱", "### 附說：", "### 附說二：", "結構全貌圖", "【出版凡例"):
        if not any(nm in l and l.startswith("#") for l in L):
            raise SystemExit("卷首之目失實：目錄宣『%s』而正文無其題" % nm)
    print("  卷首六目俱有實題 ✓（目錄之卷首一行自此自證，不再憑記憶手抄）")
    k = next(i for i, l in enumerate(L) if l.strip().startswith(ANCHOR))
    L[k:k] = seg + ["", "---", ""]
    bad = sorted({c for l in seg for c in PS.hits(l)})
    print(f"生成 {len(seg)} 行・篇{cnt[0]}・章{cnt[1]}・節{cnt[2]}・附錄{cnt[3]}・簡形 {bad}")
    for x in seg[:16]:
        print("   ", x[:74])
    if bad:
        raise SystemExit("帶簡形，不落盤")
    if not W:
        print("（試跑：未落盤）")
        return
    (BAK / (F2 + ".pre_toc")).write_bytes(raw)
    data = "\r\n".join(L).encode("utf-8")
    p.write_bytes(data)
    print(f"  ● {F2[:6]}・{len(L)} 行・SHA {hashlib.sha256(raw).hexdigest()[:12]} → {hashlib.sha256(data).hexdigest()[:12]}")


main()
