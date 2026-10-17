# -*- coding: utf-8 -*-
# 第 180 輪·外路第二十三批『文義窒礙與段落銜接十六目』全書掃描軸（待診軸，恆退 0）。
#
# 十一目皆**有形可量**之判；凡須讀文意方能斷者一律不立（168／170 輪之教）。
# 範圍：印面（擯 `_tk.bottom_lines()`，此集為 0 起點）；圍欄圖與 HTML 註記不較。
# 出處：全冊清冊寫入 `_work/r180list.txt`，stdout 只報各目計數與首見數則。
# 本軸**永不升長檢**：乙丙丁己癸諸目所判屬文體與氣韻，升閘即以器縛文（166 輪之戒）；
#   唯甲、戊、壬、庚四目所逮屬形制與結構，可作套改之據。
import io
import re
import sys

sys.path.insert(0, u'.')
import _tk

L = _tk.LINES
CAND = sys.argv[1] if len(sys.argv) > 1 else None
if CAND:                      # 負測以副本掃之：植病須『同位換字、不增不刪行』，否则底冊豁免失準
    L = io.open(CAND, encoding=u'utf-8').read().split(u'\n')
B = _tk.bottom_lines()
OUT = u'_work/r180list.txt'


# ── 圍欄段（``` 之内不較）───────────────────────────────────────
fence, inf = [], False
for l in L:
    if l.strip().startswith(u'```'):
        inf = not inf
        fence.append(True)
        continue
    fence.append(inf)


def printable(i):
    return i not in B and not fence[i] and not l_strip(i).startswith(u'<!--')


def l_strip(i):
    return L[i].strip()


def hanc(s):
    return len(re.findall(u'[一-鿿]', s))


# ── 篇・節・款・案例之上下文 ─────────────────────────────────────
def headings():
    out = []
    for i, l in enumerate(L):
        m = re.match(u'^(#{1,6}) (.*)$', l)
        if m:
            out.append((len(m.group(1)), m.group(2).strip(), i))
    return out


HS = headings()


def enclosing(i, lvl):
    cur = u''
    for lv, t, j in HS:
        if j <= i and lv == lvl:
            cur = t
    return cur


def sect(i):
    """回傳 (章, 節) 之標題文字。"""
    return enclosing(i, 1), enclosing(i, 3)


BLOCKS = {}


def flush(key, rows):
    if rows:
        BLOCKS.setdefault(key, []).extend(rows)


roster = []


def rec(tag, i, why, txt):
    roster.append((tag, i + 1, why, re.sub(u'\\s+', u' ', txt)[:150]))


# ═════ 甲：事相經過欄內之『量刑級差科判』（問題一）═════════════════
CASE = re.compile(u'^#### 〔(遮|開|僧)(\\d+)〕')
KOPAN = re.compile(u'(未白|作白已|作白前|白竟|盡突吉羅|盡波逸提|前盡|已則盡|同一戒之|初制|二制)')
CRIME = re.compile(u'(突吉羅|波逸提|偷蘭遮|僧殘|波羅夷|越法罪)')
n_case = n_jia = 0
i = 0


def case_seg(i):
    """回傳該案『事相經過』區之行 (idx, text)；非此式者回 None。
    邊界：H4『#### 〔X N〕案名』→ 首個 H5『##### 事相經過』→ 至下一個 H5／H4 前。
    （本器初稿令 k 自 j 起算，j 自身即『##### 事相經過』故迴圈永不進入，甲己兩目遂恆報零——
      報告點名之〔遮20〕L5366 明明是病而軸不報，由此現形。）"""
    j = i + 1
    while j < len(L) and not L[j].startswith(u'#####'):
        j += 1
    if j >= len(L) or u'事相' not in L[j]:
        return None
    k = j + 1                                   # 自標題之下一行起算
    while k < len(L) and not (L[k].startswith(u'##### ') or L[k].startswith(u'#### ')):
        k += 1
    return [(x, L[x]) for x in range(j + 1, k) if printable(x) and L[x].strip()]


