# -*- coding: utf-8 -*-
"""r166link.py —— 段際連貫體檢（第 166 輪立，**待診軸**：恆退 0，不為閘）。

緣起：第 1、2 期所治者皆在『節內』——拆超長段、解整段括號（段之形）、補『標題→內容』之
承接句（節之首）。獨『上段與下段之間有無橋』一向無器問之。本軸專問此事。

五類分報（甲乙為『缺橋』之兩向，丙丁戊為『有橋而橋劣』）：
  甲 斷崖：下段首句既無承接之形、與上段又零實詞相承；
  乙 表列之後另起論述而無橋（上段乃表或列——與第 2 期『裸表』相反之斷點）；
  丙 平列無層：同節內以『另／又／此外／其次』起首之段 ≥3（堆疊而無遞進）；
  丁 碎段如雨：同節散文段 ≥5 而段長中位 ≤40 字（骨架化之末梢）；
  戊 標點懸空：上段以冒號／分號收而下段非其所領（下無列項、亦非續行）。

豁免六桶（**先分桶再論病**——第 159 輪之教：指標不分桶則虛高，且引誘以模板語濫補）：
  子一 案例模板欄位（【事相經過】／【心相照鏡】／【佛陀處斷】／【人間智慧】與 `**【…】**` 式小標）；
  子二 逐字引文段（以「 起以 」終，或整段為『…』之書語引述）——引證製式，其橋在『：』與標界括註；
  子三 序碼起首（一、／二、／其一／甲、／①／1.）——序碼即橋；
  子四 同名標題重複五度以上之引言塊欄位（第六章百則之製式）；
  子五 詩偈與法印（四字句群以分號相聯、或『是名…』之結句）；
  子六 上下段同屬一個硬換行群（行尾兩空格相連者乃一段之續，非段際）。

口徑：印面（去底冊 `_tk.bottom_lines()`、去圍欄圖）；段＝以空行切之連續行。
承接之形唯認**句首**（句中『故』字慣用不計，免把口癖認作橋）。
重疊以 CJK 二字組計，取上段首 60 字＋末 240 字（主題詞多在段首）對下段首二句。
用法：`PYTHONPATH=. python -X utf8 _work/r166link.py [主檔副本] [--sample N] [--strict]`
      給副本即掃副本（供原病回植之負測）。
退出碼：恆 0（待診）；`--strict` 時甲乙戊合計 >0 則退 1。
"""
import io, os, re, sys, statistics, random
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as t

STRICT = '--strict' in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
OUTCSV = os.path.join(HERE, 'r166cases.csv')
SAMPLE = int(sys.argv[sys.argv.index('--sample') + 1]) if '--sample' in sys.argv else 0
SKIP = {str(SAMPLE)} if SAMPLE else set()
ARGS = [a for a in sys.argv[1:] if not a.startswith('-') and a not in SKIP]

if ARGS:
    L = io.open(ARGS[0], encoding='utf-8').read().split('\n')
    BOT = set()
    for nm in t.BOTTOM_NAMES:
        k = 0
        for i, l in enumerate(L):
            if l.startswith('# ') and nm in l:
                k = i
                break
        j = len(L)
        for i in range(k + 1, len(L)):
            if L[i].startswith('# ') and i > k:
                j = i
                break
        if k:
            BOT.update(range(k, j))
else:
    L = t.LINES
    BOT = t.bottom_lines()
N = len(L)

FEN = [False] * N
_in = False
for i, l in enumerate(L):
    if l.strip().startswith(u'```'):
        _in = not _in
        FEN[i] = True
        continue
    FEN[i] = _in
PRINT = [i for i in range(N) if i not in BOT and not FEN[i]]
PSET = set(PRINT)

CN_NUM = u'一二三四五六七八九十'
RE_LIST = re.compile(r'^\s*(?:[-*]|\d+[.)、]|[①-⓿]|[' + CN_NUM + u']{1,3}[、.)]|[' + CN_NUM +
                     u']{1,2}[一二三四五六七八九十][、.])')
RE_ENUM = re.compile(r'^\s*(?:[' + CN_NUM + r']{1,3}[、.)]|[' + CN_NUM + r']{1,2}[、.]|其[' + CN_NUM + r']|\d+[.)、])')
RE_SUBHEAD = re.compile(r'^\s*(?:>?\s*)?\**【[^】]{2,24}】\**')
RE_QUOTE = re.compile(r'^\s*[「『][^」』]{6,}[」』]\s*[。：*\s]*$')
RE_VERSE = re.compile(r'^[^\u4e00-\u9fff]*([一-鿿]{3,4}[，、；][^\n]{0,4}){2,}')


