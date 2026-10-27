# -*- coding: utf-8 -*-
"""雙子星兩冊之產器——《起心動念》（心法卷）・《如法推尋》（法制卷）。

法源不另起（承 列印SOP.md 今制）：pandoc 旗標・print38.css・無頭 Chromium 列印與落盤
四防・圍欄幾何回量・stamp_pdf 之書籤與書訊，俱借 _print/build38.py 與
_print/build_hulan.py 之現成件；本檔唯立兩冊之書參數與形制歸一。

形制歸一在**產物層**（正本一字不動，與護欄冊『目錄頁碼注入在產物層』同一今制）：
  篇 → H1・章 → H2・節 → H3・款 → H4・目 → H5
（心法卷原以 篇／章 俱作 H1、法制卷原以 章／節 俱作 H3，兩冊皆撞『一章兩 H1』
 『章節同階』之形，印面分頁與書籤層級遂無所依。）

用法：
  python -X utf8 _print/build_pair.py screen        # 兩冊各一 PDF（螢幕版・對稱邊距）
  python -X utf8 _print/build_pair.py print          # 兩冊各一 PDF（影印版・鏡像邊距）
  python -X utf8 _print/build_pair.py screen 1       # 只出第一冊
  python -X utf8 _print/build_pair.py screen --dry   # 只報形制與封面計數，不出冊
"""
import io
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, ROOT)

_ARGS = [a.lower() for a in sys.argv[1:]]
SCREEN = any("screen" in a or "螢幕" in a or "屏幕" in a for a in _ARGS)
DRY = "--dry" in _ARGS
ONLY = next((a for a in _ARGS if a in ("1", "2")), None)

# 先餽 build38 以本式之 argv（其 argv 解析於匯入時發生），再取護欄管線之增修（CSS・圍欄件）
_ARGV = sys.argv
sys.argv = ["build38", "full"] + (["screen"] if SCREEN else ["print"])
import build38 as b38            # noqa: E402
import build_hulan as bh         # noqa: E402  （匯入時已把 PRINT_CSS 增修掛上 b38）
sys.path.insert(0, os.path.join(ROOT, "_work"))
import paircase_lib as CL        # noqa: E402  （案號三形載體之共器：封面計數與刀・尺同源）
sys.argv = _ARGV

TAG = "_screen" if SCREEN else ""
TAGL = "螢幕版" if SCREEN else "影印版"
MERGED_STEM = u"雙子星合冊_起心動念＋如法推尋_"     # 合冊檔名之唯一法源（產器與覆核尺共此一名）
COVER_MUST = (chr(0x6B47), chr(0x548C), u"合 冊", u"起心動念", u"如法推尋",
              u"雙 子 星 大 典")                      # 合冊封面必見之字（產器自證與 pairface 己目同源）
COVER_EDGE = 45                                      # 封面一字不得越此界（同上，尺不另抄）


def merged_name(ed):
    return MERGED_STEM + ed + ".pdf"


def layout_pad(n1):
    """卷一有 n1 頁時，隔頁之後是否須補一空白頁（使卷二自 recto 起）。
    封面 1 頁＋卷一 n1 頁→隔頁落 2+n1（1-based）；為奇則落 recto，其後須補白，卷二方仍自 recto。"""
    return 1 if (2 + n1) % 2 == 1 else 0


def cjk_font(pg, kind="serif", tag="pf"):
    """把系統中文字型檔**嵌入**本頁，回其字型名。
    合冊封面與合璧說明是 pymupdf 直畫之頁，舊用內建 `china-s`／`china-ss`——PyMuPDF 之 CJK
    內建字型**不嵌入**（`get_page_fonts` 之 ext='n/a'），換檢視器即整頁隱形（外路實測：只見
    兩方框與數字，文字層俱在而畫不出）。故一律取字型檔，嵌入後方繪。"""
    win = os.environ.get("WINDIR", r"C:\Windows")
    cands = ("mingliu.ttc", "simsun.ttc") if kind == "serif" else ("msjh.ttc", "msyh.ttc")
    for n in cands:
        p = os.path.join(win, "Fonts", n)
        if os.path.isfile(p):
            nm = tag + ("s" if kind == "serif" else "h")
            pg.insert_font(fontname=nm, fontfile=p)
            return nm
    raise SystemExit(u"找不到可嵌入之中文字型檔（%s）——直畫之封面將成隱形字"
                     % u"／".join(cands))

cn = bh._cn

_HAN = "〇一二三四五六七八九十百"
RE_PIAN = re.compile(r"^#{1,6}\s*(第[%s]+篇[:：].*)$" % _HAN)
RE_ZHANG = re.compile(r"^#{1,6}\s*(第[%s]+章[　 ].*)$" % _HAN)
RE_JIE = re.compile(r"^#{1,6}\s*(第[%s]+節[　 ].*)$" % _HAN)
RE_END = re.compile(r"^#{1,6}\s*(終卷[　 ].*)$")
RE_CARD = re.compile(r"^#{1,6}\s*#{0,0}[【\[]?(?:制度)?案[卷例]")


TXT_PIAN = re.compile(r"^第[%s]+篇[:：]" % _HAN)
TXT_ZHANG = re.compile(r"^第[%s]+章[　 ]" % _HAN)
TXT_CARD = re.compile(r"^[【\[](?:制度)?案卷\s*[0-9]{2}")


def remap(lines):
    """篇→H1・章→H2・節→H3・款→H4・目→H5；圍欄內之『#』是框線圖，不動。"""
    out, fence, log = [], False, {"篇": 0, "章": 0, "節": 0, "款": 0, "目": 0, "終卷": 0}
    for l in lines:
        if re.match(r"^\s*```", l):
            fence = not fence
            out.append(l)
            continue
        if fence or not l.startswith("#"):
            out.append(l)
            continue
        s = l.strip()
        for rx, lv, key in ((RE_PIAN, 1, "篇"), (RE_ZHANG, 2, "章"), (RE_JIE, 3, "節"),
                           (RE_END, 2, "終卷")):
            m = rx.match(s)
            if m:
                out.append("#" * lv + " " + m.group(1))
                log[key] += 1
                break
        else:
            m = re.match(r"^(#{1,6})\s+(.*)$", s)
            if m and len(m.group(1)) >= 4:
                lv = len(m.group(1))
                log["款" if lv == 4 else "目"] += 1
            out.append(l)
    return out, log


