# -*- coding: utf-8 -*-
"""新冊終審之尺・一律量產物本身（指南第四回「全書終審驗收規準清單」十指標）。

鐵則：尺不讀規則之自報，只讀冊身；並逐段回查兩本舊冊，量『文在不在』而非『碼在不在』。
凡例一段自述公約之形（『不立某某』者），計殘留時除之，以免自量成自縛。
用法：python -X utf8 _book/check.py [--book=路徑]
"""
import io, os, re, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import parse as P
import assemble as A

BOOK = os.path.join(ROOT, u"佛陀的護欄_四分律行為心理學與現代僧伽治理.md")
for a in sys.argv[1:]:
    if a.startswith("--book="):
        BOOK = a.split("=", 1)[1]

book = io.open(BOOK, encoding="utf-8").read()
BL = book.split("\n")
FAIL, NOTE = [], []
HEADS = [(i, len(m.group(1)), m.group(2)) for i, l in enumerate(BL, 1)
         for m in [re.match(r"^(#{1,6}) (.*)$", l)] if m]


def bad(m):
    FAIL.append(m)


def note(m):
    NOTE.append(m)


def norm(s):
    return re.sub(u"[^\\u3400-\\u9fff]", u"", s or u"")


H1 = [(i, t) for i, l2, t in HEADS if l2 == 1]
H1P = [i for i, _ in H1] + [len(BL) + 1]
CHAP = {}
for k, (i, t) in enumerate(H1):
    m = re.match(u"(第[一二三四五六七八九十]+章)　(.*)$", t)
    if m:
        CHAP[m.group(1)] = (i, H1P[k + 1] - 1, m.group(2))
fan_i = next((n for n, l in enumerate(BL, 1) if l.startswith(u"## 【卷首・") and u"凡例】" in l), 0)
fan_j = next((k for k, l in enumerate(BL[fan_i:], fan_i + 1) if l.startswith(u"## ")), len(BL)) if fan_i else 0
CORE = u"\n".join(BL[:fan_i - 1] + BL[fan_j - 1:]) if fan_i else book
BN = norm(book)
BGRAM = set(BN[i:i + 6] for i in range(0, max(0, len(BN) - 6)))


def cnt(pat, text=None):
    return len(re.findall(pat, text if text is not None else CORE))


# ── 一・結構 ────────────────────────────────────────────────────────────────
parts = [l for l in BL if re.match(r"^# 【第[一二三四五六七八九十]+部：", l)]
apxs = [l for l in BL if re.match(r"^## 附錄[一二三四五]　", l)]
if len(parts) != 7:
    bad(u"部數 %d ≠ 7" % len(parts))
if len(CHAP) != 28:
    bad(u"章數 %d ≠ 28" % len(CHAP))
if len(apxs) != 5:
    bad(u"附錄數 %d ≠ 5" % len(apxs))
if not [l for l in BL if l.startswith(u"# 終卷")]:
    bad(u"終卷佚")
for f in [u"【題詞與獻辭】", u"【自序】", u"【導讀指南】", u"凡例】", u"【全書路標】",
          u"【開卷總提撕】", u"總目錄】", u"【三篇立言之總意】", u"【本書之斷】", u"引文承諾六律"]:
    if not any(l.startswith(u"#") and f in l for l in BL):
        bad(u"卷首・斷語件佚：%s" % f)
short = []
for t, (a, b, sub) in CHAP.items():
    z = len(norm(u"\n".join(BL[a:b])))
    if z < 1200:
        short.append(u"%s（%d）" % (t, z))
if short:
    bad(u"章身過短：%s" % u"、".join(short))

