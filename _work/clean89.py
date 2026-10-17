# -*- coding: utf-8 -*-
"""第 89 輪之工作檔清理（只動 _work；--go 才真刪，並落憑據於 _archive）。

保：書中／SOP／_tk 點名之檔、可重跑之軸、本批回滾點（round84_pre.md 與
    round88_pre.md）、clean82.py／clean89.py 本身。
刪：一輪性套改腳本與其輸出（其結案之實已記入附錄M 編年）。
"""
import io, os, re, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WF = os.path.join(ROOT, "_work")
GO = "--go" in sys.argv
MDNAME = "ver38四分律_起心動念心智分析框架_修正版.md"

src = io.open(os.path.join(ROOT, MDNAME), encoding="utf-8").read()
src += io.open(os.path.join(ROOT, u"列印SOP.md"), encoding="utf-8").read()
src += io.open(os.path.join(ROOT, "_tk.py"), encoding="utf-8").read()
src += io.open(os.path.join(ROOT, "_print", "build38.py"), encoding="utf-8").read()
src += io.open(os.path.join(ROOT, "_print", "verify38.py"), encoding="utf-8").read()

NAMED = set(re.findall(r"([A-Za-z0-9_\-]+\.(?:py|json|txt|md|css|html|pdf))", src))
KEEP = {"clean82.py", "clean82.txt", "clean89.py"}
# 舊回滾點（round84／88／93／96_pre.md）隨歷輪結案除之；新輪起點副本由當輪自備。

gone, stay = [], []
for f in sorted(os.listdir(WF)):
    p = os.path.join(WF, f)
    if not os.path.isfile(p):
        continue
    if f in NAMED or f in KEEP:
        stay.append(f)
    elif f.startswith("__pycache__"):
        gone.append(f)
    else:
        gone.append(f)

sys.stdout.write("KEEP %d  DELETE %d  (%.1f MB)\n"
                 % (len(stay), len(gone),
                    sum(os.path.getsize(os.path.join(WF, x)) for x in gone) / 1048576.0))
io.open(os.path.join(WF, "clean89_list.txt"), "w", encoding="utf-8").write(
    u"## 保留（在册或被點名）%d\n  %s\n\n## 擬刪 %d\n  %s\n"
    % (len(stay), u" ".join(stay), len(gone), u"\n  ".join(gone)))

if not GO:
    raise SystemExit(0)

ARC = os.path.join(ROOT, "_archive")
man = [u"# 清除憑據（第 89 輪工作檔之清蕩 · %s）" % time.strftime("%Y-%m-%d %H:%M"),
       u"", u"## 保留（書中或管線點名、可重跑之軸、本批回滾點）%d 項" % len(stay),
       u"  " + u" ".join(stay), u"", u"## 删除（一輪性腳本與其輸出；結案之實已載附錄M）%d 項" % len(gone)]
freed = 0
for f in gone:
    p = os.path.join(WF, f)
    if f == "clean89_list.txt":
        continue
    freed += os.path.getsize(p)
    os.remove(p)
    man.append(u"  _work/" + f)
man.append(u"")
man.append(u" freed %.1f MB" % (freed / 1048576.0))
io.open(os.path.join(ARC, "DELETED-20260923.txt"), "a", encoding="utf-8").write(
    u"\n" + u"\n".join(man) + u"\n")
os.remove(os.path.join(WF, "clean89_list.txt"))
sys.stdout.write("DONE  kept %d\n" % len([x for x in os.listdir(WF) if os.path.isfile(os.path.join(WF, x))]))
