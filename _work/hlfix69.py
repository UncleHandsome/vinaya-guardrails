# -*- coding: utf-8 -*-
"""第 69 輪・甲：新第十二章草稿之預修刀（去重複 H1・圍欄重鑄・歸真・降式樣・指針與落點）＋入冊。
法：草稿先行（逐條命中數斷言）→ 自證三閘（粗體「」與【律制】須連寫・簡形須零・無 U+30FB）→
    行錨入冊 → CRLF 等式・行數等式・備份・SHA・回讀块體相等。乾跑為預設，--go 始寫檔。
用法：python -X utf8 _work/hlfix69.py [--go]
"""
import os as _hp_os, sys as _hp_sys
_hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__))))
import hulan_path as HP
import hashlib
import io
import os
import re
import shutil
import sys

sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.abspath(__file__)))
import _tk
from _simpdict import MAP as SIMP

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
DRAFT = r"C:\Users\lionc\.qoder\tmp\C--Users-lionc-OneDrive-----------------\attachments\bfc14756-f6f1-4240-bfe7-fba2a0d6f592\8408c013-a228-45b3-8091-9ff7856c96b1.txt"
BOOK = HP.SRC
BAK = HP.bakpath("69a")
GO = "--go" in sys.argv
PUNC = re.compile(u"[，、；：！？「」『』（）()《》〈〉·．。\\-—…﹑＂\"'*＿　\\s]")
PAT1 = re.compile(u"\\*\\*\\s*「([^「」]+?)」\\s*\\*\\*|「\\s*\\*\\*([^「」]+?)\\*\\*\\s*」")

dr_raw = io.open(DRAFT, encoding="utf-8", newline=u"").read()
assert dr_raw.count(u"\r") == dr_raw.count(u"\n") == dr_raw.count(u"\r\n"), u"草稿 CRLF 異常"
D = dr_raw.split(u"\r\n")
assert D[-1] == u"---" and D[-2] == u"", u"草稿末兩行非『空行＋---』：%r" % D[-2:]
N0 = len(D)
print(u"草稿 %d 行（末自帶分隔線）" % N0)

# 舊正本只讀一次，為『迎回舊章自制考訂』取字——長句一律自此截出，不假手重打（逐字須複製）。
book_raw0 = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert book_raw0.count(u"\r") == book_raw0.count(u"\n"), u"正本入口 CRLF 已傷"
B0 = book_raw0.split(u"\r\n")


def harvest(snip, start, endsnip=None):
    hits = [l for l in B0 if snip in l]
    assert len(hits) == 1, u"迎回錨在正本見 %d 處（欲 1）：%s" % (len(hits), snip)
    l = hits[0]
    a = l.index(start)
    return l[a:] if endsnip is None else l[a:l.index(endsnip) + len(endsnip)]


OLD_JING = harvest(u"『八敬』之名本律無文", u"（『八敬』之名")
assert OLD_JING.endswith(u"）"), u"八敬考訂之末非括弧：%r" % OLD_JING[-12:]
OLD_YI = harvest(u"五衣」（於三衣之外", u"（於三衣之外", u"此詞本律無文）")
OLD_RED = harvest(u"調查的一條紅線（本書之程序倫理）", u"* **調查的一條紅線")
assert OLD_RED.startswith(u"* ") and not OLD_RED.endswith(u" "), u"紅線段形異：%r" % OLD_RED[-20:]


def cw(s):
    return sum(2 if ord(c) > 0x2E80 else 1 for c in s)


def do(tag, ln, old, new, want=1):
    i = ln - 1
    c = D[i].count(old)
    assert c == want, u"%s｜稿L%d 命中 %d（欲 %d）：%s" % (tag, ln, c, want, old[:26])
    assert old != new, u"%s｜舊新同形" % tag
    D[i] = D[i].replace(old, new)
    print(u"  %s 稿L%-4d ✓×%d" % (tag, ln, want))


def sub_all(tag, old, new, want):
    n = sum(l.count(old) for l in D)
    assert n == want, u"%s｜全稿命中 %d（欲 %d）：%s" % (tag, n, want, old[:20])
    for i, l in enumerate(D):
        if old in l:
            D[i] = l.replace(old, new)
    print(u"  %s 全稿 ✓×%d" % (tag, n))