# ── 二・指標 1・2：人造數字與後台代碼零殘留 ───────────────────────────────
BANNED = [
    (u"一百基準|100 則基準|百則基準|基準判例|不計入百則", u"基準定額"),
    (u"133 處|133 綁|共 133", u"133 平帳"),
    (u"107 處|落點次數|與落點", u"落點平帳"),
    (u"三十格|30 格|6x5|六乘五", u"三十格矩陣"),
    (u"道岔", u"通道代號"),
    (u"問\\[|\\[1\\] 至 \\[16\\]", u"問卷代碼"),
    (u"〔(?:遮|開|僧|補遺|尼-波)\\d+〕", u"案碼"),
    (u"〔素材|子案編號|母案碼", u"素材卡標"),
    (u"〔◈", u"符號帽子"),
    (u"定位｜根本心|\\*\\*定位", u"案頭 Frontmatter"),
    (u"syncchk|bqa|負測|Python|python|腳本|回歸測試|驗證器", u"程式術語"),
    (u"聲譜分析|雜湊值|AI 鑑定|人工智慧鑑定", u"科幻取證"),
    (u"檢索總表|全覽表|款級索引|綁定台帳|台帳|定位行", u"平帳之名"),
    (u"附錄C|附錄K|附錄L|附錄M|I-3|全書附錄共十二篇", u"應移出之附錄"),
    (u"〔待寫|〔待校|〔指針待判|〔指針已重算|〔未裁|〔缺：|〔此節移入|〔評議", u"未竟之帳"),
    (u"〔合編說明〕|〔編者指針〕|（素材卡）", u"合編脚手架"),
    (u"本地語料|檢索得|詞頻", u"語料統計"),
    (u"！！！|看哪|何其可怕|無恥之尤", u"咆哮體"),
    (u"〔校勘|〔待校", u"校勘痕跡"),
    (u"第三十八版|Ver ?[0-9]+|合規率|校驗程序|[0-9]+/[0-9]+ 全部|起心動念心智分析框架", u"舊版印記"),
]
for pat, name in BANNED:
    n = cnt(pat)
    if n:
        lines = [i for i, l in enumerate(BL, 1)
                 if re.search(pat, l) and not (fan_i and fan_i <= i < fan_j)][:5]
        bad(u"殘留「%s」%d 處（行 %s）" % (name, n, u",".join(map(str, lines))))
for pat, name in [(u"括號之四制|四制各司", u"四制宣告"), (u"全形［］唯得見於", u"圍欄括號約")]:
    if cnt(pat):
        bad(u"殘留「%s」" % name)
note(u"考證夾注〔案：…〕%d 處（出版之夾注，非帳目）" % cnt(u"〔案：", book))

# ── 三・指標 4：人稱機位 ────────────────────────────────────────────────────
SEC = re.compile(u"#### (心相照鏡|人間智慧與行持|法相剖析|事相經過|佛陀處斷)\n\n(.{0,1200}?)(?=\n#### |\n### |\Z)", re.S)
secs = collections.defaultdict(list)
for m in SEC.finditer(book):
    secs[m.group(1)].append(m.group(2))
no_you = [s for s in secs[u"心相照鏡"] if u"你" not in s]
no_we = [s for s in secs[u"人間智慧與行持"] if u"我們" not in s]
if len(secs[u"人間智慧與行持"]) < 60:
    bad(u"人間智慧與行持僅 %d 段" % len(secs[u"人間智慧與行持"]))
if no_you:
    bad(u"心相照鏡無第二人稱 %d/%d 段：例「%s」" % (len(no_you), len(secs[u"心相照鏡"]), norm(no_you[0])[:22]))
if no_we:
    bad(u"人間智慧無第一人稱複數 %d/%d 段：例「%s」" % (len(no_we), len(secs[u"人間智慧與行持"]), norm(no_we[0])[:22]))
note(u"人稱機位：心相 %d・智慧 %d・剖析 %d・事相 %d・處斷 %d 段" % (
    len(secs[u"心相照鏡"]), len(secs[u"人間智慧與行持"]), len(secs[u"法相剖析"]),
    len(secs[u"事相經過"]), len(secs[u"佛陀處斷"])))