def kind(l):
    s = l.strip()
    if not s:
        return u'空'
    if s.startswith(u'|'):
        return u'表'
    if s.startswith(u'#'):
        return u'題'
    if s.startswith(u'>'):
        return u'引'
    if s.startswith(u'---') or s.startswith(u'==='):
        return u'線'
    if RE_LIST.match(s):
        return u'列'
    return u'散'


# ── 切段：連續非空行為一段（空行斷段；**標題行另立一段**——案例卡片之 `##### 小標`
#    與內文相連無空行，若併入同段則『跨節』會被誤判為『段際』，虛報百倍）──
PARAS = []
i = 0
while i < N:
    if i not in PSET or not L[i].strip():
        i += 1
        continue
    if L[i].lstrip().startswith(u'#'):           # 標題自成一體
        PARAS.append(dict(a=i, b=i, kind=u'題', txt=L[i].strip(), lines=[(i, L[i])]))
        i += 1
        continue
    j = i
    lines = []
    while j < N and j in PSET and L[j].strip() and not L[j].lstrip().startswith(u'#'):
        lines.append((j, L[j]))
        j += 1
    ks = Counter(kind(x) for _, x in lines)
    kd = ks.most_common(1)[0][0]
    body = u' '.join(x.strip().lstrip(u'># ').strip() for _, x in lines)
    body = re.sub(r'<!--[^>]*-->', u' ', body)      # SLIM 標記與 HTML 註解不入印面之判
    PARAS.append(dict(a=i, b=j - 1, kind=kd, txt=re.sub(u'\\s+', u' ', body), lines=lines))
    i = j

# ── 標題路徑與章 ──
def head_path(idx):
    h = {2: u'', 3: u'', 4: u''}
    for j in range(idx, -1, -1):
        s = L[j].strip()
        for lv in (2, 3, 4):
            pre = u'#' * lv + u' '
            if s.startswith(pre) and not h[lv]:
                h[lv] = s[len(pre):len(pre) + 26]
        if all(h.values()):
            break
    return h[2], h[3], h[4]


def chap_of(idx):
    for j in range(idx, -1, -1):
        if L[j].startswith(u'# '):
            return L[j][2:14]
    return u'卷首'


# ── 承接之形（唯認句首）──
CONN = sorted(set(u'''故 是故 是以 由是 因是 因而 於是 職是 然 然而 然則 雖然 惟 唯 夫 蓋 凡 且 況 則 而 今
此 這 那 該 既 暨 迨 及 至若 若夫 若其 如其 要之 大抵 總之 要而言之 此外 另 另外 再者 其次 再次 又 更 復 次
先 大凡 舉凡 凡此 如此 如是 如前 承上 上言 前說 自此 自是 爾時 時 彼時 方 當 適 俄而 已而 既而 未久 厥後
而後 然後 繼而 嗣是 就中 其中 其尤 其要 所以 然則 是則 且夫 至如 至若 假使 設使 或曰 客曰 或問 試言 惜乎
怪哉 嗟夫 悲夫 信夫 誠哉 固然 雖則 縱使 設令 借使 脫不 萬一 直到 直至 迨至 方其 及其 當其 適逢
二者 三者 四者 此三 此二 是三者 此二者 為此 由彼 自茲 一者 對此 於此 就此 即此 此等 此種 這般 那般
是故 故曰 夫然 雖云 縱令 設若 由是觀之 以此觀之 依此 準此 承此 本節 本章 篇末 是篇
它 本軸 此偈 是偈 偈中 前偈 後文 前文 上文 下表 上表 此表 是表 三者咬合 四者 其 彼 斯 '''.split()), key=len, reverse=True)
LISTISH = u'另外 此外 再者 其次 再次 又另 更次 次之 又次 另'.split()
STOP = set(u'之 以 而 其 者 也 於 為 則 蓋 夫 矣 焉 哉 所 與 及 或 且 然 一切 如此 如是 所謂 本書 全書'.split())
CJK2 = re.compile(u'[一-鿿]+')


def grams(s):
    """取 CJK **重疊**二字組為詞彙集。舊寫 `[一-鿿]{2}` 乃不重疊配對，
    一串 n 字只得 n//2 組，凡詞跨塊界（如「談話指針」之『指針』）即漏，
    重疊率遂系統性少算一半——虛報斷崖。（第 167 輪由 L2817 一案戳破）"""
    s = re.sub(u'[|*`#>\\-—…（）()「」『』〔〕【】《》、，。：；！？·\\s]', u'', s)
    out = set()
    for w in CJK2.findall(s):
        for k in range(len(w) - 1):
            g = w[k:k + 2]
            if g not in STOP:
                out.add(g)
    return out


def clean(s):
    return re.sub(u'[\\s|>#*\\-—]', u'', s)


def sents(s):
    return [x for x in re.split(u'[。！？]', clean(s)) if x]


def head_word(s):
    return re.sub(u'^[\\s>#*\\-—、（）()【】\\[\\]]+', u'', s.strip())[:8]


