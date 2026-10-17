# -*- coding: utf-8 -*-
"""在真實 final38.html 上做對照實驗：追加不同寫法之 break 規則，看章題是否回到頁首。"""
import io, os, re, subprocess, tempfile, time, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_print"))
import build38 as B
import pymupdf as fitz

SRC = os.path.join(B.HERE, "final38.html")
H = io.open(SRC, encoding="utf-8").read()
CH = [u"第一章　", u"第二章　", u"第三章　", u"第四章　", u"第五章　", u"第六章　", u"第七章　", u"第八章　", u"第九章　", u"結語　"]
prof = tempfile.mkdtemp(prefix="t109b-")


def render(extra, tag):
    h = H.replace("</body>", "<style>%s</style></body>" % extra) if "</body>" in H else H + extra
    hp = os.path.join(prof, "x_%s.html" % tag)
    pp = os.path.join(prof, "x_%s.pdf" % tag)
    io.open(hp, "w", encoding="utf-8").write(h)
    subprocess.run([B.find_browser(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--user-data-dir=" + os.path.join(prof, "ud-" + tag),
                    "--print-to-pdf=" + pp, "file:///" + hp.replace("\\", "/")], capture_output=True)
    for _ in range(400):
        if os.path.exists(pp) and os.path.getsize(pp) > 0:
            break
        time.sleep(0.1)
    time.sleep(1.2)
    d = fitz.open(pp)
    tops = 0
    for c in CH:
        for i in range(11, d.page_count):
            ls = [x.strip() for x in d[i].get_text().split("\n") if x.strip()]
            if any(x.startswith(c) for x in ls[:2]):
                tops += 1; break
    print("  %-22s 頁 %4d｜章題居頁首 %d／10" % (tag, d.page_count, tops))
    d.close()


render("", "base")
render("body > h1 { break-before: page !important; }", "body_h1")
render("h1 { break-before: page !important; } blockquote h1 { break-before: auto !important; }", "h1_plain")
