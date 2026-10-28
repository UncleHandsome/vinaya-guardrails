# -*- coding: utf-8 -*-
"""第 66 輪・甲：換入作者新第八章＋新第九章（預修＋入冊）。

口徑承 64／65 輪，四條：
 一・款①（粗體＋「」）須於 _tk.VINAYA 連寫可查——可歸真者歸真，屬本書評語者降其式樣（義不動）。
    本稿 38 段無據：歸真 9・降式樣 29（含『（括注）』移出引號者 4）。
 二・計數須對實際（hlchk 甲軸）：稿之『四大防御板塊／四大防禦重鎮』而正文各有五層，俱改『五』。
 三・標題形制：『#### ★ 案例十三（…）：…』不合全書『#### 案例N：…』之式（案例之數
    由諸尺共計：case_inventory／apxchk／gen_appendix／tocsync／refchk）➔歸正式，壓軸之評移入副題。
 四・圍欄四段俱自溢（90／85／102／86 格）➔改單欄樹，節點俱附主幹，單行不越 72 格。
另：稿內『第 N 條』之半形空格，一律歸全書通例『第N條』（形制畫一，且免生指針解析之分岔）。
用法：python -X utf8 _work/hlfix66.py [--go]
"""
import hashlib
import io
import os
import re
import shutil
import sys

sys.path.insert(0, os.getcwd())
import _tk  # noqa: E402

GO = u"--go" in sys.argv
BOOK = u"佛陀的護欄 四分律比丘與比丘尼戒的行為心理學解析.txt"
DFT = r"C:\Users\lionc\.qoder\tmp\C--Users-lionc-OneDrive-----------------\attachments\bfc14756-f6f1-4240-bfe7-fba2a0d6f592\80c6b263-a8e0-4499-951a-a69b036d998a.txt"
BAK = BOOK + u".bak66a"

PUNC = re.compile(u"[，。、：；！？『「』』\"'" + u"\\s" + u"（）()《》·＝]")
PAT1 = re.compile(u"\\*\\*\\s*「([^「」]+?)」\\s*\\*\\*|「\\s*\\*\\*([^「」]+?)\\*\\*\\s*」")


def has(s):
    return _tk.norm(PUNC.sub(u"", s)) in _tk.VINAYA


raw = io.open(DFT, "rb").read()
D = raw.decode("utf-8").replace(u"\r\n", u"\n").split(u"\n")
assert D[2] == u"# 第八章 九十單提（上）" and D[343] == u"# 第九章 九十單提（下）", u"新稿之章界不合"
assert D[-1].startswith(u"在接下來的"), u"新稿之尾不合"
N0 = len(D)
print(u"新稿 %d 行｜sha %s｜第八章 稿L3–L343｜第九章 稿L344–L%d" % (
    N0, hashlib.sha256(raw).hexdigest()[:12], N0))


def rep(tag, idx, old, new, want=1):
    l = D[idx - 1]
    c = l.count(old)
    assert c == want, u"%s｜稿L%d 錨命中 %d（欲 %d）：%s" % (tag, idx, c, want, old[:32])
    for m in PAT1.finditer(new):
        s = (m.group(1) or m.group(2)).replace(u"**", u"")
        for frag in re.split(u"……|…", s):
            nb = _tk.norm(PUNC.sub(u"", frag))
            if len(nb) >= 4:
                assert has(nb), u"%s：新文掛逐字式樣而語料無據 → %s" % (tag, frag[:40])
    D[idx - 1] = l.replace(old, new)
    return c


NREP = [0]


def do(tag, idx, old, new, want=1):
    NREP[0] += rep(tag, idx, old, new, want)
    print(u"  %s 稿L%-4d ✓×%d" % (tag, idx, want))


# ── 甲・形制畫一：『第 N 條』之半形空格歸例 ──────────────────────────
SP1 = re.compile(u"第\\s+(?=[0-9])")
SP2 = re.compile(u"(?<=[0-9、～~])\\s+條")
SP3 = re.compile(u"([～~])\\s+(?=[0-9])")
nrm = 0
for i, t in enumerate(D):
    u = SP3.sub(u"\\g<1>", SP2.sub(u"條", SP1.sub(u"第", t)))
    if u != t:
        nrm += 1
        D[i] = u
