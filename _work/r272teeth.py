# -*- coding: utf-8 -*-
"""272 輪立・牙列矩陣：逐目植病，驗「每一目真有牙」（目數隨尺長，基線之 N 即針數之上限）。

緣起：`不變量 31/31 全綠` 只證今冊無病，不證三十有一目皆能紅。
      歷輪之負測皆係「一輪一植」，餘目之牙從未同時校過——本器把三十一目一次問完。
口徑：① 植病者改**冊之副本**（ tempfile 內，ROOT 不落新檔），產器與尺身之病（24・31）改**尺之副本**（須在 `_work/`，因 ROOT 自 __file__ 推得）；
      ② 判「逮」＝本目在紅名單內；連帶紅者如實記，不諱不刪（一植多紅＝該植非針尖，只作記錄不作病）；
      ③ 副本之基線必先全綠，否則一切紅皆屬「因崩而紅」，整盤作廢；
      ④ 錨不可求者報「未植」，不許默過；尺自身崩（stderr 非空／目數非基線之 N）報「崩」。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r272teeth.py
退碼：逮 < 針數即退 1（欠牙・未植・殭針・崩皆屬欠）；基線不綠則退 2。
"""
import glob
import io
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, u'_work')
sys.path.insert(0, WORK)
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
SRC = os.path.join(ROOT, NAME)
CHK = os.path.join(WORK, u'v39chk.py')
CHKTXT = io.open(CHK, encoding=u'utf-8').read()
BASE = io.open(SRC, encoding=u'utf-8').read().split(u'\n')
env = dict(os.environ, PYTHONIOENCODING=u'utf-8')
TMPD = tempfile.mkdtemp(prefix=u'r272teeth_')

# 與尺同式之範圍（只為挑落點，不作判決）
BODY0 = next((i for i, l in enumerate(BASE) if l.startswith(u'# 第一章')), 0)
END = next((i for i, l in enumerate(BASE) if l.startswith(u'# 終卷')), len(BASE))
Toc0 = next((i for i, l in enumerate(BASE) if l.startswith(u'## 【全書開卷標準目錄】')), 0)
FEN = set()
_op = None
for i, l in enumerate(BASE):
    if l.strip().startswith(u'```'):
        if _op is None:
            _op = i
        else:
            FEN |= set(range(_op, i + 1))
            _op = None


def prose(k=0):
    """第 k 個可落字之印面散句行（非題・非表・非引・非圍欄）。"""
    out = [i for i, l in enumerate(BASE)
           if BODY0 < i < END and i not in FEN and len(l) >= 40
           and not l.lstrip().startswith((u'#', u'|', u'>', u'*', u'-', u'`'))]
    return out[k]


def repl(L, idx, old, new):
    """行內精確一替；錨不中即raise（未植不許默過）。"""
    if L[idx].count(old) != 1:
        raise ValueError(u'L%d 錨非一：%s' % (idx + 1, old[:20]))
    L[idx] = L[idx].replace(old, new)
    return idx


def find_line(pred, start=0):
    for i in range(start, len(BASE)):
        if pred(BASE[i], i):
            return i
    raise ValueError(u'錨不可求')


# ── 簡形植字：與尺同一張名單（名單勿兩抄，逕讀尺所用之兩帳）
import contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import recordsimp
from _simpdict import MAP as _SD
CORP = set()
for _f in glob.glob(os.path.join(ROOT, u'原文', u'*.txt')):
    CORP |= set(io.open(_f, encoding=u'utf-8', errors=u'ignore').read())
SIMP = (set(recordsimp.S) | set(u'两当强随旧总') | (set(_SD) - {c for c in _SD if c in CORP}))
assert len(SIMP) > 400, u'簡形名單不可為空（今 %d）' % len(SIMP)

# ── 27 目之錯系植法：取兩卡卡題，其共同子串 ≤1，以 A 題之頭冠於 B 號之下
from difflib import SequenceMatcher
PUNC = re.compile(u'[\\s\u3000，、；：？！。\u2014\\-「」『』（）()〔〕【】\\[\\]·]')


