# -*- coding: utf-8 -*-
"""《佛陀的護欄》列印管線——沿用 _print/build38.py 之同一法源。

共用之處（絕不另起第二套口徑，第 173 輪『小樣不同旗標即不同書』之誡）：
  pandoc 旗標、print38.css、PRINT_CSS 全版字級覆寫、封面注入、
  retune_tables／table_keep／quote_keep／nowrap_case_ids／fit_pre_blocks／
  pali_span／scrub_ctrl 之 HTML 後處理、render_pdf 之無頭列印與落盤四防、
  stamp_pdf 之大綱增量蓋入與覆核。

用法：python _print/build_hulan.py [print|screen]
來源：環境變數 HULAN_SRC 指向正文檔；未給則取工作資料夾根目錄之《佛陀的護欄》（法源 hulan_path）。
產出：_print/佛陀的護欄_…_影印版.pdf｜…_螢幕版.pdf
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import difflib
import html as html_module                          # 圍欄標籤配對時解實字體（&gt; 之類）
import json
import os
import re
import shutil
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
_ARGS = [a.lower() for a in sys.argv[1:]]


def _flag(*ws):
    return any(any(w in a for w in ws) for a in _ARGS)


SCREEN = _flag("screen", "螢幕", "屏幕")
SLIM = _flag("slim", "精簡")           # 精簡版：不印《全戒本歷條總表》之附錄
LAYOUT = "screen" if SCREEN else "print"

SRC = os.environ.get("HULAN_SRC") or HP.SRC

TAGL = ("精簡螢幕版" if SCREEN else "精簡版") if SLIM else ("螢幕版" if SCREEN else "影印版")
SFX = "%s%s" % ("_screen" if SCREEN else "", "_slim" if SLIM else "")
STEM = "佛陀的護欄_四分律戒律之行為心理學解析_" + TAGL
FENCE_BLOCKS = []          # main 內填入：源檔各段圍欄之行，供印面回量
MD = os.path.join(HERE, "hulan_列印版%s.md" % SFX)
HTML = os.path.join(HERE, "hulan_列印版%s.html" % SFX)
FINAL = os.path.join(HERE, "final_hulan%s.html" % SFX)
PDF = os.path.join(HERE, "hulan%s.pdf" % SFX)
PDF_OUT = os.path.join(HERE, STEM + ".pdf")

# ── 取 build38 之全套零件（其 argv 解析於匯入時發生，故先餽之以本式）──
_ARGV = sys.argv
sys.argv = ["build38", "full"] + (["screen"] if SCREEN else ["print"])
import build38 as b38                                    # noqa: E402
sys.argv = _ARGV

b38.MD, b38.HTML, b38.FINAL, b38.PDF = MD, HTML, FINAL, PDF
# 目錄頁碼之暖起點快檔：本冊精簡版須與 ver38 之「精簡本」及各式分開，否則拿錯暖起點、目錄頁碼全亂
b38.SUFFIX = "_護欄精簡" if SLIM else b38.SUFFIX

BOOK_TITLE = "佛陀的護欄"
EDITION = "第一版·" + TAGL


def _cn(n):
    d = u"零一二三四五六七八九"
    if n >= 100:
        s = d[n // 100] + u"百"
        r = n % 100
        if not r:
            return s
        if r < 10:
            return s + u"零" + d[r]
        s += d[r // 10] + u"十"
        return s + (d[r % 10] if r % 10 else u"")
    if n >= 10:
        return (u"" if n // 10 == 1 else d[n // 10]) + u"十" + (d[n % 10] if n % 10 else u"")
    return d[n]


# 封面計數自正文取，手打之數必落後於正文
_SRC_L = io.open(SRC, encoding="utf-8", newline="").read().split("\r\n")
N_CHAP = sum(1 for x in _SRC_L if re.match(u"^# 第.+章", x))
N_CASE = sum(1 for x in _SRC_L if x.startswith(u"#### 案例"))
APPS = u"五大部·%s章·%s則戒相與犍度之現場解剖" % (_cn(N_CHAP), _cn(N_CASE))
COVER = """<section id="print-cover" class="cov">
  <p class="cov-eyebrow">大正藏第一四二八號·四分律</p>
  <div class="cov-main">
    <div class="cov-sutra">佛陀的護欄</div>
    <div class="cov-title">四分律比丘與比丘尼戒的行為心理學解析</div>
    <div class="cov-rule"></div>
    <p class="cov-sub">以遮衛性——解碼律藏的行為防禦工程</p>
    <p class="cov-motto">小戒不是鎖鏈　小戒是安全氣囊<br />
       佛陀不與人性賭博　只預先修築護欄</p>
    <p class="cov-cap">二百五十條比丘戒·三百四十八條比丘尼戒·同心圓五重陣地</p>
  </div>
  <div class="cov-foot">
    <p class="cov-edition">__EDITION__</p>
    <p class="cov-meta">__APPS__<br />原典：漢譯《四分律》六十卷</p>
  </div>
