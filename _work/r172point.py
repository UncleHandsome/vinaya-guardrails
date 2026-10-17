# -*- coding: utf-8 -*-
"""r172point.py —— 方位指針之可達性體檢（第 172 輪立，**待診軸**：恆退 0，不為閘）。

緣起：歷輪 `anchorref` 校章名篇名之死鏈、`claimnum` 校宣稱之項數、166 輪校段際之橋，
皆未問『上表／下表／如左／上列／本圖』一类**方位指針**其所指之物是否真在讀者目力可及之處。
本書經百余輪搬移增刪，最易生之病即『指針仍在、所指已遷』——**紙上隔一節之『上表』於螢幕無礙、
於書則誤人**（螢幕可滾，紙上須回翻）。

口徑（第 172 輪四度修尺之後定讞，皆『先疑其報而後疑文』）：
  · 距量須取**至該形最近一行**（非塊首）——長表動輒數十行，指針若在其下之凡例塊內，
    量至塊首即虛報數百行（初測『本表在 365 行前』即此誤）；
  · 判病唯取**越節**（指針與所指之間隔一標題）與**查無**（其方向全書無此形）兩條——
    同節之內隔幾段領起之文乃正格，非病；『太遠若干行』須讀文意方能定跨頁與否（跨頁屬產物層），
    依 168、170、171 之教**不設行數之界**（初設 6／24 行，虛報十筆）；
  · 須辨**切位**：『該表決』『上列表』『見表下』之『表』屬他詞（表決／列表／表下）；
    『前段／後段』在此書乃**案例之前後段**（〔開18〕『前段無心開許、後段行淫極刑』），非段落之指；
  · **inline 自足**：指針同句之內已列三項（以『、』『；』或〔案例代號〕相羅）者，其所指即在此句。

目：甲 向後領起而所領在別節；乙 向前回顧而所指在別節；丙 就地自指而十二行內無其形；丁 查無。
豁免：底冊（附錄C／K／L／M／終卷）、圍欄圖內、卷首目錄區、「」引號與『』書語、〔〕標界之內。
用法：`PYTHONPATH=. python -X utf8 _work/r172point.py [主檔副本] [--csv] [--show N]`
退出碼：恆 0（待診）。
"""
import io, os, re, sys, csv
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as t

SHOW = int(sys.argv[sys.argv.index('--show') + 1]) if '--show' in sys.argv else 40
ARGS = [a for a in sys.argv[1:] if not a.startswith('-') and not a.isdigit()]
HERE = os.path.dirname(os.path.abspath(__file__))
OUTCSV = os.path.join(HERE, 'r172cases.csv')

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

TOC = set()
_toc = False
for i, l in enumerate(L):
    if re.match(u'^#{1,3}.*(目錄|目次)', l.strip()):
        _toc = True
        continue
    if _toc and l.startswith(u'# ') and i > 4:
        _toc = False
    if _toc:
        TOC.add(i)


def kind(i):
    s = L[i].strip()
    if not s:
        return u'空'
    if s.startswith(u'|') and u'|' in s[1:]:
        return u'表'
    if s.startswith(u'#'):
        return u'題'
    if s.startswith(u'>'):
        return u'引'
    if s in (u'---', u'***', u'———'):
        return u'線'
    if re.match(u'^\\s*([-*]|\\d+[.)、]|[①-⓿]|[（(][一二三四五六七八九十\\d]+[）)])\\s*[*\\[]?', s):
        return u'列'
    return u'文'


KIND = [kind(i) for i in range(N)]
FORM = {u'表': set(i for i in range(N) if KIND[i] == u'表'),
        u'圖': set(i for i in range(N) if FEN[i] or L[i].strip().startswith(u'```')),
        u'列': set(i for i in range(N) if KIND[i] in (u'列', u'表', u'引'))}

