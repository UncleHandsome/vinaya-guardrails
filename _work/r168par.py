# -*- coding: utf-8 -*-
"""r168par.py —— 列表平行性體檢（第 168 輪立，**待診軸**：恆退 0，不為閘）。

緣起：本書骨架六成是列表（`readchk` 一目：列 28.7%＋表 9.4%＋題 15.8%），歷輪諸軸問『對錯』
（欄數、成對、簡形、序號連貫），獨未問『同一個清單之內，諸項是否同一副面孔』。
項末一句一逗、項首忽標籤忽直敘，讀者於無形中要重設兩次句法——此即『不通順』之末梢。

三目（**皆只報無可置辯者**——親量之後，可量之形制病遠比想像少）：
  甲 末項未收：一個論述式清單（兄弟項多以分號相聯）之**真末項**未以句號或問號收束；
  乙 項首式不一：同塊內『**標籤**：內容』與『直敘內容』混列，且非第六章卡片之『三環』製式；
  丙 序碼混用：**同一縮排**之兄弟項雜糅標記（`1.` 與 `*` 並列）。

三目之外，歷試而撤之判（留此存照，免後人重犯）：
  · 『中段早收』（一串分號之中忽有項以句號收）**撤**——一塊之內常含數個相連之序列
    （三輯、六領域、三法式各為一串，串末自當以句號收），序列之邊界須讀文意方能定，非標點可量。
  · 末項之義取**全塊之真末項**：引文項、標題項雖不入比較，卻仍是序列之收束，
    取『剔除後之末位』會把中途分號誤當未收（初測五案全屬此誤）。
  · 序碼**按形制歸類**不按字面：`一、二、三` 是一串而非三制（`markclass()`）。

豁免（**先分桶再論病**，同 159、166 兩輪之教）：
  · 項內含直角雙引號『「…」』之逐字律文——其標點屬引文，一字動不得；
  · 領起項（以破折號或冒號收而子列續於其下）不與兄弟項較其收尾；
  · 標題項與目錄式清單（卷首導航、路線圖：項即篇題，本無句讀）；
  · 第六章卡片之『初環／次環／三環／終環』製式（標籤領起＋細節成列）；
  · 項數 < 3 之塊與同縮排項數 < 3 之序碼比較。

用法：`PYTHONPATH=. python -X utf8 _work/r168par.py [主檔副本] [--sample N] [--csv]`
退出碼：恆 0（待診）。
"""
import io, os, re, sys, random
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as t

SAMPLE = int(sys.argv[sys.argv.index('--sample') + 1]) if '--sample' in sys.argv else 0
SKIP = {str(SAMPLE)} if SAMPLE else set()
ARGS = [a for a in sys.argv[1:] if not a.startswith('-') and a not in SKIP]
HERE = os.path.dirname(os.path.abspath(__file__))
OUTCSV = os.path.join(HERE, 'r168cases.csv')

if ARGS:
    L = io.open(ARGS[0], encoding='utf-8').read().split('\n')
    BOT = set()
    for nm in t.BOTTOM_NAMES:
        k = next((i for i, l in enumerate(L) if l.startswith(u'# ') and nm in l), None)
        if k is None:
            continue
        j = next((i for i in range(k + 1, len(L)) if L[i].startswith(u'# ')), len(L))
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
PRINT = set(i for i in range(N) if i not in BOT and not FEN[i])

CN = u'一二三四五六七八九十'
RE_LBL = re.compile(r'^\**【[^】]{2,24}】\**|^(\*\*|__)[^*_]{1,44}\1\s*[：:]')
RE_QUOT = re.compile(u'「[^」]{6,}」')
RE_MARKONLY = re.compile(r'^\s*(?:[-*+]\s+|\d+[.)、]\s+|[①-⓿]\s*|['
                         + CN + r']{1,3}[、.]\s*)')


def markclass(m):
    """序碼**按形制歸類**，不按字面：`1.`／`2.` 同屬『數字』，`一、`／`二、` 同屬『漢數』，
    `①`／`②` 同屬『圈數』——否則一串『一、二、三』會被當成三種形制混用（第 168 輪之誤）。"""
    m = m.strip()
    if re.match(r'^\d+[.)、]', m):
        return u'數字'
    if re.match(r'^[' + CN + r']{1,3}[、.]', m):
        return u'漢數'
    if m and all(c in CN for c in m[:3].strip()):
        return u'漢數'          # 解析器只截到首字時（『一、』截成『一』）亦歸同類
    if re.match(r'^[①-⓿]', m):
        return u'圈數'
    return m[:1]


def indent(l):
    return len(l) - len(l.lstrip())