</section>
"""
b38.COVER, b38.EDITION, b38.APPS = COVER, EDITION, APPS
# 部題不另佔一頁：舊法 `.part-open{break-after:page}` 使部題獨頁，全冊遂有 5 頁近全空
# （實測每頁尾白 727pt）。今改令部題與其下首章同頁——部題作部Banner（去底線、不留邊距），
# 首章之 h1 以 break-before:avoid 提回同頁（選擇器 specificity 勝過通則 h1{break-before:page}）。
b38.PRINT_CSS = b38.PRINT_CSS + (
    "\n.part-open { break-after: avoid; border-bottom: none; margin-bottom: 0; padding-bottom: 0; }\n"
    ".part-open + h1 { break-before: avoid; }\n"
    # 圍欄內之東亞寬字放大 10%，使 CJK 步進恰為框線／數字之兩倍（格寬模型見 pre_wide_span）；
    # line-height:1 俾行框仍由窄字決定，圖不因此長高。
    "\npre .pw { font-size: 1.1em; line-height: 1; }\n"
    # 第二病之終（第 57 輪探針 _work/hlpfprobe57.py 實測）：『→↑↓▼』於基準字級下之 natural advance
    # 恰為 0.55em＝一格（與空格・框線同寬），故不需再降字級。舊令 `.pf{.55em}` 出之，字形縮半、
    # advance 亦縮至 0.55 格——圖內凡含此字者其右諸欄左移半格有奇，全冊更因此生細字 89 枚。
    # 是故今不包 span（見 pre_wide_span 之 PF），此條 CSS 亦除。
    # 目錄頁碼（第 56 輪）：條目改列身內 flex 三事——標題可折行、點線填其餘、頁碼靠右界；
    # `.tp` 之級・距・底線一依 print38.css 之 h3，免部題改形後全冊行數無端漂移。
    "\n.tp { font-size: 14.0pt; font-weight: 700; margin: .6em 0 .32em;"
    " padding-bottom: .15em; border-bottom: 1px solid #b9b9b9;"
    " page-break-after: avoid; text-align: left; }\n"
    "\n.ti { display: flex; align-items: baseline; break-inside: avoid; }\n"
    "\n.ti .tx { flex: 0 1 auto; min-width: 4em; }\n"
    "\n.ti .ld { flex: 1 1 .6em; align-self: flex-end; margin: 0 .35em .28em;"
    " border-bottom: 1px dotted #a2a2a2; min-width: .9em; }\n"
    "\n.ti .tn { flex: 0 0 auto; font-weight: 400; color: #333;"
    " font-variant-numeric: tabular-nums; }\n"
    "\n.tp .ti .tx { font-weight: 700; }\n"
    # 附錄扉頁（第 78 輪・外路第廿八報之裝幀案）：附錄之 H1 本即目錄條與書籤之靶，今不再於其下
    # 直排導言長段——把該 H1 升為整頁之封面（大字・居中・去底線・下沉至版心上緣之下一停），
    # 其下副題兩行（號數由產生器自算，非手打），`break-after: page` 令導言另起一頁。
    # 情感之尾聲與工具之歷條遂有緩衝，且頁數唯增一，不動正文之排。
    # 類名不用 build38 之 `appendix-start`：彼只認『附錄』後接拉丁字母之 id（附錄A～H），
    # 此冊之題不中（實測 CSS 全不生效），故由 `mark_appendix()` 自標 `.apx-open`。
    "\nh1.apx-open { font-size: 27.0pt; letter-spacing: .1em; text-indent: .1em;"
    " border-bottom: none; padding-top: 34mm; margin-bottom: .9em; }\n"
    "\n.apxcover { break-after: page; text-align: center; margin: 0; }\n"
    "\n.apxcover p { margin: 0; text-align: center; }\n"
    "\n.apxcover .arule { width: 16mm; border-top: 1.2px solid #555; margin: 0 auto 7mm; }\n"
    "\n.apxcover .ac2 { font-size: 13.2pt; color: #111; line-height: 1.9; }\n"
    "\n.apxcover .ac3 { font-size: 11.6pt; color: #555; line-height: 1.9; margin-top: 2.2mm; }\n"
)

META = {
    "title": "%s｜四分律比丘與比丘尼戒的行為心理學解析｜%s" % (BOOK_TITLE, EDITION),
    "author": "編者",
    "subject": "以遮衛性——解碼律藏的行為防禦工程",
    "keywords": "四分律；毘奈耶；波羅夷；僧殘；捨墮；單提；眾學法；七滅諍；"
                "行為心理學；大正藏 No.1428",
    "creator": "build_hulan 管線（沿用 build38 之法源：pandoc → 無頭 Chromium 列印）",
    "producer": "build_hulan",
}

TOC_ANCHOR = "# 第一章 為什麼現代人讀不懂戒律？"
FENCE = "```"

# ── 目錄頁碼（第 56 輪）────────────────────────────────────────────────────
# 作者手寫之【全書詳細目錄】字句與層級一動不得，管線唯於**產物層**為每一條注入頁碼
# （注入在中介 md，正本零改——與 ver38 之點線目錄同一『產物層治目錄』之路，唯此冊之
# 目錄為手寫，故不改寫其文，只為它配頁）。
# 頁碼之法源＝印面實測：正文標題逐條在已成之冊上取字級 ≥HEAD_MIN 之 span 定其物理頁
# （目錄條目本級 12.9pt，進不了此門，故不會自指目錄頁）；目錄條目先與正文標題配對
# （單調游標＋四級退路），配不著者退而『承上』取其最近上位之頁——無一条以算式臆造。
# 收斂：注入頁碼會微動行寬而可能改頁數，故以『頁碼＋頁數』同穩為止（暖起點存盤）。
# `--toc-audit` 印全表（條目↔標題↔頁↔方式）逐條親核；有條目全無落點即硬退，不靜默。
TOC_TITLE = u"# 【全書詳細目錄】"
HEAD_MIN = 13.2                  # 印面標題級下限（H4 實測 13.7／目錄條目 12.9）
TOC_CACHE = os.path.join(HERE, "_hulantoc%s.json" % SFX)
TOC_VER = u"v1"
CROWN_CUT = u"："


def norm_txt(s):
    """條目與標題之共用法正規形：去粗體／反引號、削尾部括註、摺去所有空白。"""
    s = re.sub(r"[*`]", u"", s)
    s = re.sub(u"（[^（）]*）$", u"", s)
    return re.sub(r"\s+", u"", s).strip()


def ckey(lvl, nm, occ):
    return u"%d|%s|%d" % (lvl, nm, occ)


def toc_bounds(lines):
    """目錄區塊之md行範圍 [起, 迄)：起於『# 【全書詳細目錄】』，迄於其後第一個 H1。"""
    a = next((n for n, l in enumerate(lines) if l.startswith(TOC_TITLE)), None)
    if a is None:
        raise SystemExit(u"目錄定位失敗：中介檔無『%s』" % TOC_TITLE)
    b = next((n for n in range(a + 1, len(lines)) if re.match(r"^# ", lines[n])), None)
    if b is None:
        raise SystemExit(u"目錄迄點定位失敗：『%s』之後俱無 H1" % TOC_TITLE[:8])
    return a, b


def toc_items(lines):
    """目錄之條目行 → [(md行, 層, 顯示文字, 正規, 同名序)]。
    層 0＝部題（源作 `### **【…】**`）、1＝章、2＝節、3＝目；層由縮排自算，不靠名單。"""
    a, b = toc_bounds(lines)
    out, seen = [], {}
    for n in range(a + 1, b):
        l = lines[n]
        m = re.match(u"^### \\*\\*(.+?)\\*\\*$", l)
        if m:
            lvl, disp = 0, m.group(1)
        else:
            m = re.match(r"^(\s*)([*+-])\s+(.*)$", l)
            if not m:
                continue
            lvl, disp = 1 + len(m.group(1)) // 2, m.group(3)
        nm = norm_txt(disp)
        if not nm:
            continue
        occ = seen.get((lvl, nm), 0) + 1
        seen[(lvl, nm)] = occ
        out.append((n, lvl, disp, nm, occ))
    return out


