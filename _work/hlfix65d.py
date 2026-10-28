# -*- coding: utf-8 -*-
"""第 65 輪・丁：新第七章之三段收尾刀。

 一・「催告演算法」屬本書語而掛款①式樣（hlchk 戊軸點名 1 段）→ 降其式樣。
 二・第七章章首題記新增之署名附大正藏冊號（義引，合今制），唯『卷中一』之卷次本地無從覆核
    （行事鈔但分卷，無『中一』之目）→ 削其卷次，存其署名與冊號，使可檢索者仍可檢索。
 三・六處【案發現場】欄內一行一拍（相鄰無空行）被 pandoc 併為一段，印面 340～602 字之黑塊
    → 於語意轉折處補空行（一字不增刪）。口徑承第 20 報：單位是『印面段落』，不是源檔單行。
用法：python -X utf8 _work/hlfix65d.py [--go]
"""
import hashlib
import io
import os
import re
import shutil
import sys

GO = u"--go" in sys.argv
BOOK = u"佛陀的護欄 四分律比丘與比丘尼戒的行為心理學解析.txt"
BAK = BOOK + u".bak65d"
raw = io.open(BOOK, "rb").read()
sha0 = hashlib.sha256(raw).hexdigest()
L = raw.decode("utf-8").split(u"\r\n")
N0 = len(L)
assert raw.count(b"\r") == raw.count(b"\n"), u"入口 CRLF 已傷"
print(u"正本 sha %s｜%d 行" % (sha0[:12], N0))


def find1(sub, start=0):
    hits = [i for i in range(start, len(L)) if sub in L[i]]
    assert len(hits) == 1, u"錨『%s』命中 %d 枚（須 1）" % (sub[:30], len(hits))
    return hits[0]


# ── 一・催告演算法之式樣 ─────────────────────────────────────────────
i = find1(u"**「催告演算法」**")
assert L[i].count(u"**「催告演算法」**") == 1
L[i] = L[i].replace(u"**「催告演算法」**", u"**催告演算法**")
print(u"  一 降式樣 L%d｜佛陀所立之名，非律之語" % (i + 1))

# ── 二・題記之卷次 ───────────────────────────────────────────────────
i = find1(u"行事鈔》卷中一（大正藏 T40n1804 義引）")
L[i] = L[i].replace(u"行事鈔》卷中一（大正藏 T40n1804 義引）",
                    u"行事鈔》（大正藏 T40n1804 義引）")
print(u"  二 削卷次 L%d｜『卷中一』本地無從覆核，義引與冊號俱存" % (i + 1))

# ── 三・六處黑塊之分段 ───────────────────────────────────────────────
LEADS = [u"  舍衛國祇樹給孤獨園。安居結束、功德衣",
         u"  舍衛國，六群比丘不喜隨身攜帶沉重繁複的三衣",
         u"  舍衛國，一乞食比丘於某居士門外",
         u"  國王、大臣或富商發心供養比丘衣服",
         u"  舍衛國祇樹給孤獨園。城中一大臣信奉佛法",
         u"  舍衛國。一位極具信心的富裕長者"]
ins = []
for lead in LEADS:
    i = find1(lead)
    assert L[i - 1].startswith(u"* **【案發現場（制戒因緣）】：**"), u"欄首之上一行非【案發現場】：%s" % L[i - 1][:24]
    j = i + 1
    n = 0
    while j < len(L) and L[j].strip():
        assert L[j].startswith(u"  ") or L[j].startswith(u">"), u"欄內行首非縮排亦非引框：%s" % L[j][:20]
        if L[j].startswith(u">"):        # 引框自成一拍，其前亦須空行
            ins.append(j)
        else:
            ins.append(j)
            L[j - 1] = L[j - 1].rstrip()
        n += 1
        j += 1
    print(u"  三 補空行｜%-14s…%d 拍（含欄首共 %d 行）" % (lead[2:14], n, n + 1))
for j in sorted(set(ins), reverse=True):
    L[j:j] = [u""]
print(u"  三 合計插入空行 %d 處" % len(set(ins)))

# ── 出口自證 ─────────────────────────────────────────────────────────
txt = u"\r\n".join(L)
assert txt.count(u"\r") == txt.count(u"\n") == len(L) - 1, u"CRLF 變形"
assert sum(1 for l in L if l.startswith(u"#### 案例")) == 163, u"案例之數變形"
assert sum(1 for l in L if l.startswith(u"```")) == 46, u"圍欄對數變形"
print(u"行數 %d→%d｜圍欄 %d 段" % (N0, len(L), sum(1 for l in L if l.startswith(u"```")) // 2))
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
assert not os.path.exists(BAK), u"備份已存在：%s" % BAK
shutil.copy2(BOOK, BAK)
io.open(BOOK, "w", encoding="utf-8", newline=u"").write(txt)
chk = io.open(BOOK, "rb").read()
print(u"已寫檔｜sha %s→%s｜%d B｜備份 %s" % (
    sha0[:12], hashlib.sha256(chk).hexdigest()[:12], len(chk), os.path.basename(BAK)))
