# -*- coding: utf-8 -*-
"""回退合併版：把合併版之書身・產器・產出封存進 `_archive/合併版/`，兩冊舊本迎回根目錄作正本。

預設試跑（只印名與數，一檔不動）；`--go` 方落刀。法：逐名列檔、不用前綴通配；
目標已存在即中止；搬畢逐檔回讀斷言原位已空・新位存在；兩冊正本另以 SHA 自證未傷一字。
"""
import io
import os
import sys
import glob
import time
import shutil
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GO = "--go" in sys.argv

# 碼位構形：顯示／傳遞層會把繁體歸簡，此處不靠字面
FO = "".join(chr(c) for c in (0x4F5B, 0x9640, 0x7684, 0x8B77, 0x6B04))        # 佛陀的護欄
JIU = "".join(chr(c) for c in (0x820A, 0x672C))                               # 舊本
HE = "".join(chr(c) for c in (0x5408, 0x4F75, 0x7248))                        # 合併版
SHU = "".join(chr(c) for c in (0x66F8, 0x8EAB))                               # 書身
CHN = "".join(chr(c) for c in (0x7522, 0x51FA))                               # 產出
DEST = os.path.join(ROOT, "_archive", HE)
D_SHU = os.path.join(DEST, SHU)
D_PDF = os.path.join(DEST, CHN)
D_BOOK = os.path.join(DEST, "_book")
D_PRINT = os.path.join(DEST, "_print")
D_WORK = os.path.join(DEST, "_work")

# 今日之暫存腳本（合併版一役之用畢者）；KEEP 俱本輪自用，留在原處待清
KEEP = set(["_ulist.txt", "_base_fw.txt", "_base_hl.txt", "revert_merge.py", "_dryrun.txt"])
# 框架冊查核器自寫自讀之輸出（每次 verify_audit 即重寫）——留原處，不作合併版之帳
FW_OUT = set(["check.txt", "order.txt", "summary.txt"] +
             ["verify_%s.txt" % s for s in ("c6", "e", "f", "bq", "bqa")])
TODAY = time.mktime(time.strptime("2026-10-19", "%Y-%m-%d"))

moves = []          # (abs_src, abs_dst)
deletes = []        # abs path
notes = []


def add_move(src, dst_dir):
    if not os.path.isfile(src):
        return
    dst = os.path.join(dst_dir, os.path.basename(src))
    if os.path.exists(dst):
        raise SystemExit("目標已存在，中止：%s" % dst)
    moves.append((src, dst))


# 一・根目錄之合併版書身（前綴＋底線者唯合併版有之；正本那支作空格且為 .txt）
for p in sorted(glob.glob(os.path.join(ROOT, FO + "_*.md"))):
    add_move(p, D_SHU)

# 二・`_print/` 之合併版交付 PDF（唯取今日所出者；舊護欄四式作於 10-17，留在原處）
for p in sorted(glob.glob(os.path.join(ROOT, "_print", FO + "_*.pdf"))):
    if os.path.getmtime(p) >= TODAY:
        add_move(p, D_PDF)

# 三・合併版之產器與產器層列印件
for p in sorted(glob.glob(os.path.join(ROOT, "_book", "*"))):
    if os.path.isfile(p):
        add_move(p, D_BOOK)
add_move(os.path.join(ROOT, "_print", "build_book.py"), D_PRINT)

# 四・`_work/` 今日之暫存腳本與帳檔（逐名取，非通配刪）
for p in sorted(glob.glob(os.path.join(ROOT, "_work", "*"))):
    if os.path.isfile(p) and os.path.basename(p) not in KEEP and os.path.basename(p) not in FW_OUT:
        if os.path.getmtime(p) >= TODAY:
            add_move(p, D_WORK)

# 五・合併版之中介產物（gitignore 內・可重建・其冊已廢）→ 除
MID = ["book.pdf", "book_screen.pdf",
       u"book_\u5217\u5370\u7248.md", u"book_\u5217\u5370\u7248.html",
       u"book_\u5217\u5370\u7248_screen.md", u"book_\u5217\u5370\u7248_screen.html",
       "final_book.html", "final_book_screen.html",
       "log_build_book.txt", "log_build_screen.txt",
       "_toccache_book.json", "_toccache_book_screen.json"]
for fn in MID:
    p = os.path.join(ROOT, "_print", fn)
    if os.path.isfile(p):
        deletes.append(p)
