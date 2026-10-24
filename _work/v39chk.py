# -*- coding: utf-8 -*-
"""ver39 查核公約（第 254 輪立）：三十九版之形制與數目不變量，一跑一行。

緣起：`_tk.py check` 與 52 軸之錨俱指 ver38 字面（附錄 A–M、四欄卡、133 綁定點……），
      新冊不可援舊綠為證，亦不可遽以舊紅判冊病——故另立此尺。
口徑：範圍＝印面（唯擯卷首目錄區與『終卷』之後）；圍欄內之形制病另目；名單須斷非空。
退碼：任一 FAIL 即退 1（依 120 輪之通則：凡以 rc 為閘者須先負測）。

用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/v39chk.py [自訂源檔路徑]
"""
import io
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, '_work'))
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, NAME)
LINES = io.open(PATH, encoding=u'utf-8').read().split(u'\n')
F = u'\n'.join(LINES)

import contextlib

import _casedef as CD            # noqa: E402  276・案號定義載體之唯一法源
with contextlib.redirect_stdout(io.StringIO()):               # recordsimp 於匯入時自印一行，非本尺之聲
    import recordsimp
from _simpdict import MAP as _SD                            # noqa: E402  全書尺之緊口徑（384 枚）

# 簡形之名單今合兩張字典（第 263 輪）：舊尺唯用 `_simpmap.S`（233 枚），名單之外之
# 『动・无・价・经・脱・过・项・让』八枚歷輪無報（今以 `_work/r263simp.py` 量得而盡改）。
# 凡該簡形實見於本地語料者（并・谷・余 之類，乃律文舊形照錄）自動豁免，不假手名冊。
CORP = set()
for _f in glob.glob(os.path.join(ROOT, u'原文', u'*.txt')):
    CORP |= set(io.open(_f, encoding=u'utf-8', errors=u'ignore').read())
SIMP = (set(recordsimp.S) | set(u'两当强随旧总')
        | (set(_SD) - {c for c in _SD if c in CORP}))
assert len(SIMP) > 400, u'簡形名單不可為空且須覆兩帳（今 %d 枚）' % len(SIMP)

RES = []


def chk(name, fails, detail=u''):
    RES.append((name, list(fails), detail))


def blocks(txt):
    """以空行・標題・表列・圍欄為界之『段』清單（回傳 (起行索引, [行])）。"""
    out, cur, start = [], [], 0
    inf = False
    for i, l in enumerate(txt.split(u'\n')):
        if l.strip().startswith(u'```'):
            inf = not inf
        if inf:
            continue
        if (cur and (l.strip() == u'' or l.startswith(u'#') or l.strip().startswith(u'|')
                     or l.strip().startswith(u'---'))):
            out.append((start, cur))
            cur = []
        if not cur and l.strip() and not l.strip().startswith(u'|'):
            start = i
        if l.strip():
            cur.append(l)
    if cur:
        out.append((start, cur))
    return out


FENCE = []
_open = None
for i, l in enumerate(LINES):
    if l.strip().startswith(u'```'):
        if _open is None:
            _open = i
        else:
            FENCE.append((_open, i))
            _open = None
INFENCE = set()
for a, b in FENCE:
    INFENCE |= set(range(a, b + 1))
BODY0 = next((i for i, l in enumerate(LINES) if l.startswith(u'# 第一章')), 0)
Toc0 = next((i for i, l in enumerate(LINES) if l.startswith(u'## 【全書開卷標準目錄】')), 0)
END = next((i for i, l in enumerate(LINES) if l.startswith(u'# 終卷')), len(LINES))
ENDN = next((i for i in range(END + 1, len(LINES)) if LINES[i].startswith(u'# ')), len(LINES))


def in_print(i):
    """印面＝除卷首目錄區、除『終卷』本節（不印）、除圍欄。『終卷』之後之附錄俱在印面。"""
    return not (Toc0 <= i < BODY0) and not (END <= i < ENDN) and i not in INFENCE


def in_page(i):
    """紙面＝凡印得出來的行，**含圍欄之內**。
       269 輪之負測現形：形制之禁（黑話／官僚代號／無號指針／某某令）若只掃 `in_print`，
       圍欄內那 562 行便成被豁免之一側而無人守——而圍欄之文照樣在紙上（第 134 輪『版面之病只能用版面量』同科）。
       凡以**詞形**為鑰之禁，一律用本閘；凡以 **markdown 記號**為鑰之禁（粗體・行末空格）仍用 `in_print`。"""
    return not (Toc0 <= i < BODY0) and not (END <= i < ENDN)


# ── 1・2：案號與補遺之編序（案號定義之唯一法源＝`_CD.case_defs`，276 第六章改製後有四形載體）
DEFN = CD.case_defs(LINES)
nums = sorted(DEFN)
chk(u'案例編號連貫', [] if nums == list(range(1, len(nums) + 1)) else [u'%d 枚不連貫' % len(nums)],
    u'今 %d 枚（矩陣 %d・地標 %d・標題 %d・卡 %d）' % (
        len(nums), sum(1 for v in DEFN.values() if v[u'形'] == u'矩陣'),
        sum(1 for v in DEFN.values() if v[u'形'] == u'地標列'),
        sum(1 for v in DEFN.values() if v[u'形'] == u'標題'),
        sum(1 for v in DEFN.values() if v[u'形'] == u'卡')))
