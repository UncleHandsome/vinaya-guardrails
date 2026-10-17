# -*- coding: utf-8 -*-
"""ver38 列印版交付驗證：目錄頁碼逐條對「頁腳實印」覆核、附錄齊備、頁數。

口徑（第五十輪定案）：目錄所載頁碼 ＝ PDF 物理頁 ＝ 頁腳所印之號。
舊版此處以「正文相對頁碼」反推（want = body + pg − 1），與 build38 的同一假設互相印證，
故全書目錄恆少印一整個卷首之數而驗收仍報「偏移 0」——屬假綠，今改爲實測頁腳印字。

第七十五輪再補兩刀：
  一、目錄條目向以中介 HTML 為源；拿去對另路排版之 PDF，兩套排版各自分頁，
      必然全盤對上不了（曾因此誤報『相符 0／未定位 78』，實為驗收器之責而非冊之病）。
      今**以冊內自印之目錄為準**，中介檔降為交叉比對。
  二、附錄章首舊以整頁文字 `startswith` 判——主線每頁文字流先出頁腳數字，故恆不中；
      今逐頁取頁首數行比對，兩路皆適用。
用法：python _print/verify38.py [pdf|html|auto] [另件PDF ...]（預設 auto）
"""
import os
import re
import sys

import pymupdf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
MODE = (sys.argv[1] if len(sys.argv) > 1 else "auto").lower()
ROMAN = re.compile(r"^[ivxlcdm]+$")
DOTS = " 　.·‧…．⁠​‌‍ "
ENTRY = re.compile(r"^(.*?)[" + DOTS + r"]{2,}(\d{1,4}|[ivxlcdm]{1,7})$")


ZW = "\u2060\u200b\u200c\u200d\u202f"


_ROMAN_MAP = (("m", 1000), ("cm", 900), ("d", 500), ("cd", 400), ("c", 100), ("xc", 90),
            ("l", 50), ("xl", 40), ("x", 10), ("ix", 9), ("v", 5), ("iv", 4), ("i", 1))


def to_int(pg):
    """目錄所載頁碼 → 整數：阿拉伯直取，羅馬則累加（卷首與目錄頁印羅馬）。"""
    pg = pg.strip()
    if pg.isdigit():
        return int(pg)
    n, i = 0, 0
    for sym, v in _ROMAN_MAP:
        while pg[i:i + len(sym)] == sym:
            n += v
            i += len(sym)
    return n if i == len(pg) else None


def norm(s):
    return re.sub(r"[\s　" + ZW + "]+", "", s)


def page_lines(page):
    return [x.strip() for x in page.get_text().split("\n") if x.strip()]


_NUM = re.compile(r"^(\d{1,4}|[ivxlcdm]{1,7})$")


def band_candidates(lines):
    """頁腳候選：頁首兩行與頁尾兩行中的純號碼（瀏覽器列印之文字序不穩，兩端皆須看）。

    頁尾兩行恆看（短頁亦然）：舊作 4 行以下短頁只看頁首，致目錄尾頁（僅 4 行、
    頁腳在末行）整頁漏判為非羅馬頁，其上條目全數失檢而不自知。
    """
    edge = lines[:2] + lines[-2:]
    out, seen = [], set()
    for ln in edge:
        m = _NUM.match(ln.strip())
        if m and m.group(1) not in seen:
            seen.add(m.group(1))
            out.append(m.group(1))
    return out


