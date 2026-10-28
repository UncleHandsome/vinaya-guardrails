# -*- coding: utf-8 -*-
"""第 65 輪・丙：第七章換稿後之指針歸位與總數宣稱改約。

新第七章之案例編組全變（19→18，且序尽改）；凡指「第七章案例M」者，M 所指之案已非舊案。
歸位之法源＝條號：每處指針皆带條號（表列之第二欄、靶點之括注、第十三章之『同甲部第N條』），
故以（舊案例→條號→新案例）三對而改一改三，不憑印象。
硬斷言：改後全書不得再有指舊編之『第七章案例N』而條號不合者（交 refchk 複核）；
　　案例總數 164→163，十線地圖導言之自報同步改一字。
用法：python -X utf8 _work/hlfix65c.py [--go]
"""
import hashlib
import io
import os
import re
import shutil
import sys

GO = u"--go" in sys.argv
BOOK = u"佛陀的護欄 四分律比丘與比丘尼戒的行為心理學解析.txt"
BAK = BOOK + u".bak65c"
raw = io.open(BOOK, "rb").read()
sha0 = hashlib.sha256(raw).hexdigest()
L = raw.decode("utf-8").split(u"\r\n")
N0 = len(L)
assert raw.count(b"\r") == raw.count(b"\n"), u"入口 CRLF 已傷"

# （條號, 舊案例漢字, 新案例漢字, 唯一錨點）——錨點須含條號以免誤傷他章
FIX = [
    (u"8、9",  u"九",  u"六",  u"| 第七章案例九 | 捨墮第8、9條 |"),
    (u"18",    u"三",  u"十二", u"| 第七章案例三 | 捨墮第18條 |"),
    (u"19、20", u"八",  u"十三", u"| 第七章案例八 | 捨墮第19、20條 |"),
    (u"10",    u"十",  u"七",   u"| 第七章案例十 | 捨墮第10條 |"),
    (u"23",    u"十五", u"十四", u"| 第七章案例十五 | 捨墮第23條 |"),
    (u"22",    u"十四", u"十六", u"| 第七章案例十四 | 捨墮第22條 |"),
    (u"2",     u"十三", u"二",   u"| 第七章案例十三 | 捨墮第2條 |"),
    (u"11",    u"二",  u"八",    u"| 第七章案例二 | 捨墮第11條 |"),
    (u"10",    u"十",  u"七",    u"【第七章案例十：過三反語六反立戒（第10條）】"),
    (u"23",    u"十五", u"十四", u"【第七章案例十五：自乞縷線使織師織衣（捨墮第23條）】"),
    (u"15",    u"十九", u"十",   u"【第七章案例十九：新坐具帖故（第15條）】"),
    (u"4、5",  u"五",  u"四",    u"各各繫心」（第七章案例五）"),
    (u"17",    u"十六", u"四",   u"【第七章案例十六：使非親里比丘尼浣染擘羊毛（捨墮第17條）】"),
    (u"18",    u"三",  u"十二",  u"【第七章案例三：自手捉持金銀（捨墮第18條）】"),
    (u"11",    u"二",  u"八",    u"【第七章案例二：雜野蠶綿作新臥具（覆身之物亦有帳）】"),
    (u"18",    u"三",  u"十二",  u"（第七章案例三、案例一（第18條、第1條））"),
    # 第十三章第二節之『同甲部第N條，見第七章案例M』一串九指
    (u"6",     u"六",  u"五",    u"同甲部第6條，見第七章案例六"),
    (u"10",    u"十",  u"七",    u"甲部第10條，見第七章案例十"),
    (u"18",    u"三",  u"十二",  u"第18條，見第七章案例三"),
    (u"20",    u"八",  u"十三",  u"20條，並見第七章案例八"),
    (u"23",    u"十五", u"十四", u"同甲部第23條，見第七章案例十五"),
    (u"24",    u"十九", u"十四", u"與價」事，見第七章案例十九"),
    (u"30",    u"四",  u"十八",  u"第30條，見第七章案例四"),
    (u"3",     u"十九", u"三",   u"時制之兩面，見第七章案例十九"),
]
n = 0
for rule, old, new, anchor in FIX:
    assert anchor.endswith(u"第七章案例%s" % old) or anchor.count(u"案例%s" % old) >= 1, u"錨缺舊號：%s" % anchor
    hits = [i for i, t in enumerate(L) if anchor in t]
    assert len(hits) == 1, u"錨『%s』命中 %d 枚（須 1）" % (anchor[:34], len(hits))
    i = hits[0]
    c = L[i].count(anchor)
    assert c == 1, u"錨於该行出現 %d 次：%s" % (c, anchor[:34])
    L[i] = L[i].replace(anchor, anchor.replace(u"案例%s" % old, u"案例%s" % new))
    n += 1
    print(u"  歸位 %2d｜捨墮第%-5s｜案例%s→%s｜L%d" % (n, rule, old, new, i + 1))

# ── 總數宣稱：一百六十四則 → 一百六十三則（第七章 19→18） ──────────
KN = u"把全書一百六十四則案例"
hits = [i for i, t in enumerate(L) if KN in t]
assert len(hits) == 1, u"總數宣稱命中 %d 枚" % len(hits)
L[hits[0]] = L[hits[0]].replace(KN, u"把全書一百六十三則案例")
print(u"  改約｜L%d 一百六十四則 → 一百六十三則" % (hits[0] + 1))

# ── 出口自證 ─────────────────────────────────────────────────────────
NCASE = sum(1 for l in L if l.startswith(u"#### 案例"))
assert NCASE == 163, u"全書案例實數 %d ≠ 163" % NCASE
assert u"一百六十四" not in u"".join(L), u"仍殘『一百六十四』之自報"
CH7 = [l for l in L if u"第七章案例" in l]
print(u"  覆核｜全書案例 %d 則｜仍含『第七章案例』之行 %d 行（俱應已依條號歸位）" % (NCASE, len(CH7)))
txt = u"\r\n".join(L)
assert txt.count(u"\r") == txt.count(u"\n") == len(L) - 1, u"CRLF 變形"
assert len(L) == N0, u"行數變形"
print(u"正本 sha（改前）%s" % sha0[:12])
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
assert not os.path.exists(BAK), u"備份已存在：%s" % BAK
shutil.copy2(BOOK, BAK)
io.open(BOOK, "w", encoding="utf-8", newline=u"").write(txt)
chk = io.open(BOOK, "rb").read()
print(u"已寫檔｜sha %s→%s｜%d B｜備份 %s" % (
    sha0[:12], hashlib.sha256(chk).hexdigest()[:12], len(chk), os.path.basename(BAK)))
