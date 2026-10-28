# -*- coding: utf-8 -*-
"""《佛陀的護欄》全書結構與引文校驗（本輪重建）。

甲 章序：H1「第X章」須 一→N 各現一次且單調；
乙 節序：每章「### 一、二、…」自一起、逐格加一；
丙 目錄對正文：每章 TOC 之節題、樞紐題與案例題須與正文相當（去標點與空白後比）；
丁 三段式：每個「#### 案例」須具【引文行】、【案發現場】、【防禦靶點】、【行為心理剖析】；
戊 引文閘：條文行與【案發現場】區內之「」片段，折異體去標點後須為律藏連寫子串（以「……」分段）；
己 圍欄「」」必成對。
壬 【律制】欄（案例卡之逐字欄，凡例款②）：去括註、以「……」分段後，每段必為律藏連寫子串（硬）。
癸 出處篇聚名（【案發現場（…）】與十線地圖篇聚欄）須為本地二十犍度之實目（硬）。
已知豁免：末章（現代指南）之案例不引律文，只列不判。
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import os
import re
import sys

sys.path.insert(0, ".")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import _tk  # noqa: E402
import hlpara  # noqa: E402  共器：印面段落之模型・中間層之形
import lane  # noqa: E402   共器：律文欄之形制＋款①式樣之判別（辛丁與降式樣之刀同此法源）

BOOK = os.environ.get("HULAN_CHK") or HP.SRC
raw = io.open(BOOK, encoding="utf-8", newline="").read()
assert raw.count("\n") == raw.count("\r\n"), u"孤 LF"
L = raw.split(u"\r\n")
U = u"零一二三四五六七八九十"
PUNC = re.compile(u"[，、：；。（）「」『』…—·\\s\\*]")
errs, warns = [], []


def cn2int(s):
    if len(s) == 1:
        return U.index(s)
    if s.startswith(u"十"):
        return 10 + (U.index(s[1]) if len(s) == 2 else 0)
    if s.endswith(u"十"):
        return U.index(s[0]) * 10
    if len(s) == 3 and s[1] == u"十":
        return U.index(s[0]) * 10 + U.index(s[2])
    return None


def key(s):
    return PUNC.sub(u"", s)


chs = []
for i, l in enumerate(L):
    m = re.match(u"^# 第([一二三四五六七八九十]{1,3})章\\s", l)
    if m:
        chs.append((i, cn2int(m.group(1))))
seq = [c[1] for c in chs]
print(u"甲 章題 %d 個：%s → %s" % (len(chs), seq[:3], seq[-3:]))
if seq != list(range(1, len(chs) + 1)):
    errs.append(u"【甲】章序不連貫：%s" % seq)
bounds = []
for k, (i, n) in enumerate(chs):
    bounds.append((n, i, chs[k + 1][0] if k + 1 < len(chs) else len(L)))

for n, a, b in bounds:
    got = [cn2int(m.group(1)) for m in (re.match(u"^### ([一二三四五六七八九十]+)、", l) for l in L[a:b]) if m]
    if got != list(range(1, len(got) + 1)):
        errs.append(u"【乙】第%s章 節序 %s" % (n, got))

toc_end = next(i for i, l in enumerate(L) if l.startswith(u"# 【全書詳細目錄】"))
body_start = next(i for i, l in enumerate(L) if l.startswith(u"# 第一章"))
LAYER = hlpara.LAYER        # 共器（_work/hlpara.py）：四名一支，`tocsync` 同此——形制一改只改一處
toc_items, cur, inb = {}, None, False
for l in L[toc_end:body_start]:
    m = re.match(u"^\\* \\*\\*第([一二三四五六七八九十]{1,3})章 ", l)
    if m:
        cur = cn2int(m.group(1))
        toc_items[cur] = []
        inb = False
        continue
    if cur is None:
        continue
    m = re.match(u"^\\s+\\* (案例[一二三四五六七八九十]+：.*)$", l)
    if m:
        toc_items[cur].append(u"c" + key(m.group(1)))
        inb = False
        continue
    # 中間層（第 57 輪『第N樞紐』、第 65 輪『第N陣地』、第 66 輪『第N板塊』與『第N重鎮』：正文作 H3『### 【第N…：…】』、
    # 目錄作『* **【…】**』）。此層須與案例同入配對，否則其條目落進『別式』之 C 而正文各題落進 s，
    # 全章案例隨之錯位一名（形制一改，尺先學新形——第 57 輪之帳）。
    m = re.match(u"^\\s+\\* \\*\\*(" + LAYER + u".*】)\\*\\*$", l)
    if m:
        toc_items[cur].append(u"C" + key(m.group(1)))
        continue
    # 別式：節題（縮二）含「案例」者起，其下同層（縮四）之連列即該章之案例清單
    # （第十章、第十二章之目錄不書「案例N：」而直列案題，前式之尺數不到，便成『0 項／正文 N 項』之假缺）。
    m = re.match(u"^\\s{2}\\* ([一二三四五六七八九十]+、.*案例.*)$", l)
    if m:
        toc_items[cur].append(u"s" + key(m.group(1)))
        inb = True
        continue
    m = re.match(u"^\\s{4}\\* (?!案例)(.+)$", l)
    if m and inb:
        toc_items[cur].append(u"C" + key(m.group(1)))
        continue
    if re.match(u"^\\s{2}\\* ", l):
        inb = False
    m = re.match(u"^\\s{2}\\* (尾聲：.*)$", l)
    if m and cur is not None:
        toc_items[cur].append(u"s" + key(m.group(1)))
        continue
    m = re.match(u"^\\s{2}\\* ([一二三四五六七八九十]+、.*)$", l)
    if m:
        toc_items[cur].append(u"s" + key(m.group(1)))
for n, a, b in bounds:
    body = []
    for l in L[a:b]:
        m = re.match(u"^### (.*)$", l)
        if m:
            body.append((u"C" if re.match(LAYER, m.group(1))
                         else u"s") + key(m.group(1)))
            continue
        m = re.match(u"^#### (案例[一二三四五六七八九十]+：.*)$", l)
        if m:
            body.append(u"c" + key(m.group(1)))
    tb = toc_items.get(n, [])
    ts = [x for x in tb if x[0] == u"s"]
    bs = [x for x in body if x[0] == u"s"]
    tc = [x for x in tb if x[0] in (u"c", u"C")]
    bc = [x for x in body if x[0] in (u"c", u"C")]
    if len(ts) != len(bs):
        errs.append(u"【丙】第%s章 節數 %d/%d（目錄／正文）" % (n, len(ts), len(bs)))
    elif len(tc) != len(bc):
        warns.append(u"【丙】第%s章 目錄案例 %d 項／正文 %d 項（目錄或以別式列名）" % (n, len(tc), len(bc)))
    for x, y in zip(ts, bs):          # 目錄得為正文之省寫，取前綴相當
        if not (y.startswith(x) or x.startswith(y)):
            warns.append(u"【丙】第%s章 目錄「%s」與正文「%s」字面有異" % (n, x[:26], y[:26]))
    # 案例級：舊尺只數其多寡不比其文字，遂令目錄與內文各說各話（第七批外審之實害）。
    # 今一律以正文為準——目錄之案例題須與「#### 案例N：」逐字合（_work/tocsync.py 專職覆蓋）。
    # 樞紐級同此：目錄之『* **【第N樞紐…】**』須與正文之『### 【第N樞紐…】』同層同字面。
    for x, y in zip(tc, bc):
        if x[0] != y[0]:
            errs.append(u"【丙】第%s章 目錄『%s』與正文『%s』不同層（案例／中間層錯序）"
                        % (n, x[1:26], y[1:26]))
        elif x[1:] != y[1:]:
            errs.append(u"【丙】第%s章 目錄案例「%s」與正文「%s」不合" % (n, x[1:26], y[1:26]))
print(u"丙 逐章比對：%d 章節數相符（共 %d 章）" %
      (len(seq) - len([e for e in errs if u"【丙】" in e]), len(seq)))

Q = re.compile(u"「(.+?)」", re.S)
QB = re.compile(u"「\\*\\*(.+?)\\*\\*」", re.S)
ncase = ntri = 0
vh = vm = vn = vnm = vv = 0        # 逐字之數／無據；戒文行之地數／無據；白話引文之數
misses = []
for n, a, b in bounds:
    blk = L[a:b]
    idx = [i for i, l in enumerate(blk) if l.startswith(u"#### 案例")] + [len(blk)]
    for k in range(len(idx) - 1):
        seg = blk[idx[k]:idx[k + 1]]
        ncase += 1
        need = [u"> **【", u"* **【案發現場", u"* **【防禦靶點", u"* **【行為心理剖析"]
        miss = [p for p in need if not any(l.startswith(p) for l in seg)]
        if miss:
            (warns if n == max(seq) else errs).append(
                u"【丁】第%s章 %s 缺 %s" % (n, seg[0][:20], u",".join(miss)))
        else:
            ntri += 1
        for l in seg:
            if l.startswith(u"> **【"):
                t = re.sub(u"^> \\*\\*【[^】]*】：\\*\\*\\s*", u"", l)
                for frag in re.split(u"…+", t):
                    nm = _tk.norm(key(frag))
                    if len(nm) < 4:
                        continue
                    vn += 1
                    if nm not in _tk.VINAYA:
                        vnm += 1
                        misses.append((n, u"戒文省寫", frag[:46]))
        j0 = next((x for x, l in enumerate(seg) if l.startswith(u"* **【案發現場")), None)
        j1 = next((x for x, l in enumerate(seg) if l.startswith(u"* **【防禦靶點")), len(seg))
        if j0 is None:
            continue
        zone = u"\n".join(seg[j0:j1])
        allq = [m.group(1) for m in Q.finditer(zone)]
        # 全書另有 **「…」」式（粗體包引號）之自稱逐字：舊口徑只看「」內之 **，遂漏此式。
        boldq = [m.group(1) for m in re.finditer(u"\\*\\*「([^」]+)」", zone)]
        for c in allq:
            for i, part in enumerate(c.split(u"**")):
                if i % 2 == 0:                 # 偶數段為白話轉寫，不閘
                    continue
                for frag in re.split(u"…+", part):
                    nm = _tk.norm(key(frag))
                    if len(nm) < 4:
                        continue
                    vh += 1
                    if nm not in _tk.VINAYA:
                        vm += 1
                        misses.append((n, u"逐字引文", frag[:46]))
        vv += sum(1 for c in allq if u"**" not in c)
        for c in boldq:                            # **「…」」＝整段自稱逐字，全段入閘
            for frag in re.split(u"…+", c):
                nm = _tk.norm(key(frag))
                if len(nm) < 4:
                    continue
                vh += 1
                if nm not in _tk.VINAYA:
                    vm += 1
                    misses.append((n, u"逐字引文（粗體包引號）", frag[:46]))
print(u"丁 案例 %d 則｜三段式完備 %d" % (ncase, ntri))
print(u"戊 逐字引文（「**…**」）%d 段，語料無據 %d｜白話引文 %d 段（不閘）｜戒文行 %d 段，非連寫 %d"
      % (vh, vm, vv, vn, vnm))
for n, zone, q in misses:
    print(u"    第%s章｜%s｜%s" % (n, zone, q))
if vm:
    errs.append(u"【戊】自稱逐字之引文有 %d 段於語料無據" % vm)

# 庚：有署名之題詞引文（章首／卷首之 blockquote ＋「—— 出處」行）。此類之逐字與否由**署名**背書，
#     與案例區內「粗體即背書」是兩制；舊尺兩頭都不管，遂令偽託逐字（第十六章大迦葉語）與偽託名人
#     （第十七章弘一題詞）一路過關。署《四分律》者入語料閘；署他師他典者語料無從證，一律列「須人工核」。
apx0 = next((i for i, l in enumerate(L) if l.startswith(u"# 附錄")), len(L))
LIT = re.compile(u"四分律|波羅夷法|僧殘法|拘睒彌|揵度|犍度|律藏")
OTH = re.compile(u"弘一|道宣|元照|資持記|行事鈔|尼鈔|法句經|中阿含|阿姜查|涅槃經|大智度|俱舍|善見")
ATT = re.compile(u"^>?\\s*——\\s*(.+)$")
DISC = re.compile(u"義引|大意|義譯|括其旨|括旨|擄其旨|非逐字|無此文|無此句|無文|今訳"
                  u"|本書括旨|未及逐覆|非其書之句|非其經之句")
# 第 56 輪・學術嚴謹版：他師之引語若附大正藏編號（T…n…卷…篇），即為『可檢索之逐字引』，
# 不強求『義引』式標記——此形制比舊標記更嚴：讀者可按號直查，查無即紅在紙上。
CANON = re.compile(u"T\\d{2,4}n\\d{3,4}")
g_in = g_out = g_bad = g_canon = g_disc = 0
att_lines = set()                           # 有署名題詞所佔之行（辛軸不複報）
i = 0
while i < apx0:
    if not L[i].startswith(u">"):
        i += 1
        continue
    j = i
    while j < apx0 and (L[j].startswith(u">") or not L[j].strip()):
        j += 1
    reg = L[i:j]
    att = u""
    for k, l in enumerate(reg):
        m = ATT.match(l.strip())
        if m:
            att = m.group(1).strip()
            reg = reg[:k] + reg[k + 1:]
            break
    if att:
        att_lines.update(range(i, j))
        q = re.sub(u"[>＊*｜`]", u"", u"".join(reg))
        for frag in re.split(u"…+", q):
            for piece in re.findall(u"「([^」]+)」", frag) or [frag]:
                nm = _tk.norm(key(piece))
                if len(nm) < 6:
                    continue
                if OTH.search(att):
                    g_out += 1
                    if CANON.search(att):
                        g_canon += 1
                        warns.append(u"【庚】他師逐字引・附大正藏編號可檢索：%s｜%s"
                                     % (att[:22], nm[:34]))
                    elif DISC.search(att):
                        g_disc += 1
                        warns.append(u"【庚】他師他典題詞已標『如實』（括旨／未及逐覆），語料無從證真偽：%s｜%s"
                                     % (att[:22], nm[:34]))
                    else:
                        errs.append(u"【庚】他師他典題詞掛逐字式樣而未如實標記"
                                    u"（須〔本書括旨〕／未及逐覆／或大正藏編號 T…n…）：%s｜%s"
                                    % (att[:22], nm[:34]))
                elif LIT.search(att):
                    g_in += 1
                    if nm not in _tk.VINAYA:
                        g_bad += 1
                        errs.append(u"【庚】署名律藏而語料無據：%s｜%s" % (att[:22], nm[:44]))
    i = max(j, i + 1)
print(u"庚 署名題詞：律藏入閘 %d 段（無據 %d）｜他師他典 %d 段（其中附大正藏編號可檢索 %d・括旨如實標 %d・未標即硬錯）"
      % (g_in, g_bad, g_out, g_canon, g_disc))

# 辛：無署名而作律文句法之粗體引文（案例區外）。此類不掛出處，卻以「若比丘…」「世尊…」之經體
#     自稱律文——第四章「以十利故，與諸比丘結戒」即如是漏網（律文實作「集十句義」）。
#     判準須用句法而非「有無粗體」：書中「」兼作術語標記，凡以粗體包術語者不勝枚舉，一律入閘必報百條偽陽性。
LITSTYLE = re.compile(u"若比丘|世尊|爾時|諸比丘|結戒|波逸提|婆尸沙|不共住|波羅夷|僧伽梨|式叉迦羅尼|突吉羅|羯磨")
in_case = set()
for n, a, b in bounds:
    blk = L[a:b]
    ci = [i for i, l in enumerate(blk) if l.startswith(u"#### 案例")] + [len(blk)]
    for k in range(len(ci) - 1):
        in_case.update(range(a + ci[k], a + ci[k + 1]))
BQ = re.compile(u"「\\*\\*(.+?)\\*\\*」|\\*\\*「([^」]+)」\\*\\*", re.S)
x_in = x_bad = 0
seen_x = set()                              # 同一引文可跨多行重複出現，去重後逐段全收
buf = []
for i in range(apx0):
    if i in in_case or i in att_lines:      # 有署名之題詞歸庚管，此處不複報
        buf = []
        continue
    buf.append(L[i])
    txt = u"\n".join(buf[-6:])
    got = [m.group(1) or m.group(2) for m in BQ.finditer(txt)]
    if not got:
        continue
    buf = []                                 # 收完即棄，免同段再入下一窗
    for q0 in got:                           # 舊版只取首段即 break，一段多引則漏報
        q = re.sub(r"\s+", u"", q0)
        if not LITSTYLE.search(q) or re.search(u"[A-Za-z]", q):
            continue                            # 附梵巴轉寫者乃術語標記，非引文
        for frag in re.split(u"…+", q):
            nm = _tk.norm(key(frag))
            if len(nm) < 6 or nm in seen_x:
                continue
            seen_x.add(nm)
            x_in += 1
            if nm not in _tk.VINAYA:
                x_bad += 1
                errs.append(u"【辛】律文句法之自稱逐字於語料無據：L%d｜%s" % (i + 1, nm[:44]))
print(u"辛 案例區外律文句法之自稱逐字：%d 段入閘（無據 %d）" % (x_in, x_bad))

# 辛乙：散文裡「某律師／某祖師／某師在《某鈔》中指出：**「…」**」——此類不掛「——」題詞行，
#        舊庚不管；又無律文句法，舊辛亦不管。第七批外審即由此路入（元照、道宣擬古文三處）。
ATT2 = re.compile(u"律師|祖師|大師|尊者|元照|道宣|弘一|資持記|行事鈔|比丘尼鈔|法句經|中阿含|阿姜")
y_in = y_bad = 0
for i in range(apx0):
    if i in in_case or i in att_lines:
        continue
    for m in lane.PIN.finditer(L[i]):            # 同款①式樣，形制判別共器（免抄本＋免 `\*` 之escape警告）
        q0 = m.group(1) or m.group(2)
        # 須是本行「某人／某書 ＋ 冒號 ＋ 引文」之式，方算自稱祖師逐字；
        # 本書術語（如『城郭宮殿之喻』『七葉窟五百結集』）之粗體引號不在此列（前版取±2行之寬，即報七條偽陽性）。
        head = L[i][:m.start()]
        if not ATT2.search(head) or u"：" not in head or DISC.search(head):
            continue
        for frag in re.split(u"…+", re.sub(r"\s+", u"", q0)):
            t2 = _tk.norm(key(frag))
            if len(t2) < 6 or re.search(u"[A-Za-z]", t2) or t2 in _tk.VINAYA:
                continue
            y_in += 1
            y_bad += 1
            errs.append(u"【辛乙】以他師他典名義自稱逐字而未標如實：L%d｜%s" % (i + 1, t2[:44]))
print(u"辛乙 散文牽他師他典之自稱逐字：%d 段入閘（未如實標記 %d）" % (y_in, y_bad))

# 辛丁（軟報・如實列數）：款①之式樣（「」與粗體相合）而語料無據、又無律文句法者——
#   此類讀來像律文，實為本書評語借律文之式樣（如『意志力是一種……有限資源。』）。
#   硬檢會報百條偽陽性（『』兼作術語標記），故只印數與樣例，候作者裁：甲＝降其式樣，
#   乙＝改款①之約（明言『「」＋粗體唯律文，評語改用粗體或『』』）。第 62 輪自抓：59 段中
#   有 2 段確係律句而無標脫字（L5378 脫『瞻視』・L5955 脫『若裹時』），已補；其餘 57 段屬此縫。
LIT4 = lane.LIT            # 律文句法之判：名源共器 `lane`（降式樣之刀同取，免兩抄本）
NV4 = lane.corpus_flat()
z_in = z_soft = 0
z_lit = []
z_dem = []
for i in range(apx0):
    for m in lane.PIN.finditer(L[i]):
        q0 = (m.group(1) or m.group(2) or u"").strip()
        lit4, ping = lane.pin_kind(q0, NV4)
        z_in += len(lit4) + len(ping)
        for f in lit4:
            z_lit.append(u"L%d｜%s" % (i + 1, f[:34]))
        for f in ping:
            z_soft += 1
            z_dem.append((i + 1, m.start(), f[:40]))
if z_lit:
    errs.append(u"【辛丁】款①式樣・含律文句法而語料無據（須補字或標『……』）：" + u"　".join(z_lit[:4]))
warns.append(u"【辛丁】款①式樣而語料無據・屬本書評語者：%d 段（評語借律文式樣之縫・候裁：降式樣或改款①）"
             % z_soft)
print(u"辛丁 款①式樣無據：律句 %d（硬檢）・評語 %d（軟報）" % (len(z_lit), z_soft))
if z_dem and u"-v" in sys.argv:                 # 軟報亦須點名（第 74 輪：無名之軟報即無尺）
    seen = set()
    for i, c, f in z_dem:
        if (i, f) in seen:
            continue
        seen.add((i, f))
        print(u"    △ L%-5d 偏移%s｜%s" % (i, c, f))
# 壬：案例卡之【律制】欄＝凡例款②所定之逐字欄。戊軸把『戒文行不連寫』只記成軟報（條文行多带（律釋）括註，
#     不得不軟），遂開一縫：第 57 輪之外來新稿 27 條【律制】有 12 條係『省字而不標省略』或『兩處之語接龍』，
#     全數走過。此欄無括註之由，故改硬：先取「…」內之文，再以「……」分段，逐段（≥6 字）必為律藏連寫子串。
LZ = re.compile(u"^> \\*\\*【律制】：\\*\\*\\s*(.*)$")
PAR = re.compile(u"[（(][^（()）]*[)）]")
lz_in = lz_bad = 0
for i in range(apx0):
    m = LZ.match(L[i])
    if not m:
        continue
    for q in re.findall(u"『?「([^」]+)」", PAR.sub(u"", m.group(1))):
        for frag in re.split(u"…+", q):
            t2 = _tk.norm(key(frag))
            if len(t2) < 6:
                continue
            lz_in += 1
            if t2 not in _tk.VINAYA:
                lz_bad += 1
                errs.append(u"【壬】【律制】欄自稱律文而語料無據：L%d｜%s" % (i + 1, t2[:44]))
print(u"壬 【律制】欄逐字：%d 段入閘（無據 %d）" % (lz_in, lz_bad))
# 癸：出處欄之篇聚名須為本地《四分律》之實目。第 57 輪之實害：新稿與十線地圖以『結界／和尚／瞻病／授戒犍度』
#     為篇題（本地二十犍度無此四目），另兩處所標篇聚與律文實位不符（『五法授人大戒』在雜犍度、象師黑石蜜在戒本）。
#     口徑只掃『出處之位』（案例卡之【案發現場（…）】與十線地圖之篇聚欄），不掃散文——散文多云指，非歸屬宣稱。
KDU = set(u"受戒 說戒 安居 自恣 皮革 衣 藥 迦絺那衣 拘睒彌 瞻波 呵責 覆藏 遮 破僧 滅諍 "
          u"比丘尼 法 房舍 雜".split())
ROW = re.compile(u"^\\| 第[一二三四五六七八九十]+章案例[^|]*\\| ([^|]+) \\|")
k_in = k_bad = 0
for i in range(apx0):
    m = re.match(u"^\\s*\\* \\*\\*【案發現場（(.+?)）】", L[i])
    row = m.group(1) if m else (ROW.match(L[i]) and ROW.match(L[i]).group(1))
    if not row:
        continue
    for x in re.findall(u"([一-龥]{1,7})犍度", row):
        if x == u"二十":                      # 『二十犍度』係總稱，非篇題
            continue
        k_in += 1
        if x not in KDU:
            k_bad += 1
            errs.append(u"【癸】出處篇聚名本地無此目：L%d｜%s犍度" % (i + 1, x))
print(u"癸 出處篇聚名：%d 枚入閘（非本地篇題 %d）" % (k_in, k_bad))
inf, nopen = False, 0
for l in L:
    if l.startswith(u"```"):
        nopen += not inf
        inf = not inf
if inf:
    errs.append(u"【己】圍欄未成對")
print(u"己 圍欄 %d 段%s" % (nopen, u"（俱成對）" if not inf else u"（有未閉者）"))
print(u"=== 硬檢 %d 項｜豁免 %d 項" % (len(errs), len(warns)))
for e in errs:
    print(u"  ×" + e)
for w in warns:
    print(u"  ·" + w)
sys.exit(1 if errs else 0)
