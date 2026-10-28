# -*- coding: utf-8 -*-
"""第十一波・C 段：框架文字之稱名同步（卷首自序・第十六章章末指針・終卷・終局迴向偈）。

A4 已把第四篇之章・節・款題歸純律，而**題名有四抄**（正文／卷首全貌圖／章首解剖句／總目錄）之外，
尚有**框架之文**暗引舊名——此即『名單勿兩抄』之債：題改了而卷首自序與章末指針仍呼舊名，讀者據目錄求之不得。
本刀只動『稱名』，不動論證（正文之比擬與案例名一仍其舊，屬候裁⑤）。

六刀：C1 自序（並解『非營利組織／三線』一句兩見之重出）・C2〜C4 第十六章章末指針三句・
      C5 終卷『吹哨盾牌』➔『反報五盾』（呼第十四章第三節新題）・C6 迴向偈『穿透審計／長照安養』
      ➔『穿透名實／瞻病安養』（七言不動・韻腳『隨』不動）。

用法：python -X utf8 _work/pair11c.py          # 試跑
      python -X utf8 _work/pair11c.py --write  # 落盤（備 .pre_a11c）
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import pairsimp as PS  # noqa: E402

W = "--write" in sys.argv
LF = chr(10)
CRLF = chr(13) + LF
F2 = ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt"

FRAGS = [
    ("本書徹底承接了古老律藏中最具重量的法治遺產，並將其與當代非營利組織治理、內部控制三線模型、體恤受暴之調查、"
     "吹哨人護念之制、寺產名義代持之穿透稽核及非營利組織之三線風控全息會通。",
     "本書徹底承接了古老律藏中最具重量的法治遺產，並將其與當代道場之共議分權、三重護念、受暴非願之問訊、"
     "舉罪五德與庇護見聞疑三根、名實之辨與四種僧物之守護，全息會通。"),
    ("帳冊穿透審計清楚了，土地信託確權了，病寮的熱湯藥端上去了。",
     "帳冊名實辨清了，土地信託確權了，病寮的熱湯藥端上去了。"),
    ("負責經管常住資產與長照醫療的執事長老啊",
     "負責經管常住資產與瞻病照護的執事長老啊"),
    ("我們學會了實質受益人審查，學會了代持信託的三軌確權，學會了長照耗竭的制度防禦，",
     "我們學會了四種僧物之不可分，學會了代持信託之三軌確權，學會了瞻病次第差之防耗竭，"),
    ("四瑕疵一票否決與吹哨盾牌", "四瑕疵一票否決與反報五盾"),
    ("穿透審計守常住，長照安養菩提隨", "穿透名實守常住，瞻病安養菩提隨"),
]


def clean(new, tag):
    if PS.flag(new):
        raise SystemExit("%s 簡形閘攔下：%s 於『%s』" % (tag, PS.hits(new), new[:40]))
    for wd in re.findall(r"[A-Za-z]{2,}", new):
        raise SystemExit("%s 夾英文『%s』於『%s』" % (tag, wd, new[:40]))


def main():
    raw = F2.read_bytes().decode("utf-8-sig")
    nl = CRLF if CRLF in raw else LF
    L = raw.replace(CRLF, LF).split(LF)
    before = len(L)
    for k, (old, new) in enumerate(FRAGS, 1):
        i = [x for x, l in enumerate(L) if l.count(old) == 1]
        if len(i) != 1:
            raise SystemExit("C%d 錨非唯一：%r → %d 行" % (k, old[:20], len(i)))
        clean(new, "C%d" % k)
        L[i[0]] = L[i[0]].replace(old, new)
        print("  C%d 稱名同步於 L%d（%d ➔ %d 字）" % (k, i[0] + 1, len(old), len(new)))
    for w in ("非營利組織", "穿透審計", "實質受益人", "長照醫療", "長照耗竭", "吹哨盾牌"):
        print("  框架殘跡『%s』今 %d 見" % (w, sum(1 for l in L if w in l)))
    bad = [(x + 1, PS.hits(l)) for x, l in enumerate(L) if PS.flag(l)]
    if bad:
        raise SystemExit("簡形閘攔下：%s" % bad[:6])
    print("  行數 %d ➔ %d（應不變）・簡形 0 ✓" % (before, len(L)))
    if len(L) != before:
        raise SystemExit("行數變動，非本刀所許")
    if not W:
        print("  （試跑：未落盤）")
        return
    (ROOT / "_archive/備份/AI清理前" / (F2.name + ".pre_a11c")).write_bytes(raw.encode("utf-8"))
    data = nl.join(L).encode("utf-8")
    F2.write_bytes(data)
    print("  落盤：SHA %s ➔ %s" % (hashlib.sha256(raw.encode()).hexdigest()[:12],
                                    hashlib.sha256(data).hexdigest()[:12]))


if __name__ == "__main__":
    main()