def _pl(s):
    return PUNC.sub(u'', s)


def _lcs(a, b):
    return SequenceMatcher(None, a, b, autojunk=False).find_longest_match(0, len(a), 0, len(b)).size


TIT = {}
import _casedef as _CD                                             # 276：案號定義共器
for _n, _v in _CD.case_defs(BASE).items():
    TIT[(u'案例', u'%02d' % _n)] = re.split(u'—|--|：', _v[u'名'])[0]
PAIR = None
PAIR = None
for ka in TIT:
    ha = _pl(TIT[ka])
    if len(ha) < 6:
        continue
    nm = re.sub(u'[^\u4e00-\u9fff]', u'', ha)[:8]
    if len(nm) < 6:
        continue
    for kb in TIT:
        if kb == ka or kb[0] != u'案例':
            continue
        if _lcs(nm, _pl(TIT[kb])) <= 1:
            PAIR = (kb, nm, ka)
            break
    if PAIR:
        break
assert PAIR, u'錯系之植法不可得（兩卡卡題無從判孤）'

# ── 圍欄內之落點
FLINE = next(i for i in sorted(FEN) if BASE[i].strip() and not BASE[i].strip().startswith(u'```'))
# ── 附錄四內之表列
A4 = find_line(lambda l, i: l.startswith(u'# 附錄四'))
A5 = find_line(lambda l, i: l.startswith(u'# 附錄五'), A4 + 1)
R4ROW = next(i for i in range(A4, A5) if BASE[i].startswith(u'|')
             and re.search(u'\u3014案\u4f8b ?([0-9]+)\u3015', BASE[i])
             and not re.search(u'\u3014案\u4f8b ?(01|1)\u3015', BASE[i]))
# ── 分隔線之落點
DASH = find_line(lambda l, i: i > BODY0 and i not in FEN and l.strip() == u'---'
                 and BASE[i - 1].strip() == u'' and i - 1 not in FEN)
# ── 目錄內之一條
TOCLINE = next(i for i in range(Toc0, BODY0) if re.match(u'^\\s+\\* ', BASE[i]) and len(BASE[i]) > 30)

# ═════════ 植病表：目序 → (名, 函) ═════════
PLANTS = {}


def plant(n):
    def deco(fn):
        PLANTS[n] = fn
        return fn
    return deco


@plant(1)
def p1():
    """末案之**定義載體**改號：276・第六章改製後案號有四形載體（卡／矩陣／地標列／標題），
       落點逕向共器 case_defs 取，勿再硬編『### 〔案例 N〕』之形（曾因此只改到附錄四之表列，目 1 不紅）。"""
    L = list(BASE)
    d = _CD.case_defs(BASE)
    n = max(d)
    v = d[n]
    i = v[u'行'] - 1                                      # case_defs 之行號乃 1-based（印面座標）
    return L, repl(L, i, u'案例 %d' % n, u'案例 %d' % (n + 1)), \
        u'末案 %d→%d（斷號不連貫・載體=%s・L%d）' % (n, n + 1, v[u'形'], i + 1)


@plant(2)
def p2():
    L = list(BASE)
    i = find_line(lambda l, idx: l.startswith(u'### 〔調部專題 15〕'))
    return L, repl(L, i, u'15〕', u'16〕'), u'專題 15→16（越序）'


@plant(3)
def p3():
    L = list(BASE)
    i = find_line(lambda l, idx: l.strip().startswith(u'*   **案號**'))
    del L[i]
    return L, i, u'鉸掉一果地標案號列（案號無可追）'


@plant(4)
def p4():
    L = list(BASE)
    i = prose()
    L[i] += u'〔案例103〕'
    return L, i, u'加無卡之號指針〔案例103〕'


@plant(5)
def p5():
    L = list(BASE)
    i = prose()
    L[i] += u'〔調部專題16〕'
    return L, i, u'加無號之指針〔調部專題16〕'


@plant(6)
def p6():
    L = list(BASE)
    i = prose(1)
    L[i] += u'（本回）'
    return L, i, u'嵌分批語『本回』'


