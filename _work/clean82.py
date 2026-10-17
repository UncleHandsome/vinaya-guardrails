# -*- coding: utf-8 -*-
"""清理試算（dry run）。--go 才真刪。分類原則：
   保：被書中或SOP 點名者、仍在使用之驗收軸、本輪回滾點、現行主檔與腳本。
   刪：一輪性腳本與探針輸出、舊回滾點、過時 PDF、build log、__pycache__。
   存檔：舊版本文檔與舊驗收器（移入 _archive，不即刪）。"""
import io, os, re, sys, shutil, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GO = "--go" in sys.argv
MDNAME = u"ver38四分律_起心動念心智分析框架_修正版.md"
md = io.open(os.path.join(ROOT, MDNAME), encoding="utf-8").read()
sop = io.open(os.path.join(ROOT, u"列印SOP.md"), encoding="utf-8").read()
tk = io.open(os.path.join(ROOT, "_tk.py"), encoding="utf-8").read()
NAMED = set(re.findall(r"_work/([A-Za-z0-9_.\-]+)", md + sop + tk))
NAMED |= {x for n in list(NAMED) for x in (n, n.split("/")[0])}

LIVE = {"rows2.py", "sweep66.py", "sweep67.py", "sweep67b.py", "suspect74.py", "jp74c.py",
        "p2probe.py", "dupaudit79.py", "patch_dedup2.json", "h4seq.py", "duphead.py",
        "selfcount72.py", "zhengli72b.py", "matrix81.txt", "sweep67c.py"}

cat = {}


def put(k, path, why=u""):
    cat.setdefault(k, []).append((os.path.relpath(path, ROOT).replace("\\", "/"),
                                  os.path.getsize(path) if os.path.isfile(path) else 0, why))


# ---------- _work ----------
WF = os.path.join(ROOT, "_work")
for f in sorted(os.listdir(WF)):
    p = os.path.join(WF, f)
    if not os.path.isfile(p):
        continue
    if f in ("ls82.txt", "ls82b.txt", "t82ls.py", "t82ls2.py", "clean82.py", "clean82.txt"):
        put("本輪盤點檔（試算後亦刪）", p)
        continue
    if f.startswith("round81"):
        put("保留：本轮回滚点", p)
        continue
    if f.startswith("round") and f.endswith("_pre.md"):
        put("删：旧回滚点", p)
        continue
    if f in LIVE or f in NAMED:
        put("保留：在册工具或书中点名", p)
        continue
    if re.match(r"^r\d{2}", f) or f.startswith("t81") or f.startswith("t82"):
        put("删：一轮性脚本", p)
        continue
    if f.endswith((".txt", ".log", ".json", ".css")):
        put("删：探针输出与日志", p)
        continue
    put("删：一轮性脚本", p)

# ---------- _print ----------
PR = os.path.join(ROOT, "_print")
for f in sorted(os.listdir(PR)):
    p = os.path.join(PR, f)
    if os.path.isdir(p):
        if f == "__pycache__":
            put("删：__pycache__", p)
        else:
            put("保留：目录 " + f, p)
        continue
    if f.endswith(".pdf") or f.endswith(".docx"):
        (put(u"删：Typst 一路（明令退役）", p) if ("Typst" in f or "typst" in f)
         else put(u"删：過時產物（可重建）", p))
        continue
    if f.endswith(".typ") or f == "build38_typst.py":
        put(u"删：Typst 一路（明令退役）", p)
        continue
    if f in ("build38.py", "verify38.py", "print38.css"):
        put("保留：现行列印管線", p)
        continue
    if f in ("verify31.py", "verify32.py", "verify35.py", "verify35_run.log"):
        put(u"存档：舊版驗收器", p)
        continue
    if os.path.splitext(f)[1] in (".txt", ".log", ".html", ".md") or re.match(r"^_", f) or f.startswith("r2_"):
        put(u"删：過時產物與探針（可重建）", p)
        continue
    put(u"删：過時產物與探針（可重建）", p)

# ---------- root ----------
for f in sorted(os.listdir(ROOT)):
    p = os.path.join(ROOT, f)
    if os.path.isdir(p) and f == "__pycache__":
        put("删：__pycache__", p)
    elif os.path.isfile(p) and re.match(r"^ver3[56]", f):
        put("存档：旧版本文档", p)
    elif os.path.isfile(p) and f == "ref.txt":
        put("存档：来源不明之参考撷取（09-20）", p)

keys = sorted(cat)
out = []
tot = 0
for k in keys:
    rows = cat.get(k, [])
    sz = sum(r[1] for r in rows) / 1024.0
    if k.startswith(u"删"):
        tot += sz
    out.append(u"### %s：%d 項，%.1f MB" % (k, len(rows), sz / 1024.0))
    if k.startswith(u"保留"):
        out.append(u"    " + u" ".join(r[0].split("/")[-1] for r in rows[:80]))

miss = sorted(x for x in NAMED if "." in x and not os.path.exists(os.path.join(WF, x)))
out.append(u"")
out.append(u"### 點名而實不存在之 _work 檔（編年虛報，待改）%d" % len(miss))
out.append(u"    " + u" ".join(miss))
io.open(os.path.join(ROOT, "_work", "clean82.txt"), "w", encoding="utf-8").write(u"\n".join(out))
print("TO_DELETE_MB %.1f  NAMED_MISSING %d" % (tot / 1024.0, len(miss)))

SELF = {"_work/clean82.py", "_work/clean82.txt"}
if not GO:
    raise SystemExit(0)

ARC = os.path.join(ROOT, "_archive")
if not os.path.isdir(ARC):
    os.makedirs(ARC)
man = [u"# 清除憑據（2026-09-22 第 82 輪工作檔清蕩）"]
BAD = []
freed = 0
for k in sorted(cat):
    rows = cat[k]
    if k.startswith(u"存档"):
        man.append(u"")
        man.append(u"## 移存 _archive：%s（%d 項）" % (k, len(rows)))
        for rel, sz, _w in rows:
            src = os.path.join(ROOT, rel.replace("/", os.sep))
            try:
                shutil.move(src, os.path.join(ARC, os.path.basename(rel)))
                man.append(u"  %s  (%.1f KB)" % (rel, sz / 1024.0))
            except Exception as e:
                BAD.append(u"MOVE %s %s" % (rel, e))
    elif k.startswith(u"删"):
        man.append(u"")
        man.append(u"## 删：%s（%d 項，%.1f MB）" % (k, len(rows), sum(r[1] for r in rows) / 1048576.0))
        for rel, sz, _w in rows:
            if rel in SELF:
                continue
            p = os.path.join(ROOT, rel.replace("/", os.sep))
            try:
                if os.path.isdir(p):
                    shutil.rmtree(p)
                else:
                    os.remove(p)
                    freed += sz
                man.append(u"  " + rel)
            except Exception as e:
                BAD.append(u"DEL %s %s" % (rel, e))
io.open(os.path.join(ARC, "DELETED-20260922.txt"), "w", encoding="utf-8").write(
    u"\n".join(man) + u"\n\n## 本次未成（可重跑續清）%d 項\n" % len(BAD) + u"\n".join(BAD))
print("DONE freed_MB %.1f  failed %d  manifest %d lines" % (freed / 1048576.0, len(BAD), len(man)))