def outline_pairs(lines):
    """歸一後之標題梯（圍欄內不取），供書籤與封面計數。"""
    out, fence = [], False
    for l in lines:
        if re.match(r"^\s*```", l):
            fence = not fence
            continue
        if fence:
            continue
        m = re.match(r"^(#{1,6})\s+(\S.*)$", l.strip())
        if m:
            out.append((len(m.group(1)), re.sub(r"[*`]", "", m.group(2)).strip()))
    return out


def cover_of(cfg, counts):
    """兩冊之專封面：同一骨架，四處相異——①眉標卷次 ②一字心印方印（歇／和，各出本卷終局之字）
    ③框線之制（卷一雙細線／卷二外粗內虛）④分隔帶（double 線／實夾線）。另立『姊妹篇＝卷N』互認一行，
    單頁在手即知為兩冊之哪一冊。純邊框與文字，不恃底色（無頭 Chromium 未開 print-background）。"""
    return """<section id="print-cover" class="cov pcov pcov-%s">
  <div class="pcov-out"><div class="pcov-in">
    <p class="pcov-series">雙 子 星 大 典</p>
    <p class="pcov-vol">%s・%s</p>
    <div class="pcov-seal"><span>%s</span></div>
    <p class="pcov-sealtag">本卷終局心印</p>
    <p class="pcov-sutra">大正藏第一四二八號・四分律</p>
    <p class="pcov-title">%s</p>
    <p class="pcov-sub">%s</p>
    <div class="pcov-band"></div>
    <p class="pcov-motto">%s<br />%s</p>
    <p class="pcov-count">%s・%s・%s</p>
    <p class="pcov-twin">姊妹篇《%s》＝%s・%s・終局心印『%s』</p>
    <p class="pcov-foot">第一版・%s　兩冊各自成冊，合冊本另為接排</p>
  </div></div>
</section>
""" % (cfg["frame"], cfg["vol"], cfg["vol_cn"], cfg["seal"], cfg["short"], cfg["subtitle"],
       cfg["motto1"], cfg["motto2"], counts["pian_c"], counts["zhang_c"], counts["cap"],
       cfg["sister"], cfg["sister_vol"], cfg["sister_cn"], cfg["sister_seal"], TAGL)


BOOKS = [
    dict(key="1", short=u"起心動念",
         file=u"起心動念：四分律的心智顯微鏡與唯識解剖.txt",
         subtitle=u"四分律的心智顯微鏡與唯識解剖", subtitle2=u"心法卷·心智現象學",
         motto1=u"修己之鏡，非量人之尺　平日但持三十二字",
         motto2=u"臨事唯照起心動念　鏡不照人，專照己心",
         out=u"起心動念_四分律的心智顯微鏡與唯識解剖_",
         sister=u"如法推尋",
         vol=u"卷 一", vol_cn=u"心 法 卷", seal=chr(0x6B47),          # 歇
         sister_vol=u"卷 二", sister_cn=u"法 制 卷", sister_seal=chr(0x548C),  # 和
         frame="a",
         part=re.compile(u"第[一二三四五六七八九十]+篇[:：]")),
    dict(key="2", short=u"如法推尋",
         file=u"如法推尋：僧伽憲政、法權審理與修復正義.txt",
         subtitle=u"僧伽憲政、法權審理與修復正義", subtitle2=u"法制卷·制度憲政學",
         motto1=u"給權力套上鎖鏈　給跌倒者回家的階梯",
         motto2=u"案結諍平，法架自捨　正法久住，天下無事",
         out=u"如法推尋_僧伽憲政法權審理與修復正義_",
         sister=u"起心動念",
         vol=u"卷 二", vol_cn=u"法 制 卷", seal=chr(0x548C),          # 和
         sister_vol=u"卷 一", sister_cn=u"心 法 卷", sister_seal=chr(0x6B47),  # 歇
         frame="b",
         part=re.compile(u"第[一二三四五六七八九十]+篇[:：]")),
]

