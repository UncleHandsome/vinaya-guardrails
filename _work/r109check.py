# -*- coding: utf-8 -*-
"""第 109 輪之軸：章級 H1 是否真另起新頁（讀成品 PDF，非信中介檔）。

用法：python -X utf8 _work/r109check.py [PDF 檔名...]；未給檔則驗 _print 下四式交付檔。
判準：章題須落在該頁頭兩行之內（第一行或頁碼之後之第二行）。
"""
import io, os, sys
import pymupdf as fitz

sys.stdout.reconfigure(encoding='utf-8', errors='replace')   # 免受 CP950 控制台所困

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = [u"第一章　", u"第二章　", u"第三章　", u"第四章　", u"第五章　", u"第六章　",
      u"第七章　", u"第八章　", u"第九章　", u"結語　", u"附錄A　", u"附錄B　",
      u"附錄C　", u"附錄D　", u"附錄E　", u"附錄F　", u"附錄H　", u"附錄I　",
      u"附錄J　", u"附錄K　", u"附錄L　", u"附錄M　", u"終卷　"]
DEFAULT = [u"ver38四分律_起心動念心智分析框架_第三十八版_列印版.pdf",
           u"ver38四分律_起心動念心智分析框架_第三十八版_列印版_精簡本.pdf",
           u"ver38四分律_起心動念心智分析框架_第三十八版_螢幕版.pdf",
           u"ver38四分律_起心動念心智分析框架_第三十八版_螢幕版_精簡本.pdf"]
files = sys.argv[1:] or DEFAULT
bad = 0
for fn in files:
    p = fn if os.path.exists(fn) else os.path.join(HERE, "_print", fn)
    d = fitz.open(p)
    present, tops = [], []
    for c in CH:
        for i in range(11, d.page_count):
            lines = [x.strip() for x in d[i].get_text().split("\n") if x.strip()]
            for j, x in enumerate(lines):
                if x.startswith(c) and "." not in x:
                    present.append(c)
                    tops.append((c, i + 1, j))
                    break
            else:
                continue
            break
    late = [(c, pg + 1, j) for c, pg, j in tops if j > 1]
    print("%-46s 頁 %4d｜篇題 %2d／%2d｜居頁首 %2d｜未居頁首 %d %s" % (
        os.path.basename(fn)[:46], d.page_count, len(present), len(CH), len(tops) - len(late), len(late),
        ("← " + "、".join("%s(p%d 第%d行)" % (c, pg, j) for c, pg, j in late[:6])) if late else "✔"))
    bad += len(late)
    d.close()
print("總計未居頁首 %d 處" % bad)
sys.exit(1 if bad else 0)
