# -*- coding: utf-8 -*-
"""ver39 雙版建置（承 build38.py 全套流程，來源改 ver39 修正版／第三十九版）

【ver39 之異於 ver38 者（升版當輪記）】
  一、附錄已改名并收為六篇（附錄一～附錄六，『十五則深描』分上・下兩篇 H1），
      編纂底冊四篇與終卷呈辭之去留一仍舊制（終卷不印）。
  二、正文八章（原第九章升格為第八章），第七章與第八章各分（上）（下）兩 H1。
  三、精簡本之削塊名單係對 ver38 字面而設，ver39 未立新制——run slim 即擲回，
      不產『半削之冊』（第 142 輪『寧可使建置失敗』之制今改為明閘）。

用法： python _print/build38.py [full|slim] [print|screen]
  full（預設）：完整版，全部附錄收錄，交叉引用不致落空
  slim       ：ver39 未定義精簡規則，跑即擲回（見上『三、』）
  print（預設）：影印版——鏡像邊距（內 18mm／外 10mm）＋章奇數頁起排（雙面裝訂用）
  screen     ：螢幕版——對稱邊距（左右 14mm）＋章連續起頁（無空白頁，PDF 直讀用）

成品一律放在 _print/（影印版沿用舊檔名，螢幕版另加「螢幕版」字樣，兩軌不互蓋）。
"""
import json, os, re, shutil, subprocess, sys, time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

_ARGS = [a.lower() for a in sys.argv[1:]]
MODE = next((a for a in _ARGS if a in ("full", "slim")), "full")
LAYOUT = next((a for a in _ARGS if a in ("print", "screen", "列印", "影印", "螢幕", "屏幕")),
              os.environ.get("LAYOUT", "print").lower())
if LAYOUT in ("列印", "影印"):
    LAYOUT = "print"
elif LAYOUT in ("螢幕", "屏幕"):
    LAYOUT = "screen"
if LAYOUT not in ("print", "screen"):
    LAYOUT = "print"
SCREEN = (LAYOUT == "screen")
TBLW = os.environ.get("TBLW", "content").lower()
TBLW_POW = float(os.environ.get("TBLW_POW", "0.5"))
CLEAN = any(a in ("clean", u"出淨", u"淨本") for a in _ARGS)     # 出淨本：卸案語與工程自述，正本一字不動
# 瀏覽器之虛擬時鐘與合成器旗標俱已撤除（第八十九輪交錯量測：同一 293 頁樣本，
# 現行旗標三遍取最小 44.8s，撤此二旗標 42.7s，省約 5%，而產物之位元組數、頁數、
# 文字長度三者全同）。近空白頁之啟動底數 2.9s，故 94% 之耗時在排版與落盤本身，
# 非進程冷啟動——CDP 常駐瀏覽器之方案於此最多省六成之五，不採。
# 若他日字型或資源改自網路取，須同時取回此二旗標（以 verify38 覆核為後盾）。
# 目錄頁碼之暖起點：以 `TOCSEED=0` 可廢。詳見 main 之說明。
TOCSEED = os.environ.get("TOCSEED", "1") != "0"
SUFFIX = "" if MODE == "full" else "_精簡本"
SUFFIX += "_出淨" if CLEAN else ""
TAG = "" if not SCREEN else "_screen"
STEM = ("ver39四分律_起心動念心智分析框架_第三十九版_列印版" + SUFFIX
        if not SCREEN else
        "ver39四分律_起心動念心智分析框架_第三十九版_螢幕版" + SUFFIX)

SRC = os.path.join(ROOT, "ver39四分律_起心動念心智分析框架_修正版.md")
MD = os.path.join(HERE, "ver39_列印版%s%s.md" % (SUFFIX, TAG))
HTML = os.path.join(HERE, "ver39_列印版%s%s.html" % (SUFFIX, TAG))
FINAL = os.path.join(HERE, "final39%s%s.html" % (SUFFIX, TAG))
PDF = os.path.join(HERE, "ver39_列印版%s%s.pdf" % (SUFFIX, TAG))
# 註：SUFFIX 已使 full／slim 各自擁有獨立的 .md／.html／.pdf 中介檔，
#     兩者可先後執行而不互相覆蓋（早期版本共用中介檔導致 DOCX 產生失敗）。
PDF_OUT = os.path.join(HERE, STEM + ".pdf")
DOCX_OUT = os.path.join(HERE, STEM + ".docx")
CSS_FILE = "print38.css"

# 精簡本僅收 A、B；K 款級台帳自第 79 輪起並連定本亦不隨冊（編者自查之表，退工作檔）
SLIM_KEEP = {"A", "B"}   # 精簡本不附款級台帳（內部查核表，讀者無用）
EDITION = ("第三十九版" + ("（通讀精簡本）" if MODE == "slim" else "（出淨本）" if CLEAN else "（定本）")
           + ("·螢幕版" if SCREEN else ""))
APPS = "附錄一～六　六篇隨冊"

SUBTITLE = "心法、律相與群體治理的立體成型，而終歸於斷有漏"

CN_DIG = {1: u"一", 2: u"二", 3: u"三", 4: u"四", 5: u"五", 6: u"六", 7: u"七", 8: u"八", 9: u"九",
          10: u"十", 11: u"十一", 12: u"十二"}


def book_meta():
    """封面之數字自書身算出——不硬寫。歷輪之教：硬寫之數必與冊身脫節（此處舊作『一百則判例』，
    而第六章於第 254 輪已依作者『取消一百個定數』之親裁成為 102 則，封面遂成虛報）。"""
    t = open(SRC, encoding="utf-8").read()
    ch = len({m.group(1) for m in re.finditer(u"(?m)^# 第([一二三四五六七八九])章", t)})
    import sys as _s; _s.path.insert(0, os.path.join(os.path.dirname(HERE), "_work"))
    import _casedef as _CD            # 276：案號定義共器（第六章改製，卡節已亡）
    cases = len(_CD.case_defs(t.splitlines()))
    buyi = len(re.findall(u"(?m)^### 〔調部深描 \\d+〕", t))
    gates = len(set(re.findall(u"(?m)^### 閘門([一二三四五六])", t)))
    axioms = len(set(re.findall(u"正理([一二三四五六七八])：", t)))
    for k, v in ((u"章", ch), (u"案例卡", cases), (u"深描", buyi), (u"閘門", gates), (u"正理", axioms)):
        assert v > 0, u"封面之數算得 %r＝0，源檔形制已變，須先改此器再出冊" % k
    return (u"%s章·%d 則判例·%d 則深描·%d 重心智閘門·%d 大正理"
            % (CN_DIG.get(ch, ch), cases, buyi, gates, axioms))

# ── 封面（簡約風）：無框、大留白、一線分隔 ──────────────────────
COVER = """<section id="print-cover" class="cov">
  <p class="cov-eyebrow">大正藏第一四二八號·四分律</p>
  <div class="cov-main">
    <div class="cov-sutra">四分律</div>
    <div class="cov-title">起心動念心智分析框架</div>
    <div class="cov-rule"></div>
    <p class="cov-sub">心法、律相與群體治理的立體成型，而終歸於斷有漏</p>
    <p class="cov-motto">善護三業　但自觀行　蜂採其華　不惱他人<br />
       明眼避險　自淨其意　勤學無憂　常樂空閑</p>
    <p class="cov-cap">諸佛教心印·三十二字略戒憲綱</p>
  </div>
  <div class="cov-foot">
    <p class="cov-edition">__EDITION__</p>
    <p class="cov-meta">__META__<br />
       __APPS__</p>
  </div>
</section>
"""

DROP_QUOTE_PREFIX = ("**本版說明**", "**新舊名對照見附錄D-3**")
BODY_ANCHOR = "<!--BODY-START-->"   # 正文起點標記：以 HTML 註解形之，僅供中介檔定位，
#     絕不落地印出（舊法以 0.35pt 白字藏「【正文起點】」四字，Chrome 列印仍照印，
#     並在正文前撐出一整頁空白——第七十六輪改弦更張）
SLIM_NOTE = (
    "> **〔存檔聲明〕**本精簡本供通讀，僅收附錄 A（宗門心法）、B（壓力測試）；"
    "修訂誌、跨章款級索引二篇與深度稽核報告同屬編纂底冊，兩式皆不隨冊；"
    "術語對照、原典出處對照表、經論互證表、調部存檔、現代治理對照屬考據檔案，見定本。"
    "正文凡稱「見附錄 C／D／E／F／H／I／J／K」者，均指該等存檔。"
)

# 列印版不錄：上篇前置宣告與「終卷」之竣工呈辭（H1 以關鍵語內含比對）。
# 編纂底冊四篇（附錄C 修訂誌・K 款級台帳・L 十維驗收・M 全書校勘記）自第 250 輪起另存
#   `_archive/編纂底冊.md`，已不入主檔——故不在此列，改由下方 `BOTTOM_KEYS` 反向守之：
#   主檔若再見此四題，即有人把底冊貼回書檔（讀者又看得見了），全建擲回。
# 卷首標準目錄段不在此列——它由 write_md 就地換成點線目錄。
DROP_H1 = ("全書竣工呈辭",)
BOTTOM_KEYS = ("修訂誌", "跨章款級索引", "十維驗收", "全書校勘記")
TOC_H2 = "【全書開卷標準目錄"        # 卷首標準目錄段首（H2 標題前綴）


def strip_md(s):
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    return re.sub(r"[`*]", "", s).strip()


def read_source():
    lines = open(SRC, encoding="utf-8").read().split("\n")
    out, skip = [], False
    for ln in lines:
        if ln.startswith("# 《四分律"):
            continue
        if ln.startswith("——"):
            continue
        # 卷首 stray：版次眉題已由封面承載，正文首段若殘留即成 P2 空白寡行頁之源，逕除；
        # 其後緊隨之首個 ---（水平線）亦同除，否則 <hr/> 獨佔 P2 仍成寡行頁
        if ln.strip() in ("【第三十八版·全書深度校勘定本】", "**【全新深度校勘定本】**"):
            continue
        if ln.strip() == "---" and not any(
            l.startswith("## 【開卷總提撕】") or l.startswith("## 【自序")
            or l.startswith("# 第一章") for l in out
        ):
            # 尚未見開卷/FM 前之分隔線即視為卷首 stray 的一部分
            # （正文內之 --- 因 out 已含開卷標記而不受影響）
            continue
        if ln.startswith("> "):
            body = ln[2:].strip()
            if any(body.startswith(p) for p in DROP_QUOTE_PREFIX):
                skip = True
                continue
            if skip and body == "":
                skip = False
                continue
            skip = False
        else:
            skip = False
        out.append(ln)
    return out