b38.PRINT_CSS = b38.PRINT_CSS + (
    "\n/* 雙子星兩冊之形制歸一：章（H2）另起一頁；篇 Banner 不獨佔一頁 */\n"
    "h2 { break-before: page; }\n"
    ".part-open + h2 { break-before: avoid; }\n"
    ".part-open { break-after: avoid; }\n"
    "/* 一字心印（原 TeX display math・產物層化）*/\n"
    ".onechar { text-align: center; font-weight: 700; letter-spacing: .18em;"
    " margin: 1.5em 0 1.1em; }\n"
    "/* 頁碼口徑歸一：兩冊卷首已印絕對阿拉伯頁（五十輪定案之延伸），目錄頁不得中途改羅馬，"
    "故覆寫 print38.css 之 `page: toc`——目錄所報之號須與頁腳所印者同形。*/\n"
    ".toc-lead { page: auto; }\n"
    "/* 目錄長條折行之續行：貼緊前一行、無多餘間隔（折行保字級，不縮字）*/\n"
    ".toc-cont { line-height: 1.12; margin: 0 0 -.18em; }\n"
    "/* 標題不落頁底：節／卡之題與其下第一塊同頁（外路第十六報告：案卷卡之題與引文孤立\n"
    "   頁底而正文全在次頁）；表圖之題同法，不與其表分家。惟 .part-open 已另有其制。*/\n"
    "h3, h4, h5 { break-after: avoid; }\n"
    "blockquote > p:first-child { break-after: avoid; }\n"
    ".keep { break-inside: avoid; }\n"
    "/* ── 雙子星專封面：兩冊同一骨架，四處相異（眉標卷次・一字心印方印・框線之制・分隔帶）"
    "＋姊妹互認一行。純邊框與文字，不恃底色。── */\n"
    ".pcov { width: 210mm; height: 296.6mm; padding: 16mm 18mm 18mm; }\n"
    ".pcov-out { box-sizing: border-box; width: 100%; height: 100%;"
    " border: 2.4px solid #000; padding: 2.2mm; }\n"
    ".pcov-in { box-sizing: border-box; width: 100%; height: 100%; border: 1px solid #000;"
    " display: flex; flex-direction: column; align-items: center; justify-content: center;"
    " text-align: center; padding: 6mm 5mm; }\n"
    ".pcov-b .pcov-in { border: 1px dashed #000; }\n"
    ".pcov-series { font-size: 10.5pt; letter-spacing: .52em; text-indent: .52em;"
    " color: #333; margin: 0; }\n"
    ".pcov-vol { font-family: \"MingLiU\", \"PMingLiU\", serif; font-weight: 700; font-size: 15pt;"
    " letter-spacing: .3em; text-indent: .3em; color: #000; margin: 3.4mm 0 7mm; }\n"
    ".pcov-seal { box-sizing: border-box; width: 27mm; height: 27mm; border: 2.4px solid #000;"
    " display: flex; align-items: center; justify-content: center; margin: 0 0 2.6mm; }\n"
    ".pcov-seal span { font-family: \"MingLiU\", \"PMingLiU\", serif; font-size: 46pt;"
    " line-height: 1; font-weight: 600; color: #000; }\n"
    ".pcov-sealtag { font-size: 9.5pt; letter-spacing: .26em; text-indent: .26em;"
    " color: #555; margin: 0 0 8mm; }\n"
    ".pcov-sutra { font-size: 10.5pt; letter-spacing: .3em; text-indent: .3em;"
    " color: #444; margin: 0; }\n"
    ".pcov-title { font-family: \"MingLiU\", \"PMingLiU\", serif; font-size: 33pt;"
    " font-weight: 600; letter-spacing: .22em; text-indent: .22em; line-height: 1.25;"
    " color: #000; margin: 4.5mm 0 0; }\n"
    ".pcov-sub { font-size: 12.5pt; letter-spacing: .1em; color: #222; margin: 3.2mm 0 0;"
    " line-height: 1.7; }\n"
    ".pcov-band { width: 58mm; height: 0; border-top: 3px double #000; margin: 8mm auto; }\n"
    ".pcov-b .pcov-band { height: 2.6mm; border-top: 2px solid #000;"
    " border-bottom: 1px solid #000; }\n"
    ".pcov-motto { font-family: \"MingLiU\", \"PMingLiU\", serif; font-size: 13pt;"
    " line-height: 2; letter-spacing: .12em; text-indent: .12em; color: #000;"
    " font-weight: 600; margin: 0; }\n"
    ".pcov-count { font-size: 10.5pt; letter-spacing: .18em; text-indent: .18em;"
    " color: #444; margin: 5mm 0 0; }\n"
    ".pcov-twin { font-size: 10.5pt; letter-spacing: .08em; color: #111; margin: 9mm 0 0;"
    " border-top: 1px solid #999; padding-top: 3.4mm; }\n"
    ".pcov-foot { font-size: 10pt; letter-spacing: .16em; text-indent: .16em;"
    " color: #555; margin: 6mm 0 0; }\n"
)


def demath(lines):
    """兩冊卷末之『一字心印』以 TeX display math 出之（$$\\Huge \\text{「 歇 」}$$）——
    無頭列印不載 MathJax，紙上會見原式。印面不需公式，故於產物層化為置中大字之 HTML 塊。"""
    out, done, dollar, fence = [], 0, [], False
    for k, l in enumerate(lines, 1):
        if re.match(r"^\s*```", l):
            fence = not fence
            out.append(l)
            continue
        if fence:
            out.append(l)
            continue
        m = re.match(r"^\s*\$\$(.+?)\$\$\s*$", l)
        if m:
            body = m.group(1)
            inner = "".join(re.findall(r"\\text\{([^}]*)\}", body)) or \
                re.sub(r"\\[a-zA-Z]+|[{}$\\]", "", body).strip()
            size = "34pt" if "huge" in body.lower() else "24pt"
            out.append(u'<p class="onechar" style="font-size:%s">%s</p>' % (size, inner))
            done += 1
            continue
        if "$" in l:
            dollar.append((k, l.strip()[:44]))
        out.append(l)
    return out, done, dollar


def audit_headings(md_path, html_path):
    """同 build38 之產物自證，唯加一事：pandoc 之 smart 擴將直撇號『'』排成曲撇『’』，
    舊比對不折此異體，遂以『DON'Ts』對『DON’Ts』報假漏失（本冊第十四章兩題親踩）。
    折異體而不放寬其餘——題文仍須同級、仍須在冊。"""
    from html import unescape

    def norm(s):
        s = unescape(re.sub(r"<[^>]+>", "", s))
        s = re.sub(u"[\\u2018\\u2019\\u02bc']", "'", s)
        s = re.sub(u"[\\u201c\\u201d]", '"', s)
        return re.sub(r"\s+", "", s).replace("*", "").replace("`", "")

    pool = {}
    for m in re.finditer(r"<h([1-6])(\s[^>]*)?>(.*?)</h\1>",
                         open(html_path, encoding="utf-8").read(), re.S | re.I):
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
    print(u"  標題覆核：源 %d 行俱化為同級元素（撇號異體已折）・册內 h1..h6 = %s"
          % (nmd, [len(pool.get(k, [])) for k in range(1, 7)]))


b38.audit_headings = audit_headings        # 兩冊之標題覆核取折異體之口徑（不改 build38 在役件）

# ── 目錄頁碼：法源一本（正文標題），頁碼在產物層反查印面後注入 ──────────────
TOC_HEAD = re.compile(u"^#{1,2}\\s*【全書標準總目錄】")
b38.skip_in_toc = lambda lvl, title: str(title).startswith(
    (u"【全書五篇二十章結構全貌圖", u"【全書四篇十二章結構全貌圖", u"【全書標準總目錄", u"目　　錄"))
