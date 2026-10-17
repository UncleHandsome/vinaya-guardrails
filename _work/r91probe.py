# -*- coding: utf-8 -*-
"""第三份外部報告逐條查證：所引文字是否仍在書中、在何處、其前後文如何。"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk

LINES = _tk.DOC.split("\n")
DROP = [u"修訂誌", u"跨章款級索引", u"十維驗收", u"全書校勘記", u"全書竣工呈辭"]
in_drop, zone = False, u"卷首"
CHAP = re.compile(r"^# (第[一二三四五六七八九]章|附錄[A-M]|結語|終卷)")

KEYS = [
    u"台帳者，一致之驗", u"處斷多點一號", u"改一處必隨", u"計數口徑", u"母數不同",
    u"免來日校計者", u"林下留白觀", u"空白格之如實", u"通道之名", u"階者粗細之階",
    u"不掛逐字引文", u"逐名語料頻次", u"診斷詞彙封存令", u"妄作異語", u"自然人心證",
    u"Forms Sunset", u"Meeting Minimization", u"Simplicity Over", u"Peer Review",
    u"One-Stop", u"以丁廢甲", u"以丙代甲", u"以乙代甲", u"常式六", u"複合態",
    u"字心髓", u"字樞紐", u"字錨點", u"四項中三項", u"見罪自肯", u"非法足數",
    u"骨牌式", u"提貨券契", u"斷彼心", u"剛性負面清單", u"三禁", u"拉布",
    u"自然變根", u"半月摩那埵", u"教唆撤回", u"另結", u"覆藏日數",
]
out = [u"##### 第三份報告所引 44 事之查證 #####"]
for k in KEYS:
    hits = [(i + 1, l) for i, l in enumerate(LINES) if k in l]
    zn = {}
    cur = u"卷首"
    for i, l in enumerate(LINES):
        m = CHAP.match(l)
        if m:
            cur = m.group(1)
        if l.startswith("# ") and any(d in l for d in DROP):
            cur = u"底冊"
        if i + 1 in [h[0] for h in hits]:
            zn[cur] = zn.get(cur, 0) + 1
    out.append(u"%-16s 全書 %2d 見｜%s" % (k, len(hits), zn if hits else u"0（書中無此語）"))
    for ln, l in hits[:3]:
        j = l.find(k)
        out.append(u"        L%-6d …%s…" % (ln, l[max(0, j - 40):j + len(k) + 40]))
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "r91probe.txt"),
        "w", encoding="utf-8").write("\n".join(out) + "\n")
sys.stdout.write("keys %d\n" % len(KEYS))