def collect_all_headings(lines, deep=4):
    hs = []
    for i, ln in enumerate(lines):
        m = re.match(r"^(#{%d,%d})\s+(.*)$" % (1, deep), ln)
        if m:
            hs.append((len(m.group(1)), m.group(2).strip(), i))
    return hs


def drop_blocks(lines, hs):
    """抽掉列印版不收的整段：深度稽核報告三篇、上篇前置宣告。"""
    h1 = [t for l, t, _ in hs if l == 1]
    back = [k for k in BOTTOM_KEYS if any(k in t for t in h1)]
    if back:
        raise SystemExit("底冊四篇已另檔（第 250 輪奉令移出書檔），主檔再見其題即又落讀者之眼：%s"
                         "——請移回 `_archive/編纂底冊.md`（查核器由 `_tk.BSRC` 串接照舊見其文）"
                         % back)
    dead = [k for k in DROP_H1 if not any(k in t for t in h1)]
    if dead:
        raise SystemExit("DROP_H1 關鍵語比不中任何 H1（篇名已改而未隨動）：%s｜現存 H1：%s"
                         % (dead, h1[-6:]))
    kill = []
    for lvl, title, i in hs:
        if lvl == 1 and any(k in title for k in DROP_H1):
            end = next((i2 for l2, _t, i2 in hs if i2 > i and l2 == 1), len(lines))
            kill.append((i, end))
        elif lvl == 3 and title.startswith("上篇："):
            end = next((i2 for l2, _t, i2 in hs if i2 > i and l2 <= 3), len(lines))
            kill.append((i, end))
    for s, e in sorted(kill, reverse=True):
        del lines[s:e]
    return lines


def drop_appendices(lines, hs):
    kill = []
    for lvl, title, i in hs:
        if lvl != 1:
            continue
        m = re.match(r"^附錄([A-Z])", title)
        if m and MODE == "slim" and m.group(1) not in SLIM_KEEP:
            end = next((i2 for l2, _t, i2 in hs if i2 > i and l2 == 1), len(lines))
            kill.append((i, end))
    for s, e in sorted(kill, reverse=True):
        del lines[s:e]
    return lines


def strip_ch6_yuandian(lines, hs):
    """精簡本：第六章百則每案之「◎原典」出處段不收（定位行～人間智慧保留）。

    刪除範圍：第六章 H1 內，整行恰為 `◎原典` 者，及其後連續之空行與
    引文(`>`）行。只在 slim 模式執行。
    """
    if MODE != "slim":
        return lines
    s = next((i for lvl, t, i in hs if lvl == 1 and t.startswith("第六章")), None)
    if s is None:
        return lines
    e = next((i for lvl, _t, i in hs if i > s and lvl == 1), len(lines))
    kill = []
    i = s
    while i < e:
        if lines[i].strip() == "◎原典":
            j = i + 1
            while j < e and (lines[j].strip() == "" or lines[j].lstrip().startswith(">")):
                j += 1
            kill.append((i, j))
            i = j
        else:
            i += 1
    for a, b in sorted(kill, reverse=True):
        del lines[a:b]
    print("  精簡本去原典：第六章刪除 %d 段" % len(kill))
    # 精簡本體例同步：P9 凡例「六段式」在去原典後實為五段，若不註明即成體例承諾落空；
    # 此處僅列印時替換，不動源檔（定本仍六段）。
    for i, l in enumerate(lines):
        if "案例六段式規格" in l:
            lines[i] = l.replace("案例六段式規格", "案例五段式規格（精簡本）").replace(
                "`人間智慧` ──► `文末原典`",
                "`人間智慧`（精簡本去「◎原典」出處段，定本六段見附錄E）")
            print("  精簡本體例註記：P9 六段式→五段式已同步")
            break
    return lines


def apply_slim_markers(lines):
    """區塊級開關（第 119 輪立）：`<!--SLIM-OUT-->…` 唯定本印，`<!--SLIM-ONLY-->…` 唯精簡本印。

    兩冊皆自 pandoc 之前過濾，故目錄、錨點、台帳所見即印面所有，不留半削之痕。
    標記須成對、不得巢疊——錯配或未閉即硬報（寧可使建置失敗，不靜默跳過）。"""
    res, stack, seen = [], [], 0
    for ln in lines:
        t = ln.strip()
        if t in (u"<!--SLIM-OUT-->", u"<!--SLIM-ONLY-->"):
            if stack:
                raise SystemExit(u"SLIM 標記巢疊未閉：%s" % t)
            stack.append(u"OUT" if "OUT" in t else u"ONLY")
            seen += 1
            continue
        if t in (u"<!--/SLIM-OUT-->", u"<!--/SLIM-ONLY-->"):
            want = u"OUT" if "OUT" in t else u"ONLY"
            if not stack or stack[-1] != want:
                raise SystemExit(u"SLIM 標記錯配：%s（棧：%s）" % (t, stack))
            stack.pop()
            continue
        if stack:
            inside = stack[-1]
            keep = (inside == u"ONLY") if MODE == "slim" else (inside == u"OUT")
            if not keep:
                continue
        res.append(ln)
    if stack:
        raise SystemExit(u"SLIM 標記未閉：%s" % stack)
    if seen:
        print(u"  SLIM 區塊開關：%d 對標記（今 %s mode，剔除 %d 行）" % (
            seen, MODE, len(lines) - len(res)))
    return res


def apply_slim_cuts(lines, hs):
    """精簡本減重（第 112 輪立）：削檢索附具三塊，並同步其被指涉之語。

    所削者皆「以案查案」之附具，數據另有所在（第六章定位行、第七章綁定台帳），
    削之不傷義理；唯削後印面凡稱指此三塊之語皆須隨動，否則成死指。
    口徑：每一關鍵語須恰中一次——不中或重中即硬報寧可使建置失敗，
    不可靜默跳過而留下半削之冊（歷輪『假綠』之教）。定本一律不動。"""
    if MODE != "slim":
        return lines
    cuts = [(3, u"第二節　五維立體檢索樞紐"),
            (3, u"第五節　全書百則基準檢索總表"),
            (4, u"四、29 則複統攝深水案例")]
    edits = [(u"——宏觀檢索樞紐、生命之樹生態全景與實體收束閉環",
              u"——生命之樹生態全景與實體收束閉環"),
             (u"### 第三節　八大正理統攝矩陣與 29 則複統攝深水稱重法式",
              u"### 第三節　八大正理統攝矩陣與 29 則複統攝"),
             (u"第七章總表是『以案查心』之歸處", u"第七章綁定台帳是『以案查心』之歸處"),
             (u"第七章的『五維速查』，降維交接為", u"第七章的『正理對位台帳』，降維交接為"),
             (u"> 深研**天平稱重之法（第三節）**，徹見主觀動機與客觀底線在深水區如何嚴密咬合；",
              u"> 深研**八大正理統攝之矩陣（第三節）**，徹見主觀動機與客觀底線如何嚴密咬合；"),
             (u"> 繼而循**四階終極壓縮（第四節）**，體會千經萬論如何消融於三十二字略戒；",
              u"> 繼而循**四階終極壓縮（第四節）**，體會千經萬論如何消融於三十二字略戒。")]
    dels = [u"> 次握**五維檢索之鑰（第二節）**",
            u"> 最後，將**百則基準台帳（第五節）**"]
    kill = []
    for lvl, key in cuts:
        got = [i for l, t, i in hs if l == lvl and key in t]
        if len(got) != 1:
            raise SystemExit(u"SLIM 削塊關鍵語命中 %d 次（須恰 1）：%s" % (len(got), key))
        i = got[0]
        end = next((i2 for l2, _t, i2 in hs if i2 > i and l2 <= lvl), len(lines))
        kill.append((i, end, lvl, key))
    for i, end, lvl, key in sorted(kill, reverse=True):
        del lines[i:end]
        print(u"  精簡本削塊：H%d「%s」%d 行" % (lvl, key, end - i))
    for old, new in edits:
        n = sum(1 for l in lines if old in l)
        if n != 1:
            raise SystemExit(u"SLIM 隨改命中 %d 次（須恰 1）：%s" % (n, old[:30]))
        lines = [l.replace(old, new) if old in l else l for l in lines]
    for pre in dels:
        idx = [i for i, l in enumerate(lines) if pre in l]
        if len(idx) != 1:
            raise SystemExit(u"SLIM 隨刪命中 %d 次（須恰 1）：%s" % (len(idx), pre[:30]))
        del lines[idx[0]]
    print(u"  精簡本隨動：改 %d 處、刪 %d 行（死指已塞）" % (len(edits), len(dels)))
    return lines


def collect_headings(lines, deep=3):
    """目錄收錄：H1 章／附錄、H2、H3。"""
    in_toc, hs = False, []
    for i, ln in enumerate(lines):
        if ln.startswith("## " + TOC_H2) or ln.strip() in ("## 目錄", "### 目錄"):
            in_toc = True
            continue
        if in_toc and ln.strip().startswith("# 第一章"):
            in_toc = False
        m = re.match(r"^(#{1,%d})\s+(.*)$" % deep, ln)
        if not m:
            continue
        if in_toc:
            continue
        hs.append((len(m.group(1)), m.group(2).strip(), i))
    return hs


# 置於目錄之前者不列（無法以正文頁碼表示）：卷首三卷
TOC_SKIP_PREFIX = ("【開卷總提撕】", "【卷首憲綱", "【卷首導讀",
                   "卷頭：", "第一篇：四大編撰憲章", "第二篇：", "第三篇：")
TOC_SKIP_UNTIL_CHAPTER = True


def skip_in_toc(lvl, title):
    if TOC_SKIP_UNTIL_CHAPTER and any(title.startswith(p) for p in TOC_SKIP_PREFIX):
        return True
    return False


