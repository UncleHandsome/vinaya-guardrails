# -*- coding: utf-8 -*-
"""《佛陀的護欄》全書結構與引文校驗（本輪重建）。

甲 章序：H1「第X章」須 一→N 各現一次且單調；
乙 節序：每章「### 一、二、…」自一起、逐格加一；
丙 目錄對正文：每章 TOC 之節題與案例題須與正文相當（去標點與空白後比）；
丁 三段式：每個「#### 案例」須具【引文行】、【案發現場】、【防禦靶點】、【行為心理剖析】；
戊 引文閘：條文行與【案發現場】區內之「」片段，折異體去標點後須為律藏連寫子串（以「……」分段）；
己 圍欄「」」必成對。
已知豁免：末章（現代指南）之案例不引律文，只列不判。
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import os
import re
import sys

sys.path.insert(0, ".")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import _tk  # noqa: E402

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
            body.append(u"s" + key(m.group(1)))
            continue
        m = re.match(u"^#### (案例[一二三四五六七八九十]+：.*)$", l)
        if m:
            body.append(u"c" + key(m.group(1)))
    tb = toc_items.get(n, [])
    ts = [x for x in tb if x[0] == u"s"]
    bs = [x for x in body if x[0] == u"s"]
    tc = [x for x in tb if x[0] in (u"c", u"C")]
    bc = [x for x in body if x[0] == u"c"]
    if len(ts) != len(bs):
        errs.append(u"【丙】第%s章 節數 %d/%d（目錄／正文）" % (n, len(ts), len(bs)))
    elif len(tc) != len(bc):
        warns.append(u"【丙】第%s章 目錄案例 %d 項／正文 %d 項（目錄或以別式列名）" % (n, len(tc), len(bc)))
    for x, y in zip(ts, bs):          # 目錄得為正文之省寫，取前綴相當
        if not (y.startswith(x) or x.startswith(y)):
            warns.append(u"【丙】第%s章 目錄「%s」與正文「%s」字面有異" % (n, x[:26], y[:26]))
    # 案例級：舊尺只數其多寡不比其文字，遂令目錄與內文各說各話（第七批外審之實害）。
    # 今一律以正文為準——目錄之案例題須與「#### 案例N：」逐字合（_work/tocsync.py 專職覆蓋）。
    for x, y in zip(tc, bc):
        if x[0] == u"c" and x[1:] != y[1:]:
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
DISC = re.compile(u"義引|大意|義譯|括其旨|括旨|擄其旨|非逐字|無此文|無此句|無文|今訳")
g_in = g_out = g_bad = 0
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
                    if not DISC.search(att):
                        errs.append(u"【庚】他師他典題詞掛逐字式樣而未如實標記（須義引／大意／義譯／括旨／無文）：%s｜%s"
                                    % (att[:22], nm[:34]))
                    else:
                        warns.append(u"【庚】他師他典題詞已標『如實』，語料無從證真偽：%s｜%s"
                                     % (att[:22], nm[:34]))
                elif LIT.search(att):
                    g_in += 1
                    if nm not in _tk.VINAYA:
                        g_bad += 1
                        errs.append(u"【庚】署名律藏而語料無據：%s｜%s" % (att[:22], nm[:44]))
    i = max(j, i + 1)
print(u"庚 署名題詞：律藏入閘 %d 段（無據 %d）｜他師他典 %d 段（須帶如實標記，未帶即硬錯）" % (g_in, g_bad, g_out))

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
    for m in re.finditer(u"「\*\*(.+?)\*\*」|\*\*「([^」]+)」\*\*", L[i], re.S):
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
