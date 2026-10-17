# -*- coding: utf-8 -*-
"""r190f3.py —— 附錄F-3 揭露清單之兩向完備（第 190 輪立・待診・恆退 0）。

緣起：第 187 輪曾以『全書《X》名目』為鍵試建此器，得 62 候選而親量盡屬旁物（律內篇題、世俗法條與契約名、
本書自製篇名、名目異形之拆詞）——**口徑以『凡書名』為域，必泛**。本輪改採**窄口徑**：
只取**行內已自我宣稱**『本地未收／本地語料未收／無從覆核／未入本地』等語之句，其同句內之《X》即構成一筆
『揭露之債』——此類宣稱既出，F-3 便應有其列（凡例引文承諾：本地無從覆核者別見 F-3）。

兩向：
 甲（漏揭露）：印面行含宣稱語 ∧ 句內有《X》（X 非《四分律》《戒本》）∧ X 之名目不見於 F-3 篇文（字面互含）。
 乙（幽列）  ：F-3 各列第 3 欄之《X》在**全書他處**（含附錄F-1、第八章以下）已無一處出現——列存而無引。
旁證：丙＝宣稱語在行內而其書名在別行（跨行之引，只報其數）；丁＝X 實已入本地語料檔名（宣稱過重，宜改正）。
 丙之初版只問『行內有宣稱語而無《》』，遂把**揭露之器自身的自述**盡數撈入（11 筆：F-3 篇題與表列、
 附錄F 篇首凡例、卷首目錄、附錄E 凡例各一）——那是詞不是引。第 235 輪擭緊三層：附錄F 篇內不較、
 行內須有「」8 字以上之逐字形貌（引的是篇目職分者不算）、已以案語就地標界者不較。擭緊後丙 **0**，甲亦 0。
豁免：底冊（附錄C／K／L／M、終卷）與圍欄不較；『本地有據』一類反向語不計。
退出碼：恆 0。`argv[1]`＋`require-hit` 供負測（唯甲計入 hit）。
收報路徑：已錨於本檔之根（`os.path.abspath(__file__)`）——以 cwd 相對路徑寫檔者，他目錄一跑即 `FileNotFoundError`（第 217 輪自犯現形）。

量訖而不立之維（第 217 輪・他典逐字引文之存在性，兼 F-3 坦承之真實）：
 本軸之甲只校『**行內已自陳未收**』者之有列；今另問兩事——**印面以「」逐字引他典而未自陳者，其文果在否**，
 及『**已列不等於列得實**』。五版探針量訖（三問俱無病，未立軸）：
  甲 印面《》去重 108 名、總見 453；本地 `佛經/` 十一檔可校者唯 11 典（餘如《成唯識論》28 見、《大智度論》14 見、
    《楞嚴經》6 見之屬，即 214 輪『語料之可核邊界』）。
  乙 **本地有檔之他典長引（折一 ≥8 字）26 段：中 24／未中 2**——未中者俱在 L11739《大乘起信論》（真諦譯 T1666），
    而 F-3 第 3–5 列已逐條明陳『本地檔作「謂依如來藏有生滅心轉…」，譯本不同，逐字無從覆核』⇒ 非病，勿刀。
  丙 **不可核（本地無其檔）78 段、涉 23 典，其典名全數已見於 F-3（未列 0）**——與本軸之甲 0 同向互證。
  丁 **倒影（坦承之真實）**：F-3 區內所引之典而本地實有其檔者 3 行（《大乘起信論》《中論》《入菩薩行論》），
    親量俱屬**譯本／版本層之精確陳述**（真諦譯未收、羅什譯未收、此句唯他典有）⇒ 虛報 0。
 不立軸之故：典名→檔須手立《異題對照表》（中論＝中觀根本慧論頌、起信論＝大乘起信論、勝鬘師子吼…＝勝鬘經 之屬），
 一有新增他典即須補表——**立軸須手列豁免即成手工帳**（196 輪近似形錯拼一維之同科），故只落此註。
 尺之教（五版五犯，皆器不是書）：① 跨行取典之窗會把 A 行之引配給 B 行之典（表列尤甚，虛報 33）；
 ② 同行之內尚須分**隨文注源**（『「引文」（《X》卷一）』——有括號方算）與**領起標**（『《X》：「甲」「乙」』——
 一枚領起統領其後數引），優先序錯則把甲乙盡配給下一組之領起（L11734、L11737、L11747 即此）；
 ③ 折一 <8 字之短引不校（『心地無非自性戒』一類七字名目，假中假不中俱易生）；
 ④ 『F-3 之區界』須取**標題行**，不得取字面『F-3』之首次命中——印面早以『已列 F-3』回指，
 一刀切遂把 F-1、F-2 撈入，『全已揭露』之斷語一度是虛（214『碎語重搜』之又一形）。
"""
import io, os, re, sys, glob
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as t

