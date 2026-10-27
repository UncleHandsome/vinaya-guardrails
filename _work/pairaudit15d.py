# -*- coding: utf-8 -*-
"""第十五波・取證第四輪：稱名之各抄本・卷段之檔名・款級之靶・兩圖之身。"""
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import _tk                                            # noqa: E402

F1 = next(os.path.join(ROOT, x) for x in os.listdir(ROOT) if x.startswith(u"起心動念") and x.endswith(u".txt"))
F2 = next(os.path.join(ROOT, x) for x in os.listdir(ROOT) if x.startswith(u"如法推尋") and x.endswith(u".txt"))


def rd(p):
    return io.open(p, encoding="utf-8-sig").read().replace("\r\n", "\n").split("\n")


A, B = rd(F1), rd(F2)

print("=" * 74)
print("壹・稱名之抄 —— 十五/十六/二十章・二分法相・案卷 103〜105 之全落點")
for w in (u"第十五章", u"第十六章", u"第二十章", u"二分法相", u"審理主幹", u"言詞問"):
    for nm, L in ((u"F1", A), (u"F2", B)):
        for i, l in enumerate(L, 1):
            if w in l:
                print("   『%s』%s L%-5d %s" % (w, nm, i, l.strip()[:88]))
for w in (u"案卷 103", u"案卷 104", u"案卷 105", u"瞻病犍度", u"亡僧遺物"):
    for i, l in enumerate(B, 1):
        if w in l:
            print("   『%s』F2 L%-5d %s" % (w, i, l.strip()[:84]))

print("=" * 74)
print("貳・全貌圖與三級收納（F2 卷首）")
fs, st = [], False
for l in B:
    if re.match(r"^\s*(```|~~~)", l):
        st = not st
    fs.append(st)
for i, l in enumerate(B, 1):
    if 20 <= i <= 160 and (u"第十五章" in l or u"第十六章" in l or u"第二十章" in l):
        print("   L%-4d%s|%s" % (i, u"〔柵〕" if fs[i - 1] else u"", l[:100]))
print("   ── E2 三級收纳之身：")
for i, l in enumerate(B, 1):
    if i < 260 and (u"三級" in l or u"查考" in l or u"記憶" in l):
        print("      L%-4d%s|%s" % (i, u"〔柵〕" if fs[i - 1] else u"", l[:96]))
print("   凡例第八律全文（L173）：")
print("      " + B[172][:200])

print("=" * 74)
print("參・乙2 —— 款級／目級標題帶企業專名者")
TERMS = (u"董事會", u"監事會", u"三線", u"非營利", u"SOP", u"KPI", u"穿透審計",
         u"實質受益人", u"機構化", u"合規", u"稽核", u"法人")
for nm, L in ((u"F1", A), (u"F2", B)):
    for i, l in enumerate(L, 1):
        m = re.match(r"^(#{1,6})\s+(\S.*)$", l)
        if m and any(t in m.group(2) for t in TERMS):
            print("   %s H%d L%-5d %s" % (nm, len(m.group(1)), i, m.group(2)[:78]))
print("   ── 企業專名之全部落點（F2・含圍欄內）：")
for t in TERMS:
    for i, l in enumerate(B, 1):
        if t in l:
            print("      %-9s L%-5d%s %s" % (t, i, u"〔柵〕" if fs[i - 1] else u"", l.strip()[:74]))

print("=" * 74)
print("肆・丁2 —— F1 兩張對照圖之全文（柵 #22・#23）")
op = [i for i, l in enumerate(A) if re.match(r"^\s*```", l)]
for k in range(0, len(op) - 1, 2):
    lo, hi = op[k], op[k + 1]
    body = A[lo + 1:hi]
    tag = body[1] if len(body) > 1 else body[0]
    if u"發動鏈對照" not in tag:
        continue
    print("   ── 柵 L%d–L%d・行 %d：" % (lo + 1, hi + 1, len(body)))
    for x in body:
        w = sum(2 if ord(c) > 0x2000 else 1 for c in x)
        print("      [%3d] %s" % (w, x[:100]))

print("=" * 74)
print("伍・本地卷段之檔名（新引兩條須定其檔）")
for needle in (u"我共汝作伴", u"以利養故生嫉妬心", u"內懷弊惡", u"徇自名利"):
    files = []
    for p in sorted(glob.glob(os.path.join(ROOT, u"原文", u"*.txt"))):
        try:
            if needle in _tk.norm(_tk.read(p)):
                files.append(os.path.basename(p))
        except Exception as e:
            print("      讀檔失敗 %s：%s" % (os.path.basename(p), e))
    for p in sorted(glob.glob(os.path.join(ROOT, u"佛經", u"**", u"*.txt"), recursive=True)):
        if needle in _tk.norm(io.open(p, encoding="utf-8", errors="replace").read()):
            files.append(os.path.relpath(p, ROOT))
    print("   『%s』見於：%s" % (needle, "、".join(files) or "無"))
for p in sorted(glob.glob(os.path.join(ROOT, u"佛經", u"成唯識論", u"*.txt"))):
    t = io.open(p, encoding="utf-8", errors="replace").read()
    print("      檔 %s・長 %d・其卷標：%s" % (os.path.basename(p), len(t),
          "、".join(re.findall(u"卷[一二三四五六七八九十]+", t[:400])[:3]) or "首段無"))
