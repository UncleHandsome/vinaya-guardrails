# -*- coding: utf-8 -*-
"""第 67 輪・甲：新第十章草稿之預修刀（款①歸真／降式樣・數之對合・圍欄重鑄）＋入冊。
法：草稿先行（逐條命中數斷言）→ 自證兩閘（粗體「」須連寫・簡形須零）→ 行錨入冊 →
    CRLF 等式・行數等式・備份・SHA・回讀块體相等。乾跑為預設，--go 始寫檔。
用法：python -X utf8 _work/hlfix67.py [--go]
"""
import os as _hp_os, sys as _hp_sys
_hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__))))
import hulan_path as HP
_hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.abspath(__file__)))
import io
import hashlib
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk
from _simpdict import MAP as SIMP

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
DRAFT = r"C:\Users\lionc\.qoder\tmp\C--Users-lionc-OneDrive-----------------\attachments\bfc14756-f6f1-4240-bfe7-fba2a0d6f592\cff8231b-35c8-439a-bbce-666e6b147f11.txt"
BOOK = HP.SRC
BAK = BOOK + ".bak67a"
GO = "--go" in sys.argv
PUNC = re.compile(u"[，、；：！？「」『』（）()《》〈〉·．。\\-—…﹑＂\"'*＿　\\s]")
PAT1 = re.compile(u"\\*\\*\\s*「([^「」]+?)」\\s*\\*\\*|「\\s*\\*\\*([^「」]+?)\\*\\*\\s*」")

dr_raw = io.open(DRAFT, encoding="utf-8", newline=u"").read()
assert dr_raw.count(u"\r") == dr_raw.count(u"\n") == dr_raw.count(u"\r\n"), u"草稿 CRLF 異常"
D = dr_raw.split(u"\r\n")
if D and not D[-1].strip():
    D = D[:-1]
N0 = len(D)
print(u"草稿 %d 行（去尾空行）" % N0)


def cw(s):
    return sum(2 if ord(c) > 0x2E80 else 1 for c in s)


def do(tag, ln, old, new, want=1):
    i = ln - 1
    c = D[i].count(old)
    assert c == want, u"%s｜稿L%d 命中 %d（欲 %d）：%s" % (tag, ln, c, want, old[:28])
    assert old != new, u"%s｜舊新同形" % tag
    D[i] = D[i].replace(old, new)
    print(u"  %s 稿L%-4d ✓×%d" % (tag, ln, want))


def sub_all(tag, old, new, want):
    n = sum(l.count(old) for l in D)
    assert n == want, u"%s｜全稿命中 %d（欲 %d）" % (tag, n, want)
    for i, l in enumerate(D):
        if old in l:
            D[i] = l.replace(old, new)
    print(u"  %s 全稿 ✓×%d" % (tag, n))


print(u"\n―― 壹・降式樣（本書語／名相借逐字式樣者，去其粗體）――")
for t, ln, s in [
    (u"甲1", 12, u"四提舍尼法（波羅提提舍尼，Pāṭidesanīya）"),
    (u"甲2", 14, u"向人發露、自責悔過"),
    (u"甲3", 43, u"百眾學法（式叉迦羅尼，Sekhiya-dhamma）"),
    (u"甲4", 46, u"突吉羅（Duṣkṛta，惡作）"),
    (u"甲5", 54, u"正念（Sati）的即時心電圖"),
    (u"甲6", 126, u"無責任能力人免責原則"),
    (u"甲7", 140, u"如同在惡臭的糞穢之上，覆蓋上一層厚厚碧綠的青草"),
    (u"甲8", 221, u"自始不成立"),
]:
    do(t, ln, u"**「%s」**" % s, u"「%s」" % s)

print(u"\n―― 貳・歸真（語料有原句者改回原形，已逐條預驗）――")
do(u"乙1", 158, u"甩動肩膀手臂走——「**搖身掉臂如市井浪子**」；衣服鬆垮露出胸腋——「**處處露形如似外道**」",
   u"甩動肩膀走——「**搖身行入白衣舍，如似國王大臣。**」；甩動雙臂走——「**今掉臂行入白衣舍，似如國王大臣長者居士種。**」；"
   u"衣服鬆垮露出胸腋——「**所著衣服不好覆身行入白衣舍，如似婆羅門。**」")