def parse_blocks():
    """回傳 [(起行, [項,...])]；項 = dict(mark, text, lines, sub)。"""
    blocks, i = [], 0
    while i < N:
        if i not in PRINT or not RE_MARKONLY.match(L[i]):
            i += 1
            continue
        base = indent(L[i])
        items, j = [], i
        while j < N and j in PRINT and L[j].strip():
            m = RE_MARKONLY.match(L[j])
            ind = indent(L[j])
            if m and ind <= base + 1:
                mk = L[j].strip().split(u' ', 1)[0] if u' ' in L[j].strip() else L[j].strip()[:1]
                body = L[j].strip()
                body = body[len(mk):].strip() if body.startswith(mk) else body.lstrip(u'-*+ ')
                items.append(dict(a=j, mark=mk, text=[body], sub=0, ind=indent(L[j])))
            elif items and (m or ind > base):
                if m:
                    mk2 = L[j].strip().split(u' ', 1)[0]
                    items.append(dict(a=j, mark=mk2,
                                      text=[L[j].strip()[len(mk2):].strip()],
                                      sub=1 if indent(L[j]) > base else 0,
                                      ind=indent(L[j])))
                else:
                    items[-1]['text'].append(L[j].strip())
                    if m is None and indent(L[j]) > base:
                        items[-1]['sub'] += 1
            elif not items and not m:
                break
            j += 1
        if items:
            blocks.append((i, items))
        i = max(j, i + 1)
    return blocks


CLOSE = {u'」': u'「', u'』': u'『', u'）': u'（', u')': u'(', u'】': u'【'}


def tail_class(s):
    s = s.rstrip(u' 　')
    s = re.sub(r'\*+$', u'', s).rstrip()
    # 先剝去行尾之閉合符（標界括註、案語、篇題之【】），以**內層末字**定其句讀——
    # 否則『…聽。（《卷五十七》）』與『…聽。』會被判成兩類，虛報一片。
    while s and s[-1] in CLOSE:
        k = s.rfind(CLOSE[s[-1]])
        if k < 0:
            break
        s = s[:k].rstrip()
    s = re.sub(r'\*+$', u'', s).rstrip()
    if not s:
        return u'空'
    c = s[-1]
    if c in u'。':
        return u'句'
    if c in u'；;':
        return u'分'
    if c in u'，,':
        return u'逗'
    if c in u'？?':
        return u'問'
    if c in u'：:':
        return u'冒'
    if c in u'、':
        return u'頓'
    return u'無'


def head_class(s):
    if RE_LBL.match(s):
        return u'標籤'
    if s[:1] in u'「『':
        return u'引文'
    return u'直敘'


def clip(s, n=52):
    s = re.sub(u'\\s+', u' ', s)
    return (s[:n] + u'…') if len(s) > n else s


BLOCKS = parse_blocks()
ITEMS = sum(len(b[1]) for b in BLOCKS)
HD = Counter()
for _, items in BLOCKS:
    for it in items:
        m = re.match(r'^\**【([^】]{2,24})】', it['text'][0])
        if m:
            HD[m.group(1)] += 1
TPL = {k for k, v in HD.items() if v >= 5}

A_JIA, A_YI, A_BING = [], [], []
for a, items in BLOCKS:
    if len(items) < 3:
        continue
    keep = []
    for it in items:
        t0 = it['text'][0]
        lab = re.match(r'^\**【([^】]{2,24})】', t0)
        if lab and lab.group(1) in TPL:
            continue                       # 案例模板欄位
        keep.append(it)
    for it in keep:
        b = re.sub(r'\*+$', u'', it['text'][-1].rstrip()).rstrip()
        it['rawtail'] = b[-1:] if b else u''
        it['tail'] = tail_class(u' '.join(it['text']))
        it['head'] = head_class(it['text'][0])
        it['full'] = u' '.join(it['text'])
    quotal = [it for it in keep if RE_QUOT.search(it['full'])]
    free = [it for it in keep if it not in quotal]
    # 領起項（以破折號或冒號收而子列續於其下）不與兄弟項較其收尾
    free = [it for it in free if it['rawtail'] not in (u'—', u'——') and it['tail'] != u'冒']
    # 標題項（整項即一篇題，如卷首導航之【…】）本無句讀，不入甲之比較
    def is_title(it):
        b = re.sub(r'\*+', u'', it['text'][0]).strip()
        return it['tail'] in (u'空',) or (len(re.sub(u'[\\s]', u'', b)) <= 20
                                         and not re.search(u'[。；，]', b.rstrip(u'：')))
    tit = [it for it in free if is_title(it)]
    free = [it for it in free if not is_title(it)]
    # 目錄式清單（卷首導航、路線圖）：項即篇題，本無句讀，不判甲
    lens = [len(re.sub(u'[\\s|>#*\\-—]', u'', it['full'])) for it in keep]
    if len(lens) >= 3 and (sum(1 for x in lens if x <= 20) >= 0.8 * len(lens)
                           or len(tit) >= 0.8 * len(keep)):
        free = []
    if len(free) >= 3:
        # 【規則二『中段早收』已撤（第 168 輪親量後）】：一塊之內常含**數個相連之序列**
        # （三輯、六領域、三法式各為一串，串末自當以句號收），比『同類相連之段』仍必誤判——
        # 序列之邊界須讀文意方能定，非標點可量。今唯留兩條無可置辯者：
        odd = []
        style = Counter(it['tail'] for it in free[:-1]).most_common(1)[0][0]
        # 末項須取**全塊之真末項**：引文項、標題項雖不入比較，卻仍是序列之收束——
        # 取『剔除後之末位』會把中途分號誤當未收（第 168 輪五案全屬此誤）。
        last = keep[-1]
        # 末項以冒號收者乃**領起式列項**（小標在下、其文續於更深縮排），本書通例如此，非未收
        if style in (u'句', u'分') and last['tail'] not in (u'句', u'問', u'冒'):
            last['why'] = u'全塊末項未收(%s)' % last['tail']
            odd.append(last)
        for it in free:
            if it['tail'] in (u'逗', u'頓'):
                it['why'] = u'項末%s未收' % it['tail']
                odd.append(it)
        if odd:
            A_JIA.append((a, free, style, odd))
        hc = Counter(it['head'] for it in free)
        card = any(re.match(r'^\**[（\[?]?\s*[初次三終]環', it['text'][0]) for it in keep)
        if (len(hc) > 1 and u'直敘' in hc and u'標籤' in hc and not card
                and hc[u'直敘'] * 2 < hc[u'標籤'] * 3 and hc[u'標籤'] * 2 < hc[u'直敘'] * 3):
            A_YI.append((a, free, dict(hc)))
    # 序碼之比較**限同一縮排**（父子巢狀本用不同形制：父作 `1.`、子作 `*`，非混用）
    byi = defaultdict(list)
    for it in keep:
        byi[it.get('ind', 0)].append(it)
    for ind, its in sorted(byi.items()):
        if len(its) < 3:
            continue
        mk = Counter(markclass(it['mark']) for it in its)
        if len(mk) > 1:
            A_BING.append((a, dict(mk), ind, its[0]['a']))