@plant(7)
def p7():
    L = list(BASE)
    i = prose(1)
    L[i] += u'〔遮9〕'
    return L, i, u'嵌舊帳案號〔遮9〕'


@plant(8)
def p8():
    L = list(BASE)
    c = sorted(SIMP)[:1]                                   # 名單不另抄：逕取尺所用量單之首（已除語料所見之形）
    assert c, u'簡形名單為空'
    i = prose(2)
    L2 = list(L)
    L2[i] = L[i] + u'（校%s之例）' % c[0]
    return L2, i, u'引號外落一簡形・字見輸出'


@plant(9)
def p9():
    L = list(BASE)
    i = prose(2)
    L[i] += u'（'
    return L, i, u'段內添一單邊小括號'


@plant(10)
def p10():
    L = list(BASE)
    # 落點自算：印面內第一個其下仍有文之括題（舊針硬編『#### 【心相照鏡】』，第六章改製後該題已不存 → 未植）
    i = find_line(lambda l, idx: re.match(u'^#{3,4} 【.+】$', l) is not None
                  and BODY0 < idx < END and idx not in FEN and BASE[idx + 1].strip())
    L.insert(i, L[i])
    return L, i, u'標題連出兩遍（其前無文）'


@plant(11)
def p11():
    L = list(BASE)
    i = TOCLINE
    return L, repl(L, i, u'* ', u'* 癸辛'), u'目錄條改其題（指空）'


@plant(12)
def p12():
    L = list(BASE)
    i = prose(3)
    L[i] += u'（第九章第七節）'
    return L, i, u'指無此章之節'


@plant(13)
def p13():
    L = list(BASE)
    v = sum(1 for l in BASE if l.startswith(u'### 〔案例 ')) + 1      # 虛數自卡數推得，卡數若變此針不齟
    i = prose(3)
    L[i] += u'（今 %d 則判例）' % v
    return L, i, u'自報之數增一枚（實數之外造一虛宣）'


@plant(14)
def p14():
    L = list(BASE)
    i = FLINE
    L[i] = u'**' + L[i].strip() + u'**'
    return L, i, u'圍欄內添 markdown 粗體'


@plant(15)
def p15():
    L = list(BASE)
    i = prose(4)
    L[i] = L[i] + u' '
    return L, i, u'行末添一枚空格'


@plant(16)
def p16():
    L = list(BASE)
    i = find_line(lambda l, idx: l.strip() == u'#### 【事相經過】')
    L[i] = L[i] + u'。'
    return L, i, u'標題行末著句號'


@plant(17)
def p17():
    L = list(BASE)
    L[DASH - 1] = u'分隔線前抽去空行'
    return L, DASH - 1, u'分隔線前無空行'


@plant(18)
def p18():
    L = list(BASE)
    i = prose(4)
    L[i] += u'（）'
    return L, i, u'嵌空殼小括號'


@plant(19)
def p19():
    L = list(BASE)
    i = find_line(lambda l, idx: l.startswith(u'### 〔調部專題 11〕'))
    return L, repl(L, i, u'### ', u'#### '), u'降一則專題為四級題（篇內少一則）'


@plant(20)
def p20():
    L = list(BASE)
    i = prose(5)
    L[i] += u'阿[少/兔]陀'
    return L, i, u'非表列行嵌 CBETA 組字碼'


@plant(21)
def p21():
    L = list(BASE)
    i = prose(5)
    L[i] += u'『'
    return L, i, u'行內添一單邊『'


@plant(22)
def p22():
    L = list(BASE)
    i = prose(6)
    L[i] += u'（01-10 卷）'
    return L, i, u'嵌檔名式引卷'


def p22b():
    """277 之新網眼：裸檔名區間而無『卷』字相隨（『（50-60、卷二十二至三十）』之形）。"""
    L = list(BASE)
    i = prose(7)
    L[i] += u'（50-60、卷三十三）'
    return L, i, u'嵌裸檔名區間（無『卷』相隨）'


@plant(23)
def p23():
    L = list(BASE)
    i = prose(6)
    L[i] += u'律意：近於「如法」'
    return L, i, u'律意之攝述雜逐字引號'


