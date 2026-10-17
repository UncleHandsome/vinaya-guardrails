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


def write_md():
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
    io.open(MD, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    n = sum(1 for l in lines if l.startswith("# "))
    print("源：%s｜行=%d→%d（正規化補空行 %d）｜H1=%d｜中介 md 已出"
          % (os.path.basename(SRC), n0, len(lines), len(lines) - n0, n))
    return lines


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
    """逐條標題在**已印出之冊**中向前搜其字面，定物理頁（不信任何算式）。
    字面須先摺去所有空白——印面折行會插斷整串搜尋（第 223／240 輪之誡）。"""
    pages = [re.sub(r"\s+", "", doc[i].get_text()) for i in range(doc.page_count)]
    cur, out, miss = 0, [], []
    for lvl, title in hs:
        key = title[:12]
        if not key:
            continue
        got = None
        for cand in range(cur, len(pages)):
            if key in pages[cand]:
                got = cand
                break
        if got is None:                       # 向前搜不到，回頭自 0 再搜一次
            for cand in range(len(pages)):
                if key in pages[cand]:
                    got = cand
                    break
        if got is None:
            miss.append(title[:16])
            continue
        cur = got
        out.append([min(lvl, 4), title[:80], got + 1])
    fixed, prev = [], 0                        # PDF 大綱：自 1 起，每次至多降一級
    for lv, ti, pg in out:
        if not fixed:
            lv = 1
        elif lv > prev + 1:
            lv = prev + 1
        fixed.append([lv, ti, pg])
        prev = lv
    return fixed, miss


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
    """令圍欄內之東亞寬字（ord≥0x2E80）以 1.1em 出字。

    印面實測（第 244 輪）：Consolas 之框線／數字／空白步進 0.55em，正黑之 CJK 步進 1.00em，
    比值 1.82；而源檔 22 段框線圖一律以「CJK＝兩格、框線＝一格」（即 2:1）排格，
    故欄位必逐格左漂——十三僧殘五道防線圖至第五欄已錯開近一字。將寬字放大 10% 後
    比值恰為 2.00，`_cw` 之格寬模型與印面相符，fit_pre_blocks 之縮字亦隨之準確。
    標籤皆純 ASCII（ord<0x2E80），故包 span 不會截斷既有標記或字元實體。
    """
    html = io.open(FINAL, encoding="utf-8").read()

    def one(m):
        head, inner, tail = m.group(1), m.group(2), m.group(3)
        out, run = [], []

        def flush():
            if run:
                out.append('<span class="pw">' + "".join(run) + "</span>")
                del run[:]

        for ch in inner:
            if ord(ch) >= 0x2E80:
                run.append(ch)
            else:
                flush()
                out.append(ch)
        flush()
        return head + "".join(out) + tail

    new, n = re.subn(r"(?s)(<pre\b[^>]*>)(.*?)(</pre>)", one, html)
    if n:
        io.open(FINAL, "w", encoding="utf-8").write(new)
    print("圍欄寬字加 span：%d 段（CJK 出字 1.1em，合 2:1 格寬）" % n)


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


def pre_overflows(pdf, blocks):
    """以印面實測回量每段圍欄：所在頁、內容左界、窄字字級、最長格數。
    須縮者回傳 {段序: 新字級}。不再猜容器內距——左界與字級俱由冊中量出，
    故 blockquote／列表／邊框之類任何縮排來源一律自動吸收。
    """
    import pymupdf

    d = pymupdf.open(pdf)

    def nn(s):
        return "".join(s.split())

    pages = [nn(d[i].get_text()) for i in range(d.page_count)]
    need = {}
    for k, b in enumerate(blocks, 1):
        head, tail = nn(b[0])[:12], nn(b[-1])[:12]
        at = next((i for i, t in enumerate(pages) if head in t and tail in t), None)
        if at is None:
            continue
        rows = []
        for bl in d[at].get_text("rawdict")["blocks"]:
            for ln in bl.get("lines", []):
                txt = "".join(c["c"] for sp in ln.get("spans", []) for c in sp["chars"])
                if not txt.strip():
                    continue
                sz = min(sp.get("size", 99.0) for sp in ln.get("spans", []))
                rows.append((ln["bbox"][1], ln["bbox"][0], ln["bbox"][2], sz, nn(txt)))
        ys = [r[0] for r in rows if r[4].startswith(head)]
        ye = [r[0] for r in rows if r[4].startswith(tail)]
        if not ys or not ye:
            continue
        seg = [r for r in rows if ys[0] - 1 <= r[0] <= max(ye) + 2]
        x0 = min(r[1] for r in seg)
        # 取段內最小字級＝窄字（Consolas）之級；寬字 span 為 1.1 倍，若誤取大者必永不收斂。
        size = min(r[3] for r in seg)
        wmax = max(cw_units(x) for x in b)
        # 右界不採假設之頁邊距——本冊鏡像排版（外 10mm／內 18mm），奇偶頁可用寬不同。
        # 逕取該段圍欄之灰底框（pre 之 border box）右緣，內距與框線一併扣掉。
        box = [g["rect"] for g in d[at].get_drawings()
               if g.get("fill") and seg[0][0] - 2 <= g["rect"].y0 <= max(ye) + 2
               and g["rect"].x0 <= x0 + 1 and g["rect"].x1 > x0 + 100]
        right = min((r.x1 for r in box), default=d[at].rect.width - 51.0)
        avail = right - 0.55 * size - 1.2 - x0
        if 0.55 * wmax * size > avail + 0.5:
            need[k] = round(max(6.2, avail / (0.55 * wmax + 1.1)), 2)
    d.close()
    return need


def apply_pre_sizes(sizes):
    """把第 k 段 pre 之 inline 字級改為量得之值（只改標籤，不動內容）。
    一次取全部標籤、由後而前改寫，免位移錯號。"""
    html = io.open(FINAL, encoding="utf-8").read()
    tags = [m for m in re.finditer(r"(?s)<pre\b[^>]*>", html)]
    done = 0
    for k in sorted(sizes, reverse=True):
        if k > len(tags):
            break
        m = tags[k - 1]
        head = m.group(0)
        new = re.sub(r"font-size:\s*[\d.]+pt", "font-size:%gpt" % sizes[k], head)
        if new == head:
            new = head[:-1].rstrip() + ' style="font-size:%gpt;">' % sizes[k]
        html = html[:m.start()] + new + html[m.end():]
        done += 1
    io.open(FINAL, "w", encoding="utf-8").write(html)
    return done


def refit_pre(loop=3):
    """渲染→量→縮→再渲染，直至無一段圍欄溢出（或達回合上限）。"""
    blocks = FENCE_BLOCKS
    for rd in range(loop):
        need = pre_overflows(PDF, blocks)
        if not need:
            print("圍欄回量：第 %d 回合，%d 段俱合版寬，無須再縮" % (rd + 1, len(blocks)))
            return
        n = apply_pre_sizes(need)
        print("圍欄回量：第 %d 回合縮 %d 段（%s）"
              % (rd + 1, n, "、".join("#%d→%gpt" % (k, need[k]) for k in sorted(need)[:6])))
        b38.render_pdf()


def main():
    t0 = time.perf_counter()
    if not os.path.isfile(SRC):
        raise SystemExit("找不到來源檔：%s" % SRC)
    lines = write_md()
    hs = headings(lines)
    global FENCE_BLOCKS
    FENCE_BLOCKS = fence_blocks(lines)
    b38.render_html([])                        # 目錄由書本自有，大綱留待冊內定位
    drop_hr_before_h1()
    mark_part_pages()
    pre_wide_span()
    b38.render_pdf()
    refit_pre()
    npage = deliver()
    import pymupdf as pm
    d = pm.open(PDF)
    outline, miss = build_outline(d, hs)
    d.close()
    if not outline:
        print("內嵌大綱：零條——標題盡數定位失敗，須查 build_outline 之口徑")
    else:
        b38.stamp_pdf(PDF, outline, META)
        b38.stamp_pdf(PDF_OUT, outline, META)
        print("內嵌大綱：%d 條（定位失敗未入者 %d）｜書：%s"
              % (len(outline), len(miss), META["title"]))
        if miss:
            print("  未入大綱：%s" % "、".join(miss[:6]))
    print("交付：%s｜%d 頁｜%d KB｜本次總用時 %d 秒"
          % (os.path.basename(PDF_OUT), npage, os.path.getsize(PDF_OUT) // 1024,
             time.perf_counter() - t0))


if __name__ == "__main__":
    main()
