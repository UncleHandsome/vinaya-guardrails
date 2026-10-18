# -*- coding: utf-8 -*-
"""末關・只掩兩冊帳之機器路徑（碼不改，故尺仍跑得）；`_merge` 之三支一次性工具改由 .gitignore 除外。"""
import os, re, sys, io, getpass
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER = getpass.getuser()
GO = "--go" in sys.argv
LED = ["_archive/MOVED-20261018.txt", "_archive/DELETED-20260922.txt"]
NOTE = ("\n〔附註・2026-10-18〕本冊內之機器絕對路徑前綴已掩為 `<HOME>`（僅掩前綴，逐條內容未動・時間與檔名與原因俱在）。"
        "掩之為入公開庫計：不留使用者名與資料夾結構。\n")
for n in LED:
    p = os.path.join(ROOT, *n.split("/"))
    t = open(p, encoding="utf-8").read()
    before = t.count(USER)
    t2 = re.sub(r"[A-Za-z]:(?:\\\\)+Users(?:\\\\)+" + re.escape(USER), "<HOME>", t)
    t2 = re.sub(r"[A-Za-z]:\\Users\\" + re.escape(USER), "<HOME>", t2)
    t2 = re.sub(r"[A-Za-z]:/Users/" + re.escape(USER), "<HOME>", t2)
    print("   %-32s 使用者名 %d 處 → 餘 %d 處" % (n, before, t2.count(USER)))
    if GO and t2 != t:
        open(p, "w", encoding="utf-8", newline="\n").write(t2 + NOTE)
print("   %s" % ("已落刀並附註" if GO else "試跑（未動檔）"))
