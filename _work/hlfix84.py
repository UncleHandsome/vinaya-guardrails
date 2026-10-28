# -*- coding: utf-8 -*-
"""第 84 輪・外路第三十三報之真病（其前三項已於 83 輪修畢，此報所讀為舊版）：
   甲、第十五章案例二之條文框：先有一行『（第122至127條，順次規範…）』之總括，其下 122～127 又逐條全列
       （與 83 輪所削之 151～155 總括同型）→ 削總括。
   乙、條文框之次序跳躍（兩案）：第十四章案例二 150,156,176,157,158,151-155,177,178；
       第十五章案例二 121,165,166,168,122-127,167——皆非戒本次第。逐框按號排序（各條文俱單行，整行隨號走）。
   丙、『在舊版中，第111條被荒謬地塞在做衣服的案例二十裡』——改稿備忘外洩，改為讀者面向之法理句。
   丁、『大師母』二處——摩訶波闍波提本書已作『大愛道』，『大師母』帶江湖氣（且 60 輪已有『大師母歸大愛道』之成例）。
   戊、『齋優婆私』——語料 16 見，是『持齋之女居士』之通稱，非人名；首見處加一注以免誤讀。
"""
import hashlib
import io
import os
import re
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
LBL = re.compile(u"^> \\*\\*【第(\\d+)條 條文】：")


def one(pred, what):
    got = [i for i, s in enumerate(L) if pred(s)]
    if len(got) != 1:
        errs.append(u"%s 命中 %d（宜 1）" % (what, len(got)))
        return None
    return got[0]


# 甲
i = one(lambda s: s.startswith(u"> （第122至127條，順次規範"), u"甲之總括行")
if i is not None:
    del L[i]
    print(u"甲｜削總括行（原 L%d）" % (i + 1))

# 乙
for tag, case_head in ((u"第十四章案例二", u"#### 案例二：感官享受、美容按摩與魅態封殺"),):
    pass
for tag, head, want in (
        (u"第十四章案例二", u"#### 案例二：感官享受", 12),
        (u"第十五章案例二", u"#### 案例二：僧團准入風控Ⅱ", 11)):
    h = one(lambda s, x=head: s.startswith(x), tag + u" 之題")
    if h is None:
        continue
    k = h + 1
    while k < len(L) and L[k].strip() == u"":
        k += 1
    run = []
    while k + len(run) < len(L) and LBL.match(L[k + len(run)]):
        run.append(L[k + len(run)])
    nums = [int(LBL.match(s).group(1)) for s in run]
    if len(run) != want:
        errs.append(u"%s 之條文行 %d（宜 %d）" % (tag, len(run), want))
        continue
    order = u",".join(str(n) for n in nums)
    run2 = [s for _n, s in sorted(zip(nums, run), key=lambda p: p[0])]
    nums2 = sorted(nums)
    if len(set(nums)) != len(nums):
        errs.append(u"%s 之號有重" % tag)
        continue
    L[k:k + len(run)] = run2
    print(u"乙｜%s｜%s → %s" % (tag, order, u",".join(str(n) for n in nums2)))

# 丙
i = one(lambda s: u"在舊版中，第111條被荒謬地塞在做衣服的案例二十裡" in s, u"丙之舊版句")
if i is not None:
    L[i] = L[i].replace(
        u"在舊版中，第111條被荒謬地塞在做衣服的案例二十裡。如今將其歸入此處，讀者終於能清晰看見：",
        u"本條若只當作尋常違紀，便看不清它的司法本質；歸入同住義務的脈絡，讀者方能清晰看見：")

# 丁
n_d = 0
for k, s in enumerate(L):
    if u"大師母" in s:
        n_d += s.count(u"大師母")
        L[k] = s.replace(u"大師母", u"大愛道")
print(u"丁｜大師母→大愛道 %d 處" % n_d)

# 戊
i = one(lambda s: u"在家好友之婦「齋優婆私」" in s, u"戊之首見")
if i is not None:
    L[i] = L[i].replace(u"在家好友之婦「齋優婆私」",
                        u"在家好友之婦「齋優婆私」（持齋之女居士）")

if errs:
    for e in errs:
        print(u"✗ " + e)
    sys.exit(1)
print(u"行數 %d → %d" % (len(raw.split(u"\r\n")), len(L)))
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
BK = HP.bakpath(u"84a")
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
