# -*- coding: utf-8 -*-
"""第 46 輪修補：第三章兩則按語、第二部卷端程序指針、第二十章自稱歸實。

法源：全書骨架不動（F／G／H／I 已封存，同心圓層級語不動），只加字句與指針。
斷言：每处以「舊形唯一命中」為前提；行數與 CR 數当场報。
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
NL = chr(13) + chr(10)
GO = u"--go" in sys.argv

raw = io.open(BOOK, encoding="utf-8", newline="").read()
L = raw.split(NL)
n0 = len(L)
assert raw.count(chr(13)) == n0 - 1, (u"CR 數不符", raw.count(chr(13)), n0 - 1)


def anchor(idx, head, tag):
    """idx 為 1 起之行號；head 非空則該行須以此開頭，head 為空則該行須確為空行。"""
    got = L[idx - 1]
    if head:
        assert got.startswith(head), (u"錨點不符：" + tag, got[:60])
    else:
        assert got == u"", (u"空行不符：" + tag, repr(got[:40]))
    return got


def ins_after(idx, lines, tag):
    """在行號 idx 之後插入 lines（呼叫端須先確認 idx 之後是空行）。"""
    for t in lines:
        assert u"・" not in t and u"！" not in t, (u"禁用字形：" + tag)
    L[idx:idx] = lines
    print(u"插入 %s：L%d 後 +%d 行" % (tag, idx, len(lines)))


# ── 一・第三章：既有按語之後添兩則按 ──
anchor(1005, u"**按：城牆之", u"第三章・既按")
anchor(1006, u"", u"第三章・空行")
anchor(1007, u"---", u"第三章・分隔線")
AN1 = (u"**按：圖自上而下畫的是敵軍攻入的方向，正文自內向外走的是戒本次第。**"
       u" 第五重之內有兩處設施：最外寬廣的護城河是百眾學法，稍內的前哨檢查站是四提舍尼法。"
       u"故圖上先列眾學、正文先列提舍尼，兩名同在一重之中，不是上下級，而是職司之分："
       u"一者管的是身與口最細的節拍，一者管的是進村受食那條人際界線。"
       u"出罪之法亦隨之而異——提舍尼之義本是「向人發露」，犯者須對一位清淨比丘說；"
       u"眾學法犯者但結最輕的突吉羅。二說俱見第十章第一、二節。")
AN2 = (u"**按：同心圓外還有兩類法，而此圖的名數只依比丘戒本。**"
       u" 二不定法不是一種罪名，而是一個待證的程序狀態——所犯落在波羅夷、僧殘、波逸提三檔中的哪一檔，"
       u"取決於目擊者的指說與當事人的自陳，律既不預立其名，此圖便無從給它一「重」。"
       u"本書依戒本次第把它列在第六章案例六，其如何斷、如何滅則歸在第十章第三節。"
       u"七滅諍法同理不入此圖：它不是城防的一圈，而是全城共用的法庭，"
       u"本書於第十章第三節名之為『最高憲法法院』，於第十一章專敘其制。"
       u"又此五重之名與條數皆從比丘戒本，比丘尼端同名諸重的條數與邊界俱異："
       u"同一樁染心相觸，在比丘是僧殘，在比丘尼是死罪；同一樁覆他重罪，在比丘是單提，在比丘尼亦是波羅夷。"
       u"故同心圓的等距緩衝，到女眾端須把間距重畫——那不是圖畫錯，是兩座城的牆距本就不同。"
       u"說詳第十二章第三、五節。")
ins_after(1006, [AN1, u"", AN2, u""], u"第三章・兩則按語")

# ── 二・第二部卷端：程序名相之歸屬 ──
anchor(1215 + 4, u"在接下來的", u"第二部卷端")
anchor(1216 + 4, u"", u"卷端・空行")
anchor(1217 + 4, u"---", u"卷端・分隔線")
NOTE = (u"讀本部有一個約定須先說明：諸章屢及程序之名——白四羯磨、別住、行覆藏、本日治、摩那埵——"
        u"此處但取其用於罪相，看的是「這一條犯了要怎麼治」；"
        u"至於誰能作、幾個人算數、說幾次才算成立，那些行款的全貌在第十一章。")
ins_after(1216 + 4, [NOTE, u""], u"第二部卷端・程序約定")

# ── 三・第二十章：自稱歸實（書中「輕推」唯此節用之，無「向來作總名」之事） ──
OLD = u"本書向來以「輕推」作總名，為的是讀者一眼認得；但嚴格說，"
NEW = u"本書前文多以「護欄」與「情境工程」言之，讀者或以為這便是「輕推」；但嚴格說，"
hits = [i for i, t in enumerate(L) if OLD in t]
assert len(hits) == 1, (u"自稱句命中數", len(hits))
L[hits[0]] = L[hits[0]].replace(OLD, NEW)
print(u"改寫 第二十章自稱：L%d 命中 1" % (hits[0] + 1))

assert len(L) == n0 + 6, (u"行數不符", len(L), n0 + 6)
out = NL.join(L)
print(u"行數 %d → %d ｜ CR %d" % (n0, len(L), out.count(chr(13))))
if GO:
    io.open(BOOK, "w", encoding="utf-8", newline="").write(out)
    print(u"已寫入")
else:
    print(u"（試跑，未寫入）")