do(u"乙2", 158, u"東張西望——「**左右顧視如似盜竊人**」；當街大笑——「**露齒戲笑如似獼猴**」",
   u"東張西望——「**如似盜竊人，左右顧視行入白衣舍。**」；當街大笑——「**戲笑行入白衣舍，如似獼猴。**」")
do(u"乙3", 158, u"：「白衣舍者村落也，跳行者雙脚跳，蹲坐者尻不至地，左右顧視者處處看，戲笑者露齒而笑。」行後又有坐，每一式各成一戒。",
   u"：「**白衣舍者，村落也。**」「**跳行者，雙脚跳。**」「**蹲坐者，若在地、若在床上，尻不至地。**」"
   u"「**彼左右顧視者，處處看。**」「**戲笑者，露齒而笑。**」「**坐亦如是。**」——行後又有坐，每一式各成一戒。")
do(u"乙4", 161, u"聽浣染香熏已持入。", u"聽浣染香熏已持來入。")
do(u"乙5", 164, u"諸比丘疑，不敢為守護故止宿佛塔中。", u"時有比丘疑，不敢為守護故止宿佛塔中。")
do(u"乙6", 164, u"為守護故，聽。", u"為守護故無犯。")
do(u"乙7", 165, u"若為堅牢，聽。", u"若為堅牢無犯。")
do(u"乙8", 154, u"人在高座己在下座不得為說法，尸叉罽賴尼。",
   u"人在高坐己在下坐不得為說法，除病，尸叉罽賴尼。")
do(u"乙9", 154, u"不得為持杖、持蓋、持刀劍、乘車馬者說法，尸叉罽賴尼。",
   u"人持杖不應為說法，尸叉罽賴尼。」「人持蓋不應為說法，除病，尸叉罽賴尼。」「不得為騎乘者說法，除病，尸叉罽賴尼。")
do(u"乙10", 181, u"不得嚼飯作聲食，式叉迦羅尼。", u"不得嚼飯作聲食，尸叉罽賴尼。")
do(u"乙11", 188, u"大摶飯食，令口不容受", u"大摶飯食，令口不受")
do(u"乙12", 193, u"「口不容受」", u"「口不受」")
do(u"乙13", 231, u"我從生以來未曾憶夢中行淫", u"我從生以來未曾憶夢中行不淨")
do(u"乙14", 231, u"哀求：**「諸長老！莫數詰問我！」**", u"哀求：「諸長老！**莫數詰問我。**」")
do(u"乙15", 249, u"**「大眾在爭鬥中，多犯眾戒、非沙門法，亦作亦說，出入無限。」**",
   u"大眾在爭鬥中，**「多犯眾戒、非沙門法，亦作亦說，出入無限。」**")
do(u"乙16", 250, u"不得如法滅除，令僧不得安樂！", u"不得如法如毘尼、如佛所教滅除諍事，令僧不得安樂！")
do(u"乙17", 192,
   u"私下譏嫌嘲笑：**「此沙門釋子無有慚愧、受取無厭，受食溢鉢似如飢餓貪夫；其進食狼吞虎嚥、嚼食作聲，與豬狗、駱駝、驢牛、烏鳥吃食有何區別？」**",
   u"私下譏嫌嘲笑：**「此沙門釋子無有慚愧、受取無厭。……受食溢鉢，似如飢餓之人貪多。……如似猪狗、駱駝、驢牛、烏鳥食。」**")

print(u"\n―― 參・數之對合與指針歸位――")
do(u"丙1", 172, u"鳥雀、裸形外道、新婚得意者、盜賊、獼猴——居士口中的七個比喻",
   u"鳥雀、裸形婆羅門、新婚憍恣者、國王大臣（二見）、婆羅門、盜竊人、獼猴——居士一連八個比喻")