# ── 四・指標 5・7・8・9：四項裁定落地 ──────────────────────────────────────
MUST = [
    (u"挫折慢心療法|Ego-Crushing|認知行為療法（CBT）", u"指標五・舊說未拔", 0),
    (u"政治生存保護費|政治保護費", u"指標五・歷史定性", 1),
    (u"逆向審計", u"指標五・女眾制衡", 1),
    (u"公訴法權讓位", u"指標七・法權讓位", 1),
    (u"預防性物理動線隔離", u"指標七・物理隔離", 1),
    (u"協助國法執行之除名宣告", u"指標七・定讞除名", 1),
    (u"特留分", u"指標八・寺產信託", 1),
    (u"志願服務協議", u"指標九・志工合規", 1),
    (u"正規勞動契約", u"指標九・核心勞力正規", 1),
    (u"但意無犯", u"模組三・三・公堂自制", 1),
    (u"法界有功德", u"模組三・四・後門焊死", 1),
    (u"繳械", u"模組四・二・終局之印", 1),
    (u"微型道場與邊地極限救濟", u"第三回・新增補強", 1),
    (u"去科幻化之取證底線", u"第四回・去科幻", 1),
    (u"善護三業", u"模組一・略戒為體", 1),
]
for pat, name, need in MUST:
    n = cnt(pat, book)
    if name.startswith(u"指標五・舊說"):
        if n:
            bad(u"「%s」仍見 %d 處" % (name, n))
        continue
    if n < need:
        bad(u"「%s」只 %d 處，須 ≥%d" % (name, n, need))

RIT = [u"吃茶", u"出坡洗心", u"樹下吹風", u"松風吹拂", u"林下無事，天下太平"]
hits = []
for t, (a, b, sub) in CHAP.items():
    if t == u"第二十八章":
        continue
    tail = u"\n".join(BL[max(a, b - 25):b])
    for r in RIT:
        if r in tail:
            hits.append(u"%s・%s" % (t, r))
if hits:
    bad(u"章末公式化抒情：%s" % u"、".join(hits))

# ── 五・案例完備 ────────────────────────────────────────────────────────────
CASE_RE = re.compile(u"^### 案例([一二三四五六七八九十]+)：", re.M)
per = collections.OrderedDict()
for t, (a, b, sub) in CHAP.items():
    per[t] = [m.group(1) for m in CASE_RE.finditer(u"\n".join(BL[a:b]))]
total_case = sum(len(v) for v in per.values())
want = sum(len(A.PLAN.get(t, [])) for t in per)
fused = sum(1 for t, items in A.PLAN.items() for _, code, hcase in items if code and hcase)
if total_case != want:
    bad(u"案例總數 %d ≠ 清冊 %d（其中缝合 %d 案）" % (total_case, want, fused))
placed_fw = set()
for t, items in A.PLAN.items():
    for _, code, hcase in items:
        if code:
            placed_fw.add(code)
for key in A.CASE_MAP:
    placed_fw.discard(None)
if len(placed_fw) != 115:
    bad(u"框架卡入冊 %d ≠ 115" % len(placed_fw))
if len(A.CASE_MAP) != 164:
    bad(u"護欄案入冊 %d ≠ 164" % len(A.CASE_MAP))
note(u"清冊：案例 %d 案（框架 115・護欄 164・同案合一 %d）" % (total_case, fused))
for t, ns in per.items():
    if ns and P.cnum(ns[0]) != 1:
        bad(u"%s 案例未自一起（首為%s）" % (t, ns[0]))
    if len(ns) != len(set(ns)):
        bad(u"%s 案例序重複" % t)
    for k, n in enumerate(ns, 1):
        if P.cnum(n) != k:
            bad(u"%s 案例序斷於第 %d 位（%s）" % (t, k, n))
            break
note(u"案例：%d 案・分 %d 章（無案例之章 %d）" % (
    total_case, len(per), sum(1 for v in per.values() if not v)))