def _roman(n):
    vals = [(1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"), (90, "xc"),
            (50, "l"), (40, "xl"), (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]
    s = ""
    for v, sym in vals:
        while n >= v:
            s += sym
            n -= v
    return s


def resolve_bands(pages_lines):
    """逐頁定其頁腳印字：以『等於物理頁號』之候選為準（本冊口徑：頁腳＝全冊絕對頁）。

    頁內容常另有純數字行（表格計數、圖中序號），單取末行會誤讀，故只認與物理頁相符者；
    前置頁（卷首與目錄）印羅馬，故阿拉伯與羅馬兩式皆受。若兩式俱無則取末位候補，
    由上層判為頁腳不符與否。
    """
    labels = []
    for i, lines in enumerate(pages_lines):
        cands = band_candidates(lines)
        want, wm = str(i + 1), _roman(i + 1)
        if want in cands:
            labels.append(want)
        elif wm in cands:
            labels.append(wm)
        else:
            labels.append(cands[-1] if cands else "")
    return labels


def toc_entries_html(final):
    """weasyprint 中介檔之點線目錄（僅作交叉比對與 PDF 解析不確時之備援）。"""
    if not final or not os.path.exists(final):
        return []
    html = open(final, encoding="utf-8").read()
    m = re.search(r'(?s)<div class="toc-lead">(.*?)</div>', html)
    if not m:
        return []
    rows = []
    for r in re.finditer(r'(?s)<p class="toc-line toc-l(\d)">\s*<span class="t"[^>]*>(.*?)</span>'
                         r'<span class="d">.*?</span><span class="pg">(\d*)</span></p>', m.group(1)):
        rows.append((int(r.group(1)), re.sub(r"<[^>]+>", "", r.group(2)).strip(), r.group(3)))
    return rows


_ZW_STRIP = re.compile(r"[⁠​‌‍﻿ ]")
_DOTS_TAIL = re.compile(r"[ 　.·‧…．⁠​‌‍ ]{2,}\s*$")
_TOC_TITLE_SKIP = re.compile(r"^\s*目\s*錄\s*$")  # 目錄大標：不得暫存為折行前半，否則短標題首條被黏合吞沒


def toc_entries_pdf(lines, tocset):
    """冊內自印之目錄（兩路通用）：取目錄頁各行，解『標題＋點線＋頁碼』式。

    PDF 文字流無層級資訊，故一律記為層 0；條目內之空白（如『「 歇 」』）原樣保留。
    兩則容錯（皆有實例）：① 目錄數字前偶帶零寬黏合字（\u2060 等排版膠），
    先剝除再解；② 大字級目錄行被折為兩行（標題行無點線頁碼、數字行標題為空），
    以「上一行非點線尾＋本行初見頁碼」合併後再解，否則該條永遠失檢。
    """
    rows = []
    for i in sorted(tocset):
        prev = ""
        for ln in lines[i]:
            if ROMAN.match(ln) or _TOC_TITLE_SKIP.match(ln) or set(ln) <= set(DOTS):
                continue
            m = ENTRY.match(_ZW_STRIP.sub("", ln))
            title = m.group(1).strip() if m else ""
            if m and norm(title) and (not prev or len(norm(title)) >= 16):
                rows.append((0, title, m.group(2)))
                prev = ""
            elif m and prev:
                # 折行後半（短標題殘段或純數字行）：與前半合併後重解；
                # 前半本無點線（如台帳式「標題行＋數字行」），須手補點線膠合，
                # 否則「標題＋數字」直連永遠解不出頁碼。
                m2 = ENTRY.match(_ZW_STRIP.sub("", prev + title) + ".." + (m.group(2) or ""))
                if m2 and norm(m2.group(1)):
                    rows.append((0, m2.group(1).strip(), m2.group(2) or m.group(2)))
                prev = ""
            elif not m and not _DOTS_TAIL.search(_ZW_STRIP.sub("", ln)):
                prev = ln  # 無頁碼非點線尾：暫存為折行前半
            else:
                prev = ""
    return rows


def appendix_heads(lines, n, tocset):
    """附錄章首：逐頁取頁首四行比對『附錄X』起頭者（主線頁首先出頁腳號，故不可用 startswith）。"""
    found = {}
    for i in range(n):
        if i in tocset:
            continue
        for ln in lines[i][:4]:
            m = re.match(u"^附錄([A-Z])", ln)
            if m and m.group(1) not in found:
                found[m.group(1)] = i + 1
                break
    return found


def check(pdf, final, label):
    doc = pymupdf.open(pdf)
    n = doc.page_count
    lines = [page_lines(doc[i]) for i in range(n)]
    doc.close()
    pages = [norm("".join(l)) for l in lines]
    heads = [norm("".join(l[:2]) + "".join(l[-3:])) for l in lines]
    labels = resolve_bands(lines)   # 頁腳印字（前後候補之擇定）
    tocset = {i for i in range(n) if ROMAN.match(labels[i])}

    r_pdf = toc_entries_pdf(lines, tocset)
    r_html = toc_entries_html(final)
    src = u"冊內自印"
    rows = r_pdf
    if MODE == "html" and r_html:
        rows, src = r_html, u"中介檔"
    elif MODE in ("auto", "pdf") and r_html and len(r_pdf) < 0.8 * len(r_html):
        rows, src = r_html, u"中介檔（冊內目錄解析條目偏少，退回備援）"

    ok = foot_bad = wrong = miss = 0
    detail = []
    for _lvl, title, pg in rows:
        key = norm(title)
        if not key or not pg:
            continue
        num = to_int(pg)
        if num is None:
            miss += 1
            detail.append("    x 頁碼不可解：%s 載 p%s" % (title[:30], pg))
            continue
        i = num - 1                                  # 目錄號即物理頁／頁腳號
        if not 0 <= i < n:
            miss += 1
            detail.append("    x 頁碼越界：%s 載 p%s" % (title[:30], pg))
            continue
        if labels[i] != pg:
            foot_bad += 1
            detail.append("    ! 頁腳不符：%s 目錄載 %s，該頁頁腳實印 %s"
                          % (title[:26], pg, labels[i] or "(無)"))
        if key[:16] in heads[i] or key[:16] in pages[i]:
            ok += 1
            continue
        act = next((j for j in range(n) if j not in tocset and key[:16] in heads[j]), None)
        if act is None:
            miss += 1
            detail.append("    x 未定位：%s（載 p%s）" % (title[:30], pg))
        else:
            wrong += 1
            detail.append("    ! 偏移 %+d：%s 載 p%s，實在 p%d" % (act - i, title[:28], pg, act + 1))
    tot = ok + wrong + miss
    nopg = sum(1 for _, _, p in rows if not p)
    out = ["", "=" * 60, "[%s] %s" % (label, os.path.basename(pdf)),
           "  總頁數 %d｜目錄頁（羅馬頁腳）%d 頁｜目錄條目 %d（源：%s）" % (n, len(tocset), len(rows), src),
           "  可核對 %d；目錄號與該頁標題相符 %d（%.0f%%）；頁腳印字不符 %d；偏移 %d；未定位 %d"
           % (tot, ok, 100.0 * ok / max(1, tot), foot_bad, wrong, miss),
           "  目錄中無頁碼者：%d 條（卷首序文與極短小節，依凡例不入目錄頁碼之列）" % nopg]
    if MODE == "auto" and r_html and r_pdf:
        a = {norm(t) for _l, t, p in r_pdf if p}
        b = {norm(t) for _l, t, p in r_html if p}
        out.append("  交叉比對：冊內 %d 條｜中介檔 %d 條｜各自獨有 %d／%d（兩路各自分頁，集合有出入屬正常）"
                   % (len(a), len(b), len(a - b), len(b - a)))
    out += detail[:12]
    found = appendix_heads(lines, n, tocset)
    # 各式應有之附錄（C 修訂誌與 L／M 同屬編纂底冊，不入印本；精簡本唯隨 A、B）
    # 判冊別須依檔名——label 於他處可能重複，不足據。
    want = "AB" if "精簡本" in os.path.basename(pdf) else "ABDEFHIJ"
    apps = []
    for a in "ABCDEFHIJK":
        if a in found:
            apps.append(a + ("!" if a not in want else ""))
        elif a in want:
            apps.append(a + "(缺！)")
        else:
            apps.append(a + "（不隨冊）")
    out.append("  附錄：%s｜應有 %s" % (" ".join(apps), want))
    bad = list(detail) + [u"  附錄 %s" % a for a in apps if "!" in a]

    # 內嵌大綱與書訊（第 131 輪）：無頭瀏覽器列印不產大綱，title 又默認洩用中介檔名，
    # 故管線另有 stamp_pdf／docx_meta 兩器——此處驗其確已生效，且抽驗書籤所指之頁真有該標題。
    d2 = pymupdf.open(pdf)
    bm = d2.get_toc()
    meta = d2.metadata or {}
    d2.close()
    title = (meta.get("title") or u"").strip()
    out.append(u"  內嵌大綱 %d 條｜書訊 title『%s』｜author『%s』"
               % (len(bm), title[:44] or u"（空）", (meta.get("author") or u"（空）")[:12]))
    if not bm:
        bad.append(u"    x 內嵌大綱 0 條（未經 stamp_pdf，讀者無導航可用）")
    if u"三十八版" not in title:
        bad.append(u"    x 書訊 title 未含版次：『%s』" % (title[:40] or u"（空）"))
    if bm:
        probe = bm[:1] + bm[len(bm) // 2:len(bm) // 2 + 1] + bm[-1:]
        for _lv, ti, pg in probe:
            key = norm(ti)[:12]
            hit = bool(key) and 1 <= pg <= n and key in pages[pg - 1]
            out.append(u"    大綱抽驗：%s → p%d %s" % (ti[:22], pg, u"有標題" if hit else u"未見"))
            if not hit:
                bad.append(u"    ! 大綱所指頁無該標題：%s → p%d" % (ti[:22], pg))
    return out, bad


def main():
    pairs = [("ver38四分律_起心動念心智分析框架_第三十八版_列印版.pdf", "final38.html", "完整版·影印"),
             ("ver38四分律_起心動念心智分析框架_第三十八版_列印版_精簡本.pdf", "final38_精簡本.html", "精簡本·影印"),
             ("ver38四分律_起心動念心智分析框架_第三十八版_螢幕版.pdf", "final38_screen.html", "完整版·螢幕"),
             ("ver38四分律_起心動念心智分析框架_第三十八版_螢幕版_精簡本.pdf", "final38_精簡本_screen.html", "精簡本·螢幕")]
    extra = [a for a in sys.argv[2:] if a.lower().endswith(".pdf")]
    res = []
    allbad = []
    for pdf, final, label in pairs:
        p, f = os.path.join(HERE, pdf), os.path.join(HERE, final)
        if os.path.exists(p):
            o, bd = check(p, f if MODE in ("auto", "html") else None, label)
            res += o
            allbad += ["[%s]%s" % (label, x.strip()) for x in bd]
        else:
            res.append("  （略過 %s：檔案不存在）" % label)
            allbad.append(u"  缺件：%s" % label)
    for e in extra:
        q = e if os.path.isabs(e) else os.path.join(HERE, e)
        if os.path.exists(q):
            o, bd = check(q, None, "另件")
            res += o
            allbad += ["[另件]%s" % x.strip() for x in bd]
        else:
            res.append("  （略過另件：%s 不存在）" % e)
    res.append(u"\n" + (u"不合格 0 處——全綠" if not allbad else
                        u"不合格 %d 處：\n%s" % (len(allbad), u"\n".join(u"  · " + x for x in allbad))))
    txt = "\n".join(res)
    open(os.path.join(HERE, "_verify38.txt"), "w", encoding="utf-8").write(txt)
    print(txt)
    if allbad:
        sys.exit(1)


if __name__ == "__main__":
    main()