do(u"丙2", 150, u"十次「我不敢」、十次「佛言聽」", u"五次「我不敢」、六次「佛言聽」")
do(u"丙3", 173, u"**十次「我不敢」與十次「佛言聽」的立法自省：**", u"**五次「我不敢」、六次「佛言聽」的立法自省：**")
do(u"丙4", 221, u"**正當程序的四現前：**", u"**正當程序之三現前：**")
do(u"丙5", 221, u"人現前（被告原告在場）、法現前（律法依據在場）、律現前（審訊程序在場）、僧現前（法定合規人數在場）",
   u"人現前（被告與原告在場）、法現前（律法依據在場）、僧現前（法定合規人數在場）")
do(u"丙6", 169, u"【第二十犍度·塔與法之守護】、【第八章第83條非時入聚落】",
   u"【眾學法之『塔』與『說法』兩組（尸叉罽賴尼）】、【第九章案例四（第83條·非時入聚落博戲）】")
do(u"丙7", 178, u"（眾學法第26～48條，整合原案例一與五）", u"（眾學法第26～48條）")
sub_all(u"丙8", u"兩百五十", u"二百五十", 2)
do(u"丙9", 265, u"整部《四分律·比丘戒本》的二百五十條戒相", u"整部《四分律》之比丘戒本二百五十條戒相")
do(u"丙10", 173, u"佛陀沒有斥責她們多疑", u"佛陀沒有斥責他們多疑")
do(u"丙11", 173, u"「除中間有隔」", u"「中間有隔」")

print(u"\n―― 肆・補條（舊章已歸真而新稿遺落者，以內容錨定位插行）――")


def ins_after(anchor, block, tag):
    hits = [i for i, l in enumerate(D) if anchor in l]
    assert len(hits) == 1, u"%s｜錨命中 %d（欲 1）：%s" % (tag, len(hits), anchor[:24])
    D[hits[0] + 1:hits[0] + 1] = block
    print(u"  %s 插入 %d 行（錨 L%d 之後）" % (tag, len(block), hits[0] + 1))


ins_after(u"病比丘疲極不堪蹲", [u"  「**彼疑，不敢為病人說法。**」佛答：**「聽。**」  "], u"丁1")
ins_after(u"細判三段式", [u"", u"> （按：上兩行律文一作『式叉迦羅尼』、一作『尸叉罽賴尼』，乃同一梵語之異譯，"
                         u"皆指百眾學法——『應學』之義。律文兩見，今存其舊，讀者不必疑為兩罪。）"], u"丁2")