print(u"\n―― 壹・形制與 apparatus（刪行留到最後，免行號漂移）――")
do(u"甲2", 99, u"（編按：比丘尼前四波羅夷與大僧同制，其案發現場詳見本書第五章；本章案例解碼由女眾特設之第五波羅夷起編。）",
   u"> （按：比丘尼前四波羅夷與大僧同制，其案發現場詳見本書第五章；本章之案例解碼，由女眾特設之第五波羅夷起編。）")

print(u"\n―― 貳・歸真（律語回原形，俱已預驗連寫）――")
do(u"乙1", 134, u"**「此是我妹！我若向人說，懼彼得惡名稱；若彼得惡名稱，於我亦惡！」**",
   u"**「此坻舍難陀是我妹，今犯波羅夷法。我正欲向人說，懼彼得惡名稱；若彼得惡名稱，於我亦惡！」**")
do(u"乙2", 134, u"**「我先知彼有如是事。」**", u"**「我先知有如是如是罪。」**")
do(u"乙3", 196, u"**「我前後供養此比丘尼之美食，折算市價已達五百金錢，此等資財足夠買下一個世俗女人！」**",
   u"**「我前後與此比丘尼食，計其價可五百金錢，足直一女人。」**")
do(u"乙4", 197, u"**「此比丘尼若非貪愛於我，為何日日受我美食？」**",
   u"**「若此比丘尼意不貪樂我者，何以受我食？」**")
do(u"乙5", 272, u"長老尼嚴肅正告：「今正有此二比丘尼共相覆罪，更無有餘！」",
   u"長老尼嚴肅正告：「今正有此二比丘尼……共相覆罪，更無有餘！」")
do(u"乙6", 136, u"宣揚淫欲非障道之邪見、且抗拒處分的阿梨吒比丘（或頑劣抗諫之闡陀）舉行羯磨",
   u"在拘睒彌宣揚邪見、頑劣抗諫之闡陀比丘舉行羯磨")
sub_all(u"乙7", u"偷蘭難陀", u"偷羅難陀", 12)
do(u"乙8", 113, u"她留下了全律最露骨的一句試探", u"她留下了全律中最露骨的一句自白")
do(u"乙9", 17, u"佛陀才以制定嚴苛的『八敬法』為前提，開許了女性出家僧團的成立。",
   u"佛陀才以制定嚴苛的『八敬法（巴利 Aṭṭhagarudhamma）』為前提，開許了女性出家僧團的成立。" + OLD_JING)
do(u"乙10", 59, u"強制要求比丘尼必須持守「五衣」（增設蔽胸的僧祇支與覆肩衣）",
   u"強制要求比丘尼必須持守「五衣」" + OLD_YI)
print(u"  乙9・乙10 迎回舊章之失考考訂（『八敬』・『厥修羅』俱本律無文，其名出後世）")

print(u"\n―― 參・降式樣（今語與本書術語，去其『「』＋粗體』之自稱逐字形）――")
for t, ln, s in [
    (u"丙1", 143, u"**「內部情感包庇（閨蜜同盟）」**"),
    (u"丙2", 143, u"**「外部盲從權威（盲信叛僧）」**"),
    (u"丙3", 239, u"**「沙門釋迦女毫無慚愧，收容死刑通緝要犯，所謂的佛門精舍，不過是一群女賊的銷贓避難所！」**"),
    (u"丙4", 260, u"**「強制分開居住（別住）」**"),
    (u"丙5", 262, u"**「妳們千萬不要聽僧團的話分開！妳們就要死死抱在一起！寺裡的長老全是在公報私仇、派系打壓！別人搞小圈子僧團都不管，偏偏針對妳們，這是僧團出於嫉妒瞋恨才懲罰妳們！」**"),
    (u"丙6", 268, u"**「物理隔離（強制別住）」**"),
    (u"丙7", 270, u"**「挑動受罰者的受害者心理」**"),
    (u"丙8", 283, u"**「我不幹了！我今天就退出佛門，捨佛、捨法、捨僧！天底下又不是只有你們釋迦牟尼佛一家能修道，外道婆羅門多了去了，我大可以去他們那裡出家修梵行！」**"),
    (u"丙9", 285, u"**「這場審判根本不公！主持羯磨的那些大長老尼全都在搞偏袒——她們有偏愛（愛）、有私怨（恚）、畏懼強權（怖）、糊塗無能（癡）！僧團上下全是一群昏官！」**"),
]:
    do(t, ln, s, s[2:-2])

