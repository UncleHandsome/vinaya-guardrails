# -*- coding: utf-8 -*-
"""第十波・附刀：『二百五十六案』之虛數歸實（心法卷三處）。

量得：本地語料無從立此數——《四分律》比丘戒本通數二百五十（八・十七・三十・九十二・四・百），
      『汝以何心』凡 96 見，兩冊案卷合 130 則（F1 28＋F2 102），俱不得 256 之數；
      而『九十二』可通（本律波逸提九十二法），故只除 256，不動 92（作者之口徑，非數之誤）。
      又依『枝節之病直接改詞，不鋪案語』之戒，三處俱以等寬之詞替之（圍欄內之幅分毫不移）。

用法：python -X utf8 _work/pairwords2.py [--write]
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import pairsimp as PS  # noqa: E402

W = "--write" in sys.argv
F1 = ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt"
EDITS = [
    ("【逕依事相劃線（256 案）】", "【逕依事相劃線（不待問）】"),
    ("#### 一、事相確鑿、結果不可逆之案（逕依事相劃線之 256 案）",
     "#### 一、事相確鑿、結果不可逆之案（逕依事相劃線者）"),
    ("九十二次之垂問乃「言詞問」，二百五十六案之逕判乃「證據問」。",
     "九十二次之垂問乃「言詞問」，不待口供而逕依事相者乃「證據問」。"),
]


def dw(s):
    """表示幅：全形（含框線・假名・漢字）計 2，半形計 1。"""
    return sum(2 if ord(c) > 0x2E7F or 0x3000 <= ord(c) <= 0x303F or 0xFF00 <= ord(c) else 1
               for c in s)


def fence_mask(ls):
    m, f = [], False
    for l in ls:
        if re.match(r"^\s*```", l):
            f = not f
            m.append(True)
            continue
        m.append(f)
    return m


raw = F1.read_bytes().decode("utf-8-sig")
nl = "\r\n" if "\r\n" in raw else "\n"
lines = raw.replace("\r\n", "\n").split("\n")
mask = fence_mask(lines)
for old, new in EDITS:
    k = [i for i, l in enumerate(lines) if old in l]
    if len(k) == 0:
        if any(new in l for l in lines):
            print("已改（重入之護）：%s…" % new[:14])
            continue
        raise SystemExit("靶不可求：%r" % old[:24])
    if len(k) > 1:
        raise SystemExit("靶歧：%r → %d 處" % (old[:24], len(k)))
    if mask[k[0]] and dw(old) != dw(new):
        # 等寬之護唯圍欄內須守（框線圖以空格對欄）；散文與標題不在此約
        raise SystemExit("等寬之護破產（圍欄內）：%d ≠ %d" % (dw(old), dw(new)))
    if PS.flag(new):
        raise SystemExit("簡形閘攔下：『%s』" % PS.hits(new))
    lines[k[0]] = lines[k[0]].replace(old, new)
    print("歸實 L%d・%s（%s幅 %d→%d）" % (k[0] + 1, new[:26],
                                     "圍欄內・等" if mask[k[0]] else "散文・", dw(old), dw(new)))

print("行數 %d ➔ %d" % (len(lines), len(lines)))
if not W:
    print("（試跑：未落盤）")
    raise SystemExit(0)
bak = ROOT / "_archive/備份/AI清理前" / (F1.name + ".pre_words2")
bak.write_bytes(raw.encode("utf-8"))
body = nl.join(lines).encode("utf-8")
F1.write_bytes(body)
with (ROOT / "_work/pairwords2_cuts.txt").open("a", encoding="utf-8") as fh:
    fh.write("%s\t去『二百五十六案』之虛數 3 處（等寬）\t%s\n" % (F1.name, hashlib.sha256(body).hexdigest()[:12]))
print("落盤：%d B・SHA %s ➔ %s" % (len(body), hashlib.sha256(raw.encode()).hexdigest()[:12],
                                   hashlib.sha256(body).hexdigest()[:12]))
