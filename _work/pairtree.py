# -*- coding: utf-8 -*-
"""生命之樹圖之產生器（卷首・【生命之樹生態全景與心智顯微鏡】）。
手排 ASCII 會隨內容漂：各行長短不一，尾端右欄 `│` 各落其欄，循環線遂斷成數段
（第廿三波實測同一圖有 74/82/86/88/91/94 六種行寬）。故改由本器定位落欄：
    A = 38   樹軸
    R = 72   右欄（循環線）
    兩框 18–58（內寬 38）
用法：python -X utf8 _work/pairtree.py            # 只印
      python -X utf8 _work/pairtree.py --write    # 覆寫正本之該段圍欄
"""
import io
import os
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "起心動念：四分律的心智顯微鏡與唯識解剖.txt")
A, R, BL, IN = 38, 72, 18, 38
WRITE = "--write" in sys.argv


def dw(s):
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def row(t):
    if dw(t) > R - 1:
        raise SystemExit(u"行逾右欄：%d＞%d｜%s" % (dw(t), R - 1, t))
    return t + u" " * (R - dw(t) - 1) + u"│"


def ax(s):
    return u" " * max(0, A - dw(s) // 2) + s


def conn(lab=None):
    return row(u" " * A + u"│" + (u" " + lab if lab else u""))


def box(s):
    w = dw(s)
    if w > IN:
        raise SystemExit(u"框內逾寬：%d＞%d｜%s" % (w, IN, s))
    l = (IN - w) // 2
    return row(u" " * BL + u"│" + u" " * l + s + u" " * (IN - w - l) + u"│")


def bar(l, r, mid):
    return row(u" " * BL + l + mid * IN + r)


def build():
    L = []
    L.append(row(ax(u"【果實：斷現在有漏、斷未來有漏】（正理八·解脫終極歸宿）")))
    L.append(row(u" " * A + u"▲")[:R] + u"（果熟落核）")
    L.append(conn(u"（成熟解脫·無漏清涼）"))
    L.append(bar(u"┌", u"┐", u"─"))
    L.append(box(u"法相之葉（起心動念臨床全息案卷）"))
    L.append(box(u"貪愛換裝 ｜ 瞋恚匕首 ｜ 傲慢重甲"))
    L.append(box(u"差誤盲區 ｜ 慈悲界限"))
    L.append(bar(u"└", u"┘", u"─"))
    L.append(row(u" " * A + u"▲"))
    L.append(row(ax(u"六大領域主枝（生活場域展開·生態掛載）")))
    L.append(row(ax(u"〔個人修煉〕  〔人際互動〕  〔僧團事務〕")))
    L.append(row(ax(u"〔僧俗邊界〕  〔危機時刻〕  〔照護護生〕")))
    L.append(row(u" " * A + u"▲"))
    L.append(conn(u"（微觀過濾·起心動念）"))
    L.append(row(ax(u"【動機審查窗櫺】")))
    L.append(row(ax(u"（境想作意 ➔ 意志動發 ➔ 邊界自察）")))
    L.append(row(u" " * A + u"▲"))
    L.append(conn(u"（法度支撐·天平尺規）"))
    L.append(row(ax(u"【八大天平尺規】")))
    L.append(row(ax(u"（衡平自心動機之八把天平尺）")))
    L.append(row(ax(u"心事/信心/慈悲/無心/底線/程序/復權/斷漏")))
    L.append(row(u" " * A + u"▲"))
    L.append(conn(u"（主幹貫注·生機源泉）"))
    L.append(row(ax(u"【樹幹唯一判準：佛問「汝以何心？」】")))
    L.append(row(ax(u"（起心動念之根本定性）")))
    L.append(row(u" " * A + u"▲"))
    L.append(conn(u"（深層吸納·染淨發動）"))
    L.append(bar(u"┌", u"┐", u"─"))
    L.append(box(u"【樹根：心所動力與根本心】"))
    L.append(box(u"根本煩惱（貪瞋癡慢疑見）"))
    L.append(box(u"╳ 隨煩惱（覆慳掉悔等）"))
    L.append(box(u"╳ 善心所（十一善）"))
    L.append(bar(u"└", u"┘", u"─"))
    L.append(conn(u"（環境滋養·立足根基）"))
    L.append(row(u" " * BL + u"=" * IN))
    L.append(row(ax(u"【土壤環境：自淨其意之法性空間 ＋ 世間信心防火牆】")))
    L.append(row(u" " * A + u"▲")[:R] + u"（歸土化泥）")
    L.append(row(u" " * A + u"│")[:-1] + u"▼")
    L.append(u" " * A + u"│ （種子萌發·長養林下無事之清淨日常）")
    seed = ax(u"【種子：三十二字略戒心印（體）】") + u" ◄"
    L.append(seed + u"─" * (R - dw(seed) - 1) + u"┘")
    L.append(ax(u"（善護三業，但自觀行；蜂採其華，不惱他人；"))
    L.append(ax(u"  明眼避險，自淨其意；勤學無憂，常樂空閑）"))
    return L


def main():
    block = build()
    bad = [x for x in block if dw(x) > 96]
    if bad:
        raise SystemExit(u"圖過寬：%s" % bad[0])
    cols = sorted({dw(x) for x in block if x.endswith(u"│")})
    print(u"圖 %d 行・右欄落點 %s・最大寬 %d" % (len(block), cols, max(dw(x) for x in block)))
    if cols != [R]:
        raise SystemExit(u"右欄不齊：%s（應唯 %d）" % (cols, R))
    if not WRITE:
        print("\n".join(block))
        return
    L = io.open(BOOK, "rb").read().decode("utf-8-sig").split("\n")
    s = [i for i, l in enumerate(L) if i > 110 and l.startswith("```text")]
    for i in s:
        if u"果實" in L[i + 1]:
            start = i
            break
    else:
        raise SystemExit(u"找不到生命之樹之圍欄")
    e = start + 1
    while not L[e].startswith("```"):
        e += 1
    L2 = L[:start + 1] + block + L[e:]
    out = "\r\n".join(x.rstrip("\r") for x in L2).encode("utf-8")
    if io.open(BOOK, "rb").read().startswith(b"\xef\xbb\xbf"):
        out = b"\xef\xbb\xbf" + out
    io.open(BOOK, "wb").write(out)
    print(u"已覆寫：圍欄 L%d–L%d・新體 %d 行" % (start + 1, e + 1, len(block)))


main()
