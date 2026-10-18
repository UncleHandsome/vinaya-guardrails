# -*- coding: utf-8 -*-
"""合編本產成器（甲案・骨架＋全量素材安置）。

讀 `_archive/舊本/` 兩冊 → 依「七部二十八章」產出合編本於工作資料夾根。
鐵則：① 兩本舊本一字不動（只讀）；② 框架百則卡〔遮/開/僧N〕連碼整卡搬入，碼與定位行不動；
③ 護欄 164 案升為六段式，缺欄不編造——一律掛 `〔待寫：…〕`／`〔待校：…〕`，由 merge_check 計數；
④ 凡指針未經重算者，原樣帶入並掛 `〔指針已重算・待復核〕`，不做半改。
用法：python -X utf8 _merge/merge_build.py [--out=路徑]
"""
import os, re, sys, io, glob, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import refnum as RN
import chapmap as CM

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = os.path.join(ROOT, "_archive", u"舊本")
V = glob.glob(os.path.join(OLD, "ver38*.md"))[0]
H = glob.glob(os.path.join(OLD, u"佛陀的護欄*.txt"))[0]
OUT = os.path.join(ROOT, u"合編本_以遮衛性_四分律起心動念心智全書.md")
for a in sys.argv[1:]:
    if a.startswith("--out="):
        OUT = a.split("=", 1)[1]

vtxt = io.open(V, encoding="utf-8").read()
htxt = io.open(H, encoding="utf-8").read()
vlines, hlines = vtxt.split("\n"), htxt.split("\n")

# ── 框架切冊 ────────────────────────────────────────────────────────────────
def h1_ranges(lines, pat=r"^# "):
    ix = [i for i, l in enumerate(lines, 1) if re.match(pat, l)]
    out = []
    for k, i in enumerate(ix):
        j = ix[k + 1] - 1 if k + 1 < len(ix) else len(lines)
        out.append((lines[i - 1].strip("# ").strip(), i, j))
    return out

V_CHAP = {}
for t, i, j in h1_ranges(vlines):
    m = re.match(r"第([一二三四五六七八九])章", t)
    if m:
        V_CHAP[t[:3]] = (i, j)
V_HEAD = (1, V_CHAP["第一章"][0] - 1)      # 书名＋卷首諸件
V_CARDS = {}                                # 〔X N〕 → (起, 迄, 全文)
HD_END = sorted(i for i, l in enumerate(vlines, 1) if re.match(r"^#{1,6} ", l))


def next_head(a, lines, from_idx, lvl=4):
    """自 from_idx 起下一個『不高於卡身層級』之標題行。

    卡是 H4（`#### 〔遮1〕`／`#### 案例一`），其六段欄目標題是 H5——若以『任何層級』為界，
    卡身即在其第一根 H5 欄桿處攔腰折斷，百則只留卡題與定位行（第三十八輪之實測）。
    """
    for i in range(from_idx, len(lines) + 1):
        m = re.match(r"^(#{1,%d}) " % lvl, lines[i - 1])
        if m and i > a:
            return i
    return len(lines) + 1


cix = [(i, l) for i, l in enumerate(vlines, 1) if re.match(r"^#### 〔(?:遮|開|僧|補遺)\d+〕", l)]
for k, (i, l) in enumerate(cix):
    j = next_head(i, vlines, i + 1) - 1
    code = re.match(r"^#### (〔[^〕]+〕)", l).group(1)
    V_CARDS[code] = (i, j, "\n".join(vlines[i - 1:j]).rstrip())
# 附錄
V_APX = {}
for t, i, j in h1_ranges(vlines):
    m = re.match(r"附錄([A-Z])", t)
    if m:
        V_APX[m.group(1)] = (i, j)
    if t.startswith("結語") or t.startswith("終卷"):
        V_APX["結語" if t.startswith("結語") else "終卷"] = (i, j)

# 卡之「主聚」（整卡不拆・唯一歸章；跨聚者另於他章列指針）
CLUSTER = [(u"第七章", [u"波羅夷"]), (u"第八章", [u"僧殘", u"僧伽婆屍沙", u"偷蘭遮", u"二不定"]),
           (u"第九章", [u"捨墮", u"尼薩耆"]), (u"第十章", [u"單提", u"波逸提"]),
           (u"第十一章", [u"波逸提"]), (u"第十二章", [u"提舍尼", u"眾學", u"应当學", u"式叉迦羅尼"]),
           (u"第十三章", [u"犍度", u"羯磨", u"安居", "自恣", u"布薩", u"分衣", u"受戒"])]
CARD_HOME = {}
CNU = {c: i + 1 for i, c in enumerate(u"一二三四五六七八九十")}


