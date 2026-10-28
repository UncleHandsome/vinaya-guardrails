# -*- coding: utf-8 -*-
"""第十波・字數之宣稱歸實：兩冊漢字今測 207,427（F1 84,871＋F2 122,556）➔『近二十萬言』改『二十餘萬言』。

用法：python -X utf8 _work/pairwords.py [--write]
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import pairsimp as PS  # noqa: E402

W = "--write" in sys.argv
EDITS = [
    ("起心動念：四分律的心智顯微鏡與唯識解剖.txt", [
        ("> 走過近二十萬言的微觀推演，行者在此刻必須明白：",
         "> 走過二十餘萬言的微觀推演，行者在此刻必須明白："),
        ("翻過近二十萬言的推演，走過上百則案卷的驚濤駭浪，毘奈耶的心靈公堂在此徹底落鎖。",
         "翻過二十餘萬言的推演，走過上百則案卷的驚濤駭浪，毘奈耶的心靈公堂在此徹底落鎖。"),
        ("> 若問兩冊都計近二十萬言、六重心智門、八大正理尺，壓縮到自性源頭，究竟要交付行者哪一個字？",
         "> 若問兩冊都計二十餘萬言、六重心智門、八大正理尺，壓縮到自性源頭，究竟要交付行者哪一個字？"),
    ]),
]

for fname, rules in EDITS:
    p = ROOT / fname
    raw = p.read_bytes().decode("utf-8-sig")
    nl = "\r\n" if "\r\n" in raw else "\n"
    lines = raw.replace("\r\n", "\n").split("\n")
    print("■", fname[:12])
    for old, new in rules:
        k = [i for i, l in enumerate(lines) if l.strip() == old]
        if len(k) != 1:
            if len(k) == 0 and any(l.strip() == new for l in lines):
                print("   已改（重入之護）：%s…" % new[:16])
                continue
            raise SystemExit("錨非唯一：%r → %d 處" % (old[:20], len(k)))
        if PS.flag(new):
            raise SystemExit("簡形閘攔下：『%s』" % PS.hits(new))
        lines[k[0]] = new
        print("   歸實 L%d" % (k[0] + 1))
    other = (ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt" if fname.startswith("起")
             else ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt")
    han_this = len(re.findall(r"[一-鿿]", nl.join(lines)))
    han_other = len(re.findall(r"[一-鿿]", other.read_bytes().decode("utf-8-sig")))
    print("   改後本冊漢字 %d・姊妹冊（今檔）%d・兩冊合 %d ➔ 宣稱『二十餘萬言』%s"
          % (han_this, han_other, han_this + han_other,
             "如實 ✓" if 200000 <= han_this + han_other < 250000 else "★不合，須另立其數"))
    if not W:
        print("   （試跑：未落盤）")
        continue
    bak = ROOT / "_archive/備份/AI清理前" / (fname + ".pre_words")
    bak.write_bytes(raw.encode("utf-8"))
    body = nl.join(lines).encode("utf-8")
    p.write_bytes(body)
    print("   落盤：SHA %s ➔ %s" % (hashlib.sha256(raw.encode()).hexdigest()[:12],
                                     hashlib.sha256(body).hexdigest()[:12]))