# 點線目錄：以 monospace 點字元模擬 leader，對齊由 1ch 網格保證
# 目錄點線：以「字寬單位」精算，整行統一 CJK 字型（見 print38.css 註）
# 容量之尺（第 165 輪以冊內實測重校）：舊註謂『10.3pt 時全形＝13.25pt』（比 1.286），
# 據此定 TOC_GRID＝64 而縮字 22 條、最細 8.4pt，與同頁鄰行之 11.8pt 判若兩冊。
# 今於印成之冊上量目錄 L3 行：22 全形占 259.2pt@11.82 ⇒ 全形＝1.00×字号（舊尺誤近一倍）。
# 字寬不復手抄：徑自正黑體檔讀 cmap/hmtx（實測破折號 1.08em、句點 0.23em、
# 拉丁 0.28–0.81em 各異——以 ord>0x2E80 判全形者，遇「——」即低估 0.08em×枚數，
# 冊上五行遂觸內容右界，故必以字型本檔為據）。讀不到檔則退回保守上界並印警語。
CONTENT_W_PT = 182 / 25.4 * 72       # 版寬：A4 減外 10mm／內 18mm（鏡像兩面同寬）
TOC_PAD_PT = {1: 0.0, 2: 18.75, 3: 37.5}   # .toc-lN 之 padding-left（1.5em／3em × 12.5pt）
PDF_PT_SCALE = 0.985                 # 印面實字級與 CSS 字級之比（冊內量得 13.4→13.2）
TOC_LINE_SIZE = 12.5                 # .toc-line 本級：點線與頁碼由此級排
TOC_MIN_SIZE = 10.5                  # 縮字之下限：再小即報警，不靜默印成細字
TOC_SAFE = 0.98                      # 估算與實排之安全閾：字寬雖自字型檔來，瀏覽器仍按
                                     #   裝置像素捨入（冊上實測殘差 0.5–0.6pt），留 2% 餘地
TOC_DOT_EM = 0.2385                  # 點線之『印面』字寬：冊上實測 29 點占 85.1pt@12.31
# ↑ 正黑體 hmtx 之句點為 0.230em，然無頭瀏覽器落盤時按裝置像素捨入，實排寬 0.2385em
#   （差 3.7%）。一行數十點，誤差即積至 2–3pt 而觸內容右界——故點線獨採實測值。
TOC_WIDE_FALLBACK = 1.08             # 字型檔讀不到時之保守上界
TOC_LABEL = {1: "", 2: "　　", 3: "　　　　"}
TOC_FONT = {"": ("msjh.ttc", 0), "bold": ("msjhbd.ttc", 0)}
_ADV_CACHE = {}


def _adv_table(bold=False):
    """由正黑體檔取 {碼位: 字寬(em)}；讀不到回 None（改用保守上界）。"""
    key = "bold" if bold else ""
    if key in _ADV_CACHE:
        return _ADV_CACHE[key]
    out = None
    fn, idx = TOC_FONT[key]
    for root in (os.environ.get("WINDIR", r"C:\Windows"), r"C:\Windows"):
        p = os.path.join(root, "Fonts", fn)
        if not os.path.isfile(p):
            continue
        try:
            from fontTools.ttLib import TTCollection, TTFont
            f = (TTCollection(p, lazy=True).fonts[idx] if p.endswith(".ttc")
                 else TTFont(p, lazy=True))
            upm = f["head"].unitsPerEm
            names = f["cmap"].getBestCmap()
            hmtx = f["hmtx"]
            out = {cp: hmtx[g][0] / upm for cp, g in names.items() if g}
        except Exception as e:                       # 字型不在或無 fontTools：退保守上界
            print("目錄字寬退回保守上界（%s 讀取失敗：%s）" % (fn, e))
            out = None
        break
    if out is None:
        print("目錄字寬退回保守上界：未找到 %s" % fn)
    _ADV_CACHE[key] = out
    return out


def _wpt(s, size, bold=False):
    """一行之實排寬（pt）：逐字符取字型檔字寬，未知者以全形上界計。"""
    tab = _adv_table(bold)
    if tab is None:
        return sum((TOC_WIDE_FALLBACK if ord(c) > 0x2000 else 0.85) * size for c in s)
    return sum(tab.get(ord(c), TOC_WIDE_FALLBACK) * size for c in s)


TOC_BASE_SIZE = {1: 13.4, 2: 12.4, 3: 12.0}  # 與 print38.css 各級 .t 字級對應


def toc_room(lvl):
    """該級目錄行可排之實寬（pt，已扣縮排與安全閾）。"""
    return (CONTENT_W_PT - TOC_PAD_PT.get(lvl, 37.5)) * TOC_SAFE


def toc_line(lvl, title, page):
    label = TOC_LABEL.get(lvl, "　　　　")
    pg = str(page) if page else ""
    base = TOC_BASE_SIZE.get(lvl, 12.0)
    bold = (lvl == 1)                       # .toc-l1 .t 為 700
    size = base * PDF_PT_SCALE
    room = toc_room(lvl)
    dot_w = TOC_DOT_EM * TOC_LINE_SIZE * PDF_PT_SCALE
    tail = _wpt(pg + " ", TOC_LINE_SIZE * PDF_PT_SCALE) if pg else 0.0
    head = _wpt(label + title, size, bold)
    style = ""
    dots_pt = room - head - tail
    if pg and dots_pt < 3 * dot_w:                       # 標題過長：縮字以保頁碼不被裁
        need = room - tail - 3 * dot_w
        k = need / head
        if base * k < TOC_MIN_SIZE:
            print("目錄條目過長，縮至 %.1fpt（低於下限 %.1f）：%s"
                  % (base * k, TOC_MIN_SIZE, title))
        size = size * k
        head = _wpt(label + title, size, bold)
        # 字級只可捨入向小：四捨五入向上則實排寬逾估寬，行尾反被裁（冊上實測 3.4pt）
        css_size = int(size / PDF_PT_SCALE * 10) / 10.0
        style = ' style="font-size:%.1fpt"' % css_size
        size = css_size * PDF_PT_SCALE
        head = _wpt(label + title, size, bold)
        dots_pt = room - head - tail
    dots = max(3, int(dots_pt / dot_w))
    cls = "toc-line toc-l%d" % lvl
    esc = title.replace("&", "&amp;").replace("<", "&lt;")
    return ('<p class="%s"><span class="t"%s>%s</span>'
            '<span class="d">%s </span><span class="pg">%s</span></p>'
            % (cls, style, label + esc, "." * dots, pg))


def _ckey(key):
    """目錄鍵 (級, 基底標題, 同名序) ↔ 字串：JSON 之鍵須為字串。"""
    return "%d|%s|%d" % key


def _ukey(s):
    a, b, c = s.split("|", 2)
    return (int(a), b, int(c))


def prepare_toc_entries(hs):
    """目錄條目正規化，回傳 [(lvl, 顯示標題, key)]（key 唯一，供頁碼回填）。

    1. 捨第一章之前的卷首 H2/H3（開卷總提撕／卷首憲綱／卷首導讀諸節）：
       它們落在正文錨點（BODY_ANCHOR，目錄佔位處）之前，頁碼恆為空，
       列出只會留下無頁碼的孤兒行。
    2. 同名標題消歧：第二個同名者加「（之N）」後綴，使重複標題仍可各自定位。
    """
    start = next((k for k, (lv, t, _) in enumerate(hs)
                  if lv == 1 and strip_md(t).startswith("第一章")), 0)
    counts, out = {}, []
    for lvl, title, _ in hs[start:]:
        base = strip_md(title).replace("|", "｜")
        n = counts.get((lvl, base), 0) + 1
        counts[(lvl, base)] = n
        disp = base if n == 1 else "%s（之%d）" % (base, n)
        out.append((lvl, disp, (lvl, base, n)))
    return out


def build_toc_html(entries, pages):
    """列出目錄行（entries 取自 prepare_toc_entries）。"""
    seen = set()
    rows = ['<div class="toc-lead">', "<h2>目　　錄</h2>"]
    for lvl, disp, key in entries:
        if disp == "目錄" or skip_in_toc(lvl, disp):
            continue
        if disp in seen:
            continue
        seen.add(disp)
        rows.append(toc_line(lvl, disp, pages.get(key)))
    rows.append("</div>")
    return rows


# ---- 出淨本之清創規則（CLEAN 模式专用：只動產物層，正本一字不動）------------------
# 取捨：削『案語・版次自述・詞頻清單・校勘口徑段』四類；**留**台帳表格（檢索工具，且為
#       書內指針之靶）與附錄 F-3（削之則『已列附錄F-3』諸指針成懸指）。
CLEAN_SPANS = [
    (u"案語〔案：〕", re.compile(u"〔案：[^〕\n]*〕")),
    (u"案語〔編者按〕", re.compile(u"〔編者按：[^〕\n]*〕")),
    (u"版次『於第N版…時』", re.compile(u"[，、]?於第[一二三四五六七八九十百]{1,4}版[^，。；\n]{0,14}時")),
    (u"版次『依第N版』", re.compile(u"依第[一二三四五六七八九十百]{1,4}版")),
]
CLEAN_DROPS = [
    (u"詞頻括註", re.compile(u"^（?諸數皆字頻|（諸數皆字頻[^）]*）")),
    (u"校勘口徑段", re.compile(r"^\s*\*\s\*\*〔口徑定義|^\s*\*\s\*\*統計口徑之檢索式")),
    (u"詞頻清單", re.compile(r"出現次數為|一語出現 9\d 次|出現 9\d 次之多")),
    (u"升格梯隊條", re.compile(r"^\s*\*\s\*\*第[一二三]梯隊")),
    (u"附錄升格自述", re.compile(r"^>?\s*本書於第[三四五六七八九十]{1,3}版")),
]


def apply_clean_cuts(lines):
    """出淨本：先削行內案語與版次自述之 span，再削整行的詞頻清單與校勘口徑段。
    凡削後只餘 markdown 骨架（空行、`>`、`-`、`*`、序號）之行一併除之；逐則報命中數。"""
    tally = {}
    for name, _rx in CLEAN_SPANS + CLEAN_DROPS:
        tally[name] = 0
    out = []
    for l in lines:
        s = l
        for name, rx in CLEAN_SPANS:
            s2, n = rx.subn(u"", s)
            if n:
                tally[name] += n
                s = s2
        if not s.strip() and l.strip():
            tally[u"（骨架行隨削而除）"] = tally.get(u"（骨架行隨削而除）", 0) + 1
            continue
        drop = False
        for name, rx in CLEAN_DROPS:
            if rx.search(s):
                tally[name] += 1
                drop = True
                break
        if drop:
            continue
        out.append(s)
    print(u"出淨本清創：" + u"｜".join(u"%s %d" % (k, v) for k, v in tally.items() if v))
    print(u"  行 %d → %d（削 %d 行）" % (len(lines), len(out), len(lines) - len(out)))
    return out


