# -*- coding: utf-8 -*-
"""第十四波・新尺 `pairtocnum`：目錄之頁碼須逐條對合印面（管護欄冊 `tocnum` 之同職於雙子星兩冊）。

三口徑（皆以產物量，不以源檔推）：
  甲 **有號**：目錄每條行末必帶頁碼（無號即紅）；
  乙 **對合**：該號須等於書籤（＝印面實頁）所定之頁（錯號即紅，並點名兩數）；
  丙 **戶口**：篇・章・節（及案卷卡）各須在目錄中有一條（缺目即紅）。
另印：目錄頁數・條目數・收斂之證據（目錄首尾頁）。

用法：python -X utf8 _work/pairtocnum.py            # 兩冊兩式四檔
      python -X utf8 _work/pairtocnum.py 1          # 只查心法卷
"""
import os
import re
import sys

import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.join(ROOT, "_print")
BOOKS = [(u"起心動念_四分律的心智顯微鏡與唯識解剖_", u"起心動念"),
         (u"如法推尋_僧伽憲政法權審理與修復正義_", u"如法推尋")]
EDS = [u"螢幕版", u"影印版"]
ONLY = next((a for a in sys.argv[1:] if a in ("1", "2")), None)
TOC_FLOOR = 10.5                   # 目錄字級之下限：冊上量得小於此即細字
FOLDS = 0                          # 本冊此式印面上被折為兩行之目錄條數（量產物，非取產生器之自報）
NUM_END = re.compile(u"^(.*?)\\s*\\.{0,80}\\s*([0-9]{1,4})\\s*$")
HEAD_OK = re.compile(u"^(第[一二三四五六七八九十]+[篇章节]|终卷|終卷|附錄|附錄|【|第[一二三四五六七八九十]+章)")


def norm(s):
    return re.sub(r"[\s.·・‧]+", "", s)


def num_rows(doc, p):
    """一頁之中行末帶號之條數（目錄頁之指紋）。"""
    return sum(1 for l in doc[p].get_text().split("\n")
               if l.strip() and NUM_END.match(l.strip()) and len(norm(NUM_END.match(l.strip()).group(1))) >= 2)


def toc_pages(doc):
    """目錄所在頁：先尋『目』『錄』並見且帶號條密集之起頁，再**順勢前推**至號條斷絕為止。
    舊法只收『含目錄二字』之頁，遂把跨頁之目錄鋸成一頁——本冊目錄長 130/167 條，
    必跨數頁；只量首頁則條目少報、缺目虛紅（尺自己之病，非冊之病）。"""
    start = None
    for p in range(doc.page_count):
        txt = doc[p].get_text()
        if num_rows(doc, p) >= 5 and u"目" in txt and u"錄" in txt[:200]:
            start = p
            break
    if start is None:
        return []
    out = [start]
    p = start + 1
    while p < doc.page_count:
        n = num_rows(doc, p)
        # 目錄頁之指紋：除點線條與純數字之頁腳，別無他文。末頁常只賸一二條（舊律『≥5』
        # 遂把尾巴鋸掉，F1 實少報四條），故續頁之判改從『內容純為目錄行』。
        other = [l for l in doc[p].get_text().split("\n") if l.strip()
                 and not NUM_END.match(l.strip()) and not l.strip().isdigit()]
        if n >= 5 or (n >= 1 and not other):
            out.append(p)
            p += 1
            continue
        break
    return out


def rows_on(doc, p):
    global FOLDS
    out = []
    for l in doc[p].get_text().split("\n"):
        s = l.strip()
        if not s:
            continue
        m = NUM_END.match(s)
        if m and len(norm(m.group(1))) >= 2:
            out.append((m.group(1).strip(), int(m.group(2))))
        elif len(norm(s)) >= 4 and s[0] not in ("-", "*", u"│", u"┌", u"└"):
            out.append((s, None))
    # 折行之接合：目錄長條今分兩行印（第十四波・保級不縮字）。前導之無號行若其後
    # 緊接一有號行，即同一条之上半，須併回。**真缺號**之形是『標題＋點線而無號』，
    # 以點線辨之（有尾點者不併），否則接合之律會把缺號一并抹綠。
    merged = []
    k = 0
    while k < len(out):
        t, n = out[k]
        if n is None and not t.endswith(u"." ):
            j = k + 1
            buf = t
            while j < len(out) and out[j][1] is None and not out[j][0].endswith(u"."):
                buf += out[j][0]
                j += 1
            if j < len(out) and out[j][1] is not None:
                FOLDS += 1
                merged.append((buf + out[j][0], out[j][1]))
                k = j + 1
                continue
        merged.append((t, n))
        k += 1
    return merged


