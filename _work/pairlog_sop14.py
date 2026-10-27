# -*- coding: utf-8 -*-
"""第十四波・SOP 入帳（目錄改產器生成並載頁碼）。

行號定位而非字面錨點：找『## 產出位置』之標題，在其前插入本輪之條目。
落盤前後各印正本 SHA（本器不動正本，只動 `列印SOP.md`），並以簡形閘自掃新文。
"""
import hashlib
import io
import os
import sys

SOP = u"列印SOP.md"
MARK = u"## 產出位置"

TXT = u"""- **第十四波・奉令『目錄沒有頁碼』（2026-10-27・目錄自此為產物而非手抄）**：
  **斷因（先量）**：兩冊之目錄向是正本內之**手抄 markdown 清單**（F1 凡 60 行・F2 凡 129 行），其形制本無頁碼可載，且與正文標題梯可漂移——『沒有頁碼』非漏打，是**載體錯**。目錄之法源應是正文標題，故刀落於產器。
  **刀（`_work/pair14.py`・四閘：唯一錨・行形白名單・條目數≥20・不入圍欄）**：除兩冊之目錄塊。F1 L240–299（60 行）➔ **3,993 行・`4400ed6165a0`**；F2 L231–359（129 行）➔ **5,041 行・`ff8eeb6769a1`**（正本餘文一字不動）。
  **產器之改（`_print/build_pair.py`）**：目錄今由 `build38.build_toc_html` 之**點線目錄**印出，條目法源一本＝正文標題梯（篇 H1・章 H2・節 H3＋案卷卡〔卡名含【案卷】之 H4〕歸三級），**頁碼以印面反查回填**：排一版→量各題所在之物理頁→注入→再排，至不動點（上限 6 回合；不收斂如實報『末回仍有位移』，未入號即擲而**不交付**）。今兩式俱**第 2 回合收斂**。
  **自逮自治四病（皆產器之病，非冊之病）**：① 佔位錨若退落首個 H2，目錄被提到卷首之前➔改錨**首個篇題 H1**（『正文之前、卷首之後』）。② 目錄頁含全書標題，若入掃描池則『自序』等卷首之題會自指目錄自己那頁➔立 `toc_pages_of`（帶點線頁碼之行≥5 者）擯之。③ `build38.scan_pages` 之 TH=14.5pt 大字門於本冊全數失效（本冊標題最細 13.9pt）➔改 `entry_map(entries, locate(…)[2])`：按文取號・同名者依出現之序 consumption（不重複指同一頁）。④ `refit_pre` 若落在回填之後，圍欄縮字即挪頁，目錄遂帶 ±1 之漂移（實測 F1『入林與觀心警示』印 6／實 5）➔改『**先圍欄回量，後只替 FINAL 內 `<!--TOC-A-->`…`<!--TOC-B-->` 之區段，每回合僅重跑 `render_pdf`**』。
  **細字一病（目錄之細字仍是印面之細字）**：舊法遇超長條目按比例縮字，F2 三條案卷卡遂排成 9.3／10.0／10.4pt，破其自報之下限 10.5。➔產器立 `toc_line_split`（**保級折行**：折點取『：、（，；—|』自右向左取首行合版寬者，至多三行；無折點者回落縮字並報警），CSS 加 `.toc-cont`。今 **F1 折 3 條・F2 折 5 條**（兩式同數；建置日誌所報之數已去重，因收斂各回合皆重排目錄，不去重即倍報）。
  **新尺 `_work/pairtocnum.py`（四軸俱量產物，不取產生器之自報）**：甲 條條有號・乙 號與印面合（對書籤）・丙 戶口（篇・章・節・案卷卡俱須在目；【全書…結構全貌圖】如實豁免——該圖即目錄之身，產生器已定不重複入目）・丁 字級下限（目錄頁 span 實量，純數字頁腳不入）。**器病三則由自驗現形**：初版 `toc_pages` 只認含『目』『錄』二字之首頁➔F1 130 條報 41、丙虛紅 17（此即『校驗器之管轄須與宣稱同寬』之舊案再現）；改『順勢前推而至號條斷絕』後末頁（只賸一二條）仍被鋸➔續頁之判改從**內容純為目錄行**（除帶號行與純數字頁腳外別無他文）；折行之接合須以『**尾無點線**』辨上半行，否則真缺號（標題＋點線而無號）同遭抹綠。**負測以重建前之陳影印版為盆**：丁報 9.30pt・破下限 p14，乙報 6／10 條不合——四軸俱曾現形，非殭尺。
  **退舊器**：`_work/pairf1toc.py`／`_work/pairf2toc.py`（手抄目錄之重算器）首行立擲閘退役，往後之覆核改走 `pairtocnum`。
  **今量（第十四波後）**：F1 **3,993 行・`4400ed6165a0`** ➔ **119 頁・書籤 433・目錄 130 條**；F2 **5,041 行・`ff8eeb6769a1`** ➔ **173 頁・459・目錄 167 條**（印 166 行＋全貌圖豁免一）；合冊 **293 頁・接排 893**。頁數自 117／172／290 之增（F1+2・F2+1）純因目錄由手抄清單改點線生成，**非正文之增**。`pairtocnum` 退碼 **0**（四檔俱：目錄 4 頁 p11–p14・甲 0・乙 0・丙 0・丁 11.78／12.00pt）。諸尺齊跑：`pairface` 全綠（同期✓・書籤對合 459/459・圍欄外字面標記 0・骨架 篇4/章12・篇5/章20 對合）、`pairrefchk` 失指 0（管轄 622 條）、`pairtrim_check` 簡形 0 行、`pairclose` 三軸 0、`pairfence` F1 #22 如實不鎖（62 行矩陣，舊案同形）、`pairgeom` 真出框 0。**候裁諸案一仍其舊，未越一步。**
"""


