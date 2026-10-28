# -*- coding: utf-8 -*-
"""第 56 輪之兩刀（外路『弘一題詞三問題』查證後）：護欄正本 L633／L6160 之章首題詞。

甲·執理廢事 → 執事昧理：此句之主語是『不知制意而持戒』之病（死執事相），
    『執理廢事』恰為其反義（執理而廢事相，即本書第一章第二節所判之『空泛心性論』），
    一句之中兩病相殺，是義理硬傷。全書此詞唯此兩見，別無『執事昧理』。
乙·削《律學要略》之書名：凡例款②自約『標「大意」者，出其書之旨，非其書之句』，
    而該講記之傳世大纲（戒律傳入因緣・南山源流・三皈五戒八戒乃至菩薩戒之義）無『制意』之旨，
    故書名之掛為虛宣。改標『弘一大師論學戒之旨（本書撮其大意）』——去其未證之書名，
    留其人之旨，且『大意』二字仍是凡例所許之標記（庚軸與 sigchk 之口徑不動）。

護三道：先備份並記 SHA；兩靶各斷命中數＝2（此題詞於第一・十七章各重出一遍，同改）；
        寫檔 newline='' 保 CRLF 並斷 CR＝LF＝行數；回讀斷舊形殘留＝0。
用法：python -X utf8 _work/hlfix56.py          # 只量不改（印命中）
      python -X utf8 _work/hlfix56.py --go     # 入刀
"""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import hulan_path as HP                                        # noqa: E402

CUTS = [
    (u"執理廢事", u"執事昧理", 2),
    (u"弘一大師《律學要略》之大意", u"弘一大師論學戒之旨（本書撮其大意）", 2),
]
GO = "--go" in sys.argv[1:]
raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()
n_cr = raw.count("\r\n")
lines = raw.split("\r\n")
print(u"正本：%s" % os.path.basename(HP.SRC))
print(u"起點 SHA %s｜%d 行｜CRLF %d" % (sha0[:16], len(lines), n_cr))

hit_rows = []
for old, new, want in CUTS:
    idx = [i for i, l in enumerate(lines) if old in l]
    print(u"靶『%s』命中 %d 行（須 %d）：%s"
          % (old, len(idx), want, u"、".join(u"L%d" % (i + 1) for i in idx)))
    if len(idx) != want:
        raise SystemExit(u"命中數不合，未動一字。")
    for i in idx:
        if new in lines[i]:
            raise SystemExit(u"新形已在 L%d——疑已入刀，中止。" % (i + 1))
        hit_rows.append((i, old, new))

for i, old, new in hit_rows:
    lines[i] = lines[i].replace(old, new)
out = "\r\n".join(lines)
print(u"刀後：行 %d（原 %d）｜CRLF %d（原 %d）｜字 %d（原 %d）"
      % (len(lines), len(raw.split("\r\n")), out.count("\r\n"), n_cr,
         len(out), len(raw)))
if len(out.split("\r\n")) != len(lines) or out.count("\r\n") != n_cr:
    raise SystemExit(u"行數或換行不合，未寫檔。")
for old, _new, _w in CUTS:
    if old in out:
        raise SystemExit(u"舊形殘留：%s" % old)
if not GO:
    print(u"（覆核模式，未寫檔；加 --go 即入刀）")
    raise SystemExit(0)

bak = HP.SRC + u".bak56"
if not os.path.exists(bak):
    io.open(bak, "w", encoding="utf-8", newline="").write(raw)
io.open(HP.SRC, "w", encoding="utf-8", newline="").write(out)
chk = io.open(HP.SRC, encoding="utf-8", newline="").read()
sha1 = hashlib.sha256(chk.encode("utf-8")).hexdigest()
print(u"已入刀：SHA %s｜備份 %s" % (sha1[:16], os.path.basename(bak)))
print(u"回讀：執理廢事 %d・執事昧理 %d・《律學要略》 %d・論學戒之旨 %d"
      % (chk.count(u"執理廢事"), chk.count(u"執事昧理"),
         chk.count(u"《律學要略》"), chk.count(u"論學戒之旨")))
