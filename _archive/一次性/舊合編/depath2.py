# -*- coding: utf-8 -*-
"""二修：① 四尺補 plain `import os`（其檔內只 `import os as _hp_os`）② memsimp 之記憶路徑改由工作夾名推 slug（口徑如舊）。"""
import os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
WORK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GO = "--go" in sys.argv

A = ["ordchk.py", "tocsync.py", "hlface.py", "apxdiff.py"]
for n in A:
    p = os.path.join(WORK, "_work", n)
    t = open(p, encoding="utf-8").read()
    if re.search(r"^import os$", t, re.M):
        print("%-14s 已有 import os（略）" % n)
        continue
    m = re.search(r"^(\s*)(?:sys\.path\.insert|NEW = |LAST = )", t, re.M)
    lines = t.split("\n")
    idx = next((i for i, l in enumerate(lines)
                if re.search(r"\bos\.path\.", l) and not l.strip().startswith("import os as")), None)
    lines.insert(idx, "import os")
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines)) if GO else None
    print("%-14s 於第 %d 行前插 `import os`" % (n, idx + 1))

# memsimp：slug 由工作夾絕對路徑推得（非英數皆換 '-'），與 Qoder 之專案目錄同名——口徑復舊，不掃他專案
p = os.path.join(WORK, "_work", "memsimp.py")
t = open(p, encoding="utf-8").read()
OLD = "DIRS = [os.path.expanduser(u'~/.qoder/memory'),\n        u'~/.qoder/projects/*/memory']"
NEW = ("import re as _re\n"
       "ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n"
       "SLUG = _re.sub(u'[^0-9A-Za-z]', u'-', ROOT)\n"
       "DIRS = [os.path.expanduser(u'~/.qoder/memory'),\n"
       "        os.path.expanduser(u'~/.qoder/projects/%s/memory' % SLUG)]")
if OLD in t:
    t = t.replace(OLD, NEW)
    print("memsimp.py     記憶路徑改由 slug 推得（僅本專案・他機亦通）")
    open(p, "w", encoding="utf-8", newline="\n").write(t) if GO else None
else:
    print("memsimp.py     ★形制不符，未改（須目核）：\n" + "\n".join(t.split("\n")[:8]))
