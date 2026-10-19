# -*- coding: utf-8 -*-
"""《佛陀的護欄・四分律行為心理學與現代僧伽治理》合編本・列印管線。

法源不另起：pandoc 旗標、print38.css、字級覆寫、ensure_blank、render_html／render_pdf／
stamp_pdf、圍欄回量、部題 Banner、drop_hr_before_h1、pre_wide_span、deliver 諸件
皆取 build_hulan／build38 之現成函式（第 173 輪『小樣不同旗標即不同書』之誡）。

本冊獨有者三：
① 封面計數自冊身取（部・章・節・案・附錄），不手打；
② 印面清創之殘留名單改依本冊之工具名（_book／relink…），有殘即退；
③ 目錄走 build38 之收斂法——冊身那份無頁碼之【本書總目錄】於印面剷去，改由管線以
   『渲染→掃描冊內大字級標題→回填頁碼』反覆至頁數與頁碼俱定；出冊後再驗印面
   （目錄有碼・圍欄不換行・不出框・不斷頁），有病即退。
用法：python -X utf8 _print/build_book.py [print|screen] [noseed]
"""
import io
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, ROOT)
import build_hulan as BH                                   # noqa: E402
import build38 as b38                                      # noqa: E402

_ARGS = [a.lower() for a in sys.argv[1:]]
SCREEN = any("screen" in a or u"螢幕" in a for a in _ARGS)
NOSEED = any("noseed" in a for a in _ARGS)
TAGL = u"螢幕版" if SCREEN else u"影印版"
SFX = "_screen" if SCREEN else ""
STEM = u"佛陀的護欄_重構版_" + TAGL

# 冊身今為《重構版》（20 章・5 篇＋終卷）；產器 `_book/build.py` 已退為歷史，其輸出留檔對校
SRC = os.path.join(ROOT, u"佛陀的護欄_重構版.md")
if not os.path.isfile(SRC):
    raise SystemExit(u"找不到冊身（先跑 python -X utf8 _book/build.py）")

MD = os.path.join(HERE, u"book_列印版%s.md" % SFX)
HTML = os.path.join(HERE, u"book_列印版%s.html" % SFX)
FINAL = os.path.join(HERE, u"final_book%s.html" % SFX)
PDF = os.path.join(HERE, u"book%s.pdf" % SFX)
PDF_OUT = os.path.join(HERE, STEM + u".pdf")
CACHE = os.path.join(HERE, u"_toccache_book%s.json" % SFX)

BH.SRC, BH.MD, BH.HTML, BH.FINAL, BH.PDF, BH.PDF_OUT = SRC, MD, HTML, FINAL, PDF, PDF_OUT
BH.STEM, BH.TAGL, BH.SFX, BH.SCREEN, BH.SLIM = STEM, TAGL, SFX, SCREEN, False
BH.LAYOUT = u"screen" if SCREEN else u"print"
BH.FENCE_BLOCKS = []
b38.MD, b38.HTML, b38.FINAL, b38.PDF = MD, HTML, FINAL, PDF
b38.SUFFIX = u"_book"
BH.PART = re.compile(u"【(?:第[一二三四五六七八九十]+[部篇]：[^】]*|卷末・工具與附錄[^】]*|終卷：[^】]*)】"
                     u"|^# 終卷|^# 佛陀的護欄")
TOC_ANCHOR_RE = re.compile(u"^# 第一章　", re.M)

BOOK_TITLE = u"佛陀的護欄"
EDITION = u"重構定本・" + TAGL
MD_TOC_HEAD = u"## 【本書總目錄】"

TOOL = [(u"`_book/build.py`", u"本冊產製法則"), (u"`_book/check.py`", u"校刊驗尺"),
        (u"_book/build.py", u"本冊產製法則"), (u"_book/check.py", u"校刊驗尺"),
        (u"relink", u"指針重算"), (u"build.py", u"產製法則"), (u"check.py", u"驗尺")]
RESIDUE = re.compile(u"_book/|relink|build\\.py|check\\.py|POLISH|SHA|pandoc")

# 目錄所收：篇（1）・章（2）・節（3）；附錄與終卷／卷末亦列
RE_SEC1 = re.compile(u"^# (【.+】)$")                     # 篇・終卷・卷末（皆帶【】之 H1）
RE_CHAP = re.compile(u"^# (第[一二三四五六七八九十]+章　.+)$")
RE_SEC = re.compile(u"^## (第[一二三四五六七八九十]+節　.+)$")
RE_APX = re.compile(u"^## (附錄[一二三四五六七八九十][　 ].+)$")