# ── 六・指針活鏈 ────────────────────────────────────────────────────────────
dead = []
for m in re.finditer(u"第([一二三四五六七八九十]+)章(?:案例([一二三四五六七八九十]+)|『([^』]{1,20})』案)?", book):
    key = u"第%s章" % m.group(1)
    if key not in CHAP:
        dead.append(m.group(0))
    elif m.group(2) and P.cnum(m.group(2)) > len(per.get(key, [])):
        dead.append(u"%s（該章僅 %d 案）" % (m.group(0), len(per.get(key, []))))
if dead:
    bad(u"死鏈 %d 條：%s" % (len(dead), u"｜".join(sorted(set(dead))[:6])))
else:
    note(u"指針：章級與案級全活（章指針 %d 條）" % len(list(re.finditer(u"第[一二三四五六七八九十]+章", book))))

# ── 七・素材涵蓋率（逐段回查兩本舊冊）──────────────────────────────────────
EXC = [u"三十格", u"林下留白", u"空白格", u"留白觀", u"章末收卷", u"全章收卷", u"公堂燈熄",
       u"吃茶", u"松風", u"樹下吹風", u"章末引橋", u"把法袍留在門外", u"核心引橋",
       u"引橋：手握總帳", u"走出解剖室",
       u"檢索", u"速查", u"綁定台帳", u"台帳", u"全覽表", u"複統攝", u"終極壓縮", u"心智生態系統全貌",
       u"附錄收編", u"開卷標準目錄", u"全書詳細目錄", u"卷首導讀", u"挫折慢心療法", u"核心命題錨定",
       u"三層標記", u"人機協同", u"自然人心證自律宣告書", u"道岔", u"目錄",
       u"跨章精準導流", u"標題層級體例", u"附錄之界", u"編序"]


def heads(lines):
    return [(i, len(m.group(1)), m.group(2)) for i, l in enumerate(lines, 1)
            for m in [re.match(r"^(#{1,6}) (.*)$", l)] if m]


PARA_SKIP = [u"定位根本心", u"跨章精準導流", u"標題層級體例", u"三層標記系統", u"法架警示",
             u"本書章直轄節"]
# 同案合一者，框架卡之「事相經過」約述依策不兩出——先照冊登其形，不計為佚文
PAIRED = set(code for t, items in A.PLAN.items() for _, code, hc in items if code and hc)
DECLARED = set()
for _code in PAIRED:
    _f = A.CARDS.get(_code, {}).get("fields", {})
    for _p in re.split(u"\n\n+", _f.get(u"事相經過", u"")):
        n = norm(_p)
        if len(n) > 24:
            DECLARED.add(n)
note(u"同案不兩抄：框架卡約述之已宣告段 %d（%d 案与其事相合流）" % (len(DECLARED), len(PAIRED)))


def covered(para):
    n = norm(para)
    if len(n) < 24 or any(x in n[:30] for x in PARA_SKIP):
        return True
    q = n.replace(u"事相經過", u"", 1)
    if len(q) > 24 and any(q in blob for blob in DECLARED):
        return True
    for i in range(0, max(1, len(n) - 12), 6):
        if n[i:i + 12] in BN:
            return True
    g = set(n[i:i + 6] for i in range(0, max(0, len(n) - 6)))
    return bool(g) and len(g & BGRAM) / float(len(g)) > 0.55


def lost_in(lines, a, b):
    out = []
    for p in re.split(u"\n\n+", u"\n".join(lines[a - 1:b])):
        q = p.strip()
        if len(norm(q)) > 40 and u"定位｜根本心" not in q and not covered(q):
            out.append(q)
    return out


def census(lines, tag):
    """以『葉節』為單位，且祖先標題命中排除表者連帶不計（H2・卷首・附錄皆不漏量）。"""
    hs = heads(lines)
    starts = [i for i, l2, t in hs if 2 <= l2 <= 5]
    nxt = sorted(set([i for i, l2, t in hs if l2 <= 5] + [len(lines) + 1]))
    miss = collections.OrderedDict()
    for i in starts:
        anc = [t for j, l2, t in hs if j <= i]        # 自 H1 而下之歷代標題
        if any(any(x in t for x in EXC) for t in anc):
            continue
        e = next(j - 1 for j in nxt if j > i)
        lost = lost_in(lines, i, e)
        if lost:
            t = next(tt for j, l2, tt in hs if j == i)
            miss[u"%s・L%d・%s" % (tag, i, t[:24])] = (len(lost), sum(len(norm(p)) for p in lost), lost)
    return miss


