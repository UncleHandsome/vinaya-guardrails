# -*- coding: utf-8 -*-
"""r19move - 把《佛陀的護欄》正文檔從 XW 目錄搬回工作資料夾根。
複製→逐位元組比對→才刪原檔；未加 --go 一律只試跑。"""
import os, re, io, sys, hashlib, shutil

HERE = os.path.dirname(os.path.abspath(__file__))          # _work
ROOT = os.path.dirname(HERE)
GO = "--go" in sys.argv

# 舊路徑自現行腳本原始碼取出，不在本檔手打中文
src_code = io.open(os.path.join(HERE, "apxchk.py"), encoding="utf-8").read()
m = re.findall(r'BOOK = r"([^"]+\.txt)"', src_code)
assert len(m) == 1, m
OLD = m[0]
assert os.path.isfile(OLD), OLD
DEST = os.path.join(ROOT, os.path.basename(OLD))
assert not os.path.exists(DEST), "目的地已存在: " + DEST

b_old = io.open(OLD, "rb").read()
sha_old = hashlib.sha256(b_old).hexdigest()
t = b_old.decode("utf-8")
print("OLD  =", OLD)
print("DEST =", DEST)
print("bytes=%d sha256=%s" % (len(b_old), sha_old[:16]))
print("splitlines=%d CR=%d LF=%d CJK=%d" % (
    len(t.splitlines()), t.count("\r"), t.count("\n"),
    sum(1 for c in t if ord(c) >= 0x2E80)))

par = os.path.dirname(OLD)
print("--- 原目錄 %s 尚有何檔 ---" % par)
for n in sorted(os.listdir(par)):
    fp = os.path.join(par, n)
    print("   ", n, "/" if os.path.isdir(fp) else " %dKB" % (os.path.getsize(fp)//1024))

if not GO:
    print("DRY-RUN（加 --go 才真搬）")
    sys.exit(0)

shutil.copy2(OLD, DEST)
b_new = io.open(DEST, "rb").read()
assert b_new == b_old, "內容不符"
assert hashlib.sha256(b_new).hexdigest() == sha_old
assert os.stat(DEST).st_size == len(b_old)
print("複製完成且逐位元組相符 → 刪原檔")
os.remove(OLD)
assert not os.path.exists(OLD)
print("原檔已不存在，搬移完成")

sys.path.insert(0, ROOT)
import hulan_path as HP
assert os.path.abspath(HP.SRC) == os.path.abspath(DEST), (HP.SRC, DEST)
print("法源已指向:", HP.SRC)