print(u'== 列表平行性體檢（第 168 輪立）%s ==' % (u'｜副本 ' + ARGS[0] if ARGS else u''))
print(u'列塊 %d 個、列項 %d 條｜模板欄位名 %d 個' % (len(BLOCKS), ITEMS, len(TPL)))


def show(rows, tag, k):
    print(u'\n── %s：%d 塊 ──' % (tag, len(rows)))
    pick = rows
    if SAMPLE:
        random.seed(11)
        pick = random.sample(rows, min(SAMPLE, len(rows)))
    for row in pick[:k]:
        a, items, top, odd = row if len(row) == 4 else (row[0], row[1], row[2], [])
        print(u'   L%-6d 主流『%s』異類 %d 項（共 %d 項）' % (a + 1, top, len(odd), len(items)))
        for it in (odd[:3] if odd else items[:3]):
            print(u'      [%s/%s·%s] %s' % (it['mark'], it['tail'], it.get('why', u''),
                                            clip(it['full'], 44)))


show(A_JIA, u'甲 項末標點不一', 10 if not SAMPLE else SAMPLE)
print(u'\n── 乙 項首式不一（標籤與直敘混列）：%d 塊 ──' % len(A_YI))
for a, items, hc in (A_YI[:8] if not SAMPLE else random.sample(A_YI, min(SAMPLE, len(A_YI)))):
    print(u'   L%-6d %s' % (a + 1, hc))
    for it in items[:4]:
        print(u'      [%s] %s' % (it['head'], clip(it['full'], 46)))
print(u'\n── 丙 同縮排序碼混用：%d 處 ──' % len(A_BING))
for a, mk, ind, first in A_BING[:10]:
    print(u'   塊L%-6d 縮排 %d、首項 L%-6d %s' % (a + 1, ind, first + 1, mk))
if '--csv' in sys.argv:
    with io.open(OUTCSV, 'w', encoding='utf-8', newline='') as fh:
        w = csv_writer = __import__('csv').writer(fh)
        w.writerow([u'目', u'塊起行', u'項行', u'主流', u'其由', u'內有句號', u'項末', u'標記', u'內容'])
        for a, items, top, odd in A_JIA:
            for it in odd:
                inner = re.sub(r'\*+', u'', it['full']).strip()
                w.writerow([u'甲', a + 1, it['a'] + 1, top, it.get('why', u''),
                            u'有' if u'。' in inner[:-1] else u'無',
                            it['tail'], it['mark'], clip(it['full'], 70)])
        for a, items, hc in A_YI:
            for it in items:
                w.writerow([u'乙', a + 1, it['a'] + 1, str(hc), u'', u'-', it['tail'], it['head'],
                            clip(it['full'], 70)])
    print(u'清冊已寫：%s' % OUTCSV)
print(u'\n== 合計：甲 %d 塊、乙 %d 塊、丙 %d 塊 ==' % (len(A_JIA), len(A_YI), len(A_BING)))