print(u"\n―― 肆・指針・落點・數之對合――")
do(u"丁1", 50, u"（單提第101條露身浴戒之因緣）", u"（尼單提第101條露身浴戒之因緣，見第十四章案例二）")
do(u"丁2", 93, u"在屏處坐直接入單提（第80、81條）", u"在屏處坐直接入單提（尼單提第80、81條，見第十四章案例十七）")
do(u"丁3", 166, u"#### 1. 為什麼女眾僧殘沒有「營造二戒」與「自慰四階」？",
   u"#### 1. 為什麼女眾僧殘沒有「營造二戒」與「自慰四階」？（同制七條：尼僧殘第1、2、3、10、11、12、13條）")
do(u"丁4", 167, u"比丘僧殘前四條（身相觸、粗惡語、自歎身索供）在女眾端**完全消失**——因為佛陀直接將這一切調情與接觸，升格到了前述的第五、第六「波羅夷死罪」！",
   u"比丘僧殘之前四條（故漏失、身相觸、粗惡語、自歎身索供）在女眾端**全數改判**——漏失一條本非女身所涉，"
   u"其餘三條之調情與接觸，佛陀直接升格到了前述的第五、第六「波羅夷死罪」！")

print(u"\n―― 伍・刪行與補行（刪留最後・補以內容錨，免行號漂移）――")
H1 = u"# 第十二章 為什麼比丘尼戒更多？"
dup = [i for i, l in enumerate(D) if l == H1]
assert len(dup) == 2, u"本章 H1 見 %d 處（稿之上篇與下篇各一）：%s" % (len(dup), [x + 1 for x in dup])
del D[dup[1]]
print(u"  甲1 刪稿L%d 重複 H1 ✓（全書仍 20 個 H1）" % (dup[1] + 1))
a = [i for i, l in enumerate(D) if l.startswith(u"  4. **沙彌尼在場的司法意義：**")]
assert len(a) == 1, u"紅線段之插入點見 %d 處" % len(a)
D.insert(a[0] + 1, u"  5. " + OLD_RED[2:].replace(u"：**律之判準", u"：** 律之判準"))
print(u"  乙11 補回舊章『調查的一條紅線（本書之程序倫理）』為案例剖析第 5 項（稿L%d）" % (a[0] + 2))

print(u"\n―― 陸・圍欄三段之重鑄（舊稿溢框：83／101／96 格）――")
FENCE = [
    [u"【比丘尼八波羅夷之立體結構】",
     u"├─ 第一重城牆：四條根本共通性戒（第1～4條・大僧同名而尼端別宣）",
     u"│    ① 斷頭婬戒（不淨行，乃至共畜生）",
     u"│    ② 斷頭盜戒（盜滿五錢，王法應死）",
     u"│    ③ 斷頭殺戒（殺人、讚死、勸死）",
     u"│    ④ 斷頭大妄語戒（未證言證聖法）",
     u"└─ 第二重城牆：四條女眾特設死罪（第5～8條・將死線大幅前推）",
     u"     ⑤ 摩觸戒（受染心男子撫摩，腋下至膝上）",
     u"     ⑥ 八事成重戒（約會、牽手、屏處幽會八事）",
     u"     ⑦ 覆藏重罪戒（知同修破大戒而包庇隱匿）",
     u"     ⑧ 隨順被舉比丘戒（附和對抗全體僧團之叛僧）"],
    [u"【比丘尼十七僧殘之結構解剖】",
     u"├─ 七條與大僧同制",
     u"│    媒嫁（1）、無根謗（2）、取片謗（3）、破和合僧（10）、",
     u"│    伴黨助破（11）、污家（12）、惡性不受諫（13）。",
     u"└─ 十條女眾專屬特設",
     u"     獨行四事（7）、染心受食（8）、教人受食（9）、詣官言人（4）、",
     u"     出界外解罪（6）、度賊女（5）、共住覆罪（14）、教莫別住（15）、",
     u"     小事瞋捨三寶（16）、謗僧四偏（17）。"],
    [u"【比丘尼重戒背後的三大人性深淵】",
     u"├─ 深淵一：依附心理與肉體代價（摩觸、八事、染心受食）",
     u"│    渴望透過男性的物質與情感青睞尋求安全感，",
     u"│    最終被迫在肉體與僧格上支付慘烈代價。",
     u"├─ 深淵二：名譽同盟與司法失明（覆藏重罪、展轉覆罪）",
     u"│    將私人情感與面子維護置於公共正義之上，",
     u"│    形成阻礙糾錯的黑箱攻守同盟。",
     u"└─ 深淵三：受害者敘事與解構反噬（捨三寶、謗僧四偏、詣官）",
     u"     遭遇挫折時迅速退化為極端抗拒，撕毀契約、砸碎法庭，",
     u"     企圖利用世俗暴力或陰謀論實施反擊。"],
]
marks = [i for i, l in enumerate(D) if l.startswith(u"```")]
assert len(marks) == 6, u"圍欄標記 %d 枚（欲 6）" % len(marks)
for blk in FENCE:
    for k, x in enumerate(blk):
        blk[k] = x.replace(u"・", u"·").replace(u"・", u"·")