print(u"  甲 條號空格歸例｜%d 行" % nrm)

# ── 乙・計數與標題之形制（先於他刀，因錨以歸例後之形為準） ───────────
do(u"乙1 板塊之數", 17, u"鎖定了凡夫在日常中最容易失控的四大前線陣地：**「言語的欺瞞與挑撥」**、"
   u"**「空間獨處引發的情欲幾何」**、**「飲食的特權與口腹節制」**，以及**「對微細生命的敬畏」**。",
   u"鎖定了凡夫在日常中最容易失控的五大前線：**言語的欺瞞與挑撥**、**空間獨處引發的情欲幾何**、"
   u"**飲食的特權與口腹節制**、**對微細生命的敬畏**，以及**共有秩序與二部僧之邊界**。")
do(u"乙2 節題之數", 21, u"### 二、 前半部四大防禦板塊矩陣（第1～45條）",
   u"### 二、 前半部五大防禦板塊矩陣（第1～45條）")
do(u"乙3 重鎮之數", 365, u"### 二、 後半部四大防禦重鎮全新矩陣（第46～90條）",
   u"### 二、 後半部五大防禦重鎮全新矩陣（第46～90條）")
do(u"乙4 壓軸案例歸正式", 658,
   u"#### ★ 案例十三（全篇終極壓軸大案）：神格僭奪與扮演上帝的終結——與如來等量作衣戒（第90條）",
   u"#### 案例十三：與如來等量作衣戒（第90條）——全篇終極壓軸大案，神格僭奪與扮演上帝的終結")

# ── 丙・款①之歸真（九處，俱以 _tk.VINAYA 連寫為準） ─────────────────
do(u"丙1 貪餮之問", 203, u"**「汝實爾貪餮，不知足食、不足食耶？」**",
   u"**「汝實爾，貪餮不知足食不足食、不知餘食不餘食，得便食之耶？」**")
do(u"丙2 嫌窄之詞", 278, u"**「彼嫌窄者自當去」**",
   u"**「彼若嫌窄者，自當避我去」**")
do(u"丙3 軍陣之譏", 449, u"**「我等為國難恩愛興此軍陣，汝等出家人往軍中何所作，乃為箭所射耶？」**",
   u"**「我等為恩愛故興此軍陣，汝等出家人往軍中何所作耶？」**")
do(u"丙4 蛤蟆之問", 484, u"**「此娑伽陀比丘癡人！如今還能降伏一隻小蛤蟆不？如今不能降伏小龍，況能降伏大龍！」**",
   u"（旁有溝中蟾蜍爬過其面，舐食嘔吐之物。）佛陀停下腳步，指著地上的娑伽陀，"
   u"對阿難說出了全律藏最冷酷的一句反問：**「此娑伽陀比丘癡人！如今不能降伏小龍，況能降伏大龍！」**")
do(u"丙5 草木頭之禁", 485, u"**「自今已去，乃至不得以草木頭內著酒中而入口！」**",
   u"**「自今以去，以我為師者，乃至不得以草木頭內著酒中而入口！」**")
do(u"丙6 不學此戒", 515, u"**「我現在不學這條戒！等我去請教其他精通律法的大律師比丘之後再說！」**",
   u"**「我今不學此戒，當問餘智慧持律比丘。」**——把『質疑法律本身的權威性』当作拖字訣，"
   u"企圖以此無限期癱瘓審判。")
do(u"丙7 詐稱始知", 534, u"**「哎呀！我今天才是頭一次知道戒經裡居然寫了這條法規呢！這部戒本不是每半個月都在宣讀嗎？我以前怎麼完全不知道！」**",
   u"滿臉無辜、裝瘋賣傻地搶先大叫：**「我今始知此法戒經所載，半月半月說戒經來。」**"
   u"——我今天才知道戒經裡有這一条！這本戒半個月宣讀一次，我從前怎麼從沒聽過！")
