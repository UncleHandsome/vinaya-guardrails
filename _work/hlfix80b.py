# -*- coding: utf-8 -*-
"""第 80 輪・外路第廿九報之三刀（俱以今冊量得之真病，非報告之推測）：
   甲、『（今依其通說譯為漢言，非逐字）：  ：』——多一冒號與尾空白（源 L3839 即如此，非排印之誤）。
   乙、第十章前『---』連書兩行——pandoc 以後行者為 setext 之 underline，遂於第十章題上印出孤立『—』
       （實測 p108 上緣 x=64 處一枚「—」在 H1 之上）；削其一。
   丙、第三部・第四部有目無題——目錄兩條在，正文卻無 `# 【第N部…】` 之 Banner，
       配對於是落『近似0.44／承上』，兩部之號俱作 181（實測 _tocaudit）。今依第二部之式補之：
       在『---』與章題之間立 Banner，其字取目錄之條（不重打）。
"""
import hashlib
import io
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import hulan_path as HP                                        # noqa: E402

GO = u"--go" in sys.argv
raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
L = raw.split(u"\r\n")
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
errs, log = [], []


def uniq(pred, what):
    got = [i for i, s in enumerate(L) if pred(s)]
    if len(got) != 1:
        errs.append(u"%s 命中 %d（宜 1）" % (what, len(got)))
        return None
    return got[0]


# 甲・雙冒號
i = uniq(lambda s: u"非逐字）：  ：" in s, u"雙冒號行")
if i is not None:
    new = L[i].replace(u"非逐字）：  ：", u"非逐字）：").rstrip()
    log.append((u"甲", i + 1, L[i][-26:], new[-26:]))
    L[i] = new

# 乙・重複之 ---
dup = [k for k in range(len(L) - 1) if L[k].strip() == u"---" and L[k + 1].strip() == u"---"]
if len(dup) != 1:
    errs.append(u"連書『---』之對數 %d（宜 1）" % len(dup))
else:
    k = dup[0]
    log.append((u"乙", k + 2, u"'---'", u"（削）"))
    del L[k + 1]

# 丙・補二部題（字取目錄之條）
for cn, key in ((u"十二", u"第三部"), (u"十六", u"第四部")):
    toc = uniq(lambda s: s.startswith(u"### **【" + key + u"："), u"目錄之【%s】條" % key)
    if toc is None:
        continue
    banner = u"# " + L[toc].strip()[len(u"### **"):-len(u"**")]
    hidx = uniq(lambda s: s.startswith(u"# 第" + cn + u"章"), u"第%s章 H1" % cn)
    if hidx is None:
        continue
    if not (L[hidx - 2].strip() == u"---" and L[hidx - 1].strip() == u""):
        errs.append(u"第%s章前非『---＋空行』：%r" % (cn, [L[hidx - 2][:12], L[hidx - 1][:12]]))
        continue
    L[hidx:hidx] = [banner, u"", u"---", u""]
    log.append((u"丙", hidx + 1, u"（原第%s章處）" % cn, banner[:30]))

for tag, ln, a, b in log:
    print(u"%s｜L%-5d %s → %s" % (tag, ln, a, b))
if errs:
    for e in errs:
        print(u"✗ " + e)
    sys.exit(1)
print(u"行數 %d → %d" % (len(raw.split(u"\r\n")), len(L)))
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
BK = HP.bakpath(u"80b")
io.open(BK, "wb").write(raw.encode("utf-8"))
out = u"\r\n".join(L)
for k in range(3):
    try:
        io.open(HP.SRC, "wb").write(out.encode("utf-8"))
        break
    except OSError as e:
        print(u"  寫檔重試 %d：%s" % (k + 1, e))
        time.sleep(2)
chk = io.open(HP.SRC, "rb").read().decode("utf-8")
print(u"已寫檔｜sha %s→%s｜回讀%s｜備份 %s" % (
    sha0, hashlib.sha256(chk.encode("utf-8")).hexdigest()[:12],
    u"全等" if chk == out else u"不等!", os.path.relpath(BK, ROOT)))