def main():
    go = "--write" in sys.argv
    raw = io.open(SOP, "rb").read()
    sha12 = hashlib.sha256(raw).hexdigest()[:12]
    text = raw.decode("utf-8")
    L = text.split("\n")
    k = next((i for i, l in enumerate(L) if l.startswith(MARK)), None)
    if k is None:
        raise SystemExit(u"找不到『%s』之標題，不落刀（免誤插他處）" % MARK)
    if u"第十四波・奉令『目錄沒有頁碼』" in text:
        print(u"  ・已在帳（重入之閘），不復插")
        return 0
    new = TXT.rstrip("\n").split("\n")
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
    import pairsimp                        # 共器：簡形之口徑不另抄一張
    bad = [(l, pairsimp.hits(l)) for l in new if pairsimp.hits(l)]
    print(u"SOP %s・%d 行・SHA %s" % (SOP, len(L), sha12))
    print(u"  插於 L%d 之前（『%s』）・新文 %d 行" % (k + 1, MARK, len(new)))
    print(u"  簡形之掃（新文）：%d 行命中" % len(bad))
    for l, h in bad:
        print(u"      「%s」➔%s" % (h, l[:50]))
    if bad:
        raise SystemExit(u"新文帶簡形，不落刀")
    if not go:
        print(u"（試跑・加 --write 始落盤）")
        return 0
    L[k:k] = new + [u""]
    bdir = os.path.join(u"_archive", u"備份", u"SOP")
    if not os.path.isdir(bdir):
        os.makedirs(bdir)
    bpath = os.path.join(bdir, u"列印SOP.pre_toc.md")
    io.open(bpath, "wb").write(raw)                      # 一步回退：先存舊帳，再寫新帳
    io.open(SOP, "wb").write("\n".join(L).encode("utf-8"))
    back = hashlib.sha256(io.open(SOP, "rb").read()).hexdigest()[:12]
    print(u"  落盤：SOP %d 行・SHA %s➔%s・備份 %s" % (len(L), sha12, back, bpath))
    return 0


if __name__ == "__main__":
    sys.exit(main())
