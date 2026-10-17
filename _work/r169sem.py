# -*- coding: utf-8 -*-
"""r169sem.py —— 表頭欄名與欄內內容之相副（第 169 輪立，**待診軸**：恆退 0，不為閘）。

緣起：歷輪表軸唯校『形』——`tblaudit` 甲軸校欄數與表頭齊、乙軸校格線不缺字、
`_tk` 之不變量校空表頭與空格；**獨未問『此欄之名是否真是此欄之義』**。
欄名過窄（如名『對應案例』而欄內是法義）或欄內錯置（如『卷次』欄混入處分），
於形制全綠之下紙上誤人——此屬語義層，非對錯層，故立為待診而非長檢。

兩目：
  甲 欄名之期望 vs 欄內之相符率：依欄名關鍵詞推定內容之形（案例代號、卷次、
     心所名、正理、處分羯磨、閘門階次、數字…），逐欄算相符率，<0.6 者報。
  乙 案例代號之越界：〔遮N〕N≤45、〔開N〕N≤25、〔僧N〕N≤30，且須真存在
     （第六章百則之號）——欄內出現非法代號者報。

口徑：印面（去底冊 `_tk.bottom_lines()`、去圍欄）；表＝連續以 `|` 起之行，
     首行為表頭、次行為分隔線；空格、『—』、『同上』、『/』不入住計算之例
     （『同上』乃第 164 輪所定之續行記號，非內容）。
用法：`PYTHONPATH=. python -X utf8 _work/r169sem.py [主檔副本] [--csv] [--all]`
退出碼：恆 0（待診）。
"""
import io, os, re, sys, csv
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as t

ARGS = [a for a in sys.argv[1:] if not a.startswith('-')]
SHOWALL = '--all' in sys.argv
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

BLANK = {u'', u'—', u'-', u'－', u'/', u'同上', u'—／－', u'（空）', u'*'}
CASE = re.compile(u'[遮開僧]\\s*\\d+')
NUM = re.compile(u'\\d')
JUAN = re.compile(u'[卷][\\s一二三四五六七八九十百\\d]|[\\d一二三四五六七八九十百]\\s*[-~至]?[卷段]')
XIN = re.compile(u'貪|瞋|恚|癡|慢|愛|怖|清淨|無記|懈怠|覆\\b|慳|掉舉|惡作|悔')
LEI = re.compile(u'遍行|別境|善心所|煩惱|隨惑|不定|大隨|小隨|中隨')
LI = re.compile(u'正理\\s*[一二三四五六七八\\d]')
LIMAP = re.compile(u'^正理\\s*[一二三四五六七八]$')     # 第七章矩陣之『正理N』欄是**計數**，非正理文
CHU = re.compile(u'波羅夷|僧殘|僧伽婆尸沙|偷蘭遮|波逸提|突吉羅|提舍尼|別住|摩那埵|出罪|滅擯|呵責|擯|悔過|發露|羯磨|遮|開許')
MEN = re.compile(u'閘門\\s*[一二三四五六\\d]|[初次三終]環|第[一二三]環|\\d\\s*階|[一二三四五]階')
STG = re.compile(u'[一二三四五六七八九十][、.)]|\\d\\s*[、.)]|階|境|想|思|相')

# 欄名 → 內容之期望。**關鍵詞須以整辭判，不可見字即認**（初版之誤）：
#   『卷首憲綱』非卷次、『統攝案例數』是計數非代號、『認知層次』非數字欄。
EXPECT = [
    (u'(案例|判例)(?!數|計|目)|代表案|對照案|所屬案', CASE, u'案例代號'),
    (u'卷次|所在卷|卷段|第\\s*\\S{0,2}\\s*卷|卷\\)\\s*$', JUAN, u'卷次'),
    (u'根本心|心所(?!類別|功能)|煩惱名', XIN, u'心所名'),
    (u'心所類別|類別', LEI, u'心所類名'),
    (u'^正理$|正理(?!一|二|三|四|五|六|七|八)|所攝正理', LI, u'正理'),
    (u'處分|羯磨|結罪|罪名', CHU, u'處分羯磨'),
    (u'閘門|之環|三環|漏斗', MEN, u'閘門階次'),
    (u'階段|次第|序位', STG, u'序碼或階'),
    (u'數$|計$|比率|占比|額|頁碼', NUM, u'數字'),
]
# 欄名之**修辭用法**不入期望：『單／雙／三正理分佈驗算公式』是算式而非正理名目，
# 『罪名實質』『心所功能』『認知層次』所問皆非該類詞之字面——見此類詞即跳過該規則。
SKIP_HD = u'公式|分佈|驗算|說明|示意|範例|指針|要義|實質|功能|層次|對照'


def cells(line):
    s = line.strip()
    if not s.startswith(u'|'):
        return None
    parts = [p.strip() for p in s.strip(u'|').split(u'|')]
    return parts


