# -*- coding: utf-8 -*-
"""星號之復原：前run之『空斜體清理』規則太貪，把 `* **粗體**` 之起手法則一并吞去（親犯，現於印面 8 處）。
   判式：行首為 `*` 而緊接非空白非星號者，其 `**` 必成對——奇數者即被吞，補回 `** ` 一節。
用法：python -X utf8 _work/pairstar_fix.py [--write]
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = ["如法推尋：僧伽憲政、法權審理與修復正義.txt",
         "起心動念：四分律的心智顯微鏡與唯識解剖.txt"]
BULLET_STAR = re.compile(r"^\*(?=[^\s*])")


def main():
    write = "--write" in sys.argv
    tot = 0
    for fn in FILES:
        p = ROOT / fn
        ls = p.read_bytes().decode("utf-8").split("\r\n")
        hits = []
        for i, l in enumerate(ls):
            if not BULLET_STAR.match(l) or l.strip().count("**") % 2 == 0:
                continue
            ls[i] = "* ** " + l[1:]
            hits.append((i + 1, l.strip()[:44], ls[i].strip()[:48]))
        tot += len(hits)
        print(f"■ {fn[:14]}…・復原 {len(hits)} 行")
        for i, o, n in hits:
            print(f"    L{i:<6} 故 {o}\n           新 {n}")
        if write and hits:
            raw = p.read_bytes()
            (ROOT / "_archive/備份/AI清理前" / (fn + ".pre_starfix")).write_bytes(raw)
            p.write_bytes("\r\n".join(ls).encode("utf-8"))
            print(f"    落盤：SHA {hashlib.sha256(raw).hexdigest()[:12]} → {hashlib.sha256(p.read_bytes()).hexdigest()[:12]}")
    print("合計", tot, "行", "（試跑：未落盤）" if not write else "")


main()
