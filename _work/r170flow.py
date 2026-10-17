# -*- coding: utf-8 -*-
"""r170flow.py —— 句法窒礙體檢（第 170 輪立，**待診軸**：恆退 0，不為閘）。

緣起：`readchk` 十二目量『段之形、句之長、節之斷』，166 輪另量『段際有無橋』；
獨**句內之主干是否被插語淹沒**無人問之。書中慣以全形括號作註、以直角引號載律文，
二者皆體例所定；然括注一長、引文一重，主語與述語便隔成兩截，讀之必喘——
此病不在『長』（二目已量），在『斷』。三目：

  甲 括注淹主幹：一句之內，全形括號（）〔〕「（」形）之內容 ≥25 字，
     而**同句括號之外**之句幹 <15 字——主干反短於註腳。
  乙 引文淹句：一句之內「…」之字數占該句 ≥70%，且引號外 <10 字——
     全句只餘『如云：「…」』一类空殼（引文自為正文者不在此列，見豁免）。
  丙 問號懸空——**已撤（第 170 輪）**：段末以問號收而下文無作答之形。『作答』無從自動判定：
     放寬則下文一句陳述即算有答（永不報，負測兩度不中），收緊則三鏡、捫心自省、天平衝突
     諸設問之卡全報（初測 20 處，親量皆屬製式）。依 168 輪之教，須讀文意方能判者器即當退。

豁免（**先分桶再論病**，同 159、166、168 三輪之教）：
  · 標界與體例括註：『（本地語料未收…）』『〔◈本書法式…〕』『〔案：…〕』『〔名相〕』
    及卷次兼注『兼 NN-MM卷段』——此乃凡例所定之形制，動之即違約；
  · 括號在句末（其後無文）者不淹主幹，不判；
  · 『◎原典』以下整段引文、案例卡片之『「…」』判語欄——引文即正文，非插語；
  · 問號出於律文逐字（引號之內）者不判；
  · 底冊（附錄C／K／L／M／終卷）與圍欄圖全免。
用法：`PYTHONPATH=. python -X utf8 _work/r170flow.py [主檔副本] [--sample N] [--csv]`
退出碼：恆 0（待診）。
"""
import io, os, re, sys, csv, random
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as t

SAMPLE = int(sys.argv[sys.argv.index('--sample') + 1]) if '--sample' in sys.argv else 0
SKIP = {str(SAMPLE)} if SAMPLE else set()
ARGS = [a for a in sys.argv[1:] if not a.startswith('-') and a not in SKIP]
HERE = os.path.dirname(os.path.abspath(__file__))
OUTCSV = os.path.join(HERE, 'r170cases.csv')

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

CJK = re.compile(u'[一-鿿]')          # 唯計漢字：括弧與標界符不充句幹
BRACK = re.compile(u'[（〔][^（〔）〕]{6,}[）〕]')
QUOTE = re.compile(u'「[^」]{6,}」')
BODY = re.compile(u'[（〔][^）〕]*[）〕]')
# 體例性括註：標界、法式、案語、名相、卷次兼注——皆凡例所定，動之即違約
EXBR = re.compile(u'^（[^）]*(本地語料未收|未收|詳見|見附|另見|或作|下同|例同|卷段|兼)'
                  u'|^〔[^〕]*(◈|案：|名相|口徑|求證|示例|通行名|現代法域|限定|今譯|非本律逐字|拆聲|衡平擬制|但書)')
# 釋義式括注：`**術語**（釋義）`——括注即該術語之定義，主幹短是形制而非病（卷首憲綱、
# 八大正理諸條皆然）；目次式行（『第N節 X（其所載）』）同理，乃導航之目，非句中之插語。
GLOSS = re.compile(r'^[\s*.0-9>-]*\*\*[^*]{2,26}\*\*[\s*[（〔]')
TOCISH = re.compile(r'^[\s*>-]*(?:\*\*)?(?:第\s*[一二三四五六七八九十\d]+\s*[節章篇]|'
                    u'閘門\\s*[一二三四五六]|正理\\s*[一二三四五六七八]|附錄\\s*[A-M]|[①-⓿]|'
                    u'[一二三四五六七八九十]{1,3}[、.]|\\d{1,2}[、.)])')
# 問卡製式：三鏡、捫心自省、天平衝突、觀心問諸欄——設問即其職，本無作答之義務
ASKCARD = re.compile(u'^[\\s*>-]*\\*{0,2}(?:第[一二三]鏡|捫心自省|天平衝突|觀心問|自問|'
                     u'[初次三終]環|【?第?\\s*[一二三四五六七八九十\\d]+\\s*問)')
