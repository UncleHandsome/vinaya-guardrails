# -*- coding: utf-8 -*-
"""第 57 輪・重建段5【十三僧殘法：五道防線】之圍欄圖（五欄並列 → 直幹分枝）。
病（印面實測 _work/hlgrid57.py・源檔形制 hlfchk57.py 俱紅）：舊圖以五欄排開，欄間全憑空白對格，
    而欄內又於語中鋸斷（『【一·婬之／五階】』『6 無主自／乞作屋』『大房不／指授』）；加之
    ▼ 以 .55em 出字，每枚左漂 0.45 格，至第五欄已錯開近一字——印面遂散。
治：改直幹（├─ ×5，皆出於同一空格數・同一框線字，不與漢字欄寬相倚），枝內逐條以『、』連綴，
    僅第一道因超寬而續行，續行之起格由該枝自身之『：』位算得（算而不抄，免手工數空格）。
自證：① 十三條之名目與序號逐枚點名：新圖以全名核（一枚不遺），舊圖以其斷片核（FRAG 帳，
          即舊圖鋸斷之處——全名不在舊圖而又未列斷片帳者亦紅，免漏帳）；
      ② 五枝之印面格數俱 ≤74（11.8pt 版寬之上限 78，留裕）；
      ③ 行首只容空格（禁他種縮排來源）・行尾無殘空白；
      ④ 段外之行逐行等（一字不動）・CR==LF==行數・回讀與所寫合・備份 .bak57i＋SHA 可回退。
"""
import hashlib
import io
import os
import shutil
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "_print"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import build_hulan as BH                              # noqa: E402

SRC = BH.SRC
BAK = SRC + u".bak57i"
KEY = u"十三僧殘法：五道防線"
TRUNK = 8                     # 直幹之格位（純空格前導，與框線字同器）
FLOOR = 74                    # 一行之格數上限（11.8pt 之版寬可容 78，留裕）
BR = [(u"一", u"婬之五階", [u"1 故弄失精", u"2 身相觸", u"3 麁惡語", u"4 自歎身索供養", u"5 媒嫁"], 3),
      (u"二", u"居處與資生", [u"6 無主自作屋", u"7 有主作大房不指授"]),
      (u"三", u"言語武器化", [u"8 無根波羅夷謗", u"9 異分事中取片謗"]),
      (u"四", u"組織分裂", [u"10 破和合僧", u"11 助破僧", u"12 污家行惡行"]),
      (u"五", u"最後開關", [u"13 惡性不受人語（三諫而後結罪）"])]
TAIL = [u"        【防第一重婬戒、第二重盜戒、第四重妄語戒，",
        u"          並死守僧團作為「能自我糾錯之共同體」的可能】"]

cw = BH.cw_units


def pack(items, col, cut=None):
    """自 col 格起以『、』連綴；給 cut 則於該枚之後斷行（先於 FLOOR 之判），逾 FLOOR 者亦斷（回 [字串]）。"""
    out, cur, used = [], [], col
    for idx, it in enumerate(items):
        w = cw(it)
        add = w if not cur else w + 2          # 『、』佔兩格
        if cur and (used + add > FLOOR or (cut is not None and idx == cut)):
            out.append(u"、".join(cur))
            cur, used = [it], col + w
        else:
            cur.append(it)
            used += add
    if cur:
        out.append(u"、".join(cur))
    return out


NEW, grid, MADE = [], [], []
NEW.append(u" " * TRUNK + u"【十三僧殘法：五道防線】")
NEW.append(u" " * TRUNK + u"│")
for ent in BR:
    num, lab, items = ent[0], ent[1], ent[2]
    cut = ent[3] if len(ent) > 3 else None
    pre = u" " * TRUNK + u"├─ 第%s道·%s：" % (num, lab)
    col = cw(pre)
    seg = pack(items, col, cut)
    got = []
    for j, s in enumerate(seg):
        line = pre + s if j == 0 else u" " * TRUNK + u"│" + u" " * (col - TRUNK - 1) + s
        NEW.append(line)
        got.append(line)
    grid.append(col)
    MADE.append((num, col, got))
NEW.append(u" " * TRUNK + u"│")
NEW.append(u" " * TRUNK + u"▼")
NEW.extend(TAIL)

ITEMS = [z for ent in BR for z in ent[2]]
# 舊圖之斷片（列證其鋸處：核靶只以此形對舊圖，新圖則以全名對）
FRAG = {u"自歎身索供養": [u"自歎身", u"索供養"],
        u"無主自作屋": [u"無主自", u"乞作屋"],
        u"有主作大房不指授": [u"有主作", u"大房不", u"指授"],
        u"無根波羅夷謗": [u"無根", u"波羅夷謗"],
        u"異分事中取片謗": [u"異分事", u"中取片謗"],
        u"破和合僧": [u"破和合", u"僧"],
        u"污家行惡行": [u"污家", u"行惡行"],
        u"惡性不受人語（三諫而後結罪）": [u"惡性", u"不受人語", u"（三諫而", u"後結罪）"]}
raw = io.open(SRC, encoding="utf-8", newline=u"").read()
sha_old = hashlib.sha256(raw.encode("utf-8")).hexdigest()
assert raw.count(u"\r") == raw.count(u"\n"), u"CR/LF 之計不等，先清換行再改"
L = raw.split(u"\r\n")

