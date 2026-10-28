# -*- coding: utf-8 -*-
"""把諸器之簡形順掃收歸共器 _work/pairsimp.py（唯一法源）：
   刀自新文之護（set(new) & SIMPLE）照舊從嚴；全冊順掃改走 PS.hits()——
   引號內之語料原形（大正藏『並』『衆』之類）不為病。
用法：python -X utf8 _work/pairsimp_wire.py [--write]"""
import re
import sys
from pathlib import Path

W = "--write" in sys.argv
FILES = ["pairpurge.py", "pairpurge2.py", "pairpurge3.py", "pairdelaw3.py", "pairdelaw4.py",
         "pairtrim.py", "pairtrim_check.py"]
HEAD = re.compile(r"^(\s*)simp = \[\(i \+ 1, \"\"\.join\(sorted\(set\(c for c in l if c in SIMPLE\)\)\)(.*)$")
for f in FILES:
    p = Path("_work") / f
    s = p.read_bytes().decode("utf-8")
    out, cnt, armed = [], 0, False
    COND = "if any(c in SIMPLE for c in l)]"
    JOIN = '"".join(sorted(set(c for c in l if c in SIMPLE)))'
    for line in s.split("\n"):
        if line.lstrip().startswith("simp = [(i + 1,") and JOIN in line:
            rest = line.replace(JOIN, "PS.hits(l)").replace(COND, "if PS.flag(l)]")
            armed = COND not in line                  # 條件在下一行者，待下行改
            out.append(rest)
            cnt += 1
            continue
        if armed and COND in line:
            line = line.replace(COND, "if PS.flag(l)]")
            armed = False
        out.append(line)
    s2 = "\n".join(out)
    if cnt and COND in s2:
        raise SystemExit("條件未改盡：" + f)
    if cnt and "PS.hits(l)" not in s2:
        raise SystemExit("共器未接入：" + f)
    if cnt and "import pairsimp as PS" not in s2:
        for anchor in ("import importlib\n", "import re\n", "import sys\n"):
            if anchor in s2:
                s2 = s2.replace(anchor, anchor + "import pairsimp as PS  # noqa: E402\n", 1)
                break
        else:
            raise SystemExit("無插入錨：" + f)
    print(f"{f:<18}順掃之式改 {cnt} 處")
    if W and cnt:
        p.write_bytes(s2.encode("utf-8"))
