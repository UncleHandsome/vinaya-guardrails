# -*- coding: utf-8 -*-
"""第 56 輪附六・正文之『括某書之旨』與時代錯亂詞（外路第五報查證後之存留者）。

今檔實測：『未及逐覆』0・『〔本書括旨〕』0・凡例款②已改——該報第一、五類所指者上午已淨空（彼據舊冊）。
真正還活著的兩類，本刀處理：
  甲·正文四處『本書括《資持記》／《行事鈔》之旨』——此仍是對該書內容的未證宣稱（本地無此二書，
     庚軸只能列『須人工核』）。改約：不稱『括其書之旨』，只稱『本書效古德語氣自為之文，
     非其書之文』——把宣稱從『內容對應』降為『語氣仿作』，後者可驗，前者不可驗。
  乙·兩處時代錯亂之詞：『立大憲典』（憲法義乃近世譯名）、『外納公議』（議會義乃近世語）——
     今雖已不掛道宣之名，語仍歸之如來與二部僧，故換律家語：綱紀／事必白眾（四字對四字，版面不動）。
另：篇目之爭已定——《行事鈔》〈結界方法篇〉是**第六**（第三乃〈足數眾相篇〉），外路此條亦誤。
用法：python -X utf8 _work/hlbody56.py [--go]
"""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import hulan_path as HP  # noqa: E402

CUTS = [
    (u"元照律師在《資持記》中辨明遮性相依之義，本書括其旨曰：",
     u"遮性相依之義，南山律門所同判；此十六字乃本書自為之語：", 1),
    (u"元照律師在《資持記》中悲痛地斥末世輕忽微細之弊，本書括其旨曰（『護城河』之喻是本書語，"
     u"此處但取其意）：",
     u"斥末世輕忽微細之弊，律門同聲；此段乃本書效古德語氣自為之文（『護城河』之喻亦是本書語）：", 1),
    (u"道宣律師痛斥那些輕視小戒的義學僧人；以下一段乃本書括《行事鈔》之旨，非其逐字：",
     u"輕視小戒之弊，南山律門歷代同憂；以下一段乃本書效古德語氣自為之文，非《行事鈔》之文：", 1),
    (u"元照律師在《資持記》卷首發出了獅子吼（以下乃本書括其旨，非逐字）：",
     u"律門呵斥撥無因果之弊，向作獅子吼觀（以下一段乃本書效古德語氣自為之文，非《資持記》之文）：", 1),
    (u"立大憲典以衛清規", u"立大綱紀以衛清規", 1),
    (u"折伏傲慢，外納公議", u"折伏傲慢，事必白眾", 1),
]
GO = u"--go" in sys.argv[1:]
raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
c0 = raw.count(u"\r\n")
print(u"起點 SHA %s｜%d 字｜CRLF %d" % (hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16],
                                        len(raw), c0))
for i, (old, new, want) in enumerate(CUTS, 1):
    g = raw.count(old)
    if g != want:
        raise SystemExit(u"靶 %d 命中 %d（須 %d）：%s" % (i, g, want, old[:28]))
    if len(new) != len(old) and i >= 5:
        raise SystemExit(u"靶 %d 字數不等（形制須四字對四字）" % i)
    raw = raw.replace(old, new)
    print(u"刀%d｜命中 %d ✓｜%s" % (i, want, old[:26]))
if raw.count(u"\r\n") != c0:
    raise SystemExit(u"CRLF 變形")
for k in (u"括其旨", u"本書括《", u"未及逐覆", u"憲典", u"公議"):
    if k in raw:
        raise SystemExit(u"殘留：%s（%d 處）" % (k, raw.count(k)))
print(u"終檢：括旨 0・未及逐覆 0・憲典 0・公議 0｜字 %+d"
      % (len(raw) - len(io.open(HP.SRC, encoding='utf-8', newline='').read())))
if not GO:
    print(u"（覆核模式，未寫檔；加 --go 即入刀）")
    raise SystemExit(0)
bak = HP.SRC + u".bak56e"
if not os.path.exists(bak):
    io.open(bak, "w", encoding="utf-8", newline="").write(
        io.open(HP.SRC, encoding="utf-8", newline="").read())
io.open(HP.SRC, "w", encoding="utf-8", newline="").write(raw)
print(u"已入刀：SHA %s" % hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16])
