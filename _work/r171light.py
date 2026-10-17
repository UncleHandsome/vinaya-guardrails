# -*- coding: utf-8 -*-
"""r171light.py —— 輕動詞冗語與公文腔之體檢（第 171 輪立，**待診軸**：恆退 0，不為閘）。

緣起：歷輪量段之形（readchk）、段際之橋（166）、句內之插語（170），本輪先試『虛詞鏈』
而歸零——全書同一句讀之內無『A之B之C』三連嵌套（三見者俱為『、』所分隔之並列，乃正格
排比），故甲乙二目改為**護欄**（守未來新文），另立真病形：
**輕動詞構式**（light verb）——『進行／予以／作出＋動名詞』。此構式以動詞充當名詞之殼，
削其殼則殼內之動名詞自任述語，文意全失者方改寫，故**十之七八可逕削二字而不損一義**：
『進行實質審查』→『實質審查』，『予以剔除』→『當場剔除』。此為近代公文之習慣，非律藏語彙，亦非書中自創術語。

  甲 進行＋動名詞（『進行』之後有實義動名詞作其賓語）
  乙 予以＋動詞
  丙 作出＋動名詞
  丁 三連嵌套之護欄——**已撤（第 171 輪）**：同一句讀之內『之』『的』三見者全書唯三例，親量
     俱非病（一為並列，二為一氣貫下而讀不滯）；鏈之為病須讀文意方能判，依 168、170 兩輪之教，
     器即當退——本輪遂改以『輕動詞』立目（其病有形、其治可量、其零可證）。
  戊 報而不治：公文腔介詞與術語load（針對／基於／透過／機制／相關／層面／落实…之計數）——
     此類或為法令用語、或為書中定名，**只記其量，不列為病**；尤以『通過』一語，全書二十七見
     幾盡為『羯磨通過』之律語，若入病目即百分之百假陽性，此為本輪最重之一條反例。

豁免（先分桶再論病）：
  · 『得以進行』『方式進行』『程序進行』——此『進行』自動詞用（＝進行得下去），非輕動詞；
  · 『塞進行囊』一类：『進』屬上動詞、『行』屬下名詞之Cut位假陽性；
  · 世俗法令之原文轉述（如《勞資爭議處理法》『雇主予以降調、減薪……者，依法無效』）——
    法條之字不減不改（第 155 輪『引文逐字』之制與作者判令『世俗法條照舊』一以貫之）；
  · 引號「」『』與括號〔〕之內不判（律文與標界自有其形制）；
  · 底冊（附錄C／K／L／M／終卷）與圍欄圖全免；表、題、引行全免。
用法：`PYTHONPATH=. python -X utf8 _work/r171light.py [主檔副本] [--csv] [--wide N]`
退出碼：恆 0（待診）。
"""
import io, os, re, sys, csv
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as t

ARGS = [a for a in sys.argv[1:] if not a.startswith('-')]
WIDE = '--wide' in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
OUTCSV = os.path.join(HERE, 'r171cases.csv')

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

CJK = re.compile(u'[一-鿿]')
Q1 = re.compile(u'「[^」]*」')
Q2 = re.compile(u'『[^』]*』')
BQ = re.compile(u'〔[^〕]*〕')
SEG = re.compile(u'[，、；：！？。]')
CHAIN_ZHI = re.compile(u'之[^，、；：！？。]{1,12}?之[^，、；：！？。]{1,12}?之')
CHAIN_DE = re.compile(u'的[^，、；：！？。]{1,12}?的[^，、；：！？。]{1,12}?的')
# 自動詞之『進行』＝『進行得下去／以…方式進行』：其後無賓語（一句讀之內即盡），非冗語
OBJ = re.compile(u'^[一-鿿]{2,}')
INTRANSIT = re.compile(u'^[^一-鿿]')
# 『塞進行囊』：進屬上動詞、行屬下名詞之切位假陽性
FALSECUT = re.compile(u'[塞放投插推闖走跑]進行[囊腳列程]')
# 法令原文轉述之『予以』（法條之字不改）
STATUTE = re.compile(u'.{0,18}予以.{0,24}(?:依法無效|無效|處分者|得據以)')
LIGHT = [(u'甲', u'進行'), (u'乙', u'予以'), (u'丙', u'作出')]
OFFICE = [u'針對', u'基於', u'透過', u'通過', u'對於', u'機制', u'相關', u'層面', u'落實',
          u'全面', u'不斷', u'進一步', u'充分', u'深入', u'旨在', u'給予', u'情況', u'情況下']


