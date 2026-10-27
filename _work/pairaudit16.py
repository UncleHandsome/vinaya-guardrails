# -*- coding: utf-8 -*-
"""第十六波外路報告・逐條量今檔（只量不改）。每目自印管轄與實數，偽病灶點名其誤。

目：
  甲 字型嵌入——Type0 而無嵌入檔者（Type3 之 CharProc 自足，另列不計病）
  乙 目錄號與印面——取目錄所示之號，回量該號頁之實文；並反查標題所在頁之頁腳號
  丙 引號斷行——行末『「』或行首『」』之數（禁則之失）
  丁 簡形三處——報告所引『名目里』『倾』『并妙用』在今檔有無
  戊 孤行短頁——每頁正文行數 ≤ 5 者（篇扉頁・書名頁另計）
  己 標題孤懸——書籤所指之標題为其頁最後一行，而下頁另有正文者
  庚 內部痕跡——報告所引六語在今檔之虛實
用法：python -X utf8 _work/pairaudit16.py
"""
import io
import os
import re
import sys

import pymupdf as pm

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "_print")
sys.path.insert(0, P)
import build_pair as BP                                       # noqa: E402

F1 = ROOT + os.sep + "起心動念：四分律的心智顯微鏡與唯識解剖.txt"
F2 = ROOT + os.sep + "如法推尋：僧伽憲政、法權審理與修復正義.txt"
PAIRS = [(BP.BOOKS[0], F1), (BP.BOOKS[1], F2)]


def lines_of(pg):
    out = []
    for b in pg.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            txt = "".join(s["text"] for s in ln["spans"])
            if txt.strip():
                out.append((ln["bbox"][1], ln["bbox"][3], max(s["size"] for s in ln["spans"]), txt))
    out.sort()
    return out


print("=" * 74)
print("甲 字型嵌入（掃六檔）")
for cfg, _ in PAIRS:
    for ed in ("螢幕版", "影印版"):
        f = os.path.join(P, cfg["out"] + ed + ".pdf")
        d = pm.open(f)
        bad, t3 = {}, set()
        for p in range(d.page_count):
            for x in d.get_page_fonts(p):
                if x[2] == "Type3":
                    t3.add(p + 1)
                elif x[1] in ("n/a", ""):
                    bad.setdefault((x[3] or "(無名)", x[4]), set()).add(p + 1)
        d.close()
        print("  %s｜%s：未嵌入 %d 種・Type3（自足）%d 頁 %s"
              % (cfg["key"], ed, len(bad), len(t3),
                 sorted(t3)[:6]))
        for k, v in bad.items():
            print("       ⚠ %s／%s ➔ 頁 %s（%d 頁）" % (k[0], k[1], sorted(v)[:8], len(v)))
for ed in ("螢幕版", "影印版"):
    f = os.path.join(P, BP.merged_name(ed))
    d = pm.open(f)
    bad, t3 = {}, set()
    for p in range(d.page_count):
        for x in d.get_page_fonts(p):
            if x[2] == "Type3":
                t3.add(p + 1)
            elif x[1] in ("n/a", ""):
                bad.setdefault((x[3] or "(無名)", x[4]), set()).add(p + 1)
    d.close()
    print("  合冊｜%s：未嵌入 %d 種・Type3（自足）%d 頁 %s"
          % (ed, len(bad), len(t3), sorted(t3)[:8]))
    for k, v in bad.items():
        print("       ⚠ %s／%s ➔ 頁 %s（%d 頁）" % (k[0], k[1], sorted(v)[:8], len(v)))

print("=" * 74)
print("乙 目錄號與印面（卷一第三章・卷二第一章第四五節）")
d = pm.open(os.path.join(P, BP.BOOKS[0]["out"] + "影印版.pdf"))
# 目錄行：標題＋點線＋號
toc_no = {}
for p in range(d.page_count):
    for _, _, _, t in lines_of(d[p]):
        m = re.match(r"^(第[一二三四五六七八九十]+章[　 ].*?)[.．\s]{3,}(\d+)\s*$", t.strip())
        if m:
            toc_no[m.group(1).strip()] = int(m.group(2))
for k in list(toc_no)[:3]:
    print("   目錄樣本：", k, "➔", toc_no[k])
# 頁腳號：最後一行純數字
foot = {}
for p in range(d.page_count):
    ls = lines_of(d[p])
    if ls and re.fullmatch(r"\d{1,3}", ls[-1][3].strip()):
        foot[p + 1] = int(ls[-1][3].strip())
# 第三章標題所在之物理頁
target = None
for p in range(d.page_count):
    for _, _, _, t in lines_of(d[p]):
        if re.match(r"^第三章[　 ]衡平動機", t.strip()):
            target = p + 1
            print("   第三章標題實在物理 p%d・頁腳號 %s" % (target, foot.get(target)))
            break
    if target:
        break