PYC = [os.path.join(ROOT, "__pycache__"), os.path.join(ROOT, "_book", "__pycache__"),
       os.path.join(ROOT, "_print", "__pycache__"), os.path.join(ROOT, "_work", "__pycache__")]
PYC = [p for p in PYC if os.path.isdir(p)]

# 六・兩冊舊本迎回根目錄
OLDLAYER = os.path.join(ROOT, "_archive", JIU)
back = []
for pat in ("ver[0-9]*.md", FO + "*.txt"):
    for p in sorted(glob.glob(os.path.join(OLDLAYER, pat))):
        dst = os.path.join(ROOT, os.path.basename(p))
        if os.path.exists(dst):
            raise SystemExit("根目錄已有同名檔，中止：%s" % dst)
        back.append((p, dst))

print("== 試跑：%s ==" % ("落刀（--go）" if GO else "只印名，不動檔"))
print("封存 %d 檔｜除中介 %d 檔｜迎回 %d 檔｜清 pycache %d 夾"
      % (len(moves), len(deletes), len(back), len(PYC)))
print("\n-- 入 `_archive/%s/` --" % HE)
for s, d in moves:
    print("  %-8s %s" % (os.path.relpath(d, DEST).split(os.sep)[0], os.path.relpath(s, ROOT)))
print("\n-- 迎回正本 --")
for s, d in back:
    print("  %s" % os.path.relpath(s, ROOT))
print("\n-- 除（可重建之中介）--")
for p in deletes:
    print("  %s" % os.path.relpath(p, ROOT))
print("  (pycache) " + " ".join(os.path.relpath(p, ROOT) for p in PYC))

if not GO:
    raise SystemExit("試跑畢；加 --go 方動檔")

# 落刀
for d in (D_SHU, D_PDF, D_BOOK, D_PRINT, D_WORK):
    os.makedirs(d, exist_ok=True)
sha_before = {}
for s, d in back:
    sha_before[os.path.basename(s)] = hashlib.sha256(io.open(s, "rb").read()).hexdigest()
    notes.append((s, d))
for s, d in moves:
    shutil.move(s, d)
for s, d in back:
    shutil.move(s, d)
for p in deletes:
    os.remove(p)
for p in PYC:
    shutil.rmtree(p)
mrg = os.path.join(ROOT, "_merge")
if os.path.isdir(mrg) and not os.listdir(mrg):
    os.rmdir(mrg)
    print("_merge/ 空夾已除")

# 覆核：原位須空・新位須在・正本 SHA 須一字不動
bad = []
for s, d in moves + back:
    if os.path.exists(s) or not os.path.isfile(d):
        bad.append(("move", s, d))
for p in deletes:
    if os.path.exists(p):
        bad.append(("del", p))
for name, h in sha_before.items():
    p = os.path.join(ROOT, name)
    if hashlib.sha256(io.open(p, "rb").read()).hexdigest() != h:
        bad.append(("sha", p))
print("\n== 覆核：%s ==" % ("全中（搬 %d・除 %d・正本 SHA 不動 %d）"
                           % (len(moves) + len(back), len(deletes), len(back))) if not bad else "有失")
for b in bad:
    print("  ✗ %s" % (b,))

# 落帳：搬移清冊（源 <TAB> 的）並附一行式復原
REC = os.path.join(ROOT, "_archive", "MOVED-20261019.txt")
with io.open(REC, "a", encoding="utf-8", newline="") as f:
    f.write("\n\n# 回退合併版（同日第二段）\n\n")
    f.write(u"緣起：作者令「放棄合併版本，改回使用打磨舊版兩冊」。"
            u"合併版之書身・產器・產出・暫存腳本逐名封入 `_archive/合併版/`，"
            u"兩冊正本自 `_archive/%s/` 迎回根目錄。合併版書身與 `_book/` 諸檔已入庫者，"
            u"歷代內容仍可自 git 取回。\n" % JIU)
    f.write(u"復原：每行作 `源 <TAB> 的`，可逐枚原路搬回。\n\n")
    for s, d in moves:
        f.write(u"%s\t%s\n" % (os.path.relpath(s, ROOT), os.path.relpath(d, ROOT)))
    f.write("\n-- 迎回正本 --\n")
    for s, d in back:
        f.write(u"%s\t%s\n" % (os.path.relpath(s, ROOT), os.path.relpath(d, ROOT)))
print("清冊已附於 %s" % os.path.relpath(REC, ROOT))