COP = sys.argv[1] if len(sys.argv) > 1 else None
REQ = u'require-hit' in sys.argv

if COP:
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(ROOT)
    L = io.open(COP, encoding=u'utf-8').read().split(u'\n')
    BOT, inb = set(), False
    for i, l in enumerate(L):
        if l.startswith(u'# '):
            inb = any(k in l for k in t.BOTTOM_NAMES)
        if inb:
            BOT.add(i)
else:
    L = t.LINES
    BOT = t.bottom_lines()

FENCE = chr(96) * 3
fence, inf = [False] * len(L), False
for i, l in enumerate(L):
    if l.strip().startswith(FENCE):
        inf = not inf
        fence[i] = True
        continue
    fence[i] = inf

DOC = u'\n'.join(L)
# F-3 區間
s3 = e3 = None
for i, l in enumerate(L):
    if l.startswith(u'### ') and u'F-3' in l:
        s3 = i
    elif s3 is not None and l.startswith(u'### ') and i > s3:
        e3 = i
        break
if s3 is None:
    print(u'未尋得 F-3 篇界——器之立足點已失，如實退')
    sys.exit(0 if not COP else 1)
if e3 is None:
    e3 = len(L)
F3 = u'\n'.join(L[s3:e3])
F3_HEADS = [l for l in F3.split(u'\n') if l.startswith(u'|')]
BOOK = re.compile(u'《([^》]{1,40})》')
CLAIM = re.compile(u'(本地未收|本地語料未收|本地未檔|未入本地|本地無從覆核|無從覆核|本地未收之典)')
LOCAL = set()
for _p in (glob.glob(os.path.join(t.ROOT, u'佛經', u'**', u'*.txt'), recursive=True) +
           glob.glob(os.path.join(t.ROOT, u'原文', u'*.txt'))):
    _rel = os.path.relpath(_p, t.ROOT).replace('\\', u'/')
    for _part in _rel.split(u'/'):        # 目錄名亦是典名（解深密經／成唯識論／菩薩地_戒品俱以資料夾存檔，
        _part = re.sub(u'\\.txt$', u'', _part)   # 初版只取檔名，遂把『2.txt』之『2』當典名而誤判『未收』
        if len(_part) >= 3:
            LOCAL.add(_part)
SKIP = (u'四分律', u'戒本', u'大正新脩大藏經')
CONTEXT = re.compile(u'(未逐字|旁證|非逐字|屬羅什譯本|本地語料作|譯本小異)')


F3_NAMES = [x for x in re.findall(u'《([^》]{1,40})》', F3) if x]

# 附錄F 全篇之界（丙桶之豁免域：篇內之宣稱語是『揭露之器』的自述，非一筆待揭露之引文）
sF = eF = None
for _i, _l in enumerate(L):
    if _l.startswith(u'# ') and u'附錄F' in _l:
        sF = _i
    elif sF is not None and _l.startswith(u'# ') and _i > sF:
        eF = _i
        break
Q8 = re.compile(u'「([^」]{8,})」')          # 具逐字引文形貌者方入丙
NAMES = re.compile(u'(篇|節|表|清單|附錄|目錄|章|卷次|版本|典籍)')   # 引的是篇目職分，非經論文句
ANC = re.compile(u'(該典未入|〔案：|（案：|另於附錄|如實標界)')      # 已就地交代


def in_f3(nm):
    return any(nm in f or f in nm for f in F3_NAMES)