def cn2n(s):
    if s.isdigit():
        return int(s)
    if s == u"十":
        return 10
    if u"十" in s:
        a, _, b = s.partition(u"十")
        return (CNU.get(a, 1) or 1) * 10 + (CNU.get(b, 0) or 0)
    return CNU.get(s, 0)


# 主聚之判（規則公開、可改）：取卡內『篇聚名＋第N條』之眾數；篇聚名依正文用詞
CLU = [(u"第九章", [u"尼薩耆波逸提", u"尼薩耆", u"捨墮"]),
       (u"第十二章", [u"波羅提提舍尼", u"提舍尼", u"式叉迦羅尼", u"眾學"]),
       (u"第八章", [u"僧伽婆屍沙", u"僧殘"]),
       (u"第七章", [u"波羅夷"]),
       (u"第十三章", [u"犍度"]),
       (u"第十、十一章", [u"波逸提"])]


def home_of(code, body):
    hit = []
    for fam, names in CLU:
        for nm in names:
            for m in re.finditer(nm + u"[第\\s]{0,2}([0-9]{1,3}|[一二三四五六七八九十]{1,4})[條]?条?", body):
                hit.append((fam, cn2n(m.group(1))))
    if not hit:
        for fam, names in CLU:
            if any(nm in body for nm in names):
                hit.append((fam, 0))
    if not hit:
        return u"第十二章"
    cnt = {}
    for fam, n in hit:
        cnt[fam] = cnt.get(fam, 0) + 1
    top = max(cnt, key=lambda k: (cnt[k], -[c[0] for c in CLU].index(k)))
    if top == u"第十、十一章":
        ns = [n for fam, n in hit if fam == u"第十、十一章" and n > 0]
        lo = sum(1 for x in ns if x <= 45)
        hi = sum(1 for x in ns if x > 45)
        return u"第十一章" if hi > lo else u"第十章"
    return top


for code, (i, j, body) in V_CARDS.items():
    if code.startswith(u"〔補遺"):
        CARD_HOME[code] = u"第十二章"          # 調部補遺歸「威儀最前哨與調部極限裁判」
        continue
    CARD_HOME[code] = home_of(code, body)

# 指南對照表之歸章優先（其表內 97 行俱已落地；附件佚失時改讀 `_merge/掛載表.tsv`）
PLAN_HOME = {}
TSV = os.path.join(ROOT, "_merge", u"掛載表.tsv")
ATT = [a for a in sys.argv[1:] if not a.startswith("--")]
if ATT and os.path.isfile(ATT[0]):
    at = io.open(ATT[0], encoding="utf-8").read()
    io.open(TSV, "w", encoding="utf-8", newline="\n").write(
        "\n".join(l for l in at.split("\n") if l.strip().startswith("|") and (u"〔" in l or u"文獻一" in l)))
if os.path.isfile(TSV):
    cur = None
    for l in io.open(TSV, encoding="utf-8").read().split("\n"):
        cs = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(cs) < 3:
            continue
        m = re.search(u"第([一二三四五六七八九十]+)章", cs[0])
        if m and u"同上" not in cs[0]:
            cur = u"第%s章" % m.group(1)
        for c in re.findall(u"〔(?:遮|開|僧)\\d+〕", cs[2]):
            if cur:
                PLAN_HOME.setdefault(c, cur)
AUTO = 0
for c, h in PLAN_HOME.items():
    if c in CARD_HOME and CARD_HOME[c] != h:
        CARD_HOME[c] = h
        AUTO += 1
print("歸章：指南對照表改寫 %d 卡；其餘 %d 卡依『篇聚名＋條次眾數』規則自動歸章（皆須復核）" % (
    AUTO, len(CARD_HOME) - AUTO))


def normalize_h1(text):
    """全冊最後一掃：非本冊骨架之 H1 一律降為 H2（搬入之塊不許保留原冊章・附錄之 H1）。"""
    KEEP = set(u"# %s　" % ch for ch in TITLES)
    KEEP |= {u"# 【第", u"# 【卷首", u"# 【卷末", u"# 以遮衛性", u"# 合編本", u"# 《"}
    out, fence = [], False
    for l in text.split("\n"):
        if l.startswith("```"):
            fence = not fence
            out.append(l)
            continue
        if not fence and l.startswith(u"# ") and not any(l.startswith(k) for k in KEEP):
            l = u"##" + l[1:]
        out.append(l)
    return "\n".join(out)

# ── 護欄切冊 ────────────────────────────────────────────────────────────────
H_CHAP = {}
for t, i, j in h1_ranges(hlines):
    m = re.match(r"第([一二三四五六七八九十百]+)章", t)
    if m:
        H_CHAP[m.group(0)] = (i, j)
H_FRONT = {"扉頁": (1, 24), "獻辭": (11, 24), "自序": (25, 54), "導讀": (55, 65),
           "凡例": (66, 76), "目錄": (77, 441), "十線": (442, 626)}
