# -*- coding: utf-8 -*-
"""清場搬移器：逐名列檔（不用前綴通配），試跑印名，落刀前復核；寫清冊、可單行復原。

用法：
  python -X utf8 _merge/tidy_move.py            # 試跑：只印拟搬之名與size，不動檔
  python -X utf8 _merge/tidy_move.py --go       # 落刀
"""
import os, sys, io, shutil, hashlib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GO = "--go" in sys.argv

# 拟搬之名（逐枚列檔・無通配）
# 註：`ver35／ver36／verify31-32-35／ref.txt` **不搬**——列印SOP 第 82 行明文載其位於 `_archive/`，
#     且 `_work/clean82.py` 依名取用；改其座次即壞記錄檔之宣稱（一處宣稱須窮舉其載體）。
BAK = [
    "_archive/主檔備份-20261016-底冊未移.md",
    "_archive/佛陀的護欄_backup_20261015_波羅夷章前.txt",
    "_archive/佛陀的護欄_backup_20261015_圍欄重排前.txt",
    "_archive/佛陀的護欄_backup_20261015_簡形修前.txt",
    "_archive/佛陀的護欄_backup_20261015_補八案前.txt",
    "_archive/佛陀的護欄_backup_20261015_補八案乙前.txt",
    "_archive/佛陀的護欄_backup_20261015_補八案丙前.txt",
    "_archive/佛陀的護欄_backup_20261015_補九案前.txt",
    "_archive/佛陀的護欄_backup_20261015_補十一案前.txt",
    "_work/bak_r13.txt",
]
ONE_TIME_TOOLS = [
    "_archive/r19move.py",
    "_archive/r19repoint.py",
    "_work/r16fix.py",
    "_work/r170negtest.py",
    "_work/r173negtest.py",
    "_work/r179sync.py",
    "_work/r180negtest.py",
    "_work/r215negtest.py",
    "_work/r236gate.py",
]
WORK_OUTPUTS = [
    "_work/verify_bq.txt",
    "_work/verify_bqa.txt",
    "_work/verify_c6.txt",
    "_work/verify_f.txt",
]
DEST = {"BAK": "_archive/備份", "ONE_TIME_TOOLS": "_archive/一次性",
        "WORK_OUTPUTS": "_archive/一次性/產出"}
GROUPS = [("BAK", BAK), ("ONE_TIME_TOOLS", ONE_TIME_TOOLS), ("WORK_OUTPUTS", WORK_OUTPUTS)]

# 不可動之釘死檔（先自證：這些路徑須仍在原處，且不在拟搬之列）
PINNED = ["_archive/編纂底冊.md", "_archive/編年工程日誌.md", "ver38四分律_起心動念心智分析框架_修正版.md",
          "列印SOP.md", "_tk.py", "hulan_path.py", "verify_audit.py",
          "_archive/ver35四分律_起心動念心智分析框架_修正版.md",
          "_archive/ver36四分律_起心動念心智分析框架_修正版.md",
          "_archive/ref.txt", "_archive/verify31.py", "_archive/verify32.py", "_archive/verify35.py"]


def sha(p, n=16):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:n] if os.path.isfile(p) else "缺失"


print("== 0. 釘死檔自證（這些須原地不動且仍在原處）==")
bad = [p for p in PINNED if not os.path.isfile(os.path.join(ROOT, p))]
for p in PINNED:
    print("  %-56s %s" % (p, "在原處" if os.path.isfile(os.path.join(ROOT, p)) else "★不見★"))
inlist = {x for _, g in GROUPS for x in g}
clash = [p for p in PINNED if p in inlist]
assert not bad and not clash, "釘死檔有失或缺，中止"

bookA = os.path.join(ROOT, "ver38四分律_起心動念心智分析框架_修正版.md")
sys.path.insert(0, ROOT)
import hulan_path as HP          # 護欄正本之路徑唯一起點，不另立第二份判準
bookB = HP.SRC
pre = {bookA: sha(bookA), bookB: sha(bookB)}
print("\n== 1. 正本跑前 SHA ==")
for k, v in pre.items():
    print("  %s  %s" % (v, os.path.basename(k)[:30]))

print("\n== 2. 拟搬（%s）==" % ("落刀" if GO else "試跑"))
moves, total = [], 0
for gname, grp in GROUPS:
    d = os.path.join(ROOT, DEST[gname])
    print("  【%s → %s/】" % (gname, DEST[gname]))
    for rel in grp:
        s = os.path.join(ROOT, rel.replace("/", os.sep))
        if not os.path.isfile(s):
            print("     查無此檔（略）：%s" % rel)
            continue
        sz = os.path.getsize(s) / 1024.0
        total += sz
        tgt = os.path.join(d, os.path.basename(rel))
        flag = ""
        if os.path.exists(tgt):
            flag = "★目標已存在，拒搬★"
        print("     %-52s %9.1fK %s" % (os.path.basename(rel), sz, flag))
        if not flag:
            moves.append((s, tgt))
print("  合計 %d 檔／%.1f MB" % (len(moves), total / 1024.0))
if not GO:
    print("\n試跑畢（未動一檔）。落刀請加 --go")
    sys.exit(0)

print("\n== 3. 落刀 ==")
for gname, _ in GROUPS:
    os.makedirs(os.path.join(ROOT, DEST[gname].replace("/", os.sep)), exist_ok=True)
led = ["# 搬移清冊 MOVED-20261018（由 _merge/tidy_move.py --go 產）", "",
       "緣起：清理根目錄與 _work，將舊版・一次性腳本・舊產出歸入 _archive 之下。",
       "法則：逐名列檔，不用前綴通配；目標已存在即拒搬；釘死檔（編纂底冊・編年日誌・正本・SOP・_tk・hulan_path・verify_audit）自證在原處。",
       "復原：本冊每行作 `源 <TAB> 的`，可逐枚原路搬回（見文末一行式）。", ""]
done = 0
for s, t in moves:
    shutil.move(s, t)
    done += 1
    led.append("%s\t%s" % (os.path.relpath(s, ROOT), os.path.relpath(t, ROOT)))
led += ["", "## 一行式復原（PowerShell 逐行粘貼即可；先 cd 至工作資料夾）", ""]
for s, t in moves:
    led.append("Move-Item -LiteralPath '%s' -Destination '%s'" %
               (os.path.relpath(t, ROOT), os.path.relpath(s, ROOT)))
post = {bookA: sha(bookA), bookB: sha(bookB)}
led += ["", "## 正本未動之證", ""]
for k in pre:
    led.append("%s  跑前 %s → 跑後 %s  %s" % (os.path.basename(k)[:28], pre[k], post[k],
                                          "同（未動）" if pre[k] == post[k] else "★變了★"))
lp = os.path.join(ROOT, "_archive", "MOVED-20261018.txt")
open(lp, "w", encoding="utf-8").write("\n".join(led) + "\n")
print("  搬成 %d 檔；清冊：%s" % (done, os.path.relpath(lp, ROOT)))
print("\n== 4. 正本跑後 SHA ==")
ok = True
for k, v in pre.items():
    print("  %s → %s  %s" % (v, post[k], "同" if v == post[k] else "★異★"))
    ok = ok and v == post[k]
print("判定：正本%s" % ("未動一字 ✓" if ok else "被動了，立即以清冊復原！"))
