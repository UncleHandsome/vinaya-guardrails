# -*- coding: utf-8 -*-
"""去絕對路徑：把 _work 諸尺內之 `C:\\Users\\lionc\\…` 字面改為自 __file__ 推得（本機行為不變，他機可用）。

規則（逐支明列，非通配改寫）：
  A) `sys.path.insert(0, r"<ROOT>")`        → 由 __file__ 推資料夾根
  B) `X = r"<ROOT>\\_work\\y"`              → os.path.join(dirname(__file__), "y")（本檔即在 _work）
  C) memsimp 之專案記憶絕對路徑            → glob 于 ~/.qoder/projects/*/memory
用法：python -X utf8 _merge/depath.py [--go]
"""
import os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
WORK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GO = "--go" in sys.argv
ROOTLIT = "C:\\Users\\lionc\\OneDrive\\桌面\\教務交接\\星韋師\\戒律分析"

A_FILES = ["ordchk.py", "tocsync.py", "r7patch7.py", "r7patch7b.py", "r8patch.py", "r9fix.py",
           "r9fix2.py", "r9patch.py", "r10fix.py", "r10patch.py"]
B_MAP = {"hlface.py": "hlface.last", "apxdiff.py": "appendix_jieben.md"}
C_FILES = ["memsimp.py"]

A_LIT = 'r"%s"' % ROOTLIT
A_NEW = 'os.path.dirname(os.path.dirname(os.path.abspath(__file__)))'
A2_LIT = 'r"%s\\_work"' % ROOTLIT          # r9fix 之變體：直接指向 _work
A2_NEW = 'os.path.dirname(os.path.abspath(__file__))'

changed = []
for name in A_FILES + ["r9fix.py"]:
    p = os.path.join(WORK, "_work", name)
    t = open(p, encoding="utf-8").read()
    lit, new = (A_LIT, A_NEW)
    if lit not in t and A2_LIT in t:
        lit, new = A2_LIT, A2_NEW
    if lit not in t:
        changed.append((name, "規則 A 之字面不在檔（略）"))
        continue
    n = t.count(lit)
    t = t.replace(lit, new)
    if not re.search(r"^import os\b|^import os$|^import os[ ,]", t, re.M):
        t = t.replace(A_NEW + ")", A_NEW + ")", 1)
        # 於第一处使用前補 import os（本檔已 import sys，故附於其後）
        t = re.sub(r"^(import sys\b[^\n]*\n)", r"\1import os\n", t, count=1, flags=re.M)
    changed.append((name, "規則 A：換 %d 处%s" % (n, "＋補 import os" if "import os\n" in t and not re.search(r"^import os\b", t, re.M) else "")))
    if GO:
        open(p, "w", encoding="utf-8", newline="\n").write(t)

for name, leaf in B_MAP.items():
    p = os.path.join(WORK, "_work", name)
    t = open(p, encoding="utf-8").read()
    lit = 'r"%s\\_work\\%s"' % (ROOTLIT, leaf)
    if lit not in t:
        changed.append((name, "規則 B 之字面不在檔（略）"))
        continue
    t = t.replace(lit, 'os.path.join(os.path.dirname(os.path.abspath(__file__)), u"%s")' % leaf)
    if not re.search(r"^import os\b", t, re.M):
        t = re.sub(r"^(import io\b[^\n]*\n)", r"\1import os\n", t, count=1, flags=re.M)
    changed.append((name, "規則 B：換 1 处"))
    if GO:
        open(p, "w", encoding="utf-8", newline="\n").write(t)

for name in C_FILES:
    p = os.path.join(WORK, "_work", name)
    t = open(p, encoding="utf-8").read()
    lit = "u'C:/Users/lionc/.qoder/projects/C--Users-lionc-OneDrive-----------------/memory'"
    if lit not in t:
        changed.append((name, "規則 C 之字面不在檔（略）"))
        continue
    t = t.replace(lit, "u'~/.qoder/projects/*/memory'").replace(
        "for f in sorted(glob.glob(os.path.join(d, u'*.md'))):",
        "for f in sorted(glob.glob(os.path.join(os.path.expanduser(d), u'*.md'))):")
    changed.append((name, "規則 C：記憶庫改 glob 於 ~/.qoder/projects/*/memory"))
    if GO:
        open(p, "w", encoding="utf-8", newline="\n").write(t)

print("== 擬改／已改（%s）==" % ("落刀" if GO else "試跑"))
for n, d in changed:
    print("   %-16s %s" % (n, d))

left = []
for r, ds, fs in os.walk(os.path.join(WORK, "_work")):
    if "__pycache__" in r:
        continue
    for f in fs:
        if f.endswith(".py") and "lionc" in open(os.path.join(r, f), encoding="utf-8", errors="ignore").read():
            left.append(f)
print("\n落刀後仍含使用者名者：%s" % (sorted(left) if left else "無"))
if not GO:
    print("（試跑未動檔；落刀加 --go）")