H_APX = next((i for i, l in enumerate(hlines, 1) if l.startswith("# 附錄")), None)
H_TAIL = (H_APX, len(hlines))
H_CH20 = H_CHAP.get(u"第二十章", (6580, 6773))

def h_cases(chap_cn):
    """護欄某章之案例卡（起訖・標題）。"""
    if chap_cn not in H_CHAP:
        return []
    s, e = H_CHAP[chap_cn]
    out = []
    for k, l in enumerate(hlines[s - 1:e], s):
        if re.match(r"^#### 案例", l):
            j = next_head(k, hlines[:e], k + 1) - 1
            out.append((k, j, l.strip("# ").strip(), "\n".join(hlines[k - 1:j]).rstrip()))
    return out

# 護欄章 → 合編章
H2N = {u"第一章": u"第一章", u"第二章": u"第二章", u"第三章": u"第三章", u"第四章": u"第四章",
       u"第五章": u"第七章", u"第六章": u"第八章", u"第七章": u"第九章",
       u"第八章": u"第十章", u"第九章": u"第十一章", u"第十章": u"第十二章", u"第十一章": u"第十三章",
       u"第十二章": u"第十四章", u"第十三章": u"第十六章", u"第十四章": u"第十七章",
       u"第十五章": u"第十八章", u"第十六章": u"第二十二章", u"第十七章": u"第二十三章",
       u"第十八章": u"第二十四章", u"第十九章": u"第二十五章", u"第二十章": u"第二十六章"}
# ── 指針重算（relink）：舊冊章次 → 本冊章次 ────────────────────────────────
# 台帳之自裁（可改）：三帳分立——百則帳（框架 100 碼・133 綁定不動）・今冊另立「案帳」
# （164 素材卡之定位行自算，不入 133）・不立〔尼-波N〕新碼（女眾案以素材碼行世）。
V_MAP, H_MAP, SPLIT = CM.V_MAP, CM.H_MAP, CM.SPLIT    # 地圖之法源在 `_merge/chapmap.py`
relink_stat = {u"改指針": 0, u"存疑未改": 0, u"戒本表改": 0, u"多章待裁": 0}
CUT_BUYI = [0]                       # 附錄H 內被挖代之補遺卡數（挖在重算之前，否則替不到）
CUT_V6 = [0]                         # 框架第六章原卷首搬入字量


def _map_ch(num, sec, src):
    m = V_MAP if src == "v" else H_MAP
    key = num if num.startswith(u"第") else u"第%s章" % num
    sp = SPLIT.get(key)                                  # 拆章者唯 SPLIT 有，故先問 SPLIT；
    if sp:                                                # 先問地圖則「第四章」之屬 v 而不在 V_MAP，
        if sec and sp[2] in sec:                          #   未命中即原樣回拋——七十六條死鏈由此而生。
            return sp[1]
        if not sec:
            relink_stat[u"存疑未改"] += 1
            return sp[0] + u"（另見%s）" % sp[1]
        return sp[0]
    if key not in m:
        return None
    if u"～" in m[key]:
        relink_stat[u"多章待裁"] += 1
    return m[key]


def relink(text, src):
    """塊內之舊冊章次 → 本冊章次。圍欄內・`> ` 逐字引文行不動（彼為『如實登載』之域）。"""
    out, fence = [], False
    for l in text.split("\n"):
        if l.startswith("```"):
            fence = not fence
            out.append(l)
            continue
        if fence or l.startswith("> "):
            out.append(l)
            continue
        if src == "h" and u"書中：第" in l:                      # 戒本歷條總表之 377 條指針
            def fx(mo):
                tg = _map_ch(mo.group(1), u"", "h")
                if not tg:
                    return mo.group(0)
                relink_stat[u"戒本表改"] += 1
                return u"書中：%s %s（素材卡）" % (tg, mo.group(2))
            l = re.sub(u"書中：第([一二三四五六七八九十]+)章(案例[一二三四五六七八九十]+)", fx, l)

        def fix(mo):
            tg = _map_ch(mo.group(1), mo.group(2) or u"", src)
            if not tg:
                relink_stat[u"存疑未改"] += 1
                return mo.group(0)
            relink_stat[u"改指針"] += 1
            return tg + (mo.group(2) or u"")
        l = re.sub(u"第([一二三四五六七八九十]+)章(第[一二三四五六七八九十]+節)?", fix, l)
        out.append(l)
    return "\n".join(out)


TODER = [u"第一章", u"第二章", u"第三章", u"第四章", u"第五章", u"第六章", u"第七章", u"第八章",
         u"第九章", u"第十章", u"第十一章", u"第十二章", u"第十三章", u"第十四章", u"第十五章"]

