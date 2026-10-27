# -*- coding: utf-8 -*-
"""第十五波・取證第二輪：語料實形（甲2①・乙3）・細字定位（丁2）・工具箱原文（戊1）・章節之細（甲3）。"""
import io
import os
import re
import sys

import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import _tk                                            # noqa: E402

F1 = next(os.path.join(ROOT, x) for x in os.listdir(ROOT) if x.startswith(u"起心動念") and x.endswith(u".txt"))
F2 = next(os.path.join(ROOT, x) for x in os.listdir(ROOT) if x.startswith(u"如法推尋") and x.endswith(u".txt"))
V39 = os.path.join(ROOT, u"ver39四分律_起心動念心智分析框架_修正版.md")


def rd(p):
    return io.open(p, encoding="utf-8-sig").read().replace("\r\n", "\n").split("\n")


print("=" * 74)
print("壹・丁3 —— 兩冊冊首八行之對稱")
for nm, p in ((u"F1", F1), (u"F2", F2)):
    L = rd(p)
    print("   %s：" % nm)
    for i, l in enumerate(L[:8], 1):
        print("      L%d|%s" % (i, l[:88]))

print("=" * 74)
print("貳・乙3 —— 三段式樣之語料實形")
A = rd(F1)
B = rd(F2)
for w in (u"染污心", u"分惡房", u"徇自名利", u"不耐他榮", u"妒忌為性", u"瞋恚一分"):
    for i, l in enumerate(A, 1):
        if w in l:
            print("   F1 L%-5d %s" % (i, l.strip()[:120]))
print("   ── 語料對勘（_tk.norm＋FOLD）：")
for w in (u"染污心共染污心男子身相觸", u"分惡房", u"惡房", u"徇自名利", u"不耐他榮",
          u"妒忌為性", u"瞋恚一分為體", u"嫉妒"):
    v = _tk.norm(w)
    hit = _tk.norm(_tk.VINAYA).find(v)
    oth = [(k, _tk.norm(x).find(v)) for k, x in _tk.OTHER.items() if _tk.norm(x).find(v) >= 0]
    print("      『%s』本律 %s｜他典 %s" % (w, ("見@%d" % hit) if hit >= 0 else "0 見",
                                          "、".join("%s@%d" % (k[-14:], j) for k, j in oth[:3]) or "無"))
print("   ── 成唯識論之嫉條原文（取窗）：")
for k in _tk.OTHER:
    if u"唯識" in k:
        t = _tk.OTHER[k]
        j = t.find(u"徇自名利")
        if j >= 0:
            print("      檔『%s』…%s…" % (k[-16:], t[max(0, j - 40):j + 40].replace("\n", "")))
print("   ── 『卷六／卷八』之嫉在《成唯識論》本地檔之卷次標記：")
for k in _tk.OTHER:
    if u"唯識" in k:
        t = _tk.OTHER[k]
        j = t.find(u"徇自名利")
        if j >= 0:
            seg = t[:j]
            vols = re.findall(u"卷([一二三四五六七八九十百]+)", seg)
            print("      前文所見『卷N』%s" % (vols[-3:] if vols else "無"))

print("=" * 74)
print("參・甲2① —— 新節文本之逐字宣稱須先見形於語料")
for w in (u"我共汝作伴", u"共汝作伴", u"捨別住", u"舍別住", u"摩那埤", u"摩那埵", u"白四羯磨",
          u"二十清淨大僧", u"二十僧", u"出罪"):
    v = _tk.norm(w)
    hit = _tk.norm(_tk.VINAYA).find(v)
    print("      『%s』本律 %s｜F1 今檔 %d 見｜F2 今檔 %d 見"
          % (w, ("見@%d" % hit) if hit >= 0 else "0 見",
             sum(1 for l in A if w in l), sum(1 for l in B if w in l)))
print("   今節（L3017–L3049）之全文：")
for i in range(3016, min(3050, len(A))):
    print("      L%d|%s" % (i + 1, A[i][:100]))

print("=" * 74)
print("肆・丁2 —— 印面細字之定位（F1 兩式）")
for ed in (u"_螢幕版", u"_影印版"):
    p = os.path.join(ROOT, "_print", u"起心動念_四分律的心智顯微鏡與唯識解剖" + ed + ".pdf")
    d = pymupdf.open(p)
    bad = []
    for i in range(d.page_count):
        lo = None
        for b in d[i].get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                for s in ln.get("spans", []):
                    if s["text"].strip() and not s["text"].strip().isdigit():
                        if lo is None or s["size"] < lo:
                            lo = s["size"]
        if lo and lo < 9.0:
            bad.append((i + 1, round(lo, 2)))
    print("   %s：9pt 以下之頁 %s" % (ed, bad))
    for pg, _ in bad[:2]:
        txt = [x for x in d[pg - 1].get_text().split("\n") if x.strip()]
        print("      p%d 首四行：%s" % (pg, " / ".join(x[:30] for x in txt[1:5])))
    d.close()

print("=" * 74)
print("伍・甲3 —— F2 十五・十六章之節細與凡例第八律")
hs = [(i + 1, len(m.group(1)), m.group(2).strip())
      for i, l in enumerate(B) for m in [re.match(r"^(#{1,6})\s+(\S.*)$", l)] if m]
for lo, hi, nm in ((3265, 3397, u"第十五章"), (3397, 3700, u"第十六章")):
    print("   %s L%d–L%d 之內：" % (nm, lo, hi))
    for ln, lv, t in hs:
        if lo <= ln < hi:
            print("      H%d L%d %s" % (lv, ln, t[:64]))
for i, l in enumerate(B, 1):
    if 3265 <= i <= 3270 or 3397 <= i <= 3402:
        print("      正文 L%d|%s" % (i, l[:92]))
print("   凡例八律之條文（F2 L163–L180）：")
for i in range(162, 180):
    if B[i].strip():
        print("      L%d|%s" % (i + 1, B[i][:96]))
print("   『子案與新增案之號』全書落點：")
for i, l in enumerate(B, 1):
    if u"新增案" in l or u"子案" in l:
        print("      L%d|%s" % (i, l.strip()[:100]))
print("   F1 L177 之引：")
print("      " + A[176][:140])

print("=" * 74)
print("陸・戊1 —— ver39 工具箱與四署／一票否決之原文")
V = rd(V39)
print("   工具箱三段 L7005–L7160 之骨架：")
for i in range(7004, min(7165, len(V))):
    l = V[i]
    if re.match(r"^#{1,6}\s", l) or u"[ ]" in l or u"[x]" in l:
        print("      L%d|%s" % (i + 1, l[:96]))
print("   其行列點之樣（前 12 條）：")
n = 0
for i in range(7004, min(7175, len(V))):
    if re.match(r"^\s*[-*]\s", V[i]):
        print("      L%d|%s" % (i + 1, V[i][:88]))
        n += 1
        if n >= 12:
            break
print("   『一票否決』ver39 落點：")
for i, l in enumerate(V, 1):
    if u"一票否決" in l:
        print("      L%d|%s" % (i, l.strip()[:96]))
print("   『四署』ver39 落點（L6570–L6615）：")
for i in range(6569, 6615):
    if V[i].strip():
        print("      L%d|%s" % (i + 1, V[i][:92]))