print(u"\n―― 伍・圍欄三段之重鑄（舊稿溢框：86／89／83 格）――")
FENCE = [
    [u"【百眾學法（100條）之四大雷達網】",
     u"├─ 行止與穿衣（第1～25條）",
     u"│    齊整著衣、不跳行、不搖身晃肩、不左右顧視",
     u"├─ 飲食與受食（第26～48條）",
     u"│    不大摶食、不含食語、不嚼食作聲、不舔手",
     u"├─ 衛生與敬自然（第49～51條）",
     u"│    不生草上便溺、不水中大小便涕唾、不無病立大小便（慈護微蟲）",
     u"└─ 為人在說法（第52～100條）",
     u"     不為持杖、持刀劍、覆頭、乘車、高坐者說（捍衛真理尊嚴）",
     u"歸  時時刻刻身念處：在最微末處檢測神經系統的放逸度"],
    [u"【七滅諍法：平息內部戰火的最高司法程序】",
     u"├─ 程序與人權保障",
     u"│    ① 現前毘尼（當面審理·缺席不判）",
     u"│    ② 憶念毘尼（證聖清白・一事不再理）",
     u"│    ③ 不癡毘尼（精神失常免責）",
     u"├─ 實質正義與心理審查",
     u"│    ④ 自言治（口供自願・禁止刑訊）",
     u"│    ⑤ 罪處所／覓罪相（前後相違者即此定罪）",
     u"└─ 大局和合與集體赦免",
     u"     ⑥ 多人覓罪（知法者多數決）",
     u"     ⑦ 如草覆地（微細口過全體一筆勾銷）",
     u"歸  徹底撲滅第十、十一僧殘「破和合僧」，杜絕僧團走向政治分裂"],
    [u"【比丘二百五十戒：立體城郭防禦全景（由外而內）】",
     u"├─ 最外層護城河與斥候哨所｜百眾學法（100條）、四提舍尼（4條）",
     u"│    監控行走、穿衣、飲食細行與受食邊界，時刻啟動身念處「動態雷達」。",
     u"├─ 外城牆與動態警戒陣地｜九十單提法（前半部 第1～45條）",
     u"│    封鎖妄語、兩舌、獨處、非時食，阻斷起心動念的私密滲透。",
     u"│    （二不定法 2條・別附於第六章第三節）",
     u"├─ 物資軍械管制與內城門｜三十捨墮法（30條）",
     u"│    強制沒收長衣、長鉢、自手摸錢，在物理上徹底抽乾「偷盜」溫床。",
     u"├─ 內城防暴與法治陣地｜九十單提法（後半部 第46～90條）",
     u"│    阻斷肢體暴擊、邪見異端、流氓議事與傲慢特權，守護程序正義。",
     u"├─ 皇城宮牆與加護救治所｜十三僧殘法（13條）",
     u"│    攔截性騷擾、造謠誣告與組織分裂；以別住、摩那埵開復健之路。",
     u"├─ 國王的心臟與宗廟｜四大波羅夷（4條・根本性戒）",
     u"│    絕對不可逾越的死線：斷絕殺、盜、婬、妄，失守即僧格暴斃。",
     u"└─ 最高憲法法院｜七滅諍法（7條・司法閉環）",
     u"     爭端爆發時以現前、憶念、罪處所與如草覆地平息內亂，守護和合。"],
]
marks = [i for i, l in enumerate(D) if l.startswith(u"```")]
for blk in FENCE:                             # 書中之制：分隔點用『·』U+00B7，不用『・』U+30FB
    for k, x in enumerate(blk):
        blk[k] = x.replace(u"・", u"·")
assert len(marks) == 6, u"圍欄標記 %d 枚（欲 6）" % len(marks)
for k in (2, 1, 0):                     # 由後往前，免插拔亂序
    a, b = marks[2 * k], marks[2 * k + 1]
    old_w = max(cw(x) for x in D[a + 1:b])
    D[a + 1:b] = FENCE[k]
    new_w = max(cw(x) for x in FENCE[k])
    assert new_w <= 72, u"段%d 仍寬 %d 格" % (k + 1, new_w)
    print(u"  段%d 重鑄：%d 行・%d 格 → %d 行・%d 格" % (k + 1, b - a - 1, old_w, len(FENCE[k]), new_w))

print(u"\n―― 陸・自證兩閘（寫檔前必過）――")
txt = u"\r\n".join(D)
bad = []
for i, l in enumerate(D):
    for m in PAT1.finditer(l):
        s = (m.group(1) or m.group(2)).strip()
        for frag in re.split(u"……|…", s):
            nb = _tk.norm(PUNC.sub(u"", frag))
            if len(nb) >= 4 and nb not in _tk.VINAYA:
                bad.append((i + 1, frag[:44]))
print(u"  款①之連寫：粗體「」逐一核語料｜無據 %d 枚" % len(bad))
for i, f in bad:
    print(u"    × 稿L%-4d %s" % (i, f))
assert not bad, u"款①閘未過"
assert u"・" not in txt, u"稿內有 U+30FB『・』（書中之制為 U+00B7『·』）"
CORPF = set(_tk.VINAYA)                       # 豁免自算：見於語料之形只查引號外（與 simp_sweep 同口徑）
spans = [m.span() for m in re.finditer(u"「[^」]*」", txt)]
inq = lambda i: any(a <= i < b for a, b in spans)
simp = []
for ch, tr in SIMP.items():
    if ch in CORPF:
        for m in re.finditer(re.escape(ch), txt):
            if not inq(m.start()):
                simp.append((ch, tr, txt[:m.start()].count(u"\r\n") + 1))
    else:
        for m in re.finditer(re.escape(ch), txt):
            simp.append((ch, tr, txt[:m.start()].count(u"\r\n") + 1))