# ── 升六段式 ────────────────────────────────────────────────────────────────
FIELD_MAP = {u"案發現場": u"事相經過", u"行為心理剖析": u"心相照鏡", u"防禦靶點": None,
             u"佛陀處斷": u"佛陀處斷", u"人間智慧": u"人間智慧"}
MISS = u"〔待寫：%s〕（護欄原卡無此欄，須新寫後方可刪此標）"
UNCHECK = u"〔待校：定位行〕"

def upgrade_hulan(chap_cn, body, title):
    """護欄案例卡 → 六段式（缺欄掛待寫，不編造）。"""
    # 原卡自帶 `#### 案例N：…` 標題，須剝去——否則本冊之 H4 卡被它截斷，六段散架
    body = relink(body, "h")                     # 先重算章次，再切欄
    body = re.sub(r"^#### 案例[一二三四五六七八九十]+：[^\n]*\n", "", body)
    body = re.sub(r"^#### ", "###### ", body, flags=re.M)
    out = [u"##### 事相經過", ""]
    seg = re.split(r"\n(?=\*\s*\*\*【)", body)
    parts = {}
    for s in seg:
        m = re.match(r"\*\s*\*\*【([^】]{2,14})", s)
        if m:
            parts[m.group(1)] = s
    out.append(parts.get(u"案發現場", body).strip())
    out += ["", u"##### 心相照鏡", "",
            parts.get(u"行為心理剖析", MISS % u"心相照鏡（第二人稱）").strip()]
    out += ["", u"##### 佛陀處斷", "",
            MISS % u"佛陀處斷（三環：初環見真實・次環安僧伽・終環入無事）"]
    out += ["", u"##### 人間智慧", "",
            MISS % u"人間智慧"]
    yd = [l for l in body.split("\n") if l.startswith("> ") and (u"【" in l or u"若比丘" in l)]
    out += ["", u"◎原典", "",
            ("\n".join(yd) if yd else MISS % u"原典逐字（須冠卷段方構成逐字宣稱）").strip(),
            "", u"〔待校：卷段出處〕" if yd else ""]
    return "\n".join([UNCHECK] + out).rstrip()

# ── 骨架 ────────────────────────────────────────────────────────────────────
PARTS = [(u"第一部", u"理論奠基——懸崖邊的修道要塞（體・哲學與立法本懷）",
          [u"第一章", u"第二章", u"第三章", u"第四章"]),
         (u"第二部", u"深層心相——起心動念的心智解剖室（相・唯識心所與微觀動機）", [u"第五章", u"第六章"]),
         (u"第三部", u"比丘戒防禦體系與古典判例法典（用・男眾學處與行為設計）",
          [u"第七章", u"第八章", u"第九章", u"第十章", u"第十一章", u"第十二章", u"第十三章"]),
         (u"第四部", u"比丘尼戒的鋼鐵防護網（用・女眾學處與性別防暴工程）",
          [u"第十四章", u"第十五章", u"第十六章", u"第十七章", u"第十八章"]),
         (u"第五部", u"僧伽司法程序——法權、證據與復權（法・正當程序與制度急診）",
          [u"第十九章", u"第二十章", u"第二十一章"]),
         (u"第六部", u"法意深探——歷史爭議與世界律學（源・法統傳承與跨域共振）",
          [u"第二十二章", u"第二十三章", u"第二十四章"]),
         (u"第七部", u"現代啟示——從個人自律到組織治理（化・古老智慧之當代落地）",
          [u"第二十五章", u"第二十六章", u"第二十七章", u"第二十八章"])]