buyi = [int(m.group(1)) for m in re.finditer(u'(?m)^### 〔補遺 (\\d+)〕', F)]
chk(u'補遺卡編序（29–44 除 36）',
    [] if sorted(buyi) == [n for n in range(29, 45) if n != 36] else [u'%s' % sorted(buyi)],
    u'今 %d 枚' % len(buyi))
# ── 3・案之載體（旧目『每卡六欄』：276 量得卡形定義 0 枚，該分支空轉，故連卡題・六欄・導航之舊循環俱刪）
bad2 = [(DEFN[n][u'行'], u'%s 案無名' % n) for n in nums if not DEFN[n][u'名']]
NAV_RE = re.compile(u'^\\s*\\*+\\s*\\*{0,2}法相導航')
for i in [k for k, x in enumerate(LINES)
          if re.match(u'^### 【(經典地標深描|雙螺旋對照專題)', x)]:
    j = next((k for k in range(i + 1, len(LINES)) if LINES[k].startswith(u'### ')), len(LINES))
    seg = LINES[i:j]
    tag = u'地標' if u'經典地標' in LINES[i] else u'雙螺旋'
    if tag == u'地標' and not any(NAV_RE.match(x) for x in seg):     # 雙螺旋以『代表判例・物理表業・主觀意志』為欄，不較導航
        bad2.append((i + 1, u'%s無導航欄：%s' % (tag, LINES[i][4:22])))
    if not any(u'案例' in x for x in seg):                          # 案號須可追溯：題內・子題・案號列皆可
        bad2.append((i + 1, u'%s無案號可追：%s' % (tag, LINES[i][4:22])))
chk(u'案之載體（有名・地標有導航・案號可追溯）', bad2)

# ── 3：指針可達
cardset = set(nums)
dead = sorted({int(m.group(1)) for m in re.finditer(u'〔案例 ?(\\d{1,3})〕', F)} - cardset)
chk(u'案例指針可達', [(u'指向無此卡：%s' % d,) for d in dead])
dead2 = sorted({int(m.group(1)) for m in re.finditer(u'〔補遺 ?(\\d+)〕', F)} - set(buyi))
chk(u'補遺指針可達', [(u'指向無此卡：%s' % d,) for d in dead2])

# ── 4：分批提示與舊帳
PROMPT = [u'交付完畢', u'下回預告', u'共十二回', u'次對話', u'隨時準備接續推進', u'本回',
          u'發布完畢', u'修訂藍圖', u'工程藍圖']
chk(u'分批產出提示零殘留',
    [(u'『%s』%d 見' % (k, F.count(k)),) for k in PROMPT if F.count(k)])
OLDL = re.findall(u'〔(?:遮|開|僧)\\d+〕', F)
chk(u'舊帳案號零殘留', [(u'%d 見' % len(OLDL),)] if OLDL else [])

# ── 5：簡形（引號外・印面）
hit = [(i + 1, w) for i, l in enumerate(LINES) if in_print(i)
       for w in sorted(set(re.sub(u'『[^』]*』', u'', re.sub(u'「[^」]*」', u'', l))) & SIMP)]
chk(u'印面引號外無簡形', hit)

# ── 6・7：段內括號平衡與星號成對
PAIRS = [(u'（', u'）'), (u'〔', u'〕'), (u'「', u'」'), (u'『', u'』'), (u'《', u'》'), (u'【', u'】')]
bad = []
for st, bl in blocks(F):
    if not in_print(st):
        continue
    t = u''.join(bl)
    for a, b in PAIRS:
        if t.count(a) != t.count(b):
            bad.append((u'%s%s' % (a, b), bl[0][:24]))
    tt = re.sub(u'⁽[^⁾]*⁾', u'', u'\n'.join(
        re.sub(u'^\\s*(?:>\\s*)*\\*\\s+', u'', x) for x in bl)).replace(u'\\*', u'')
    odd = [q for q, on in ((u'星號奇數', tt.count(u'*') % 2),
                           (u'粗體不成對', tt.count(u'**') % 2)) if on]
    if odd:
        bad.append((u'・'.join(odd), bl[0][:24]))
chk(u'段內六族括號平衡・粗體記號成對', bad)

# ── 8：標題不懸空（H1–H4）
hs = [(len(m.group(1)), i) for i, l in enumerate(LINES)
      if (m := re.match(u'^(#{1,4})\\s', l)) and in_print(i)]
bad = []
for k, (lv, i) in enumerate(hs):
    nxt = next((j for _l, j in hs[k + 1:] if _l <= lv), len(LINES))
    body = [x for x in LINES[i + 1:nxt] if x.strip() and x.strip() != u'---']
    if not body:
        bad.append((i + 1, LINES[i][:34]))
chk(u'H1–H4 標題不懸空', bad)

