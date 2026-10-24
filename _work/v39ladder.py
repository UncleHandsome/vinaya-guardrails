# -*- coding: utf-8 -*-
"""277 輪・第十尺：第七章『處分階梯軸』與『四諍軸』之名單，須與各案自報之律刑對合。

緣起：外路第六報告指『落水救拔・師徒瞻視・安隱尼問倒』被列入『不可懺·極刑滅擯』——此乃 276 之前
      『迎回補丁』以分號追加之殘（其時只為湊足『共 N 案』之數）。量得：第一階 18 案中 7 案自始非極刑。
口徑：（一）**極刑階須有極刑之據**——凡列於第一階者，其證（附錄四該行之卷段篇聚＋第六章其定義載體
            前後十行）必含『波羅夷・滅擯・難法・斷頭』之一，無據即紅（此則亦擋得住『救人反成死罪』之荒謬）；
      （二）第二〜五階同理各驗其刑名（僧殘／偷蘭遮／波逸提・尼薩耆／突吉羅・提舍尼），
            **只禁『有此刑名者不得入他階』之逆向錯配？否**——一案數支者眾（16 之三戒・05 之兩判），
            故採寬式：列於第 N 階者，其證須含該階刑名（含即過，不含即報『疑錯列』，由人裁）；
      （三）第六・七階乃『無刑』之兩面（教誡・開許），語義不可自動判，故不校，但**自報之數須與實列對合**；
      （四）四諍軸不校歸屬（義理之判），只校自報之數與實列；
      （五）278・全書凡自報案數之名冊（『共 N 案』『（N 案）』）一律對合其實收之唯一案號——
            數目亦是宣稱，宣稱須在尺內（不分章、不分欄與題）。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/v39ladder.py [檔] [-v]
退碼：錯列或數不合 ≥1 即退 1。
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (ROOT, os.path.join(ROOT, u'_work')):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import _casedef as CD                                              # noqa: E402
import _tk                                                     # noqa: E402

SRC_PATH = next((a for a in sys.argv[1:] if not a.startswith(u'-')), None)
verbose = u'-v' in sys.argv
if SRC_PATH:
    LINES = io.open(SRC_PATH, encoding=u'utf-8-sig').read().replace(u'\r\n', u'\n').split(u'\n')
else:
    LINES = _tk.MAIN_LINES

H6 = next(i for i, l in enumerate(LINES) if l.startswith(u'# 第六章'))
H7 = next(i for i, l in enumerate(LINES) if l.startswith(u'# 第七章'))
A4 = next((i for i, l in enumerate(LINES) if l.startswith(u'# 附錄四')), None)
A5 = next((i for i, l in enumerate(LINES) if l.startswith(u'# 附錄五')), len(LINES))
DEFN = CD.case_defs(LINES)
KEYS = {u'一': (u'波羅夷', u'滅擯', u'難法', u'斷頭', u'極刑', u'五逆'),
        u'二': (u'僧殘', u'僧伽婆尸沙'),
        u'三': (u'偷蘭遮',),
        u'四': (u'波逸提', u'尼薩耆', u'捨墮'),
        u'五': (u'突吉羅', u'提舍尼', u'向彼悔')}
CN = {u'一': 1, u'二': 2, u'三': 3, u'四': 4, u'五': 5, u'六': 6, u'七': 7}

# 附錄四：案號 ➔ 該行全文（卷段篇聚＋逐字原句）
APX = {}
for i in range(A4 or 0, A5):
    for n in {int(x) for x in re.findall(r'〔案例 ?0*(\d+)(?:[^0-9][^〕]*)?〕', LINES[i])}:
        APX.setdefault(n, []).append(LINES[i])


def token_re(n):
    return re.compile(u'〔案例 ?0*%d(?:[^0-9][^〕]*)?〕' % n)


def axis_rows():
    """兩軸之名單行（此軸自列之案號不可作本案之據，須除）。"""
    out = set()
    for h in (next((i for i, l in enumerate(LINES) if l.startswith(u'#### 三、四諍衝突學軸')), None),
              next((i for i, l in enumerate(LINES) if l.startswith(u'#### 四、處分階梯軸')), None)):
        if h is None:
            continue
        end = next((i for i in range(h + 1, len(LINES)) if LINES[i].startswith(u'#### ')), len(LINES))
        out.update(range(h, end))
    return out


AXIS_ROWS = axis_rows()


def evidence(n):
    """該案之自報律刑證據＝全書凡以『〔案例 N…〕』token 指名本案之各行（軸內之名單行除，免自證）
       ＋其下八行內之『法相導航』（地標之刑名掛在導航行）＋附錄四之該行。"""
    tok = token_re(n)
    hits = [i for i, l in enumerate(LINES) if i not in AXIS_ROWS and tok.search(l)]
    txt = u'∥'.join(LINES[i] for i in hits)
    for i in hits:
        for k in range(i + 1, min(i + 9, len(LINES))):
            if u'法相導航' in LINES[k]:
                txt += u'∥' + LINES[k]
    return txt + u'∥' + u'∥'.join(APX.get(n, []))


# 例外：一案數支，其一支之刑見於他章之敘述而不在本案之 token 行——逐一註明所據，不容空欄
EXEMPT = {
    5: u'解牛雙判：既遂支結波羅夷（螺旋對照 A 之判語；慈心支另見第六階）',
    7: u'洗瘡雙判：殺心支結波羅夷（同上；無殺心支另見第七階）',
    9: u'十一種自以為無犯：情到則結波羅夷（見第三章閘門一與對照 B）',
    21: u'闡陀連環抗拒：第十三僧殘・波逸提第十二條・突吉羅三罪俱有（見第二章與本章）',
    22: u'阿濕婆污他家：擯出羯磨隨僧殘法行，別支之惡作見波逸提（見第五章處分表）',
    34: u'功德衣五月日落：出衣遲緩之結罪見波逸提法第三十四條（見第二章場域表）',
    56: u'知水有蟲：飲用澆地結波逸提，不畜濾水囊行路則突吉羅（兩階俱列，非錯置）',
    65: u'百眾學法（式叉迦羅尼）皆突吉羅，其篇聚作『百眾學法』不現刑名',
    74: u'難遮雙層守門：度人未審結突吉羅，隱前科受戒則戒體不生（兩階俱列）',
    102: u'受請安居聞利背約：失歲並結違要之突吉羅（見第五章第一節與安居犍度）',
}



# ── 取兩軸之名單
def axis(title):
    h = next((i for i, l in enumerate(LINES) if l.startswith(title)), None)
    if h is None:
        return []
    end = next((i for i in range(h + 1, len(LINES)) if LINES[i].startswith(u'#### ')), len(LINES))
    out, cur = [], None
    for i in range(h + 1, end):
        m = re.match(u'^\\* \\*\\*(?:[一二三四]、.*?|[第]([一二三四五六七])階：.*?)，?共 (\\d+) 案', LINES[i])
        if m:
            cur = [m.group(1) or u'', int(m.group(2)), [], i + 1]
            out.append(cur)
        elif cur is not None and u'〔案例' in LINES[i]:
            cur[2].extend(int(x) for x in re.findall(r'〔案例 ?0*(\d+)〕', LINES[i]))
    return out


lad = axis(u'#### 四、處分階梯軸')
zeng = axis(u'#### 三、四諍衝突學軸')
bad = []
print(u'處分階梯軸 %d 階・四諍軸 %d 類' % (len(lad), len(zeng)))
for order, claim, nums, ln in lad:
    k = CN.get(order)
    u = sorted(set(nums))
    tag = u'' if k in (6, 7) else u'刑證'
    miss = []
    if order in KEYS:
        for n in u:
            if n in EXEMPT:
                continue                                 # 數支之案，其據註於 EXEMPT，逐枚可查
            if not any(x in evidence(n) for x in KEYS[order]):
                miss.append(n)
    ok = (claim == len(u)) and not miss
    if not ok:
        bad.append((u'階' + order, claim, len(u), miss))
    print(u'%s第%s階｜宣稱%d・唯一%d｜無%s者：%s' % (u'✗ ' if not ok else u'✓ ', order, claim, len(u),
                                                  tag or u'判（不校）', miss or u'無'))
    if verbose and miss:
        for n in miss:
            print(u'      案%03d｜%s' % (n, evidence(n)[:110].replace(u'\n', u'')))
for name, claim, nums, ln in zeng:
    u = sorted(set(nums))
    ok = claim == len(u)
    if not ok:
        bad.append((u'諍' + name[:2], claim, len(u), []))
    print(u'%s%s｜宣稱%d・唯一%d' % (u'✗ ' if not ok else u'✓ ', name[:16], claim, len(u)))

# ── 278・全書自報案數之名冊（凡『共 N 案』『（N 案）』皆入冊，不限第七章兩軸）
#   緣起：第六章改製後，集群矩陣之題曰『（13 案）』而地標案號列另立，其數之實證散落數處；
#         278 量得非染污端一組報 38 而實收 30（孤行九枚落在『---』之外，尺不及）。
#   管轄：宣稱行至 ①同級或更高級標題、②下一宣稱行、③『---』、④（宣稱行乃列舉項目者）同縮排之下一項目——
#         四者之最先；案數＝區內〔案例 NN〕去重（『〔案例 07 / 遮3〕』之兼帶代號亦算一枚）。
CLAIM = re.compile(u'共 (\\d+) 案|（(\\d+) 案）')
HEADL = re.compile(u'^(#{2,6}) ')
CASET = re.compile(u'〔案例 ?0*(\\d+)(?![0-9])')


def _lv(s):
    m = HEADL.match(s)
    return len(m.group(1)) if m else 99


roster, rbad = [], []
for i, l in enumerate(LINES):
    m = CLAIM.search(l)
    if not m:
        continue
    hm = HEADL.match(l)
    kind = u'標題' if hm else u'項目'
    mylv, ind = _lv(l), l[:len(l) - len(l.lstrip())]
    end = len(LINES)
    for k in range(i + 1, len(LINES)):
        s = LINES[k]
        if HEADL.match(s) and _lv(s) <= mylv or CLAIM.search(s) or s.strip() == u'---':
            end = k
            break
        if kind == u'項目' and (len(s) - len(s.lstrip())) == ind and s.lstrip().startswith(u'* '):
            end = k
            break
    uq = {int(x) for x in CASET.findall(u'\n'.join(LINES[i + 1:end]))}
    claim = int(m.group(1) or m.group(2))
    roster.append((i + 1, kind, claim, len(uq), l.strip()[:40]))
    if claim != len(uq):
        rbad.append((u'L%d' % (i + 1), claim, len(uq), l.strip()[:26]))
print(u'自報案數之名冊 %d 枝（全書）・不合 %d 枝%s' % (
    len(roster), len(rbad), u'' if not rbad else u'：%s' % rbad[:6]))
bad.extend(rbad)
print(u'———— 階梯・四諍・名冊：錯 %d 處%s' % (len(bad), u'' if not bad else u'：%s' % bad))
sys.exit(1 if bad else 0)