do(u"丙8 先忍今不忍", 579, u"**「我先忍故不說，今不忍故說！」**",
   u"**「我先忍便不說，今不忍故說。」**")
do(u"丙9 等量作衣之呵", 669, u"**「汝愚癡人！何以無知乃與如來等量作衣？此愚癡人內懷弊惡，企圖竊奪如來之威相！」**",
   u"**「汝等云何與如來等量作衣，或過量作？」**——律中的呵責只有這一句，"
   u"但其所指極重：他把如來的威相也當成了可以裁量的規格。")

# ── 丁・款①之降式樣（二十九處，義不動，只去其『逐字』之外衣） ───────
DEM = [(12, u"微神經感測網"), (71, u"真開悟都不准說，何況說假話！"),
       (138, u"空間規避連續演進史"), (190, u"餐桌公義"), (204, u"我曹賈客每日操持買賣、流血流汗，尚且吃不起這種美食，何況汝等出家人？"),
       (233, u"改變物理交互形式"), (269, u"物料工程"), (446, u"軍事中立墮落三部曲"),
       (468, u"若實知者，王法應死！"), (512, u"毒蛇之喻"), (540, u"對抗司法矯正的三種心理防禦形態"),
       (533, u"諸大德！何必每半個月反覆唸這些雞毛蒜皮的碎屑小戒？念得大家心裡又煩惱、又慚愧、又懷疑自己犯戒，除了製造心理焦慮，有何用處？真要誦，誦四條根本大戒就夠了！"),
       (559, u"我當初授權的是那件事，不是這件事！那場表決不算數！"),
       (577, u"你們當初審理不周、觀察不清、判決不善！這樁案子不算數，必須重審！"),
       (584, u"審判必須有終點"), (595, u"照你們這樣問，你們已經犯了第四波羅夷大妄語，你們根本已經不是比丘了！"),
       (602, u"微型權力霸凌"), (652, u"極簡主義毫米級防線"), (690, u"反流氓政治憲政體系"),
       (727, u"四提舍尼法"), (728, u"百眾學法"), (729, u"七滅諍法")]
for idx, s in DEM:
    do(u"丁・降式樣 L%d" % idx, idx, u"**「%s」**" % s, u"「%s」" % s)
for idx, old, new in [
        (17, u"**「私人身心修養與日常微環境防禦」**", u"『私人身心修養與日常微環境防禦』"),
        (165, u"**「共期（事先約定）」**", u"**共期**（事先約定）"),
        (209, u"**「公地悲劇（Tragedy of the Commons）」**", u"『公地悲劇（Tragedy of the Commons）』"),
        (271, u"**「先到權（先住者優先）」**", u"**先到權**（先住者優先）"),
        (514, u"**「惡見不捨滅擯（永久開除）」**", u"**惡見不捨，滅擯**（永久開除）")]:
    do(u"丁・式樣歸位 L%d" % idx, idx, old, new)
# 「准」為簡形之用字，改從書中通例「不許」
do(u"丁・用字", 71, u"「真開悟都不准說，何況說假話！」", u"「真開悟都不許說，何況說假話！」")