# ── 9：目錄雙向
def key(s):
    s = re.sub(u'（.*?）', u'', s, flags=re.S)
    return re.sub(u'[《》「」『』〔〕【】（）·：:，,、／/\\s#*➔\\-—]', u'', s)[:14]
toc = [key(l) for l in LINES[Toc0:BODY0] if re.match(u'^\\s+\\* ', l)]
h13 = [key(l.lstrip(u'#')) for i, l in enumerate(LINES)
       if re.match(u'^#{1,3} ', l) and not (Toc0 <= i < BODY0)]
chk(u'目錄不指空', [(x,) for x in toc if x and x not in set(h13)])

# ── 10・11：章級與節級指針
ch_titles = [l for i, l in enumerate(LINES) if l.startswith(u'# 第') and in_print(i)]
nch = len({re.match(u'^# 第([一二三四五六七八九])章', t).group(1) for t in ch_titles})
secs = {}
cur = None
for i, l in enumerate(LINES):
    if not in_print(i):
        continue
    if l.startswith(u'# '):
        m = re.match(u'^# 第([一二三四五六七八九十]+)章', l)
        cur = u'第%s章' % m.group(1) if m else None
        if cur:
            secs.setdefault(cur, set())
    m = re.match(u'^### 第([一二三四五六七八九十]+)節', l)
    if m and cur:
        secs[cur].add(m.group(1))
bad = []
for m in re.finditer(u'第([一二三四五六七八九])章第([一二三四五六七八九十]+)節', F):
    c = u'第%s章' % m.group(1)
    if c not in secs:
        bad.append((u'無此章：%s' % c,))
    elif m.group(2) not in secs[c]:
        bad.append((u'%s 無第%s節' % (c, m.group(2)),))
#   270 輪加網・**蒙上省寫**：『第八章第二節**與第四節**』省其章名（中文常形，非病），而第 10 目只認
#   『第N章第M節』全形，故省寫之後項**向在網外**。今按同句（至下一個句號）追其章，核其節序可達；
#   該章不以節為序者（第三章以閘門為序・第六章以組為序）如實報「節制不合」，不強判落空亦不默過。
def _ord(x):                                              # 漢字序數之值（display 用，非判準）
    u5 = u'一二三四五六七八九十'
    if x in u5:
        return u5.index(x) + 1
    if x.startswith(u'十'):
        return 10 + (u5.index(x[1]) + 1 if len(x) > 1 else 0)
    if u'十' in x:
        a, b = x.split(u'十', 1)
        return (u5.index(a) + 1 if a else 1) * 10 + (u5.index(b) + 1 if b else 0)
    return 99

ELLIP = 0
for i, l in enumerate(LINES):
    if not in_print(i):
        continue
    for m in re.finditer(u'第([一二三四五六七八九])章第([一二三四五六七八九十]+)節', l):
        c = u'第%s章' % m.group(1)
        tail = l[m.end(): (l.index(u'。', m.end()) + 1) if u'。' in l[m.end():] else len(l)]
        for t in re.finditer(u'[、與及或，]{1,3}第([一二三四五六七八九十]+)節', tail):
            if re.search(u'第[一二三四五六七八九]章', tail[:t.start()]):
                continue                                   # 後項已另冠章名
            ELLIP += 1
            if not secs.get(c):
                bad.append((u'L%d 省寫『第%s節』・%s 不以節為序（節制不合）' % (
                    i + 1, t.group(1), c),))
            elif t.group(1) not in secs[c]:
                bad.append((u'L%d 省寫落空：%s 無第%s節（今有 %s）' % (
                    i + 1, c, t.group(1), u'・'.join(sorted(secs[c], key=_ord))),))
chk(u'章節指針可達（章級與節級，含蒙上省寫）', sorted(set(bad)),
    u'章 %d・節表 %d 章・省寫 %d 處' % (nch, len(secs), ELLIP))

# ── 12：自報之數可校
CLAIM = [(u'案例卡數', len(nums), 102), (u'補遺則數', len(buyi), 15),
         (u'章數', nch, 8), (u'閘門數', len(set(re.findall(u'### 閘門([一二三四五六])', F))), 6),
         (u'正理數', len(set(re.findall(u'正理([一二三四五六七八])：', F))), 8)]
bad = [(u'%s：實 %d 宣 %d' % (n, a, b),) for n, a, b in CLAIM if a != b]
for m in re.finditer(u'(\\d+) 則判例|(\\d+) 個判例單元|全章 (\\d+) 案', F):
    v = int(next(g for g in m.groups() if g))
    if v != len(nums):
        bad.append((u'書面宣稱 %d 則而實 %d 則' % (v, len(nums)),))
chk(u'自報之數與實測相符', sorted(set(bad)))

# ── 13・14・15：印面形制
bad = [(i + 1, LINES[i][:40]) for i in INFENCE
       if u'**' in LINES[i] and not (END <= i < ENDN) and not (Toc0 <= i < BODY0)]
chk(u'圍欄內無 markdown 粗體記號', bad)
bad = [(i + 1,) for i, l in enumerate(LINES)
       if in_print(i) and (len(l) - len(l.rstrip(u' '))) == 1
       and not re.match(u'^\\s*(?:>\\s*)+$', l)]      # 『> 』空引行只一枚空格乃引用塊之正寫法
