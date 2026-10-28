# -*- coding: utf-8 -*-
"""版心之側：合冊影印版之裝訂邊，須隨**物理頁奇偶**交替。

量法：頁腳頁碼是「欄心對齊」——其橫向中心隨版心而移，且不受內文縮排干擾。
  內 18mm／外 10mm ⇒ 欄心二值：奇頁（寬右）≈286.4pt；偶頁（寬左）≈309.0pt。
右開（右側裝訂）之約：物理奇數頁（recto）寬邊在右；偶數頁（verso）寬邊在左。
封面、隔頁、各卷自身之封面（無頁碼）不判，如實印免判之數。

用法：python -X utf8 _work/pairgutter.py [pdf]   # 預設量現行合冊影印版
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEF = os.path.join(ROOT, "_print", u"雙子星合冊_起心動念＋如法推尋_影印版.pdf")
PDF = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else DEF
NEG = "--neg" in sys.argv          # 負測：互換期望值（現行冊應全紅），證尺能紅能點名
import pymupdf  # noqa: E402

C_OUTER, C_INNER = 286.4, 309.0      # 奇頁（寬右）／偶頁（寬左）之頁碼中心
if NEG:
    C_OUTER, C_INNER = C_INNER, C_OUTER
TOL = 4.0


def label_prefix(lb):
    s = lb.get("prefix", u"") or u""
    m = re.match(r"^<([0-9A-Fa-f]+)>$", s)
    if not m:
        return s
    b = bytes.fromhex(m.group(1))
    for enc in ("utf-8", "utf-16-be"):
        try:
            return b.decode(enc)
        except UnicodeDecodeError:
            continue
    return s


def footer_center(pg):
    for blk in pg.get_text("dict")["blocks"]:
        for ln in blk.get("lines", []):
            for sp in ln["spans"]:
                t = sp["text"].strip()
                if re.fullmatch(r"\d{1,3}", t) and sp["bbox"][1] > 760:
                    return (sp["bbox"][0] + sp["bbox"][2]) / 2
    return None


d = pymupdf.open(PDF)
labels = d.get_page_labels()
if len(labels) < 4:
    raise SystemExit(u"頁碼標籤不足（%d 段）——非合冊之形" % len(labels))
names = [label_prefix(x) for x in labels]
starts = [x["startpage"] for x in labels] + [d.page_count]
ranges = [(names[i], starts[i], starts[i + 1]) for i in range(len(labels))]
vols = [(nm, a, b) for nm, a, b in ranges if nm.startswith(u"卷一") or nm.startswith(u"卷二")]
div = [(nm, a, b) for nm, a, b in ranges if nm.startswith(u"合璧")]

bad, skipped, checked = [], 0, 0
for nm, a, b in vols:
    for i in range(a, b):
        c = footer_center(d[i])
        if c is None:
            skipped += 1
            continue
        want = C_OUTER if (i + 1) % 2 == 1 else C_INNER
        checked += 1
        if abs(c - want) > TOL:
            bad.append((nm, i + 1, round(c, 1), want))

print(u"版心之側｜%s" % os.path.basename(PDF))
print(u"  管轄：卷一 %d–%d・卷二 %d–%d・隔頁 %s（免判）・判 %d 頁・免判 %d 頁（無頁碼：封面類）"
      % (vols[0][1] + 1, vols[0][2], vols[1][1] + 1, vols[1][2],
         (u"%d–%d" % (div[0][1] + 1, div[0][2])) if div else u"無", checked, skipped))
if bad:
    print(u"  ✗ 版心翻面 %d 頁（卷・物理頁・頁碼中心・應為）" % len(bad))
    for nm, phys, c, want in bad[:10]:
        print(u"     %s p%d  實測 %.1f  應 %.1f" % (nm, phys, c, want))
    if len(bad) > 10:
        print(u"     ……餘 %d 頁" % (len(bad) - 10))
    d.close()
    sys.exit(1)
print(u"  ✓ 奇頁寬右・偶頁寬左，兩卷一致；接縫處不翻面")
d.close()
sys.exit(0)