def write_md(lines, hs, pages):
    """以點線目錄（HTML）取代卷首標準目錄整段（含舊目錄清單）。"""
    s = next((i for i, l in enumerate(lines)
              if l.startswith("## " + TOC_H2) or l.strip() in ("## 目錄", "### 目錄")), None)
    if s is None:
        body = lines
    else:
        e = next((i for i in range(s + 1, len(lines))
                  if re.match(r"^#{1,2}\s", lines[i])), len(lines))
        body = lines[:s] + ["<!--TOC-PLACEHOLDER-->", "",
                            BODY_ANCHOR, ""] + lines[e:]
    # 為「開卷總提撕」掛 id，供 CSS 重置正文頁碼（封面不編碼、目錄用羅馬數字）
    body = [l.replace("## 【開卷總提撕】",
                       '<h2 id="opening-note">【開卷總提撕】</h2>', 1)
            if l.startswith("## 【開卷總提撕】") else l for l in body]
    if MODE == "slim":
        k = next((i for i, l in enumerate(body) if l.startswith("## 【卷首導讀")), 1)
        body = body[:k] + [SLIM_NOTE, ""] + body[k:]
        # 精簡本唯隨 A、B 二篇：凡正文指往不隨冊之附錄者，改標『定本附錄X』，
        # 免冊內讀者按圖索驥而落空（存檔聲明自身已說明分冊，故略之）。
        # 「附錄」與字母間容有空白（全書百有六處），故 \s* 與查核器同一口徑。
        off = re.compile(u"(?<!定本)附錄\\s*([CDEFGHIJKLM])")
        body = [l if l == SLIM_NOTE else off.sub(u"定本附錄\\1", l) for l in body]
    open(MD, "w", encoding="utf-8").write("\n".join(body))


def _cw(s):
    s = re.sub(r"(?s)<[^>]+>", "", s)
    s = s.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    return sum(2 if ord(ch) > 0x2E80 else 1 for ch in s)


CAP = 104.0
PAD = 2.4


def _table_height(ws, rows):
    total = 0
    for u in rows:
        ln = 1
        for i, x in enumerate(u):
            cap = ws[i] / 100.0 * CAP - PAD
            if cap <= 0.5:
                return 10 ** 9
            e = int((x + 0.4) / cap)
            if (x + 0.4) - e * cap > 1e-9:
                e += 1
            if e > ln:
                ln = e
        total += ln
    return total


def retune_tables(html, mode="content", power=0.5):
    if mode == "keep":
        return html

    def fix(m):
        tb = m.group(0)
        rows = re.findall(r"(?s)<tr>(.*?)</tr>", tb)
        cells = [re.findall(r"(?s)<t[hd][^>]*>(.*?)</t[hd]>", r) for r in rows]
        n = max((len(c) for c in cells), default=0)
        if n < 2:
            return tb
        if mode == "auto":
            return re.sub(r"(?s)<colgroup[^>]*>.*?</colgroup>\s*", "", tb)
        units = [[_cw(c) for c in cs] + [0] * (n - len(cs)) for cs in cells]
        sums = [sum(u[i] for u in units) for i in range(n)]
        w = [max(s, 6.0) ** power for s in sums]
        tot = sum(w)
        lo = 6.0
        ws = [x / tot * 100.0 for x in w]
        # 標籤欄之可讀下限（第 164 輪據產物層改）：舊唯設全表下限 6%，而 CAP=104、PAD=2.4
        # 之下 6% 每行僅折 1.9 個漢字——『領域軸＼心智軸』『新編號』一類標籤欄遂一字一行。
        # 今令每行至少容該欄最長『短格』（≤24 半形單位，即標籤類之格）之半，且不少於四個漢字。
        fl = []
        for i in range(n):
            labs = [u[i] for u in units if 0 < u[i] <= 24]
            wide = 8.0 if not labs else max(8.0, min(max(labs) / 2.0, 12.0))
            fl.append(max(lo, (wide + PAD) / CAP * 100.0))
        if sum(fl) > 92.0:                       # 欄多而下限總和過高時按比例退讓，唯不破全表下限
            k = 92.0 / sum(fl)
            fl = [max(lo, x * k) for x in fl]
        for _ in range(8):
            over = [i for i in range(n) if ws[i] < fl[i]]
            if not over:
                break
            under = sorted((i for i in range(n) if i not in set(over)), key=lambda i: -(ws[i] - fl[i]))
            for i in over:
                need = fl[i] - ws[i]
                for j in under:
                    take = min(need, ws[j] - fl[j])
                    if take <= 0:
                        continue
                    ws[j] -= take
                    ws[i] += take
                    need -= take
                    if need <= 1e-9:
                        break
        best = _table_height(ws, units)
        if len(units) >= 4 and n >= 3:
            for _ in range(40):
                moved = False
                for i in range(n):
                    for j in range(n):
                        if i == j or ws[j] - 2.0 < fl[j]:
                            continue
                        trial = ws[:]
                        trial[i] += 2.0
                        trial[j] -= 2.0
                        h = _table_height(trial, units)
                        if h < best - 1e-9:
                            ws, best, moved = trial, h, True
                if not moved:
                    break
        new = "<colgroup>" + "".join(
            '<col style="width: %.1f%%" />' % p for p in ws) + "</colgroup>"
        if "<colgroup" in tb:
            return re.sub(r"(?s)<colgroup[^>]*>.*?</colgroup>", lambda _m: new, tb, count=1)
        return re.sub(r"(<table[^>]*>)", lambda _m: _m.group(1) + new, tb, count=1)

    return re.sub(r"(?s)<table[^>]*>.*?</table>", fix, html)


def fit_pre_blocks(html):
    """依每段 pre 之最長顯示寬自動縮字；高度可容一頁者加 class="keep" 鎖為不跨頁。

    寬度單位同 _cw（CJK 與框線字符算 2、其餘算 1），Consolas 字寬約 0.55em，
    故所需字級 ≈ 版寬 ÷ (0.55×最長單位數 + 內邊)。    字級介於 6.2–11.8pt：
    再小則印場難讀，故超寬圖仍可能換行（今已 word-break: keep-all，換行只发生在空白處）。
    版寬取 A4 減左右各 10mm；一頁文字高約 774pt，留安全閾後以 700pt 為鎖頁上限。
    """
    from html import unescape as _un
    CONTENT_W = (210 - 20) / 25.4 * 72
    MAXF, MINF, LH, PAD, KEEP_H = 11.8, 6.2, 1.30, 1.6, 700.0

    def one(m):
        head, inner = m.group(1), m.group(2)
        txt = _un(re.sub(r"(?s)<[^>]+>", "", inner))
        lines = txt.split("\n")
        if not any(x.strip() for x in lines):
            return m.group(0)
        wmax = max(_cw(x) for x in lines)
        nl = sum(1 for x in lines if x.strip())
        size = min(MAXF, CONTENT_W / max(1.0, 0.55 * wmax + PAD))
        size = max(MINF, round(size, 2))
        fits = (nl * size * LH + 6) <= KEEP_H
        st = "font-size:%gpt;" % size
        if 'style="' in head:
            head = re.sub(r'style="([^"]*)"', lambda z: 'style="' + st + z.group(1) + '"', head)
        else:
            head = head[:-1].rstrip() + ' style="' + st + '">'
        if fits:                      # 帶 class 之圍欄框（sourceCode markdown 等）亦得鎖頁
            head = re.sub(r'class="([^"]*)"', lambda z: 'class="' + z.group(1).strip() + ' keep"', head, count=1)
            if 'class="' not in head:
                head = head[:-1].rstrip() + ' class="keep">'
        return head + inner + m.group(3)

    out = re.sub(r"(?s)(<pre\b[^>]*>)(.*?)(</pre>)", one, html)
    n = len(re.findall(r"(?s)<pre\b[^>]*>", out))
    k = len(re.findall(r'<pre[^>]*class="[^"]*keep', out))
    # 細字之報：縮字下限 6.2pt 係『不換行』之代價，凡落於 9pt 以下者須讓建置日誌看見，
    # 免如第 165 輪之十六觀心決策圖，印至 8.2pt 而歷輪無一人知（親目方覺其細）。
    small = [float(x) for x in re.findall(r'<pre\b[^>]*?font-size:([\d.]+)pt', out) if float(x) < 9.0]
    print("pre 自動縮字：%d 段，其中鎖頁 %d 段%s"
          % (n, k, "；細於 9pt 者 %d 段（最細 %.1fpt）" % (len(small), min(small)) if small else ""))
    return out


# ── mermaid 圍欄 → 預渲染 SVG（第 244 輪·乙批之器）─────────────────────
# 字符畫成之圖，其字級由 fit_pre_blocks 縮到 8.1–8.2pt（第 165 輪之帳）。改以
# mermaid 源入冊者，於此預渲染為 SVG 再依版心縮放；圖內最小字級低於 MMD_FLOOR
# 即擲回整建——寧可紅給我看，不靜默印成無法卒讀之細字（承第 ㉛ 戒：尺先立）。
MMD_DIR = os.path.join(HERE, "_mmd")
MMD_CFG = os.path.join(HERE, "mmdcfg.json")
MMD_FLOOR = 8.1                    # pt：今冊最細實印字級即此數，圖不得更細
MMD_W_PT = CONTENT_W_PT            # 版寬（鏡像式外側 18mm 之最窄者）·同一法源
MMD_H_PT = 700.0                   # 鎖頁高度上限·同 fit_pre_blocks 之 KEEP_H


def _npx():
    for c in ("npx.cmd", "npx"):
        p = shutil.which(c)
        if p:
            return p
    raise SystemExit("找不到 npx：無法渲染 mermaid 圍欄。寧可不印，不可把圖源原樣印進冊子。")


