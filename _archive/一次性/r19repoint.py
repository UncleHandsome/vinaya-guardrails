# -*- coding: utf-8 -*-
"""r19repoint - 把 _work/_print 各腳本硬編之正文檔路徑，一律改為 hulan_path 法源。
_transforms: (1) os.path.join(目錄, 檔名) 形 → HP.SRC  (2) 單一 .txt 字串面值 → HP.SRC
再注入 prelude（放在 module docstring 之後，以免 __doc__ 失效）。未加 --go 只試跑。"""
import os, re, io, sys, ast

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GO = "--go" in sys.argv
HP = "HP.SRC"
PRELUDE = ("import os as _hp_os, sys as _hp_sys; "
           "_hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname("
           "_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path")

JOIN_RE = re.compile(
    r'os\.path\.join\(\s*r?"[^"\n]*XW[^"\n]*"\s*,\s*"[^"\n]*\.txt"\s*\)', re.S)
LIT_RE = re.compile(r'[A-Za-z]{0,2}"[^"\n]*XW[^"\n]*\.txt"')

COMMENT_FIX = [
    (u"未給則取 XW 目錄之《佛陀的護欄》。",
     u"未給則取工作資料夾根目錄之《佛陀的護欄》（法源 hulan_path）。"),
    (u"（基準預設為 XW 之本書現檔）",
     u"（基準預設為工作資料夾根目錄之本書現檔）"),
]


def targets():
    out = []
    for sub in ("_work", "_print"):
        d = os.path.join(ROOT, sub)
        for dirpath, dirnames, filenames in os.walk(d):
            dirnames[:] = [x for x in dirnames
                           if x not in ("__pycache__", "_retired_31" + u"\u7248")]
            for fn in filenames:
                if fn.endswith(".py") and not fn.startswith("r19"):
                    out.append(os.path.join(dirpath, fn))
    return sorted(out)


def insert_pos(lines):
    src = "\n".join(lines)
    try:
        node = ast.parse(src)
    except SyntaxError:
        return None
    if (node.body and isinstance(node.body[0], ast.Expr)
            and isinstance(getattr(node.body[0], "value", None), ast.Constant)
            and isinstance(node.body[0].value.value, str)):
        return node.body[0].end_lineno            # 1-based → 插入其後
    pos = 0
    while pos < len(lines) and (not lines[pos].strip()
                                or lines[pos].lstrip().startswith("#")):
        pos += 1
    return pos


report = []
for fp in targets():
    rel = os.path.relpath(fp, ROOT)
    t = io.open(fp, encoding="utf-8").read().replace("\r\n", "\n").replace("\r", "\n")
    if "XW" not in t:
        continue
    n_join = len(JOIN_RE.findall(t))
    t2 = JOIN_RE.sub(HP, t)
    hits = LIT_RE.findall(t2)
    t2 = LIT_RE.sub(HP, t2)
    n_lit = len(hits)
    cmts = 0
    for old, new in COMMENT_FIX:
        if old in t2:
            cmts += t2.count(old)
            t2 = t2.replace(old, new)
    lines = t2.split("\n")
    added = 0
    if "import hulan_path" not in t2:
        p = insert_pos(lines)
        if p is None:
            report.append((rel, n_join, n_lit, cmts, 0, "AST-FAIL"))
            continue
        lines.insert(p, PRELUDE)
        added = 1
        t2 = "\n".join(lines)
    residue = [i + 1 for i, l in enumerate(lines) if "XW" in l]
    report.append((rel, n_join, n_lit, cmts, added, residue))
    if GO:
        io.open(fp, "w", encoding="utf-8", newline="").write(t2)

print("%-34s %5s %5s %5s %6s  %s" % ("file", "join", "lit", "cmt", "prelude", "residue"))
bad = 0
for rel, a, b, c, d, res in report:
    print("%-34s %5d %5d %5d %6d  %s" % (rel, a, b, c, d, res))
    if res != [] or (a + b + c) == 0:
        bad += 1
print("files=%d  bad=%d  mode=%s" % (len(report), bad, "GO" if GO else "DRY"))
