# -*- coding: utf-8 -*-
"""記錄檔之簡形歸正（逐行點名，不做全檔通換）：
   引號之內（『「）者為供狀或大正藏原形，一律不動——此即『以錯字為供狀』之護。
   只治本次與前次親手添寫之數行；行號由命令行給，器不自行猜範圍。
用法：python -X utf8 _work/recsimp_fix.py [--write] <檔>::<行號,行號…>
      例：python -X utf8 _work/recsimp_fix.py "列印SOP.md::27,40,41,42,43"
"""
import importlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
SD = importlib.import_module("_simpdict")
SM = importlib.import_module("_simpmap")
MAP = dict(SD.MAP)
for k, v in (getattr(SM, "MAP", {}) or {}).items():
    MAP.setdefault(k, v)
QUOTED = re.compile(r"『[^』]*』|「[^」]*」|“[^”]*”|‘[^’]*’|`[^`]*`")


def outside_quotes(line, cb):
    """對引號外之每一字調 cb(c)→新字（None 即不動）。"""
    keep = [(m.start(), m.end()) for m in QUOTED.finditer(line)]
    out = []
    for i, c in enumerate(line):
        if any(a <= i < b for a, b in keep):
            out.append(c)
            continue
        out.append(cb(c) or c)
    return "".join(out)


def main():
    write = "--write" in sys.argv
    specs = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not specs:
        raise SystemExit("須指名『檔::行號』，不作全檔通換")
    for s in specs:
        fn, nums = s.split("::")
        p = Path(fn) if Path(fn).is_absolute() else ROOT / fn
        raw = p.read_bytes().decode("utf-8")
        nl = "\r\n" if "\r\n" in raw else "\n"
        L = raw.split(nl)
        for n in [int(x) for x in nums.split(",")]:
            old = L[n - 1]
            got = [(c, MAP[c]) for c in dict.fromkeys(old) if c in MAP and MAP[c] != c]
            new = outside_quotes(old, lambda c: MAP.get(c))
            print(f"■ {p.name[:14]} L{n}・名單命中 {len(got)} 枚・引號外治 {sum(1 for a, b in zip(old, new) if a != b)} 字")
            print(f"    故 {old.strip()[:88]}")
            print(f"    新 {new.strip()[:88]}")
            if new != old:
                L[n - 1] = new
        if write:
            p.write_bytes(nl.join(L).encode("utf-8"))
            print("  ● 落盤")


main()