fw, hl = P.load(ROOT)
miss = dict(list(census(fw.lines, u"框架").items()) + list(census(hl.lines, u"護欄").items()))
lost_n = sum(v[0] for v in miss.values())
lost_z = sum(v[1] for v in miss.values())
for k, v in sorted(miss.items(), key=lambda z: -z[1][1])[:12]:
    note(u"　佚 %5d 字・%2d 段｜%s　例：%s" % (v[1], v[0], k, norm(v[2][0])[:22]))
if lost_z > 6000:
    bad(u"素材未落地：%d 段／%d 漢字（門檻 6,000）" % (lost_n, lost_z))
else:
    note(u"素材涵蓋：未落地 %d 段／%d 漢字（門檻 6,000）" % (lost_n, lost_z))

# ── 八・圍欄與表 ────────────────────────────────────────────────────────────
if len(re.findall(u"^```", book, re.M)) % 2:
    bad(u"圍欄不齊")
badrows = [i for i, l in enumerate(BL, 1) if l.strip().startswith(u"|") and l.count(u"|") < 2]
if badrows:
    bad(u"殘行表格 %d 行（例 %s）" % (len(badrows), badrows[:3]))
if u"\x01" in book:
    bad(u"護符未收（\\x01 殘留）")

# ── 九・册題之尺：結構標題須與產器自報之清冊一字不差（防規則誤傷標題）────
MAN = os.path.join(HERE, u"册題清冊.tsv")
if not os.path.exists(MAN):
    bad(u"册題清冊佚（產器未出冊題，無從核標題）")
else:
    want = [l.rstrip() for l in io.open(MAN, encoding="utf-8").read().split("\n") if l.strip()]
    have = set(l.rstrip() for l in BL if l.startswith(u"# ") or l.startswith(u"## 附錄"))
    gone = [l for l in want if l not in have]
    extra = [l for l in sorted(have) if l not in want and (
        l.startswith(u"# 【") or l.startswith(u"# 第") or l.startswith(u"# 終卷")
        or l.startswith(u"# 佛陀") or re.match(u"^## 附錄[一二三四五]　", l))]
    if gone:
        bad(u"册題失實（產器宣有而今無，疑被規則改動）：%s" % u"｜".join(x[:34] for x in gone[:5]))
    if extra:
        bad(u"册外之題（冊身多出產器未宣之結構標題）：%s" % u"｜".join(x[:34] for x in extra[:5]))
    if not gone and not extra:
        note(u"册題：%d 條結構標題與產器清冊一字不差" % len(want))

# ── 十・出處閘門：自稱『律藏原文』者必冠卷段（凡例第三條之自證）──────────
YUAN = re.compile(u"#### 律藏原文\n\n(.{0,3000}?)(?=\n#### |\n### |\Z)", re.S)
yq = YUAN.findall(book)
yn = [s for s in yq if not re.search(u"卷[一二三四五六七八九十0-9]|卷 [0-9]|大正|No\\.142|《戒本》", s)]
if yn:
    bad(u"『律藏原文』無出處 %d/%d 欄：例「%s」" % (len(yn), len(yq), norm(yn[0])[:24]))
note(u"出處閘門：律藏原文 %d 欄俱冠卷段・戒文（依戒本次第）%d 欄" % (
    len(yq), len(re.findall(u"#### 戒文（戒本次第）", book))))