def bare(s):
    return re.sub(u'[\\s*`>#|]', u'', s)


def nlen(s):
    return len(CJK.findall(bare(s)))


def core_of(s):
    return BQ.sub(u'', Q2.sub(u'', Q1.sub(u'', s)))


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


def clip(s, n=64):
    s = re.sub(u'\\s+', u' ', s)
    return (s[:n] + u'…') if len(s) > n else s


rows = {u'甲': [], u'乙': [], u'丙': []}
exempt = []
offcnt = Counter()
for i in sorted(PRINT):
    s = L[i].strip()
    if not s or s[0] in u'|#>' or s.startswith(u'---'):
        continue
    core = core_of(s)
    for tag, w in LIGHT:
        for m in re.finditer(w, core):
            tail = core[m.end():]
            after = tail[:12]
            if FALSECUT.search(core[max(0, m.start() - 1):m.end() + 1]):
                exempt.append((i, w, u'切位假陽性（動詞＋行囊之屬）'))
                continue
            if not OBJ.match(tail):
                exempt.append((i, w, u'自動詞（其後無賓語，即『進行得下去』義）'))
                continue
            if w == u'予以' and STATUTE.search(core[max(0, m.start() - 20):m.end() + 26]):
                exempt.append((i, w, u'法令原文轉述'))
                continue
            rows[tag].append((i, core[max(0, m.start() - 30):m.end() + 30], after))
    # 【丁目『三連嵌套護欄』已撤（第 171 輪）】：同一句讀之內『之』『的』三見者，全書唯三例
    # （『之數與教授尼眾之任』乃並列、『山門的規矩守護的是整個佛法的尊嚴』與『換來的只是表面的
    # 順從與內心更深的怨毒』俱一氣貫下而讀不滯）——無一為病。**『鏈』之為病與否須讀文意方能判，
    # 依 168、170 兩輪之教，器即當退**；本輪遂改以『輕動詞』立目（其病有形、其治可量）。
    for w in OFFICE:
        offcnt[w] += core.count(w)

for tag in (u'甲', u'乙', u'丙'):
    rs = rows[tag]
    print(u'\n── %s：%d 處 ──' % (tag, len(rs)))
    if rs:
        per = Counter(chap_of(r[0]) for r in rs)
        print(u'   分布：' + u'、'.join(u'%s %d' % (c[:6], m) for c, m in per.most_common(9)))
    for i, seg, x in (rs if not WIDE else rs[:200]):
        print(u'   L%-6d ｜%s' % (i + 1, clip(seg, 88 if WIDE else 66)))
print(u'\n── 豁免：%d 處（自動詞・切位假陽性・法令原文）──' % len(exempt))
per = Counter((w, why) for _, w, why in exempt)
for (w, why), m in per.most_common():
    print(u'   %s／%s：%d' % (w, why, m))
print(u'\n── 戊 報而不治：公文腔與術語 load（不列為病）──')
print(u'   ' + u'、'.join(u'%s %d' % (w, offcnt[w]) for w in OFFICE if offcnt[w]))
if '--csv' in sys.argv:
    with io.open(OUTCSV, 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh)
        w.writerow([u'目', u'行', u'章', u'節', u'前後文'])
        for tag in (u'甲', u'乙', u'丙'):
            for i, seg, x in rows[tag]:
                w.writerow([tag, i + 1, chap_of(i), sec_of(i), clip(seg, 110)])
    print(u'清冊已寫：%s' % OUTCSV)
print(u'\n== 合計：甲 %d、乙 %d、丙 %d（丁目『三連嵌套』已撤）；豁免 %d ==' %
      (len(rows[u'甲']), len(rows[u'乙']), len(rows[u'丙']), len(exempt)))
