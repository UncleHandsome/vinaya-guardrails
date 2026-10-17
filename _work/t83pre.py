# -*- coding: utf-8 -*-
"""印面框線圖之字級診斷：以 build38 自家之 _cw 與 fit_pre_blocks 同一算式實測。"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "_print"))
import build38 as B  # noqa

MD = os.path.join(ROOT, u"ver38四分律_起心動念心智分析框架_修正版.md")
lines = io.open(MD, encoding="utf-8").read().split("\n")
NO = B.DROP_H1 if hasattr(B, "DROP_H1") else (u"修訂誌", u"跨章款級索引", u"十維驗收", u"全書校勘記", u"全書竣工呈辭")

CW = B._cw
CONTENT_W = (210 - 20) / 25.4 * 72
MAXF, MINF, PAD = 11.8, 6.2, 1.6

h1 = [(i, l[2:].strip()) for i, l in enumerate(lines) if l.startswith("# ")]


def sect(i):
    cur = ""
    for k, l in h1:
        if k <= i:
            cur = l
        else:
            break
    return cur


def near(i):
    """最近之較小標題（H2–H5），便於指認。"""
    for k in range(i, max(0, i - 90), -1):
        m = re.match(r"^#{2,5}\s*(.+)$", lines[k])
        if m:
            return m.group(1).strip()[:34]
    return u"？"


blocks = []
i = 0
while i < len(lines):
    m = re.match(r"^(\s*)(`{3,}|~{3,})", lines[i])
    if m:
        fence, ind = m.group(2)[0] * 3, m.group(1)
        j = i + 1
        body = []
        while j < len(lines) and not lines[j].strip().startswith(fence):
            body.append(lines[j])
            j += 1
        blocks.append((i, j, ind, body))
        i = j + 1
        continue
    i += 1

out = [u"##### 印面 pre 之實測字級（完整版／影印版口徑：版寬 %.1fpt，上限 %.1f、下限 %.1f）#####" % (CONTENT_W, MAXF, MINF)]
bad = []
for (a, b, ind, body) in blocks:
    s = sect(a)
    if any(k in s for k in NO):
        continue
    if not any(x.strip() for x in body):
        continue
    wmax = max([CW(x) for x in body] + [1])
    nl = sum(1 for x in body if x.strip())
    size = max(MINF, round(min(MAXF, CONTENT_W / max(1.0, 0.55 * wmax + PAD)), 2))
    inbq = bool(ind) or any(l.strip().startswith(">") for l in body)
    keep = (nl * size * 1.30 + 6) <= 700.0
    rec = (size, wmax, nl, a + 1, s[:5], near(a), inbq, keep)
    bad.append(rec)

bad.sort()
out.append(u"%-6s %-5s %-4s %-7s %-5s %-3s %-3s %s" % (u"pt", u"寬位", u"行", u"行號", u"章", u"框", u"鎖", u"最近小標"))
for size, wmax, nl, ln, ch, hd, inbq, keep in bad:
    flag = u"◂◂" if size < 7.6 else (u"◂" if size < 9.5 else u"")
    out.append(u"%5.2f %5d %4d L%-6d %-5s %-3s %-3s %s %s" % (
        size, wmax, nl, ln, ch, u"BQ" if inbq else u"", u"Y" if keep else u"N", hd, flag))
full = [x for x in bad if x[0] >= MAXF - 0.01]
out.append(u"")
out.append(u"共 %d 段印面 pre：飽和（11.8pt）%d 段；低於 9.5pt %d 段；低於 7.6pt %d 段" % (
    len(bad), len(full), sum(1 for x in bad if x[0] < 9.5), sum(1 for x in bad if x[0] < 7.6)))
out.append(u"欲飽和須 wmax ≤ %d 位；欲 ≥9pt 須 wmax ≤ %d 位；欲 ≥8pt 須 wmax ≤ %d 位" % (
    int((CONTENT_W / MAXF - PAD) / 0.55), int((CONTENT_W / 9.0 - PAD) / 0.55), int((CONTENT_W / 8.0 - PAD) / 0.55)))
io.open(os.path.join(HERE, "prewidth.txt"), "w", encoding="utf-8").write(u"\n".join(out))
print("blocks", len(bad))
