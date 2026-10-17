# -*- coding: utf-8 -*-
"""hlbattery.py —— 《佛陀的護欄》諸尺跑批器（第 52 輪立）。名單在本檔，不在指令裡。

緣起：歷輪『全尺覆核』其實是把十餘支尺名手打在指令裡；新立之尺一旦忘了補進指令，永遠不會
    被跑到，報告照樣寫『諸尺俱清』（同 battery.py 於他冊所記『名單之外』之敗）。本冊又添一
    重路徑之險：正文檔第 52 輪才搬回工作資料夾，此前 49 支工具各別硬編舊位址。故立兩件：
 ① 逐尺跑 `_work/<尺>.py`，獨立取 rc（不以管線尾端之 rc 冒充），跑前跑後各量一次正文檔之
    SHA-256——校驗器本身若偷偷改稿，此關即紅。
 ② 防漏列：凡 docstring 首行自稱 `尺（檔名）` 者，須在 RULERS 或 ARGV_ONLY 上，未列點名退 1。
    （舊尺不自稱者不可枚舉，只防『新加的尺沒入冊』這一向漂移。）

用法：
    python -X utf8 _work/hlbattery.py                 # 全跑
    python -X utf8 _work/hlbattery.py --only=sigchk,punctchk
退出碼：任一尺退非 0、正文檔被改、有未列之尺 → 1。
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import hashlib
import io
import os
import re
import subprocess
import sys

ROOT = HP.ROOT
HERE = os.path.dirname(os.path.abspath(__file__))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RULERS = ["srccchk", "hlchk", "ordchk", "refchk", "apxchk", "claimchk", "sigchk",
          "punctchk", "tocsync", "gapcensus", "simp_sweep", "starbal", "h4seq",
          "hlface", "fence_audit", "exchkr", "case_inventory"]
# 需外部參數（草稿檔／待檢檔／中介檔）者，跑批不跑，只入冊防漂移
ARGV_ONLY = ["inschk", "hl_unseen", "fence_size", "hl_render", "draft_clean",
             "topic_audit"]
# 三支有寫檔之路，然俱在 argv 閘之後（第 52 輪逐支讀碼：tocsync L117 --go、
# exchkr L57 not GO 即 exit、simp_sweep L42 argv[1]=="fix"）→ 不帶參只量不改
GATED = {"tocsync", "exchkr", "simp_sweep"}

UNGUARDED = re.compile(
    r"open\([^)\n]*(?:BOOK|HP\.SRC|hulan_path\.SRC)[^)\n]*[\"'][wab]")
DECL = re.compile(r'"""[^\n]*尺（([A-Za-z0-9_]+)）')

only = None
for a in sys.argv[1:]:
    if a.startswith("--only="):
        only = [x for x in a[7:].split(",") if x]
todo = only or RULERS

# ── 漂移檢查 ────────────────────────────────────────────────────────────────
drift = []
for fn in sorted(os.listdir(HERE)):
    if not fn.endswith(".py"):
        continue
    stem = fn[:-3]
    head = "".join(io.open(os.path.join(HERE, fn), encoding="utf-8",
                           errors="replace").readlines()[:3])
    m = DECL.search(head)
    if m and m.group(1) == stem and stem not in RULERS and stem not in ARGV_ONLY:
        drift.append(stem)

# ── 逐尺跑 ─────────────────────────────────────────────────────────────────
H0 = hashlib.sha256(io.open(HP.SRC, "rb").read()).hexdigest()
env = dict(os.environ)
env["PYTHONIOENCODING"] = "utf-8"
env["PYTHONPATH"] = "."
print("SRC = %s" % HP.SRC)
print("%-15s %-4s %-6s %s" % ("尺", "rc", "gate", "末行"))
bad = []
for name in todo:
    p = os.path.join(HERE, name + ".py")
    if not os.path.isfile(p):
        print("%-15s %-4s %-6s %s" % (name, "??", "-", "MISSING"))
        bad.append(name)
        continue
    t = io.open(p, encoding="utf-8", errors="replace").read()
    gated = bool(UNGUARDED.search(t))
    if gated and name not in GATED:
        print("%-15s %-4s %-6s %s" % (name, "SKIP", "WRITE", "無閘寫檔，不可當校驗跑"))
        bad.append(name)
        continue
    r = subprocess.run([sys.executable, "-X", "utf8", p], cwd=ROOT,
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=env)
    ls = [l.strip() for l in (r.stdout or "").splitlines() if l.strip()]
    print("%-15s %-4d %-6s %s" % (name, r.returncode, "gated" if gated else "ro",
                                  " ⏎ ".join(ls[-2:])[:118]))
    if r.returncode != 0:
        bad.append(name)
        for l in ls[-14:]:
            print("      | " + l[:150])
        if r.stderr and r.stderr.strip():
            print("      ! " + r.stderr.strip()[:400])

H1 = hashlib.sha256(io.open(HP.SRC, "rb").read()).hexdigest()
if H0 != H1:
    print("✗ 跑批過程中正文檔被改了：%s → %s" % (H0[:12], H1[:12]))
    bad.append("BOOK-MUTATED")
else:
    print("正文檔未動：%s（%d bytes）" % (H1[:16], os.path.getsize(HP.SRC)))
if drift:
    print("✗ 自稱『尺（名）』而未入冊者：%s" % ",".join(drift))
else:
    print("漂移檢：自稱尺（名）者俱在冊")
rc = 1 if (bad or drift) else 0
print("== 護欄跑批：%d 尺｜不合格 %s" % (len(todo), bad or "無"))
sys.exit(rc)