chk(u'印面行末不是一枚空格（零或兩枚硬換行）', bad)
bad = [(i + 1, LINES[i][:34]) for i, l in enumerate(LINES)
       if in_print(i) and re.match(u'^#{1,5} ', l) and re.search(u'[。；，、：]\\s*$', l)]
chk(u'標題行末不帶句讀', bad)
bad = [(i + 1,) for i, l in enumerate(LINES)
       if in_print(i) and l.strip() in (u'---', u'***') and i and LINES[i - 1].strip()]
chk(u'分隔線前有空行（防 setext 劫持）', bad)
bad = [(i + 1, l[:40]) for i, l in enumerate(LINES) if in_print(i)
       and re.search(u'（）|〔〕|「」|『』|【】|\\[\\]', re.sub(u'^\\s*\\|', u'', l))]
chk(u'印面無空殼括號', bad)

# ── 16：篇題之數自校
bad = []
for i, l in enumerate(LINES):
    if in_print(i) and l.startswith(u'# ') and u' appendix' not in l:
        m = re.match(u'^# 附錄六　.*十五則', l)
        if m and len(buyi) != 15:
            bad.append((u'篇題稱十五則而實 %d' % len(buyi),))
chk(u'篇題之數與篇內實列相符', bad)

# ── 17・18：語料殘跡（本輪回填之兩道新敞口）
# 合字一處現存於附錄三（語料作『阿[少/兔]樓陀』，正字㝹屬 ext-A，是否入印面，候作者裁決）；餘者不容新漏
BRACKET_EXC = set([u'[少/兔]'])                            # 唯附錄三『阿[少/兔]樓陀』一行（Anuruddha）
bad = [(i + 1, m.group(0)) for i, l in enumerate(LINES) if in_print(i)
       for m in re.finditer(u'\\[[^\\]\\s]{1,3}[*\\/][^\\]\\s]{1,3}\\]', l)
       if m.group(0) not in BRACKET_EXC or not l.lstrip().startswith(u'|')]
chk(u'印面無 CBETA 組字碼（除已立案之合字一處）', bad)
bad = [(i + 1, l[:34]) for i, l in enumerate(LINES) if in_print(i)
       and l.count(u'\u300e') != l.count(u'\u300f')]
chk(u'行內 『』 成對（回填不得留下單之語料引號）', bad)
bad = [(i + 1, m.group(0)) for i, l in enumerate(LINES) if in_print(i)
       for m in re.finditer(u'[0-9]{1,2}-[0-9]{1,2}(?![0-9])', l)      # 277 放寬：裸檔名區間（不待『卷』字相隨）亦禁
       if not l[:m.start()].rstrip(u'（(' ).endswith(u'卷段')
       and u'卷段' not in l[max(0, m.start() - 14):m.start()]]        # 「大正藏卷段 50-60」乃本書既定之定位式，放行
bad += [(i + 1, m.group(0)) for i, l in enumerate(LINES) if in_print(i)
        for m in re.finditer(u'[0-9]{1,2}-[0-9]{1,2}\\s*\u5377', l)]     # 語料檔名區間非讀者語
chk(u'印面無檔名式引卷（『01-10卷段』之類須作漢字卷段）', bad)
bad = [(i + 1, l[:40]) for i, l in enumerate(LINES) if in_print(i)
       and re.search(u'\u5f8b\u610f\uff1a.*\u300c|\u300c[^\u300d]*\u5f8b\u610f\uff1a', l)]
chk(u'『律意』之攝述與「逐字」之掛引號不相雜', bad)

# ── 24：產器不得硬寫冊身之數（封面之宣稱須自書身算出）
BP = os.path.join(ROOT, u'_print', u'build39.py')
bt = io.open(BP, encoding=u'utf-8').read() if os.path.exists(BP) else u''
bad = []
if bt:
    if u'cov-meta">__META__' not in bt:
        bad.append((u'封面之數未自算（cov-meta 模板缺 __META__，恐已硬寫）',))
    for m in re.finditer(u'cov-meta">([^<]{0,60})', bt):
        if u'__META__' not in m.group(1) and m.group(1).strip():
            bad.append((u'封面行仍硬寫：%s' % m.group(1)[:34],))
else:
    bad.append((u'產器不可讀（缺尺即無尺）',))
chk(u'封面之數自書身算出（產器不硬寫）', bad)

# ── 25：附錄四一案一行（其表頭自稱『一案一行・匯自定義載體』，須量得出）
a4 = next((i for i, l in enumerate(LINES) if l.startswith(u'# 附錄四')), None)
a5 = next((i for i in range(a4 + 1, len(LINES)) if LINES[i].startswith(u'# 附錄五')), len(LINES)) if a4 else 0
r4 = set()
for l in (LINES[a4:a5] if a4 else []):
    if l.startswith(u'|'):
        for m in re.finditer(u'\u3014\u6848\u4f8b ?(\\d+)\u3015', l):
            r4.add(int(m.group(1)))
bad = []
if not a4:
    bad.append((u'附錄四不可見',))