def de_adorn(lines):
    out, n = [], 0
    for i, l in enumerate(lines):
        if l.strip() == u"---" and out and out[-1].startswith(u"#"):
            out.append(u"")
            n += 1
        out.append(l)
    print(u"標題與『---』間補空行：%d 處（防 pandoc 吞區）" % n)
    return out


def drop_md_toc(lines):
    """印面之目錄由管線生成（帶頁碼），故剷冊身那份無頁碼之【本書總目錄】整段。"""
    i = next((k for k, l in enumerate(lines) if l.startswith(MD_TOC_HEAD)), None)
    if i is None:
        raise SystemExit(u"卷首無『%s』——產器改了形制，剷目之須隨改" % MD_TOC_HEAD)
    j = i + 1
    while j < len(lines) and not lines[j].startswith(u"# "):
        j += 1
    print(u"剷除冊身無頁碼目錄：%d 行（印面改由收斂法生成帶頁碼之目）" % (j - i))
    return lines[:i] + lines[j:]


def toc_entries(lines):
    """由印面實題生成目錄條目 [(lvl, 顯示標題, key)]。
    顯示標題一律用冊上原文（不添『（之N）』——掃描器以標題前 8 字為鑰，添 suffix 即永不得頁碼）；
    同名者以 key 之序分辨，掃描自上次命中之次頁續找，故各得其頁。"""
    cnt, out = {}, []
    for l in lines:
        lvl, title = 0, u""
        for rx, lv in ((RE_SEC1, 1), (RE_CHAP, 2), (RE_SEC, 3), (RE_APX, 2)):
            m = rx.match(l)
            if m:
                title, lvl = m.group(1).strip(), lv
                break
        if not lvl:
            continue
        base = b38.strip_md(title).replace("|", u"｜")
        n = cnt.get((lvl, base), 0) + 1
        cnt[(lvl, base)] = n
        out.append((lvl, base, (lvl, base, n)))
    return out


def toc_html(entries, pages):
    """本冊之目錄：部為附題，章／節／附錄／終卷為點線行（同名標題各列一行，不消歧、不合併）。"""
    rows = ['<div class="toc-lead">', "<h2>目　　錄</h2>"]
    for lvl, disp, key in entries:
        if disp == u"目錄" or b38.skip_in_toc(lvl, disp):
            continue
        if lvl == 1:
            esc = disp.replace("&", "&amp;").replace("<", "&lt;")
            rows.append('<p style="break-after:avoid;margin:9pt 0 2pt;font-weight:700;'
                        'font-size:11.5pt">%s</p>' % esc)
            continue
        rows.append(b38.toc_line(lvl, disp, pages.get(key)))
    rows.append("</div>")
    return rows


def write_md():
    raw = io.open(SRC, encoding="utf-8-sig").read()
    lines = raw.replace("\r\n", "\n").split("\n")
    n = 0
    for i, l in enumerate(lines):
        new = l
        for a, b in TOOL:
            if a in new:
                new = new.replace(a, b)
        if new != l:
            lines[i] = new
            n += 1
    if not any(TOC_ANCHOR_RE.match(l) for l in lines):
        raise SystemExit(u"中介檔定位失敗：源檔無『# 第一章　』")
    lines = drop_md_toc(lines)
    i = next(k for k, l in enumerate(lines) if TOC_ANCHOR_RE.match(l))
    lines.insert(i, u"<!--TOC-PLACEHOLDER-->\n")
    if lines[i - 1].strip() != u"":
        lines.insert(i, u"")
    lines = de_adorn(lines)
    lines = b38.ensure_blank(lines)
    txt = u"\n".join(lines)
    io.open(MD, "w", encoding="utf-8", newline="\n").write(txt)
    left = RESIDUE.findall(txt)
    print(u"源：%s｜工程字面隨改 %d 行｜中介 md 已出｜殘留工具名：%d 處"
          % (os.path.basename(SRC), n, len(left)))
    if left:
        raise SystemExit(u"印面清創未淨：%s" % u"、".join(sorted(set(left))))
    return lines


COVER = u"""<section id="print-cover" class="cov">
  <p class="cov-eyebrow">大正藏第一四二八號·四分律</p>
  <div class="cov-main">
    <div class="cov-sutra">佛陀的護欄</div>
    <div class="cov-title">四分律行為心理學與現代僧伽治理</div>
    <div class="cov-rule"></div>
    <p class="cov-sub">__SUB__</p>
    <p class="cov-motto">小戒不是鎖鏈　小戒是安全氣囊<br />
       律不與人性賭博　只預先修築護欄</p>
    <p class="cov-cap">__APPS__<br />原典：漢譯《四分律》六十卷·大正藏 No.1429《戒本》</p>
  </div>
  <div class="cov-foot">
    <p class="cov-edition">__EDITION__</p>
    <p class="cov-meta">依《四分律》而立·以遮衛性為宗·以僧伽治理為用</p>
  </div>
</section>
"""


