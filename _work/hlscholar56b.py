# -*- coding: utf-8 -*-
"""第 56 輪・學術嚴謹版第二刀（續 hlscholar56）：餘下四处仍作『粗體＋引號』之非律文引語。

款①自約『引號與粗體相合者＝漢譯《四分律》原句』，故凡他典・他師・本書之概括，
  皆須改作〔本書括旨〕之形（不掛引號、不加粗體）——否則形制即為不實之宣稱。
  此四處之外，其餘 `**「…」**` 俱屬《四分律》（過語料閘）或本書評語（款①判別句所容）。
用法：python -X utf8 _work/hlscholar56b.py [--go]
"""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import hulan_path as HP  # noqa: E402

T = u"〔本書括旨〕"
D = u"**"
Q = chr(0x300c) + u"學戒者，先須明其制意。若不知佛陀何以制此戒，則持戒流於形骸，執事昧理，終無實益。" + chr(0x300d)
CUTS = [
    (D + Q + D, T + Q[1:-1], 2),                       # 第一・十七章題詞（弘一之旨，本書撮）
    (D + chr(0x300c) + u"女子幼年從父，青年從夫，夫死從子，女子不得享有自主。" + chr(0x300d) + D,
     T + u"女子幼年從父，青年從夫，夫死從子，女子不得享有自主。", 1),   # 《摩奴法典》通說
    (D + chr(0x300c) + u"自今已後，微細戒可捨。" + chr(0x300d) + D,
     T + u"自今已後，微細戒可捨。", 1),                                  # 南傳《大般涅槃經》
]
GO = u"--go" in sys.argv[1:]
raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
n_cr = raw.count(u"\r\n")
print(u"起點 SHA %s｜%d 字｜CRLF %d" % (hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16],
                                        len(raw), n_cr))
for i, (old, new, want) in enumerate(CUTS, 1):
    got = raw.count(old)
    if got != want:
        raise SystemExit(u"靶 %d 命中 %d（須 %d），未動一字：%s" % (i, got, want, old[:30]))
    raw = raw.replace(old, new)
    print(u"刀%d｜命中 %d ✓｜%s" % (i, want, old[:34]))
if raw.count(u"\r\n") != n_cr:
    raise SystemExit(u"CRLF 變形，未寫檔。")
print(u"字 %d → %d（%+d）" % (len(io.open(HP.SRC, encoding='utf-8', newline='').read()),
                                len(raw), len(raw) - len(io.open(HP.SRC, encoding='utf-8', newline='').read())))
if not GO:
    print(u"（覆核模式，未寫檔）")
    raise SystemExit(0)
io.open(HP.SRC, "w", encoding="utf-8", newline="").write(raw)
chk = io.open(HP.SRC, encoding="utf-8", newline="").read()
print(u"已入刀：SHA %s｜〔本書括旨〕今 %d 處" % (
    hashlib.sha256(chk.encode("utf-8")).hexdigest()[:16], chk.count(T)))