def _mmd_render(src):
    """mermaid 源 → (雜湊, SVG 字串)；快取於 _print/_mmd/，同圖不重渲。"""
    import hashlib
    key = hashlib.sha1(src.encode("utf-8")).hexdigest()[:16]
    svg = os.path.join(MMD_DIR, key + ".svg")
    if not os.path.exists(svg):
        if not os.path.isdir(MMD_DIR):
            os.makedirs(MMD_DIR)
        mmd = os.path.join(MMD_DIR, key + ".mmd")
        with open(mmd, "w", encoding="utf-8") as f:
            f.write(src)
        pptr = os.path.join(MMD_DIR, "pptr.json")
        with open(pptr, "w", encoding="utf-8") as f:
            json.dump({"executablePath": find_browser().replace("\\", "/"),
                       "headless": True,
                       "args": ["--no-sandbox", "--disable-gpu"]}, f)
        env = dict(os.environ, PUPPETEER_SKIP_DOWNLOAD="1")
        try:
            subprocess.run([_npx(), "-y", "@mermaid-js/mermaid-cli", "-i", mmd, "-o", svg,
                            "-c", MMD_CFG, "-p", pptr],
                           check=True, env=env, timeout=600,
                           stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        finally:
            if os.path.exists(mmd):
                os.remove(mmd)
    return key, open(svg, encoding="utf-8").read()


def _mmd_fit(key, svg):
    """SVG → (印面寬 mm, 印面高 mm, 圖內最小字級 pt, 改過 id 範圍與本幅之 SVG)。

    1px = 0.75pt；字級取圖內一切 font-size 之最小值（標籤細於框，故取全局最小）。
    svg 之 id 改名，免同頁兩圖之 CSS 選擇器與 defs 相撞。"""
    num = lambda m, gi: float(m.group(gi)) if m else 0.0
    mvb = re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', svg)
    wpx = num(re.search(r'<svg[^>]*\bwidth="([\d.]+)', svg), 1) or num(mvb, 1)
    hpx = num(re.search(r'<svg[^>]*\bheight="([\d.]+)', svg), 1) or num(mvb, 2)
    if not (wpx and hpx):
        raise SystemExit("mermaid 圖 %s：讀不到本幅（無 width/height 亦無 viewBox）" % key)
    fs = [float(x) for x in re.findall(r'font-size:\s*([\d.]+)px', svg)]
    fs += [float(x) for x in re.findall(r'\bfont-size="([\d.]+)"', svg)]
    if not fs:
        raise SystemExit("mermaid 圖 %s：圖內讀不出字級" % key)
    scale = min(MMD_W_PT / (wpx * 0.75), MMD_H_PT / (hpx * 0.75), 1.0)
    wmm = wpx * 0.75 * scale / 72 * 25.4
    hmm = hpx * 0.75 * scale / 72 * 25.4
    uid = "mmd" + key
    seen = "".join(re.findall(u'[一-鿿]', svg))
    out = svg.replace("my-svg", uid)
    if "".join(re.findall(u'[一-鿿]', out)) != seen:
        raise SystemExit("mermaid 圖 %s：id 改名動到漢字內容（理應只及選擇器與 defs）" % key)
    out = re.sub(r'<svg([^>]*)>',
                 lambda m: '<svg%s width="%.1fmm" height="%.1fmm"'
                             ' preserveAspectRatio="xMidYMid meet">'
                 % (re.sub(r'\s(style|width|height)="[^"]*"', "", m.group(1)), wmm, hmm),
                 out, count=1)
    return wmm, hmm, min(fs) * 0.75 * scale, out


def inline_mermaid(html):
    """<pre class="mermaid"><code>…</code></pre> → 就地 SVG；圖過大即拒印。"""
    from html import unescape as _un
    if '<pre class="mermaid"' not in html:
        print("mermaid 圖：0 座（印面無 mermaid 圍欄，此步不觸發）")
        return html
    n, bad = 0, []

    def one(m):
        nonlocal n
        key, raw = _mmd_render(_un(m.group(1)).strip("\n"))
        if "my-svg" in _un(m.group(1)):
            raise SystemExit("mermaid 圖 %s：圖源內含 my-svg 字串，與 id 改名相犯，請改其 label。" % key[:8])
        wmm, hmm, eff, scoped = _mmd_fit(key, raw)
        if eff < MMD_FLOOR:
            bad.append("%s｜%.0f×%.0fmm｜圖內最小 %.1fpt＜%.1fpt"
                       % (key[:8], wmm, hmm, eff, MMD_FLOOR))
            return m.group(0)
        n += 1
        return '<div class="mmdfig keep" id="fig-%s">%s</div>' % (key[:8], scoped)

    out = re.sub(r'(?s)<pre class="mermaid"[^>]*><code>(.*?)</code></pre>', one, html)
    if bad:
        raise SystemExit("mermaid 圖置入版心後字級破下限，拒印：\n  " + "\n  ".join(bad)
                         + "\n→ 少框數、縮短標籤以減本幅；否則留 ASCII 圍欄。")
    print("mermaid 圖：%d 座嵌入（版心 %.0fpt×%.0fpt・字級下限 %.1fpt）"
          % (n, MMD_W_PT, MMD_H_PT, MMD_FLOOR))
    return out


def nowrap_case_ids(html):
    r"""案號〔遮NN〕〔開NN〕〔僧NN〕〔遺NN〕〔補遺NN〕不可折行——根治總表編號欄折成兩行（第 105 輪）。

    只動 pre／code 以外之文字節點，免亂 ASCII 圖之欄對齊。"""
    parts = re.split(r"(?s)(<pre.*?</pre>|<code.*?</code>)", html)
    idre = re.compile(u"[〔](遮|開|僧|遺|補遺|調部深描 ?)([0-9]{1,3})[〕]")
    n = 0
    for i in range(0, len(parts), 2):
        seg = parts[i]
        if not seg:
            continue
        seg, c = idre.subn(lambda m: u'<span class="nb">〔' + m.group(1) + m.group(2) + u"〕</span>", seg)
        n += c
        parts[i] = seg
    print("案號不可折行：%d 處包 span.nb" % n)
    return "".join(parts)


def quote_keep(html, max_chars=120):
    """標籤式小框整體禁跨頁：起首帶標籤（粗體或【／〔）且全文 <= max_chars 者掛 keep。

    只治『框題孤留頁底』一症——三兩行的檢核框、四問框被撕裂最難看，整框下推僅費數行。
    舊閘放至 650 字，遂將 160 段引用框盡數鎖死，於體例無據（長框理當跨頁，書中無一處如此），故收之。
    第七十八輪實測：鎖頁由 160 段削至 41 段，精簡本僅由 295 頁減為 294 頁——冊身之膨不在這裡，
    而在 `PRINT_CSS` 之全版字級覆寫（內文 +1pt、表格 +1.9pt），後人勿再以本閘為省頁之計。
    斷頭之虞由 CSS 之 orphans/widows 守。
    """
    from html import unescape as _un

    def one(m):
        head, inner = m.group(1), m.group(2)
        if "class=" in head:
            return m.group(0)
        if re.search(r"<(table|pre)[\s>]", inner):
            return m.group(0)
        body = inner.lstrip()
        txt = _un(re.sub(r"(?s)<[^>]+>", "", inner)).strip()
        if len(txt) > max_chars:
            return m.group(0)
        if not (body.startswith("<strong>") or txt[:1] in ("【", "〔", "〖")):
            return m.group(0)
        return head[:-1].rstrip() + ' class="keep">' + inner + m.group(3)

    out = re.sub(r"(?s)(<blockquote\b[^>]*>)(.*?)(</blockquote>)", one, html)
    k = len(re.findall(r"<blockquote[^>]*class=\"keep\"", out))
    print("blockquote 鎖頁：%d 段標籤小框掛 keep（整體禁跨頁）" % k)
    return out


def table_keep(html, max_rows=9, max_chars=1500):
    r"""整體禁跨頁之表：小表（列數 <= max_rows）或一頁可容之表（列數 <= 18 且正文 <= max_chars 字）。

    對應 P15-16 三十二字對稱表首行孤留頁底、九章 15 項自檢表被攔腰折斷之類：整表下推至次頁。
    長表（第七章百則總表、附錄K 三頁總表之類）仍准跨頁，表頭由 thead 逐頁重現。"""

    def ok(tb):
        rows = len(re.findall(r"<tr>", tb))
        nch = len(re.sub(r"(?s)<[^>]+>", "", tb))
        return rows <= max_rows or (rows <= 18 and nch <= max_chars)

    def fix(m):
        tb = m.group(0)
        head = tb[: tb.find(">") + 1]
        if not ok(tb):
            return tb
        if "class=" in head:
            return re.sub(r'class="([^"]*)"',
                          lambda z: 'class="' + z.group(1).strip() + ' keep"', tb, count=1)
        return re.sub(r"<table([^>]*)>", r'<table\1 class="keep">', tb, count=1)

    out = re.sub(r"(?s)<table[^>]*>.*?</table>", fix, html)
    k = len(re.findall(r'<table[^>]*class="[^"]*keep', out))
    print("table 鎖頁：%d 張表掛 keep（整體禁跨頁）" % k)
    return out



def pali_span(html):
    r"""梵巴轉寫之含變音符者，整詞包 `<span class="pali">`——免粗體時逐字落別家字型。

    病（第 132 輪印面實測）：粗體語境之 `Manasikāra`、`Mānattaciṇṇa` 由微軟正黑粗體排拉丁、
    ā/ṇ 等卻 fallback 至別家，字距參差，紙上作 `Manasik ā ra`。
    只動 pre／code 以外之文字節點；詞內須至少含一枚變音符方包，免無謂標記。
    """
    DIAC = u"\u00c0-\u024f\u1e00-\u1eff"   # 含 Latin-1（ñ 之屬），免 Saṃjñā 被鋸成兩段
    word = re.compile(u"[" + DIAC + u"A-Za-z]" + u"[" + DIAC + u"A-Za-z." + chr(0x5C)*2 + u"-]*")
    has = re.compile(u"[" + DIAC + u"]")

    def one(seg):
        return word.sub(lambda m: (u'<span class="pali">%s</span>' % m.group(0))
                        if has.search(m.group(0)) and u'<' not in m.group(0) else m.group(0), seg)

    parts = re.split(r"(?s)(<pre.*?</pre>|<code.*?</code>)", html)
    out = []
    for i, p in enumerate(parts):
        if i % 2 == 1:
            out.append(p)
            continue
        segs = re.split(r"(<[^>]+>)", p)          # 標籤原樣保留，只改文字段
        out.append(u''.join(t if t.startswith(u'<') else one(t) for t in segs))
    res = u''.join(out)
    print(u"梵巴變音符包 span：%d 處" % res.count(u'<span class="pali">'))
    return res


def scrub_ctrl(html):
    r"""護欄自癒：後處理字串若混入控制字元，會靜默改寫標籤名而令整張表散架。

    第 105 輪 table_keep 之複寫字串曾落下 \x01，遂成 <table\x01 class="keep">——
    解析器視之為未知標籤，td/th 全數丟棄，三十四張表於印面化為一團連寫文字。
    故寫入前一律剔除 \x00-\x08、\x0b、\x0c、\x0e-\x1f（留 \t\n\r），並如實報數。"""
    bad = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
    n = len(bad.findall(html))
    if n:
        print("剔除控制字元：%d 處（否則標籤名被改寫，表格散架）" % n)
        html = bad.sub("", html)
    return html


# 全版字級間距覆寫（後勝先；影印／螢幕共用，不分版）：
# 內文 12.2→13.2pt（+1pt）、標題同步 +1pt 保層級（h4 14.0 仍大於內文）、
# 表格 10.3→12.2pt（貼近內文）、段距行距同步收緊抵銷增頁。
PRINT_CSS = """
/* —— 全版字級間距覆寫（build38.py 自動附加，兩版共用）—— */
html { font-size: 13.2pt; }
body { line-height: 1.28; }
body > h1, h1 { font-size: 23.4pt; }
h1 + p { margin: 0 0 .9em; }
h2 { font-size: 18.2pt; margin: .6em 0 .35em; padding: .2em .45em; }
h3 { font-size: 15.0pt; margin: .45em 0 .28em; }
h4 { font-size: 14.0pt; margin: .4em 0 .22em; }
h5, h6 { font-size: 13.4pt; margin: .4em 0 .2em; }
p { margin: .2em 0; }
blockquote { margin: .3em 0; padding: .26em .6em; }
ul, ol { margin: .18em 0 .18em 1.35em; }
li { margin: .06em 0; }
table { font-size: 12.2pt; line-height: 1.25; margin: .25em 0; }
pre { font-size: 11.6pt; line-height: 1.30; margin: .3em 0; padding: .3em .5em; }
hr { margin: .6em 0; }
"""


def audit_headings(md_path, html_path):
    """源 md 之每一行標題都須在成册 HTML 中化為**同級** `<hN>` 元素。

    pandoc 之 simple table 口徑會把相鄰區塊（註解＋H1＋H2）吞成一欄表格，
    徵狀為印面出現字面 `#`、副題整行消失——此病只在看册時才見，故在此以
    產物自證：不複用渲染器之假設，逕向 HTML 數元素。
    """
    from html import unescape
    norm = lambda s: re.sub(r"\s+", "", unescape(re.sub(r"<[^>]+>", "", s))).replace("*", "").replace("`", "")
    pool = {}
    for m in re.finditer(r"<h([1-6])(\s[^>]*)?>(.*?)</h\1>", open(html_path, encoding="utf-8").read(), re.S | re.I):
        pool.setdefault(int(m.group(1)), []).append(norm(m.group(3)))
    fence, bad, nmd = False, [], 0
    lines = open(md_path, encoding="utf-8").read().replace("\r\n", "\n").split("\n")
    for i, l in enumerate(lines):
        if re.match(r"^\s*(```|~~~)", l):
            fence = not fence
            continue
        if fence:
            continue
        m = re.match(r"^(#{1,6})\s+(\S.*)$", l.strip())
        if not m:
            continue
        nmd += 1
        lv, t = len(m.group(1)), norm(m.group(2))
        if not any(t in x for x in pool.get(lv, [])):
            bad.append(u"L%d(h%d)%s" % (i + 1, lv, t[:22]))
    if bad:
        raise SystemExit(u"HTML 標題漏失 %d 處：%s｜疑為 pandoc 表格吞區" % (len(bad), u"；".join(bad[:6])))
    print(u"  標題覆核：源 %d 行俱化為同級元素｜册內 h1..h6 = %s"
          % (nmd, [len(pool.get(k, [])) for k in range(1, 7)]))


def render_html(toc_html):
    subprocess.run(
        [PANDOC, MD, "-f", "markdown-yaml_metadata_block+pipe_tables+raw_html-blank_before_header", "--no-highlight",   # 圍欄標了 ```markdown／```text 時 pandoc 會去『高亮』它——
        #   實測存檔卡內『1.』『[ ]』兩行被當成 markdown 清單標記，
        #   遂上色（#bb6688／#60a0b0）並轉斜體，表單之莊齊盡失（第 132 輪印面實測）。
        "-t", "html5", "-s",
         "--metadata", "lang=zh-Hant", "-c", CSS_FILE, "-o", HTML],
        check=True, cwd=HERE)
    html = open(HTML, encoding="utf-8").read()
    css = open(os.path.join(HERE, CSS_FILE), encoding="utf-8").read()
    if SCREEN:
        # 螢幕版覆寫（後勝先）：對稱邊距＋章連續起頁。
        # 鏡像邊距與奇頁起排只為雙面裝訂服務；螢幕直讀時它們只會造成
        # 「偶數頁偏左」與無謂空白頁，故在此一併關閉。
        css += ("\n/* —— 螢幕版覆寫（build38.py 自動附加）—— */\n"
                "@page { margin: 10mm 14mm 14mm 14mm; }\n"
                "@page :left { margin: 10mm 14mm 14mm 14mm; }\n"
                "@page :right { margin: 10mm 14mm 14mm 14mm; }\n"
                "h1 { break-before: page; }\n"
                "h1.appendix-start { break-before: page; }\n")
    css += "\n" + PRINT_CSS
    cover = (COVER.replace("__EDITION__", EDITION)
             .replace("__APPS__", APPS).replace("__META__", book_meta()))
    assert "<!--TOC-PLACEHOLDER-->" in html, "未定位目錄佔位"
    html = html.replace("<!--TOC-PLACEHOLDER-->", "\n".join(toc_html))
    # 舊「<p>【正文起點】</p> 加 class=body-anchor」之置換已除：標記今為 HTML 註解，不生元素
    html = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + "\n" + cover, html, count=1)
    # 卷首（開卷總提撕～凡例末）與目錄同屬前置內容，一併改用羅馬頁碼：
    # 舊況為『卷首阿拉伯→目錄羅馬→正文阿拉伯』三段反復，屬分節設定未整之典型瑕疵。
    # 目錄條目本不含卷首（prepare_toc_entries 自第一章起列），故頁碼回填无需變動。
    html = html.replace('<h2 id="opening-note">', '<div class="fm">\n<h2 id="opening-note">', 1)
    html = html.replace('<div class="toc-lead">', '</div>\n<div class="toc-lead">', 1)
    # pandoc 會把小寫化後的錨點寫進 id（附錄A → 附錄a-…），故以大小寫無關比對；
    # 長標題時 pandoc 會把 <h1 與 id 斷行（<h1\nid=…>），故空白以 \s+ 匹配
    html = re.sub(r'<h1(\s+)id="(附錄[a-zA-Z][^"]*)"\s*>',
                  r'<h1\1class="appendix-start" id="\2">', html)
    html = inline_mermaid(html)
    html = retune_tables(html, TBLW, TBLW_POW)
    html = table_keep(html)
    html = nowrap_case_ids(html)
    html = quote_keep(html)
    html = fit_pre_blocks(html)
    html = pali_span(html)
    html = scrub_ctrl(html)
    open(FINAL, "w", encoding="utf-8").write(
        html.replace('<link rel="stylesheet" href="%s" />' % CSS_FILE,
                     "<style>\n" + css + "\n</style>"))
    audit_headings(MD, FINAL)


