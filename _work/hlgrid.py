# -*- coding: utf-8 -*-
"""格實測尺（hlgrid）：量印面圍欄每一行『實測格數』對源檔『預測格數』（CJK=2・框線=1），
   並校單頁之段『印面行數』不超『源行數』。兩式（影印・螢幕）俱校。
立尺之故（第 57 輪）：管線之回量器（build_hulan.pre_overflows）舊唯據『最長行應有之寬』縮字，
   又有 0.3pt 之免擾閘，遂令兩事俱漏——① 缺字（→↓↑▼）以 .55em 出字，advance 只 0.55 格，
   一行之內凡含此字者其右諸欄左漂（段5 至第五欄錯開近一字）；② 貼邊之行折為兩行，兩行各自
   短於框，『應有之寬』唯逾可用之寬 7pt 有奇，而按比例算得之縮幅不足 0.3pt，盡被閘住——
   11 段歷輪報『俱合版寬・無換行』而印面鋸字。本尺不猜模型、不聽宣稱，逕量產物。
同齡之約：產物若舊於正本，則所量乃陳印鑑——擲校（rc=1），不許假綠。
用法：python -X utf8 _work/hlgrid.py [--tol=0.5] [--pdf=路徑]（不給 --pdf 則兩式俱校）
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "_print"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import pymupdf as pm                                  # noqa: E402
import build_hulan as BH                              # noqa: E402

TOL = 0.5
ONLY = None
for a in sys.argv[1:]:
    if a.startswith(u"--tol="):
        TOL = float(a[6:])
    if a.startswith(u"--pdf="):
        ONLY = a[6:]
PRINT_DIR = os.path.join(HERE, "_print")
EDS = [ONLY] if ONLY else [os.path.join(PRINT_DIR, u"佛陀的護欄_四分律戒律之行為心理學解析_影印版.pdf"),
                           os.path.join(PRINT_DIR, u"佛陀的護欄_四分律戒律之行為心理學解析_螢幕版.pdf")]
lines = io.open(BH.SRC, encoding="utf-8", newline=u"").read().split(u"\r\n")
blocks = BH.fence_blocks(lines)
src_mtime = os.path.getmtime(BH.SRC)


def nn(s):
    return u"".join(s.split())


def page_rows(doc, pg, base):
    """該頁之等寬行：[(y, 行文字, 行左, 墨右, [空格寬])]。
    一格須取『本段窗內』之空格，不可取全頁之最小——同頁常有兩段圍欄而字級不同（第 57 輪實測：
    段5 與段4 同頁，以全頁最小空格為『一格』則 0.55×基準之驗必不合，十段遂成『未校』假紅）。"""
    out = []
    for bl in doc[pg].get_text("rawdict")["blocks"]:
        for ln in bl.get("lines", []):
            ch = [(c["c"], c["bbox"][0], c["bbox"][2]) for sp in ln.get("spans", []) for c in sp["chars"]]
            txt = u"".join(c for c, _x, _y in ch)
            if not txt.strip():
                continue
            if max(sp.get("size", 0) for sp in ln.get("spans", [])) > 1.1 * base + 0.4:
                continue
            spw = [y - x for c, x, y in ch if c == u" " and 0.25 * base < y - x < 0.85 * base]
            out.append((ln["bbox"][1], nn(txt), ln["bbox"][0],
                        max(y for _c, _x, y in ch), spw))
    out.sort()
    return out


def one_edition(pdf):
    """回 (病列表, 管轄 dict)。"""
    if not os.path.exists(pdf):
        return [(0, u"產物不存在：%s" % os.path.basename(pdf))], {}
    if os.path.getmtime(pdf) < src_mtime - 1:
        return [(0, u"陳印鑑：產物舊於正本（產 %s／源 %s）——擲校，先重建" % (
            __import__("time").strftime(u"%m-%d %H:%M", __import__("time").localtime(os.path.getmtime(pdf))),
            __import__("time").strftime(u"%m-%d %H:%M", __import__("time").localtime(src_mtime))))], {}
    mp, _n, miss = BH.pre_tag_map(blocks)
    bases = BH.pre_base_sizes()
    d = pm.open(pdf)
    pages = [u"".join(d[i].get_text().split()) for i in range(d.page_count)]
    bad = []
    unmet = []
    nchk = nseg = nun = 0
    NSEG = len(blocks)
    for k, b in enumerate(blocks, 1):
        head, tail = nn(b[0])[:12], nn(b[-1])[:12]
        ph = [i for i, t in enumerate(pages) if head in t]
        pt = [i for i, t in enumerate(pages) if tail in t]
        if not ph or not pt:
            bad.append((k, u"印面失首／失尾"))
            continue
        base = bases[mp[k]] if k in mp and mp[k] < len(bases) else None
        if not base:
            bad.append((k, u"無基準字級"))
            continue
        pgs = sorted(set(ph) & set(pt)) or list(range(min(ph), min(max(pt) + 1, min(ph) + 5)))
        srcmap = {}
        for s in b:
            if nn(s):
                srcmap.setdefault(nn(s), []).append(s)
        rows = []
        for pg in pgs:
            rows.extend(page_rows(d, pg, base))
        rows.sort()
        yh = [y for y, t, _x0, _x1, _s in rows if t.startswith(head)]
        yt = [y for y, t, _x0, _x1, _s in rows if t.startswith(tail)]
        if not yh or not yt:
            bad.append((k, u"窗界失（首或尾行未入等寬之列）"))
            continue
        win = [r for r in rows if min(yh) - 1 <= r[0] <= max(yt) + 1]
        spw = [w for r in win for w in r[4]]
        if not spw:
            bad.append((k, u"窗內無空格・一格無從定・未校"))
            continue
        cell = min(spw)
        if abs(cell - 0.55 * base) > 0.08 * base:
            bad.append((k, u"一格 %.2fpt 與 0.55×字級 %.2fpt 不合（差 %.2f）・未校"
                        % (cell, 0.55 * base, abs(cell - 0.55 * base))))
            continue
        for y, t, x0, x1, _s in win:
            m = srcmap.get(t)
            if not m:
                nun += 1                     # 印面有此行而源文無對（折行之半段・雜行）
                unmet.append((k, t[:46]))
                continue
            if len(m) != 1:
                continue                     # 源文重出，不敢斷言是哪一行
            pred = BH.cw_units(m[0].rstrip())
            meas = (x1 - x0) / cell
            nchk += 1
            if abs(pred - meas) > TOL:
                bad.append((k, u"L%d  pred %d 格｜實 %.2f 格｜差 %+.2f｜%s" % (
                    b.index(m[0]) + 1, pred, meas, meas - pred, m[0].rstrip()[:30])))
        nseg += 1
        if len(pgs) == 1:
            nsrc = len([x for x in b if nn(x)])
            if len(win) > nsrc:
                bad.append((k, u"印 %d 行 > 源 %d 行（有行被鋸）" % (len(win), nsrc)))
    d.close()
    return bad, dict(seg=nseg, chk=nchk, fold=nun, tot=NSEG, unmet=unmet[:4])


rc = 0
for pdf in EDS:
    bad, cov = one_edition(pdf)
    print(u"%s｜入校 %d/%d 段（段數自正本實算）・校格 %d 行・源文未及配對之印行 %d・容差 %.1f 格" % (
        os.path.basename(pdf), cov.get("seg", 0), cov.get("tot", 0),
        cov.get("chk", 0), cov.get("fold", 0), TOL))
    for k, t in cov.get("unmet", []):
        print(u"  · 段%-3d 未及配對之行｜«%s»" % (k, t))
    if not bad:
        print(u"  ✓ 格・行俱合")
    for k, msg in bad[:30]:
        print(u"  ✗ 段%-3d %s" % (k, msg))
    if len(bad) > 30:
        print(u"  … 另有 %d 條" % (len(bad) - 30))
    rc = rc or (1 if bad else 0)
print(u"總判：%s" % (u"綠" if rc == 0 else u"紅"))
sys.exit(rc)
