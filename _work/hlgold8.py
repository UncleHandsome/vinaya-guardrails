# -*- coding: utf-8 -*-
import io, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import hulan_path as HP
GO = "--go" in sys.argv

# 七處新增：每處取『段末』（下一標題或分隔線之前）插入一行，一律標明本書之解／推，不掛逐字式樣
SITES = [
 (u"#### 案例三十：向白衣說",
  u"* **界須再划一刀（本書之解）：**『不對外直播』所護者，是私德過失、威儀失檢與僧團內部的人際磨擦；"
  u"一旦所涉乃世俗法律上的重大公訴罪——性侵、傷害致死、巨額侵占——被侵害的已是在世的人身與財產法益，"
  u"出世防線在此讓位。依法向世俗機關舉報，不犯此戒：僧團於私德不公審，以全其慚愧；於重罪不包庇，以盡人間之義。"),
 (u"#### 3. 自言治",
  u"* **界（本書之解）：**僧團無警政之權——不能搜索、不能監聽、不能強制到案，故界內問事必守不自言不應治，"
  u"以防酷吏與獵巫。若當事人抵賴而所涉乃重大公訴罪，如法的處置不是私設刑堂逼供，而是先行物理隔離、"
  u"依法移送世俗司法；待判決確定，僧團據此客觀事實作除名之處分。『不自言不應治』所防的是權力濫用，不是拿去替罪行遮蓋。"),
 (u"### 四、 殘之治", None),      # 第六章：以節界定址，見下 SPECIFIC
 (u"#### 案例一：第五波羅夷·摩觸戒",
  u"* **調查的一條紅線（本書之程序倫理）：**律之判準在『樂與不樂』，本為辨染淨、護受犯者；然此判準一落入盤問之手，"
  u"便能反過來傷人。極端暴力之下，身體自有不由意志作主的反應；反覆詰問受害者當時可有快感、可有迎合，是第二次傷害。"
  u"故本書以為：客觀上既有暴力、脅迫或違背意願之事實，即應先判無犯，不待其自證清白；細目之問只問加害的一方，不問受害的一方。"
  u"律文沒有說過這句話，是律文劃下的界限教的。"),
 (u"#### 案例十：迦蘭陀竹園",
  u"* **這筆信託今天卡在哪裡（本書之解）：**律把僧物歸於四方僧，不記在創始人名下，也不記在任何執事名下。"
  u"今世最常見的破口，是道場為圖登記方便，把信眾捐建的房地寫在住持個人名下；住持一旦圓寂，其世俗親屬便可依法定繼承"
  u"（含強制份額）主張權利，十方布施遂淪為私產之爭。故常住資產須於生前以世俗法律有效之方式——法人登記或信託確權——"
  u"與個人私產徹底切割，不可僅憑一張遺囑或一句口頭交代。以法護僧物，不是不信人。"),
 (u"#### 6. 如草覆地",
  u"* **退堂之後（本書之行法）：**案已結、羯磨已成，審者之職即畢。散會之後，走廊與茶席上不復咀嚼案情、"
  u"不復品評他人過失——語業歸零；然後去做一件粗重的活，掃地、洗碗、搬柴，親手把自己從審判者的位子上請下來，"
  u"回到我亦隨時可能失足的人。護欄是擋自己的，不是拿量別人的；把法讀成一張驗傷單，便是學錯了方向。"),
 (u"#### 案例八：故斷畜生命戒",
  u"* **向下轉移的怒氣（本書之推）：**律在此只記不喜見烏，不記他此前受過何呵責；本書敢補的只有一層現代心理學——"
  u"一個在體制內受了處分又不肯正視自己過失的人，常把胸中積壓的羞辱轉嫁給絕無反抗之力的弱小者，於是削竹為弓，殺一庭啼鴉。"
  u"慈悲不是抽象的口號：慈悲是絕不把自身的受挫，轉嫁到比你更弱小的存在身上。"),
]
# 第四目（舉罪五德鏡盾）另依正文句定址，插於『舉發要有根據』條之後
SIT2_ANCHOR = u"**舉他比丘應以三事：若見、若聞、若疑**"
SIT2_TEXT = (u"@@N@@. **一面鏡子，不是一面盾牌（本書之解）：**舉罪須有據，故律只認見、聞、疑三項；"
             u"而勸諫者所具之德（知時、如實、利益、柔軟、慈心）是開口前的自省之鏡，不是被舉者在公堂上的脫罪之盾。"
             u"所舉屬實，公堂便須先審實體，不得因對方態度不好、挑的時辰不對而擱置調查——把是非之爭改判成態度之爭，"
             u"是濫用程序最體面的一件外衣。")