def find_pandoc():
    """pandoc 執行檔：PATH → winget 套件目錄 → 常見安裝處；全不可得即明報。

    本機 pandoc 係 winget 套件（JohnMacFarlane.Pandoc_pandoc-3.11），其目錄未必在
    非登入式 shell 之 PATH 上——後台建置曾因此四式齊飛 rc=1（附錄M 第 83 條）。
    """
    import glob
    import shutil
    w = shutil.which("pandoc")
    if w:
        return w
    pats = [
        os.path.join(os.path.expandvars(r"%LOCALAPPDATA%"), "Microsoft", "WinGet", "Packages",
                      "JohnMacFarlane.Pandoc*", "pandoc-*", "pandoc.exe"),
        os.path.join(os.path.expandvars(r"%LOCALAPPDATA%"), "Pandoc", "pandoc.exe"),
        r"C:\Program Files\Pandoc\pandoc.exe",
        r"C:\Program Files (x86)\Pandoc\pandoc.exe",
    ]
    for pat in pats:
        for hit in sorted(glob.glob(pat), reverse=True):
            if os.path.isfile(hit):
                return hit
    raise SystemExit("找不到 pandoc 執行檔（請裝 pandoc 或於 PATH 標明其位）；現試過：%s" % pats[0])


PANDOC = find_pandoc()

def find_browser():
    """尋找系統中的 Edge 或 Chrome"""
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    # 如果路徑不在上述位置，嘗試直接呼叫環境變數
    return "msedge"


# ── 產品層之書籤與書訊（第 131 輪）──────────────────────────────
# 無頭 Chromium 列印不產 PDF 大綱（實測四式 get_toc() 皆 0 條），而 title 默認洩用
# 中介檔名（實測作「ver39_列印版」）。395 頁之冊無書籤，螢幕讀者無導航可用，故補之。
# 大綱之頁碼**不信 pages 表而另以冊內定位**：於 hint±1 頁中搜標題之正規化字串，
# 搜得者方入大綱（生成器與驗收器不同口徑，承第 90 輪之教）。

BOOK_TITLE = u"四分律起心動念心智分析框架"
CROWN = (u"完整版" if MODE == "full" else u"精簡本") + (u"·螢幕版" if SCREEN else u"·影印版")
META = {
    "title": u"%s｜%s｜%s" % (BOOK_TITLE, EDITION, CROWN),
    "author": u"編者",
    "subject": SUBTITLE,
    "keywords": u"四分律；毘奈耶；心所；戒相；僧團治理；大正藏 No.1428；No.1429",
    "creator": u"build38 管線（pandoc → 無頭 Chromium 列印）",
    "producer": u"build38",
}


def build_outline(doc, entries, pages):
    """由目錄條目在**已印出之冊**中定位各標題之物理頁碼（1 起），回傳 [層級, 標題, 頁]。"""
    import re as _r
    norm = lambda s: _r.sub(r"\s+", u"", s)
    cache = {}
    out, seen, miss, dup = [], set(), [], []
    for lvl, disp, key in entries:
        if disp == u"目錄" or skip_in_toc(lvl, disp):
            continue
        # 去重之鑰須含**層級**：舊唯以 `disp` 為鑰，遂把**同名跨級**者（第六章九個組題之 H2
        # 與附錄四mirror 其題之 H3）盡數靜默擲去，而印出之目錄仍列 221 行——
        # 『定位失敗未入者 0』與『大綱少九條』同時為真（自驗之數不.cover 跳過之數）。
        if (lvl, disp) in seen:
            dup.append(disp[:16])
            continue
        seen.add((lvl, disp))
        hint = pages.get(key)
        if not hint:
            miss.append(disp[:14])
            continue
        target = norm(disp)[:12]
        wide = norm(disp)[:20]       # 同 scan_pages：（上）（下）之雙 H1 前十二字全同
        got = None
        for tg in ([wide, target] if wide != target else [target]):
            for cand in range(int(hint) - 2, int(hint) + 2):
                if cand < 0 or cand >= doc.page_count:
                    continue
                if cand not in cache:
                    cache[cand] = norm(doc[cand].get_text())
                if tg and tg in cache[cand]:
                    got = cand + 1
                    break
            if got is not None:
                break
        if got is None:
            miss.append(disp[:14])
            continue
        out.append([1 if lvl <= 1 else (2 if lvl == 2 else 3), disp[:70], got])
    # PDF 大綱之層級須自 1 起且每次至多降一級（PyMuPDF 強驗），故整形：
    # 目錄首項常是深一級的導讀篇，直接寫入即報 bad hierarchy level。
    fixed, prev = [], 0
    for lv, ti, pg in out:
        if not fixed:
            lv = 1
        elif lv > prev + 1:
            lv = prev + 1
        fixed.append([lv, ti, pg])
        prev = lv
    return fixed, miss, dup