# 指針表：(詞, 形, 向)；向 f=所指在後、b=所指在前、s=就地自指
PTR = [(u'下表', u'表', u'f'), (u'上表', u'表', u'b'), (u'前表', u'表', u'b'),
       (u'後表', u'表', u'f'), (u'如表', u'表', u'f'), (u'表下', u'表', u'b'),
       (u'見表', u'表', u'f'), (u'本表', u'表', u's'), (u'此表', u'表', u's'),
       (u'上列', u'列', u'b'), (u'前列', u'列', u'b'), (u'下列', u'列', u'f'),
       (u'後列', u'列', u'f'), (u'如下', u'列', u'f'), (u'如上', u'列', u'b'),
       (u'見上', u'列', u'b'), (u'詳見下', u'列', u'f'), (u'如左', u'表', u'f'),
       (u'上圖', u'圖', u'b'), (u'下圖', u'圖', u'f'), (u'前圖', u'圖', u'b'),
       (u'本圖', u'圖', u's'), (u'此圖', u'圖', u's'), (u'本卡', u'列', u's'),
       (u'此卡', u'列', u's')]
SKIPW = {u'詳見下', u'如左', u'本卡', u'此卡', u'如上'}
NEXT_BAD = {u'表': set(u'決示揚彰格明率面'), u'列': set(u'表'), u'圖': set(u'片譜')}
PRE_BAD = {u'表下': set(u'見說詳'), u'見表': set(u'說')}   # 『說見表下〔案外如實〕』所指乃標界案語，非表塊
QIN = re.compile(u'「[^」]*」')
QOUT = re.compile(u'『[^』]*』')
BRQ = re.compile(u'〔[^〕]*〕')
INLINE = re.compile(u'、[^、、：]{2,}、[^、、：]{2,}|；[^；；]{4,}；|(?:〔[^〕]{1,6}〕){3}')


def segs_at(txt, pos):
    """取指針所在之句中、指針其後之言（至本句末）。"""
    hi = len(txt)
    for x in u'。！？':
        k = txt.find(x, pos + 1)
        if k >= 0:
            hi = min(hi, k + 1)
    return txt[pos:hi]


def near(idx, form, direction):
    pool = FORM[form]
    if not pool:
        return None, None
    if direction == u's':
        return min(abs(p - idx) for p in pool), None
    if direction == u'f':
        cand = [p for p in pool if p > idx]
        return (min(cand) - idx, min(cand)) if cand else (None, None)
    cand = [p for p in pool if p < idx]
    return (idx - max(cand), max(cand)) if cand else (None, None)


def crossed(a, b):
    lo, hi = sorted((a, b))
    return any(KIND[x] == u'題' for x in range(lo, hi + 1))


def chap_of(idx):
    for j in range(idx, -1, -1):
        if L[j].startswith(u'# '):
            return L[j][2:14]
    return u'卷首'


def sec_of(idx):
    for j in range(idx, -1, -1):
        s = L[j].strip()
        for lv in (4, 3, 2):
            p = u'#' * lv + u' '
            if s.startswith(p):
                return s[len(p):len(p) + 26]
    return u''



# ── 紙面之距：頁數與每頁字數俱向產物量取（守則㉗，不手抄常數）──
CJK_ALL = re.compile(u'[\u4e00-\u9fff]')


def pdf_pages(path):
    try:
        import pymupdf as fitz
    except Exception:
        return None
    try:
        d = fitz.open(path)
        n = d.page_count
        d.close()
        return n
    except Exception:
        return None


PDF = os.path.join(os.path.dirname(HERE), u'_print', u'ver38_列印版.pdf')
PAGES = pdf_pages(PDF)
ZI = sum(len(CJK_ALL.findall(l)) for i, l in enumerate(L) if i in PRINT)
FALLBACK = 600.0                      # 無冊可读時之保守下界（寧嚴勿寬，不令本軸自閉）
PAGE_ZI = (ZI / PAGES) if PAGES else FALLBACK
CUM = [0] * (N + 1)
for _i in range(N):
    CUM[_i + 1] = CUM[_i] + (len(CJK_ALL.findall(L[_i])) if _i in PRINT else 0)


