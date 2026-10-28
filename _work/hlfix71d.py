# -*- coding: utf-8 -*-
"""第 71 輪・指針與宣稱之總歸位。
法源：附錄〈全戒本歷條總表〉乙部「一百七十八單提」段之『書中：』欄（由 `_work/gen_appendix.py` 生，
      故本器只讀 `_work/appendix_jieben.md`，不另立第二套落點）。
病：第十四／十五章今改主題制（各八案，條號錯落第 70～178 之間），舊指針仍按歷數之『第N章案例M』引，
    遂兩病：①死指（案例九以上，兩章俱唯八案）；②號同實異（舊「案例二」≠新「案例二」）。
治：凡正文（附錄以前、第一章以後）指入第十四／十五章之『案例M』，取其最近之尼單提條號組，
    依附錄圖求唯一落點而改；落點為『第N節』（案外之條目）者改指該節；一號多點・無號可拘者列「須裁」，
    須裁未清則不寫檔（老规矩：器不猜）。
另兩刀：①全書自稱案例總數 ➔ 實數（本器當場數「#### 案例」標題，不自信舊帳）；
       ②第十三章導言「不共單提法的前半部（第70至124條）」乃舊分卷之說，今章以主題分，改如實語（條數亦自附錄算）。
"""
import io
import os
import re
import sys
import time
import hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "_work"))
import hulan_path as HP  # noqa: E402

GO = u"--go" in sys.argv
MD = os.path.join(ROOT, "_work", "appendix_jieben.md")

raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
old_sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
L = raw.split(u"\r\n")

# ── 附錄圖（只取「一百七十八單提」段）───────────────────────────────
M = io.open(MD, encoding="utf-8").read().split(u"\n")
i0 = next(i for i, s in enumerate(M) if u"一百七十八單提" in s and s.startswith(u"#"))
i1 = next((i for i in range(i0 + 1, len(M)) if M[i].startswith(u"# ")), len(M))
# 只認「波逸提」之戒文行，且號在 70～178（不共單提）：段末另有「七滅諍」之 1～7 目，非戒條，勿混入圖。
ROW = re.compile(u"^\\s*([0-9]+)(?:～([0-9]+))?\\.[^｜]*波逸提[^｜]*｜\\s*書中：(第[^｜\\s]+)")
MAP = {}
for s in M[i0:i1]:
    m = ROW.match(s)
    if not m:
        continue
    a = int(m.group(1))
    for n in range(a, int(m.group(2) or a) + 1):
        if 70 <= n <= 178:
            MAP[n] = m.group(3).rstrip(u"、，。")
sys.stdout.write(u"圖：%s 段 L%d～%d｜尼單提落點 %d 號（第%d～%d條）\n"
                 % (M[i0][:22], i0 + 1, i1, len(MAP), min(MAP), max(MAP)))

body0 = 0
apx = next(i for i, s in enumerate(L) if s.startswith(u"# 附錄"))
# 卷首之「十線地圖」表（L465 附近）亦帶指針，故掃描自檔頭起；惟須辨其落於哪一節，逐處隨印。
H1 = [(i, s[:20]) for i, s in enumerate(L) if s.startswith(u"# ")]


def sect(i):
    cur = u"（卷首·扉頁）"
    for h, t in H1:
        if h <= i:
            cur = t
        else:
            break
    return cur


sys.stdout.write(u"正本 %d 行｜掃描界 L1～L%d（附錄以前）｜H1 %d 個\n"
                 % (len(L), apx + 1, len(H1)))

U10 = [u"零", u"一", u"二", u"三", u"四", u"五", u"六", u"七", u"八", u"九"]