TITLES = {u"第一章": u"為什麼現代人讀不懂戒律？——法條主義與立法本懷的千年斷裂",
          u"第二章": u"正統律學的核心密碼——什麼是「以遮衛性」？",
          u"第三章": u"城郭宮殿之喻——同心圓防禦工程與五重陣地模型",
          u"第四章": u"結戒十句義與八大正理——僧伽要塞的母法中樞與四大神聖邊界",
          u"第五章": u"樹根與枝幹：微觀心所動力學與六大領域換裝之則",
          u"第六章": u"照鏡察心：三軸病灶、六重心智閘門與四大臨界標尺（但書）",
          u"第七章": u"四波羅夷——斷頭之罪：王城的四次失守與不可逆客觀死線",
          u"第八章": u"十三僧殘——身受重傷的宮牆、欲望改裝與僧中復健制度",
          u"第九章": u"三十捨墮——斬斷物質貪婪，以物理沒收打造極簡真空",
          u"第十章": u"九十單提（上）——言語、獨處與微環境行為管理（第 1～45 條）",
          u"第十一章": u"九十單提（下）——暴力阻斷、思想防毒與司法正義（第 46～90 條）",
          u"第十二章": u"威儀最前哨與調部極限裁判——提舍尼、眾學法與邊緣疑難判例法",
          u"第十三章": u"二十犍度（上）——僧團憲典與組織運作現場（行舍羅、安居與分衣）",
          u"第十四章": u"為什麼比丘尼戒更多？——古印度生存深淵與女性自衛工程",
          u"第十五章": u"比丘尼八波羅夷與十七僧殘——觸電即死的高壓護欄與獨立自治",
          u"第十六章": u"比丘尼三十捨墮——五衣裝甲、器物自戀祛魅與公義信託",
          u"第十七章": u"109 條不共單提（上）——身體純化、斷除自慰與防暴機制（第 70～124 條）",
          u"第十八章": u"109 條不共單提（下）——招生風控、二部僧治理與尊卑秩序（第 125～178 條）",
          u"第十九章": u"如法推尋——自言治、結界管轄與控辯正義",
          u"第二十章": u"四諍與七滅諍體系——僧團最高憲法法院與如草覆地和解法式",
          u"第二十一章": u"解縛還淨——處分、可懺性、僧殘別住算法與出罪復權閉環",
          u"第二十二章": u"阿難的困惑——「微細戒可捨」公案、五百結集與歷史代價",
          u"第二十三章": u"歷代祖師的智慧——南山律宗的千年接力",
          u"第二十四章": u"南北傳的交匯——世界律學視角下的「情境選擇架構」共振",
          u"第二十五章": u"當欲望來臨時，意志力為何不堪一擊？——神經科學與前額葉叛變",
          u"第二十六章": u"個人生活的「四重護欄工程指南」",
          u"第二十七章": u"現代道場與機構治理會通指南",
          u"第二十八章": u"重新定義自由——法架自捨，重歸林下（繳械印：「 歇 」）"}

def vslice(key, sub=None):
    s, e = V_CHAP[key]
    lines = vlines[s - 1:e]
    if sub:
        ix = [i for i, l in enumerate(lines) if l.startswith("### ") and sub in l]
        if not ix:
            return u"〔缺：%s 之 %s〕" % (key, sub)
        a = ix[0]
        b = next((i for i in range(a + 1, len(lines)) if lines[i].startswith("### ")), len(lines))
        lines = lines[a:b]
    return relink(strip_h1("\n".join(lines).rstrip()), "v")


def vslice_minus(key, sub):
    """取整章而挖去某一節（供 19 章＝框架第四章除第五節；20 章唯取該節）。"""
    full = vslice(key)
    seg = vslice(key, sub)
    return full.replace(seg, u"〔此節移入本冊之第廿章〕") if seg and seg in full else full


def strip_h1(t):
    """搬入之整章／整附錄須脫其原 H1（新冊自有其題），否則章數與目錄皆亂；
    塊內若還殘他冊 H1（部題・結語・附錄題），一律降為 H2。"""
    lines = t.split("\n")
    while lines and (not lines[0].strip() or lines[0].startswith(u"# ")):
        lines.pop(0)
    out, fence = [], False
    for l in lines:
        if l.startswith("```"):
            fence = not fence
        elif not fence and l.startswith(u"# "):
            l = u"## " + l[2:]
        out.append(l)
    return "\n".join(out).rstrip()

def hslice(chap_cn):
    if chap_cn not in H_CHAP:
        return u"〔缺：護欄 %s〕" % chap_cn
    s, e = H_CHAP[chap_cn]
    return relink(strip_h1("\n".join(hlines[s - 1:e]).rstrip()), "h")


def h_prose(chap_cn, before=None, after=None):
    """護欄某章之『非卡散文』（章首論述・結構解剖・圖表）。卡身另由 h_cases 升六段式，
    故此處逐張挖去卡身，只留其餘——昔時只搬卡不搬論述，女眾兩章之導言遂全佚（第三十八輪實測）。

    before／after：以某標題字樣為刀，取其一側（供護欄第十二章分隸合編第十四・十五兩章）。
    """
    if chap_cn not in H_CHAP:
        return u""
    s, e = H_CHAP[chap_cn]
    seg = "\n".join(hlines[s - 1:e]).rstrip()
    if before and before in seg:
        seg = seg.split(before)[0]
    elif after and after in seg:
        seg = seg[seg.find(after):]
    for i, j, t, bd in h_cases(chap_cn):
        seg = seg.replace(bd, u"")
    seg = re.sub(r"\n{3,}", "\n\n", seg).strip()
    if len(seg) < 60:
        return u""
    return relink(strip_h1(seg), "h")


