# -*- coding: utf-8 -*-
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(ROOT, "ver38" + u"\u56db\u5206\u5f8b_\u8d77\u5fc3\u52d5\u5ff5\u5fc3\u667a\u5206\u6790\u6846\u67b6_\u4fee\u6b63\u7248.md")
GO = "--go" in sys.argv

raw = io.open(F, encoding="utf-8", newline="").read()
NL = "\r\n" if "\r\n" in raw else "\n"
lines = raw.split(NL)
n0, cr0 = len(lines), raw.count("\r\n")


def cw(s):                                   # 格寬口徑同 build_hulan.cw_units
    return sum(2 if ord(c) > 0x2E80 else 1 for c in s)


E = []
# 刀一・附錄E 導讀：去「120/120」與「合規率 100.0%」之驗收語，其義改從書中本語（校驗程序・當場核得）
E.append((
    u"本欄現存引號片段 **120/120 全部逐字可查得**（合規率 100.0%，百列中有引文之 99 列皆然，"
    u"餘一列依本表三態之「未造逐字引文」正當著錄），不再有部分案例為縮寫撮要之情形",
    u"本欄現存引號片段**俱可逐字查得**（其數不固化於此，一以本書校驗程序當場核得為準，免一數兩載而互異），"
    u"不再有部分案例為縮寫撮要之情形；至本表三態之『未造逐字引文』一式，乃正當著錄而非闕漏"))

# 刀二・附錄I-3：削行數之自報（隨輪變動之計數勿寫進散文），標題與圍欄格位同去，格寬斷言不變
E.append((u"### I-3\u3000核心命題錨定索引（二十三行全表）", u"### I-3\u3000核心命題錨定索引表"))
E.append((u"#### 二、核心命題錨定索引二十三行標準總表", u"#### 二、核心命題錨定索引標準總表"))
E.append((
    u"本索引表共計十六組核心主題；其中「八大正理」獨立拆分為八行（正理一至正理八），"
    u"故全表**精確計為二十三行**，為全書核心法理之索引網絡。",
    u"本索引表以十六組核心主題為目；其中「八大正理」獨立拆為八行（正理一至正理八），"
    u"逐行各標其深度錨定之所在，為全書核心法理之索引網絡。"))
OLDCELL = u"  \u2502 核心命題錨定索引（二十三行）  \u2502"
PRE = u"  \u2502 核心命題錨定索引"
NEWCELL = PRE + " " * (cw(OLDCELL) - cw(PRE) - 1) + u"\u2502"      # 減右界那一格，格寬方不失
E.append((OLDCELL, NEWCELL))

# 刀三・附錄H-0：削「348 減 326」之答難排解，留口徑定義（語料復算之書中對應說明，不可去）
E.append((
    u"二者**口徑定義不同、不可相加相減**（348 減 326 之差，即源於此口徑差異，並非 22 則案例未經判定）。",
    u"二者**口徑定義不同、不可相加相減**。"))

print(u"刀數 %d｜行 %d｜CR %d" % (len(E), n0, cr0))
bad = []
for old, new in E:
    c = raw.count(old)
    if c != 1:
        bad.append((c, old[:40]))
        continue
    print(u"  命中 %d｜%s" % (c, old[:52].replace(NL, "")))
if cw(OLDCELL) != cw(NEWCELL):
    bad.append(("格寬異", cw(OLDCELL), cw(NEWCELL)))
    print(u"  ✗ 圍欄格寬：舊 %d 新 %d" % (cw(OLDCELL), cw(NEWCELL)))
else:
    print(u"  圍欄格寬不變：%d 格" % cw(OLDCELL))
if bad:
    for b in bad:
        print(u"  ✗ %s" % (b,))
    raise SystemExit(u"預檢未過，一字未寫")
if not GO:
    raise SystemExit(u"試跑畢；加 --go 方寫檔")

out = raw
for old, new in E:
    out = out.replace(old, new, 1)
io.open(F, "w", encoding="utf-8", newline="").write(out)

# 回讀自證：新形俱在・舊形俱失・行數與 CRLF 不變
chk = io.open(F, encoding="utf-8", newline="").read()
errs = []
for old, new in E:
    if chk.count(new) != 1:
        errs.append(u"新形未立：%s" % new[:40])
    if chk.count(old) != 0:
        errs.append(u"舊形猶在：%s" % old[:40])
if len(chk.split(NL)) != n0 or chk.count("\r\n") != cr0:
    errs.append(u"行數或 EOL 走樣：%d/%d vs %d/%d" % (len(chk.split(NL)), chk.count("\r\n"), n0, cr0))
print(u"== 回讀：%s ==" % (u"全中（行 %d・CR %d 俱不變）" % (n0, cr0)) if not errs else u"有失")
for e in errs:
    print(u"  ✗ " + e)
sys.exit(1 if errs else 0)