else:
    if len(r4) != len(nums):
        bad.append((u'表列案號 %d 個 ≠ 定義 %d 枚' % (len(r4), len(nums)),))
    if sorted(set(nums) - r4):
        bad.append((u'表中缺案：%s' % sorted(set(nums) - r4)[:8],))
    if sorted(r4 - set(nums)):
        bad.append((u'表有定無：%s' % sorted(r4 - set(nums))[:8],))
chk(u'附錄四一案一行（行數＝案數・號號相當）', bad, u'今 %d 行' % len(r4))

# ── 26：印面命題不作行政『令』（第 267 輪・外路第八案之裁）
#   判準：作者叮囑讀者者曰『警策』，僧團對事所立者曰『禁約』（叢林原生語），
#         『某某令』乃官府軍政公文之形，與本冊『大醫王隨病設藥』之聲口相乖。
LINGLE = re.compile(u'(?:\\*\\*|【)[^*【】\\n]{2,18}令(?:\\*\\*|】|：)')
bad = [(i + 1, m.group(0)[:30]) for i, l in enumerate(LINES) if in_page(i)
       for m in [LINGLE.search(l)] if m]
chk(u'印面命題不作『某某令』（對讀者曰警策・對事曰禁約）', bad)

# ── 27：案號與案名之對合（第 266 輪立・第 267 輪放寬兩網眼）
#   判準（窄，免以描述語為病）：內聯『〔案例NN〕某某』之引名，若與**本號卡題**之最長共同子串 ≤1 字，
#   卻與**他卡卡題**共同 ≥5 字，則必是號錯（或名錯）——描述性短語（如『取官木私建重閣』）雖不合題，
#   因無另一卡與之更合，故不報。口徑一變即須重標基線，勿據舊數判事。
#   267 輪放寬：① 號前**容許一枚空格**（『〔案例 89〕』式全書 283 見向在網外）；
#             ② **卷首亦掃**（今時五病灶對讀索引即在卷首，舊以 `i < BODY0` 一筆擲去全卷首）。
#   放寬後基線：內聯可判 443 處・報 0（267 輪實測；刀後另增卷首 13 枚有號指針，俱合卡題）。
try:
    from difflib import SequenceMatcher
    def _lcs(a, b):
        s = SequenceMatcher(None, a, b, autojunk=False)
        return s.find_longest_match(0, len(a), 0, len(b)).size

    PUNC = re.compile(u'[\\s\u3000，、；：？！。\u2014\\-「」『』（）()〔〕\\[\\]·]')
    def _pl(s):                                             # 校名只須去標點，不引 _tk（免重載語料）
        return PUNC.sub(u'', s)
    TIT = {}
    for n, v in DEFN.items():                                 # 276・定義載體皆入名冊（卡亡而案仍在）
        TIT[(u'案例', u'%02d' % n)] = re.split(u'—|--|：', v[u'名'])[0]
    for l in LINES:
        mm = re.match(u'^### 〔(案例|補遺) ([0-9]+)〕(.*)$', l)
        if mm:
            TIT[(mm.group(1), mm.group(2))] = re.split(u'—|--|：', mm.group(3))[0]
    bad = []
    for i, l in enumerate(LINES):
        if not in_print(i) or l.startswith(u'### '):
            continue
        for m2 in re.finditer(u'〔(案例|補遺) ?([0-9]+)〕([一-鿿]{3,14})', l):
            ckey = (m2.group(1), m2.group(2).zfill(2))     # 275：舊名 key 會遮蔽第 9 目之同名正則器，故改稱
            head = TIT.get(ckey)
            if not head:
                bad.append((i + 1, u'%s%s 查無此卡' % ckey))
                continue
            nm = _pl(m2.group(3))
            own = _lcs(nm, _pl(head))
            if own >= 2:
                continue
            bo, bk = max((_lcs(nm, _pl(h)), k2) for k2, h in TIT.items() if k2 != ckey)
            if bo >= 5:
                bad.append((i + 1, u'%s%s『%s』不合本卡題『%s』而合 %s%s' % (
                    m2.group(1), m2.group(2), m2.group(3)[:10], head[:10], bk[0], bk[1])))
    chk(u'案號與案名對合（引名全異於本卡而合他卡者）', sorted(set(bad)))
except Exception as e:                                        # 尺不得以崩冒充判決
    chk(u'案號與案名對合（引名全異於本卡而合他卡者）', [(u'尺自身出錯：%s' % e,)])

# ── 28：案例指針必帶號（第 267 輪・把『於目逐條查』降為一形制之禁）
#   266 輪之債③『幽靈名無尺』之解：幽靈名與描述語同形，無可分別之口徑即無尺；
#   但**無號之〔案例·名〕形制**有邊界可量——它天生落在第 27 目（號↔名）之網外，故禁其形，
#   則全書每一處案例指稱自動歸 27 目之管。形制禁令＝把人工覆核換成機器可驗之約。
#   例外：〔案例 J-3〕之字母式乃『現代深水案例』之別一命名空間（非第六章卡），不在此禁。
try:
    NOREF = re.compile(u'〔(?:案例|補遺)·|〔(?:案例|補遺)〕|〔(?:案例|補遺)\\s+〔')
    bad = [(i + 1, NOREF.search(l).group(0)) for i, l in enumerate(LINES)
           if in_page(i) for m in [NOREF.search(l)] if m]
    chk(u'案例指針必帶號（無號『〔案例·名〕』形制歸零）', bad)