def cn(n):
    if n < 10:
        return U10[n]
    if n < 20:
        return u"十" + (U10[n % 10] if n % 10 else u"")
    if n < 100:
        return U10[n // 10] + u"十" + (U10[n % 10] if n % 10 else u"")
    r = n % 100
    s = U10[n // 100] + u"百"
    if r == 0:
        return s
    if r < 10:
        return s + u"零" + U10[r]
    if r < 20:
        return s + u"一" + cn(r)
    return s + cn(r)


# ── 案例實數 ──────────────────────────────────────────────────────
NC = sum(1 for s in L[:apx] if s.startswith(u"#### 案例"))
sys.stdout.write(u"案例實數：%d（『#### 案例』標題，正文內）\n" % NC)
assert NC == 115, u"案例實數與本輪之計（115）不合，先查再改"

edits = []


def add(i, a, b, txt, why):
    for ei, ea, eb, _ in edits:
        if ei == i and ea < b and eb > a:
            sys.stdout.write(u"  ✗ 重疊不改 L%d|%s｜已佔 %d～%d\n" % (i + 1, why, ea, eb))
            return False
    edits.append((i, a, b, txt))
    return True


# ── ① 指針歸位 ────────────────────────────────────────────────────
PTR = re.compile(u"第([四十五十]+)章案例([0-9一二三四五六七八九十]+)")
GRP = re.compile(u"第\\s*([0-9]+(?:\\s*[、,，~～-]\\s*[0-9]+)*)\\s*條")


def expand(seg):
    out = []
    for it in re.split(u"[、,，]", seg):
        it = it.strip()
        if not it:
            continue
        if re.search(u"[~～-]", it):
            a, b = re.split(u"[~～-]", it)
            out += range(int(a), int(b) + 1)
        else:
            out.append(int(it))
    return out


manual = []
for i in range(body0, apx):
    s = L[i]
    for m in PTR.finditer(s):
        if m.group(1) not in (u"十四", u"十五"):
            continue
        gs = []
        for g in GRP.finditer(s):
            d = (m.start() - g.end()) if g.end() <= m.start() else (g.start() - m.end()) + 40
            gs.append((abs(d) if d >= 0 else -d, g))
        if not gs:
            manual.append((i + 1, m.group(0), u"行內無條號", s))
            continue
        gs.sort(key=lambda x: x[0])
        dist, g = gs[0]
        if dist > 120:
            manual.append((i + 1, m.group(0), u"最近條號距 %d＞120（不敢硬配）" % dist, s))
            continue
        nums = [n for n in expand(g.group(1)) if n in MAP]
        if not nums:
            manual.append((i + 1, m.group(0), u"第 %s 條不在尼單提圖內" % g.group(1), s))
            continue
        pts = sorted(set(MAP[n] for n in nums))
        if len(pts) > 1:
            manual.append((i + 1, m.group(0), u"一組條號多点：%s｜號=%s" % (pts, nums), s))
            continue
        tgt = pts[0]
        if not re.match(u"第十[四五]章", tgt):
            manual.append((i + 1, m.group(0),
                           u"條號第%s條落於 %s（非十四／十五，恐誤配）" % (g.group(1), tgt), s))
            continue
        if tgt == m.group(0):
            continue
        if u"案例" in tgt:
            sys.stdout.write(u"  ○ L%-5d|[%s] %s ➔ %s（據單提第%s條｜窗內另見：%s）\n"
                             % (i + 1, sect(i), m.group(0), tgt, g.group(1),
                                u",".join(x.group(1) for x in GRP.finditer(s))))
            add(i, m.start(), m.end(), tgt, m.group(0))
        else:
            manual.append((i + 1, m.group(0), u"落點非案例而為%s（須改句式）" % tgt, s))

# ── ② 親裁兩處（無條號可拘，依文義定）─────────────────────────────
ADJ = [(u"持沙門衣施與外道白衣者", u"第十四章案例二十", u"第十四章第二節",
        u"第107條之落點在第十四章第二節【案外之條目】"),
       (u"百歲尼禮新戒之解剖", u"第十五章案例七", u"第十五章案例八",
        u"八敬第一「百臘比丘尼見初受戒比丘」之解剖在今第十五章案例八（八敬法與位階攻防）"),
       (u"床是空間最誠實的記錄", u"第十四章案例十八", u"第十四章案例五",
        u"一行五號：84・115・116 落案例五，90・91 落案例一；行旨乃『白衣舍之床與不辭而去』➔從多數亦從主題"),
       (u"兩年考核：十八加二", u"第十五章案例八", u"第十五章案例二",
        u"一行多號：121～127・168 落案例二（准入風控Ⅱ・兩年考核期），131 落案例三，129～130 入第二節案外➔從主題")]
for anchor, a, b, why in ADJ:
    hit = [i for i in range(body0, apx) if anchor in L[i] and a in L[i]]
    if len(hit) != 1:
        manual.append((0, a, u"锚命中 %d 次（%s）" % (len(hit), anchor), u""))
        continue
    i = hit[0]
    sys.stdout.write(u"  △ L%-5d|%s ➔ %s（親裁：%s）\n" % (i + 1, a, b, why))
    add(i, L[i].index(a), L[i].index(a) + len(a), b, a)
    manual = [x for x in manual if x[1] != a]

# ── ③ 自稱總數 ────────────────────────────────────────────────────
for pat in (u"一百三十七則案例", u"一百三十七則", u"137 則案例", u"137則案例"):
    hit = [i for i in range(body0, apx) if pat in L[i]]
    for i in hit:
        sys.stdout.write(u"  ‧ L%-5d|自稱 %s ➔ 案例實數 %d\n" % (i + 1, pat, NC))
        seg = (cn(NC) + u"則案例") if pat.startswith(u"一百") else (u"%d 則案例" % NC)
        add(i, L[i].index(pat), L[i].index(pat) + len(pat), seg, pat)
    if hit:
        break
else:
    sys.stdout.write(u"  ‧ 全書自稱總數：未尋得舊句式（殘留搜索見下）\n")
RES = re.compile(u"一百三十[七则則]|全書[一二0-9]{2,3}則案例")
r = [i + 1 for i in range(body0, apx)
     if RES.search(L[i]) and not any(e[0] == i for e in edits)]
sys.stdout.write(u"  殘留舊總數（已排隊者除外）：%s\n" % (r or u"無"))

# ── ④ 第十三章導言舊分卷宣稱 ──────────────────────────────────────
n14 = len([n for n, p in MAP.items() if p.startswith(u"第十四章")])
n15 = len([n for n, p in MAP.items() if p.startswith(u"第十五章")])
sys.stdout.write(u"依附錄算：第十四章落點 %d 條｜第十五章落點 %d 條｜合 %d\n"
                 % (n14, n15, n14 + n15))
OLD_CLAIM = u"一百零九條比丘尼不共單提法的前半部（第70至124條）"
NEW_CLAIM = (u"一百零九條比丘尼不共單提法中關乎女眾身軀、衣物、空間與共住安隱的 %s"
             u"（條號錯落於第70至178條之間，其餘 %s另入第十五章）"
             % (cn(n14) + u"條", cn(n15) + u"條"))
hit = [i for i in range(body0, apx) if OLD_CLAIM in L[i]]
if len(hit) == 1:
    i = hit[0]
    sys.stdout.write(u"  ‧ L%-5d|分卷宣稱 ➔ 主題宣稱（如實 %d 條）\n" % (i + 1, n14))
    add(i, L[i].index(OLD_CLAIM), L[i].index(OLD_CLAIM) + len(OLD_CLAIM), NEW_CLAIM, OLD_CLAIM)
else:
    sys.stdout.write(u"  ‧ 分卷宣稱锚命中 %d 次，不改：%s\n"
                     % (len(hit), [x + 1 for x in hit]))
    manual.append((0, OLD_CLAIM, u"锚 %d 次" % len(hit), u""))

# ── 第十五章導言之「（下）」是否亦有舊範圍說 ───────────────────────
h15 = next(i for i, s in enumerate(L) if s.startswith(u"# 第十五章"))
sys.stdout.write(u"\n===== 第十五章導言首六行（覆核有無舊分卷宣稱）=====\n")
for k in range(h15, min(h15 + 18, apx)):
    if L[k].strip():
        sys.stdout.write(u"  L%-5d|%s\n" % (k + 1, L[k][:170]))

sys.stdout.write(u"\n共 %d 處改｜須裁 %d 處\n" % (len(edits), len(manual)))
for x in manual:
    sys.stdout.write(u"  ✗ L%s|%s｜%s\n" % (x[0], x[1], x[2]))
if manual:
    sys.stdout.write(u"須裁未清，不敢寫檔。\n")
    sys.exit(1)
if not GO:
    sys.stdout.write(u"（乾跑：加 --go 始寫檔）\n")
    sys.exit(0)

byline = {}
for i, a, b, txt in edits:
    byline.setdefault(i, []).append((a, b, txt))
for i in sorted(byline, reverse=True):
    s = L[i]
    for a, b, txt in sorted(byline[i], key=lambda x: -x[0]):
        s = s[:a] + txt + s[b:]
    L[i] = s
out = u"\r\n".join(L)
BK = HP.bakpath("71d")
if not os.path.isdir(os.path.dirname(BK)):
    os.makedirs(os.path.dirname(BK))
io.open(BK, "wb").write(raw.encode("utf-8"))
for k in range(3):
    try:
        io.open(HP.SRC, "wb").write(out.encode("utf-8"))
        break
    except OSError as e:
        sys.stdout.write(u"  寫檔重試 %d：%s\n" % (k + 1, e))
        time.sleep(2)
chk = io.open(HP.SRC, "rb").read().decode("utf-8")
sys.stdout.write(u"已寫檔｜行數 %d → %d｜sha %s→%s｜回讀%s｜備份 %s\n"
                 % (len(L), chk.count(u"\r\n") + 1, old_sha,
                    hashlib.sha256(chk.encode("utf-8")).hexdigest()[:12],
                    u"全等" if chk == out else u"不等!",
                    os.path.relpath(BK, ROOT)))