# ── 十一・引號之闭合（律文原樣登載者不計・新冊不得自造破口）──────────────
IA3 = next((i for i, l in enumerate(BL, 1) if l.startswith(u"## 附錄三")), 0)
IB3 = next((i for i in range(IA3 + 1, len(BL)) if BL[i - 1].startswith(u"## 附錄四")), len(BL))
NL = chr(10)
OFF3 = book.index(NL.join(BL[IA3:IB3])) if IA3 else -1
OFF4 = book.index(NL.join(BL[IB3 - 1:IB3])) if IB3 < len(BL) else len(book)


def walk(op, cl, nm, allow_zone=None):
    st, miss = [], []
    for i, c in enumerate(book):
        if c == op:
            st.append(i)
        elif c == cl:
            if st:
                st.pop()
            else:
                miss.append((u"多闭合", i))
    miss += [(u"未闭合", x) for x in st]
    for kind, i in miss:
        ln = book[:i].count(NL) + 1
        txt = u"%s%s L%d：%s" % (nm, kind, ln, book[max(0, i - 40):i + 26].replace(NL, " "))
        if allow_zone and allow_zone[0] <= i <= allow_zone[1]:
            note(u"　引號例外（律文原樣登載）：%s" % txt)
        else:
            bad_(txt)
    return len(miss)


bad_ = []


def bad_(txt):
    FAIL.append(u"引號破口・" + txt)


zone = (OFF3, OFF4) if OFF3 >= 0 else None
for op, cl, nm in [(u"「", u"」", u"方引號"), (u"『", u"』", u"雙引號"), (u"〔", u"〕", u"六角")]:
    walk(op, cl, nm, zone)
if not any(x.startswith(u"引號破口") for x in FAIL):
    note(u"引號之闭合：除附錄三律文原樣登載者外，俱合")

# ── 十二・節號一制（章內 H2 須自一連貫・形制唯一）────────────────────────
for t, (a, b, sub) in CHAP.items():
    js = [m.group(1) for m in re.finditer(u"^## 第([一二三四五六七八九十]+)節", u"\n".join(BL[a:b]), re.M)]
    ns = [m.group(1) for m in re.finditer(u"^## ([一二三四五六七八九十]+)、", u"\n".join(BL[a:b]), re.M)]
    if js and ns:
        bad(u"%s 節號兩制並存（第N節 %d・裸序 %d）" % (t, len(js), len(ns)))
    if js and [P.cnum(x) for x in js] != list(range(1, len(js) + 1)):
        bad(u"%s 節號不連貫：%s" % (t, js))

# ── 十三・附錄三戒本歷條：各篇之數須副其自宣（號段行按段計）─────────────
ia = next((i for i, l in enumerate(BL, 1) if l.startswith(u"## 附錄三")), 0)
ib = next((i for i in range(ia + 1, len(BL)) if BL[i - 1].startswith(u"## 附錄四")), len(BL))
secs = [(i, BL[i - 1]) for i in range(ia + 1, ib)
        if BL[i - 1].startswith(u"### ") and (u"甲、" in BL[i - 1] or u"乙、" in BL[i - 1])]
tot = 0
for k, (i, h) in enumerate(secs):
    w = re.search(u"戒本 (\\d+) 條", h)
    if not w:
        continue
    want = int(w.group(1))
    md = re.search(u"其第(\\d+)[～~](\\d+)號與前部共戒", h)
    ded = (int(md.group(2)) - int(md.group(1)) + 1) if md else (1 if u"其第1號與前部共戒" in h else 0)
    end = secs[k + 1][0] - 1 if k + 1 < len(secs) else ib
    have = set()
    for l in BL[i:end]:
        r = re.match(u"^\\s*(\\d+)(?:[～~](\\d+))?\\.\\s", l)
        if not r:
            continue
        if r.group(2):
            have.update(range(int(r.group(1)), int(r.group(2)) + 1))
        else:
            have.add(int(r.group(1)))
    tot += len(have)
    if len(have) != want:
        bad(u"戒本篇 %s：宣 %d 號・列 %d（缺 %s）" % (h[4:26], want, len(have),
            u",".join(str(x) for x in sorted(set(range(1, want + 1)) - have)[:10])))
