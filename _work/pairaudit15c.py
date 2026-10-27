# -*- coding: utf-8 -*-
"""第十五波・取證第三輪：口宣句式之律形・式樣軟探之名冊・二十章之戶口・工具箱三段之身。"""
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
V39 = os.path.join(ROOT, u"ver39四分律_起心動念心智分析框架_修正版.md")


def rd(p):
    return io.open(p, encoding="utf-8-sig").read().replace("\r\n", "\n").split("\n")


A, B, V = rd(F1), rd(F2), rd(V39)
VR = _tk.norm(_tk.VINAYA)
RAW = _tk.VINAYA

print("=" * 74)
print("壹・甲2① —— 『捨別住』在本律之實形（口宣句式須照律）")
for w in (u"別住", u"捨", u"摩那埵"):
    print("   『%s』本律見 %d 處" % (w, VR.count(_tk.norm(w))))
idx = [m.start() for m in re.finditer(u"別住", RAW)]
print("   『別住』原形 %d 見；其前後 26 字之窗（前 14 枚）：" % len(idx))
seen = set()
for i in idx:
    win = RAW[max(0, i - 14):i + 14].replace("\n", "")
    key = win[:8]
    if key in seen:
        continue
    seen.add(key)
    mark = u"←捨" if (u"捨" in win or u"舍" in win) else u""
    print("      @%-7d %s %s" % (i, win, mark))
    if len(seen) >= 14:
        break
print("   『我共汝作伴』之窗與所在之檔：")
j = RAW.find(u"我共汝作伴")
print("      @%d …%s…" % (j, RAW[max(0, j - 34):j + 34].replace("\n", "")))
for p in sorted(glob.glob(os.path.join(ROOT, u"原文", u"*.txt"))):
    t = _tk.read(p)
    if u"我共汝作伴" in _tk.norm(t):
        print("      檔：%s" % os.path.basename(p))
print("   F1・F2 今檔之『我共汝作伴』落點：")
for nm, L in ((u"F1", A), (u"F2", B)):
    for i, l in enumerate(L, 1):
        if u"我共汝作伴" in l:
            print("      %s L%d|%s" % (nm, i, l.strip()[:96]))

print("=" * 74)
print("貳・乙3 —— 全冊『「…」』而左側無出處者之名冊（軟探・非病灶之數）")
GATE = re.compile(u"[《本]｜本地|卷[一二三四五六七八九十]|之檔|大正藏")
for nm, L in ((u"F1", A), (u"F2", B)):
    print("   ■ %s" % nm)
    for i, l in enumerate(L, 1):
        for m in re.finditer(u"「[^」]{6,}」", l):
            left = l[max(0, m.start() - 46):m.start()]
            if re.search(u"《|本地|卷[一二三四五六七八九十百]|之檔|大正藏|律作|原典", left):
                continue
            print("      L%-5d %s" % (i, m.group(0)[:56]))
print("   ── 三句之語料實形：")
for w in (u"以利養故生嫉妬心", u"以利養故生嫉妒心", u"心懷弊惡", u"染污心", u"身相觸"):
    print("      『%s』本律 %d 見｜F1 %d 見｜F2 %d 見"
          % (w, VR.count(_tk.norm(w)), sum(1 for l in A if w in l), sum(1 for l in B if w in l)))
for w in (u"以利養故", u"生嫉妒心", u"弊惡"):
    j = VR.find(_tk.norm(w))
    print("      『%s』首見@%d …%s…" % (w, j, _tk.VINAYA[max(0, j - 20):j + 26].replace("\n", "") if j >= 0 else ""))

print("=" * 74)
print("參・戊1 —— ver39 工具箱三段之身＋F2 第二十章之戶口＋四署今形")
print("   九則引橋 L7012–L7028：")
for i in range(7011, 7029):
    if V[i].strip():
        print("      L%d|%s" % (i + 1, V[i][:94]))
print("   四大行動卡 L7029–L7060 之目：")
for i in range(7028, 7112):
    if re.match(r"^\s*(#{1,6}\s|\*\*)", V[i]) or u"卡" in V[i][:12]:
        print("      L%d|%s" % (i + 1, V[i][:88]))
print("   自檢表 L7112–L7133 之首尾：")
for i in range(7111, 7134):
    if V[i].strip():
        print("      L%d|%s" % (i + 1, V[i][:90]))
hs = [(i + 1, len(m.group(1)), m.group(2).strip())
      for i, l in enumerate(B) for m in [re.match(r"^(#{1,6})\s+(\S.*)$", l)] if m]
c0 = next(ln for ln, lv, t in hs if t.startswith(u"第二十章"))
nxt = next((ln for ln, lv, t in hs if ln > c0 and lv <= 3), len(B) + 1)
print("   F2 第二十章 L%d–L%d・其下之節：" % (c0, nxt - 1))
for ln, lv, t in hs:
    if c0 <= ln < nxt and lv <= 3:
        print("      H%d L%d %s" % (lv, ln, t[:62]))
print("   F2『四署』%d 見｜F1 %d 見｜ver39 %d 見" % (sum(1 for l in B if u"四署" in l),
      sum(1 for l in A if u"四署" in l), sum(1 for l in V if u"四署" in l)))
for i, l in enumerate(B, 1):
    if u"四署" in l:
        print("      F2 L%d|%s" % (i, l.strip()[:92]))
print("   F2『一票否決』%d 見：%s" % (sum(1 for l in B if u"一票否決" in l),
      "、".join(str(i + 1) for i, l in enumerate(B) if u"一票否決" in l)[:70]))
print("   ver39 L6570–L6590（四署宣告之原形）：")
for i in range(6569, 6590):
    if V[i].strip():
        print("      L%d|%s" % (i + 1, V[i][:88]))