except Exception as e:
    chk(u'案例指針必帶號（無號『〔案例·名〕』形制歸零）', [(u'尺自身出錯：%s' % e,)])

# ── 29：印面不作工程黑話與官僚分級代號（第 269 輪・外路第四報告之實存四項，刀後立禁以護之）
#   口徑：黑話以**詞**為單位，不以義為單位（以義為單位即墮『幽靈名與描述語同形』之盲，267 輪之誡）；
#         兩張名單各須斷非空，詞數當場報入目名（名單之大小亦是宣稱）。
#   有實事所指者**不入禁**，如實記於此：SOP（第八章節題之實）・矩陣（量刑階梯・四奪之圖）・
#         表單（第八章『表單落日原則』所論之對象即是表單）・面向・對帳（銀行對帳單）・審計（三線模型之第三線）。
#   『代碼』『參數』等詞若日後因世俗法之實指而須入冊，須在此目下開一類外並寫明誰守該類外，不可逕自放寬名單。
JARGON = [u'解耦', u'模組', u'測試集', u'流水號', u'工單', u'序列化', u'微服務', u'快取', u'緩存',
          u'參數', u'接口', u'陣列', u'資料庫', u'管線', u'腳本', u'迭代', u'正規化', u'顆粒度',
          u'三聯單', u'核取方塊', u'票據', u'代碼', u'API', u'SDK', u'pipeline', u'Repository',
          u'回呼', u'佔位']
CODES = [u'甲級', u'乙級', u'丙級', u'三級判準', u'以丙代甲', u'以乙代甲', u'甲乙丙',
         u'分流碼', u'一式三份', u'存檔卡', u'執存', u'編號格式']
assert len(JARGON) >= 20 and len(CODES) >= 8, u'兩單不可空（今 %d／%d）' % (len(JARGON), len(CODES))
bad = [(i + 1, w) for i, l in enumerate(LINES) if in_page(i)
       for w in JARGON + CODES if w in l]
chk(u'印面不作工程黑話與官僚代號', bad, u'%d＋%d 詞・今量 %d' % (len(JARGON), len(CODES), len(bad)))

# ── 30：書名號內之**本律篇名**須見於本地語料（第 271 輪・《僧殘犍度》之虛篇名現形）
#   口徑：只認含『犍度』之《X》——此為《四分律》之結構篇名，本地六十卷必可覆核；
#         先剝『書名・』前綴（《四分律・呵責犍度》取其『呵責犍度』），再折異體（語料作『揵度』）而對 _tk.VINAYA。
#   不在此目：他典之品名（《中論・觀四諦品》《梵網經心地戒品》）——本地不儲其檔，強校即生偽缺，
#         其界由凡例【未收之典須自標其界】守（260 輪之制）；『二十犍度』乃總數之稱，非篇名，亦擲之。
#   ⚠ 語料必經 `_tk.VINAYA`：`原文/*.txt` 非 UTF-8，自讀必全報 0 見（護欄冊之舊誡，此處同一）。
try:
    with contextlib.redirect_stdout(io.StringIO()):
        sys.path.insert(0, ROOT)
        import _tk as _V39TK
    NC = re.sub(u'[\\s\\u3000，、；：？！。]', u'', _V39TK.VINAYA).replace(u'揵度', u'犍度')
    assert len(NC) > 400000, u'語料不可為空（今 %d 字）' % len(NC)
    bad = []
    n30 = 0
    for i, l in enumerate(LINES):
        if not in_page(i):
            continue
        for m in re.finditer(u'《([^》\n]{1,26}犍度[^》\n]{0,8})》', l):
            k = m.group(1)
            k = re.sub(u'^.{1,10}[·・/]', u'', k)                  # 剝『書名・』前綴
            if k in (u'二十犍度', u'二十二犍度'):
                continue
            n30 += 1
            if k not in NC:
                bad.append((i + 1, u'《%s》語料無此連綴' % k))
    chk(u'書名號內之本律篇名須見於語料', sorted(set(bad)), u'%d 形・虛 %d' % (n30, len(bad)))
except Exception as e:
    chk(u'書名號內之本律篇名須見於語料', [(u'尺自身出錯：%s' % e,)])

