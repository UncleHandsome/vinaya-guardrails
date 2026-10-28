# -*- coding: utf-8 -*-
"""第 64 輪・乙：新第六章入冊之後的三件跟刀。

 一・印面段落之黑塊：案例五之【案發現場】四拍併為一段（495 字），§四・2 兩拍併為一段（327 字）
    ——於語意轉折處補空行（一字不增刪，只改分段）。理據：第 20 報之治法＝補空行不分段。
 二・「微型道場之困」：作者之「佛陀准許集結鄰近道場……」乃推衍而非律據，移入【按】內如實標名，
    並保留第 59 輪所正之四級判（出罪必滿二十，邊地唯開受戒）。按語段之戶口亦由此還缺一補十。
 三・入冊後之指針歸位：二不定法已不列案例，凡指「第六章案例六」而意在有不定法者一律改指附論；
    第六章舊文之「六群」既隨舊稿而退，第九章靶點之括註亦須除（指針不可指書中無有之事）。
用法：python -X utf8 _work/hlfix64b.py [--go]
"""
import hashlib
import io
import os
import shutil
import sys

GO = u"--go" in sys.argv
BOOK = u"佛陀的護欄 四分律比丘與比丘尼戒的行為心理學解析.txt"
BAK = BOOK + u".bak64b"

raw = io.open(BOOK, "rb").read()
sha0 = hashlib.sha256(raw).hexdigest()
L = raw.decode("utf-8").split(u"\r\n")
assert raw.count(b"\r") == raw.count(b"\n"), u"入口 CRLF 已傷"
N0 = len(L)
print(u"正本 sha %s｜%d 行" % (sha0[:12], N0))


def find1(sub, start=0):
    hits = [i for i in range(start, len(L)) if sub in L[i]]
    assert len(hits) == 1, u"錨『%s』命中 %d 枚（須 1）" % (sub[:28], len(hits))
    return hits[0]


def rep(tag, sub, new, cnt=1):
    """整行替換：先以唯一錨定位，再驗行內命中數。"""
    global L
    i = find1(sub)
    c = L[i].count(sub)
    assert c == cnt, u"%s｜錨於该行命中 %d（欲 %d）" % (tag, c, cnt)
    L[i] = L[i].replace(sub, new)
    print(u"  %s L%-5d ✓" % (tag, i + 1))


# ── 一・案例五【案發現場】之四拍分段 ────────────────────────────────
BEATS = [u"  提婆達多為了奪取僧團領導權", u"  手握世俗政經特權的提婆達多",
         u"  全案最險惡的環節記錄在第11條", u"  面對這場動搖法統的憲政危機"]
ins = []
for n, b in enumerate(BEATS):
    i = find1(b)
    assert L[i].startswith(b), u"拍『%s』非行首：%s" % (b[:12], L[i][:20])
    if n:
        ins.append(i)
    if n < 3:
        assert L[i].endswith(u"  "), u"拍 %d 行尾無硬斷之兩空格，口徑已變" % (n + 1)
        L[i] = L[i].rstrip()
print(u"  分段之據：四拍俱以硬斷相連（行尾雙空格），今改為空行分隔")

for i in sorted(ins, reverse=True):
    L[i:i] = [u""]
print(u"  一 補空行 %d 處（案例五之【案發現場】495 字 → 四段）" % len(ins))

# ── 二・§四・2「微型道場之困」之重排（義不動，歸屬如實） ────────────
i1 = find1(u"在古代，二十人僧雲集的僧伽藍極為普遍")
i2 = find1(u"律藏在犍度中早已留下了宏大的法理生機")
assert i2 == i1 + 1 and L[i1].endswith(u"  "), u"§四・2 兩拍之界與預期不合"
NEW = [
    u"在古代，二十人僧雲集的僧伽藍極為普遍；但在現代社會，多數都市精舍或鄉村道場常處於「一師二三眾」"
    u"的微型規模。這引發了無數現代律學者的焦慮：若道場人數不足二十人，是否意味著犯僧殘者將永遠無法出罪、"
    u"陷入絕境？",
    u"",
    u"律藏在犍度中早已留下了宏大的法理生機：**僧團的法權隨教法而立，不隨地理而絕。**"
    u"制度的本質是為了救拔受傷的生命，絕非為了在算術上將迷途者逼上絕路。",
    u"",
    u"**按：邊地四級之判。** 律於僧數本有四級之判（四人、五人、十人、二十人），四級各有開除："
    u"四人僧除自恣、受大戒、出罪；五人僧於中國亦除受大戒與出罪（邊地於受戒得開）；"
    u"十人僧除出罪；二十人僧則一切羯磨應作。然所開者唯受戒之緣，出罪一法必滿二十，無得而減。"
    u"故僧數不具之處，得集結鄰近道場之大僧，或由行者前往足數之清淨大寺請求出罪"
    u"——此係本書據律意之推衍，非律之明文。",
]
L[i1:i2 + 1] = NEW
print(u"  二 §四・2 重排為三段（原兩拍 327 字・四級判與推衍之標俱在）")

# ── 三・指針歸位 ─────────────────────────────────────────────────────
rep(u"三1 十線地圖", u"| 第六章案例六 | 二不定法第1、2條 |",
    u"| 第六章第三節附論 | 二不定法第1、2條 |")
rep(u"三2 城牆圖之按", u"本書依戒本次第把它列在第六章案例六，其如何斷",
    u"本書依戒本次第把它列在第六章第三節之附論，其如何斷")
rep(u"三3 七滅諍靶點", u"【第六章案例六：二不定法——證言與自陳的分層】",
    u"【第六章附論：二不定法——證言與自陳的分層】")
rep(u"三4 六群之括註", u"【第十七群童子之另一面（第六章僧殘之六群）】",
    u"【第十七群童子之另一面】")
for sub in (u"第六章案例六", u"僧殘之六群"):
    left = [i + 1 for i, l in enumerate(L) if sub in l]
    print(u"  覆核：書中殘留『%s』%d 處 %s" % (sub, len(left), left))

# ── 出口自證 ─────────────────────────────────────────────────────────
txt = u"\r\n".join(L)
assert txt.count(u"\r") == txt.count(u"\n") == len(L) - 1, u"出口 CRLF 變形"
assert sum(1 for l in L if l.startswith(u"#### 案例")) == 164, u"全書案例之數變形"
assert sum(1 for l in L if l.startswith(u"```")) % 2 == 0, u"圍欄未成對"
print(u"行數 %d→%d" % (N0, len(L)))
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
assert not os.path.exists(BAK), u"備份已存在：%s" % BAK
shutil.copy2(BOOK, BAK)
io.open(BOOK, "w", encoding="utf-8", newline=u"").write(txt)
chk = io.open(BOOK, "rb").read()
print(u"已寫檔｜sha %s→%s｜%d B｜備份 %s" % (
    sha0[:12], hashlib.sha256(chk).hexdigest()[:12], len(chk), os.path.basename(BAK)))