def v_prose6():
    """框架第六章之『非卡散文』（原卷首凡例・情境導航矩陣・三聚之題）。
    百則之卡已分隸第七～十三章，唯此段導航文字昔時未搬——不搬則三聚之名與矩陣俱亡。"""
    s, e = V_CHAP[u"第六章"]
    seg = "\n".join(vlines[s - 1:e]).rstrip()
    for c, (i, j, bd) in V_CARDS.items():
        if s <= i <= e and bd and bd in seg:
            seg = seg.replace(bd, u"")
    seg = re.sub(r"\n{3,}", "\n\n", seg).strip()
    return relink(strip_h1(seg), "v") if len(seg) > 60 else u""



def demote(t, levels=1):
    """搬入之塊須降其標題層，否則合冊之 H 序亂（跳過 ``` 圍欄內之行）。"""
    out, fence = [], False
    for l in t.split("\n"):
        if l.startswith("```"):
            fence = not fence
            out.append(l)
            continue
        if not fence and l.startswith("#"):
            n = len(l) - len(l.lstrip("#"))
            out.append("#" * min(6, n + levels) + l[n:])
        else:
            out.append(l)
    return "\n".join(out).rstrip()


def vcards_of(chap_cn, with_buyi=False):
    codes = [c for c, h in CARD_HOME.items() if h == chap_cn and not c.startswith(u"〔補遺")]
    if with_buyi:
        codes += [c for c in V_CARDS if c.startswith(u"〔補遺")]
    codes = sorted(codes, key=lambda z: (z[0].startswith(u"〔補遺"), int(re.search(r"\d+", z).group())))
    return "\n\n---\n\n".join(relink(V_CARDS[c][2], "v") for c in codes) if codes else u"（本章無框架母案卡）"

O = []
w = O.append
w(u"# 以遮衛性——四分律行為心理學與起心動念心智分析框架【合編本】")
w(u"")
w(u"> **產製**：`_merge/merge_build.py`（讀 `_archive/舊本/` 兩冊・只讀；雨本一字不動）")
w(u"> **落成**：%s｜骨架＝七部二十八章｜案例＝雙層（框架百則連碼整卡＋護欄 164 案升六段式）" % datetime.date.today().isoformat())
w(u"> **現況**：骨架與全量素材已安置；凡 `〔待寫〕``〔待校〕``〔指針已重算・待復核〕` 皆係未竟之帳，"
  u"由 `_merge/merge_check.py` 計數——**此標未清零，即不得稱為定本。**")