while i < len(L):
    m = CASE.match(L[i].strip()) if printable(i) else None
    if not m:
        i += 1
        continue
    n_case += 1
    cid = m.group(0)[5:]
    seg = case_seg(i) or []
    for x, t in seg:
        if KOPAN.search(t) and CRIME.search(t):
            n_jia += 1
            rec(u'甲·事相混科判', x, cid, t)
    i += 1


# ═════ 乙：長句之標點嵌套（問題二）═════════════════════════════════
# 尺之修（第 182 輪）：『：』『；』『——』之數**只計括號之外**——括註內之冒號（如
#   『（調查實務：舉罪五德…）』）乃列舉之領起，不淹句子主幹，舊尺連括內一併計之，
#   遂使卷首『吹哨之序』一类『一領四層、每層各附括注』之正格長句入單（**見報先疑器**）。
#   括號之巢深仍計（那是真的嵌套），句長之母數亦仍以全句漢字為準。
SENT = re.compile(u'[^。！？]*[。！？]')


def out_paren(s):
    o, d = [], 0
    for ch in s:
        if ch in u'（〔[':
            d += 1
        elif ch in u'）〕]':
            d = max(0, d - 1)
        elif d == 0:
            o.append(ch)
    return u''.join(o)


n_yi = 0
for i, l in enumerate(L):
    if not printable(i) or l_strip(i).startswith(u'|'):
        continue
    for s in SENT.findall(re.sub(u'\\s+', u'', l)):
        if hanc(s) < 100:
            continue
        bare = out_paren(s)
        colon = bare.count(u'：')
        semi = bare.count(u'；')
        dash = bare.count(u'——')
        depth = 0
        mx = 0
        for ch in s:
            if ch in u'（〔[':
                depth += 1
                mx = max(mx, depth)
            elif ch in u'）〕]':
                depth = max(0, depth - 1)
        if colon >= 2 or semi >= 3 or dash >= 2 or (mx >= 2 and (colon + semi) >= 2):
            n_yi += 1
            rec(u'乙·長句嵌套', i, u'漢%d｜外：%d｜外；%d｜外——%d｜巢%d' % (
                hanc(s), colon, semi, dash, mx), s)


# ═════ 丙：段末（或表欄末）之長辯護括註（病灶二）═══════════════════
DEFEND = re.compile(u'(蓋|便是|無異於|此亦本書|本書依|制度親手|若無則|否則即|所以然者|親手獎勵)')
CLOSE = re.compile(u'[）]\\s*[。：]?\\s*$|〕\\s*[。：]?\\s*$')
LAST = set()
prev = None
for i in range(len(L)):
    ok = (printable(i) and L[i].strip() and not L[i].startswith(u'#')
          and not fence[i] and not L[i].strip().startswith(u'|'))
    if ok:
        prev = i
    elif prev is not None:
        LAST.add(prev)
        prev = None
if prev is not None:
    LAST.add(prev)

PAIR = ((u'（', u'）'), (u'〔', u'〕'))


def match_open(s, idx):
    """自 s[idx]（閉符）回溯求其配對開符之位；本器初稿取 rfind(開符) 遂配到巢內之〔◈…〕，
    括內母數驟減而丙目恆報零——報告點名之第五章『修合別住』長括註明明在，軸卻無聲。"""
    for o, c in PAIR:
        if s[idx] == c:
            d = 0
            for k in range(idx, -1, -1):
                if s[k] == c:
                    d += 1
                elif s[k] == o:
                    d -= 1
                    if d == 0:
                        return k
    return -1


n_bing = 0
tails = []
for i in range(len(L)):
    if not printable(i) or fence[i] or not L[i].strip():
        continue
    if L[i].strip().startswith(u'|'):
        tails += [(i, c) for c in L[i].split(u'|')]          # 表欄亦段
    elif i in LAST:
        tails.append((i, L[i]))