CITE = re.compile(r'^[\s*>]\*{0,2}(?:正理|閘門|憲綱|十句義|第\s*[一二三四五六七八九十]+句)')      # 名目後直接經句＝引證式
ANSWER = re.compile(u'^[一-鿿　-〿＀-￯*【〔（]{0,4}(答|蓋|以|由|所以者何|此謂|者，|所謂|凡|要之|夫|然)'
                    u'|^[^。？]{0,24}[者也]。|^[^。？]{0,30}——')


def bare(s):
    return re.sub(u'[\\s*`>#|]', u'', s)


def nlen(s):
    return len(CJK.findall(bare(s)))


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


def clip(s, n=54):
    s = re.sub(u'\\s+', u' ', s)
    return (s[:n] + u'…') if len(s) > n else s


A_JIA, A_YI, A_BING = [], [], []
for i in sorted(PRINT):
    s = L[i].strip()
    if not s or s[0] in u'|#>' or s.startswith(u'---'):
        continue
    if re.match(r'^\s*[-*]\s', s):
        pass                                   # 列項之內亦有句法，一併判之
    # 以句末三符切句（全形）
    for sent in re.split(u'(?<=[。！？])', s):
        if nlen(sent) < 8:
            continue
        # 甲 括注淹主幹
        if GLOSS.match(s) or TOCISH.match(s):
            pass
        else:
            for m in BRACK.finditer(sent):
                inner = m.group(0)
                if (EXBR.match(inner) or nlen(inner) < 25
                        or nlen(BODY.sub(u'', sent)) == 0):
                    continue
                stem = nlen(BODY.sub(u'', sent))
                if stem < 15:
                    A_JIA.append((i, sent, inner, stem))
                    break
        # 乙 引文淹句
        qs = QUOTE.findall(sent)
        if qs:
            qn = sum(nlen(q) for q in qs)
            rest = nlen(QUOTE.sub(u'', sent))
            if (qn * 100 >= 70 * (qn + rest) and rest < 10 and rest > 0
                    and not CITE.match(sent) and not GLOSS.match(s) and not TOCISH.match(s)):
                A_YI.append((i, sent, qn, rest))
    # 【丙目『問號懸空』已撤（第 170 輪）】：『作答之形』無從自動判定——放寬則下文一句陳述
    # 即算有答（永不報，負測兩度不中），收緊則三鏡、捫心自省、天平衝突諸設問之卡全報
    # （初測 20 處，親量皆屬製式）。依 168 輪之教：**須讀文意方能判者，器即當退**。
    # 懸問之察留予人工覆讀；ASKCARD／ANSWER 兩表暫留，供日後另立『問卡必有一問』之軸。


def show(rows, tag, k, fmt):
    print(u'\n── %s：%d 處 ──' % (tag, len(rows)))
    if rows:
        per = Counter(chap_of(r[0]) for r in rows)
        print(u'   分布：' + u'、'.join(u'%s %d' % (c[:6], m) for c, m in per.most_common(9)))
    pick = rows
    if SAMPLE:
        random.seed(5)
        pick = random.sample(rows, min(SAMPLE, len(rows)))
    for r in pick[:k]:
        print(u'   ' + fmt(r))


show(A_JIA, u'甲 括注淹主幹（括內 ≥25 字而句幹 <15 字）', 12 if not SAMPLE else SAMPLE,
     lambda r: u'L%-6d 幹 %2d 字｜%s\n        括：%s' % (r[0] + 1, r[3], clip(r[1], 62), clip(r[2], 46)))
show(A_YI, u'乙 引文淹句（引內占句 ≥70% 而引外 <10 字）', 10 if not SAMPLE else SAMPLE,
     lambda r: u'L%-6d 引 %d／外 %d｜%s' % (r[0] + 1, r[2], r[3], clip(r[1], 66)))
if '--csv' in sys.argv:
    with io.open(OUTCSV, 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh)
        w.writerow([u'目', u'行', u'章', u'節', u'句', u'插語', u'句幹'])
        for i, sent, inner, stem in A_JIA:
            w.writerow([u'甲', i + 1, chap_of(i), sec_of(i), clip(sent, 80), clip(inner, 60), stem])
        for i, sent, qn, rest in A_YI:
            w.writerow([u'乙', i + 1, chap_of(i), sec_of(i), clip(sent, 80), u'引%d/外%d' % (qn, rest), rest])
    print(u'清冊已寫：%s' % OUTCSV)
print(u'\n== 合計：甲 %d、乙 %d（丙目已撤）==' % (len(A_JIA), len(A_YI)))
