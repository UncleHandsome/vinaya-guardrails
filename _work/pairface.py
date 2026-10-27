# -*- coding: utf-8 -*-
"""雙子星兩冊印面之覆核器（量產物，不量口徑；沿用 SOP 印面五量之維，另立兩量）。

用法：python -X utf8 _work/pairface.py [--stale]
目：
  〇 同期——正本 mtime 須早於印面，否則退 2 拒鑑（以陳印鑑新冊即假紅假綠）
  甲 頁數與大小（交付檔＝產物）
  乙 書籤逐條在其所指頁確見其題（摺平空白後搜），并报源檔標題數之對合
  丙 細字——全冊最小字級・9pt 以下之 span 數與落點頁
  丁 字面標記之殘——冊上不应見 `**`／行首 `#`／``` 圍欄符（形制歸一是否真歸一）
  戊 骨架對合——篇・章之數在冊上實見，須與正本實測同數
  己 合冊——封面之實測（必見之字・字不出框・細字）＋頁數與書籤接排之自算對合
     （合冊非兩卷之簡單相加：另加封面與『合璧說明』隔頁各一，書籤一律右移；
      陳合冊配新卷、右移少一頁、封面畫了卻不見字，三病俱唯此目能量出）
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import pymupdf as pm                                    # noqa: E402

PAIR = [("起心動念：四分律的心智顯微鏡與唯識解剖.txt",
         "起心動念_四分律的心智顯微鏡與唯識解剖_螢幕版.pdf", "final_pair1_screen.html"),
        ("如法推尋：僧伽憲政、法權審理與修復正義.txt",
         "如法推尋_僧伽憲政法權審理與修復正義_螢幕版.pdf", "final_pair2_screen.html")]
HAN = "〇一二三四五六七八九十百"
errs, notes = [], []


def fold(s):
    s = re.sub(r"[*`]", "", s)
    s = re.sub("[\u2018\u2019\u02bc]", "'", s)          # 撇號曲直之折（pandoc smart 所排）
    s = re.sub("[\u201c\u201d]", '"', s)
    return re.sub(r"\s+", "", s)


def src_titles(path):
    txt = path.read_bytes().decode("utf-8-sig")
    lines, fence, out = txt.replace("\r\n", "\n").split("\n"), False, []
    for l in lines:
        if re.match(r"^\s*```", l):
            fence = not fence
            continue
        if fence:
            continue
        m = re.match(r"^(#{1,6})\s+(\S.*)$", l.strip())
        if m:
            out.append((len(m.group(1)), re.sub(r"[*`]", "", m.group(2)).strip()))
    return out


for fn, pdfname, finname in PAIR:
    src = ROOT / fn
    pdf = ROOT / "_print" / pdfname
    print("=" * 74)
    print("■", fn)
    if not pdf.is_file():
        errs.append(f"{pdfname} 不在盤上")
        continue
    mt_src, mt_pdf = src.stat().st_mtime, pdf.stat().st_mtime
    stale = mt_src > mt_pdf
    print(f"  〇 同期：正本 {mt_src:.0f}・印面 {mt_pdf:.0f} → "
          f"{'★冊新於印（拒鑑）' if stale else '印晚於冊 ✓'}")
    if stale and "--stale" not in sys.argv:
        errs.append(f"{pdfname}：正本新於印面——須重建後方能量（拒鑑）")

    d = pm.open(str(pdf))
    n = d.page_count
    pages = [fold(d[i].get_text()) for i in range(n)]
    toc = d.get_toc()
    print(f"  甲 頁數 {n}・{os.path.getsize(pdf) // 1024} KB・書籤 {len(toc)} 條")

    hit, miss = 0, []
    for lvl, title, pg in toc:
        f = fold(title)
        if f and 1 <= pg <= n and f in pages[pg - 1]:
            hit += 1
        else:
            miss.append((pg, title[:26]))
    print(f"  乙 書籤對合：確見其題 {hit}/{len(toc)}・不符 {len(miss)}")
    for pg, t in miss[:6]:
        print(f"       ⚠ p{pg} 「{t}」")
    if miss:
        errs.append(f"{pdfname}：書籤 {len(miss)} 條所指頁不見其題")

    sizes, thin = {}, []
    for i in range(n):
        for b in d[i].get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                for sp in ln["spans"]:
                    if not sp["text"].strip():
                        continue
                    sizes[round(sp["size"], 2)] = sizes.get(round(sp["size"], 2), 0) + 1
                    if sp["size"] < 9:
                        thin.append((i + 1, round(sp["size"], 2), sp["text"][:18]))
    lo = min(sizes) if sizes else 0
    print(f"  丙 細字：最小 {lo}pt・9pt 以下 {len(thin)} span（字級分布 top6 "
          f"{sorted(sizes.items(), key=lambda kv: -kv[1])[:6]}）")
    for p, s, t in thin[:6]:
        print(f"       · p{p} {s}pt「{t}」")
    if thin:
        notes.append(f"{pdfname}：9pt 以下 {len(thin)} span（最細 {lo}pt）——護欄冊之戒，宜查")

    # 丁目須量對層：圍欄（<pre>）內之 `**` 是源檔留進框線圖的字面，pandoc 本就不解析——
    # 以整頁文字搜星號會把圖文误報成『markdown 未歸一』（本尺初跑即如此假紅 12 枚）。
    fin = ROOT / "_print" / finname
    html = Path(fin).read_text(encoding="utf-8")
    outside = re.sub(r"(?s)<style.*?</style>", "", re.sub(r"(?s)<pre\b.*?</pre>", "", html))
    otxt = re.sub(r"<[^>]+>", "", outside)
    lit = [m.group(0)[:40] for m in re.finditer(r"^\s*#{1,6}\s+\S", otxt, re.M)]
    nstar, nfence = otxt.count("**"), otxt.count("```")
    # 行內之字面標記（#／鏈）與單星斜體：只查行首即有盲區，三維同步須同目覆核
    RX_INLINE = r"(?:[\u3000\u4e00-\u9fff]\s{0,2}#{1,6}\s*\S)"
    RX_LINK = r"\[[^\]\x00-\x08\x0b-\x1f]{1,40}\]\([^\x00-\x08\x0b-\x1f\)]{1,60}\)"
    inline = [m.group(0)[:36] for m in re.finditer(RX_INLINE + "|" + RX_LINK, otxt)]
    nlink = sum(1 for m in re.finditer(RX_LINK, otxt))
    RX_ITAL = r"(?<![*/\w])\*[\u4e00-\u9fff]{2,24}\*(?![*/\w])"
    ital = [m.group(0)[:36] for m in re.finditer(RX_ITAL, otxt)]
    rawhtml = len(re.findall(r"</?(?:div|span|br|p|img|a)\\b", otxt))   # 須量剝 tag 之後：量 outside 即把正常標記當病（初跑假紅 1,191 枚）
    nline = sum(1 for l in otxt.splitlines() if l.strip())
    inpre = [i + 1 for i in range(n)
             if any("**" in sp["text"] for b in d[i].get_text("dict")["blocks"]
                    for ln in b.get("lines", []) for sp in ln["spans"])]
    print(f"  丁 字面標記之殘（圍欄外之紙面，管轄＝圍欄外 {len(otxt):,} 字／{nline:,} 行）："
          f"行首 `#` {len(lit)}・行內 `#` {len(inline) - nlink}・鏈 {nlink}・`**` {nstar}・"
          f"單星斜體 {len(ital)}・``` {nfence}・字面 HTML {rawhtml}"
          f"（另：圖文內帶星號之頁 {len(inpre)} 頁——源檔框線圖之字面，屬正文形制而非產器之失）")
    for x in (lit + inline + ital)[:5]:
        print(f"       ⚠「{x}」")
    if lit or inline or ital or nstar or nfence or rawhtml:
        errs.append(f"{pdfname}：圍欄外仍見字面 markdown（行首# {len(lit)}／行內# {len(inline) - nlink}／"
                    f"鏈 {nlink}／* {len(ital)}／** {nstar}／``` {nfence}／HTML {rawhtml}）")

    st = src_titles(src)
    pian = sum(1 for lv, t in st if re.match(rf"^第[{HAN}]+篇[:：]", t))
    zhang = sum(1 for lv, t in st if re.match(rf"^第[{HAN}]+章[　 ]", t))
    onpaper_p = sum(1 for lv, t, pg in toc if re.match(rf"^第[{HAN}]+篇[:：]", t))
    onpaper_z = sum(1 for lv, t, pg in toc if re.match(rf"^第[{HAN}]+章[　 ]", t))
    print(f"  戊 骨架對合：正本 篇{pian}・章{zhang} ｜ 冊上書籤 篇{onpaper_p}・章{onpaper_z}")
    if (pian, zhang) != (onpaper_p, onpaper_z):
        errs.append(f"{pdfname}：骨架不合（正本 篇{pian}章{zhang}・冊 篇{onpaper_p}章{onpaper_z}）")
    d.close()

print("=" * 74)

# ── 己・合冊：兩卷接排之檔。封面、合璧說明隔頁、書籤右移三事俱在合冊身上，
#    兩卷之尺量不到（陳合冊配新卷、右移少一頁、封面畫了卻不見字，皆唯此目能現）。
sys.path.insert(0, str(ROOT / "_print"))
import build_pair as BP                                        # noqa: E402

for ed in ("螢幕版", "影印版"):
    vols = [ROOT / "_print" / (cfg["out"] + ed + ".pdf") for cfg in BP.BOOKS]
    mrg = ROOT / "_print" / BP.merged_name(ed)
    print("=" * 74)
    print("■ 雙子星合冊｜%s" % ed)
    lack = [p.name for p in vols + [mrg] if not p.is_file()]
    if lack:
        errs.append("合冊%s：缺檔 %s" % (ed, "、".join(lack)))
        print("  ⚠ 缺檔：%s" % "、".join(lack))
        continue
    mt_v = max(p.stat().st_mtime for p in vols)
    mt_m = mrg.stat().st_mtime
    print("  〇 同期：兩卷 %.0f・合冊 %.0f → %s"
          % (mt_v, mt_m, "★合冊早於卷（陳合冊，拒鑑）" if mt_v > mt_m else "接排晚於卷 ✓"))
    if mt_v > mt_m and "--stale" not in sys.argv:
        errs.append("合冊%s：兩卷新於合冊——接排須重做" % ed)

    ds = [pm.open(str(p)) for p in vols]
    nv = [x.page_count for x in ds]
    tv = [len(x.get_toc()) for x in ds]
    dm = pm.open(str(mrg))
    nm, toc = dm.page_count, dm.get_toc()
    mrg_w, mrg_h = dm[0].rect.width, dm[0].rect.height
    for x in ds:
        x.close()
    pad = BP.layout_pad(nv[0])                   # 落版之補白（卷二須自 recto 起，見 build_pair）
    exp_n = 3 + nv[0] + nv[1] + pad              # 封面 1＋卷一＋隔頁 2（recto＋verso）＋卷二＋補白
    exp_t = tv[0] + tv[1] + 1                    # ＋隔頁之籤一條
    div_pg = 2 + nv[0] + pad                     # 1-based：封面 1・卷一 2..(1+nv0)・補白・隔頁
    pages = [fold(dm[i].get_text()) for i in range(nm)]
    print("  甲 頁數 %d（自算 3＋%d＋%d＋補白 %d＝%d）・%d KB・書籤 %d 條（自算 %d＋%d＋1＝%d）"
          % (nm, nv[0], nv[1], pad, exp_n, os.path.getsize(mrg) // 1024, len(toc),
             tv[0], tv[1], exp_t))
    if nm != exp_n:
        errs.append("合冊%s：頁數不合（實 %d・算 %d）——接排多頁或少頁" % (ed, nm, exp_n))
    if len(toc) != exp_t:
        errs.append("合冊%s：書籤條數不合（實 %d・算 %d）" % (ed, len(toc), exp_t))

    hit, miss, oncov = 0, [], []
    for lvl, title, pg in toc:
        f = fold(title)
        if pg == 1:
            oncov.append(title[:22])
        if f and 1 <= pg <= nm and f in pages[pg - 1]:
            hit += 1
        else:
            miss.append((pg, title[:26]))
    print("  乙 書籤對合：確見其題 %d/%d・不符 %d・指封面（p1）之籤 %d" % (hit, len(toc), len(miss), len(oncov)))
    for pg, t in miss[:6]:
        print("       ⚠ p%d 「%s」" % (pg, t))
    if miss:
        errs.append("合冊%s：書籤 %d 條所指頁不見其題（右移或接排之誤）" % (ed, len(miss)))
    if oncov:
        errs.append("合冊%s：%d 條書籤指向封面頁 ➔ %s" % (ed, len(oncov), "、".join(oncov[:3])))
    if u"合璧說明" not in pages[div_pg - 1]:
        errs.append("合冊%s：自算之隔頁 p%d 不見『合璧說明』" % (ed, div_pg))
    # 落版（recto/verso）：卷二之首頁須為 1-based 奇（recto）；隔頁落 verso；補白頁須真空白。
    vol2_pg = div_pg + 2
    print("  庚 落版：隔頁 p%d（%s）・卷二起 p%d（%s）・補白 %s"
          % (div_pg, u"recto ✓" if div_pg % 2 == 1 else u"verso ✗",
             vol2_pg, u"recto ✓" if vol2_pg % 2 == 1 else u"verso ✗",
             (u"p%d 空白 %s" % (div_pg - 1, u"✓" if not pages[div_pg - 2].strip() else u"✗")) if pad else u"無"))
    if vol2_pg % 2 != 1 or div_pg % 2 != 1:
        errs.append("合冊%s：落版不合（隔頁 p%d・卷二 p%d；應 隔頁 recto（占兩頁）・卷二 recto）" % (ed, div_pg, vol2_pg))
    if pad and pages[div_pg - 2].strip():
        errs.append("合冊%s：補白頁 p%d 非空白" % (ed, div_pg - 1))

    sizes, thin = {}, []
    for i in range(nm):
        for b in dm[i].get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                for sp in ln["spans"]:
                    if not sp["text"].strip():
                        continue
                    sizes[round(sp["size"], 2)] = sizes.get(round(sp["size"], 2), 0) + 1
                    if sp["size"] < 9:
                        thin.append((i + 1, round(sp["size"], 2), sp["text"][:18]))
    lo = min(sizes) if sizes else 0
    drawn = [t for t in thin if t[0] in (1, div_pg)]
    print("  丙 細字：最小 %spt・9pt 以下 %d span（其中產器自畫之頁 %d）" % (lo, len(thin), len(drawn)))
    for p, s, t in thin[:6]:
        print("       · p%d %spt「%s」" % (p, s, t))
    if drawn:
        errs.append("合冊%s：自畫之封面／隔頁有 9pt 以下細字 %d 處（產器之字當自持其下限）➔ %s"
                    % (ed, len(drawn), "、".join("p%d %spt「%s」" % x for x in drawn[:3])))
    elif thin:
        notes.append("合冊%s：9pt 以下 %d span（最細 %spt）——俱在兩卷正文，與分卷同其註記"
                     % (ed, len(thin), lo))

    cov = pages[0]
    gone = [w for w in BP.COVER_MUST if fold(w) not in cov]
    bad = []
    for x0, y0, x1, y1, word, *_ in dm[0].get_text("words"):
        if x1 > mrg_w - BP.COVER_EDGE or x0 < BP.COVER_EDGE or y1 > mrg_h - BP.COVER_EDGE or y0 < BP.COVER_EDGE:
            bad.append("%s[%.0f,%.0f]" % (word[:8], x1, y1))
    print("  己 封面：必見之字 %d/%d・出界之字 %d・頁寬 %.1f・界 %.0f"
          % (len(BP.COVER_MUST) - len(gone), len(BP.COVER_MUST), len(bad), mrg_w, BP.COVER_EDGE))
    if gone:
        errs.append("合冊%s：封面缺字 ➔ %s" % (ed, "、".join(gone)))
    if bad:
        errs.append("合冊%s：封面有字出界 %d 處 ➔ %s" % (ed, len(bad), "、".join(bad[:4])))
    dm.close()

# ── 辛・字型嵌入（六檔）：Type0 而無嵌入檔者即紅——換檢視器即成空白（外路第十六報告之病根）；
#    Type3 者其 CharProc 自足（本冊即『➔』U+2794 之向量字形），只報其數，不計病。
print("=" * 74)
print("■ 字型嵌入（六檔）")
FILES = [(cfg["out"] + ed + ".pdf", cfg["key"] + "｜" + ed)
         for cfg in BP.BOOKS for ed in (u"螢幕版", u"影印版")]
FILES += [(BP.merged_name(ed), u"合冊｜" + ed) for ed in (u"螢幕版", u"影印版")]
for fnm, tag in FILES:
    df = pm.open(str(ROOT / "_print" / fnm))
    bad, t3 = {}, set()
    for p in range(df.page_count):
        for xf in df.get_page_fonts(p):
            if xf[2] == "Type3":
                t3.add(p + 1)
            elif xf[1] in ("n/a", ""):
                bad.setdefault(xf[3] or u"(無名)", set()).add(p + 1)
    df.close()
    print("  %s：未嵌入 %d 種・Type3（自足）%d 頁" % (tag, len(bad), len(t3)))
    for k, v in bad.items():
        print("       ⚠ %s ➔ 頁 %s" % (k, sorted(v)[:6]))
    if bad:
        errs.append("%s：%d 種字型未嵌入（%s）" % (tag, len(bad), "、".join(bad)))

for x in notes:
    print("・", x)
if errs:
    print(f"\n✗ 紅 {len(errs)} 條：")
    for e in errs:
        print("   ⚠", e)
    sys.exit(1)
print("\n✓ 全綠：兩冊印面同期・書籤逐條對合・圍欄外無字面標記・骨架與正本同數；"
      "合冊頁數・接排・封面俱自算對合。"
      "\n   （細字一維為『報而不治』之註記，見上；超寬圖文須作者裁：或削圖、或容細字）")