def tables():
    out, i = [], 0
    while i < N:
        if i in PRINT and L[i].strip().startswith(u'|'):
            j = i
            rows = []
            while j < N and j in PRINT and L[j].strip().startswith(u'|'):
                cs = cells(L[j])
                if cs and not all(re.match(r'^:?-{2,}:?$', c or u'-') for c in cs):
                    rows.append((j, cs))
                j += 1
            if rows:
                out.append(rows)
            i = j
        else:
            i += 1
    return out


def chap_of(idx):
    for j in range(idx, -1, -1):
        if L[j].startswith(u'# '):
            return L[j][2:14]
    return u'卷首'


def sec_of(idx):
    for j in range(idx, -1, -1):
        s = L[j].strip()
        if s.startswith(u'#### '):
            return s[5:34]
        if s.startswith(u'### '):
            return s[4:34]
        if s.startswith(u'## '):
            return s[3:34]
    return u''


def clip(s, n=30):
    s = re.sub(u'\\s+', u' ', s.replace(u'<br>', u'／'))
    return (s[:n] + u'…') if len(s) > n else s


TABS = tables()
A_JIA, A_YI = [], []
EVAL = [0]                                  # 實校之欄數（有期望且實格 ≥3）
CASES_OK = set(re.findall(u'[遮開僧]\\s*\\d+', u' '.join(L[i] for i in range(N) if i in PRINT)))
for rows in TABS:
    head = rows[0][1]
    body = rows[1:]
    if len(body) < 3:
        continue
    ncol = len(head)
    for c in range(ncol):
        h = head[c] if c < len(head) else u''
        vals = [r[1][c] if c < len(r[1]) else u'' for r in body]
        real = [v for v in vals if re.sub(u'[\\s*]', u'', v) not in BLANK]
        if len(real) < 3:
            continue
        done = False
        if LIMAP.match(re.sub(u'[\\s*]', u'', h)):      # 矩陣之『正理N』欄乃計數，先定其期望
            rules = [(u'', NUM, u'數字')]
        else:
            rules = EXPECT
        for pat, rex, name in rules:
            if done:
                break
            if pat and (not re.search(pat, h) or re.search(SKIP_HD, h)):
                continue
            hit = sum(1 for v in real if rex.search(re.sub(u'<br>', u'；', v)))
            rate = hit / float(len(real))
            done = True                                 # **一欄只從一期望**：多重規則會自相矛盾
            EVAL[0] += 1
            if rate < 0.6:
                A_JIA.append((rows[0][0], h, name, rate, len(real), real))
        for v in real:
            for m in CASE.findall(v):
                mm = re.sub(u'\\s+', u'', m)
                lim = {u'遮': 45, u'開': 25, u'僧': 30}[mm[0]]
                try:
                    n = int(mm[1:])
                except ValueError:
                    continue
                if n > lim or mm not in CASES_OK:
                    A_YI.append((rows[0][0], h, mm, v))
                    break

print(u'== 表頭語義相副（第 169 輪立）%s ==' % (u'｜副本 ' + ARGS[0] if ARGS else u''))
print(u'印面表 %d 張｜實校之欄 %d（有期望且實格 ≥3）' % (len(TABS), EVAL[0]))
print(u'\n── 甲 欄名之期望與欄內相符率 <0.6：%d 欄 ──' % len(A_JIA))
per = Counter(chap_of(a) for a, h, nm, r, n, real in A_JIA)
print(u'   分布：' + u'、'.join(u'%s %d' % (c[:6], m) for c, m in per.most_common(10)))
for a, h, nm, rate, n, real in sorted(A_JIA, key=lambda x: x[3])[:14 if not SHOWALL else len(A_JIA)]:
    print(u'   L%-6d 欄『%s』期望[%s] 相符 %.0f%%（%d 格）｜%s' % (a + 1, clip(h, 16), nm, 100 * rate, n, chap_of(a)[:6]))
    print(u'      例：%s' % u'　'.join(clip(v, 22) for v in real[:4]))
print(u'\n── 乙 欄內案例代號越界或查無：%d 欄 ──' % len(A_YI))
for a, h, mm, v in A_YI[:10]:
    print(u'   L%-6d 欄『%s』%s｜%s' % (a + 1, clip(h, 14), mm, clip(v, 40)))
if '--csv' in sys.argv:
    with io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'r169cases.csv'),
                 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh)
        w.writerow([u'目', u'表起行', u'章', u'節', u'欄名', u'期望', u'相符率', u'格數', u'例一', u'例二', u'例三'])
        for a, h, nm, rate, n, real in A_JIA:
            w.writerow([u'甲', a + 1, chap_of(a), sec_of(a), clip(h, 24), nm, '%.2f' % rate, n,
                        clip(real[0], 26), clip(real[1] if len(real) > 1 else u'', 26),
                        clip(real[2] if len(real) > 2 else u'', 26)])
        for a, h, mm, v in A_YI:
            w.writerow([u'乙', a + 1, chap_of(a), sec_of(a), clip(h, 24), u'代號', u'', u'', mm, clip(v, 26), u''])
    print(u'清冊已寫。')
print(u'\n== 合計：甲 %d 欄、乙 %d 欄 ==' % (len(A_JIA), len(A_YI)))