def zdist(a, b):
    lo, hi = sorted((a, b))
    return CUM[hi + 1] - CUM[lo + 1] if hi > lo else 0


print(u'[法源] 印面漢字 %d｜冊頁 %s｜每頁約 %.0f 字%s'
      % (ZI, PAGES, PAGE_ZI,
         u'' if PAGES else u'（冊不可讀，退用保守下界 %.0f——判病不自閉）' % FALLBACK))

rows = []
NEAR = []
for i in sorted(PRINT):
    if i in TOC:
        continue
    s = QIN.sub(u'', QOUT.sub(u'', BRQ.sub(u'', L[i])))
    if not s.strip():
        continue
    for w, form, d in PTR:
        p = s.find(w)
        if p < 0:
            continue
        if s[p + len(w):p + len(w) + 1] in NEXT_BAD.get(form, set()):
            continue
        if s[max(0, p - 1):p] in PRE_BAD.get(w, set()):
            continue
        if w in SKIPW:
            continue          # 款級指針歸 anchorref、卡級自指歸體例、『如上』乃虛指非形塊
        if d in (u'f', u'b') and INLINE.search(segs_at(s, p)):
            continue                      # 本句之內、指針之後即自列其所指，不必另尋其形
        gap, tgt = near(i, form, d)
        if gap is None:
            rows.append((u'丁查無', i, w, form, None, u'其方向全書無' + form))
        elif d == u's':
            z = zdist(min(FORM[form], key=lambda q: abs(q - i)), i)
            if PAGE_ZI and z > PAGE_ZI:
                rows.append((u'丙失所', i, w, form, z, u'%s 而一頁之內無其' % w + form))
        elif crossed(i, tgt):
            z = zdist(i, tgt)
            if PAGE_ZI and z <= 1.5 * PAGE_ZI:
                NEAR.append((i, w, form, z))
            elif PAGE_ZI and z > 1.5 * PAGE_ZI:
                rows.append((u'甲隔頁' if d == u'f' else u'乙隔頁', i, w, form, z,
                             u'%d 行／%d 字%s有' % (gap, z, u'後' if d == u'f' else u'前')
                             + form + u'而中隔標題（逾一頁半）'))

print(u'[報而不治] 越節而同頁（回指前節之末表，正格之承接）：%d 筆；其最遠 %s 字'
      % (len(NEAR), max([x[3] for x in NEAR]) if NEAR else 0))
print(u'方位指針可達性：可疑 %d 筆（底冊、圍欄、目錄、引號、書語、標界、切位、inline 俱免）' % len(rows))
for k, m in Counter(r[0] for r in rows).most_common():
    print(u'   %s：%d' % (k, m))
for r in rows[:SHOW]:
    print(u'  [%s] L%-6d %s｜%s' % (r[0], r[1] + 1, r[2],
                                    re.sub(u'\\s+', u' ', L[r[1]])[:72]))
    print(u'         %s｜%s／%s' % (r[5], chap_of(r[1])[:8], sec_of(r[1])[:22]))
if '--csv' in sys.argv:
    with io.open(OUTCSV, 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh)
        w.writerow([u'目', u'行', u'指針', u'形', u'距', u'說', u'章', u'節', u'原行'])
        for r in rows:
            w.writerow([r[0], r[1] + 1, r[2], r[3], r[4], r[5], chap_of(r[1]),
                        sec_of(r[1]), re.sub(u'\\s+', u' ', L[r[1]])[:120]])
    print(u'清冊已寫：%s' % OUTCSV)
print(u'\n== 合計：%d 筆（甲 %d、乙 %d、丙 %d、丁 %d）==' % (
    len(rows), sum(1 for r in rows if r[0].startswith(u'甲')),
    sum(1 for r in rows if r[0].startswith(u'乙')),
    sum(1 for r in rows if r[0].startswith(u'丙')),
    sum(1 for r in rows if r[0].startswith(u'丁'))))