@plant(25)
def p25():
    L = list(BASE)
    i = R4ROW
    m = re.search(u'\u3014案\u4f8b ?([0-9]+)\u3015', L[i])
    return L, repl(L, i, m.group(0), u'〔案例 1〕'), u'附錄四一行改指已有之號（缺一行）'


@plant(26)
def p26():
    L = list(BASE)
    i = prose(7)
    L[i] += u'【安樂令】'
    return L, i, u'命題作『某某令』'


@plant(27)
def p27():
    L = list(BASE)
    i = prose(7)
    kb, nm, ka = PAIR
    L[i] += u'〔案例%s〕%s' % (kb[1], nm)
    return L, i, u'以 %s%s 之題冠於 %s%s 之下（錯系）' % (ka[0], ka[1], kb[0], kb[1])


@plant(28)
def p28():
    L = list(BASE)
    i = prose(8)
    L[i] += u'〔案例·牙例〕'
    return L, i, u'立無號之〔案例·名〕形制'


@plant(29)
def p29():
    L = list(BASE)
    i = prose(8)
    L[i] += u'（迭代）'
    return L, i, u'落工程黑話『迭代』'


@plant(30)
def p30():
    L = list(BASE)
    i = prose(9)
    L[i] += u'《試探犍度》'
    return L, i, u'立語料所無之《試探犍度》'


# ── 尺身之植（24・32）：改尺之副本，須落 `_work/`（275 增第 31 目『目錄條與書身題依序對合』，
#     原第 31 目『目數自對合』順移為第 32 目，其針同移）
def src_copy(fn, tag):
    txt = fn(CHKTXT)
    p = os.path.join(WORK, u'r272tmp%s.py' % tag)
    io.open(p, u'w', encoding=u'utf-8').write(txt)
    return p


def p24():
    def fn(t):
        old = u"BP = os.path.join(ROOT, u'_print', u'build39.py')"
        assert t.count(old) == 1, u'24 目植錨非一'
        return t.replace(old, u"BP = os.path.join(ROOT, u'_print', u'no_such_build_r272.py')")
    return src_copy(fn, u'24'), None, u'產器不可讀（封面之數無從自算）'


@plant(31)
def p31():
    """275 之 v1 病如實重演：目錄第五章之第四節條，其題作第四章之第四節。"""
    L = list(BASE)
    i = find_line(lambda l, idx: Toc0 <= idx < BODY0 and l.strip().startswith(u'* 第四節　僧殘治法階梯與'))
    return L, repl(L, i, u'僧殘治法階梯與心性時間對沖律', u'管轄交界與組織防衛'), \
        u'目錄條改作他章同序列之題（不指空猶綠，今須報序不合）'


def p32():
    def fn(t):
        old = u"chk(u'書名號內之本律篇名須見於語料', [(u'尺自身出錯：%s' % e,)])"
        assert t.count(old) == 1, u'32 目植錨非一'
        return t.replace(old, u"chk(u'書名號內之本律篇名須見於語改', [(u'尺自身出錯：%s' % e,)])")
    return src_copy(fn, u'32'), None, u'except 支偷改目名（源印不對合）'


def p32b():
    def fn(t):
        old = u"chk(u'印面無空殼括號', bad)"
        assert t.count(old) == 1, u'32b 植錨非一'
        return t.replace(old, u"chk(u'印面無空殼括號%d 目', bad)")
    return src_copy(fn, u'32b'), None, u'目名內著佔位符（標籤摻計數）'