CARD_T = re.compile(u"[【\\[](?:制度)?案卷")

# ── 目錄行覆寫：長條**折行**，不縮字 ────────────────────────────────────────
# build38.toc_line 遇超長條目即按比例縮字，本冊三條案卷卡遂排成 9.3／10.0／10.4pt，
# 破其自報之下限 10.5（第十四波實測）。目錄之細字仍是印面之細字，往册已結之
# 『細字一案』同一病根，故治在產生器（折行保級），不治在閾值（把下限放低即自欺）。
TOC_BRK = u"：、（，；—|"          # 折點候選：語意界，切後各自成讀
TOC_TAIL_DOT = 3                  # 末行至少三點，否則頁碼貼死標題
TOC_MAX_LINES = 3                 # 一條最多三行；仍不合者如實交舊路縮字並報警
_toc_line_orig = b38.toc_line
TOC_SPLIT = []                            # 折行之條目（管轄自印，不靜默）


def toc_line_split(lvl, title, page):
    label = b38.TOC_LABEL.get(lvl, u"　　　　")
    base = b38.TOC_BASE_SIZE.get(lvl, 12.0)
    bold = (lvl == 1)
    size = base * b38.PDF_PT_SCALE
    room = b38.toc_room(lvl)
    dot_w = b38.TOC_DOT_EM * b38.TOC_LINE_SIZE * b38.PDF_PT_SCALE
    pg = str(page) if page else ""
    tail = b38._wpt(pg + " ", b38.TOC_LINE_SIZE * b38.PDF_PT_SCALE) if pg else 0.0
    budget = room - tail - TOC_TAIL_DOT * dot_w        # 末行『標題』可排之寬

    def w(s):
        return b38._wpt(label + s, size, bold)

    def pack(t, left):
        if w(t) <= budget:
            return [t]
        if left == 1:
            return None
        for i in [k for k, c in enumerate(t) if c in TOC_BRK and k < len(t) - 1][::-1]:
            if w(t[:i + 1]) <= room:
                r = pack(t[i + 1:], left - 1)
                if r:
                    return [t[:i + 1]] + r
        return None

    parts = None
    if pg and w(title) > budget:
        parts = pack(title, TOC_MAX_LINES)
        if parts and len(parts) == 1:
            parts = None                             # 舊路已足，不必折
    if not parts:
        return _toc_line_orig(lvl, title, page)
    TOC_SPLIT.append(title)
    cls = "toc-line toc-l%d" % lvl
    out = ['<p class="%s toc-cont"><span class="t">%s</span></p>' % (cls, x.replace("&", "&amp;"))
           for x in parts[:-1]]
    last = parts[-1]
    dots = max(TOC_TAIL_DOT, int((room - w(last) - tail) / dot_w))
    out.append('<p class="%s"><span class="t">%s</span><span class="d">%s </span>'
               '<span class="pg">%s</span></p>'
               % (cls, last.replace("&", "&amp;"), "." * dots, pg))
    return "\n".join(out)


b38.toc_line = toc_line_split


def toc_entries(hds):
    """條目＝篇(H1)・章(H2)・節(H3)＋案卷卡（H3/H4，卡名含【案卷】者）；款目一律歸三級。"""
    hs = [(min(lv, 3), t, 0) for lv, t in hds if lv <= 3 or (lv == 4 and CARD_T.search(t))]
    return b38.prepare_toc_entries(hs)



def fold(s):
    """標題在冊上之可比形：去粗體／反引號、摺平所有空白、撇號與引號之曲直折為一形
    （pandoc 之 smart 擴將 DON'Ts 排成 DON’Ts，不折即生假失指）。"""
    s = re.sub(r"[*`]", "", s)
    s = re.sub(u"[\\u2018\\u2019\\u02bc]", "'", s)
    s = re.sub(u"[\\u201c\\u201d]", '"', s)
    return re.sub(r"\s+", "", s)


DOT_ROW = re.compile(r"\.{3,}\s*[0-9]{1,4}\s*$")


def toc_pages_of(doc):
    """目錄所在頁：帶點線頁碼之行密集者（目錄頁含全書標題，不得充當標題之實頁）。"""
    out = set()
    for p in range(doc.page_count):
        lines = [l.strip() for l in doc[p].get_text().split("\n") if l.strip()]
        if sum(1 for l in lines if DOT_ROW.search(l)) >= 5:
            out.add(p + 1)
    return out


HEAD_MIN_PT = 13.4          # 正文 12.96pt；H4 13.74・H3 14.73・H2 17.86・篇題 23（俱實測）


def locate(doc, heads, skip=()):
    """標題在**已印出之冊**中定物理頁：單調游標＋**逐行**立尺（行首＋字級下限）。
    舊法以全頁摺平字串求『包含』——正文之預告句『【第三章 衡平動機…】。』與真標題同形，
    遂先於真標題被逮（外路實測：目錄第三章印 26・H2 實在 27）。今以行為單位：行首須為
    標題（摺平後之前綴）且該行字級 ≥ 13.4pt，正文之提稱句（12.96pt）自不入；五級以下
    （款・目）字級近正文，仍用舊法之全頁比對，免書籤漏收。
    `skip` 為目錄頁集——目錄行內含全書標題，不擯之則『自序』等卷首之題會誤指目錄自己那頁。"""
    txt, rows = [], []
    for i in range(doc.page_count):
        txt.append(fold(doc[i].get_text()))
        if (i + 1) in skip:
            rows.append(None)
            continue
        ls = []
        for b in doc[i].get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                s = "".join(sp["text"] for sp in ln["spans"])
                if s.strip():
                    ls.append((fold(s), max(sp["size"] for sp in ln["spans"])))
        rows.append(ls)
    got, cur, miss, pm = [], 0, [], {}
    for lv, t in heads:
        f = fold(t)
        hit = None
        for p in list(range(cur, len(rows))) + list(range(0, cur)):   # 先游標之後，再回頭
            if rows[p] is None or not f:
                continue
            if lv <= 4:
                # 行首之判須『往返』：整題見於一行，或該行是題之首段（標題折行）。
                # 只取前 14 字作前綴則『…（篇·上）』與『…（篇·下）』相搶（實測：二籤同指 147）。
                hit_ok = any(sz >= HEAD_MIN_PT and
                             (lt.startswith(f) or (f.startswith(lt) and len(lt) >= 12))
                             for lt, sz in rows[p])
            else:
                hit_ok = f in txt[p]
            if hit_ok:
                hit = p + 1
                break
        if hit is None:
            miss.append(t[:22])
            continue
        cur = hit - 1
        got.append((lv, t, hit))
        pm.setdefault(f, []).append(hit)
    fixed, prev = [], 0
    for lv, t, pg in got:
        lv = min(lv, 4)
        if not fixed:
            lv = 1
        elif lv > prev + 1:
            lv = prev + 1
        fixed.append([lv, t[:80], pg])
        prev = lv
    return fixed, miss, pm