note(u"附錄三歷條：逐篇核其自宣（12 篇），共列 %d 號（比丘 250・尼別宣 233・通數 483 之制）" % tot)


# ── 十一・引號之闭合（律文原樣登載者不計・新冊不得自造破口）──────────────
IA3 = next((i for i, l in enumerate(BL, 1) if l.startswith(u"## 附錄三")), 0)
IB3 = next((i for i in range(IA3 + 1, len(BL)) if BL[i - 1].startswith(u"## 附錄四")), len(BL))
NL = chr(10)
OFF3 = book.index(NL.join(BL[IA3:IB3])) if IA3 else -1
OFF4 = book.index(NL.join(BL[IB3 - 1:IB3])) if IB3 < len(BL) else len(book)


def walk(op, cl, nm, allow_zone=None):
    st, miss = [], []
    for i, c in enumerate(book):
        if c == op:
            st.append(i)
        elif c == cl:
            if st:
                st.pop()
            else:
                miss.append((u"多闭合", i))
    miss += [(u"未闭合", x) for x in st]
    for kind, i in miss:
        ln = book[:i].count(NL) + 1
        txt = u"%s%s L%d：%s" % (nm, kind, ln, book[max(0, i - 40):i + 26].replace(NL, " "))
        if allow_zone and allow_zone[0] <= i <= allow_zone[1]:
            note(u"　引號例外（律文原樣登載）：%s" % txt)
        else:
            bad_(txt)
    return len(miss)


bad_ = []


def bad_(txt):
    FAIL.append(u"引號破口・" + txt)


zone = (OFF3, OFF4) if OFF3 >= 0 else None
for op, cl, nm in [(u"「", u"」", u"方引號"), (u"『", u"』", u"雙引號"), (u"〔", u"〕", u"六角")]:
    walk(op, cl, nm, zone)
if not any(x.startswith(u"引號破口") for x in FAIL):
    note(u"引號之闭合：除附錄三律文原樣登載者外，俱合")

# ── 十二・節號一制（章內 H2 須自一連貫・形制唯一）────────────────────────
for t, (a, b, sub) in CHAP.items():
    js = [m.group(1) for m in re.finditer(u"^## 第([一二三四五六七八九十]+)節", u"\n".join(BL[a:b]), re.M)]
    ns = [m.group(1) for m in re.finditer(u"^## ([一二三四五六七八九十]+)、", u"\n".join(BL[a:b]), re.M)]
    if js and ns:
        bad(u"%s 節號兩制並存（第N節 %d・裸序 %d）" % (t, len(js), len(ns)))
    if js and [P.cnum(x) for x in js] != list(range(1, len(js) + 1)):
        bad(u"%s 節號不連貫：%s" % (t, js))



# ── 九・節級與名級死鏈（章在而節無・案名不屬其章）──────────────────────────
CH_TXT = {t: u"\n".join(BL[a:b]) for t, (a, b, sub) in CHAP.items()}
dead_sec, dead_name = [], []
for m in re.finditer(u"第([一二三四五六七八九十]+)章(第[一二三四五六七八九十]+節)", book):
    ch = u"第%s章" % m.group(1)
    txt = CH_TXT.get(ch)
    if txt is None:
        continue
    sec = m.group(2)
    num = re.match(u"第(.+)節", sec).group(1)
    if not re.search(u"^#{2,6} " + sec, txt, re.M) and not re.search(
            u"^#{2,6} " + num + u"、", txt, re.M):
        dead_sec.append(m.group(0))
for m in re.finditer(u"第([一二三四五六七八九十]+)章案例[一二三四五六七八九十]+『([^』]{1,20})』案", book):
    ch, name = u"第%s章" % m.group(1), m.group(2)
    txt = CH_TXT.get(ch)
    if txt is None:
        continue
    if name not in txt.replace(u" ", u""):
        dead_name.append(u"%s『%s』" % (ch, name))
