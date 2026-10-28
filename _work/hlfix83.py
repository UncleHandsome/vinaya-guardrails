# -*- coding: utf-8 -*-
"""第 83 輪・外路第三十二報之真病（七刀；報告混有前兩輪已修者——p4 邏輯句、目錄副題、L00、109、㥲 皆已結）：
   甲、尼單提【第106、107條 條文】只領 106 之文（107 為『持沙門衣施與外道白衣』，本案標題作 102～106、108～110）→ 還單條。
   乙、第九章後半部矩陣宣『第46～90條』而漏第54條（矩陣所宣之號段須無缺；本案正文案例七正是第54條）→ 補一線。
   丙、同圖第五重鎮三處標名與戒本不合：56＝半月洗浴（非擯出）、60＝新衣壞色（非二食家）、62＝飲雜蟲水（非滅擯）→ 正之（字數同，圖不對齊不走）。
   丁、十線第三線之『第十四章案例五』條號誤植 90、91（屬案例一），且漏 83、85——依案例五之條文標籤現取。
   戊、第十四章案例二之條文框先有一段『第151至155條…』之總括，其下七條又逐條全列——總括為重複，削之。
   己、僧伽婆尸沙之釋末：『此乃本書依戒名之義之推衍』——此訓詁乃律家常解，不必自承推衍；削此半句。
   庚、『輕推、防錯、增程』之序與正文（防錯→增程→輕推）相反：題與目錄同步正之。
   辛、慾望／欲望混用（慾望 5・欲望 35）——統一為多數形『欲望』。
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
errs = []


def one(pred, what):
    got = [i for i, s in enumerate(L) if pred(s)]
    if len(got) != 1:
        errs.append(u"%s 命中 %d（宜 1）" % (what, len(got)))
        return None
    return got[0]


# 甲
i = one(lambda s: u"【第106、107條 條文】" in s, u"甲之標籤")
if i is not None:
    L[i] = L[i].replace(u"【第106、107條 條文】", u"【第106條 條文】")

# 乙｜丙（第九章後半部矩陣）
i3 = one(lambda s: s.startswith(u"├─ 第三重鎮·思想防毒"), u"乙之第三重鎮")
if i3 is not None:
    L.insert(i3 + 1, u"│    54 不受諫")
i56 = one(lambda s: u"56、57 擯出／燃火" in s, u"丙之 56、57 行")
if i56 is not None:
    L[i56] = L[i56].replace(u"56、57 擯出／燃火", u"56、57 洗浴／燃火")
i60 = one(lambda s: u"60～62 二食家／斷畜命／滅擯" in s, u"丙之 60～62 行")
if i60 is not None:
    L[i60] = L[i60].replace(u"60～62 二食家／斷畜命／滅擯", u"60～62 壞色衣／斷畜命／飲蟲水")

# 丁｜十線之條號（自案例五之標籤現取）
c5 = one(lambda s: s.startswith(u"#### 案例五") and u"客舍" in s or (s.startswith(u"#### 案例五") and 4400 < L.index(s) < 4700),
         u"第十四章案例五")
if c5 is not None:
    nums = []
    for k in range(c5, c5 + 40):
        if L[k].startswith(u"#### ") and k > c5:
            break
        m = __import__("re").search(u"【第(\\d+)條 條文】", L[k])
        if m:
            nums.append(m.group(1))
    print(u"丁｜案例五之條：%s" % u"、".join(nums))
    if nums:
        row = one(lambda s: u"尼單提第84、90、91、115、116條" in s, u"丁之十線行")
        if row is not None:
            L[row] = L[row].replace(u"尼單提第84、90、91、115、116條",
                                    u"尼單提第" + u"、".join(nums) + u"條")

# 戊
i = one(lambda s: s.startswith(u"> （第151至155條，順次禁止"), u"戊之總括行")
if i is not None:
    del L[i]
    if L[i].strip() == u"" and L[i - 1].strip() == u"":
        del L[i]

# 己
i = one(lambda s: u"，此乃本書依戒名之義之推衍。）" in s, u"己之半句")
if i is not None:
    L[i] = L[i].replace(u"，此乃本書依戒名之義之推衍。）", u"。）")

# 庚
i = one(lambda s: s.startswith(u"#### 1. 輕推（Nudge）、防錯"), u"庚之正文題")
if i is not None:
    L[i] = L[i].replace(u"#### 1. 輕推（Nudge）、防錯（Forcing Function）、增程（Friction）",
                        u"#### 1. 防錯（Forcing Function）、增程（Friction）、輕推（Nudge）")
j = one(lambda s: s.strip() == u"* 輕推、防錯、增程：三種強度的情境工程", u"庚之目錄條")
if j is not None:
    L[j] = L[j].replace(u"輕推、防錯、增程：三種強度的情境工程", u"防錯、增程、輕推：三種強度的情境工程")

# 辛
n_x = 0
for k, s in enumerate(L):
    if u"慾望" in s:
        n_x += s.count(u"慾望")
        L[k] = s.replace(u"慾望", u"欲望")
print(u"辛｜慾望→欲望 %d 處" % n_x)

if errs:
    for e in errs:
        print(u"✗ " + e)
    sys.exit(1)
print(u"行數 %d → %d" % (len(raw.split(u"\r\n")), len(L)))
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
BK = HP.bakpath(u"83a")
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