print(u"  簡形（緊口徑・引號內豁免）：%d 枚" % len(simp))
assert not simp, u"簡形殘留：%s" % simp[:6]
NCASE = sum(1 for l in D if l.startswith(u"#### 案例"))
NFENCE = sum(1 for l in D if l.startswith(u"```"))
assert NCASE == 5 and NFENCE == 6, u"案例 %d・圍欄標記 %d" % (NCASE, NFENCE)
print(u"  形制：案例 %d 則・圍欄 %d 段・行數 %d→%d" % (NCASE, NFENCE // 2, N0, len(D)))
print(u"  新寫之逐字串（目視覆讀・以內容錨點名）：")
for anchor in [u"甩動肩膀", u"白衣舍者，村落也", u"人持杖不應為說法", u"不敢為病人說法",
               u"私下譏嫌嘲笑", u"不得嚼飯作聲食", u"按：上兩行律文", u"五次「我不敢」",
               u"正當程序之三現前", u"【第九章案例四（第83條"]:
    for i, l in enumerate(D):
        if anchor in l:
            print(u"    稿L%-4d %s" % (i + 1, l[:176]))

if not GO:
    print(u"\n（乾跑：加 --go 始入冊）")
    sys.exit(0)

print(u"\n―― 柒・入冊（取代舊第十章）――")
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert raw.count(u"\r") == raw.count(u"\n") == raw.count(u"\r\n"), u"正本入口 CRLF 已傷"
L = raw.split(u"\r\n")
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()
i10 = next(i for i, l in enumerate(L) if l == u"# 第十章 提舍尼、眾學法與七滅諍")
i11 = next(i for i, l in enumerate(L) if l.startswith(u"# 第十一章"))
assert L[i11 - 1] == u"" and L[i11 - 2] == u"---", u"下章界非『---＋空行』：%r/%r" % (L[i11 - 2], L[i11 - 1])
assert L[i10 - 1] == u"" and L[i10 - 2] == u"---", u"上章界非『---＋空行』"
blk = D[2:] + [u"", u"---"]
NEWL = L[:i10] + blk + L[i11 - 1:]
print(u"  舊章 %d 行 → 新章 %d 行｜全書 %d → %d 行" % (i11 - 1 - i10, len(blk), len(L), len(NEWL)))
out = u"\r\n".join(NEWL)
assert out.count(u"\r") == out.count(u"\n") == len(NEWL) - 1, u"CRLF 變形"
assert not os.path.exists(BAK) or io.open(BAK, encoding="utf-8", newline=u"").read() == raw, \
    u"備份已存在且非同本（先核對再續）：%s" % BAK
if not os.path.exists(BAK):
    shutil.copy2(BOOK, BAK)
with open(BOOK, "wb") as fh:                       # 二進位寫：免 text 模式之 newline 雙譯
    fh.write(out.encode("utf-8"))
chk = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert chk == out, u"回讀不符"
back = chk.split(u"\r\n")
j = next(i for i, l in enumerate(back) if l == u"# 第十章 提舍尼、眾學法與七滅諍")
assert back[j:j + len(blk)] == blk, u"回讀块體不等"
print(u"  已寫檔｜sha %s→%s｜備份 %s" % (sha0[:12], hashlib.sha256(chk.encode("utf-8")).hexdigest()[:12],
                                        os.path.basename(BAK)))
print(u"  全書 %d 行｜案例 %d 則｜圍欄 %d 段" % (
    len(back), sum(1 for l in back if re.match(u"^#### (?:★ )?案例", l)),
    sum(1 for l in back if l == u"```") // 2))