rng, i = [], 0
while i < len(L):
    if L[i].startswith(u"```"):
        j = i + 1
        while j < len(L) and not L[j].startswith(u"```"):
            j += 1
        assert j < len(L), u"圍欄未閉：%d 行起" % i
        if any(KEY in x for x in L[i:j + 1]):
            rng.append((i, j))
        i = j + 1
    else:
        i += 1
assert len(rng) == 1, u"KEY 命中 %d 段圍欄，須唯一（實得 %s）" % (len(rng), rng)
a, b = rng[0]
old = L[a:b + 1]
assert old[0].startswith(u"```") and old[-1].startswith(u"```"), u"界非圍欄之柵"

miss = [z for z in ITEMS if not any(z in x for x in NEW)]
assert not miss, u"新圖失條目：%s" % miss
oldcat = u"".join(old).replace(u" ", u"")
miss2 = [z for z in ITEMS for f in FRAG.get(z[z.index(u" ") + 1:], [z[z.index(u" ") + 1:]])
         if f not in oldcat]
assert not miss2, u"舊圖無此斷片（靶不實，先核）：%s" % miss2
nomatch = [z for z in ITEMS if z[z.index(u" ") + 1:] not in oldcat and z[z.index(u" ") + 1:] not in FRAG]
assert not nomatch, u"全名既不在舊圖、又未列斷片之帳：%s" % nomatch
print(u"舊圖之斷片帳：%d 條名目俱以 %d 枚斷片核中（其餘以全名核中）"
      % (len(FRAG), sum(len(v) for v in FRAG.values())))
w = [cw(x.rstrip()) for x in NEW]
assert max(w) <= FLOOR, u"新圖最寬 %d 格，逾上限 %d" % (max(w), FLOOR)
for z in NEW:
    assert z == z.rstrip(), u"行尾有殘空白：%r" % z
    assert set(z[:len(z) - len(z.lstrip())]) <= set(u" "), u"前導非純空格：%r" % z
for num, c0, got in MADE:
    line = got[0]
    assert c0 == cw(line[:line.index(u"：") + 1]), u"枝 %s 之 items 起格算得 %d、列得 %d" % (num, c0, cw(line[:line.index(u"：") + 1]))
    for z in got[1:]:
        lead = len(z) - len(z.lstrip(u" "))               # 直幹前之空格
        assert z[lead] == u"│", u"續行無直幹：%r" % z
        rest = z[lead + 1:]
        colz = lead + 1 + (len(rest) - len(rest.lstrip(u" ")))
        assert colz == c0, u"枝 %s 之續行 items 起於 %d 格，枝身起於 %d（須齊）" % (num, colz, c0)
    assert cw(line) <= FLOOR and all(cw(x) <= FLOOR for x in got), u"枝 %s 逾上限：%s" % (num, [cw(x) for x in got])
print(u"新圖 %d 行・最寬 %d 格・五枝 items 起格 %s" % (len(NEW), max(w), grid))
for z in NEW:
    print(u"  [%2d] %s" % (cw(z), z))

out = L[:a] + [L[a]] + NEW + [L[b]] + L[b + 1:]
assert len(out) == len(L) - len(old) + len(NEW) + 2, u"行數不等"
assert out[a].startswith(u"```") and out[a + 1 + len(NEW)].startswith(u"```"), u"柵界被吞（新圖須仍在 ``` 之內）"
assert out[:a] == L[:a] and out[a + len(NEW) + 2:] == L[b + 1:], u"段外之行被牽動"
new_raw = u"\r\n".join(out)
if not os.path.exists(BAK):
    shutil.copyfile(SRC, BAK)
io.open(SRC, "w", encoding="utf-8", newline=u"").write(new_raw)
chk = io.open(SRC, encoding="utf-8", newline=u"").read()
assert chk == new_raw, u"回讀不合（疑半檔・換行漂移）"
assert chk.count(u"\r") == chk.count(u"\n") == len(out) - 1
bl2 = BH.fence_blocks(io.open(SRC, encoding="utf-8", newline=u"").read().split(u"\r\n"))
assert len(bl2) == len(BH.fence_blocks(L)), u"柵段數變了（%d → %d）——新圖疑落於圍欄之外" % (
    len(BH.fence_blocks(L)), len(bl2))
assert bl2[4] == [x for x in NEW if x.strip()], u"第 5 段圍欄之內容非新圖（對位失）"
print(u"柵段數：%d（不變）・第 5 段之內容＝新圖（%d 行）✓" % (len(bl2), len(NEW)))
print(u"舊圖 %d 行（含柵）・最寬 %d 格 → 新圖 %d 行（含柵）・最寬 %d 格"
      % (len(old), max(cw(x) for x in old), len(NEW) + 2, max(w)))
print(u"行數：%d → %d（%+d）・字數：%d → %d（%+d）"
      % (len(L), len(out), len(out) - len(L), len(raw), len(new_raw), len(new_raw) - len(raw)))
print(u"SHA：%s → %s（備份 %s）"
      % (sha_old[:12], hashlib.sha256(new_raw.encode("utf-8")).hexdigest()[:12], os.path.basename(BAK)))