@plant(32)
def p32c():
    """281・生肉之植：於散文行內塞一段五十言無標點之「逐字」引文。
       （norm 別除標點，故逐字兩尺俱不覺——病只在印面之斷句，須此目接住。）"""
    L = list(BASE)
    i = prose(9)
    L[i] += (u'\u300c\u82e5\u6bd4\u4e18\u77e5\u662f\u6076\u7f6a\u898b\u5df2\u4e0d\u53ef\u55dc\u6012\u4e0d\u53ef\u89aa'
             u'\u606f\u4e0d\u53ef\u8207\u5171\u4e8b\u59cb\u7d42\u5b88\u6236\u5982\u6cd5\u8aaa\u6212\u5f53\u5982\u662f'
             u'\u5b78\u5ff5\u65e5\u591c\u4e0d\u5931\u826f\u5e2b\u53d6\u8207\u6b63\u89c0\u5ff5\u5fc3\u5f97\u5b9a\u610f'
             u'\u662f\u540d\u70ba\u521d\u591c\u300d')
    return L, i, u'\u690d\u4e00\u6bb5\u4e94\u5341\u8a00\u7121\u6a1e\u9ede\u4e4b\u9010\u5b57\u5f15\u6587'


PLANTS[39] = p32
PLANTS[24] = p24
EXTRA = {39: [(u'32b', p32b)], 22: [(u'22b', p22b)]}


@plant(37)
def p37name():
    """288・款級名實之植：號存而名錯（奉裁 D6『杜絕指針有其號而引錯其名』之自動防線）。
       靶＝〔調部專題 02』『第五章第五節第九款（與波羅夷戒）』——改掛他款之題『（物權返還先於受懺）』，
       其四字實在第五節第六款，故指針之章・節・款三級俱存，唯掛名不實：目 2（章節指針）與 v39secref 俱不識，
       唯第 37 目能紅（針尖單軸）。"""
    L = list(BASE)
    old = u'第五章第五節第九款（與波羅夷戒）'
    idx = find_line(lambda l, i: old in l)
    assert L[idx].count(old) == 1, u'37 植錨非一'
    L[idx] = L[idx].replace(old, u'第五章第五節第九款（物權返還先於受懺）')
    return L, idx, u'款級指針之掛名換作他款之題'


@plant(38)
def p38name():
    """292・退位名制之植：把已改名之『略戒心印』貼回舊名『略戒憲綱』。
       （舊名非錯字・非簡形・非黑話，歷尺俱不識——唯第 38 目能紅，針尖單軸。）"""
    L = list(BASE)
    old = u'三十二字略戒心印'
    i = find_line(lambda l, idx: old in l)
    assert L[i].count(old) == 1, u'38 植錨非一'
    L[i] = L[i].replace(old, u'三十二字略戒' + chr(0x61B2) + chr(0x7DB1))
    return L, i, u'舊名『憲綱』貼回一行（第 38 目之植）'


@plant(36)
def p36h1():
    """285・章級之植：把結語之 H1 改回分上下之形（一 H1 多題・章級分題之殘跡）。
       （章級條數未動・目錄條目不含結語，故唯第 36 目當紅——針尖單軸。）"""
    L = list(BASE)
    i = find_line(lambda l, idx: l.startswith(u'# 結語'))
    L[i] = L[i] + u'（上）'
    return L, i, u'H1 著（上）之分題形（285 新目之植）'


@plant(34)
def p34seq():
    """284・地標段序之植：把地標 05 之『三、』改作『六、』（序亂而段數不改，唯段序目能識）。"""
    L = list(BASE)
    i6 = next(i for i, l in enumerate(L) if l.startswith(u'# 第六章'))
    i = next(k for k in range(i6, len(L)) if L[k] == u'#### 三、佛陀處斷：三環決策推演')
    L[i] = u'#### 六、佛陀處斷：三環決策推演'
    return L, i, u'地標段序抽換一枚（一二六四五）'


@plant(35)
def p35bad():
    """284・黑單之植：在散文行內種一枚歷輪錯字『樞點』（281 落刀殘跡之形）。"""
    L = list(BASE)
    i = prose(11)
    L[i] += u'此處之標識，即全書校勘之樞點。'
    return L, i, u'種入黑單之『樞點』一枚'


