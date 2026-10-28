# -*- coding: utf-8 -*-
"""257 輪・核卷尺：書中所引『卷N』是否確在其文之所在卷？——驗附錄四『卷段篇聚皆核合』之自稱。

法：本地語料六檔以卷段為檔（01-10／11-21／22-30／31-37／38-49／50-60），故檔名即卷區間之證。
    管轄有三（278）：①原典欄（律典原典／逐字回查）內的 「」 段（norm ≥ 10 字）與欄內所標之卷；
    ②同線冠卷次之引號（附錄四之表行與『「文」（卷N）』式），卷號依**字距最近**之引號為屬；
    ③同案跨載體之卷引（矩陣定位欄・地標案號列・附錄四卷段欄）須有公共檔——一案兩說即紅，
      此路不問逐字，專問歸屬（行內無引號之卷引，逐字兩尺俱不識，278 前向在尺外）。
    取上述 「」 段於語料求其落檔；書引之卷須落在同一檔之區間。
    無可證之段者列『未證』——未證不即錯，但不得援為『皆核合』之據（自稱須量得出）。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/v39volchk.py [-v] [-l 列管轄清冊]
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (ROOT, os.path.join(ROOT, u'_work')):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import _casedef as CD                                              # 276・原典欄之共器
import _tk                                                     # noqa: E402
import v39align                                                # noqa: E402

verbose = u'-v' in sys.argv
listing = u'-l' in sys.argv          # 278・列管轄清冊（宣稱之數亦是宣稱：殭尺之綠須現形）
HEAD = re.compile(u'^#### 【律典原典】\\s*$')
CARD = re.compile(u'^### 〔(案例|調部專題) (\\d+)〕')
STOP = re.compile(u'^(#{1,6} |---\\s*$)')
Q = re.compile(u'\u300c([^\\u300c\\u300d]+)\\u300d')
VOL = re.compile(u'卷\\s*\\[?([0-9]+|[一二三四五六七八九十]{1,4})\\]?')
RANGE = {u'01-10': (1, 10), u'11-21': (11, 21), u'22-30': (22, 30),
         u'31-37': (31, 37), u'38-49': (38, 49), u'50-60': (50, 60)}

FILES = []
for fn, raw, nt, nm in v39align.CORPUS:
    key = next((k for k in RANGE if k in fn), None)
    FILES.append((fn, nt, RANGE[key] if key else (0, 0)))


def where(seg):
    """歸一段落在哪幾卷區間（可多檔）。"""
    out = []
    for fn, nt, rng in FILES:
        if seg and rng[0] and nt.find(seg) >= 0:
            out.append(rng)
    return out


SRC_PATH = next((a for a in sys.argv[1:] if not a.startswith(u"-")), None)          # 274 輪・試跑通道：量假冊而不動正本
if SRC_PATH:
    LINES = io.open(SRC_PATH, encoding=u"utf-8-sig").read().split(u"\n")
else:
    LINES = _tk.MAIN_LINES
rows = []
i = 0
cur = None
while i < len(LINES):
    m = CARD.match(LINES[i])
    if m:
        cur = u'%s%s' % (m.group(1), m.group(2))
    _h3 = re.match(u'^### +(.*)$', LINES[i])
    if _h3:
        cur = _h3.group(1).strip()[:26]
    if not CD._verb_head(LINES[i]):
        i += 1
        continue
    j = i + 1
    cite = []
    quotes = []
    while j < len(LINES) and not STOP.match(LINES[j]):
        for v in VOL.findall(LINES[j]):                      # 一欄可兼引數卷（『卷三十六…兼卷四十九』）
            vv = _tk.cn_num(v) if not v.isdigit() else int(v)
            if vv:                                           # 數詞不recognised 者擲之，不令 None 入判（會當掉冒充紅燈）
                cite.append(vv)
        j += 1
    for q in Q.finditer(u'\n'.join(LINES[i + 1:j])):         # 276 續・併欄而求：一「……」可跨數行
        for part in _tk.ELL.split(q.group(1)):
            pn = _tk.norm(part)
            if len(pn) >= 10:
                quotes.append(pn)
    if cur:
        rows.append((cur, cite, quotes))
    i = j

n_lan = len(rows)

# ── 278・第二管轄：同線冠卷次之引卷宣稱（附錄四之百二格・附錄三與正文之『「文」（卷N）』式）
#   舊制只校原典欄，第六章改製（276）後欄存 14 而附錄四 102 格盡出尺外，
#   該表指針卻自稱『凡原典逐字可證者，引卷與文本所在卷段俱合』——宣稱之形未改而尺先瞎，
#   即『形制一改，諸尺各抄舊形』之又一版。
#   歸屬之口徑（負測丁所防）：一行之內，每個『卷N』歸予**字距最近之引號**（平手歸其後者），
#   故『卷三十六｜「文」』與『「文」（卷一至十）、「文2」（卷二十二至三十）』兩式俱得正屬，不復以鄰卷誤拖。
END = next((k for k, l in enumerate(LINES) if l.startswith(u'# 終卷')), len(LINES))
ENDN = next((k for k in range(END + 1, len(LINES)) if LINES[k].startswith(u'# ')), len(LINES))
for idx, l in enumerate(LINES):
    if END <= idx < ENDN or u'卷' not in l:
        continue
    qs = [(m.start(1), m.end(1), m.group(1)) for m in _tk.Q_RE.finditer(l)]
    vs = list(VOL.finditer(l))
    if not qs or not vs:
        continue
    cites = [[] for _q in qs]
    for m in vs:
        vv = _tk.cn_num(m.group(1)) if not m.group(1).isdigit() else int(m.group(1))
        if not vv:
            continue                                    # 數詞不recognised 者擲之，不令 None 入判
        pv, best, bd = m.start(), None, None
        for k, (s, e, _q) in enumerate(qs):
            d = 0 if s <= pv <= e else (s - pv if pv < s else pv - e)
            if bd is None or d < bd or (d == bd and s > pv):
                best, bd = k, d
        cites[best].append(vv)
    for k, (s, e, q) in enumerate(qs):
        cite = sorted(cites[k])
        segs = [p for p in (_tk.norm(x) for x in _tk.ELL.split(q)) if len(p) >= 10]
        if cite and segs:
            rows.append((u'L%d' % (idx + 1), cite, segs))
n_line = len(rows) - n_lan
if listing:
    for lab, cite, quotes in rows:
        print(u'  宣 %-8s 卷[%s] 段%d' % (lab, u','.join(str(c) for c in cite), len(quotes)))

# ── 278・第三路：同案跨載體之卷引須有公共檔（歸屬面之尺，不問逐字只問『一案兩說』）
#   緣起：第六章集群矩陣之定位欄自標卷段，與附錄四之卷段欄乃兩處各寫；276 改製後矩陣成主要載體，
#         其卷引向在諸尺之外（L5445 式之行內無 「」 者，逐字兩尺俱不識）。
#   口徑：一行恰含一枚『〔案例 N〕』且含『卷X』者作一處卷引；一案之諸載體所落『檔』集合須有公共元素，
#         無公共檔即判錯（兼引者自含兩卷，公共檔自存，不另設寬口）。
RANGE3 = [(1, 10), (11, 21), (22, 30), (31, 37), (38, 49), (50, 60)]
CASE1 = re.compile(u'〔案例 ?0*(\\d+)(?![0-9])')
xrow = {}
for idx, l in enumerate(LINES):
    ns = [int(x) for x in CASE1.findall(l)]
    if len(ns) != 1 or u'卷' not in l:
        continue
    vv = []
    for m in VOL.finditer(l):
        s = m.group(1)
        v = int(s) if s.isdigit() else _tk.cn_num(s)
        if v and 1 <= v <= 60:
            vv.append(v)
    if not vv:
        continue
    fs = frozenset(i for i, (a, b) in enumerate(RANGE3) for v in vv if a <= v <= b)
    xrow.setdefault(ns[0], []).append((idx + 1, fs))
xsets = {}
for n, h in xrow.items():
    common = None
    for _ln, fs in h:
        common = fs if common is None else (common & fs)
    xsets[n] = (len(h), common or frozenset())
xmulti = sum(1 for n, (k, _c) in xsets.items() if k > 1)
xempty = sorted(n for n, (_k, c) in xsets.items() if not c)
xerr = len(xempty)
for n in xempty[:6]:
    for ln, fs in xrow[n]:
        print(u'  ✗ 一案兩說：案%-4d L%-5d 檔%s' % (n, ln, sorted(RANGE3[i] for i in fs)))

agree = bad = unk = 0
print(u'宣稱 %d 處（原典欄 %d・同線冠卷次者 %d）・語料 %d 檔' % (len(rows), n_lan, n_line, len(FILES)))
for card, cite, quotes in rows:
    if not quotes:
        unk += 1
        if verbose:
            print(u'· %-8s 引卷%-4s・無可證之段（未證）' % (card, cite))
        continue
    rngs = []
    for pn in quotes:
        rngs += where(pn)
    if not rngs:
        unk += 1
        if verbose:
            print(u'· %-8s 引卷%-4s・段不可求（未證）' % (card, cite))
        continue
    hit = any(lo <= c <= hi for lo, hi in rngs for c in cite)
    if not cite:
        unk += 1
        print(u'? %-8s 宣稱未標卷次・文落 %s' % (card, sorted({(a, b) for a, b in rngs})))
    elif hit:
        agree += 1
    else:
        bad += 1
        print(u'✗ %-8s 引卷%s・其文實落 %s' % (
            card, u'／'.join(str(c) for c in cite), sorted({(a, b) for a, b in rngs})))
print(u'———— 核合 %d・不合 %d・未證 %d（未證者不得援為自稱之據）・一案兩說 %d（有卷引 %d 案，可比 %d 案）' % (
    agree, bad, unk, xerr, len(xsets), xmulti))
sys.exit(1 if (bad or xerr) else 0)
