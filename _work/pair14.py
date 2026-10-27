# -*- coding: utf-8 -*-
"""第十四波・目錄之頁碼（作者令：『目錄沒有頁碼』）。

病：雙子星兩冊之目錄向為**正本內之 markdown 清單**（由 pairf1toc／pairf2toc 自正文標題生成），
    清單不載頁碼——印面上唯書籤可跳，紙上無從按頁求；又因頁碼須自**印成之冊**反查，唯產物層能給。
治：產器 `_print/build_pair.py` 今改走 build38 之點線目錄生成器（`prepare_toc_entries`＋`scan_pages`
    ＋`build_toc_html`），冷起點→反查→回填→再印，至頁碼收斂（兩冊各 2 回合）；
    於是**法源仍一本**（正文標題），而目錄由產器出——正本之 markdown 目錄塊遂成『文在而印不在』之幽靈，
    本刀除之（退役 pairf1toc／pairf2toc，改由本刀＋新尺 `pairtocnum.py` 守）。

用法：python -X utf8 _work/pair14.py          # 試跑（印行數與塊界，不動檔）
      python -X utf8 _work/pair14.py --write  # 落盤（備 .pre_a14）
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W = "--write" in sys.argv
LF = chr(10)
CRLF = chr(13) + LF
BOOKS = [ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt",
         ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt"]
HEAD = re.compile(u"^#{1,2}\\s*【全書標準總目錄】")
NEXT = re.compile(u"^#{1,2}\\s")
OKLINE = re.compile(u"^(?:#{1,6}\\s|\\s*[*+-]\\s|\\s*$|\\s+\\S|-{3,}|\\*{3,}|>|\\||`{3,})")


def main():
    for src in BOOKS:
        raw = src.read_bytes().decode("utf-8-sig")
        nl = CRLF if CRLF in raw else LF
        L = raw.replace(CRLF, LF).split(LF)
        i = next((k for k, l in enumerate(L) if HEAD.match(l)), None)
        if i is None:
            print("  %s：目錄塊不在檔（已除，如實）" % src.name[:8])
            continue
        j = next((k for k in range(i + 1, len(L)) if NEXT.match(L[k])), len(L))
        blk = L[i:j]
        bad = [(i + x + 1, blk[x][:40]) for x in range(len(blk)) if not OKLINE.match(blk[x])]
        nb = sum(1 for x in blk if x.strip() and re.match(u"\\s*[*+-]\\s", x))
        if bad or nb < 20:
            raise SystemExit("塊形不合目錄之形制，不敢削：%s・條目 %d" % (bad[:4], nb))
        print("  %s：目錄塊 L%d-%d（%d 行・條目 %d 行）・其後第一題『%s』"
              % (src.name[:8], i + 1, j, j - i, nb, L[j][:36]))
        del L[i:j]
        # 除塊後之疊缝：連的空行收一枚，連段分隔不雙出
        k = i
        while k > 0 and not L[k - 1].strip():
            k -= 1
        if k and L[k - 1].strip() in ("---", "***") and k < len(L) and L[k].strip() in ("---", "***"):
            del L[k]
            print("     併缝：除重出之分隔符一枚")
        out = nl.join(L).encode("utf-8")
        print("     行數 %d ➔ %d" % (len(raw.replace(CRLF, LF).split(LF)), len(L)))
        if not W:
            print("     （試跑：未落盤）")
            continue
        (ROOT / "_archive/備份/AI清理前" / (src.name + ".pre_a14")).write_bytes(raw.encode("utf-8"))
        src.write_bytes(out)
        print("     落盤：SHA %s ➔ %s" % (hashlib.sha256(raw.encode()).hexdigest()[:12],
                                          hashlib.sha256(out).hexdigest()[:12]))


if __name__ == "__main__":
    main()