def toc_min_size(doc, p):
    """目錄頁之最小字級（純數字之頁腳除外）：字級之宣稱須量產物，不取產生器之自報。"""
    lo = None
    for b in doc[p].get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            for sp in ln.get("spans", []):
                txt = sp["text"].strip()
                if not txt or txt.isdigit():
                    continue
                if lo is None or sp["size"] < lo:
                    lo = sp["size"]
    return lo


def main():
    rc = 0
    for stem, short in BOOKS:
        if ONLY and ONLY != stem[-1]:
            continue
        for ed in EDS:
            path = os.path.join(HERE, stem + ed + u".pdf")
            if not os.path.isfile(path):
                print("缺檔：%s" % path)
                rc = 1
                continue
            d = pymupdf.open(path)
            marks = {}
            for lvl, title, page in d.get_toc():
                marks.setdefault(norm(title), page)
            tp = toc_pages(d)
            global FOLDS
            FOLDS = 0
            rows = []
            for p in tp:
                rows += rows_on(d, p)
            nokey = [(t, n) for t, n in rows if n is None]
            want = [(t, n) for t, n in rows if n is not None]
            bad = []
            for t, n in want:
                k = norm(t)
                pg = marks.get(k) or marks.get(k[:12]) or next(
                    (v for kk, v in marks.items() if kk.startswith(k[:10]) and len(kk) > 6), None)
                if pg is None:
                    bad.append((t, n, u"書籤無此題"))
                elif pg != n:
                    bad.append((t, n, u"實頁 %d" % pg))
            # 戶口：目錄須收全 篇/章/節 與案卷卡
            toc_txt = norm("".join(t for t, _ in rows))
            miss = []
            for lvl, title, page in d.get_toc():
                if lvl > 3:
                    continue
                base = norm(title)
                if not base or len(base) < 3:
                    continue
                if not re.match(u"(第[一二三四五六七八九十]+[篇章节]|終卷|【(?:全書|出版凡例|自序|開卷|附錄)|附錄[一二三四])", title):
                    if not (u"案卷" in title and lvl >= 3):
                        continue
                if re.match(u"【全書.*結構全貌圖", title):
                    continue          # 凡例之豁免：全貌圖即目錄之身，產生器已定不重複入目
                if base[:10] not in toc_txt:
                    miss.append(title[:34])
            sizes = [x for x in (toc_min_size(d, p) for p in tp) if x]
            thin = [p + 1 for p in tp if (toc_min_size(d, p) or 99) < TOC_FLOOR]
            print("■ %s｜%s｜目錄 %d 頁（p%s–p%s）・條目 %d 行・折行者 %d" % (
                short, ed, len(tp), (tp[0] + 1) if tp else "?", (tp[-1] + 1) if tp else "?",
                len(rows), FOLDS))
            print("   丁 目錄字級最細：%spt（下限 %.1f）・破下限之頁：%s" % (
                ("%.2f" % min(sizes)) if sizes else "n/a", TOC_FLOOR,
                u"無" if not thin else u"p" + u"、p".join(str(x) for x in thin)))
            print("   甲 無號之條：%d%s" % (len(nokey), u"" if not nokey else u" ➔ " + u"、".join(t[:22] for t, _ in nokey[:5])))
            print("   乙 號頁不合：%d%s" % (len(bad), u"" if not bad else u" ➔ " + u"；".join("%s（印 %s／實 %s）" % b for b in bad[:4])) )
            print("   丙 目錄缺目：%d%s" % (len(miss), u"" if not miss else u" ➔ " + u"、".join(miss[:6])))
            d.close()
            if nokey or bad or miss or thin or not tp:
                rc = 1
    print("=" * 60)
    print("退碼 %d（0 ＝ 目錄條條有號、號與印面合、篇章节與案卷卡俱入目、目錄無破下限之細字）" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