for k in (2, 1, 0):
    a, b = marks[2 * k], marks[2 * k + 1]
    old_w = max(cw(x) for x in D[a + 1:b])
    D[a + 1:b] = FENCE[k]
    new_w = max(cw(x) for x in FENCE[k])
    assert new_w <= 72, u"段%d 仍寬 %d 格" % (k + 1, new_w)
    print(u"  段%d 重鑄：%d 行・%d 格 → %d 行・%d 格" % (k + 1, b - a - 1, old_w, len(FENCE[k]), new_w))

print(u"\n―― 柒・自證三閘（寫檔前必過）――")
txt = u"\r\n".join(D)
# 本稿之條文欄作「> **【第N…·條文】：** 律文」之形，律文不入引號，
# 故款①之硬尺須另辟一徑：以【…條文】標籤為凭，取其後全文直接對語料連寫。
LABR = re.compile(u"^>\\s*\\*\\*【([^】]*條文)[^】]*】：\\*\\*\\s*(.+)$")
bad, tiao, nclaim = [], {}, 0
for i, l in enumerate(D):
    cands = [m.group(1) or m.group(2) for m in PAT1.finditer(l)]
    if l.startswith(u">") and (u"律制" in l[:16] or u"律文" in l[:16] or u"波羅夷·條文" in l[:24]
                            or u"僧殘·條文" in l[:24]):
        cands += [m.group(1) for m in re.finditer(u"「([^「」]+?)」", l)]
    m = LABR.match(l)
    if m:
        cands.append(m.group(2))
        tiao[i] = (m.start(2), m.end(2))
    nclaim += len(cands)
    for s in cands:
        for frag in re.split(u"……|…", s.strip()):
            nb = _tk.norm(PUNC.sub(u"", frag))
            if len(nb) >= 4 and nb not in _tk.VINAYA:
                bad.append((i + 1, frag[:44]))
print(u"  逐字閘（款①＋【律制】＋條文欄）：管轄 %d 枚（其中條文欄 %d 行）・無據 %d 枚"
      % (nclaim, len(tiao), len(bad)))
for i, f in bad:
    print(u"    × 稿L%-4d %s" % (i, f))
assert not bad, u"逐字閘未過"
assert len(tiao) == 14, u"條文欄 %d 行（稿實 14 行，尺若少覆便是空尺）" % len(tiao)
CORPF = set(_tk.VINAYA)
simp = []
for i, l in enumerate(D):
    ex = [(m.start(), m.end()) for m in re.finditer(u"「[^」]*」", l)]
    if i in tiao:
        ex.append(tiao[i])
    for ch in SIMP:
        for m in re.finditer(re.escape(ch), l):
            if ch in CORPF and any(a <= m.start() < b for a, b in ex):
                continue
            simp.append((ch, i + 1, l[max(0, m.start() - 10):m.start() + 10]))
