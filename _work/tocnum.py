# -*- coding: utf-8 -*-
"""尺（tocnum）——目錄頁碼之產物層覆核：冊上目錄所印之每個號，須確指其題所在之頁。

所以立之（第 56 輪）：頁碼由管線兩三回合收斂而來，收斂只證『注入之號＝注入當回合實測之號』，
    不證『交付之冊仍與所注入之號同』——若有人在收斂後又動了版面（或手改中介 md），
    目錄即成虛號。故本尺不讀管線之任何中間值，唯讀兩樣：
      ① 交付之冊（PDF）——逐頁取字級 ≥HEAD_MIN 之 span（標題級）與全頁文字；
      ② 該式實際送排之中介 md——目錄條目今為 `<span class="ti">…<span class="tn">N</span>` 之形，
         條目文字與所印之號俱從印面之形取，不另立名單（名單兩抄必落後）。
判準（四級，逐級放寬而各報其數——放寬之級須親核，故全表可出）：
  T1 直中：該頁之『標題級』字（≥HEAD_MIN）含條目前 12 字；
  T2 見頁：該頁全文字含前 12 字（印面折行或字級特殊者）；
  T3 見冠：該頁含條目之『冠』（『：』之前，≥3 字）——作者撮舉之目與章內標題不同字面，唯冠可證；
  T4 見段：該頁含條目之任一片段（冠・尾段各削括註後、及前六字，≥3 字）——如『國王的心臟與
      宗廟』一目，章內標題作『國王的心臟與修道生命——四大波羅夷』，其尾段『四大波羅夷』在頁；
  T5 承上：該條之號＝其上位條目之號，且上位已過 T1～T4——全書有撮舉之目本無自題（如
      『《摩奴法典》的三從鐵幕』），其號只能指它所屬之節；此級不自證其題，只證其歸屬。
五級俱不中 ⇒ 虛號，點名退 1。另檢：① 目錄之每一條須有號；② 所標之頁不得落在目錄自身之頁；
    ③ 冊上目錄之題須在（目錄未印即紅）。
用法：python -X utf8 _work/tocnum.py [print|screen|slim] [--all]   # 無參＝影印版；--all 印全表
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "_print"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import build_hulan as BH                                  # noqa: E402  同一路徑法源與同一正規口徑

LI = re.compile(u'^\\s*[*+-]\\s*<span class="ti"><span class="tx">(.*?)</span>'
                u'<span class="ld"></span><span class="tn">(\\d+)</span></span>$')
PP = re.compile(u'^<p class="tp"><span class="ti"><span class="tx">(.*?)</span>'
                u'<span class="ld"></span><span class="tn">(\\d+)</span></span></p>$')


def main():
    if not os.path.isfile(BH.MD):
        raise SystemExit(u"無中介 md 可量：%s" % BH.MD)
    if not os.path.isfile(BH.PDF_OUT):
        raise SystemExit(u"無冊可量：%s（本尺量產物，須先重建）" % os.path.basename(BH.PDF_OUT))
    md = io.open(BH.MD, encoding="utf-8").read().split("\n")
    _a, _b = BH.toc_bounds(md)
    rows, naked = [], []
    for n in range(_a + 1, _b):
        l = md[n]
        m = PP.match(l) or LI.match(l)
        if m:
            rows.append((n + 1, BH.norm_txt(m.group(1)), int(m.group(2))))
        elif re.match(u"^### \\*\\*", l) or re.match(r"^\s*[*+-]\s+\S", l):
            naked.append((n + 1, BH.norm_txt(l)[:36]))
    import pymupdf
    d = pymupdf.open(BH.PDF_OUT)
    big, full = BH.big_pages(d)
    npage = d.page_count
    toc_pg = next((i for i in range(npage) if BH.norm_txt(u"全書詳細目錄") in big[i]), None)
    if toc_pg is None:
        raise SystemExit(u"冊上無『全書詳細目錄』之題——目錄未印？")
    lo = min(r[2] for r in rows) if rows else toc_pg + 1
    _a, bnd = BH.toc_bounds(md)
    nxt = next((l for l in md[bnd:] if re.match(r"^# ", l)), u"")
    key0 = BH.norm_txt(nxt[2:])[:12]
    floor = next((i for i in range(toc_pg, npage) if key0 and key0 in big[i]), toc_pg)
    def segs(nm):
        """條目之可證片段：冠（削括註）、冒號後之尾段（≥4 字）、條目前 6 字。"""
        parts = [p for p in re.split(u"：|——", nm) if p]
        out = []
        for p in parts:
            out.append(p)
            out.append(re.sub(u"（[^（）]*）", u"", p))
            if len(p) >= 6:
                out.append(p[:6])
        return [p for p in dict.fromkeys(out) if len(p) >= 3]

    tier, bad, prev_ok = {}, [], (None, False)
    for ln, nm, pg in rows:
        crown = nm.split(BH.CROWN_CUT)[0]
        if not (1 <= pg <= npage):
            why = u"越界"
        elif pg < floor + 1:
            why = u"自指"
        elif nm[:12] and nm[:12] in big[pg - 1]:
            why = u"T1直中"
        elif nm[:12] and nm[:12] in full[pg - 1]:
            why = u"T2見頁"
        elif len(crown) >= 3 and crown in full[pg - 1]:
            why = u"T3見冠"
        elif any(s in full[pg - 1] for s in segs(nm)):
            why = u"T4見段"          # 撮舉之目與章內標題不同字面：取其片段（冠・尾段・前六字）
        elif prev_ok[0] == pg and prev_ok[1]:
            why = u"T5承上"
        else:
            why = u"虛號"
        tier[why] = tier.get(why, 0) + 1
        if why in (u"虛號", u"越界", u"自指"):
            bad.append((ln, nm[:26], pg, why))
        prev_ok = (pg, why not in (u"虛號", u"越界", u"自指"))
    print(u"冊：%s｜%d 頁｜目錄 p%d 起・正文起 p%d（%s）"
          % (os.path.basename(BH.PDF_OUT), npage, toc_pg + 1, floor + 1, nxt[2:16]))
    print(u"中介 md 帶號條目 %d／目錄應有條目 %d｜號標在 p%d..p%d"
          % (len(rows), len(rows) + len(naked), lo, max(r[2] for r in rows) if rows else 0))
    print(u"判級分布：%s" % u"・".join(u"%s %d" % (k, tier[k])
                                     for k in sorted(tier)))
    if "--all" in sys.argv:
        for ln, nm, pg in rows:
            print(u"  p%-4d L%-5d %s" % (pg, ln, nm[:56]))
    for ln, t in naked[:12]:
        print(u"  無號：md L%d %s" % (ln, t))
    for ln, nm, pg, why in bad[:15]:
        print(u"  ✗ md L%d『%s』標 p%d：%s" % (ln, nm, pg, why))
    n = len(bad) + len(naked)
    print(u"判：無號 %d・虛號 %d｜今 %s"
          % (len(naked), len(bad), u"合格" if n == 0 else u"不（%d 處）" % n))
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main())
