# -*- coding: utf-8 -*-
"""第 56 輪附七・重排第四章『結戒十句義』五維矩陣之圍欄圖（段 3，源 L1143-1155）。

病（印面 p39 親目＋格寬實測）：一段之內四種寬——頂框 57・題列 82・項列 70・底框 73；
  故頂框只蓋到第二欄、題列之│與項列之│不同位、底框又溢出。此即第 245 輪『格寬模型須與
  印面同源』之同族病：以字数目測補空，必散。
治：立一格線重建——欄寬 26 格（足容【第X維度：○○○○】22 格＋左右各 2）、三欄兩隔，
  全幅 82 格（印面字級 ≈ 505/(0.55×82) ≈ 11.2pt，高於 9pt 地板）；頂框於欄界作 ┬、
  主幹落第二欄欄心（第 40 格）作 ┴；底框鏡之而主幹作 ┬（向下出箭）。
自證：逐行以 `build_hulan.cw_units` 量格寬，全幅等寬＋│/┬/┴/└/┘ 位置逐欄對齊，
  不合即擲回不寫檔。
用法：python -X utf8 _work/hlfence56.py [--go]
"""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "_print"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import hulan_path as HP  # noqa: E402
from build_hulan import cw_units  # noqa: E402  格寬模型與印面同源（寬字 2 格、框線 1 格）

CELL = 26                     # 欄寬（格）
AX = 40                       # 主幹所在格（第二欄欄心）


def cell(text):
    """填一欄：左右各留 2 格，不足補至 CELL。"""
    body = u"  " + text
    pad = CELL - cw_units(body)
    if pad < 2:
        raise SystemExit(u"欄內容過長（須 ≤ %d 格）：%s" % (CELL - 4, text))
    return body + u" " * pad


def edge(left, mid_l, mid_r, right, axis):
    """橫框：欄界作 ┬/┴，主幹落 AX。"""
    s = left + u"─" * CELL + mid_l
    s += u"─" * (AX - (CELL + 1) - 1) + axis
    s += u"─" * (CELL + 1 - (AX - (CELL + 1)) - 1) + mid_r
    s += u"─" * CELL + right
    return s


def row(a, b, c):
    return u"│" + cell(a) + u"│" + cell(b) + u"│" + cell(c) + u"│"


def center(s):
    """置中於全幅（格寬口徑與印面同源，不可按字數乘 2——⑩ 之類只占一格）。"""
    wbox = cw_units(row(u"", u"", u""))
    return u" " * max(0, (wbox - cw_units(s)) // 2) + s


TOP = edge(u"┌", u"┬", u"┬", u"┐", u"┴")
BOT = edge(u"└", u"┴", u"┴", u"┘", u"┬")
ARROW = u" " * AX + u"↑"
NEW = [
    center(u"【第五維度：終極歷史使命】"),
    center(u"⑩ 正法得久住（精神永續）"),
    ARROW,
    TOP,
    row(u"【第一維度：組織運作】", u"【第二維度：社會認同】", u"【第三維度：司法公正】"),
    row(u"① 攝取於僧", u"④ 未信者令信", u"⑥ 難調者令調順"),
    row(u"② 令僧歡喜", u"⑤ 已信者令增長", u"⑦ 慚愧者得安樂"),
    row(u"③ 令僧安樂", u"", u""),
    BOT,
    ARROW,
    center(u"【第四維度：個人出世解脫】"),
    center(u"⑧ 斷現在有漏（當下防非）"),
    center(u"⑨ 斷未來有漏（永斷輪迴）"),
]

def gcols(l, ch):
    """字元 ch 在『格』刻度上的位置（字元序 ≠ 格序：CJK 占兩格）。"""
    out, g = [], 0
    for c in l:
        if c == ch:
            out.append(g)
        g += 2 if ord(c) > 0x2E80 else 1
    return out


# ── 自證：等寬・欄界對齊・主幹落格 ──────────────────────────────────
W = [cw_units(l) for l in NEW]
box = [i for i, l in enumerate(NEW) if l and l[0] in u"┌└│"]
wbox = max(W[i] for i in box)
for i in box:
    if W[i] != wbox:
        raise SystemExit(u"框內各行寬不等：第 %d 行 %d 格 ≠ %d 格" % (i, W[i], wbox))
GRID = [0, CELL + 1, 2 * CELL + 2, wbox - 1]
for i, l in enumerate(NEW):
    if l.startswith(u"│"):
        pos = gcols(l, u"│")
        if pos != GRID:
            raise SystemExit(u"欄界未對齊（第 %d 行）：%s ≠ %s" % (i, pos, GRID))
for tag in (TOP, BOT):
    nodes = sorted(sum(2 if ord(c) > 0x2E80 else 1 for c in tag[:k])
                   for k, c in enumerate(tag) if c in u"┬┴")
    if nodes != sorted(GRID[1:3] + [AX]):
        raise SystemExit(u"橫框節點錯位：%s ≠ %s｜%s" % (nodes, sorted(GRID[1:3] + [AX]), tag))
print(u"全幅 %d 格（原 57/82/70/73 四種）｜印面字級估 %.1fpt｜行 %d" % (wbox, 505.0 / (0.55 * wbox), len(NEW)))
for l in NEW:
    print(u"  %3d|%s|" % (cw_units(l), l))

raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
lines = raw.split(u"\r\n")
a, b = 1143, 1155                      # 源內圍欄內容行（含）
if not (lines[a - 1].startswith(u"                    【第五維度") and lines[b - 1].strip() == u"⑨ 斷未來有漏（永斷輪迴）"):
    raise SystemExit(u"段界定位失敗：L%d/L%d 非預期之形" % (a, b))
if b - a + 1 != 13 or len(NEW) != 13:
    raise SystemExit(u"行數不等（源 %d／新 %d）" % (b - a + 1, len(NEW)))
out = lines[:a - 1] + NEW + lines[b:]
if len(out) != len(lines):
    raise SystemExit(u"行數變形")
if u"\r\n".join(out).count(u"\r\n") != raw.count(u"\r\n"):
    raise SystemExit(u"CRLF 變形")
print(u"源 L%d-%d（%d 行）→ 新 %d 行｜字 %+d" % (a, b, b - a + 1, len(NEW),
                                                len(u"\r\n".join(out)) - len(raw)))
if u"--go" not in sys.argv[1:]:
    print(u"（覆核模式，未寫檔；加 --go 即入刀）")
    raise SystemExit(0)
bak = HP.SRC + u".bak56f"
if not os.path.exists(bak):
    io.open(bak, "w", encoding="utf-8", newline="").write(raw)
io.open(HP.SRC, "w", encoding="utf-8", newline="").write(u"\r\n".join(out))
chk = io.open(HP.SRC, encoding="utf-8", newline="").read()
print(u"已入刀：SHA %s｜備份 %s" % (hashlib.sha256(chk.encode("utf-8")).hexdigest()[:16],
                                    os.path.basename(bak)))
