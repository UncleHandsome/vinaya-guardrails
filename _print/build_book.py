# -*- coding: utf-8 -*-
"""《佛陀的護欄・四分律行為心理學與現代僧伽治理》合編本・列印管線。

法源不另起：pandoc 旗標、print38.css、字級覆寫、ensure_blank、render_html／render_pdf／
stamp_pdf、圍欄回量、部題 Banner、drop_hr_before_h1、pre_wide_span、refit_pre、deliver 諸件
皆取 build_hulan／build38 之現成函式（第 173 輪『小樣不同旗標即不同書』之誡）。

本冊獨有者二：
① 封面計數自冊身取（部・章・節・案・附錄），不手打；
② 印面清創之殘留名單改依本冊之工具名（_book／relink…），有殘即退。
卷首之【本書總目錄】（章・節二級，由冊身實題自生）隨冊同印，與《佛陀的護欄》舊版之例同
（舊版印本之目錄亦由書自備，頁碼不留——留頁碼者為 build38 之六趟收斂，另候命再上）。

用法：python -X utf8 _print/build_book.py [print|screen]  > _print/log_build_book.txt 2>&1
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
import build_hulan as BH                                   # noqa: E402
import build38 as b38                                      # noqa: E402

_ARGS = [a.lower() for a in sys.argv[1:]]
SCREEN = any("screen" in a or u"螢幕" in a for a in _ARGS)
TAGL = u"螢幕版" if SCREEN else u"影印版"
SFX = "_screen" if SCREEN else ""
STEM = u"佛陀的護欄_四分律行為心理學與現代僧伽治理_" + TAGL

SRC = os.path.join(ROOT, u"佛陀的護欄_四分律行為心理學與現代僧伽治理.md")
if not os.path.isfile(SRC):
    raise SystemExit(u"找不到冊身（先跑 python -X utf8 _book/build.py）")

MD = os.path.join(HERE, u"book_列印版%s.md" % SFX)
HTML = os.path.join(HERE, u"book_列印版%s.html" % SFX)
FINAL = os.path.join(HERE, u"final_book%s.html" % SFX)
PDF = os.path.join(HERE, u"book%s.pdf" % SFX)
PDF_OUT = os.path.join(HERE, STEM + u".pdf")

BH.SRC, BH.MD, BH.HTML, BH.FINAL, BH.PDF, BH.PDF_OUT = SRC, MD, HTML, FINAL, PDF, PDF_OUT
BH.STEM, BH.TAGL, BH.SFX, BH.SCREEN, BH.SLIM = STEM, TAGL, SFX, SCREEN, False
BH.LAYOUT = u"screen" if SCREEN else u"print"
BH.FENCE_BLOCKS = []
b38.MD, b38.HTML, b38.FINAL, b38.PDF = MD, HTML, FINAL, PDF
b38.SUFFIX = u"_book"
BH.PART = re.compile(u"【(?:第[一二三四五六七]部：[^】]*|卷末・工具與附錄)】|^# 終卷|^# 佛陀的護欄")
TOC_ANCHOR_RE = re.compile(u"^# 第一章　", re.M)

BOOK_TITLE = u"佛陀的護欄"
EDITION = u"合編本・" + TAGL

TOOL = [(u"`_book/build.py`", u"本冊產製法則"), (u"`_book/check.py`", u"校刊驗尺"),
        (u"_book/build.py", u"本冊產製法則"), (u"_book/check.py", u"校刊驗尺"),
        (u"relink", u"指針重算"), (u"build.py", u"產製法則"), (u"check.py", u"驗尺")]
RESIDUE = re.compile(u"_book/|relink|build\\.py|check\\.py|POLISH|SHA|pandoc")


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
    """（备用）印本若改走帶頁碼之收斂目錄，則以茲剷除卷首之無頁碼目。"""
    i = next((k for k, l in enumerate(lines) if l.startswith(u"## 【本書總目錄】")), None)
    if i is None:
        return lines, 0
    j = i
    while j < len(lines) and not lines[j].startswith(u"# "):
        j += 1
    print(u"剷除卷首無頁碼目錄：%d 行（改由管線生成帶頁碼之目錄）" % (j - i))
    return lines[:i] + lines[j:], j - i


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


def main():
    t0 = time.perf_counter()
    lines = write_md()
    src_txt = u"\n".join(lines)
    n_chap = len(re.findall(u"^# 第[一二三四五六七八九十]+章　", src_txt, re.M))
    n_sec = len(re.findall(u"^## 第[一二三四五六七八九十]+節", src_txt, re.M))
    n_case = len(re.findall(u"^### 案例", src_txt, re.M))
    n_part = len(re.findall(u"^# 【第[一二三四五六七]部：", src_txt, re.M))
    n_apx = len(re.findall(u"^## 附錄[一二三四五]", src_txt, re.M))
    APPS = u"七部・%d 章・%d 節・%d 案・附錄 %d 篇" % (n_chap, n_sec, n_case, n_apx)
    COVER = u"""<section id="print-cover" class="cov">
  <p class="cov-eyebrow">大正藏第一四二八號·四分律</p>
  <div class="cov-main">
    <div class="cov-sutra">佛陀的護欄</div>
    <div class="cov-title">四分律行為心理學與現代僧伽治理</div>
    <div class="cov-rule"></div>
    <p class="cov-sub">兩書合編本——七部二十八章·判例與心所並陳</p>
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
    b38.COVER, b38.EDITION, b38.APPS = COVER, EDITION, APPS
    print(u"封面計數（自冊身取，不手打）：%s" % APPS)
    hs = BH.headings(lines)
    BH.FENCE_BLOCKS = BH.fence_blocks(lines)
    b38.render_html([])
    BH.drop_hr_before_h1()
    BH.mark_part_pages()
    BH.pre_wide_span()
    b38.render_pdf()
    BH.refit_pre()
    npage = BH.deliver()
    import pymupdf as pm
    d = pm.open(PDF)
    outline, miss = BH.build_outline(d, hs)
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
    print(u"內嵌大綱：%d 條（定位失敗 %d）" % (len(outline), len(miss)))
    if miss:
        print(u"  未入大綱：%s" % u"、".join(miss[:8]))
    print(u"交付：%s｜%d 頁｜%d KB｜用時 %d 秒"
          % (os.path.basename(PDF_OUT), npage, os.path.getsize(PDF_OUT) // 1024,
             time.perf_counter() - t0))


if __name__ == "__main__":
    main()