def entry_map(entries, pm):
    """目錄條目 → 印面實頁：按文取號，同名者依出現之序 consumption（不重複指同一頁）。"""
    use, out, lost = {}, {}, []
    for lv, disp, key in entries:
        k = fold(disp)
        i = use.get(k, 0)
        seq = pm.get(k) or []
        if i < len(seq):
            out[key] = seq[i]
            use[k] = i + 1
        else:
            lost.append(disp)
    return out, lost



def build(cfg):
    src = os.path.join(ROOT, cfg["file"])
    if not os.path.isfile(src):
        raise SystemExit("找不到來源檔：%s" % src)
    raw = io.open(src, encoding="utf-8-sig").read()
    lines = raw.replace("\r\n", "\n").split("\n")
    n_src = len(lines)
    lines, log = remap(lines)
    lines, n_math, dollar = demath(lines)
    heads = outline_pairs(lines)
    # 案之戶口一以共器 paircase_lib 定義（刀・尺・產生器三處同取，名單勿兩抄）：
    #   『卡』=【案卷 NN】之標題數（雙聯合一卡）；『案』=其案號（雙聯各計）＋子案（帶字母者各計一）
    card_titles = [t for lv, t in heads if lv >= 3 and TXT_CARD.match(t.strip())]

    def _sub(t):
        return bool(CL.SUB.search(t))

    nums = {int(x) for t in card_titles if not _sub(t)
            for x in re.findall(r"\d{2,3}", t.split("】")[0])}
    nsub = sum(1 for t in card_titles if _sub(t))
    n_case = len(nums) + nsub           # 卡所涵之案號（雙聯各計）＋子案（帶字母者各計一）
    topics = {int(x) for x in re.findall(r"【專題\s*(\d{2})[：:]", raw)}
    modern = {int(x) for x in re.findall(r"〔案例\s*現(\d{2})〕", raw)}
    pian = sum(1 for lv, t in heads if lv == 1 and TXT_PIAN.match(t))
    zhang = sum(1 for lv, t in heads if lv == 2 and TXT_ZHANG.match(t))
    counts = dict(pian=pian, zhang=zhang, cases=n_case, ncard=len(card_titles),
                  topics=len(topics), modern=len(modern))
    capbits = []
    if counts["ncard"]:
        capbits.append(u"案卷 %s 卡・%s 案" % (cn(counts["ncard"]), cn(counts["cases"])))
    if counts["topics"]:
        capbits.append(u"調部專題 %s 則" % cn(counts["topics"]))
    if counts["modern"]:
        capbits.append(u"現代四境 %s 則" % cn(counts["modern"]))
    counts["cap"] = u"・".join(capbits) or u"案卷俱在章中"
    counts["pian_c"] = u"%s篇" % cn(pian)
    counts["zhang_c"] = u"%s章" % cn(zhang)
    print("\n" + "=" * 72)
    print("■ %s｜%s" % (cfg["short"], cfg["file"]))
    print("  形制歸一：篇 %d・章 %d・節 %d・款 %d・目 %d・終卷 %d（源 %d 行）"
          % (log["篇"], log["章"], log["節"], log["款"], log["目"], log["終卷"], n_src))
    print("  封面計數（自正文取）：%s・%s・%s" % (counts["pian_c"], counts["zhang_c"], counts["cap"]))
    print("  標題梯共 %d 枚（H1 %d・H2 %d・H3 %d・H4 %d・H5 %d）"
          % (len(heads), *[sum(1 for lv, _ in heads if lv == k) for k in (1, 2, 3, 4, 5)]))
    print("  公式化印：display math %d 塊轉置中大字・殘留 $ 之行 %d" % (n_math, len(dollar)))
    for k, s in dollar[:4]:
        print("       · L%d「%s」" % (k, s))
    if DRY:
        print("  （--dry：不出冊）")
        return
    stem = cfg["out"] + TAGL
    md = os.path.join(HERE, "pair_%s%s.md" % (cfg["key"], TAG))
    html = os.path.join(HERE, "pair_%s%s.html" % (cfg["key"], TAG))
    final = os.path.join(HERE, "final_pair%s%s.html" % (cfg["key"], TAG))
    pdf = os.path.join(HERE, "pair%s%s.pdf" % (cfg["key"], TAG))
    pdf_out = os.path.join(HERE, stem + ".pdf")

    # 目錄：正本之 markdown 目錄塊不再入印（頁碼須自印面反查，唯產物層能給），
    # 今改由 build38 之點線目錄生成器接手——法源仍是正文標題，不另抄名單。
    itoc = next((k for k, l in enumerate(lines) if TOC_HEAD.match(l)), None)
    entries = toc_entries(heads)
    if itoc is not None:
        jtoc = next((k for k in range(itoc + 1, len(lines)) if re.match(r"^#{1,2}\s", lines[k])), len(lines))
        lines[itoc:jtoc] = [u"<!--TOC-PLACEHOLDER-->\n"]
        print("  產物層換目錄：削 markdown 目錄塊 %d 行，佔位立於 L%d・目錄條目 %d 條"
              % (jtoc - itoc, itoc + 1, len(entries)))
    else:
        i = next((k for k, l in enumerate(lines)
                  if re.match(u"^#\\s*第[一二三四五六七八九十]+篇", l)), None)
        if i is None:
            i = next((k for k, l in enumerate(lines) if l.startswith("## ")), None)
        if i is None:
            raise SystemExit("產物層定位失敗：無篇題亦無 H2 可放目錄佔位")
        lines.insert(i, u"<!--TOC-PLACEHOLDER-->\n")
        if lines[i - 1].strip():
            lines.insert(i, u"")
        print("  目錄佔位居於**正文之前、卷首之後**（源檔無目錄塊）・條目 %d 條" % len(entries))
    n0 = len(lines)
    lines = b38.ensure_blank(lines)
    io.open(md, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print("  中介 md：%d 行→%d 行（ensure_blank 補空行 %d）" % (n0, len(lines), len(lines) - n0))

    b38.MD, b38.HTML, b38.FINAL, b38.PDF = md, html, final, pdf
    b38.COVER, b38.EDITION, b38.APPS = cover_of(cfg, counts), u"第一版·" + TAGL, counts["cap"]
    bh.MD, bh.HTML, bh.FINAL, bh.PDF, bh.PDF_OUT = md, html, final, pdf, pdf_out
    bh.PART = cfg["part"]
    meta = {"title": u"%s｜%s｜%s｜%s" % (cfg["short"], cfg["subtitle"], cfg["subtitle2"], TAGL),
            "author": u"編者", "subject": cfg["subtitle2"],
            "keywords": u"四分律；毘奈耶；%s；大正藏 No.1428" % cfg["short"],
            "creator": u"build_pair 管線（沿用 build38 之法源：pandoc → 無頭 Chromium 列印）",
            "producer": u"build_pair"}

    t0 = time.perf_counter()

    def render(rows):
        b38.render_html(rows)
        bh.drop_hr_before_h1()
        bh.mark_part_pages()
        bh.pre_wide_span()
        b38.render_pdf()

    import pymupdf
    MARK = u"<!--TOC-A--><!--TOC-B-->"
    render([MARK])                                       # 佔位先印：此後只改 FINAL 之目錄段，不再生 md
    bh.FENCE_BLOCKS = bh.fence_blocks(lines)
    print("  圍欄段：%d 段入回量" % len(bh.FENCE_BLOCKS))
    bh.refit_pre()                                       # 圍欄字級先定（否則回填後之縮字會挪頁）
    with pymupdf.open(pdf) as d0:
        pages, lost = entry_map(entries, locate(d0, heads)[2])
    for rd in range(6):
        rows = u"\n".join(b38.build_toc_html(entries, {k: str(v) for k, v in pages.items()}))
        html = io.open(bh.FINAL, encoding="utf-8").read()
        html = re.sub(u"(?s)<!--TOC-A-->.*?<!--TOC-B-->",
                      lambda m: u"<!--TOC-A-->" + rows + u"<!--TOC-B-->", html, count=1)
        io.open(bh.FINAL, "w", encoding="utf-8").write(html)
        b38.render_pdf()
        with pymupdf.open(pdf) as d1:
            newp, newlost = entry_map(entries, locate(d1, heads, skip=toc_pages_of(d1))[2])
            np0 = d1.page_count
        if newp == pages:
            lost = newlost
            print("  目錄頁碼：第 %d 回合收斂・入號 %d 條・冊 %d 頁" % (rd + 1, len(pages), np0))
            break
        pages = newp
        lost = newlost
    else:
        print("  ★目錄頁碼達回合上限，末回仍有位移——須查（免『未收斂之綠』）")
    if lost:
        print("  ★目錄未入號 %d 條：%s" % (len(lost), u"、".join(t[:26] for t in lost[:8])))
        raise SystemExit("目錄有虛號，不交付（標題在冊上求不得）")
    if TOC_SPLIT:
        uniq = sorted(set(TOC_SPLIT))          # 收斂各回合皆重排目錄，計數須去重（不然倍報）
        print("  目錄折行：%d 條（保級不縮字）：%s"
              % (len(uniq), u"、".join(t[:22] for t in uniq[:4])))
        del TOC_SPLIT[:]

    import pymupdf as pm
    d = pm.open(pdf)
    npage = d.page_count
    outline, miss, _pm = locate(d, heads, skip=toc_pages_of(d))
    d.close()
    b38.stamp_pdf(pdf, outline, meta)
    n = bh.deliver()
    b38.stamp_pdf(pdf_out, outline, meta)
    print("  交付：%s｜%d 頁｜%d KB｜大綱 %d 條（定位失敗 %d）｜用時 %d 秒"
          % (os.path.basename(pdf_out), n, os.path.getsize(pdf_out) // 1024,
             len(outline), len(miss), time.perf_counter() - t0))
    if miss:
        print("    未入大綱：%s" % u"、".join(miss[:8]))
    spine = [t for lv, t in heads if TXT_PIAN.match(t) or TXT_ZHANG.match(t)]
    lost_spine = [t for t in spine if any(t[:10] in m or m in t for m in miss)]
    print("  書籤骨幹（篇＋章）%d 條・未定位 %d 條・全梯命中 %d/%d"
          % (len(spine), len(lost_spine), len(outline), len(heads)))
    if lost_spine:
        raise SystemExit("篇・章之書籤求不得頁（不造數、不靜默）：%s"
                         % u"、".join(x[:16] for x in lost_spine[:6]))
    return pdf_out, n, len(outline), len(miss)


def divider_lines(a, b):
    """合璧說明之文（兩卷頁數一律自算——宣稱須實測，不許手打）。"""
    return [u"", u"", u"", u"雙 子 星 合 冊", u"", u"姊妹卷合璧說明", u"", u"──────", u"",
            u"心法卷《起心動念：四分律的心智顯微鏡與唯識解剖》　%d 頁" % a,
            u"法制卷《如法推尋：僧伽憲政、法權審理與修復正義》　%d 頁" % b, u"",
            u"本冊係兩卷接排，兩卷頁碼各自為起訖：前卷 %d 至 %d，後卷 %d 至 %d。" % (1, a, 1, b),
            u"兩冊之【全書標準總目錄】今由本管線之點線目錄生成器印出，**條條載頁碼**（頁碼自印成之冊反查回填，至收斂為止）；",
        u"頁碼為各冊自身之絕對頁，故合冊之中兩冊頁碼各自起訖——跨冊檢索仍以書籤之層級與章節之號為準。",
            u"跨卷之引（『《如法推尋》〔案例 NN〕』、『《起心動念》【案卷 NN】』之屬），",
            u"依兩冊卷首凡例第七律『跨冊案號之索』——以號索於彼冊即可，勿以頁碼尋之。", u"",
            u"另：兩卷各自之獨立檔（螢幕版・影印版）俱在，便於分卷誦讀與單卷印製。"]


def draw_pair_cover(pg, sizes, edition):
    """合冊之專封面（一頁看盡兩卷）：雙框＋兩方心印（歇／和）＋兩卷書名與自算頁數。
    居中一律交 `insert_textbox(align=1)`——手算字寬必偏（舊法右移且長行出框，實測現形）；
    每行取回之剩餘高度 <0 即擲（溢出不可靜默）。純黑白，影印分明。"""
    import pymupdf as pm
    w, h = pg.rect.width, pg.rect.height
    fs, fh = cjk_font(pg, "serif", "pcv"), cjk_font(pg, "sans", "pcv")
    for m, sw in ((34, 1.6), (41, 0.5)):
        pg.draw_rect(pm.Rect(m, m, w - m, h - m), color=(0, 0, 0), width=sw)
    IN = 52                                          # 內文距框之留白

    def cen(y, s, txt, font=None, lh=1.5):
        font = font or fs
        rc = pg.insert_textbox(pm.Rect(IN, y, w - IN, y + s * lh * 4), txt, fontname=font,
                               fontsize=s, lineheight=lh, color=(0, 0, 0), align=1)
        if rc < 0:
            raise SystemExit(u"合冊封面之文溢出框外（%s…）" % txt[:18])
        return rc

    cen(h * 0.20, 12.5, u"雙 子 星 大 典", font=fh)
    cen(h * 0.245, 19, u"合 冊　・　卷 一 ＋ 卷 二", font=fs)
    box, gap = 58.0, 46.0
    x_l = (w - 2 * box - gap) / 2
    for i, (ch, cap) in enumerate(((chr(0x6B47), u"心法卷終局心印"), (chr(0x548C), u"法制卷終局心印"))):
        x0 = x_l + i * (box + gap)
        top = h * 0.315
        pg.draw_rect(pm.Rect(x0, top, x0 + box, top + box), color=(0, 0, 0), width=1.5)
        rc = pg.insert_textbox(pm.Rect(x0 + 3, top + 3, x0 + box - 3, top + box - 3), ch,
                               fontname=fs, fontsize=30, lineheight=1.0,
                               color=(0, 0, 0), align=1)
        if rc < 0:
            raise SystemExit(u"印中之字放不下（box=%dpt・字 30pt）➔%s" % (box, ch))
        pg.insert_textbox(pm.Rect(x0 - 14, top + box + 5, x0 + box + 14, top + box + 24), cap,
                          fontname=fs, fontsize=9.0, color=(0.2, 0.2, 0.2), align=1)
    y = h * 0.475
    for i, (nm, sub) in enumerate((
            (u"起心動念", u"四分律的心智顯微鏡與唯識解剖"),
            (u"如法推尋", u"僧伽憲政、法權審理與修復正義"))):
        cen(y, 16, u"《%s》　%d 頁" % (nm, sizes[i]), font=fs)
        cen(y + 21, 10.5, sub, font=fh)
        y += 56
    pg.draw_line(pm.Point(w / 2 - 62, y - 12), pm.Point(w / 2 + 62, y - 12),
                 color=(0, 0, 0), width=1.1)
    cen(y + 14, 11, u"心法卷為修己之鏡　法制卷為立憲之柱　一體兩翼，名同位異", font=fh)
    for k, line in enumerate((
            u"本冊係兩卷接排：卷一 %d 頁在前，卷二 %d 頁在後。" % (sizes[0], sizes[1]),
            u"兩卷頁碼各自為起訖（見卷間『合璧說明』），跨冊之引依凡例第七律以號索之。",
            u"分卷之獨立檔（卷一・卷二，螢幕版與影印版）俱在，便於分卷誦讀與單卷印製。")):
        cen(y + 42 + k * 20, 10, line, font=fh)
    cen(h * 0.845, 11.5, u"第一版・%s" % edition, font=fh)
    # 產物層自證①：該上之字須真在冊上（`insert_textbox` 放不下時**靜默不畫**，
    # 橫界之檢查看不到『沒有字』——舊框 19.7pt 容 33pt 之印字遂成空框，今雙檢）。
    gone = [ch for ch in COVER_MUST if ch not in pg.get_text()]
    if gone:
        raise SystemExit(u"合冊封面缺字（畫了卻不見）：%s" % u"、".join(gone))
    # 產物層自證②：任何一字越內框半步即擲（`insert_textbox` 於無空格之中文不折行，
    # 橫向溢出非其回值所能報——故自量詞之邊界，不靠眼過）。
    bad = []
    for x0, y0, x1, y1, word, *_ in pg.get_text("words"):
        if x1 > w - COVER_EDGE or x0 < COVER_EDGE or y1 > h - COVER_EDGE or y0 < COVER_EDGE:
            bad.append(u"%s[%.0f,%.0f]" % (word[:8], x1, y1))
    if bad:
        raise SystemExit(u"合冊封面有字出框：%d 處 ➔ %s" % (len(bad), u"、".join(bad[:6])))


def merge(parts, meta):
    """兩冊合為一檔（合冊專封面・書籤接排・頁碼平移・卷間立『合璧說明』隔頁）。
    個別交付檔仍留存，合冊另出名，兩者同源同版。頁碼故不强行通編：兩卷各自之頁碼即其身分。"""
    import pymupdf as pm
    out_name = meta.pop("_out", merged_name(TAGL))
    d = pm.open()
    toc, cur = [], 0
    sizes = []
    for p0 in parts:
        t0 = pm.open(p0)
        sizes.append(t0.page_count)
        t0.close()
    div = divider_lines(sizes[0], sizes[1]) if len(sizes) > 1 else None
    if sizes:
        s0 = pm.open(parts[0])
        cov = d.new_page(pno=0, width=s0[0].rect.width, height=s0[0].rect.height)
        draw_pair_cover(cov, sizes, TAGL)
        s0.close()
        cur = 1                                      # 合冊封面占一頁：書籤一律右移一頁
    pad_i = div_i = vol2_i = None
    for i, p0 in enumerate(parts):
        s = pm.open(p0)
        extra = 0
        if i and div:
            w, h = s[0].rect.width, s[0].rect.height
            # 落版（recto/verso）：封面在 recto（1-based 奇數），雙面印時卷二之封面亦須落 recto。
            # 隔頁若不補白，卷二之起即隨卷一頁數之奇偶而漂——本波加一頁便現形（卷二封面落 p124＝verso）。
            # 今自算：隔頁落 verso（1-based 偶），卷二自 recto 起；隔頁若將落 recto，先補一空白。
            if layout_pad(sizes[0]):
                d.new_page(pno=d.page_count, width=w, height=h)
                pad_i = d.page_count - 1
                extra += 1
            n = d.page_count
            pg = d.new_page(pno=n, width=w, height=h)
            pg.insert_textbox(pm.Rect(58, 92, w - 58, h - 74), chr(10).join(div),
                              fontname=cjk_font(pg, "serif", "div"), fontsize=11.5, lineheight=1.62)
            toc.append([1, u"合璧說明", n + 1])
            div_i = n
            extra += 1
        if i:
            vol2_i = d.page_count
        d.insert_pdf(s)
        for lvl, t, pg2 in s.get_toc():
            toc.append([lvl, t, pg2 + cur + extra])
        cur += s.page_count + extra
        s.close()
    d.set_metadata(meta)
    d.set_toc(toc)
    if vol2_i is not None:                            # 落版之自證：隔頁落 verso・卷二自 recto 起
        if vol2_i % 2 != 0 or div_i % 2 != 1:
            raise SystemExit(u"落版不合（隔頁 0-based %s・卷二 0-based %s；應 奇／偶）"
                             % (div_i, vol2_i))
    # 邏輯頁碼標籤：兩卷各自起訖（合冊通編則檢視器之『第 50 頁』無從索，二卷之 50 頁相撞）。
    # 範圍：封面 1 頁・卷一・合璧說明 1 頁・卷二；號與頁腳所印者同形。
    labels = [{"startpage": 0, "prefix": u"封面", "style": "D", "firstpagenum": 1},
              {"startpage": 1, "prefix": u"卷一·", "style": "D", "firstpagenum": 1}]
    if vol2_i is not None:
        labels.append({"startpage": pad_i if pad_i is not None else div_i,
                       "prefix": u"合璧", "style": "D", "firstpagenum": 1})
        labels.append({"startpage": vol2_i, "prefix": u"卷二·", "style": "D", "firstpagenum": 1})
    d.set_page_labels(labels)
    # 子集化：封面／隔頁所嵌之明體・黑體本是整檔（一檔數十 MB），不縮則合冊由 6.7 MB 漲至 34 MB。
    # 只收本檔用到的字形（Chromium 之嵌入本已子集，重跑無損）；落檔後另以 pairface 辛目覆核。
    d.subset_fonts()
    out = os.path.join(HERE, out_name)
    d.save(out, garbage=3, deflate=True)
    n = d.page_count
    d.close()
    chk = pm.open(out)
    nl = len(chk.get_page_labels())
    chk.close()
    if nl != len(labels):
        raise SystemExit(u"邏輯頁碼標籤未落（寫 %d 段・讀回 %d 段）" % (len(labels), nl))
    print("\n合冊：%s｜%d 頁｜%d KB｜書籤 %d 條｜邏輯頁碼 %d 段"
          % (os.path.basename(out), n, os.path.getsize(out) // 1024, len(toc), nl))
    return out, n, len(toc)

def main():
    print("產器：build_pair｜版式：%s｜pandoc=%s｜瀏覽器=%s"
          % (TAGL, os.path.basename(b38.PANDOC), os.path.basename(b38.find_browser())))
    got = []
    for cfg in BOOKS:
        if ONLY and cfg["key"] != ONLY:
            continue
        r = build(cfg)
        if r:
            got.append(r)
    if DRY:
        return
    print("\n" + "=" * 72)
    for p, n, o, m in got:
        print("✓ %s｜%d 頁｜書籤 %d 條｜未定位 %d" % (os.path.basename(p), n, o, m))
    if len(got) == len(BOOKS):
        meta = {"title": u"雙子星合冊｜起心動念（心法卷）＋如法推尋（法制卷）｜%s" % TAGL,
                "author": u"編者", "subject": u"四分律之心智現象學與僧伽憲政學",
                "keywords": u"四分律；毘奈耶；心所；羯磨；大正藏 No.1428",
                "creator": u"build_pair 管線（沿用 build38 之法源）", "producer": u"build_pair",
                "_out": merged_name(TAGL)}
        merged, mn, mtoc = merge([g[0] for g in got], meta)
        print("✓ %s｜%d 頁・書籤接排 %d 條" % (os.path.basename(merged), mn, mtoc))


if __name__ == "__main__":
    main()