for i, t in tails:
    s = t.rstrip(u' \t')
    if not s:
        continue
    j = len(s) - 1
    while j >= 0 and s[j] in u'。：；':
        j -= 1
    if j < 0 or s[j] not in u'）〕':
        continue
    op = match_open(s, j)
    if op < 0:
        continue
    inside = s[op:]
    if hanc(inside) >= 60 and DEFEND.search(inside):
        n_bing += 1
        rec(u'丙·段末辯護括註', i, u'括內 %d 字' % hanc(inside), s)


# ═════ 丁：元語言／說明書腔（病灶五）═══════════════════════════════
META = [u'此處不重列', u'不重列', u'不贅', u'此處但取', u'法式見', u'本款不作', u'不復重',
        u'已立，此處', u'此其本文所有', u'唯屬檢索', u'不涉閱讀次第', u'不再重', u'具載', u'說在']
n_ding = 0
cnt = {}
for i, l in enumerate(L):
    if not printable(i):
        continue
    for p in META:
        if p in l:
            cnt[p] = cnt.get(p, 0) + l.count(p)
            n_ding += l.count(p)
            rec(u'丁·元語言', i, p, l)

# ═════ 戊：節級導言之有無（病灶一）════════════════════════════════
# 判：『節（H3）』之下、首個『款（H4）』之前，除空行與『---』外別無一字者 ⇒ 零節級導言。
#   其有文字者再看首行之形：引言框【引橋】【本節法相導引】乃本書導言制（129／159 輪所補），不算病；
#   首行即表或列者，雖有節級文字而其文在表列之後，仍報候選。
#   （159 輪之教：指標須分清結構性欄位與論述斷點，否則即以模板語濫補。）
n_wu = 0
n_wu_by = {}
h3 = [(t, j) for lv, t, j in HS if lv == 3 and j not in B]
for t, j in h3:
    k = j + 1
    body, only_fence, only_tbl = [], [], []
    while k < len(L) and not L[k].startswith(u'#### '):
        if re.match(u'^#{1,3} ', L[k]):
            break
        s = l_strip(k)
        if k in B or not s or s == u'---':
            k += 1
            continue
        if fence[k]:                      # 圍欄之行本不屬『印面可讀之文』，然其為圖，須另目計之
            only_fence.append((k, s))
        elif s.startswith(u'|') or re.match(u'^[*\\-] ', s) or re.match(u'^\\d+\\. ', s):
            only_tbl.append((k, s))
        else:
            body.append((k, s))
        k += 1
    if not body:
        kind = (u'節下唯圍欄圖' if only_fence and not only_tbl else
                u'節下唯表列' if only_tbl and not only_fence else
                u'節下即款·真無一字')
        n_wu_by[kind] = n_wu_by.get(kind, 0) + 1
        n_wu += 1
        first = (only_fence or only_tbl or [(j + 1, u'（下為 H4 款題）')])[0]
        rec(u'戊·節下零過渡', first[0], kind + u'｜' + t[:26], first[1])
        continue
    x0, first0 = body[0]
    first = body[0][1]
    kind = (u'引言框（本書導言制）' if first.startswith(u'>') else
            u'散文（已有導言）' if not (first.startswith(u'|') or re.match(u'^[*\\-] ', first)
                                       or re.match(u'^\\d+\\. ', first) or first.startswith(u'#'))
            else u'其他')
    if kind == u'其他':
        n_wu_by[u'有節級文字惟首行即表列'] = n_wu_by.get(u'有節級文字惟首行即表列', 0) + 1
        n_wu += 1
        rec(u'戊·節下零過渡', body[0][0], u'有節級文字惟首行即表列｜' + t[:26], first)


# ═════ 己：合編案例之機械堆疊（病灶三）═════════════════════════════
JOIN = re.compile(u'^(另有|復有|又|次則|另一則|其後又|更別有|別有)')
n_ji = 0
i = 0
while i < len(L):
    m = CASE.match(L[i].strip()) if printable(i) else None
    if not m:
        i += 1
        continue
    cid = m.group(0)[5:]
    seg = case_seg(i) or []
    if len(seg) >= 2:
        for x, t in seg[1:]:
            if JOIN.match(t.strip()):
                n_ji += 1
                rec(u'己·合編無縫線', x, cid, t)
    i += 1

