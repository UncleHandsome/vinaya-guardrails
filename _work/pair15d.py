# -*- coding: utf-8 -*-
"""第十五波・丁2 —— F1 兩張『雙案心智發動鏈對照』自橫列兩欄改為**上下縱向雙卡**。

裁決：否決橫頁，亦不容 6.91pt／8.9pt 之細字存於冊上。
治法：不手排——由產生器依既有之欄內容重鑄（**舊字一律自原柵析出，不重打一宇**）。
      框之寬・分隔・齊右之白，俱由 `dw()` 算出；一行逾寬即擲。

同一柵內先出上卡（第一位），空一行，再出下卡（第二位）⇒ 圍欄段數不動（pairfence 之口徑）。
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

BOOK = next(os.path.join(ROOT, x) for x in os.listdir(ROOT)
            if x.startswith(u"起心動念") and x.endswith(u".txt"))
BK = os.path.join(ROOT, "_archive", u"備份", u"AI清理前", os.path.basename(BOOK) + ".pre_a15d")
LF, CRLF = chr(10), chr(13) + chr(10)
BAR, DASH = chr(0x2502), chr(0x2500)                  # │ ─
TL, TR, BL, BR = chr(0x250c), chr(0x2510), chr(0x2514), chr(0x2518)   # ┌┐└┘
ML, MR, TT, BB, CROSS = chr(0x251c), chr(0x2524), chr(0x252c), chr(0x2534), chr(0x253c)  # ├┤┬┴┼
TW = 80                                            # 一行之總格寬（全形 2・半形 1）
CELL = TW - 4                                      # 兩柵之間可排之格


def dw(s):
    return sum(2 if ord(c) > 0x2000 else 1 for c in s)


def _dash(n):
    return DASH * n


def _horiz(a, b, c):
    """橫線：a ─×k  b(可無)  ─×m  c ⇒ 恰合 TW。全形符一枚 2 格，故 k+m(+1) = CELL//2。"""
    k = CELL // 2 - 1
    if b:
        return a + _dash(k // 2) + b + _dash(k - k // 2) + c
    return a + _dash(k + 1) + c


def wrap(text, lim):
    """依『格』折行：先於讀點處斷；斷後仍逾者硬斷。引號・括號不拆（只於點處求斷）。"""
    out, cur = [], u""
    for ch in text:
        if cur and dw(cur + ch) > lim:
            k = max(cur.rfind(chr(0x3001)), cur.rfind(chr(0xFF0C)),
                    cur.rfind(chr(0xFF1A)), cur.rfind(chr(0x3002)), cur.rfind(chr(0x300D)))
            if k > 4 and dw(cur[k + 1:] + ch) <= lim:
                out.append(cur[:k + 1])
                cur = cur[k + 1:] + ch
            else:
                out.append(cur)
                cur = ch
        else:
            cur += ch
    if cur:
        out.append(cur)
    return [x for x in out if x.strip()]


def row(text):
    t = text.rstrip()
    if dw(t) > CELL - 2:
        raise SystemExit(u"一行逾框（%d > %d）➔%s" % (dw(t), CELL - 2, t[:30]))
    return BAR + u" " + t + u" " * (CELL - 1 - dw(t)) + BAR


def title_row(text):
    t = u"【" + text.strip(u"【】") + u"】"
    lead = max(1, (CELL - dw(t)) // 2)
    return BAR + u" " * lead + t + u" " * (CELL - lead - dw(t)) + BAR


def top():
    return _horiz(TL, None, TR)


def rule():
    return _horiz(ML, None, MR)


def bot():
    return _horiz(BL, None, BR)


def card(caption, groups):
    """caption：框外之題（獨一行，作配對之鍵）；groups：[[行…],…]——空組不生橫隔。
    卡內之第一格取首組之首行（原欄首題），其餘分行排入。"""
    lines = [caption, top()]
    first = True
    for g in groups:
        g = [x for x in g if x.strip()]
        if not g:
            continue
        lines.append(rule())
        for t in g:
            for w_ in wrap(t, CELL - 4):
                lines.append(row(w_))
        first = False
    lines.append(bot())
    for x in lines[1:]:                              # 框行之等寬自證（caption 除外）
        if dw(x) != TW:
            raise SystemExit(u"框行不等寬（%d≠%d）➔%s" % (dw(x), TW, x[:44]))
    if dw(caption) > TW:
        raise SystemExit(u"caption 逾框寬 ➔ %s" % caption[:40])
    return lines


def split_cols(body):
    """依位置取兩欄：parts[1]＝左、parts[-2]＝右。留白之格不棄其鄰格之文。"""
    left, right = [], []
    for l in body:
        if l.count(BAR) < 3:
            continue
        parts = l.split(BAR)
        if len(parts) < 4:
            continue
        a, b = parts[1].strip(), parts[-2].strip()
        if not a and not b:
            continue
        if set(a) <= set(DASH) and set(b) <= set(DASH):
            continue
        if a and set(a) - set(DASH):
            left.append(a)
        if b and set(b) - set(DASH):
            right.append(b)
    return left, right


def cells_of(body):
    """舊柵之全部文字格（比遺失之用）。"""
    out = []
    for l in body:
        if l.count(BAR) < 3:
            continue
        parts = l.split(BAR)
        if len(parts) < 4:
            continue
        for x in (parts[1], parts[-2]):
            x = x.strip()
            if x and set(x) - set(DASH):
                out.append(re.sub(u"\\s+", u"", x))
    return out


def collect(L):
    """找出所有『雙欄對照柵』，回 [(lo, hi, 新行之全部内容)]（不改檔）。"""
    op = [k for k, l in enumerate(L) if re.match(r"^\s*```", l)]
    jobs = []
    for k in range(0, len(op) - 1, 2):
        lo, hi = op[k], op[k + 1]
        body = L[lo + 1:hi]
        if not (len(body) > 4 and u"發動鏈對照" in body[1] and
                max(x.count(BAR) for x in body) >= 3):
            continue
        fig = body[1].replace(chr(0x3010),u"").replace(chr(0x3011),u"").replace(BAR,u"").replace(u" ",u"").strip()
        print(u"  ── 柵 L%d–L%d・%d 行・圖名『%s』（舊格寬 %d）"
              % (lo + 1, hi + 1, len(body), fig[:22], max(dw(x) for x in body)))
        left, right = split_cols(body)
        if len(left) < 3 or len(right) < 3:
            raise SystemExit(u"兩欄之文太少（%d／%d）——形制與料不合" % (len(left), len(right)))
        cols = []
        for n, (grp, tag) in enumerate(((left, u"上卡"), (right, u"下卡"))):
            rows = [x for x in grp if x and set(x) != set(DASH)]
            cut = len(rows)
            for x in (u"佛問", u"裁決"):          # 判決之組自『佛問』起（字樣取原柵，不重打）
                idx = [m for m, t in enumerate(rows) if x in t]
                if idx:
                    cut = min(cut, idx[0])
                    break
            cap = (u"【" + fig + u"】･" + tag + u"：" + rows[0].strip(u"【】"))
            cols.append(card(cap, [rows[1:cut], rows[cut:]]))
        seg = cols[0] + [u"```", u"", u"```text"] + cols[1]  # 兩卡各自成段：同段則 69 行必破鎖頁高閾，又成細字
        keep = re.sub(u"\\s+", u"", u"".join(seg))
        gone = [x for x in cells_of(body) if x and x not in keep and x.strip(u"【】") not in keep]
        if gone:
            raise SystemExit(u"舊字有失落者（一分不可丟）：%s" % u"、".join(g[:26] for g in gone[:4]))
        mx = max(dw(x) for x in seg)
        print(u"     析出：左 %d 行／右 %d 行・重鑄 %d 行・最大格寬 %d"
              % (len(left), len(right), len(seg), mx))
        if mx > 92:
            raise SystemExit(u"重鑄之柵仍逾寬（%d 格）——須縮框內" % mx)
        for m, l in enumerate(seg, 1):
            h = pairsimp.hits(l)
            if h:
                raise SystemExit(u"簡形 ➔ 新柵第 %d 行「%s」" % (m, h))
        if fig not in u"".join(seg):
            raise SystemExit(u"圖名已失（不容把圖之名銷掉）：%s" % fig[:16])
        jobs.append((lo + 1, hi, seg))
    return jobs


def main():
    go = "--write" in sys.argv
    before = io.open(BOOK, "rb").read().decode("utf-8-sig")
    sha = hashlib.sha256(before.encode("utf-8")).hexdigest()[:12]
    L = before.replace(CRLF, LF).split(LF)
    nl = CRLF if CRLF in before else LF
    print(u"F1 %s・%d 行・SHA %s" % (os.path.basename(BOOK)[:14], len(L), sha))
    jobs = collect(L)
    if not jobs:
        print(u"  ・未見舊形之兩欄對照柵（俱已重鑄）・不落盤")
        return 0
    for lo, hi, seg in reversed(jobs):                   # 自後而前：前圖之增行不亂後圖之座標
        L[lo:hi] = seg
    out = nl.join(L).encode("utf-8")
    print(u"  合計重鑄 %d 圖・行 %d ➔ %d" % (len(jobs), len(before.replace(CRLF, LF).split(LF)), len(L)))
    if not go:
        print(u"（試跑・加 --write 始落盤）")
        return 0
    if not os.path.isdir(os.path.dirname(BK)):
        os.makedirs(os.path.dirname(BK))
    io.open(BK, "wb").write(before.encode("utf-8"))
    io.open(BOOK, "wb").write(out)
    chk = io.open(BOOK, "rb").read().decode("utf-8")
    if chk.count(chr(13)) != chk.count(chr(10)):
        raise SystemExit(u"行尾混雜")
    print(u"  落盤：%d 行・%d B・SHA %s ➔ %s・備 %s"
          % (len(L), len(out), sha, hashlib.sha256(out).hexdigest()[:12],
             os.path.relpath(BK, ROOT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
