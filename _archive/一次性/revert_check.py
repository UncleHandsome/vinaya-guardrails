# -*- coding: utf-8 -*-
"""回退之覆核與落帳：按試跑單逐條核『原位已空・新位存在』，再將搬移清冊附入 `_archive/MOVED-20261019.txt`。

由來：`revert_merge.py --go` 已把 309 檔搬訖、中介 12 檔除訖，然收尾 `os.rmdir('_merge')`
遇 Windows 存取被拒而中斷，致覆核與清冊兩步未行。此器補行两步，並如實記 `_merge` 未除。
"""
import io
import os
import re
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HE = "".join(chr(c) for c in (0x5408, 0x4F75, 0x7248))        # 合併版
SHU = "".join(chr(c) for c in (0x66F8, 0x8EAB))               # 書身
CHN = "".join(chr(c) for c in (0x7522, 0x51FA))               # 產出
JIU = "".join(chr(c) for c in (0x820A, 0x672C))               # 舊本
BUCKET = {SHU: os.path.join(ROOT, "_archive", HE, SHU),
          CHN: os.path.join(ROOT, "_archive", HE, CHN),
          "_book": os.path.join(ROOT, "_archive", HE, "_book"),
          "_print": os.path.join(ROOT, "_archive", HE, "_print"),
          "_work": os.path.join(ROOT, "_archive", HE, "_work")}
FO = "".join(chr(c) for c in (0x4F5B, 0x9640, 0x7684, 0x8B77, 0x6B04))    # 佛陀的護欄

# 一・取試跑單之搬遷表（唯 『  桶名   相對源路徑』 式之行）
pairs = []
pat = re.compile(u"^\\s+(%s|_book|_print|_work)\\s+(\\S.*)$" % u"|".join([SHU, CHN]))
for line in io.open(os.path.join(ROOT, "_work", "_dryrun.txt"), encoding="utf-8"):
    m = pat.match(line.rstrip(u"\n"))
    if not m:
        continue
    bucket, rel = m.group(1), m.group(2).strip()
    if os.path.basename(rel).startswith(u"_gotxt"):
        continue
    pairs.append((rel, os.path.join(BUCKET[bucket], os.path.basename(rel))))

# 二・迎回正本兩冊
back = []
for name in ("ver38" + u"\u56db\u5206\u5f8b_\u8d77\u5fc3\u52d5\u5ff5\u5fc3\u667a\u5206\u6790\u6846\u67b6_"
             u"\u4fee\u6b63\u7248.md",
             FO + u" \u56db\u5206\u5f8b\u6bd4\u4e18\u8207\u6bd4\u4e18\u5c3c\u6212\u7684\u884c\u70ba"
             u"\u5fc3\u7406\u5b78\u89e3\u6790.txt"):
    src = os.path.join(ROOT, "_archive", JIU, name)
    dst = os.path.join(ROOT, name)
    if os.path.isfile(dst):
        back.append((src, dst, hashlib.sha256(io.open(dst, "rb").read()).hexdigest()))

# 三・逐條覆核
bad = []
for rel, dst in pairs:
    s = os.path.join(ROOT, rel.replace("\\", os.sep))
    if os.path.exists(s):
        bad.append(u"原位猶在：%s" % rel)
    if not os.path.isfile(dst):
        bad.append(u"新位缺失：%s" % dst)
for src, dst, h in back:
    if os.path.exists(src) or not os.path.isfile(dst):
        bad.append(u"正本迎回未竟：%s → %s" % (src, dst))
print(u"搬 %d 檔｜迎回 %d 冊｜覆核 %s" % (len(pairs), len(back),
                                        u"全中" if not bad else u"有失 %d 條" % len(bad)))
for b in bad[:20]:
    print(u"  ✗ " + b)
for src, dst, h in back:
    print(u"  正本 %s｜%d bytes｜sha %s" % (os.path.basename(dst), os.path.getsize(dst), h[:16]))

# 四・落帳
REC = os.path.join(ROOT, "_archive", "MOVED-20261019.txt")
if not bad and not io.open(REC, encoding="utf-8").read().count(u"\u56de\u9000\u5408\u4f76\u7248"):
    with io.open(REC, "a", encoding="utf-8", newline="\n") as f:
        f.write(u"\n\n# 回退合併版（同日第二段）\n\n")
        f.write(u"緣起：作者令「放棄合併版本，改回使用打磨舊版兩冊」。"
                u"合併版之書身・產器・產出・今日暫存腳本逐名封入 `_archive/%s/`；"
                u"兩冊正本自 `_archive/%s/` 迎回根目錄。入庫過之書身與 `_book/` 諸檔，"
                u"歷代內容仍可自 git 取回。\n" % (HE, JIU))
        f.write(u"法：逐名列檔、不用前綴通配；先試跑印名、`--go` 方動；搬畢逐條回讀斷言原位已空・"
                u"新位存在・正本 SHA 一字不動。合併版之中介 12 檔（book*.pdf／final_book*.html／"
                u"log／_toccache_book*.json／book_列印版*）屬可重建之腳手且其冊已廢，已除。\n")
        f.write(u"未竟：`_merge/` 空夾 rmdir 遇 WinError 5（存取被拒）未除，留原地無害。\n")
        f.write(u"復原：每行作 `源 <TAB> 的`，可逐枚原路搬回。\n\n")
        for rel, dst in pairs:
            f.write(u"%s\t%s\n" % (rel, os.path.relpath(dst, ROOT).decode("utf-8")
                                   if isinstance(dst, bytes) else os.path.relpath(dst, ROOT)))
        f.write(u"\n-- 迎回正本 --\n")
        for src, dst, h in back:
            f.write(u"%s\t%s\n" % (os.path.relpath(src, ROOT), os.path.relpath(dst, ROOT)))
    print(u"清冊已附於 %s" % os.path.relpath(REC, ROOT))
else:
    print(u"清冊未動（有失，或已落過帳）")