# ── 31：目錄條與書身之題**依序**對合（第 275 輪・換章工序生出之債）
#   第 9 目『目錄不指空』只問此題是否存在於書中，不問是否在**此章此序**：275 換 ch4-5 時
#   目錄同步誤取**第四章**之第四節條覆寫第五章之條，九尺猶綠——指錯家者視為不逮，故其時以人工認賠。
#   今以『向前匹配』為約：目錄逐條（章／節／閘門）须在書身自前而後之題序列中依次命中，
#   命中則pointer前進，掃盡猶未中即報其條。**立目之先親量基線：條 48・合 48・不合 0**（先量後立）。
TOCIT = re.compile(u'^\\s+\\*+\\s*(?:\\*\\*)?(?:第([一二三四五六七八九十]+)章|第([一二三四五六七八九十]+)節|閘門([一二三四五六]))')
H3IT = re.compile(u'^### (?:第[一二三四五六七八九十]+節|閘門[一二三四五六])')
_titems = []
for _i in range(Toc0, BODY0):
    _m = TOCIT.match(LINES[_i])
    if _m:
        _titems.append((_i + 1, u'章' if _m.group(1) else u'節', key(LINES[_i])))
_hseq = []
for _i in range(BODY0, len(LINES)):
    _l = LINES[_i]
    if _l.startswith(u'# 第') and re.match(u'^# 第[一二三四五六七八九十]+章', _l):
        _hseq.append((u'章', key(_l)))
    elif _l.startswith(u'### ') and not _l.startswith(u'### 〔') and H3IT.match(_l):
        _hseq.append((u'節', key(_l[4:])))
_j, _orph = 0, []
for _ln, _kd, _k in _titems:
    while _j < len(_hseq) and _hseq[_j] != (_kd, _k):
        _j += 1
    if _j >= len(_hseq):
        _orph.append((_ln, u'%s｜%s' % (_kd, LINES[_ln - 1].strip()[:34])))
    else:
        _j += 1
chk(u'目錄條與書身題依序對合', _orph, u'條 %d・合 %d' % (len(_titems), len(_titems) - len(_orph)))

# ── 32：逐字引文須有句讀（第 281 輪・外路第九報告過『生肉文字』，量得四段）
#   緣起：附錄四與第六章之引文，有些片段繮自語料時把標點判歸刪（最長一段 516 字級無一标點）——
#         逐字尺之 norm 本就別除標點，故兩尺皆緑，病全在印面：讀者得一塊無斷句之大藏經生肉。
#   口徑：印面之行內，每個「…」段內『連續無標點與空白』最長串須 < 40 字；限值 40 者為本目現量之限（全書今 0 段）。
try:
    def _run(s2):
        best = cur = 0
        for ch in s2:
            if ch in _PUA or ch.isspace():
                cur = 0
            else:
                cur += 1
                best = max(best, cur)
        return best
    _PUA = u'，。；：、？！「」‘’（）《》【】…—·　'
    bad = [(i + 1, _run(m.group(1))) for i, l in enumerate(LINES) if in_print(i)
           for m in re.finditer(u'「([^「」]{20,})」', l) if _run(m.group(1)) >= 40]
    chk(u'逐字引文須有句讀（無標點長段以四十字為限）', sorted(set(bad)),
        u'今 %d 段達限' % len(bad))
except Exception as e:
    chk(u'逐字引文須有句讀（無標點長段以四十字為限）', [(u'尺自身出錯：%s' % e,)])

# ── 33：集群矩陣速查之式（第 282 輪・外路第十報告：276 代筆之套語與貼經已清，此約須有牙）
#   口徑：以五張表頭『案號與事相綱要｜起心動念｜核心爭點與邊界標尺｜佛陀處斷與法效｜律典原典出處』定其管轄；
#         其內每行須 ① 七欄 ② 爭點欄不得含『犯緣與開緣』式套語（276 補丁之同句模板）
#         ③ 處斷欄須以 **【 起手（刑名或法效之命題，不復直貼戒句——逐字之責在附錄四）。
#         表頭張數須為五：**管轄歸零即該目自己喊停**（殭尺之綠，五十二度）。
try:
    MHDR = u'| 案號與事相綱要 | 起心動念（微觀心所歸位） | 核心爭點與邊界標尺 | 佛陀處斷與法效 | 律典原典出處 |'
    _hs = [i for i, l in enumerate(LINES) if l.strip() == MHDR.strip()]
    _rows = []
    for _h in _hs:
        _i = _h + 2
        while _i < len(LINES) and LINES[_i].lstrip().startswith(u'|'):
            _rows.append(_i)
            _i += 1
    _b = []
    for _i in _rows:
        _c = [x.strip() for x in LINES[_i].split(u'|')]
        if len(_c) != 7:
            _b.append((_i + 1, u'欄數 %d' % len(_c)))
            continue
        if u'犯緣與開緣' in _c[3] or _c[3].endswith(u'如何判？'):
            _b.append((_i + 1, u'爭點欄殘套語：%s' % _c[3][:24]))
        if not _c[4].startswith(u'**\u3010'):
            _b.append((_i + 1, u'處斷欄不以刑名命題起手：%s' % _c[4][:24]))
    if len(_hs) != 5:
        _b.insert(0, (u'管轄', u'速查表頭今 %d 張（期 5・管轄歸零即目自身之病）' % len(_hs)))
    chk(u'集群矩陣速查之式（爭點無套語・處斷以刑名起手）', _b,
        u'表頭 %d 張・行 %d・錯 %d' % (len(_hs), len(_rows), len(_b)))
except Exception as e:
    chk(u'集群矩陣速查之式（爭點無套語・處斷以刑名起手）', [(u'尺自身出錯：%s' % e,)])

