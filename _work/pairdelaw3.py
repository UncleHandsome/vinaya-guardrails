# -*- coding: utf-8 -*-
"""去現代法令·第八刀（辛・通名之換）：全冊重複之世俗法『標籤』一律改歸律語。

承 `pairdelaw2.py`（庚）——庚治『孤句』（一錨一行），辛治『通名』（一詞十數見，非唯一錨可制）。
口徑：只換掛『世俗法』之標籤與專名，不動本書自制之『法定・憲法級・判處』與『道宣律師』之稱。

護五道：
  一・前後之數須印出（換前幾見、換後餘幾見），餘數不為零即報。
  二・圍欄內之換字須同寬：逐行比換前後之欄寬，不同寬即拒寫（免破圖）。
  三・新文須過簡形閘（`_simpmap`∪`_simpdict`）；並順掃全冊——『与学・须弥』之類由是現形；
     『几』（案几）乃繁簡同形之正字，列入白名單，不誤傷。
  四・法名之總數須真降（不降即刀落空，拒寫）。
  五・兩冊俱校畢、全無誤，方落盤（一錯則整批不動）；備份 .pre_delaw3＋SHA 對照＋清冊。

用法：python -X utf8 _work/pairdelaw3.py          # 試跑
      python -X utf8 _work/pairdelaw3.py --write  # 落盤
"""
import hashlib
import importlib
import pairsimp as PS  # noqa: E402
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
m = importlib.import_module("pairdelaw")
_simpmap = importlib.import_module("_simpmap")
_simpdict = importlib.import_module("_simpdict")

FILES = ["如法推尋：僧伽憲政、法權審理與修復正義.txt",
         "起心動念：四分律的心智顯微鏡與唯識解剖.txt"]
TOKEN = [("法律效果", "律制之效"),
         ("法律定性", "律制定性"),
         ("罪刑法定", "未制不犯"),
         ("与学比丘", "與學比丘"),
         ("须弥山", "須彌山")]
FALSE_SIMP = set("几")          # 繁簡同形之正字（案几），非簡形


def dwidth(s):
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F", "A") else 1 for c in s)


def main():
    write = "--write" in sys.argv
    SIMPLE = (set(_simpmap.MAP) | set(_simpdict.MAP)) - FALSE_SIMP
    errs, ledger, plans = [], [], []
    for old, new in TOKEN:
        for c in set(new) & SIMPLE:
            errs.append(f"新文簡形：{c}｜{new}←{old}")
    for fn in FILES:
        p = ROOT / fn
        raw = p.read_bytes()
        lines = raw.decode("utf-8").split("\r\n")
        fence = m.fence_mask(lines)
        before_law = sum(len(m.HAS_LAW.findall(l)) for l in lines)
        print("=" * 74)
        print("■", fn)
        touched_any = 0
        for old, new in TOKEN:
            n = sum(l.count(old) for l in lines)
            if not n:
                continue
            touched = 0
            for i, l in enumerate(lines):
                if old not in l:
                    continue
                nl = l.replace(old, new)
                if fence[i] and dwidth(l) != dwidth(nl):
                    errs.append(f"{fn}・L{i + 1} 圍欄內換字不同寬：{dwidth(l)}→{dwidth(nl)}｜{old}")
                    continue
                if nl != l:
                    lines[i] = nl
                    touched += 1
                    ledger.append(f"{fn}\tL{i + 1}\t辛-通名\t{l.strip()[:44]} → {nl.strip()[:44]}")
            rest = sum(l.count(old) for l in lines)
            print(f"  「{old}」→「{new}」：換前 {n} 見・動行 {touched}・換後餘 {rest} 見")
        simp = [(i + 1, PS.hits(l), l.strip()[:52])
                for i, l in enumerate(lines) if PS.flag(l)]
        print(f"  簡形之順掃（刀後）：{len(simp)} 行 {simp[:3]}")
        if simp:
            errs.append(f"{fn}・刀後仍有簡形 {len(simp)} 行")
        after_law = sum(len(m.HAS_LAW.findall(l)) for l in lines)
        print(f"  法名／制度名：{before_law} → {after_law} 見・行數 {len(lines)}（不動）")
        if touched_any and after_law >= before_law:
            errs.append(f"{fn}・法名之數未降（{before_law}→{after_law}），刀落空")
        plans.append((p, raw, lines))
    for e in errs:
        print("  ✗", e)
    if errs:
        print("★有誤 → 兩冊俱不落盤")
        return
    (ROOT / "_work" / "pairdelaw3_cuts.txt").write_text("\n".join(ledger) + "\n", encoding="utf-8")
    print(f"\n刀口清冊 {len(ledger)} 行 → _work/pairdelaw3_cuts.txt")
    if not write:
        print("（試跑：未落盤）")
        return
    for p, raw, lines in plans:
        out = "\r\n".join(lines).encode("utf-8")
        if out == raw:
            print(f"  無改，不動：{p.name}")
            continue
        bak = ROOT / "_archive" / "備份" / "AI清理前" / (p.name + ".pre_delaw3")
        bak.write_bytes(raw)
        p.write_bytes(out)
        print(f"  落盤 {p.name}：SHA {hashlib.sha256(raw).hexdigest()[:12]} → {hashlib.sha256(out).hexdigest()[:12]}"
              f"・{len(out)} B・備份 {bak.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