def stamp_pdf(path, outline, meta):
    """增量寫入大綱與書訊：頁面物件與字形嵌位一概不動，頁數必仍相同。"""
    import pymupdf
    d = pymupdf.open(path)
    if outline:
        d.set_toc(outline)
        back = d.get_toc()
        if len(back) != len(outline):
            raise SystemExit(u"內嵌大綱覆核失敗：寫 %d 得 %d" % (len(outline), len(back)))
        pn = [t[2] for t in back]
        bad = next((i for i in range(1, len(pn)) if pn[i] < pn[i - 1] or pn[i] - pn[i - 1] > 60), None)
        if bad is not None:
            raise SystemExit(u"內嵌大綱頁碼非單調或跳躍：第 %d 條『%s』p%d（前一條『%s』p%d）｜前八：%s"
                             % (bad + 1, back[bad][1][:26], pn[bad], back[bad - 1][1][:26], pn[bad - 1], pn[:8]))
    d.set_metadata(meta)
    d.save(path, incremental=True, encryption=pymupdf.PDF_ENCRYPT_KEEP)
    d.close()


def docx_meta(path, meta):
    """DOCX 之 core.xml：dc:title／creator／subject／keywords（pandoc 預設留空，實測亦然）。"""
    import zipfile
    from xml.sax.saxutils import escape
    z = zipfile.ZipFile(path)
    names = z.namelist()
    parts = {n: z.read(n) for n in names}
    z.close()
    core = parts.get("docProps/core.xml")
    if core is None:
        return False
    s = core.decode("utf-8")
    reps = [(r"(<dc:title>)(.*?)(</dc:title>)", meta["title"]),
            (r"(<dc:creator>)(.*?)(</dc:creator>)", meta["author"]),
            (r"(<cp:keywords>)(.*?)(</cp:keywords>)", meta["keywords"])]
    for pat, val in reps:
        s = re.sub(pat, lambda m, v=val: m.group(1) + escape(v) + m.group(3), s, count=1)
    if "<dc:subject>" not in s:
        s = s.replace("</cp:coreProperties>", "<dc:subject>%s</dc:subject></cp:coreProperties>"
                      % escape(meta["subject"]))
    parts["docProps/core.xml"] = s.encode("utf-8")
    tmp = path + u".tmp"
    zo = zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED)
    for n in names:
        zo.writestr(n, parts[n])
    zo.close()
    os.replace(tmp, path)
    return True


def render_pdf():
    """以無頭瀏覽器列印 PDF。

    第七十六輪之關鍵修正：瀏覽器列印為**非同步落盤**——若與既有瀏覽器行程共用設定檔，
    命令會立即返回而 PDF 遲遲未寫（或仍為上一次之舊檔），於是「回填頁碼→再印→再掃」
    之收斂迴圈讀到髒檔，最後 `shutil.copyfile` 更把舊冊交付出去
    （徵狀：中介檔已更正而交付檔仍帶舊痕，頁數亦不相符）。今多重设防：
      一、每次另起獨立 `--user-data-dir`（絕不與桌面瀏覽器共用行程；第八十九輪量得
          同一臨時目錄連用三遍不省时，故不省此開銷）；
      二、刪舊檔後輪待新檔出現且大小連續三次不變（二百五十毫秒一探，總鐈 300 秒；
          舊法三十秒必誤判，實測落盤需 33～51 秒，見下方之量測記）；
      三、驗其修改時間晚於本次起印時刻；
      四、交付後再比產物與副本之大小與頁數。
    虛擬時鐈与合成器旗標之撤除見模組上方之量測記。
    """
    import shutil as _sh
    import tempfile as _tf
    import time as _t
    browser = find_browser()
    abs_html = os.path.abspath(FINAL).replace("\\", "/")
    file_url = "file:///" + abs_html
    if os.path.exists(PDF):
        os.remove(PDF)
    profile = _tf.mkdtemp(prefix="print-profile-")
    t0 = _t.time()
    cmd = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-extensions",
        "--user-data-dir=" + profile,
        "--no-pdf-header-footer",
        "--print-to-pdf=%s" % PDF,
        file_url,
    ]
    try:
        subprocess.run(cmd, check=True, cwd=HERE, timeout=1800)
    finally:
        pass
    # 等待落盤穩定。**實測（第 119 輪）**：`subprocess.run` 於父行程即返，PDF 乃由
    # 其無頭子行程延後寫入——同一冊四式各量得 33、43、49、51 秒，故舊法「六十探×五十
    # 毫秒＝三十秒」必在寫入前即判死（徵狀：產物明明在，腳本卻報「瀏覽器未產出」，
    # 且交付檔停留於上一版）。今改為以總時鐈為準（預設 300 秒，`RENDER_WAIT` 可調），
    # 二百五十毫秒一探，連續三次同大小方定，並把實耗時間印入日誌。
    budget = float(os.environ.get("RENDER_WAIT", "300"))
    deadline = t0 + budget
    last, same = -1, 0
    while _t.time() < deadline:
        try:
            sz = os.path.getsize(PDF)
        except OSError:
            sz = -1
        if sz > 0 and sz == last:
            same += 1
            if same >= 3:
                break
        else:
            same = 0
        last = sz
        _t.sleep(0.25)
    else:
        print(u"  落盤等待逾時：%.0f 秒內未見穩定產物（%s）" % (budget, os.path.basename(PDF)))
    _sh.rmtree(profile, ignore_errors=True)
    if not os.path.exists(PDF):
        raise SystemExit("列印失敗：瀏覽器未產出 %s（本次已待 %.0f 秒）"
                         % (os.path.basename(PDF), _t.time() - t0))
    print(u"  落盤：%s，用時 %.1f 秒" % (os.path.basename(PDF), _t.time() - t0))
    if os.path.getmtime(PDF) < t0 - 1:
        raise SystemExit("列印時序異常：產物早於本次起印，恐取到舊檔")

def scan_pages(entries):
    """以大字級 span 定位標題頁碼（entries 取自 prepare_toc_entries）。

    門檻須高於內文字級：內文 13.2pt，故取 14.5（H3 15.0 以上才收）。
    回傳之頁碼為 **PDF 絕對頁碼**，與頁腳 `counter(page)` 所印者同一口徑，
    直接寫入目錄，不再換算為正文相對頁碼
    （舊法令目錄號恆小於頁腳號一整個卷首）。
    """
    import pymupdf, re as _re
    TH = 14.5
    doc = pymupdf.open(PDF)
    big = []
    for p in range(doc.page_count):
        buf = []
        for b in doc[p].get_text("dict").get("blocks", []):
            for l in b.get("lines", []):
                for s in l.get("spans", []):
                    if s.get("size", 0) >= TH:
                        buf.append(s.get("text", ""))
        big.append(_re.sub(r"\s+", "", "".join(buf)))
    _nc = {}

    def norm(p):
        """全頁文字（去空白）——僅在大字級-span 未命中時才取，且逐頁記憶。"""
        v = _nc.get(p)
        if v is None:
            v = _re.sub(r"\s+", "", doc[p].get_text())
            _nc[p] = v
        return v

    pages, last = {}, 1
    for lvl, disp, key in entries:
        if disp == "目錄" or skip_in_toc(lvl, disp):
            continue
        if key in pages:
            continue                        # 同名重複標題：不重複定位
        probe = _re.sub(r"\s+", "", disp)
        short = probe[:8]                   # 舊尺：八字之頭
        long_ = probe[:20]                  # ver39 第七章／第八章各分（上）（下）兩 H1，
        #     其前八字全同（乃至前十二字皆同），舊尺遂以（上）之頁報（下）——目錄錯十頁、
        #     大綱覆核非單調而擲回。今先以長probe求之，求不著方退回舊尺：舊冊之行為一字不動。
        if not short:
            continue
        if lvl == 1:
            last = 1
        hit = None
        for pr in ([long_, short] if long_ != short else [short]):
            hit = next((p for p in range(last - 1, doc.page_count) if pr in big[p]), None)
            if hit is None:
                hit = next((p for p in range(last - 1, doc.page_count) if pr in norm(p)), None)
            if hit is not None:
                break
        if hit is not None:
            pages[key] = hit + 1
            last = hit + 1
    n = doc.page_count
    doc.close()
    return pages, n


def _quote_prefix(s):
    """取引文前綴（如 '>', '>>', '  > '），非引文回傳 ''。"""
    m = re.match(r"^(\s*(?:>\s*)+)", s)
    return m.group(1) if m else ""


def _inner(s):
    q = _quote_prefix(s)
    return s[len(q):] if q else s


def _is_blank_md(s):
    if s.strip() == "":
        return True
    # 引文空行：'>', '> ', '>>' 等
    return bool(re.match(r"^\s*(?:>\s*)+$", s))


def _is_list_md(s):
    t = _inner(s)
    return bool(re.match(r"^\s*(?:\d+[.)]|[-*+])\s+\S", t))


def _is_table_md(s):
    t = _inner(s).strip()
    return len(t) > 2 and t.startswith("|") and t.endswith("|")


def _is_fence_md(s):
    return _inner(s).strip().startswith("```")


def _is_heading_md(s):
    return bool(re.match(r"^#{1,6}\s", _inner(s).lstrip()))


def _blank_for(s):
    """依 cur 是否為引文，回傳 '' 或對應層級的引文空行。"""
    q = _quote_prefix(s)
    if not q:
        return ""
    gt = "".join(re.findall(r">", q))
    return (gt if gt else ">") + " "


def normalize_lists_tables(lines):
    """列印前正規化：在行列／表格／圍欄前後自動補空行。

    病因：原稿大量出現「段落＋換行＋1. 清單」中間無空行，
    pandoc 會把「1.」誤判為段落內文，輸出 <p>…： 1. … 2. …</p>
    壓成一整段（八重憲綱、唯一定文錨定聲明等 400 餘處皆屬此類）。
    引文內同理（'> 文字' 直連 '> - …'），需補 '> ' 空行。
    在已是行列／表格／標題／空行之後不重複插入，連續行列項之間不插入。
    """
    res, in_fence = [], False
    for ln in lines:
        if _is_fence_md(ln):
            if not in_fence and res and not _is_blank_md(res[-1]):
                res.append(_blank_for(ln))
            res.append(ln)
            in_fence = not in_fence
            continue
        if in_fence:
            res.append(ln)
            continue
        if _is_blank_md(ln) or _is_heading_md(ln):
            res.append(ln)
            continue
        if _is_list_md(ln) or _is_table_md(ln):
            if res and not _is_blank_md(res[-1]) \
                    and not _is_list_md(res[-1]) \
                    and not _is_table_md(res[-1]) \
                    and not _is_heading_md(res[-1]) \
                    and not _is_fence_md(res[-1]):
                res.append(_blank_for(ln))
            res.append(ln)
            continue
        # 一般段落：若上一行是行列而本行不是（懶惰延續會把段落吞進行列項），補空行斷開
        if res and _is_list_md(res[-1]) and not _is_blank_md(ln):
            res.append(_blank_for(res[-1]))
        res.append(ln)
    return res


