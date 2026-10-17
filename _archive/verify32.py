# -*- coding: utf-8 -*-
"""ver32 列印版交付驗證：目錄頁碼逐條核對、附錄齊備、頁數。"""
import os, re, sys
import pymupdf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROMAN = re.compile(r"^[ivxlcdm]+$")


def norm(s):
    return re.sub(r"[\s\u3000　]+", "", s)


def band(page):
    r = pymupdf.Rect(0, page.rect.height - 60, page.rect.width, page.rect.height)
    return page.get_text(clip=r).strip()


def toc_entries(final):
    html = open(final, encoding="utf-8").read()
    m = re.search(r'(?s)<div class="toc-lead">(.*?)</div>', html)
    if not m:
        return []
    rows = []
    for r in re.finditer(r'(?s)<p class="toc-line toc-l(\d)">\s*<span class="t">(.*?)</span>'
                         r'<span class="d">.*?</span><span class="pg">(\d*)</span></p>', m.group(1)):
        rows.append((int(r.group(1)), re.sub(r"<[^>]+>", "", r.group(2)).strip(), r.group(3)))
    return rows


def check(pdf, final, label):
    doc = pymupdf.open(pdf)
    n = doc.page_count
    pages = [norm(doc[i].get_text()) for i in range(n)]
    heads = []
    for i in range(n):
        ln = [x for x in doc[i].get_text().split("\n") if x.strip()]
        heads.append(norm("".join(ln[:2]) + "".join(ln[-3:])))
    tocp = [i for i in range(n) if ROMAN.match(band(doc[i]))]
    tocset = set(tocp)
    body = next((i for i in range(n) if "正文起點" in pages[i]), (tocp[-1] + 1) if tocp else 0)
    npages = n - body
    out = ["", "=" * 60, "[%s] %s" % (label, os.path.basename(pdf)),
           "  總頁數 %d = 封面 1 + 目錄 %d + 正文 %d" % (n, len(tocp), npages),
           "  目錄 PDF p%s-p%s；正文自 PDF p%d 起算為正文第 1 頁" %
           (tocp[0] + 1 if tocp else "?", tocp[-1] + 1 if tocp else "?", body + 1)]
    rows = toc_entries(final)
    ok = wrong = miss = 0
    detail = []
    for lvl, title, pg in rows:
        key = norm(title)
        if not key or not pg:
            continue
        want = body + int(pg) - 1
        cand = [want] + [j for d in (1, -1, 2, -2) for j in (want + d,) if 0 <= want + d < n]
        hit = next((j for j in cand if j not in tocset and key[:16] in heads[j]), None)
        if hit is None:
            hit = next((j for j in cand if j not in tocset and key[:16] in pages[j]), None)
        if hit is None:
            miss += 1; detail.append("    x 未定位：%s（載 p%s）" % (title[:30], pg))
        elif hit != want:
            wrong += 1; detail.append("    ! 偏移 %+d：%s 載 p%s" % (hit - want, title[:28], pg))
        else:
            ok += 1
    tot = ok + wrong + miss
    out.append("  目錄行 %d；可核對 %d；符合所載頁 %d（%.0f%%）；偏移 %d；未定位 %d" %
               (len(rows), tot, ok, 100.0 * ok / max(1, tot), wrong, miss))
    out += detail[:10]
    nopg = sum(1 for _, _, p in rows if not p)
    out.append("  目錄中無頁碼者：%d 條（多為卷首序文與極短小節）" % nopg)
    apps = []
    for a in "ABCDEFHIJK":
        k = norm("附錄" + a)
        apps.append(a if any(pages[i].startswith(k) for i in range(body, n) if i not in tocset)
                   else a + "(未見章首)")
    out.append("  附錄：%s" % " ".join(apps))
    doc.close()
    return out


def main():
    res = []
    for pdf, final, label in [
        ("ver32四分律_起心動念心智分析框架_第二十七版_列印版.pdf", "final32.html", "完整版"),
        ("ver32四分律_起心動念心智分析框架_第二十七版_列印版_精簡本.pdf", "final32_精簡本.html", "精簡本"),
    ]:
        p, f = os.path.join(HERE, pdf), os.path.join(HERE, final)
        if os.path.exists(p) and os.path.exists(f):
            res += check(p, f, label)
        else:
            res.append("  （略過 %s：檔案不存在）" % label)
    txt = "\n".join(res)
    open(os.path.join(HERE, "_verify32.txt"), "w", encoding="utf-8").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
