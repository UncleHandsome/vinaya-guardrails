# -*- coding: utf-8 -*-
"""路徑法源尺（srccchk）：本書正文檔之位址，唯 `hulan_path` 得而知之。

緣起（第 52 輪）：正文檔原在舊鏡射目錄（兩枚大寫字母為其代號），49 支工具各別硬編同一路徑；
    搬回工作資料夾須逐支改寫，而改漏一支即以後每輪拿舊路徑之殘檔為據而不自知。此即『名單之外』
    之敗在路徑層。故立此尺，四檢俱硬：
  甲 工具檔（_work/_print 之 .py）字串面值中，指向本書之絕對路徑 → 須 0
  乙 工具檔任何一行不再出現舊鏡射之代號 → 須 0
  丙 HP.SRC 須存在，且其所在層須為工作資料夾根或 `_archive/舊本`（2026-10-18 奉令：兩本舊本移出正本層，
     唯仍作合編之素材與逐字校據，故舊尺照跑），且該層恰有此檔一支
  丁 桌面他處之同名檔：與正本全等、或改動時間不早於正本者 → 須 0（此二類皆『兩份正本』之形；
    明顯較舊之殘稿只軟報列出，不判死——殘稿在作者自己目錄內，刪否非尺所裁）
退出碼：任一不合格 1。
用法：python -X utf8 _work/srccchk.py
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = HP.ROOT
BN = os.path.basename(HP.SRC)
PREFIX = HP.PREFIX
SEED = "".join(chr(c) for c in (0x58, 0x57))          # 舊鏡射目錄之代號（兩枚大寫字母）
ABS_TXT = re.compile(r"[\"'](?:[A-Za-z]:[\\\\/][^\"'\n]*|[\\\\/]{2}[^\"'\n]*\.txt)[\"']")

fails = []


def live_tools():
    for sub in ("_work", "_print"):
        d = os.path.join(ROOT, sub)
        for dirpath, dirnames, filenames in os.walk(d):
            dirnames[:] = [x for x in dirnames
                           if x != "__pycache__" and not x.startswith("_retired")]
            for fn in filenames:
                if fn.endswith(".py"):
                    yield os.path.join(dirpath, fn)


n_a = n_b = n_files = 0
for fp in live_tools():
    rel = os.path.relpath(fp, ROOT)
    if rel.endswith("hulan_path.py"):
        continue
    n_files += 1
    lines = io.open(fp, encoding="utf-8", errors="replace").read().splitlines()
    for i, l in enumerate(lines, 1):
        if SEED in l:
            n_b += 1
            fails.append(u"乙 %s:%d 殘留舊鏡射代號 → %s" % (rel, i, l.strip()[:70]))
        for m in ABS_TXT.findall(l):
            if os.path.basename(m.strip("\"'")).startswith(PREFIX):
                n_a += 1
                fails.append(u"甲 %s:%d 硬編正文檔路徑 → %s" % (rel, i, l.strip()[:70]))
print(u"甲 硬編路徑 %d 處｜乙 舊徑殘留 %d 處｜工具檔 %d 支" % (n_a, n_b, n_files))

BASES = [ROOT, os.path.join(ROOT, "_archive", u"舊本")]   # 舊 = U+820A（勿誤寫 U+8208「興」）
src_dir = os.path.dirname(HP.SRC) if HP.SRC else None
ok_c = bool(src_dir) and os.path.isfile(HP.SRC) and src_dir in BASES
layer_hits = [f for f in os.listdir(src_dir)] if src_dir and os.path.isdir(src_dir) else []
layer_hits = [f for f in layer_hits if f.startswith(PREFIX) and f.endswith(".txt")]
if not ok_c or len(layer_hits) != 1:
    fails.append(u"丙 HP.SRC 所在層非根目錄亦非 `_archive/舊本`，或該層不止一支：%s" % layer_hits)
print(u"丙 HP.SRC＝該層之唯一 護欄 檔：%s（所在層 %s・該層 %d 支）"
      % (ok_c and len(layer_hits) == 1, os.path.relpath(src_dir or ".", ROOT), len(layer_hits)))

n_d = 0
n_soft = 0
home = os.path.expanduser("~")
desk = None
for cand in (os.path.join(home, "OneDrive", u"\u684c\u9762"), os.path.join(home, u"\u684c\u9762")):
    if os.path.isdir(cand):
        desk = cand
        break
SKIP = {"Python", "__pycache__", "node_modules", "cbeta", "wiki_juan", "cache", "Cache"}
if desk:
    import hashlib
    import time
    live_h = hashlib.sha256(io.open(HP.SRC, "rb").read()).hexdigest()
    live_m = os.path.getmtime(HP.SRC)
    for dirpath, dirnames, filenames in os.walk(desk):
        depth = dirpath[len(desk):].count(os.sep)
        dirnames[:] = [x for x in dirnames if x not in SKIP and not x.startswith(".")]
        if depth >= 4:
            dirnames[:] = []
        for fn in filenames:
            if fn != BN:
                continue
            fp = os.path.join(dirpath, fn)
            if os.path.abspath(fp) == os.path.abspath(HP.SRC):
                continue
            b = io.open(fp, "rb").read()
            tag = "size=%d sha=%s mt=%s" % (
                len(b), hashlib.sha256(b).hexdigest()[:12],
                time.strftime("%Y-%m-%d %H:%M",
                              time.localtime(os.path.getmtime(fp))))
            if hashlib.sha256(b).hexdigest() == live_h:
                n_d += 1
                fails.append(u"丁 與正本全等之外份（兩份正本必有一份是陷阱）：%s｜%s" % (fp, tag))
            elif os.path.getmtime(fp) >= live_m:
                n_d += 1
                fails.append(u"丁 不早於正本之外份（恐為平行改稿，正本 mt=%s）：%s｜%s" % (
                    time.strftime("%Y-%m-%d %H:%M", time.localtime(live_m)), fp, tag))
            else:
                n_soft += 1
                print(u"  · 軟報 舊同名稿（不在正本之災，惟勿誤編輯）：%s｜%s" % (fp, tag))
    print(u"丁 桌面同名檔：硬病 %d 處｜較舊之稿 %d 處（掃描深度 ≤4）" % (n_d, n_soft))
else:
    print(u"丁 找不到桌面目錄，此檢未行")

for f in fails[:20]:
    print(u"  ✗ " + f)
print(u"判：甲乙丁須 0、丙須真｜今 %s" % (u"合格" if not fails else u"不合格（%d 項）" % len(fails)))
sys.exit(1 if fails else 0)