if not dead_name:
    note(u"名級指針：%d 條（今冊指針唯『第N章案例M』之形，不附括弧名）" % len(re.findall(u"『[^』]{1,20}』案", book)))
if dead_sec:
    bad(u"節級死鏈 %d 條：%s" % (len(dead_sec), u"｜".join(sorted(set(dead_sec))[:10])))
if dead_name:
    bad(u"名級死鏈 %d 條：%s" % (len(dead_name), u"｜".join(sorted(set(dead_name))[:10])))
if not dead_sec and not dead_name:
    note(u"節級與名級指針：全活（節 %d・名 %d）" % (
        len(re.findall(u"第[一二三四五六七八九十]+章第[一二三四五六七八九十]+節", book)),
        len(re.findall(u"第[一二三四五六七八九十]+章『[^』]{1,20}』案", book))))
print(u"\n".join(u"✗ " + x for x in FAIL[-2:]) if (dead_sec or dead_name) else u"")

# ── 十四・字形之齊（簡形唯許存在於引號之內——引號內原典一字不篡）────────
try:
    sys.path.insert(0, os.path.join(ROOT, u"_work"))
    import _simpdict as SD
    KEYS = set(SD.MAP) - set(u"于")      # 『于』乃漢譯與文言正字，非簡形
    inq = []                             # 逐行標：是否處於跨行之引號內
    deep = 0
    for l in BL:
        seg = re.sub(u"「[^」]*」|『[^』]*』", u"", l)
        deep += l.count(u"「") - l.count(u"」") + len(re.findall(u"[「」]", l)) - len(re.findall(u"[「」]", seg))
        inq.append(deep > 0)
    stray = []
    for idx, l in enumerate(BL, 1):
        if l.startswith(u">") or inq[idx - 1]:
            continue                     # 圍注與引文如實登載，不校字形
        outside = re.sub(u"「[^」]*」|『[^』]*』", u"", l)
        for ch in outside:
            if ch in KEYS:
                stray.append((idx, ch, SD.MAP[ch], l.strip()[:44]))
                break
    if stray:
        bad(u"簡形字混入敘述文字 %d 行：%s" % (len(stray), u"｜".join(
            u"L%d %s(當為%s)" % (n, a, b) for n, a, b, _ in stray[:5])))
    else:
        note(u"字形：敘述文字全用正體（引號內如實登載者不計）")
except ImportError:
    note(u"字形之檢未行（缺 _work/_simpdict.py）")

# ── 十五・長段不兩出（同章重複為病，跨章重述只登於目）────────────────────
def chap_at(n):
    cur = u"（卷首末）"
    for t, (a, b, sub) in CHAP.items():
        if a <= n:
            cur = t
    return cur


seen = collections.defaultdict(list)
quoted = collections.defaultdict(list)
for idx, l in enumerate(BL, 1):
    t = norm(l)
    if len(t) < 60:
        continue
    (quoted if l.lstrip().startswith(u">") or l.lstrip().startswith(u"「") else seen)[t[:40]].append(idx)
same, cross = [], []
for k, v in seen.items():
    if len(v) < 2:
        continue
    (same if len(set(chap_at(x) for x in v)) == 1 else cross).append((k, v))
if same:
    bad(u"同章長段兩出 %d 組：例 L%s｜%s" % (len(same), same[0][1][:4], same[0][0][:22]))
note(u"長段：同章兩出 %d 組（須零）・跨章重述 %d 組・同章同引（律文複引，屬當然）%d 組" % (
    len(same), len(cross), sum(1 for k, v in quoted.items() if len(v) > 1)))

print(u"\n".join(u"● " + x for x in NOTE))
if FAIL:
    print(u"\n".join(u"✗ " + x for x in FAIL))
    print(u"退回：%d 項不合格" % len(FAIL))
    sys.exit(1)
print(u"✓ 十指標俱清｜冊身 %d 行・%d 字・漢字 %d" % (len(BL), len(book), len(BN)))