# ── 戊・四段圍欄之重鑄（稿者俱越界：90／85／102／86 格） ─────────────
FENCE = {}
FENCE[25] = [
    u"【九十單提法（前半部：第1～45條）之五大板塊】",
    u"│",
    u"├─ 第一板塊·言語之門（防第四重大妄語）",
    u"│    1 故妄語  2 毀呰  3 兩舌  7 說麁罪  8 說上人法",
    u"│    12 答非所問  13 屏處譏嫌",
    u"├─ 第二板塊·空間與兩性幾何（防第一重婬戒）",
    u"│    4 同室宿  9 說法過限  43 強坐  44 屏處坐  45 露天獨坐",
    u"│    5、6 共宿共誦  27、28 期尼同道／同船  30 與婦女期道行",
    u"├─ 第三板塊·飲食大防線（防第二重盜戒與特權）",
    u"│    31 一住處食  32 展轉食  33 別眾食  34 過受餅麨",
    u"│    35 足食  36 慇懃勸食  37 非時食  38 殘宿食",
    u"│    39 不受食  40 乞美食  41 外道自手食  42 小食至餘家",
    u"├─ 第四板塊·微觀慈悲（防第三重殺戒與生態）",
    u"│    10 自手掘地  11 壞鬼神村  19 知水有蟲  20 覆苫",
    u"└─ 第五板塊·共有秩序與二部僧（防霸凌與越權）",
    u"     14、15 敷僧臥具  16、17 強中間敷與驅出  18 重閣脫腳床",
    u"     21～23 教授比丘尼  24、25、26、29 與尼往來",
]
FENCE[305] = [
    u"【佛陀的微環境四重構工程】",
    u"│",
    u"├─ 空間重構·去私密化",
    u"│    封死暗室、門後、露天對坐，移除一切視覺死角",
    u"├─ 時間重構·去散亂化",
    u"│    日中之前進食，黃昏收攏活動，清空深夜之社交",
    u"├─ 口腹重構·去特權化",
    u"│    摧毀私密飯局與連環赴宴，行餐桌透明之公義",
    u"└─ 慈悲重構·器具化與儀軌化",
    u"     漉水囊與覆苫離場令，令正念化為神經反射",
]
FENCE[369] = [
    u"【九十單提法（後半部：第46～90條）之五大重鎮】",
    u"│",
    u"├─ 第一重鎮·暴力與放逸（防第三重殺戒、防失念）",
    u"│    78 瞋恚打  79 手摶  53 擊攊致死  52 水中戲",
    u"│    55 恐怖他  58 藏人衣缽",
    u"├─ 第二重鎮·權力與成癮（防王法制裁、防破中立）",
    u"│    48 觀軍陣  49 軍中二宿  50 觀戰中箭",
    u"│    81 入王宮  82 捉寶  83 非時入村博戲  67 知賊伴同行",
    u"│    51 飲酒（成癮之總源頭）",
    u"├─ 第三重鎮·思想防毒（防大妄語、防意識叛變）",
    u"│    68 惡見不捨  69 供給惡見者  70 誘畜被擯二沙彌",
    u"│    71 不學此戒  72 輕呵戒律  73 詐稱始知",
    u"├─ 第四重鎮·司法防流氓（防破僧殘、防翻案）",
    u"│    64 覆藏他麁罪  66 滅後更發  74 事後謗僧  75 未竟起去",
    u"│    76 與欲已悔  77 聽諍向彼說  80 無根僧殘謗",
    u"└─ 第五重鎮·准入、器物與神聖終局",
    u"     46 誑同行  47 受供期限  56、57 擯出／燃火  59 借而不還",
    u"     60～62 二食家／斷畜命／滅擯  63 故疑惱他  65 授未滿二十",
    u"     84～89 高床、兜羅綿、骨牙針、尼師壇、覆瘡、雨浴衣",
    u"     90 與如來等量作衣（壓軸封頂）",
]
FENCE[692] = [
    u"【佛陀的司法程序正義防禦矩陣】",
    u"│",
    u"├─ 防範少數派罷會綁架（第75條·未竟起去戒）",
    u"│    嚴禁以缺席令法定人數不足，剝奪流氓之破壞權",
    u"├─ 確立判決之終局性（第66條·諍事滅後更發戒）",
    u"│    一事不再理，禁止無休止之翻案內耗",
    u"├─ 防範誣告與惡意拖延（第80條·無根僧殘謗；第71條·不學此戒）",
    u"│    誣告者承擔反噬，不得以程序異議無限期癱瘓",
    u"└─ 代理責任之法定化（第76條·與欲已後悔戒）",
    u"     委託既成即有拘束力，杜絕事後之輸打贏要",
]


def cw(s):
    return sum(2 if ord(c) > 0x2E80 else 1 for c in s)