def cover_counts(src_txt):
    n_chap = len(re.findall(u"^# 第[一二三四五六七八九十]+章　", src_txt, re.M))
    n_sec = len(re.findall(u"^## 第[一二三四五六七八九十]+節", src_txt, re.M))
    n_case = len(re.findall(u"^### 案例", src_txt, re.M))
    n_part = len(re.findall(u"^# 【第[一二三四五六七八九十]+[部篇]：", src_txt, re.M))
    n_apx = len(re.findall(u"^## 附錄[一二三四五六七八九十]", src_txt, re.M))
    return u"%d 篇・%d 章・%d 節・%d 案・附錄 %d 件" % (n_part, n_chap, n_sec, n_case, n_apx)


def render_once(entries, pages, pre_sizes):
    """一趟：出 HTML（含目錄）→ 部題 Banner → 寬字／缺字回格 → 續用已量之字級 → 列印 → 印面回量。
       回『本趟仍須縮者』之有無；字級記於 pre_sizes，暖起點之下每趟只量一次，免層層疊印。"""
    b38.render_html(toc_html(entries, pages))
    BH.drop_hr_before_h1()
    BH.mark_part_pages()
    BH.pre_wide_span()
    if pre_sizes:
        BH.apply_pre_sizes(pre_sizes, BH.FENCE_BLOCKS)
    b38.render_pdf()
    need = BH.pre_overflows(PDF, BH.FENCE_BLOCKS)
    changed = {k: v for k, v in need.items() if pre_sizes.get(k) != v}
    if changed:
        pre_sizes.update(changed)
        BH.apply_pre_sizes(pre_sizes, BH.FENCE_BLOCKS)
        b38.render_pdf()
    return bool(changed)


def _pre_rows(doc, at):
    """該頁之印面行 [(y0, y1, 去空白之文字)]——供換行與跨頁之判。"""
    rows = []
    for bl in doc[at].get_text("rawdict")["blocks"]:
        for ln in bl.get("lines", []):
            s = "".join("".join(c["c"] for c in sp["chars"]) for sp in ln.get("spans", []))
            s = "".join(s.split())
            if s:
                rows.append((ln["bbox"][1], ln["bbox"][3], s))
    return rows


def verify_print(entries, pages, blocks):
    """印面之驗（量產物，不讀自報）：目錄逐條有碼・圍欄不換行・短圖不跨頁。
    定位口徑：先取『首尾俱在』之頁——首行文字在他頁（引文・目錄・同形框線）常再現，
    單取首行所見之頁必錯；無同頁者方看『首在頁末而尾在次頁之頂』，那才是真跨頁。"""
    import pymupdf as pm

    d = pm.open(PDF_OUT)
    np_ = d.page_count

    def nn(s):
        return "".join(s.split())

    txt = [nn(d[i].get_text()) for i in range(np_)]
    bad = []
    nocode = [disp for _l, disp, key in entries if not pages.get(key)]
    if nocode:
        bad.append(u"目錄無頁碼 %d 條（例：%s）" % (len(nocode), u"／".join(x[:14] for x in nocode[:3])))
    wrapped, split, gone = [], [], []
    for k, b in enumerate(blocks, 1):
        if not b:
            continue
        head, tail = nn(b[0])[:12], nn(b[-1])[:12]
        ph = set(i for i, t in enumerate(txt) if head in t)
        pt = set(i for i, t in enumerate(txt) if tail in t)
        both = sorted(ph & pt)
        if not both:                              # 首尾不同頁：長圖（>40 行）容其延伸至次頁，短圖則為病
            hp, tp = sorted(ph), sorted(pt)
            if hp and tp and 0 < tp[0] - hp[0] <= 3:
                if len(b) <= 40:
                    split.append((k, hp[0] + 1, len(b)))
                continue
            gone.append(k)
            continue
        at = both[0]
        rows = _pre_rows(d, at)
        ys = [r[0] for r in rows if r[2].startswith(head)]
        ye = [r[0] for r in rows if r[2].startswith(tail)]
        if not ys or not ye:
            gone.append(k)
            continue
        seg = [r for r in rows if ys[0] - 1 <= r[0] <= max(ye) + 2]
        if len(seg) > len(b) + 1:
            wrapped.append((k, len(b), len(seg)))
    d.close()
    if wrapped:
        bad.append(u"圍欄被換行 %d 段（例：%s）" % (len(wrapped), wrapped[:3]))
    if split:
        bad.append(u"圍欄跨頁 %d 段（例：%s）" % (len(split), split[:3]))
    if gone:
        bad.append(u"印面尋不得之圍欄段 %d（例：%s）" % (len(gone), gone[:5]))
    if bad:
        for x in bad:
            print(u"  ✗ 印面之病：" + x)
        raise SystemExit(u"印面有病的 %d 項未清，退冊待修" % len(bad))
    print(u"印面之驗：目錄 %d 條俱有頁碼・圍欄 %d 段不換行不断頁・%d 頁"
          % (len(entries), len(blocks), np_))


