# -*- coding: utf-8 -*-
"""提交前之兩關：① 絕對路徑全數（不限「lionc」）② ver38 刪文之去處（不失方敢入帳）。"""
import os, re, sys, io, subprocess, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

EXCL_DIRS = (".git", "Python", "__pycache__")
EXCL_PRE = ("_print/", "_archive/備份/")


def walk():
    for r, ds, fs in os.walk("."):
        r = r.replace("\\", "/").lstrip("./")
        ds[:] = [d for d in ds if os.path.join(r, d).replace("\\", "/").lstrip("./") not in
                 [os.path.join(x, y) for x in EXCL_DIRS for y in [""]]]
        ds[:] = [d for d in ds if d not in EXCL_DIRS]
        for f in fs:
            yield (r + "/" + f).replace(".//", "").lstrip("./")


print("=== 1. 絕對路徑・用戶名・记忆庫位址 之全數（候提交集）===")
PAT = re.compile(r"(C:\\+Users|C:/+Users|/Users/lionc|OneDrive|\.qoder[/\\\\](projects|memory)|lionc)")
hits = {}
for f in walk():
    if f.startswith(EXCL_PRE) or f.endswith((".pyc",)):
        continue
    if f.startswith("_print/"):
        continue
    try:
        t = open(f, encoding="utf-8", errors="ignore").read()
    except Exception:
        continue
    n = len(PAT.findall(t))
    if n:
        hits[f] = n
for k, v in sorted(hits.items(), key=lambda x: -x[1]):
    print("   %-46s %d 處" % (k, v))
print("   合计 %d 檔／%d 處" % (len(hits), sum(hits.values())))

print("\n=== 2. ver38 刪文之去處（HEAD 舊身 − 今身 = 1578 行，須有著落）===")
FN = "ver38四分律_起心動念心智分析框架_修正版.md"
old = subprocess.run(["git", "show", "HEAD:" + FN], capture_output=True).stdout.decode("utf-8").split("\n")
new = open(FN, encoding="utf-8").read().split("\n")
from collections import Counter
co, cn = Counter(old), Counter(new)
removed = []
for line, c in co.items():
    d = c - cn.get(line, 0)
    if d > 0:
        removed += [line] * d
removed = [l for l in removed if l.strip()]
print("   實刪非空行：%d（HEAD 行 %d → 今行 %d）" % (len(removed), len(old), len(new)))

store = {}
for f in ["_archive/編纂底冊.md", "_archive/編年工程日誌.md"] + glob.glob("_archive/DELETED-*.txt"):
    store[f] = open(f, encoding="utf-8", errors="ignore").read()
landed, orphan = 0, []
for l in removed:
    if any(l in s for s in store.values()):
        landed += 1
    else:
        orphan.append(l)
print("   落於底冊／日誌／刪除帳者：%d／%d" % (landed, len(removed)))
print("   無著落：%d 行" % len(orphan))
for l in orphan[:18]:
    print("      | " + l.strip()[:96])

print("\n=== 3. 新增（今身 − HEAD）须入帳之動 ===")
added = []
for line, c in cn.items():
    d = c - co.get(line, 0)
    if d > 0:
        added += [line] * d
for l in [x for x in added if x.strip()][:8]:
    print("      + " + l.strip()[:96])
print("   新增非空行：%d" % len([x for x in added if x.strip()]))