def starts_conn(s):
    h = head_word(s)
    for c in CONN:
        if h.startswith(c):
            return c
    return None


def exempt(p, q):
    """回傳豁免之桶名（無則 None）。"""
    for x, tag in ((q, u'下'), (p, u'上')):
        t2 = x['txt'].lstrip().lstrip(u'*')      # 粗體記號不掩其形：`**【…】**` 仍是小標
        if x['kind'] == u'線' or t2.strip() in (u'---', u'***', u'———'):
            return u'分隔線（有意之界）'
        if re.match(r'^◎[^\s]{0,8}$', t2.strip()):
            return u'引證標（◎原典 之類，其橋在下段之卷名）'
        if RE_SUBHEAD.match(t2):
            return u'子一小標'
        if RE_QUOTE.match(t2.strip()):
            return u'子二引文'
        if RE_ENUM.match(t2) and x is q:
            return u'子三序碼'
        if RE_VERSE.match(clean(t2)[:60]):
            return u'子五詩偈'
    h = head_word(q['txt'])
    raw0 = q['txt'].lstrip()
    raw = raw0.lstrip(u'*')            # 認標記段時先去粗體記號；留白之判仍用原形
    if raw0[:1] in u'「『（《':
        return u'子二引文或附註起首'      # 冒號領引文、表後之括注，俱屬製式而非斷崖
                                        # （須以原形判：head_word 已把行首之「（」剝去，舊誤）
    if raw.startswith(u'〔'):
        return u'子八標記段（〔◈…〕〔案：…〕自有其形制之位階）'
    if raw0.startswith(u'*') and raw0.count(u'*') == 2 and raw0.rstrip().endswith(u'*'):
        return u'子九留白與詩語（整段斜體者乃結集之語，非論述段）'
    pe = clean(p['txt'])[-3:]
    if u'？' in pe or u'?' in pe:
        return u'子七問答（上段設問、下段作答，問句即橋）'
    if pe.endswith((u'：', u':')):
        return u'子七冒號領起（其所領即下段，屬戊類之職）'
    if re.match(r'^《[^》]{2,20}》', h) or re.match(r'^[（\[?]《', h):
        return u'子六引證（上段立論、下段出處起首）'
    return None


# 子四：同名模板欄位重複五度以上
HD = Counter()
for p in PARAS:
    m = RE_SUBHEAD.match(p['txt'])
    if m:
        HD[re.sub(u'[【】*\\s]', u'', p['txt'][:20])] += 1
TPL = {k for k, v in HD.items() if v >= 5}


def is_tpl(p):
    m = RE_SUBHEAD.match(p['txt'])
    if not m:
        return False
    return re.sub(u'[【】*\\s]', u'', p['txt'][:20]) in TPL


A_JIA, A_YI, A_WU = [], [], []
for n in range(1, len(PARAS)):
    p, q = PARAS[n - 1], PARAS[n]
    if q['kind'] not in (u'散', u'引') or p['kind'] == u'題':
        continue
    if any(L[k].strip() for k in range(p['b'] + 1, q['a'])):
        continue                       # 兩段間非唯空行
    if p['b'] + 1 == q['a'] - 1 and (L[p['b']].rstrip().endswith(u'  ') or
                                     L[q['a']].startswith(u'  ')):
        continue                       # 子六：硬換行之兩端，本屬一段
    if is_tpl(p) or is_tpl(q):
        continue
    ex = exempt(p, q)
    b1s = sents(q['txt'])
    if not b1s or len(b1s[0]) < 8:
        continue                       # 過短之呼語／結句不計
    c = starts_conn(b1s[0])
    ga = grams(p['txt'][:180] + p['txt'][-260:])
    gb = grams(b1s[0] + (b1s[1] if len(b1s) > 1 else u''))
    ov = len(ga & gb)
    if ex is None:
        if p['kind'] in (u'表', u'列'):
            # 表／列之主題詞散在諸行，故取其全文（僅取頭尾則必漏，遂虛報）
            if not c and len(grams(p['txt']) & gb) < 2:
                A_YI.append((p, q, len(grams(p['txt']) & gb), c, ex))
        elif not c and (ov == 0 or (ov == 1 and len(b1s[0]) < 24)):
            A_JIA.append((p, q, ov, c, ex))
    if p['txt'].rstrip().endswith((u'：', u';', u'；')) and q['kind'] not in (u'列', u'表') \
            and head_word(q['txt'])[:1] not in u'「『（《' \
            and (ex is None or ex == u'子七冒號領起'):
        # 戊類自成一判：冒號所領若是引文、列項、小標或詩偈，屬製式；所領為另一論述段才是懸空
        A_WU.append((p, q, ov, c, ex))

