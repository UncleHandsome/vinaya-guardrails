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
    return """<section id="print-cover" class="cov">
  <p class="cov-eyebrow">大正藏第一四二八號·四分律</p>
  <div class="cov-main">
    <div class="cov-sutra">%s</div>
    <div class="cov-title">%s</div>
    <div class="cov-rule"></div>
    <p class="cov-sub">%s</p>
    <p class="cov-motto">%s<br />%s</p>
    <p class="cov-cap">%s・%s・%s</p>
  </div>
  <div class="cov-foot">
    <p class="cov-edition">第一版·%s</p>
    <p class="cov-meta">原典：漢譯《四分律》六十卷<br />姊妹篇《%s》互參</p>
  </div>
</section>
""" % (cfg["short"], cfg["subtitle"], cfg["subtitle2"], cfg["motto1"], cfg["motto2"],
       counts["pian_c"], counts["zhang_c"], counts["cap"], TAGL, cfg["sister"])


BOOKS = [
    dict(key="1", short=u"起心動念",
         file=u"起心動念：四分律的心智顯微鏡與唯識解剖.txt",
         subtitle=u"四分律的心智顯微鏡與唯識解剖", subtitle2=u"心法卷·心智現象學",
         motto1=u"修己之鏡，非量人之尺　平日但持三十二字",
         motto2=u"臨事唯照起心動念　鏡不照人，專照己心",
         out=u"起心動念_四分律的心智顯微鏡與唯識解剖_",
         sister=u"如法推尋",
         part=re.compile(u"第[一二三四五六七八九十]+篇[:：]")),
    dict(key="2", short=u"如法推尋",
         file=u"如法推尋：僧伽憲政、法權審理與修復正義.txt",
         subtitle=u"僧伽憲政、法權審理與修復正義", subtitle2=u"法制卷·制度憲政學",
         motto1=u"給權力套上鎖鏈　給跌倒者回家的階梯",
         motto2=u"案結諍平，法架自捨　正法久住，天下無事",
         out=u"如法推尋_僧伽憲政法權審理與修復正義_",
         sister=u"起心動念",
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
    "/* 目錄長條折行之续行：貼緊前一行、無多餘間隔（折行保字級，不縮字）*/\n"
    ".toc-cont { line-height: 1.12; margin: 0 0 -.18em; }\n"
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


def locate(doc, heads, skip=()):
    """標題在**已印出之冊**中定物理頁：單調游標＋全頁文字摺空白（印面折行會插斷整串搜尋）。
       `skip` 為目錄頁集——目錄行內含全書標題，不擯之則『自序』等卷首之題會誤指目錄自己那頁。"""
    txt = [fold(doc[i].get_text()) for i in range(doc.page_count)]
    pages = [None if (i + 1) in skip else txt[i] for i in range(len(txt))]
    got, cur, miss, pm = [], 0, [], {}
    for lv, t in heads:
        f = fold(t)
        hit = None
        for p in range(cur, len(pages)):
            if f and pages[p] and f in pages[p]:
                hit = p + 1
                break
        if hit is None:                      # 游標之後求不得，回頭全冊再掃一次
            for p in range(len(pages)):
                if f and pages[p] and f in pages[p]:
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


def merge(parts, meta):
    """兩冊合為一檔（書籤接排・頁碼平移・卷間立『合璧說明』隔頁）——供『兩本建成一個 PDF』之讀法。
    個別交付檔仍留存，合冊另出名，兩者同源同版。頁碼故不强行通編：兩卷各自之頁碼即其身分。"""
    import pymupdf as pm
    out_name = meta.pop("_out", u"雙子星合冊_%s.pdf" % TAGL)
    d = pm.open()
    toc, cur = [], 0
    sizes = []
    for p0 in parts:
        t0 = pm.open(p0)
        sizes.append(t0.page_count)
        t0.close()
    div = divider_lines(sizes[0], sizes[1]) if len(sizes) > 1 else None
    for i, p0 in enumerate(parts):
        s = pm.open(p0)
        shift = 0
        if i and div:
            w, h = s[0].rect.width, s[0].rect.height
            n = d.page_count
            pg = d.new_page(pno=n, width=w, height=h)
            pg.insert_textbox(pm.Rect(58, 92, w - 58, h - 74), chr(10).join(div),
                              fontname="china-s", fontsize=11.5, lineheight=1.62)
            toc.append([1, u"合璧說明", n + 1])
            shift = 1
        d.insert_pdf(s)
        for lvl, t, pg2 in s.get_toc():
            toc.append([lvl, t, pg2 + cur + shift])
        cur += s.page_count + shift
        s.close()
    d.set_metadata(meta)
    d.set_toc(toc)
    out = os.path.join(HERE, out_name)
    d.save(out, garbage=3, deflate=True)
    n = d.page_count
    d.close()
    print("\n合冊：%s｜%d 頁｜%d KB｜書籤 %d 條"
          % (os.path.basename(out), n, os.path.getsize(out) // 1024, len(toc)))
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
                "_out": u"雙子星合冊_起心動念＋如法推尋_%s.pdf" % TAGL}
        merged, mn, mtoc = merge([g[0] for g in got], meta)
        print("✓ %s｜%d 頁・書籤接排 %d 條" % (os.path.basename(merged), mn, mtoc))


if __name__ == "__main__":
    main()
