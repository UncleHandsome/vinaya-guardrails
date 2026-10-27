# -*- coding: utf-8 -*-
"""第十五波・收尾兩小刀：
① 卡題之分隔符依兩冊成例歸一（本人新造之 U+FF65『･』半形 ➔ U+30FB『・』全形，
   成例 220 見；半形入框則格寬失算——『半形斜線歸全形』之舊案）。
② F2 L2936 柵內『外部獨立理事會』➔『外部客僧覆審會』（乙1 列名之『理事會』未盡者，
   等寬七字，格數不動）。
"""
import hashlib
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "_work"))
import pairsimp                                       # noqa: E402

LF, CRLF = chr(10), chr(13) + chr(10)
FF65, MID = chr(0xFF65), chr(0x30FB)
BOOKS = [next(os.path.join(ROOT, x) for x in os.listdir(ROOT) if x.startswith(w) and x.endswith(u".txt"))
         for w in (u"起心動念", u"如法推尋")]


def dw(s):
    return sum(2 if ord(c) > 0x2000 else 1 for c in s)


def main():
    go = "--write" in sys.argv
    tot = 0
    for p in BOOKS:
        before = io.open(p, "rb").read().decode("utf-8-sig")
        sha = hashlib.sha256(before.encode("utf-8")).hexdigest()[:12]
        nl = CRLF if CRLF in before else LF
        L = before.replace(CRLF, LF).split(LF)
        n1 = sum(1 for l in L if FF65 in l)
        n2 = sum(1 for l in L if u"外部獨立理事會" in l)
        print(u"%s・%d 行・SHA %s｜FF65 %d 行・理事會 %d 行"
              % (os.path.basename(p)[:12], len(L), sha, n1, n2))
        if n1 + n2 == 0:
            print(u"  ・無新造之半形分隔符・無未盡之理事會（已歸成例）")
            continue
        for i, l in enumerate(L):
            if FF65 in l:
                new = l.replace(FF65, MID)
                if dw(new) > 80 and l.startswith(u"【"):
                    raise SystemExit(u"caption 改全形後逾框寬（%d）➔%s" % (dw(new), new[:40]))
                l = new
            if u"外部獨立理事會" in l:
                cand = l.replace(u"外部獨立理事會", u"外部客僧覆審會")   # 七字代七字・柵內格數不動
                if dw(cand) != dw(l):
                    raise SystemExit(u"替後格數異（%d≠%d）➔%s" % (dw(cand), dw(l), l[:36]))
                l = cand
            L[i] = l
        tot += n1
        for i, l in enumerate(L, 1):
            h = pairsimp.hits(l)
            if h:
                raise SystemExit(u"簡形 L%d「%s」" % (i, h))
        if not go:
            print(u"  （試跑・加 --write 始落盤）")
            continue
        bk = os.path.join(ROOT, "_archive", u"備份", u"AI清理前",
                          os.path.basename(p) + ".pre_a15e")
        io.open(bk, "wb").write(before.encode("utf-8"))
        out = nl.join(L).encode("utf-8")
        io.open(p, "wb").write(out)
        chk = io.open(p, "rb").read().decode("utf-8")
        if chk.count(chr(13)) != chk.count(chr(10)):
            raise SystemExit(u"行尾混雜")
        print(u"  落盤：%d 行・SHA %s ➔ %s" % (len(L), sha, hashlib.sha256(out).hexdigest()[:12]))
    print(u"合計歸一 %d 行" % tot)
    return 0


if __name__ == "__main__":
    sys.exit(main())