def main():
    t0 = time.perf_counter()
    lines = write_md()
    src_txt = u"\n".join(lines)
    b38.COVER, b38.EDITION = COVER, EDITION
    b38.APPS = cover_counts(src_txt)
    b38.COVER = COVER.replace(u"__SUB__", u"%s——判例與心所並陳" % b38.APPS)
    print(u"封面計數（自冊身取，不手打）：%s" % b38.APPS)
    hs = BH.headings(lines)
    BH.FENCE_BLOCKS = BH.fence_blocks(lines)
    entries = toc_entries(lines)
    print(u"目錄條目：%d 條（部・章・節・附錄・終卷）" % len(entries))

    pages, prev_n, prev = {}, -1, None
    pre_sizes = {}
    if not NOSEED and os.path.exists(CACHE):
        try:
            dd = json.load(io.open(CACHE, encoding="utf-8"))
            pages = {b38._ukey(k): v for k, v in dd["pages"].items()}
            prev_n, prev = dd["npage"], dict(pages)
            pre_sizes = {int(k): v for k, v in dd.get("pre", {}).items()}
            print(u"  暖起點：頁碼 %d 條／%d 頁・圍欄字級 %d 段（加 noseed 廢之）"
                  % (len(pages), prev_n, len(pre_sizes)))
        except Exception as e:
            print(u"  暖起點不可用，仍冷起點：", e)

    for it in range(1, 9):
        _t = time.perf_counter()
        shrunk = render_once(entries, pages, pre_sizes)
        t_r = time.perf_counter() - _t
        raw, npage = b38.scan_pages(entries)
        pages = raw
        stable = (npage == prev_n) and (pages == prev) and not shrunk
        print(u"  第 %d 趟：%d 頁・目錄回填 %d/%d 條・圍欄縮字 %d 段%s（排版＋列印＋掃描 %.1fs）%s"
              % (it, npage, sum(1 for v in pages.values() if v), len(entries), len(pre_sizes),
                 u"・本趟再縮" if shrunk else u"", t_r, u"　← 收斂" if stable else u""))
        if stable:
            break
        prev_n, prev = npage, pages
    else:
        raise SystemExit(u"目錄八趟仍未收斂——頁碼不可信，退冊待查")

    json.dump({"npage": npage, "pages": {b38._ckey(k): v for k, v in pages.items()},
               "pre": {str(k): v for k, v in pre_sizes.items()}},
              io.open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)

    npage = BH.deliver()
    import pymupdf as pm
    d = pm.open(PDF)
    outline, ml = BH.build_outline(d, hs)
    d.close()
    META = {
        "title": u"%s｜四分律行為心理學與現代僧伽治理｜合編本（%s）" % (BOOK_TITLE, TAGL),
        "author": u"編者",
        "subject": u"漢譯《四分律》六十卷之行為心理學與僧伽治理·七部二十八章",
        "keywords": u"四分律；毘奈耶；以遮衛性；八大正理；波羅夷；僧殘；捨墮；單提；眾學法；"
                    u"七滅諍；二十犍度；大正藏 No.1428",
        "creator": u"build_book 管線（沿用 build38 之法源：pandoc → 無頭 Chromium 列印）",
        "producer": u"build_book",
    }
    if outline:
        b38.stamp_pdf(PDF, outline, META)
        b38.stamp_pdf(PDF_OUT, outline, META)
    print(u"內嵌大綱：%d 條（定位失敗 %d）" % (len(outline), len(ml)))
    if ml:
        print(u"  未入大綱：%s" % u"、".join(ml[:8]))
    verify_print(entries, pages, BH.FENCE_BLOCKS)
    print(u"交付：%s｜%d 頁｜%d KB・目錄 %d 條・用時 %d 秒"
          % (os.path.basename(PDF_OUT), npage, os.path.getsize(PDF_OUT) // 1024,
             len(entries), time.perf_counter() - t0))


if __name__ == "__main__":
    main()