@plant(33)
def p33mat():
    """282・速查之植：把一枚已改鑄之集群矩陣行，其爭點欄換回 276 補丁之模板套語。
       （此行處斷欄仍合式樣，故只該由第 33 目紅——針尖須單軸，免『一植多紅』。）"""
    L = list(BASE)
    i = find_line(lambda l, idx: l.startswith(u'| **〔案例 03〕') and u'**\u3010' in l)
    cells = L[i].split(u'|')
    assert len(cells) == 7, u'33 目植錨之欄數非 7：%d' % len(cells)
    assert u'犯緣與開緣' not in cells[3], u'33 目之靶已是套語（基線不綠）'
    cells[3] = u' 犯緣與開緣之界如何判？ '
    L[i] = u'|'.join(cells)
    return L, i, u'速查行爭點欄植回模板套語'


def run(args, book):
    p = subprocess.run([sys.executable, u'-X', u'utf8'] + args + [book],
                       capture_output=True, text=True, encoding=u'utf-8', env=env, cwd=ROOT)
    return p


def parse(out):
    red, names, n = [], [], 0
    for l in out.rstrip().split(u'\n'):
        m = re.match(u'^(.*\\S)\\s+(PASS|FAIL)(?:（.*）)?$', l)
        if not m:
            continue
        names.append(m.group(1))
        n += 1
        if m.group(2) == u'FAIL':
            red.append(m.group(1))
    return red, names, n


# ═════════ 跑 ═════════
tmp_base = os.path.join(TMPD, u'base.md')
io.open(tmp_base, u'w', encoding=u'utf-8').write(u'\n'.join(BASE))
bp = run([CHK], tmp_base)
bred, bnames, bn = parse(bp.stdout)
print(u'基線副本｜rc=%d・目 %d・紅 %s・stderr=%s' % (
    bp.returncode, bn, bred or u'無', (bp.stderr or u'').strip()[:120] or u'空'))
if bred or (bp.stderr or u'').strip():
    print(u'———— 基線不綠，整盤作廢（紅皆屬『因崩而紅』）')
    sys.exit(2)
N = bn

TMPF = []
rows = []
try:
    for k in range(1, N + 1):
        if k not in PLANTS:
            rows.append((u'%d' % k, u'未植', u'此目尚無針：%s' % bnames[k - 1][:26], u'新增之目須配植病'))
            continue
        items = [(u'%d' % k, PLANTS[k])] + [(t, f) for t, f in EXTRA.get(k, [])]
        for tag, fn in items:
            try:
                a, b, note = fn()
            except Exception as e:
                rows.append((tag, u'未植', u'%s' % e, u'—'))
                continue
            if isinstance(b, int):                       # 冊之副本
                path = os.path.join(TMPD, u'p%s.md' % tag)
                io.open(path, u'w', encoding=u'utf-8').write(u'\n'.join(a))
                chkpath, book = CHK, path
                TMPF.append(path)
            else:                                        # 尺之副本
                chkpath, book, path = a, tmp_base, a
                TMPF.append(chkpath)
            p = run([chkpath], book)
            red, names, nn = parse(p.stdout)
            tgt = bnames[k - 1]
            if (p.stderr or u'').strip() or nn != N:
                rows.append((tag, u'崩', note, u'%s' % (p.stderr or u'').strip()[:80]))
            elif tgt in red:
                rows.append((tag, u'逮', note, u'連帶紅 %d：%s' % (
                    len(red), u'、'.join(x[:12] for x in red if x != tgt) or u'無')))
            else:
                rows.append((tag, u'未逮', note, u'全紅=%s' % (red or u'無')))
    for k in sorted(set(PLANTS) - set(range(1, N + 1))):
        rows.append((u'%d' % k, u'殭針', u'針無目可植（尺上已無第 %d 目）' % k, PLANTS[k].__name__))
finally:
    for pth in TMPF + [tmp_base]:
        try:
            os.remove(pth)
        except OSError:
            pass
    try:
        os.rmdir(TMPD)
    except OSError:
        pass

NG = 0
for tag, verdict, note, extra in rows:
    if verdict != u'逮':
        NG += 1
    print(u'%-4s %-3s %-34s %s' % (tag, verdict, note[:34], extra))
ndai = sum(1 for r in rows if r[1] == u'逮')
print(u'———— 牙列矩陣：目 %d・針 %d・逮 %d・欠 %d' % (N, len(rows), ndai, NG))
sys.exit(1 if NG else 0)