key = [k for k in toc_no if k.startswith("第三章 衡平") or k.startswith("第三章　衡平")]
if key:
    print("   目錄所示：『%s』➔ %s" % (key[0][:18], toc_no[key[0]]))
    print("   判：%s" % ("合" if foot.get(target) == toc_no[key[0]] else "不合"))
# 該號頁之末行（報告稱是第二章結尾）
if key:
    n = toc_no[key[0]]
    phy = [p for p, v in foot.items() if v == n]
    print("   頁腳號 %d ➔ 物理 %s" % (n, phy))
    for p in phy:
        ls = lines_of(d[p - 1])
        print("      該頁末三行：", [x[3].strip()[:18] for x in ls[-3:]])
d.close()

print("=" * 74)
print("丙 引號斷行（行末『「』／行首『」』）")
for cfg, _ in PAIRS:
    d = pm.open(os.path.join(P, cfg["out"] + "影印版.pdf"))
    end_open, start_close = [], []
    for p in range(d.page_count):
        for _, _, _, t in lines_of(d[p]):
            s = t.rstrip()
            if s.endswith(chr(0x300C)):
                end_open.append((p + 1, s[-14:]))
            if s.startswith(chr(0x300D)):
                start_close.append((p + 1, s[:14]))
    d.close()
    print("  %s：行末『「』%d 處・行首『」』%d 處" % (cfg["key"], len(end_open), len(start_close)))
    for x in (end_open + start_close)[:6]:
        print("       · p%d「%s」" % x)

print("=" * 74)
print("丁 簡形三處（報告所引）・在正本之虛實")
CASES = [("F1", F1, [u"名目里", u"名目裡", u"名目裏"]),
         ("F1", F1, [u"倾", u"傾"]),
         ("F1", F1, [u"神通并妙用", u"神通並妙用"]),
         ("F2", F2, [u"名目里", u"倾", u"并妙用"])]
for tag, fn, words in CASES:
    txt = io.open(fn, "rb").read().decode("utf-8-sig")
    print("  %s｜%s ➔ %s" % (tag, "／".join(words),
                              "、".join("%s×%d" % (w, txt.count(w)) for w in words)))

print("=" * 74)
print("戊 孤行短頁（正文行 ≤5・且非篇扉頁／書名頁）")
for cfg, _ in PAIRS:
    d = pm.open(os.path.join(P, cfg["out"] + "影印版.pdf"))
    short = []
    for p in range(d.page_count):
        ls = [x for x in lines_of(d[p]) if not re.fullmatch(r"\d{1,3}", x[3].strip())]
        big = [x for x in ls if x[2] >= 17]
        if len(ls) <= 6 and len(big) < 2:
            short.append((p + 1, len(ls), big[0][3].strip()[:16] if big else ""))
    d.close()
    print("  %s：%d 頁 ➔ %s" % (cfg["key"], len(short), short[:14]))

print("=" * 74)
print("己 標題孤懸（標題为其頁最後一行・下頁另有正文）")
for cfg, _ in PAIRS:
    d = pm.open(os.path.join(P, cfg["out"] + "影印版.pdf"))
    toc = d.get_toc()
    pages = {p: lines_of(d[p]) for p in range(d.page_count)}
    orph = []
    for lvl, title, pg in toc:
        if lvl < 3:
            continue
        key = re.sub(r"\s+", "", title)
        ls = pages[pg - 1]
        if not ls:
            continue
        last = re.sub(r"\s+", "", ls[-1][3])
        if key.startswith(last) or last.startswith(key[:12]):
            nxt = pages[pg] if pg < d.page_count else []
            if nxt:
                orph.append((pg, lvl, title[:24], round(ls[-1][2], 1)))
    d.close()
    print("  %s：%d 處" % (cfg["key"], len(orph)))
    for x in orph[:12]:
        print("       · p%d H%d %.1fpt「%s」" % (x[0], x[1], x[3], x[2]))

print("=" * 74)
print("庚 內部痕跡（報告所引六語）")
TRACE = [u"三十八版舊有", u"自動化測試報告", u"不從稿說", u"非手工抄錄", u"未盡之清創", u"破壁心智"]
for tag, fn in (("F1", F1), ("F2", F2)):
    txt = io.open(fn, "rb").read().decode("utf-8-sig")
    ls = txt.replace("\r\n", "\n").split("\n")
    for w in TRACE:
        hits = [(i + 1, l.strip()[:66]) for i, l in enumerate(ls) if w in l]
        if hits:
            print("  %s｜%s ×%d" % (tag, w, len(hits)))
            for h in hits[:2]:
                print("       L%d %s" % h)