w(u"")
w(u"---")
w(u"")
# 卷首
w(u"## 【卷首・合編凡例】（規・文獻、標記與體例公約）")
w(u"")
w(u"> 〔待校：本冊凡例須合兩制——框架「引文承諾六律」＋護欄「四例」；並定三層標記之推行範圍〕")
w(u"")
w(u"### 甲・框架冊卷首（指針已由 relink 重算）")
w(u"")
w(demote(relink("\n".join(vlines[V_HEAD[0] - 1:V_CHAP[u"第一章"][0] - 1]).rstrip(), "v"), 2))
w(u"")
w(u"### 乙・護欄冊卷首（指針已由 relink 重算）")
w(u"")
w(demote(relink("\n".join(hlines[0:H_CHAP[u"第一章"][0] - 1]).rstrip(), "h"), 2))
w(u"")
w(u"---")
w(u"")
# 七部
for pname, ptitle, chaps in PARTS:
    w(u"# 【%s：%s】" % (pname, ptitle))
    w(u"")
    for ch in chaps:
        w(u"# %s　%s" % (ch, TITLES[ch]))
        w(u"")
        body = []
        if ch in (u"第一章", u"第二章", u"第三章", u"第四章"):
            body.append(u"## 甲・護欄冊之文〔指針已重算・待復核〕\n\n" + hslice(ch)
                        if ch == u"第四章" else hslice(ch))
            if ch == u"第四章":
                body.append(u"## 乙・框架冊第一章全章（立法本懷與八大正理——本冊第四章即此兩源所合，"
                            u"故六節之序一仍其舊，凡指「第四章第N節」者皆指此）〔指針已重算・待復核〕\n\n"
                            + vslice(u"第一章"))
        elif ch == u"第五章":
            body.append(vslice(u"第二章"))
        elif ch == u"第六章":
            body.append(vslice(u"第三章"))
        elif ch in (u"第七章", u"第八章", u"第九章", u"第十章", u"第十一章", u"第十二章", u"第十三章"):
            hc = {u"第七章": u"第五章", u"第八章": u"第六章", u"第九章": u"第七章",
                  u"第十章": u"第八章", u"第十一章": u"第九章", u"第十二章": u"第十章",
                  u"第十三章": u"第十一章"}[ch]
            pr = h_prose(hc)
            if pr:
                body.append(u"## 甲・護欄本章章首論述（今語・結構解剖，卡身已挖出不兩出）〔指針已重算・待復核〕\n\n" + pr)
            if ch == u"第七章":
                p6 = v_prose6()
                if p6:
                    body.append(u"## 乙・框架百則原卷首（凡例・情境導航矩陣・三聚題序；卡身分隸本冊第七～十三章）〔指針已重算・待復核〕\n\n" + p6)
                    CUT_V6[0] = len(p6)
            body.append(u"### 第一節・古典判例（框架冊百則之歸屬此聚者，連碼整卡）\n\n" +
                        vcards_of(ch, with_buyi=(ch == u"第十二章")))
            ups = []
            for i, j, title, bd in h_cases(hc):
                ups.append(u"#### 〔素材・護欄 %s %s〕\n\n%s" %
                           (hc, re.match(r"案例[一二三四五六七八九十]+", title).group(0),
                            upgrade_hulan(hc, bd, title)))
            body.append(u"### 第二節・今語敘事（護欄冊原案，升六段式）\n\n" + ("\n\n---\n\n".join(ups) if ups else u"（本章無護欄案例卡）"))
            if ch == u"第十三章":
                body.append(u"〔未裁：二十犍度只標「上」而全書無「下」——護欄第十一章 35,090 字／27 案之剩餘部分，"
                            u"須裁另立「第十四章（下）」併入或削。〕")
                raw = "\n".join(vlines[V_APX["H"][0]:V_APX["H"][1]]).rstrip()
                for c, (i, j, bd) in V_CARDS.items():
                    if c.startswith(u"〔補遺") and bd in raw:
                        raw = raw.replace(bd, u"→ 已入第十二章第三節　%s" % c)
                        CUT_BUYI[0] += 1
                hseg = demote(relink(strip_h1(raw), "v"), 1)
                body.append(u"### 末節・調部導言與校勘之據（框架附錄 H 之非補遺部分）〔指針已重算・待復核〕\n\n" + hseg)
        elif ch in (u"第十四章", u"第十五章", u"第十六章", u"第十七章", u"第十八章"):
            hc = {u"第十四章": u"第十二章", u"第十五章": u"第十二章", u"第十六章": u"第十三章",
                  u"第十七章": u"第十四章", u"第十八章": u"第十五章"}[ch]
            cs = h_cases(hc)
            ups = [u"#### 〔素材・護欄 %s %s〕\n\n%s" %
                   (hc, re.match(u"案例([一二三四五六七八九十]+)", t).group(0),
                    upgrade_hulan(hc, b, t)) for i, j, t, b in cs]
            hd = {u"第十四章": u"甲・護欄第十二章章首論述（女眾戒何以更多）",
                  u"第十五章": u"甲・護欄第十二章『三、尼端死罪』之解剖",
                  u"第十六章": u"甲・護欄第十三章章首論述",
                  u"第十七章": u"甲・護欄第十四章章首論述",
                  u"第十八章": u"甲・護欄第十五章章首論述"}[ch] + u"〔指針已重算・待復核〕"
            pr = (h_prose(hc, before=u"### 三、") if ch == u"第十四章" else
                  h_prose(hc, after=u"### 三、") if ch == u"第十五章" else h_prose(hc))
            if pr:
                body.append(u"## %s（今語・卡身已挖出不兩出）\n\n%s" % (hd, pr))
            if ch != u"第十四章":
                body.append(u"\n\n---\n\n".join(ups) if ups else u"（本章無護欄案例卡）")
            body.append(u"〔未裁：女眾 48 案在框架側無一尼篇本位母案可掛——〔尼-波N〕係新立碼，"
                        u"用則百則閉環破（100→105）；不用則此章無法相帳。〕")
        elif ch == u"第十九章":
            body.append(vslice_minus(u"第四章", u"第五節"))   # 第五節另立為第廿章，不使兩出
        elif ch == u"第二十章":
            body.append(vslice(u"第四章", u"第五節"))
        elif ch == u"第二十一章":
            body.append(vslice(u"第五章"))
        elif ch in (u"第二十二章", u"第二十三章", u"第二十四章"):
            body.append(hslice({u"第二十二章": u"第十六章", u"第二十三章": u"第十七章",
                               u"第二十四章": u"第十八章"}[ch]))
        elif ch == u"第二十五章":
            body.append(hslice(u"第十九章"))
        elif ch == u"第二十六章":
            body.append(hslice(u"第二十章"))
        elif ch == u"第二十七章":
            body.append(vslice(u"第九章"))
        elif ch == u"第二十八章":
            if u"結語" in V_APX:
                s, e = V_APX[u"結語"]
                body.append("\n".join(vlines[s - 1:e]).rstrip())
            tix = next((i for i, l in enumerate(hlines, 1) if l.startswith(u"# 尾聲") or
                        (l.startswith("#") and u"尾聲" in l)), H_CH20[1])
            body.append(u"### 護欄冊・尾聲〔指針已重算・待復核〕\n\n" +
                        relink("\n".join(hlines[tix - 1:H_APX - 1]).rstrip(), "h"))
        if ch not in (u"第七章", u"第八章", u"第九章", u"第十章", u"第十一章", u"第十二章", u"第十三章"):
            ex = vcards_of(ch)
            if u"（本章無框架母案卡）" not in ex:
                body.append(u"### 本章所攝框架判例卡（連碼整卡・歸章待裁）\n\n" + ex)
        w("\n\n".join(x for x in body if x))
        w(u"")
        w(u"---")
        w(u"")