# 丙／丁
sec_of = {p['a']: head_path(p['a']) for p in PARAS}
listish = defaultdict(list)
for p in PARAS:
    if p['kind'] != u'散' or is_tpl(p):
        continue
    hw = head_word(p['txt'])
    for c in LISTISH:
        if hw.startswith(c):
            listish[sec_of[p['a']]].append((p['a'] + 1, c, p['txt'][:30]))
            break
C_BING = {s: r for s, r in listish.items() if len(r) >= 3}
bypar = defaultdict(list)
for p in PARAS:
    if p['kind'] == u'散' and not is_tpl(p):
        bypar[sec_of[p['a']]].append(len(clean(p['txt'])))
D_DING = [(s, len(v), int(statistics.median(v)), min(v))
          for s, v in bypar.items() if len(v) >= 5 and statistics.median(v) <= 40]


def clip(s, n=50):
    return (s[:n] + u'…') if len(s) > n else s


def show(rows, tag, k=10):
    print(u'\n── %s：%d 處 ──' % (tag, len(rows)))
    per = Counter(chap_of(p['a']) for p, _, _, _, _ in rows)
    print(u'   分布：' + u'、'.join(u'%s %d' % (c[:6], m) for c, m in per.most_common(10)))
    pick = rows
    if SAMPLE:
        random.seed(7)
        pick = random.sample(rows, min(SAMPLE, len(rows)))
    for p, q, ov, c, ex in pick[:k]:
        print(u'   L%-6d 重疊%d 橋%s' % (q['a'] + 1, ov, c or u'無'))
        print(u'      上段末：%s' % clip(p['txt'][-58:]))
        print(u'      下段首：%s' % clip(q['txt'], 58))


def csv_dump():
    """`--csv`：一_case_一行，供逐條查證與分批套改（列：類、下段行號、重疊、橋、上段末、下段首）。"""
    import csv as _c
    out = io.open(OUTCSV, 'w', encoding='utf-8', newline='')
    w = _c.writer(out)
    w.writerow([u'類', u'下段行', u'上段行', u'重疊', u'橋', u'章', u'上段末', u'下段首'])
    for tag, rows in ((u'甲', A_JIA), (u'乙', A_YI), (u'戊', A_WU)):
        for p, q, o, c, ex in rows:
            w.writerow([tag, q['a'] + 1, p['b'] + 1, o, c or u'',
                        chap_of(q['a']), clip(p['txt'][-40:], 40), clip(q['txt'], 46)])
    out.close()
    print(u'清冊已寫：%s（%d 案）' % (OUTCSV, len(A_JIA) + len(A_YI) + len(A_WU)))


if '--csv' in sys.argv:
    csv_dump()
print(u'== 段際連貫體檢（第 166 輪立）%s ==' % (u'｜副本 ' + ARGS[0] if ARGS else u''))
print(u'印面段數：%d（散文 %d／列 %d／表 %d／引 %d／題 %d）｜模板欄位名 %d 個'
      % (len(PARAS), sum(1 for p in PARAS if p['kind'] == u'散'),
         sum(1 for p in PARAS if p['kind'] == u'列'),
         sum(1 for p in PARAS if p['kind'] == u'表'),
         sum(1 for p in PARAS if p['kind'] == u'引'),
         sum(1 for p in PARAS if p['kind'] == u'題'), len(TPL)))
show(A_JIA, u'甲 斷崖（下段無承接之形且與上段零實詞相承）', 12 if not SAMPLE else SAMPLE)
show(A_YI, u'乙 表列之後直起論述（無橋）', 8 if not SAMPLE else SAMPLE)
show(A_WU, u'戊 上段以冒號／分號收而下段非其所領', 6 if not SAMPLE else SAMPLE)
print(u'\n── 丙 平列無層（同節內『另／又／此外』式起首 ≥3 段）：%d 節 ──' % len(C_BING))
for s, rows in list(C_BING.items())[:6]:
    print(u'   %s｜%s｜%d 段' % (s[1][:14], s[2][:14], len(rows)))
    for ln, c, txt in rows[:4]:
        print(u'      L%-6d %s  %s' % (ln, c, txt))
print(u'\n── 丁 碎段如雨（同節散文段 ≥5 而中位 ≤40 字）：%d 節 ──' % len(D_DING))
for s, n2, med, mn in sorted(D_DING, key=lambda x: -x[1])[:10]:
    print(u'   段 %2d、中位 %2d、最短 %2d ｜ %s｜%s' % (n2, med, mn, s[1][:16], s[2][:16]))
tot = len(A_JIA) + len(A_YI) + len(A_WU)
print(u'\n== 段際待診合計（甲 %d＋乙 %d＋戊 %d）：%d 處；丙 %d 節、丁 %d 節 =='
      % (len(A_JIA), len(A_YI), len(A_WU), tot, len(C_BING), len(D_DING)))
if STRICT and tot > 0:
    sys.exit(1)