CH6_TEXT = (u"**按：微型道場之困與出罪法權之移（本書之解）。**依律，出罪須二十人僧；而今之小道場多一師二三眾，"
            u"犯者縱已誠心服法，常苦於僧數不足。律於人數本有四級之判（四人、五人、十人、二十人，邊地別開減省），"
            u"其意一貫：法權隨人而存，不隨地理而絕。故本書以為，僧數不具之道場宜作兩段行法——服滿六夜摩那埵後，"
            u"由常住如實出具行治紀錄（所犯、所治、日數、有無更犯），移轉管轄於鄰近大叢林或區域聯合僧團，由其足數出罪。"
            u"此乃本書據律意所作的現代設計，非律之明文。")

raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
NL = u"\r\n" if u"\r\n" in raw else u"\n"
lines = raw.split(NL)
n0, cr0 = len(lines), raw.count(u"\r\n")
HEAD = re.compile(u"^#{1,4} |^---\\s*$")


def boundary(start):
    b = start + 1
    while b < len(lines) and not HEAD.match(lines[b]):
        b += 1
    while b > start + 1 and not lines[b - 1].strip():      # 退回最後一行內文之後
        b -= 1
    return b


plan = []


def _num_after(seg):
    nums = [int(m.group(1)) for m in re.finditer(r"(?m)^\s*(\d+)\. ", NL.join(seg))]
    return max(nums) if nums else 1


sys.path.insert(0, os.path.join(ROOT, "_work"))
import _simpdict                                        # 新文先過簡形閘（書側之制，工具亦須守）
for tag, txt in [(h, t) for h, t in SITES if t] + [(u"SIT2", SIT2_TEXT), (u"CH6", CH6_TEXT)]:
    bad = sorted({c for c in txt if c in _simpdict.MAP})
    if bad:
        print(u"  ✗ 新文夾簡形：%s → %s" % (tag[:16], " ".join(u"%s U+%04X" % (c, ord(c)) for c in bad)))
        sys.exit(1)
errs = []
for head, text in SITES:
    if text is None:
        continue
    idx = [i for i, l in enumerate(lines) if l.startswith(head)]
    if len(idx) != 1:
        errs.append(u"錨非唯一：%s（%d）" % (head[:22], len(idx)))
        continue
    b = boundary(idx[0])
    if b >= len(lines) or not lines[b - 1].strip():
        errs.append(u"段末之前非內文：%s" % head[:22])
        continue
    plan.append((b, text, head[:22]))

i6 = [i for i, l in enumerate(lines) if l.startswith(u"# 第六章 十三僧殘")]
h6 = [i for i, l in enumerate(lines) if l.startswith(u"### 四、 殘之治") and i > (i6[0] if i6 else -1)]
if len(h6) == 1:
    b = boundary(h6[0])
    if lines[b - 1].strip():
        plan.append((b, CH6_TEXT, u"第六章第四節"))
    else:
        errs.append(u"第六章段末不合式")
else:
    errs.append(u"第六章第四節錨 %d 處" % len(h6))

i2 = [i for i, l in enumerate(lines) if SIT2_ANCHOR in l]
if len(i2) == 1:
    nxt = i2[0] + 1
    while nxt < len(lines) and lines[nxt].strip():
        nxt += 1
    plan.append((nxt, SIT2_TEXT.replace(u"@@N@@", str(_num_after(lines[i2[0]:nxt]))), u"舉他三事"))
else:
    errs.append(u"舉他三事錨 %d 處" % len(i2))

plan.sort(key=lambda x: -x[0])
print(u"插入點 %d 處｜預增行 %d" % (len(plan), 2 * len(plan)))
for b, t, tag in plan:
    print(u"  L%-5d ← %s｜%s…" % (b + 1, tag, t[:26]))
if errs:
    for e in errs:
        print(u"  ✗ " + e)
    sys.exit(1)
if not GO:
    sys.exit(u"試跑畢；加 --go 方寫")

new = list(lines)
trims = 0
for b, t, tag in plan:
    new[b:b] = [u"", t]
    while b + 3 < len(new) and not new[b + 2].strip() and not new[b + 3].strip():
        del new[b + 3]                                    # 不許攢出兩個空行
        trims += 1
out = NL.join(new)
io.open(HP.SRC, "w", encoding="utf-8", newline="").write(out)

back = io.open(HP.SRC, encoding="utf-8", newline="").read()
bl = back.split(NL)
errs = []
want = 2 * len(plan) - trims
if len(bl) != n0 + want:
    errs.append(u"行數增量不合：%d→%d（期 +%d）" % (n0, len(bl), want))
if back.count(u"\r\n") != cr0 + want:
    errs.append(u"CR 未隨行數：%d" % back.count(u"\r\n"))
for b, t, tag in plan:
    if back.count(t) != 1:
        errs.append(u"未立：%s" % tag)
if any(re.search(u"[一-鿿][,;?!]|・|[@]", t) for _b, t, _g in plan):
    errs.append(u"新文雜質（半形標點或日式中黑）")
print(u"== 回讀：%s ==" % (u"全中（+%d 行）" % (2 * len(plan))) if not errs else u"有失")
for e in errs:
    print(u"  ✗ " + e)
sys.exit(1 if errs else 0)
