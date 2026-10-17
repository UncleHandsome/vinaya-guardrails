# -*- coding: utf-8 -*-
"""第 94 輪乙探針：印面之「自指編纂語」與「假想敵句」——真咬文嚼字所在。

自指：書中談自己如何校、如何查、如何隨動（讀者不需）；
假想敵：為防某日某人挑刺而先自辯（免…疑／來日／後世校計／或議／以免被指）。
誠實標記（本地無從覆核、屬義理推定）屬必須保留者，本軸只列其字數過長之例。
"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk

LINES = _tk.DOC.split("\n")
DROP = ["修訂誌", "跨章款級索引", "十維驗收", "全書校勘記", "全書竣工呈辭"]
in_drop, zone, marks = False, "卷首", []
for l in LINES:
    m = None
    if l.startswith("# "):
        in_drop = any(d in l for d in DROP)
        m = re.match(r"# (第[一二三四五六七八九]章|附錄[A-M]|結語|終卷)", l)
        zone = m.group(1) if m else l[2:12]
    marks.append((zone, in_drop))

SELFS = ["本書", "全書", "此處不復", "不復列", "不復錄", "隨動", "本輪", "歷輪", "校勘", "查核",
         "覆核", "實測", "自算", "印面", "底冊", "逐字比對", "口徑"]
ENEMY = ["免", "來日", "後世", "或議", "疑其", "恐", "挑", "辯駁", "無從置辯", "杜其口實",
         "免致日後", "日後有人", "以免", "以防"]
LONGPAR = re.compile(r"（[^（）]{46,}）")

out = ["##### 一、自指編纂語（印面）#####"]
tot = 0
for k in SELFS:
    hits = [(i + 1, LINES[i]) for i in range(len(LINES)) if not marks[i][1] and k in LINES[i]]
    if not hits:
        continue
    tot += len(hits)
    z = {}
    for ln, l in hits:
        z[marks[ln - 1][0]] = z.get(marks[ln - 1][0], 0) + 1
    out.append("  %-6s %3d 行｜%s" % (k, len(hits), z))
out.append("  —— 計 %d 行次 ——" % tot)

out.append("\n##### 二、假想敵句（印面，取「免／恐／來日／辯」等作自辯之語）#####")
pat = re.compile(r"[；。，、]?[^。\n]{0,26}(?:免|以免|以免日後|恐|來日|後世|防有|或議|無從置辯|杜其口實)"
                r"[^。\n]{0,40}")
seen = 0
for i in range(len(LINES)):
    if marks[i][1]:
        continue
    for m in pat.finditer(LINES[i]):
        seg = m.group(0)
        if not re.search(r"免|恐|來日|後世|防有|或議|杜其口實", seg):
            continue
        if re.search(r"難免|未免|避免|免費|免供|免別住|不免|免死|赦免|免罪|免責|開緣|免布薩|免結罪", seg):
            continue
        seen += 1
        if seen <= 26:
            out.append("  L%-6d %-10s …%s…" % (i + 1, marks[i + 1 - 1][0], seg[:76]))
out.append("  —— 計 %d 筆 ——" % seen)

out.append("\n##### 三、超長括注（46 字以上，印面前 22 例）#####")
n = 0
for i in range(len(LINES)):
    if marks[i][1] or LINES[i].startswith("|"):
        continue
    for m in LONGPAR.finditer(LINES[i]):
        n += 1
        if n <= 22:
            out.append("  L%-6d %-10s len%3d %s" % (i + 1, marks[i][0], len(m.group(0)), m.group(0)[:70]))
out.append("  —— 計 %d 處 ——" % n)
io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "r94b.txt"),
        "w", encoding="utf-8").write("\n".join(out) + "\n")
sys.stdout.write("ok\n")