def local_hit(nm):
    keys = [nm] + [x for x in re.split(u'[·、，,\\s]', nm) if len(x) >= 3]
    return any(len(k) >= 3 and (k in b or b in k) for k in keys for b in LOCAL)


def bound_claims(line):
    """宣稱語只與其前後 30 字內之書名配對——一行多典時『本地未收』之說唯指其一，
    初版以全行為域，遂把同行之中『本地實有其文』之典一併拖入（假陽性三筆，由逐條查證照出）。"""
    out = []
    for m in CLAIM.finditer(line):
        lo, hi = max(0, m.start() - 30), min(len(line), m.end() + 30)
        for mm in BOOK.finditer(line, lo, hi):
            out.append((mm.group(1), line[max(0, mm.start() - 40):mm.start() + 40]))
    return out


rows = {u'甲': [], u'丙': [], u'丁': []}
for i, l in enumerate(L):
    if i in BOT or fence[i] or not CLAIM.search(l):
        continue
    for nm, ctxw in bound_claims(l):
        if nm in SKIP or local_hit(nm) or in_f3(nm):
            continue
        if CONTEXT.search(ctxw):
            rows[u'丁'].append((i + 1, nm, l.strip()[:56]))   # 就地已交代為旁證／對譯／未逐字，非逐字宣稱
            continue
        rows[u'甲'].append((i + 1, nm, l.strip()[:56]))
    if not BOOK.findall(l):
        if sF is not None and sF <= i < (eF or len(L)):
            continue                                   # 附錄F 篇內自述（篇題·凡例·F-3 表列）
        if ANC.search(l):
            continue                                   # 〔案〕之類，就地標界已畢
        if not [f for f in Q8.findall(l) if not NAMES.search(f)]:
            continue                                   # 行無經論逐字形貌，只是一句制度說明
        rows[u'丙'].append((i + 1, u'', l.strip()[:56]))

# 乙·幽列：F-3 各列書名在全書他處是否仍見
he = []
for r in F3_HEADS:
    cs = [c.strip() for c in r.split(u'|')]
    if len(cs) < 4 or not cs[1] or not cs[1][0:1].isdigit():
        continue
    for nm in BOOK.findall(cs[3]):
        if nm in SKIP:
            continue
        others = sum(1 for j, l in enumerate(L) if nm in l and not (s3 <= j < e3))
        if others == 0:
            he.append((int(cs[1]), nm))

print(u'F-3 兩向（窄口徑）：甲·宣稱本地未收而未列 F-3 %d 筆｜乙·幽列（F-3 列而全書他處無引）%d 筆｜'
      u'丙·宣稱而配對無書名 %d 筆｜丁·就地已交代為旁證／對譯（非逐字宣稱）%d 筆'
      % (len(rows[u'甲']), len(he), len(rows[u'丙']), len(rows[u'丁'])))
for ln, nm, txt in rows[u'丁'][:6]:
    print(u'  丁 L%-6d 《%s》｜%s' % (ln, nm, txt))
for ln, nm, txt in rows[u'甲'][:10]:
    print(u'  甲 L%-6d 《%s》｜%s' % (ln, nm, txt))
for num, nm in he[:10]:
    print(u'  乙 F-3 第 %d 列《%s》全書他處零見' % (num, nm))
with io.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          u'_work', u'r190list.txt'),      # 收報須錨於根：以 cwd 相對路徑寫檔者，他目錄一跑即 FileNotFoundError（第 217 輪）
             'w', encoding=u'utf-8', newline=u'\n') as f:
    f.write(u'═══ 甲：%d ═══\n' % len(rows[u'甲']))
    for ln, nm, txt in rows[u'甲']:
        f.write(u'甲\tL%d\t《%s》\t%s\n' % (ln, nm, txt))
    f.write(u'═══ 乙：%d ═══\n' % len(he))
    for num, nm in he:
        f.write(u'乙\tF3-%d\t《%s》\n' % (num, nm))
print(u'清冊：_work/r190list.txt')
if COP and REQ:
    sys.exit(0 if rows[u'甲'] else 1)
sys.exit(0)