def set_fence(a, block):
    assert D[a - 1] == u"```", u"圍欄之界不正：稿L%d" % a
    z = a
    while D[z] != u"```":
        z += 1
    old = z - a
    mx = max(cw(x) for x in block)
    assert mx <= 72, u"稿L%d 之新圖最寬 %d 格越界" % (a, mx)
    for x in block:
        assert x.strip(), u"稿L%d 之新圖含純空行" % a
    D[a:z] = block                # a 為首拍之 0 起索引，z 為閉圍欄之 0 起索引（不含）
    print(u"  戊・圍欄 稿L%d：%d 行 ← %d 行｜最寬 %d 格" % (a, len(block), old, mx))


for a in sorted(FENCE, reverse=True):
    set_fence(a, FENCE[a])

# ── 己・新稿自身之形制覆核 ───────────────────────────────────────────
H1 = [l for l in D if re.match(u"^# ", l)]
assert len(H1) == 2 and H1[0].startswith(u"# 第八章") and H1[1].startswith(u"# 第九章"), H1
buf, fences = None, []
for l in D:
    if l.startswith(u"```"):
        if buf is None:
            buf = []
        else:
            fences.append(buf)
            buf = None
        continue
    if buf is not None:
        buf.append(l)
assert buf is None and len(fences) == 4, u"圍欄 %d 段或未閉" % len(fences)
for f in fences:
    for x in f:
        if cw(x) > 72:
            print(u"    越界 %d 格｜%r" % (cw(x), x[:70]))
    assert max(cw(x) for x in f) <= 72, u"覆核時越界：%s" % f[0][:24]
LAY8 = [l for l in D if l.startswith(u"### 【第")]
assert len(LAY8) == 10, u"中間層 %d ≠ 10（板塊 5＋重鎮 5）" % len(LAY8)
NUM8 = [re.match(u"^#### 案例([〇零一二三四五六七八九十]+)：", l).group(1)
        for l in D if l.startswith(u"#### 案例")]
assert NUM8 == [u"一", u"二", u"三", u"四", u"五", u"六", u"七", u"八", u"九", u"十",
                u"十一", u"十二"] + [u"一", u"二", u"三", u"四", u"五", u"六", u"七",
                u"八", u"九", u"十", u"十一", u"十二", u"十三"], NUM8
print(u"  己・形制：H1 2｜節 %d｜中間層 10｜案例 12＋13=25 ✓" % (
    sum(1 for l in D if re.match(u"^### [一二三四五]、", l))))

COV = set()
for l in D:
    if not l.startswith(u"#### 案例"):
        continue
    t = l[l.find(u"案例"):]
    for grp in re.findall(u"（第([0-9、～]+?)條）", t):
        for part in grp.split(u"、"):
            if u"～" in part:
                x, y = [int(v) for v in part.split(u"～")]
                COV.update(range(x, y + 1))
            elif part.isdigit():
                COV.add(int(part))
gap = sorted(set(range(1, 91)) - COV)
print(u"  己・案例標題所舉條號覆蓋 %d／90｜缺 %s" % (len(COV), gap or u"無"))
assert not gap, u"九十單提有條未落案例：%s" % gap

claim, unsup = 0, []
for i, l in enumerate(D):
    for m in PAT1.finditer(l):
        s = (m.group(1) or m.group(2)).replace(u"**", u"")
        claim += 1
        for frag in re.split(u"……|…", s):
            nb = _tk.norm(PUNC.sub(u"", frag))
            if len(nb) >= 4 and not has(nb):
                unsup.append(u"稿L%d｜%s" % (i + 1, frag[:40]))
assert not unsup, u"款① 仍有無據之逐字宣稱：\n    " + u"\n    ".join(unsup)
print(u"  己・款① 自證：%d 段俱連寫可查 ✓" % claim)
nl = [i + 1 for i, l in enumerate(D) if u"\n" in l or u"\r" in l]
assert not nl, u"有刀在單行內嵌換行符：%s" % nl
sp = [i + 1 for i, l in enumerate(D) if re.search(u"第[ \t]+[0-9]", l) or re.search(u"[0-9、～][ \t]+條", l)]
assert not sp, u"條號空格未歸例：%s" % sp[:8]