print(u"  簡形（緊口徑・引號與已驗條文欄內語料自有者豁免）：%d 枚" % len(simp))
for ch, i, ctx in simp:
    print(u"    × 稿L%-4d %s『%s』%s" % (i, u"「%s」" % ch, ctx))
assert not simp, u"簡形殘留"
assert u"・" not in txt, u"稿內有 U+30FB『・』"
NEG = 0
for i, l in enumerate(D):
    m = LABR.match(l)
    if not m:
        continue
    b = m.group(2)
    k = len(b) // 2
    NEG += 1 if _tk.norm(PUNC.sub(u"", b[:k] + u"假" + b[k + 1:])) not in _tk.VINAYA else 0
print(u"  新尺負測（條文欄逐條亂改一字，%d 條須全逮）：逮 %d 條" % (len(tiao), NEG))
assert NEG == len(tiao), u"條文欄之尺為空尺：亂改竟不被逮"
NCASE = sum(1 for l in D if l.startswith(u"#### 案例"))
NH1 = sum(1 for l in D if l.startswith(u"# 第"))
assert NCASE == 7 and NH1 == 1, u"案例 %d・H1 %d" % (NCASE, NH1)
print(u"  形制：案例 %d 則・本章 H1 %d 個・圍欄 3 段・行數 %d→%d" % (NCASE, NH1, N0, len(D)))
print(u"  改後之要緊行（目視覆讀）：")
for anchor in [u"此坻舍難陀是我妹", u"足直一女人", u"何以受我食", u"偷蘭難陀", u"（按：比丘尼前四波羅夷",
               u"同制七條：尼僧殘第", u"故漏失", u"尼單提第101條", u"尼單提第80、81條",
               u"『八敬』之名本律無文", u"厥修羅", u"調查的一條紅線"]:
    for i, l in enumerate(D):
        if anchor in l:
            print(u"    稿L%-4d %s" % (i + 1, l[:150]))

if not GO:
    print(u"\n（乾跑：加 --go 始入冊）")
    sys.exit(0)

print(u"\n―― 柒・入冊（取代舊第十二章）――")
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert raw.count(u"\r") == raw.count(u"\n") == raw.count(u"\r\n"), u"正本入口 CRLF 已傷"
L = raw.split(u"\r\n")
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()
i12 = next(i for i, l in enumerate(L) if l == u"# 第十二章 為什麼比丘尼戒更多？")
i13 = next(i for i, l in enumerate(L) if l.startswith(u"# 第十三章"))
assert L[i13 - 1] == u"" and L[i13 - 2] == u"---", u"下章界非『---＋空行』"
assert L[i12 - 1] == u"" and L[i12 - 2] == u"---", u"上章界非『---＋空行』"
blk = D[2:]
NEWL = L[:i12] + blk + L[i13 - 1:]
print(u"  舊章 %d 行 → 新章 %d 行｜全書 %d → %d 行" % (i13 - 1 - i12, len(blk), len(L), len(NEWL)))
out = u"\r\n".join(NEWL)
assert out.count(u"\r") == out.count(u"\n") == len(NEWL) - 1, u"CRLF 變形"
assert not os.path.exists(BAK) or io.open(BAK, encoding="utf-8", newline=u"").read() == raw, u"備份不同本"
if not os.path.exists(BAK):
    shutil.copy2(BOOK, BAK)
with open(BOOK, "wb") as fh:
    fh.write(out.encode("utf-8"))
chk = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert chk == out, u"回讀不符"
back = chk.split(u"\r\n")
j = next(i for i, l in enumerate(back) if l == u"# 第十二章 為什麼比丘尼戒更多？")
assert back[j:j + len(blk)] == blk, u"回讀块體不等"
print(u"  已寫檔｜sha %s→%s｜備份 %s" % (sha0[:12], hashlib.sha256(chk.encode("utf-8")).hexdigest()[:12],
                                        os.path.basename(BAK)))
print(u"  全書 %d 行｜案例 %d 則｜H1 %d 個｜圍欄 %d 段" % (
    len(back), sum(1 for l in back if re.match(u"^#### (?:★ )?案例", l)),
    sum(1 for l in back if re.match(u"^# 第[一二三四五六七八九十]+章", l)),
    sum(1 for l in back if l == u"```") // 2))
