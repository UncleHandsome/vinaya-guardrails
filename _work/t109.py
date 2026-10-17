# -*- coding: utf-8 -*-
"""最小實驗：Chromium 無頭列印是否理會 `body > h1 { break-before: page / right }`。"""
import io, os, re, subprocess, sys, tempfile, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_print"))
import build38 as B

css = {
    "none": "",
    "page": "body > h1 { break-before: page; }",
    "right": "body > h1 { break-before: right; }",
    "plainh1": "h1 { break-before: page; }",
    "plusavoid": "h1 { break-before: page; } h1 + * { break-before: avoid; }",
}
body = "".join(u"<h1>第%s章</h1><p>%s</p>" % (c, "文" * 900) for c in "甲乙丙丁")
prof = tempfile.mkdtemp(prefix="t109-")
for tag, rule in css.items():
    html = ("<!DOCTYPE html><html><head><meta charset='utf-8'><style>"
            "@page{size:A4;margin:12mm}body{font-family:'Microsoft JhengHei';font-size:12pt}"
            + rule + "</style></head><body>" + body + "</body></html>")
    h = os.path.join(prof, "t_%s.html" % tag)
    p = os.path.join(prof, "t_%s.pdf" % tag)
    io.open(h, "w", encoding="utf-8").write(html)
    subprocess.run([B.find_browser(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--user-data-dir=" + os.path.join(prof, "ud-" + tag),
                    "--print-to-pdf=" + p, "file:///" + h.replace("\\", "/")],
                   capture_output=True)
    for _ in range(60):
        if os.path.exists(p) and os.path.getsize(p) > 0:
            break
        time.sleep(0.1)
    import pymupdf as fitz
    d = fitz.open(p)
    firsts = [re.sub(r"\s", "", d[i].get_text())[:4] for i in range(d.page_count)]
    at_top = sum(1 for x in firsts if x.startswith(u"第"))
    print("  %-9s 頁 %d｜章題居頁首者 %d 处｜%s" % (tag, d.page_count, at_top, firsts[:6]))
    d.close()