def ensure_blank(lines):
    res = []
    for ln in lines:
        if res:
            prev = res[-1]
            ps = prev.strip()
            if re.match(r"^#{1,6}\s", ln) and ps != "" \
                    and not prev.lstrip().startswith("#") \
                    and not prev.lstrip().startswith("|") \
                    and not re.match(r"^\s*([-*+]|\d+[.)])\s+", prev):
                res.append("")
            elif ln.lstrip().startswith(">") and ps != "" \
                    and not prev.lstrip().startswith(">") \
                    and not prev.lstrip().startswith("|") \
                    and not re.match(r"^\s*([-*+]|\d+[.)])\s+", prev):
                res.append("")
        res.append(ln)
    res = normalize_lists_tables(res)
    return res


def docx_chapter_breaks(path):
    """DOCX：各章（Heading 1）一律另起新頁（與 CSS 之 h1 break-before 對應）。

    僅用標準庫改寫 word/document.xml：為每個 Heading 1 段落加
    <w:pageBreakBefore/>。第一個 H1（第一章）亦加（前方另有卷首內容，
    不會產生空白頁）。
    """
    import zipfile
    import xml.etree.ElementTree as ET
    W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    def q(t):
        return "{%s}%s" % (W, t)
    with zipfile.ZipFile(path, "r") as z:
        xml_bytes = z.read("word/document.xml")
        names = z.namelist()
        others = {n: z.read(n) for n in names if n != "word/document.xml"}
    root = ET.fromstring(xml_bytes)
    n = 0
    for p in root.iter(q("p")):
        pPr = p.find(q("pPr"))
        if pPr is None:
            continue
        pStyle = pPr.find(q("pStyle"))
        if pStyle is None:
            continue
        val = pStyle.get("{%s}val" % W, "")
        if val.replace(" ", "") not in ("Heading1",):
            continue
        import re as _re
        txt = "".join(t.text or "" for t in p.iter(q("t")))
        if not _re.match(r"^(第[一二三四五六七八九]章|結語|附錄)", txt):
            continue  # 卷首書名等非章節 H1 不加分頁
        if pPr.find(q("pageBreakBefore")) is None:
            pbb = ET.Element(q("pageBreakBefore"))
            pbb.set("{%s}val" % W, "1")
            pPr.append(pbb)
            n += 1
    if n:
        import io
        buf = io.BytesIO()
        with zipfile.ZipFile(path, "r") as zin:
            with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
                for item in zin.infolist():
                    data = (ET.tostring(root, encoding="utf-8", xml_declaration=True)
                            if item.filename == "word/document.xml"
                            else zin.read(item.filename))
                    zout.writestr(item, data)
        open(path, "wb").write(buf.getvalue())
    print("  DOCX 章首分頁：%d 個 Heading 1" % n)


def main():
    if MODE == "slim":
        raise SystemExit(u"ver39 未立精簡本規則（削塊名單仍指 ver38 字面），"
                         u"故不產『與完整版同冊身而自稱精簡』之冊。欲出精簡本，先依 ver39 篇目重立 SLIM_KEEP、"
                         u"apply_slim_cuts 與第六章出處段之形（ver39 作『#### 【律典原典】』非『◎原典』）。")
    t_all = time.perf_counter()
    src = read_source()
    hs0 = collect_all_headings(src)
    lines = drop_appendices(drop_blocks(src, hs0), hs0)
    lines = strip_ch6_yuandian(lines, collect_all_headings(lines))
    lines = apply_slim_markers(lines)
    lines = apply_slim_cuts(lines, collect_all_headings(lines))
    if CLEAN:
        lines = apply_clean_cuts(lines)
    lines = ensure_blank(lines)
    hs = collect_headings(lines)
    entries = prepare_toc_entries(hs)
    napp = sum(1 for l, t, _ in hs if l == 1 and re.match(r"^附錄", t))
    print("模式 %s·%s｜H1=%d H2=%d H3=%d｜附錄 %d 個｜目錄條目 %d" %
          (MODE, LAYOUT, sum(1 for l, _, _ in hs if l == 1),
           sum(1 for l, _, _ in hs if l == 2),
           sum(1 for l, _, _ in hs if l == 3), napp,
           sum(1 for lv, dp, _ in entries
               if dp != "目錄" and not skip_in_toc(lv, dp))))

    pages, prev_n, prev = {}, -1, None
    cache = os.path.join(HERE, "_toccache39%s%s.json" % (SUFFIX, TAG))
    # 暖起點之檔須帶版次：舊名 `_toccache.json` 為兩冊共用，三十九版曾以三十八版之
    # 113 條／410 頁起算（收斂仍對，只是白跑一趟），而三十九版寫盤後三十八版又反食其數。
    if TOCSEED and os.path.exists(cache):
        try:
            d = json.load(open(cache, encoding="utf-8"))
            pages = {_ukey(k): v for k, v in d["pages"].items()}
            prev_n, prev = d["npage"], dict(pages)
            print("  暖起點：取上次收斂之頁碼 %d 條／%d 頁（以 TOCSEED=0 廢之）"
                  % (len(pages), prev_n))
        except Exception as e:
            print("  暖起點不可用，仍冷起點：", e)
    for it in range(1, 7):
        _t = time.perf_counter()
        write_md(lines, hs, pages)
        render_html(build_toc_html(entries, pages))
        t_md = time.perf_counter() - _t
        _t = time.perf_counter()
        render_pdf()
        t_pdf = time.perf_counter() - _t
        _t = time.perf_counter()
        raw, npage = scan_pages(entries)
        t_scan = time.perf_counter() - _t
        pages = raw                      # 目錄號＝頁腳號＝PDF 絕對頁碼，不再減去卷首位移
        stable = (npage == prev_n) and (pages == prev)
        print("  第 %d 次：%d 頁，回填 %d 條（排版 %.1fs＋列印 %.1fs＋掃描 %.1fs）%s" %
              (it, npage, len(pages), t_md, t_pdf, t_scan, "　← 收斂" if stable else ""))
        if stable:
            break
        prev_n, prev = npage, pages
    if TOCSEED:
        try:
            json.dump({"npage": npage, "pages": {_ckey(k): v for k, v in pages.items()}},
                      open(cache, "w", encoding="utf-8"), ensure_ascii=False)
        except Exception as e:
            print("  暖起點寫盤失敗：", e)

    # 交付副本：瀏覽器剛關行程或雲端同步會短時鎖檔（第 114 輪實測：連跑四式時
    # copyfile 拋 PermissionError，若外層用 `| tail` 則 rc 被掩成 0，交付檔遂滯留舊冊）
    for _try in range(6):
        try:
            shutil.copyfile(PDF, PDF_OUT)
            break
        except OSError as e:
            if _try == 5:
                raise SystemExit("交付副本寫入失敗（檔鎖未解）：%s｜%s" % (e, PDF_OUT))
            time.sleep(0.4)
    if os.path.getmtime(PDF_OUT) < os.path.getmtime(PDF):
        raise SystemExit("交付副本滯後於產物（必為舊冊）：%s" % PDF_OUT)
    # 交付前自驗：兩檔位數與頁數必同（舊病為瀏覽器未落盤即拷貝，遂交付前一次之冊）
    import pymupdf as _pm
    if os.path.getsize(PDF_OUT) != os.path.getsize(PDF):
        raise SystemExit("交付驗證失敗：副本與產物大小不一")
    _a, _b = _pm.open(PDF), _pm.open(PDF_OUT)
    _na, _nb = _a.page_count, _b.page_count
    _a.close(); _b.close()
    if _na != _nb:
        raise SystemExit("交付驗證失敗：中介 %d 頁 與 副本 %d 頁 不合" % (_na, _nb))
    print("  交付自驗：%d 頁，副本與產物同" % _nb)

    # 內嵌大綱與書訊（第 131 輪）：中介檔與交付檔同步蓋，免兩檔異制
    import pymupdf as _pm2
    _d = _pm2.open(PDF)
    outline, miss, dup = build_outline(_d, entries, pages)
    _d.close()
    ntoc = sum(1 for lv, dp, _ in entries if dp != u"\u76ee\u9304" and not skip_in_toc(lv, dp))
    if outline:
        stamp_pdf(PDF, outline, META)
        stamp_pdf(PDF_OUT, outline, META)
        print(u"  內嵌大綱：%d 條（定位失敗未入者 %d）｜書：%s"
              % (len(outline), len(miss), META["title"]))
        if miss:
            print(u"    未入大綱：%s" % u'、'.join(miss[:6]))
        print(u"    帳：目錄印出 %d 條・大綱入 %d 條・定位失敗 %d・同級重出跳過 %d（前兩數須齊）"
              % (ntoc, len(outline), len(miss), len(dup)))
        if dup:
            print(u"    跳過之名：%s" % u'、'.join(dup[:8]))
        if ntoc - len(outline) != len(miss) + len(dup):
            print(u"    ⚠ 大綱之帳不平：印出－入＝%d 而 miss＋dup＝%d（有條目無故而擲）"
                  % (ntoc - len(outline), len(miss) + len(dup)))
    else:
        print(u"  內嵌大綱：零條——目錄條目盡數定位失敗，須查 build_outline 之口徑")
    _t = time.perf_counter()
    try:
        subprocess.run([PANDOC, MD, "-f", "markdown+pipe_tables+raw_html-blank_before_header",
                        "-t", "docx", "-o", DOCX_OUT], check=True, cwd=HERE)
        docx_chapter_breaks(DOCX_OUT)
        docx_meta(DOCX_OUT, META)
    except Exception as e:
        print("DOCX 略過：", e)
    print("  Word：%d 秒" % (time.perf_counter() - _t))
    print("交付：%s  %d KB｜本次總用時 %d 秒"
          % (os.path.basename(PDF_OUT), os.path.getsize(PDF_OUT) // 1024,
             time.perf_counter() - t_all))


if __name__ == "__main__":
    if "meta" in _ARGS:                 # 一行即驗封面之數（不出冊）：python _print/build39.py meta
        print(book_meta())
        raise SystemExit(0)
    main()