# ═════ 庚：道岔編號與閘門序號之對照（問題三）═══════════════════════
DC = re.compile(u'【道岔([一二三四五六])】（[^）]*·?閘門([一二三四五六、])[^）]*）')
dao = []
for i, l in enumerate(L):
    if not printable(i):
        continue
    for a, b in DC.findall(l):
        dao.append((a, b, i + 1))
n_geng = len(dao)
for a, b, ln in dao:
    rec(u'庚·道岔對閘門', ln - 1, u'道岔%s → 閘門%s' % (a, b), L[ln - 1])
EXPL = [p for p in (u'名目之序', u'非閘門', u'非依閘門', u'優先權限', u'編號之序', u'不必依序', u'序非閘門')
        if any(p in L[i] for i in range(len(L)) if printable(i))]
EXPL2 = []
for i, l in enumerate(L):
    if printable(i) and u'道岔' in l and re.search(u'(優先|次第|非依|不必依|其序|序號|名目之序|編號推定|以解脫|按解脫)', l):
        EXPL2.append((i + 1, re.sub(u'\\s+', u' ', l)[:88]))


# ═════ 辛：粗體記號之行內奇數（問題二『標記殘留』之實測）═══════════
n_xin = 0
for i, l in enumerate(L):
    if not printable(i) or fence[i]:
        continue
    if l.strip().startswith(u'|'):
        continue
    if l.count(u'**') % 2:
        n_xin += 1
        rec(u'辛·行內粗體落單', i, u'**%d 枚' % l.count(u'**'), l)

# ═════ 壬：列項有領無續・同層混制（問題五／病灶五之形制面）═════════
ITEM = re.compile(u'^(\\s*)([*\\-]|\\d+\\.)\\s')
n_ren_empty = 0
n_ren_mixed = 0
i = 0
while i < len(L):
    if not printable(i) or fence[i]:
        i += 1
        continue
    m = ITEM.match(L[i])
    if not m:
        i += 1
        continue
    ind, mark = len(m.group(1)), m.group(2)
    content = ind + len(mark) + len(L[i][m.end():]) - len(L[i][m.end():].lstrip()) if False else ind + len(mark) + 1
    txt = L[i]
    if re.search(u'[：:]\\s*$', txt.rstrip(u' \\t')):
        k = i + 1
        while k < len(L) and not L[k].strip():
            k += 1
        if k < len(L) and printable(k) and not fence[k] and ITEM.match(L[k]) is None:
            if len(L[k]) - len(L[k].lstrip()) < content:
                n_ren_empty += 1
                rec(u'壬·列項有領無續', i, u'縮 %d＜欄 %d' % (
                    len(L[k]) - len(L[k].lstrip()) if k < len(L) else -1, content), txt)
    i += 1
i = 0
while i < len(L):
    block = []
    while i < len(L) and printable(i) and not fence[i] and ITEM.match(L[i]):
        mm = ITEM.match(L[i])
        block.append((i, len(mm.group(1)), mm.group(2)))
        i += 1
    if len(block) >= 2:
        same = [b for b in block if b[1] == block[0][1]]
        forms = set(re.sub(u'\\d+', u'N', b[2]) for b in same)
        if len(forms) > 1:
            n_ren_mixed += 1
            rec(u'壬·同層混制', same[0][0], u'形 %s（%d 項）' % (sorted(forms), len(same)), L[same[0][0]])
    i += 1