# ── 庚・入冊（今檔第八章 L2213–L2894・第九章 L2895–L3771） ───────────
braw = io.open(BOOK, "rb").read()
bsha = hashlib.sha256(braw).hexdigest()
BL = braw.decode("utf-8").split(u"\r\n")
i8 = next(k for k, l in enumerate(BL) if l == u"# 第八章 九十單提（上）")
i9 = next(k for k, l in enumerate(BL) if l == u"# 第九章 九十單提（下）")
i10 = next(k for k, l in enumerate(BL) if l.startswith(u"# 第十章"))
assert BL[i9 - 1] == u"" and BL[i9 - 2] == u"---", u"第八章末之界不正"
assert BL[i10 - 1] == u"" and BL[i10 - 2] == u"---", u"第九章末之界不正"
F0, C0, N0b = (sum(1 for l in BL if l.startswith(u"```")) // 2,
               sum(1 for l in BL if l.startswith(u"#### 案例")), len(BL))
k9 = next(i for i, l in enumerate(D) if l == u"# 第九章 九十單提（下）")
b8 = D[2:k9] + [u"", u"---"]
b9 = D[k9:] + [u"", u"---"]
assert b8[0] == u"# 第八章 九十單提（上）" and b9[0] == u"# 第九章 九十單提（下）"
assert b8[-1] == u"---" and b9[-1] == u"---"
BL[i9 - 2:i10 - 2] = b9          # 先高索引（含舊之 ---）
BL[i8 - 2:i9 - 2] = b8
F1 = sum(1 for l in BL if l.startswith(u"```")) // 2
C1 = sum(1 for l in BL if l.startswith(u"#### 案例"))
print(u"入冊：全書 %d→%d 行｜第八章 %d 行・第九章 %d 行｜圍欄 %d→%d｜案例 %d→%d" % (
    N0b, len(BL), len(b8), len(b9), F0, F1, C0, C1))
assert F1 == F0 + 2, u"圍欄段數之變非 +2（舊各 1 段、新各 2 段）"
assert C0 == 163 and C1 == 134, u"全書案例之變非 163→134（今 %d→%d）" % (C0, C1)
out = u"\r\n".join(BL)
assert out.count(u"\r") == out.count(u"\n") == len(BL) - 1, u"CRLF 變形"
print(u"正本 sha（換入前）%s" % bsha[:12])
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
assert not os.path.exists(BAK), u"備份已存在：%s（先處置再刀）" % BAK
shutil.copy2(BOOK, BAK)
io.open(BOOK, "w", encoding="utf-8", newline=u"").write(out)
chk = io.open(BOOK, "rb").read()
CL = chk.decode("utf-8").split(u"\r\n")
assert sum(1 for l in CL if l.startswith(u"```")) // 2 == F1, u"覆讀圍欄不合"
assert sum(1 for l in CL if l.startswith(u"#### 案例")) == C1, u"覆讀案例不合"
j8 = next(k for k, l in enumerate(CL) if l == u"# 第八章 九十單提（上）")
j9 = next(k for k, l in enumerate(CL) if l == u"# 第九章 九十單提（下）")
j10 = next(k for k, l in enumerate(CL) if l.startswith(u"# 第十章"))
assert CL[j8:j8 + len(b8)] == b8, u"覆讀之第八章與所鑄者不一字不差"
assert CL[j9:j9 + len(b9)] == b9, u"覆讀之第九章與所鑄者不一字不差"
assert CL[j10 - 2] == u"---" and CL[j10 - 1] == u"", u"覆讀之章界不正"
print(u"正本 sha（換入後）%s｜%d B" % (hashlib.sha256(chk).hexdigest()[:12], len(chk)))
print(u"覆讀：第八 %d 行・第九 %d 行一字不差 ✓｜備份 %s" % (
    len(b8), len(b9), os.path.basename(BAK)))