# ── 34：經典地標大案之段序（第 284 輪・外路第十二報告逮地標 03 跳號，量得他十二則俱作一〜五）
#   口徑：第六章凡『### 【經典地標深描 NN】』者，其下『#### X、』之序須恰為『一二三四五』；
#         段數之宣稱亦在冊（第六章卷首自列『事相→心识→处断→智慧→原典』之五段式），錯位即紅。
try:
    _i6 = next((i for i, l in enumerate(LINES) if l.startswith(u'# 第六章')), None)
    _i7 = next((i for i, l in enumerate(LINES) if _i6 is not None and i > _i6 and l.startswith(u'# 第七章')),
               len(LINES))
    _b, _gs = [], []
    if _i6 is None:
        _b.append((u'第六章不可見',))
    else:
        _k = _i6
        while _k < _i7:
            if LINES[_k].startswith(u'### 【經典地標深描'):
                _j = _k + 1
                _sq = []
                while _j < _i7 and not LINES[_j].startswith(u'### '):
                    _m = re.match(u'^#### ([一二三四五六七八九十])、', LINES[_j])
                    if _m:
                        _sq.append(_m.group(1))
                    _j += 1
                _gs.append(_k + 1)
                if u''.join(_sq) != u'一二三四五':
                    _b.append((_k + 1, u'段序『%s』（期一〜五）' % (u''.join(_sq) or u'空')))
            _k += 1
    chk(u'經典地標大案之段序須一〜五連貫', _b, u'地標 %d 則・錯 %d' % (len(_gs), len(_b)))
except Exception as e:
    chk(u'經典地標大案之段序須一〜五連貫', [(u'尺自身出錯：%s' % e,)])

# ── 35：歷輪錯字之黑單（第 284 輪・凡以記憶構碼位所得之怪字，逮一即入單，免其死灰復燃）
#   只收『本書绝无正用』之形：『樞點』（標點之誤，281 落刀残跡）、『輍』（諉之誤）與歷輪現形之怪字。
#   合法難字（如 毘・罽・釐・闊・謚）不入單，故本單是**串 blacklist** 而非字集掃描；簡形之掃另在第 21 目。
BADGLYPH = [u'樞點', u'輍', u'奷', u'冱', u'遤', u'壊', u'儱', u'豂', u'訃']
try:
    _b = [(i + 1, u'『%s』' % g) for i, l in enumerate(LINES) if in_page(i)
          for g in BADGLYPH if g in l]
    chk(u'印面無歷輪錯字（黑單隨輪增補）', sorted(set(_b)),
        u'黑單 %d 枚・命中 %d 處' % (len(BADGLYPH), len(_b)))
except Exception as e:
    chk(u'印面無歷輪錯字（黑單隨輪增補）', [(u'尺自身出錯：%s' % e,)])

# ── 36：尺亦須被尺量（第 272 輪・『不變量 N/N』之 N 自身即宣稱；275 順移 32，282 順移 34，284 順移為 36）
#   三則：① 目名須為**常量**（含 % 佔位者即把計數寫進標籤，靜態對合無從比對，且 FAIL 時面目全非）；
#         ② try／except **兩支同名**（271 輪之《X犍度》目即因 except 改名而致『源中 31・實印 30』之差）；
#         ③ 源碼中唯一目名之數 ＝ 本尺實印之目數（名單勿兩抄之自版：不另立名冊，逕讀本檔）。
SELF = io.open(os.path.abspath(__file__), encoding=u'utf-8').read().split(u'\n')
tn, en, inx = set(), set(), False
for l in SELF:
    if re.match(u'^\\s*except\\s', l):
        inx = True
    m2 = re.search(u"chk\\(u'([^']+)'", l) or re.search(u'chk\\(u"([^"]+)"', l)
    if m2:
        (en if inx else tn).add(m2.group(1))
    elif l.strip() and not l.strip().startswith(u'#'):
        inx = False
bad = [(u'目名含佔位：%s' % x,) for x in sorted(tn) if u'%' in x]
bad += [(u'except 改了目名：%s' % x,) for x in sorted(en - tn)]
if len(tn | en) != len(RES) + 1:
    bad.append((u'唯一目名 %d ≠ 實印 %d' % (len(tn | en), len(RES) + 1),))
bad = [x for x in bad if x]
chk(u'目數自對合（名常量・except 同名・唯一名＝實印）', sorted(set(bad)),
    u'源 %d・印 %d' % (len(tn | en), len(RES) + 1))

n_bad = sum(1 for _n, f, _d in RES if f)
for n, f, d in RES:
    print(u'%-40s %s%s' % (n, u'PASS' if not f else u'FAIL', u'（%s）' % d if d else u''))
    for x in f[:12]:
        print(u'      ✗ %s' % (u'｜'.join(str(y) for y in x) if isinstance(x, tuple) else x))
    if len(f) > 12:
        print(u'      … 又 %d 處不具列' % (len(f) - 12))
print(u'———— 不變量 %d/%d 全綠' % (len(RES) - n_bad, len(RES)))
sys.exit(1 if n_bad else 0)