# 卷末
w(u"# 【卷末・工具箱與附錄】（息・隨身法器與考據底冊）")
w(u"")
w(u"## 工具箱　隨身操作（框架第八章原樣帶入）〔指針已重算・待復核〕")
w(u"")
w(vslice(u"第八章"))
w(u"")
for k, t in [("附錄一", "A"), ("附錄二", "B"), ("附錄三", None), ("附錄四", None),
             ("附錄五", "J"), ("附錄六", None)]:
    w(u"## %s" % k)
    w(u"")
    if t:
        w(demote(relink(strip_h1("\n".join(vlines[V_APX[t][0] - 1:V_APX[t][1]]).rstrip()), "v"), 1))
    elif k == u"附錄三":
        w(demote(relink(strip_h1("\n".join(vlines[V_CHAP[u"第七章"][0] - 1:V_CHAP[u"第七章"][1]]).rstrip()), "v"), 1))
    elif k == u"附錄四":
        w(demote(relink(strip_h1("\n".join(hlines[H_APX - 1:len(hlines)]).rstrip()), "h"), 1))
    else:
        for x in ("D", "E", "F"):
            w(demote(relink(strip_h1("\n".join(vlines[V_APX[x][0] - 1:V_APX[x][1]]).rstrip()), "v"), 1))
    w(u"")
    w(u"---")
    w(u"")
w(u"## 附錄七（合編新增・須裁）　框架隨冊之附錄 I（H 已入第十二・十三章）")
w(u"")
w(u"〔未裁：指南六大附錄未列框架之 H・I 兩篇。本篇（I，389 行／11,101 字）如實全數帶入；"
  u"H 之補遺十五則已入第十二章第三節，H 其餘部分隨冊帶入第十三章末——削與留須奉裁。〕")
w(u"")
for x in ("I",):
    w(demote(relink(strip_h1("\n".join(vlines[V_APX[x][0] - 1:V_APX[x][1]]).rstrip()), "v"), 1))
    w(u"")
w(u"## 終卷　全書竣工呈辭與終局迴向偈〔指針已重算・待復核〕")
w(u"")
w(demote(relink(strip_h1("\n".join(vlines[V_APX[u"終卷"][0] - 1:V_APX[u"終卷"][1]]).rstrip()), "v"), 1))

book = "\n".join(x for x in O if x != u"")
book = re.sub(r"\n{4,}", "\n\n\n", book)
def tag_dead_refs(text):
    """冊成之後之一掃：凡「第N章第M節」而該章實無此節者，就地掛〔指針待判〕——
    不靜態留舊號（跨冊指涉本有兩義，強猜即錯），亦不留死鏈於無形。"""
    out, n = RN.tag_dead(text)
    print("指針待判：%d 條已就地標出（跨冊兩義者，須逐條裁）" % n)
    return out


book = normalize_h1(book)
book = tag_dead_refs(book)
io.open(OUT, "w", encoding="utf-8", newline="\n").write(book + "\n")
print("產出：%s" % OUT)
print("行 %d｜漢字 %d｜章 %d｜待寫 %d｜待校 %d｜指針待改 %d｜未裁 %d" % (
    book.count("\n") + 1, len(re.findall(r"[一-鿿]", book)),
    len(re.findall(r"^# 第[一二三四五六七八九十]+章", book, re.M)),
    book.count(u"〔待寫"), book.count(u"〔待校"), book.count(u"〔指針已重算・待復核〕"), book.count(u"〔未裁")))
print("指針重算：%s" % ("｜".join("%s %d" % (k, v) for k, v in relink_stat.items())))
print("附錄H 挖代之補遺卡：%d 張（須與補遺總數相符，否則有雙出）" % CUT_BUYI[0])
print("框架第六章原卷首搬入：%d 字" % CUT_V6[0])
print("框架卡安置：%d／115（補遺 %d）" % (
    len(CARD_HOME), sum(1 for k, v in CARD_HOME.items() if k.startswith(u"〔補遺"))))
from collections import Counter as _C
hist = _C(CARD_HOME.values())
print("主聚分布（規則：卡內『篇聚名＋第N條』之眾數，可改）：")
for k in sorted(hist, key=lambda z: -hist[z]):
    print("   %-12s %2d 卡" % (k, hist[k]))