def toc_headings(lines):
    """目錄之後之正文標題 → [(md行, 級, 正規, 複合正規)]。
    複合形＝H1＋其緊接之 H2（章題與副題分兩級而目錄合作一條，如『第一章 …？——法條主義…』）。"""
    a, b = toc_bounds(lines)
    out, inf = [], False
    for n in range(b, len(lines)):
        l = lines[n]
        if l.startswith(FENCE):
            inf = not inf
            continue
        if inf:
            continue
        m = re.match(r"^(#{1,6}) (.+)$", l)
        if m:
            out.append([n, len(m.group(1)), norm_txt(m.group(2)), None])
    for i, rec in enumerate(out):
        if rec[1] == 1 and i + 1 < len(out) and out[i + 1][1] == 2:
            rec[3] = rec[2] + out[i + 1][2]
    return out


def _crown_in(crown, h):
    """冠（『：』之前）與標題之相含：整冠見於標題，或冠之各件（以『與、及／』切）依序見於標題。"""
    if crown and crown in h:
        return u"前冠含"
    toks = [t for t in re.split(u"與|、|及|／|/", crown) if len(t) >= 2]
    if len(toks) >= 2:
        k = 0
        for t in toks:
            p = h.find(t, k)
            if p < 0:
                return None
            k = p + len(t)
        return u"冠件序含"
    return None


def pair_items(items, ths):
    """目錄條目 ↔ 正文標題：單調游標（書序）→ 直中、起首相含、前冠相含、近似；
    四級俱不中則准『全局直中』（目錄末之書首圖譜條目，其靶實在書前）。回 [(序|None, 方式)]。"""
    res, cur = [], 0
    for _, _, _, nm, _occ in items:
        hit = how = None
        for j in range(cur, len(ths)):                     # ① 直中
            if nm == ths[j][2] or (ths[j][3] and nm == ths[j][3]):
                hit, how = j, u"直中"
                break
        if hit is None:
            for j in range(cur, len(ths)):                 # ② 起首相含
                for h in (ths[j][2], ths[j][3] or u""):
                    if h and (h.startswith(nm) or (nm.startswith(h) and len(h) >= 6)):
                        hit, how = j, u"起首含"
                        break
                if hit is not None:
                    break
        if hit is None:
            crown = nm.split(CROWN_CUT)[0]
            for j in range(cur, len(ths)):                 # ③ 前冠相含
                for h in (ths[j][2] + (ths[j][3] or u""),):
                    got = _crown_in(crown, h)
                    if got:
                        hit, how = j, got
                        break
                if hit is not None:
                    break
        if hit is None:
            for j in range(len(ths)):                      # ④ 全局直中（書首之靶）
                if nm == ths[j][2] or (ths[j][3] and nm == ths[j][3]):
                    hit, how = j, u"全局直中"
                    break
        if hit is None:
            best = (0.42, None)                            # ⑤ 近似（過閾始取）
            for j in range(cur, len(ths)):
                for h in (ths[j][2], ths[j][3] or u""):
                    if h:
                        r = difflib.SequenceMatcher(None, nm, h).ratio()
                        if r > best[0]:
                            best = (r, j)
            if best[1] is not None:
                hit, how = best[1], u"近似%.2f" % best[0]
        res.append((hit, how or u"未配"))
        if hit is not None:
            cur = hit + 1
    return res


def big_pages(doc):
    """逐頁取『標題級』文字（摺空白）與全頁文字：前者定標題之頁，後者為退路。"""
    import pymupdf                                   # noqa: F401  （doc 已開，此處只取 span）
    big, full = [], []
    for p in range(doc.page_count):
        buf = [s["text"] for blk in doc[p].get_text("dict")["blocks"]
               for ln in blk.get("lines", []) for s in ln["spans"]
               if s.get("size", 0) >= HEAD_MIN]
        big.append(re.sub(r"\s+", u"", u"".join(buf)))
        full.append(re.sub(r"\s+", u"", doc[p].get_text()))
    return big, full


def locate_headings(ths, big, full):
    """正文標題逐條定物理頁（1 起，單調向前）：先認標題級字，認不得才退全頁文字。"""
    cur, out, via_full = 0, [], 0
    for _n, _lv, nm, comp in ths:
        got, how = None, u"字級"
        for cand in range(cur, len(big)):
            if (nm[:12] and nm[:12] in big[cand]) or (comp and comp[:12] in big[cand]):
                got = cand
                break
        if got is None:
            for cand in range(cur, len(full)):
                if nm[:12] and nm[:12] in full[cand]:
                    got, how = cand, u"全頁"
                    break
        if got is None:
            out.append((None, None))
            continue
        if how == u"全頁":
            via_full += 1
        cur = got
        out.append((got + 1, how))
    return out, via_full


def toc_scan(doc, items, ths):
    """回 (頁碼 dict, 稽核表, 無落點之名單)。稽核表列〔層, 條目, 頁, 方式, 所配之標題〕。"""
    big, full = big_pages(doc)
    hp, via_full = locate_headings(ths, big, full)
    pairs = pair_items(items, ths)
    pages, rows, lost, last = {}, [], [], None
    for i, (ln, lvl, disp, nm, occ) in enumerate(items):
        j, how = pairs[i]
        pg = hp[j][0] if j is not None else None
        if pg is None and last is not None:
            pg, how = last, u"承上"            # 撮舉之目無自題：取其最近上位之頁
        if pg is None:
            lost.append(u"L%d %s" % (lvl, disp[:34]))
            rows.append((lvl, disp, None, u"無落點", u"－"))
            continue
        pages[ckey(lvl, nm, occ)] = pg
        last = pg
        rows.append((lvl, disp, pg, how, ths[j][2] if j is not None else u"（承上位）"))
    return pages, rows, lost, via_full


def inject_toc(lines, pages):
    """於產物層把頁碼寫進目錄：清單項前行首掛 `<span class=\"tn\">`（CSS 浮右），
    部題行改 `<p class=\"tp\">`（不再是 H3，故不入大綱、不與書中真標題搶定位）。
    行數不動，唯部題之 <p> 前後補空行（pandoc 須見空行才立為 HTML 塊）。"""
    _a, b = toc_bounds(lines)
    out = list(lines)
    for ln, lvl, disp, nm, occ in toc_items(lines):
        pg = pages.get(ckey(lvl, nm, occ))
        if not pg:
            continue
        if lvl == 0:
            out[ln] = (u'<p class="tp"><span class="ti"><span class="tx">%s</span>'
                       u'<span class="ld"></span><span class="tn">%d</span></span></p>'
                       % (disp, pg))
        else:
            m = re.match(r"^(\s*)([*+-])\s+(.*)$", lines[ln])
            out[ln] = (u'%s%s <span class="ti"><span class="tx">%s</span>'
                       u'<span class="ld"></span><span class="tn">%d</span></span>'
                       % (m.group(1), m.group(2), m.group(3), pg))
    res, added = [], 0
    for i, l in enumerate(out):
        if l.startswith(u'<p class="tp">') and res and res[-1].strip():
            res.append(u"")
            added += 1
        res.append(l)
        if l.startswith(u'<p class="tp">') and i + 1 < len(out) and out[i + 1].strip():
            res.append(u"")
            added += 1
    return res, added


