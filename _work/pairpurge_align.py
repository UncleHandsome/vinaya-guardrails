# -*- coding: utf-8 -*-
"""欄內對齊之第二招（由『前後兩行』實配，不重放刀）：
   換字後之行，若其後尚有欄間空白（≥3 格），以此消彼長之法補足／扣減，使右欄仍落原列；
   若全行只有一欄（無欄間可守），則如實縮——此乃圖題剝外文後之自然收攏，非破版。
用法：python -X utf8 _work/pairpurge_align.py [--write]
"""
import difflib
import hashlib
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FENCE = "```"
PAIRS = [("F2", "如法推尋：僧伽憲政、法權審理與修復正義.txt",
          "_archive/備份/AI清理前/如法推尋：僧伽憲政、法權審理與修復正義.txt.pre_purge"),
         ("F1", "起心動念：四分律的心智顯微鏡與唯識解剖.txt",
          "_archive/備份/AI清理前/起心動念：四分律的心智顯微鏡與唯識解剖.txt.pre_purge")]


def dw(s):
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F", "A") else 1 for c in s)


def flags(ls):
    out, inside = [], False
    for l in ls:
        if l.strip().startswith(FENCE):
            out.append(inside)
            inside = not inside
        else:
            out.append(inside)
    return out


def runs(s, frm=0):
    """回 s[frm:] 之連續空格段 [(起, 長)]。"""
    out, i = [], frm
    while i < len(s):
        if s[i] == " ":
            j = i
            while j < len(s) and s[j] == " ":
                j += 1
            out.append((i, j - i))
            i = j
        else:
            i += 1
    return out


OPEN = set("【（(「『[")
CLOSE = set("】）)」』]")


def depth_at(s, upto):
    d = 0
    for c in s[:upto]:
        if c in OPEN:
            d += 1
        elif c in CLOSE and d:
            d -= 1
    return d


def cols(s):
    """欄位起列：只認『括弧外之 ≥3 空白後接非空白』者；回 [0, c1, c2…]。"""
    out, i = [0], 0
    while i < len(s):
        if s[i] == " ":
            j = i
            while j < len(s) and s[j] == " ":
                j += 1
            if j - i >= 3 and j < len(s) and s[j] != " " and not depth_at(s, i):
                out.append(dw(s[:j]))
            i = j
        else:
            i += 1
    return out


def realign(bline, cline):
    """以『欄位起列』為準逐欄校平——總寬之差不算數（末欄因剥外文而縮短，乃自然收攏）。
       只動括弧外之欄間：框內之空白是標籤之腹，動它即撐破括號。"""
    cb = cols(bline)
    out, n_fix = cline, 0
    for k in range(1, len(cb)):
        cc = cols(out)
        if k >= len(cc) or cb[k] == cc[k]:
            continue
        gs = [(i, l) for i, l in runs(out) if l >= 3 and not depth_at(out, i)]
        if k - 1 >= len(gs):
            break
        start, ln = gs[k - 1]
        need = ln + (cb[k] - cc[k])
        if need < 3:
            break
        out = out[:start] + " " * need + out[start + ln:]
        n_fix += 1
    return out, n_fix and cols(out)[:len(cb)] == cb


def main():
    write = "--write" in sys.argv
    for tag, fn, bak in PAIRS:
        a = (ROOT / bak).read_bytes().decode("utf-8").split("\r\n")
        p = ROOT / fn
        b = p.read_bytes().decode("utf-8").split("\r\n")
        fa, fb = flags(a), flags(b)
        sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
        todo = []
        for _, t1, t2, u1, u2 in sm.get_opcodes():
            if t2 - t1 != 1 or u2 - u1 != 1 or a[t1] == b[u1] or not (fa[t1] and fb[u1]):
                continue
            new, ch = realign(a[t1], b[u1])
            if ch:
                todo.append((u1, b[u1], new))
        print(f"■ {tag}・補欄 {len(todo)} 行")
        for i, o, n in todo:
            print(f"    L{i + 1:<6} 故 {o.strip()[:50]}\n           新 {n.strip()[:50]}")
            b[i] = n
        if write and todo:
            raw = p.read_bytes()
            (ROOT / "_archive/備份/AI清理前" / (fn + ".pre_align")).write_bytes(raw)
            data = "\r\n".join(b).encode("utf-8")
            p.write_bytes(data)
            print(f"    落盤：SHA {hashlib.sha256(raw).hexdigest()[:12]} → {hashlib.sha256(data).hexdigest()[:12]}")
        elif todo:
            print("    （試跑：未落盤）")


main()