# ═════ 子：標記行之縮排非父項內容欄（問題五之『橫插一手』形）═══════
# 合法之兩式：歸零（d=0），或恰落在某開啓中之父項內容欄（d=父.col）。
# 介乎其間者，渲染後既像上項之子、又像平行之兄——即報告所指『三階流程之後橫插同級項』之形。
n_zi = 0
st = []
for i, l in enumerate(L):
    if not printable(i) or fence[i]:
        continue
    if l.startswith(u'#'):
        st = []
        continue
    m = ITEM.match(l)
    if not m:
        continue
    d, mark = len(m.group(1)), m.group(2)
    while st and st[-1][0] >= d:
        st.pop()
    if d != 0 and (not st or st[-1][1] != d):
        n_zi += 1
        rec(u'子·標記野縮排', i, u'縮 %d｜開欄 %s' % (d, [x[1] for x in st] or u'頂層'), l)
    st.append((d, d + len(mark) + 1))


MED = re.compile(u'(大醫王|手術|動刀|拔毒|紗布|縫合|病房|急診|處方|病髮|重症|康復|出院|消毒|止血|帶膿|病灶)')
LAW = re.compile(u'(公堂|法官|審計|法袍|刑具|原告|被告|傳喚|抗辯|起訴|判決|既判|管轄|羯磨|滅擯|舉罪|白四)')
NAT = re.compile(u'(生命之樹|竹筏|風吹葉落|松風|洗鉢|挑水|燒柴|吃茶|阿蘭若|林下|泉聲|雲|[花葉]|月)')
sec_stat = {}
for i, l in enumerate(L):
    if not printable(i) or fence[i]:
        continue
    ch, se = sect(i)
    key = (ch[:12], se[:26])
    d = sec_stat.setdefault(key, [0, 0, 0, 0])
    d[0] += len(MED.findall(l))
    d[1] += len(LAW.findall(l))
    d[2] += len(NAT.findall(l))
    d[3] += hanc(l)
n_gui = 0
for (ch, se), (a, b, c, n) in sorted(sec_stat.items()):
    if a >= 3 and b >= 3 and c >= 3 and n <= 4000:
        n_gui += 1
        rec(u'癸·三族同節', 0, u'%s｜%s 醫%d 法%d 林%d 字%d' % (ch, se, a, b, c, n), u'（節級統計）')

# ═════ 出冊 ═════
with io.open(OUT, 'w', encoding=u'utf-8', newline=u'\n') as f:
    for tag, ln, why, txt in roster:
        f.write(u'%s\tL%d\t%s\t%s\n' % (tag, ln, why, txt))

print(u'第六章案例實得 %d 則' % n_case)
print(u'甲·事相欄混量刑科判：%d' % n_jia)
print(u'乙·長句（≥100 字）標點嵌套：%d' % n_yi)
print(u'丙·段末長辯護括註（≥60 字）：%d' % n_bing)
print(u'丁·元語言：%d 見｜%s' % (n_ding, sorted(cnt.items(), key=lambda x: -x[1])))
print(u'戊·標題下即墜表列（無一句承接）：%d｜分式 %s' % (n_wu, sorted(n_wu_by.items(), key=lambda x: -x[1])))
print(u'己·合編案例起首機械堆疊：%d' % n_ji)
print(u'庚·道岔對閘門 %d 組｜既有交代句之形：%s｜含『道岔』且涉序義之印面行：%d' % (n_geng, EXPL or u'無', len(EXPL2)))
for ln, t in EXPL2[:6]:
    print(u'      L%-6d %s' % (ln, t))
print(u'辛·行內粗體落單：%d' % n_xin)
print(u'壬·列項有領無續 %d｜同層混制 %d' % (n_ren_empty, n_ren_mixed))
print(u'子·標記行之野縮排：%d' % n_zi)
print(u'癸·三族意象同節俱盛之節：%d（共 %d 節有數）' % (n_gui, len(sec_stat)))
print(u'清冊：%s（%d 行）' % (OUT, len(roster)))

for tag in (u'甲', u'子', u'壬', u'癸'):
    rows = [r for r in roster if r[0].startswith(tag)]
    print(u'\n--- %s 首 12 則 ---' % tag)
    for t, ln, why, txt in rows[:12]:
        print(u'  L%-6d %-26s %s' % (ln, why, txt[:78]))