def write_md(toc_pages=None):
    """源檔 → 中介 md：CRLF 歸一、大綱注入點定位，再過 build38 之 ensure_blank
    （段落直連清單／表格／圍欄而未留空行者，pandoc 會壓成一整段並印出字面星號——
    源檔此形多處，故與 ver38 同一正規化器治之，不另起第二套口徑）。"""
    raw = io.open(SRC, encoding="utf-8-sig").read()
    lines = raw.replace("\r\n", "\n").split("\n")
    if SLIM:                                    # 精簡版不隨冊之附錄：削『# 附錄』起至檔尾
        ap = next((i for i, l in enumerate(lines) if l.startswith("# 附錄")), None)
        if ap is not None:
            while ap > 0 and not lines[ap - 1].strip():
                ap -= 1
            print("精簡版：削附錄 %d 行（『%s』起）" % (len(lines) - ap, lines[ap][:18]))
            lines = lines[:ap]
        cut_toc = [i for i, l in enumerate(lines) if l.lstrip().startswith("* **附錄")]
        for i in reversed(cut_toc):
            print("精簡版：削目錄之附錄項 1 行")
            del lines[i]
    if TOC_ANCHOR not in lines:
        raise SystemExit("中介檔定位失敗：源檔無『%s』" % TOC_ANCHOR[:18])
    # 佔位符須前後各留空行：源檔此處為『---』直連『# 第一章』，佔位符插於其間即成
    # 『---／佔位符／---』三段——pandoc 據 simple table 口徑把整區吞成一欄表格，
    # 章題淪為字面文字、副題整行消失（印面 p13 之病，第 244 輪定位）。
    i = lines.index(TOC_ANCHOR)
    lines.insert(i, u"<!--TOC-PLACEHOLDER-->\n")
    if lines[i - 1].strip() != u"":
        lines.insert(i, u"")
    n0 = len(lines)
    lines = b38.ensure_blank(lines)
    base = list(lines)                              # 未注入頁碼之形：目錄條目與標題之法源
    ntp = 0
    if toc_pages:
        lines, ntp = inject_toc(lines, toc_pages)
    io.open(MD, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    n = sum(1 for l in lines if l.startswith("# "))
    print("源：%s｜行=%d→%d（正規化補空行 %d）｜H1=%d｜目錄頁碼注入 %d 條（部題塊 %d）｜中介 md 已出"
          % (os.path.basename(SRC), n0, len(lines), len(lines) - n0, n,
             len(toc_pages or {}), ntp))
    return lines, base


def headings(lines):
    """圍欄內的『#』是框線圖不是標題，故先切圍欄再取標題。"""
    out, inf = [], False
    for l in lines:
        if l.startswith(FENCE):
            inf = not inf
            continue
        if inf:
            continue
        m = re.match(r"^(#{1,4}) (.+)$", l)
        if m:
            out.append((len(m.group(1)), clean(m.group(2))))
    return out


def clean(s):
    s = re.sub(r"[*`]", "", s)
    return re.sub(r"\s+", "", s).strip()


def build_outline(doc, hs):
    """逐條標題在**已印出之冊**中定物理頁——與目錄頁碼同一把尺（`locate_headings`）：
    先認標題級字（≥HEAD_MIN），認不得才退全頁文字。舊法唯摺全頁文字，故第 56 輪目錄
    帶上頁碼後，『十線地圖』之書籤會被目錄裡同字面之條目搶走（指到 p14 而非 p15）。
    字面須先摺去所有空白——印面折行會插斷整串搜尋（第 223／240 輪之誡）。"""
    ths = [[i, lvl, title, None] for i, (lvl, title) in enumerate(hs)]
    big, full = big_pages(doc)
    got, via_full = locate_headings(ths, big, full)
    out, miss = [], []
    for rec, (pg, _how) in zip(ths, got):
        if pg is None:
            miss.append(rec[2][:16])
            continue
        out.append([min(rec[1], 4), rec[2][:80], pg])
    fixed, prev = [], 0                        # PDF 大綱：自 1 起，每次至多降一級
    for lv, ti, pg in out:
        if not fixed:
            lv = 1
        elif lv > prev + 1:
            lv = prev + 1
        fixed.append([lv, ti, pg])
        prev = lv
    if via_full:
        print("大綱定位：退全頁文字者 %d 條（字級門未認出，須查該題印面字級）" % via_full)
    return fixed, miss


H1_LINE = re.compile(r"^# (.+)$")
# 頁眉之章級：唯真『章』與兩篇工具之題入眉（卷首三題・部題皆 Banner，不入）。
# 此名單非手抄戶口——它只判形，題與頁俱自正文之 H1 與印面之字級現得。
HEAD_H1 = re.compile(u"^(?:第[一二三四五六七八九十百千]+章|十線地圖|附錄)")


def head_titles():
    """章級 H1 之**原形題**（題中空白留著——眉上要用它；圍欄內的『#』是框線圖，非標題）。"""
    inf, out = False, []
    for l in io.open(MD, encoding="utf-8").read().split("\n"):
        if l.startswith(FENCE):
            inf = not inf
            continue
        if inf:
            continue
        m = H1_LINE.match(l)
        if m:
            t = re.sub(r"[*`]", "", m.group(1)).strip()
            if HEAD_H1.match(t):
                out.append(t)
    return out


def head_pages(doc):
    """章級之題在**已成之冊**上的物理頁——與目錄・大綱同一把尺（`locate_headings`）：
    定位之字面須摺去空白（印面折行會插斷整串搜尋），顯示之題仍留原形。"""
    raw = head_titles()
    ths = [[i, 1, re.sub(r"\s+", "", t), None] for i, t in enumerate(raw)]
    big, full = big_pages(doc)
    got, via = locate_headings(ths, big, full)
    pairs = [(raw[i], got[i][0]) for i in range(len(raw)) if got[i][0]]
    lost = [raw[i][:16] for i in range(len(raw)) if not got[i][0]]
    if lost:
        print(u"頁眉：章級之題定位失敗 %d 條（此段不蓋）：%s" % (len(lost), u"、".join(lost[:6])))
    return pairs, len(raw), via


def deliver():
    """交付副本之四重護欄（承 build38.main：檔鎖重試、mtime 落後即死、
    大小與頁數須與產物同——第 114／120 輪之戒，勿以 rc 為憑）。"""
    for k in range(6):
        try:
            shutil.copyfile(PDF, PDF_OUT)
            break
        except OSError as e:
            if k == 5:
                raise SystemExit("交付副本寫入失敗（檔鎖未解）：%s｜%s" % (e, PDF_OUT))
            time.sleep(0.4)
    if os.path.getmtime(PDF_OUT) < os.path.getmtime(PDF):
        raise SystemExit("交付副本滯後於產物（必為舊冊）：%s" % PDF_OUT)
    import pymupdf as pm
    a, b = pm.open(PDF), pm.open(PDF_OUT)
    na, nb = a.page_count, b.page_count
    a.close(); b.close()
    if os.path.getsize(PDF_OUT) != os.path.getsize(PDF) or na != nb:
        raise SystemExit("交付驗證失敗：產物 %d 頁／副本 %d 頁或大小不一" % (na, nb))
    return nb


def drop_hr_before_h1():
    """篇界之 <hr> 若緊接另起新頁的 H1，紙上會撐出一整頁空白（實測 p2、p10 唯印頁碼）。
    源檔之『---』照留（它是源層的篇界法度），唯於列印層削其重覆之職——
    另起新頁已然畫出篇界，格線於此無所表示。"""
    html = io.open(FINAL, encoding="utf-8").read()
    new, n = re.subn(r"(?s)<hr\s*/?>\s*(?=<h1[\s>])", "", html)
    if n:
        io.open(FINAL, "w", encoding="utf-8").write(new)
    print("篇界格線隨頁界而削：%d 處（否則成空白頁）" % n)


PART = re.compile(u"【(?:第[一二三四五]部：[^】]*|卷首·扉頁)】")


def mark_appendix():
    """附錄之 H1 自掛 `.apx-open`——build38 之 `appendix-start` 只認『附錄』後接拉丁字母之 id
    （ver38 之附錄A～H），此冊之題作『附錄　全戒本歷條總表』，其式不中（第 78 輪實測：
    CSS 全不生效，扉頁之題仍帶正文底線・不上移），故於本式自標之。標不中即硬退，不靜默。"""
    html = io.open(FINAL, encoding="utf-8").read()

    def one(m):
        head, body = m.group(1), m.group(2)
        if not re.sub(r"<[^>]+>", "", body).strip().startswith(u"附錄"):
            return m.group(0)
        if 'class="' in head:
            head = head.replace('class="', 'class="apx-open ', 1)
        else:
            head = head[:-1].rstrip() + ' class="apx-open">'
        return head + body + "</h1>"

    new, _ = re.subn(r"(?s)(<h1\b[^>]*>)(.*?)(</h1>)", one, html)
    got = new.count('class="apx-open')
    if got != 1:
        raise SystemExit(u"附錄扉頁標記失敗：H1 掛 .apx-open 得 %d 枚（宜 1）——CSS 將全不生效" % got)
    io.open(FINAL, "w", encoding="utf-8").write(new)
    print(u"附錄之題掛 .apx-open：%d 枚（全冊 H1 %d 枚）" % (got, new.count("<h1")))


def mark_part_pages():
    """部題（及卷首題）之下緊接章題，兩者俱帶 break-before: page——Chromium 折疊相連之
    強制分頁，章題遂與部題同頁。今於部題掛 .part-open，配 CSS 令其作 Banner 而非獨頁：
    舊法曾以 break-after: page 使部題自成一頁，全冊遂生 5 頁近全空（尾白 727pt），已廢。"""
    html = io.open(FINAL, encoding="utf-8").read()

    def one(m):
        head, body = m.group(1), m.group(2)
        if not PART.search(re.sub(r"<[^>]+>", "", body)):
            return m.group(0)
        if 'class="' in head:
            head = head.replace('class="', 'class="part-open ', 1)
        else:
            head = head[:-1].rstrip() + ' class="part-open">'
        return head + body + "</h1>"

    new, _ = re.subn(r"(?s)(<h1\b[^>]*>)(.*?)(</h1>)", one, html)
    marked = new.count('class="part-open')
    if marked:
        io.open(FINAL, "w", encoding="utf-8").write(new)
    print("部題頁標記：%d 處掛 .part-open（冊內 H1 共 %d 枚）"
          % (marked, new.count("<h1")))


def pre_wide_span():
    """令圍欄內之東亞寬字（ord≥0x2E80）以 1.1em 出字；Consolas 缺字之幾何／箭頭以 .55em 出字。

    印面實測（第 244 輪）：Consolas 之框線／數字／空白步進 0.55em，正黑之 CJK 步進 1.00em，
    比值 1.82；而源檔框線圖一律以「CJK＝兩格、框線＝一格」（即 2:1）排格，
    故欄位必逐格左漂——十三僧殘五道防線圖至第五欄已錯開近一字。將寬字放大 10% 後
    比值恰為 2.00，`_cw` 之格寬模型與印面相符，fit_pre_blocks 之縮字亦隨之準確。

    第二病之終（第 57 輪探針實測，見上方 CSS 之註）：『→』『▼』諸字雖非 Consolas 所有，
    其後備字之 natural advance 恰 0.55em＝一格，與空格・框線同寬，故不須另立 `.pf` 降字級。
    第 55 輪舊法以 0.55em 出之，反使 advance 縮成 0.55 格（印面量得 3.5pt／一格 6.4pt），
    含此字之行其右諸欄左移半格有奇，且生細字 89 枚——今 PF 清空，只留此機制以備後來的真全形字。
    標籤皆純 ASCII（ord<0x2E80），故包 span 不會截斷既有標記或字元實體。
    """
    PF = frozenset()                           # 需降字級始得回填（現無：探針量得四箭與▼俱恰一格）
    html = io.open(FINAL, encoding="utf-8").read()

    def one(m):
        head, inner, tail = m.group(1), m.group(2), m.group(3)
        out, run, cls = [], [], None

        def flush():
            if run:
                out.append('<span class="%s">' % cls + "".join(run) + "</span>")
                del run[:]

        for ch in inner:
            c2 = "pw" if ord(ch) >= 0x2E80 else ("pf" if ch in PF else None)
            if c2 != cls:
                flush()
                cls = c2
            (run if c2 else out).append(ch)
        flush()
        return head + "".join(out) + tail

    new, n = re.subn(r"(?s)(<pre\b[^>]*>)(.*?)(</pre>)", one, html)
    if n:
        io.open(FINAL, "w", encoding="utf-8").write(new)
    npf = new.count('<span class="pf">')
    print("圍欄寬字加 span：%d 段（CJK 出字 1.1em，合 2:1 格寬）・缺字回一格：%d 處" % (n, npf))


def fence_blocks(lines):
    """取源檔每一段圍欄圖之行（去空行），供印面回量之用。"""
    out, inf, buf = [], False, []
    for l in lines:
        if l.startswith("```"):
            if not inf:
                inf, buf = True, []
            else:
                inf = False
                if buf:
                    out.append([x for x in buf if x.strip()])
            continue
        if inf:
            buf.append(l)
    return out


def cw_units(s):
    """格數：東亞寬字（ord>0x2E80）算兩格，框線／數字／空白算一格——與印面 2:1 同步。"""
    return sum(2 if ord(c) > 0x2E80 else 1 for c in s)


def pre_base_sizes():
    """final html 內每個 <pre> 標籤之基準字級（inline style，無則 None）。
    印面回量須以此為基準——PDF span 之最小字級不可用：段內既有 1.1em 之寬字（.pw）、
    又有 0.55em 之缺字（.pf），取其小者必把基準誤認為 0.55 倍，縮字遂連環下墜至下限。"""
    html = io.open(FINAL, encoding="utf-8").read()
    out = []
    for m in re.finditer(r"(?s)<pre\b[^>]*>", html):
        s = re.search(r"font-size:\s*([\d.]+)pt", m.group(0))
        out.append(float(s.group(1)) if s else None)
    return out


def pre_audit(doc, blocks, bases, mp, pages=None):
    """印面圍欄總稽核（量產物，不套字型模型）：回 {段序: dict(基准・源行・印行・可用・實寬・對鎖)}。
    逐段先定其所在頁（首尾同頁者一頁，跨頁者自首頁量至末頁，舊口徑唯量同頁者——遂令 67 行之
    十六觀心圖印至 10pt 而末二行被換行鋸斷、歷輪無知，第 67 輪 p517 實測）；再取該段灰底框
    （pre 之 border box）為上下左右之界，頁腳頁碼在框外故不汙行數；右界即框之右緣，故任何縮排
    來源（blockquote／列表／邊框／奇偶頁）一律自動吸收。
    實寬由「源檔行↔印面行」逐行對鎖而得：一行印成兩行（被 word-break 鋸斷）者，以其兩行寬之
    和還原其應有之寬。此步要緊——舊唯量印面最長行，則斷點恰落框內者（如源 88 格、實需 512pt
    而斷於 500pt 處）看似合框，實已散架，歷輪不報。
    基準字級取 html 標籤之 inline style（pre_base_sizes）；PDF 內 span 混 1.1em 寬字與 0.55em
    缺字，取其小者必把基準誤認為 0.55 倍，縮字遂連環下墜至 6.2pt 下限（第 67 輪之案）。
    """
    def nn(s):
        return "".join(s.split())

    if pages is None:
        pages = [nn(doc[i].get_text()) for i in range(doc.page_count)]
    out = {}
    for k, b in enumerate(blocks, 1):
        head, tail = nn(b[0])[:12], nn(b[-1])[:12]
        ph = [i for i, t in enumerate(pages) if head in t]
        pt = [i for i, t in enumerate(pages) if tail in t]
        if not ph or not pt:
            continue
        both = sorted(set(ph) & set(pt))
        if not both and max(pt) - min(ph) > 4:
            continue
        pgs = [both[0]] if both else list(range(min(ph), min(max(pt) + 1, min(ph) + 5)))
        base = bases[mp[k]] if k in mp and mp[k] < len(bases) else None
        if not base:
            continue
        rows2, avail = [], None
        for p in pgs:
            rows = []
            for bl in doc[p].get_text("rawdict")["blocks"]:
                for ln in bl.get("lines", []):
                    txt = "".join(c["c"] for sp in ln.get("spans", []) for c in sp["chars"])
                    if txt.strip():
                        mx = max(sp.get("size", 0) for sp in ln.get("spans", []))
                        rows.append((ln["bbox"][1], ln["bbox"][0], ln["bbox"][2], nn(txt), mx))
            rows.sort()
            # 唯取等寬之行：圍欄內之行其最大 span 為 base 或 1.1em（寬字），正文・頁腳俱大於此，
            # 不滤則同頁之散體文字混入行數，對鎖遂亂（第 67 輪 p516 實測：段內混入章首六行正文）。
            mono = [r for r in rows if r[4] <= 1.1 * base + 0.4]
            if not mono:
                continue
            ys = [r[0] for r in mono if r[3].startswith(head)]
            ye = [r[0] for r in mono if r[3].startswith(tail)]
            y0 = ys[0] - 1 if (p == pgs[0] and ys) else -1
            y1 = max(ye) + 2 if (p == pgs[-1] and ye) else 1e9
            seg = [r for r in mono if y0 <= r[0] <= y1]
            if not seg:
                continue
            # 灰底框取「含段首行而面積最大」之矩形，以其上下界裁之——不取諸矩形之交集，
            # 交集會把只覆蓋數行的淺框當成界，一段 41 行遂只量得 1 行（第 67 輪 #76・84-87 之帳）。
            cand = [g["rect"] for g in doc[p].get_drawings()
                    if g.get("fill") and g["rect"].x0 <= seg[0][1] + 1
                    and g["rect"].x1 > seg[0][1] + 100
                    and g["rect"].y0 - 3 <= seg[0][0] <= g["rect"].y1 + 3]
            if cand:
                g = max(cand, key=lambda z: z.width * z.height)
                seg = [r for r in seg if g.y0 - 4 <= r[0] <= g.y1 + 4]
                right = g.x1
            else:
                right = doc[p].rect.width - 51.0
            if not seg:
                continue
            x0 = min(r[1] for r in seg)
            a = right - 0.55 * base - 2.0 - x0
            avail = a if avail is None else min(avail, a)
            rows2.extend((x0, r[2], r[3], p) for r in seg)
        if not rows2 or not avail or avail <= 0:
            continue
        src = [nn(x) for x in b if nn(x)]
        w_of, i, j, nmatch = [], 0, 0, 0
        while i < len(src) and j < len(rows2):
            w = rows2[j][1] - rows2[j][0]
            if rows2[j][2] == src[i]:
                w_of.append(w)
                nmatch += 1
                i, j = i + 1, j + 1
            elif (j + 1 < len(rows2) and rows2[j + 1][3] == rows2[j][3]
                  and (rows2[j][2] + rows2[j + 1][2]) == src[i]):
                w_of.append(w + rows2[j + 1][1] - rows2[j][0])   # 鋸斷者：兩行寬之和還原
                nmatch += 1
                i, j = i + 1, j + 2
            else:
                j += 1                       # 框內雜行（頁碼・標注）：跳過再試
        ink = max(r[1] - r[0] for r in rows2)
        ok = nmatch >= max(2, int(0.6 * len(src)))
        out[k] = dict(base=base, src=len(src), rows=len(rows2), avail=avail,
                      widest=(max(w_of) if w_of else ink) if ok else ink,
                      nmatch=nmatch, sync=ok, ink=ink, pgs=len(pgs), first=b[0].strip()[:20])
    return out


def pre_overflows(pdf, blocks):
    """須縮者回傳 {段序: 新字級}。兩條病根各立其判：
    一、應有之寬逾可用之寬者，縮幅＝可用 ÷ 應有，留 1% 之裕；變化不足 0.3pt 者不報——
        免每一趟因捨入再縮 1% 而八趟不斂（第 67 輪螢幕版之帳）。
    二、對鎖既合而印面行數反超源行數者（貼邊之行折為兩行，兩行各自短於框，判一遂漏），
        一律必縮，且每回合至少縮 0.35pt。第 57 輪之帳：11 段以判一量得溢 +7.0～+7.9pt，
        而按比例所算之縮幅恰不足 0.3pt，盡被『免擾閘』閘住，歷輪報『俱合版寬・無換行』而印面鋸字。
    """
    import pymupdf

    d = pymupdf.open(pdf)
    mp, _n, _miss = pre_tag_map(blocks)
    bases = pre_base_sizes()
    need = {}
    for k, r in pre_audit(d, blocks, bases, mp).items():
        ratio = r["avail"] / r["widest"] if r["widest"] > r["avail"] else 1.0
        if not r["sync"] and r["rows"] > r["src"] + r["pgs"]:   # 對鎖失靈而行數仍超＝有行被鋸
            ratio = min(ratio, (r["src"] + r["pgs"] + 0.5) / r["rows"])
        target = r["base"] * ratio * 0.99
        folded = r["sync"] and r["rows"] > r["src"] + (r["pgs"] - 1)
        if folded:
            target = min(target, r["base"] - 0.35)
        if target < r["base"] - (0.0 if folded else 0.3):
            need[k] = round(max(6.2, target), 2)
    d.close()
    return need


def pre_tag_map(blocks):
    """源檔第 k 段圍欄 ↔ FINAL html 內第幾個 <pre>（0 起）——以首尾行內容配對。
    單靠序號必錯位：pandoc 亦會因縮排而生 <pre>（本冊實測 95 標籤 vs 源檔 93 段），
    錯位則縮字縮到別段去，該縮者永不縮、印面遂換行散架。回 ({k: idx}, 標籤數, 未配對段)。"""
    html = io.open(FINAL, encoding="utf-8").read()
    tags = [m for m in re.finditer(r"(?s)<pre\b[^>]*>(.*?)</pre>", html)]

    def nn(s):
        return "".join(html_module.unescape(re.sub(r"(?s)<[^>]+>", "", s)).split())

    body = [nn(m.group(1)) for m in tags]
    mapping, used, cur, miss = {}, set(), 0, []
    for k, b in enumerate(blocks, 1):
        if not b:
            continue
        h, t = nn("\n".join(b[:1]))[:12], nn(b[-1])[:12]
        pick = None
        for j in range(cur, len(tags)):
            if j in used or not body[j].startswith(h):
                continue
            if not t or t in body[j]:
                pick = j
                break
        if pick is None:
            for j in range(len(tags)):
                if j in used or not body[j].startswith(h):
                    continue
                if not t or t in body[j]:
                    pick = j
                    break
        if pick is None:
            miss.append(k)
            continue
        mapping[k] = pick
        used.add(pick)
        cur = pick + 1
    return mapping, len(tags), miss


def apply_pre_sizes(sizes, blocks=None):
    """把第 k 段 pre 之 inline 字級改為量得之值（只改標籤，不動內容）。
    給 blocks 則以內容配對標籤（正法）；不給則沿用序號舊口徑（他冊之 reproduce 不變）。
    一次取全部標籤、由後而前改寫，免位移錯號。"""
    html = io.open(FINAL, encoding="utf-8").read()
    tags = [m for m in re.finditer(r"(?s)<pre\b[^>]*>", html)]
    mp = {}
    if blocks:
        mp, _n, miss = pre_tag_map(blocks)
        if miss:
            print("圍欄配對：未能在印面尋得第 %s 段之標籤（此段不縮）" % "、".join(str(x) for x in miss[:6]))
    done = 0
    for k in sorted(sizes, reverse=True):
        idx = mp.get(k, k - 1) if blocks else k - 1
        if idx >= len(tags):
            break
        m = tags[idx]
        head = m.group(0)
        new = re.sub(r"font-size:\s*[\d.]+pt", "font-size:%gpt" % sizes[k], head)
        if new == head:
            new = head[:-1].rstrip() + ' style="font-size:%gpt;">' % sizes[k]
        html = html[:m.start()] + new + html[m.end():]
        done += 1
    io.open(FINAL, "w", encoding="utf-8").write(html)
    return done


def refit_pre(loop=6):
    """渲染→量→縮→再渲染，直至無一段圍欄溢出或換行（或達回合上限）。
    稱語須點名管轄（幾段入稽核・哪幾段未入）與殘餘（哪幾段仍須縮）——免『0 段須縮』之綠出於未量。
    """
    import pymupdf

    blocks = FENCE_BLOCKS
    for rd in range(loop):
        need = pre_overflows(PDF, blocks)
        if not need:
            d = pymupdf.open(PDF)
            mp, _n, _m = pre_tag_map(blocks)
            au = pre_audit(d, blocks, pre_base_sizes(), mp)
            d.close()
            out = sorted(set(range(1, len(blocks) + 1)) - set(au))
            print("圍欄回量：第 %d 回合，%d/%d 段入稽核、俱合版寬且無換行，无须再縮%s"
                  % (rd + 1, len(au), len(blocks),
                     "" if not out else "（未入稽核：%s——須查）" % "、".join("#%d" % z for z in out)))
            return
        n = apply_pre_sizes(need, blocks)
        print("圍欄回量：第 %d 回合縮 %d 段（%s）"
              % (rd + 1, n, "、".join("#%d→%gpt" % (k, need[k]) for k in sorted(need)[:6])))
        b38.render_pdf()
    print("圍欄回量：達回合上限，末回合仍須縮 %d 段（%s）——須查（見 pre_overflows）"
          % (len(pre_overflows(PDF, blocks)),
             "、".join("#%d" % k for k in sorted(pre_overflows(PDF, blocks)))))


def toc_cache_load():
    """暖起點：上次收斂之目錄頁碼（以正字為鍵，改條目即自動落空，不攜舊號）。"""
    if not os.path.isfile(TOC_CACHE):
        return {}
    try:
        d = json.load(io.open(TOC_CACHE, encoding="utf-8"))
        if d.get("ver") != TOC_VER:
            print("目錄頁碼暖起點版號不合（%s），棄之冷起點" % d.get("ver"))
            return {}
        print("  目錄頁碼暖起點：%d 條／上次 %d 頁" % (len(d["pages"]), d.get("npage", -1)))
        return dict(d["pages"])
    except Exception as e:
        print("  目錄頁碼暖起點不可用，仍冷起點：", e)
        return {}


def toc_cache_save(pages, npage):
    try:
        json.dump({"ver": TOC_VER, "npage": npage, "pages": pages},
                  io.open(TOC_CACHE, "w", encoding="utf-8"), ensure_ascii=False)
    except Exception as e:
        print("  目錄頁碼暖起點寫盤失敗：", e)


def pass_once(toc_pages, items, ths):
    """一趟完整送排：中介 md（注入目錄頁碼）→ HTML → PDF → 圍欄回量 → 回量各條目之頁。"""
    lines, base = write_md(toc_pages)
    hs = headings(lines)
    global FENCE_BLOCKS
    FENCE_BLOCKS = fence_blocks(lines)
    b38.render_html([])                        # 目錄由書本自有，大綱留待冊內定位
    drop_hr_before_h1()
    mark_part_pages()
    if not SLIM:                               # 精簡版削附錄，無題可標（標不中即硬退，故先讓路）
        mark_appendix()
    pre_wide_span()
    b38.render_pdf()
    refit_pre()
    import pymupdf as pm
    d = pm.open(PDF)
    pages, rows, lost, via_full = toc_scan(d, items, ths)
    npage = d.page_count
    d.close()
    return lines, hs, pages, rows, lost, via_full, npage


def main():
    t0 = time.perf_counter()
    if not os.path.isfile(SRC):
        raise SystemExit("找不到來源檔：%s" % SRC)
    audit = "--toc-audit" in _ARGS
    _l0, base = write_md(None)                 # 形制趟（不注入）：目錄條目與正文標題之法源
    items, ths = toc_items(base), toc_headings(base)
    print("目錄條目 %d（部題 %d・章 %d・節 %d・目 %d）｜正文標題 %d"
          % (len(items), sum(1 for i in items if i[1] == 0), sum(1 for i in items if i[1] == 1),
             sum(1 for i in items if i[1] == 2), sum(1 for i in items if i[1] == 3), len(ths)))
    pages, toc_pages = toc_cache_load(), None
    for it in range(1, 6):
        lines, hs, toc_pages, rows, lost, via_full, npage = pass_once(pages, items, ths)
        stable = (toc_pages == pages)          # 注入之號＝此冊實測之號，即為不动點
        print("  目錄頁碼第 %d 回合：注入 %d 條・實測 %d 條／冊 %d 頁（標題靠全頁退路 %d）%s"
              % (it, len(pages), len(toc_pages), npage, via_full,
                 u"　← 收斂" if stable else ""))
        if stable:
            break
        pages = toc_pages
    else:
        raise SystemExit("目錄頁碼五回合未收斂（頁碼與頁數反覆）——須查：目錄注入改了行寬而全冊震盪")
    toc_cache_save(toc_pages, npage)
    ways = {}
    for _l, _d, _p, w, _h in rows:
        ways[w] = ways.get(w, 0) + 1
    print("  目錄配對方式：%s" % u"・".join(u"%s %d" % (k, ways[k]) for k in sorted(ways)))
    if audit:
        io.open(os.path.join(HERE, "_tocaudit%s.txt" % SFX), "w", encoding="utf-8").write(
            "\n".join(u"L%d\t%s\t%s\t%s\t%s" % r for r in rows))
        print("  目錄稽核表：%s（%d 行）" % (os.path.basename(
            os.path.join(HERE, "_tocaudit%s.txt" % SFX)), len(rows)))
    if lost:
        for x in lost[:12]:
            print("    無落點：%s" % x)
        raise SystemExit("目錄有 %d 條求不得頁碼（不造數、不靜默）——先補其正文之題或改條目" % len(lost))
    import pymupdf as pm
    import hulan_head
    d = pm.open(PDF)
    outline, miss = build_outline(d, hs)
    pairs, n_h1, via_h = head_pages(d)
    d.close()
    if not outline:
        print("內嵌大綱：零條——標題盡數定位失敗，須查 build_outline 之口徑")
    else:
        b38.stamp_pdf(PDF, outline, META)
        print("內嵌大綱：%d 條（定位失敗未入者 %d）｜書：%s"
              % (len(outline), len(miss), META["title"]))
        if miss:
            print("  未入大綱：%s" % "、".join(miss[:6]))
    # 頁眉最後蓋（第 78 輪）：Chromium 無 running elements，眉唯能在成冊之後寫入天頭。
    # 寫入不改版面，故頁數・目錄頁碼・圍欄回量皆不動；交付副本於此之後自產物再複製，
    # 眉・大綱・書訊隨副本同出（舊法先複製再對兩檔各蓋，今一改即兩檔同源）。
    if pairs:
        hr = hulan_head.stamp(PDF, pairs, BOOK_TITLE)
        print(u"  頁眉：章級 %d 條（定位退全頁 %d）・正文起 p%d・蓋 %d 頁・跳 %s"
              % (n_h1, via_h, hr["起"], hr["待蓋"], u"・".join(
                  u"%s %d" % kv for kv in sorted(hr["跳"].items()))))
    else:
        raise SystemExit(u"頁眉：章級之題定位 0 條——head_pages 之口徑或字級門有變，不靜默放行")
    npage = deliver()
    print("交付：%s｜%d 頁｜%d KB｜本次總用時 %d 秒"
          % (os.path.basename(PDF_OUT), npage, os.path.getsize(PDF_OUT) // 1024,
             time.perf_counter() - t0))


if __name__ == "__main__":
    main()
