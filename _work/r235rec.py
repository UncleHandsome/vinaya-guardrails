# -*- coding: utf-8 -*-
"""第 235 輪記錄器：校勘記・編年・readchk 碼內註・列印SOP 四檔同動，逐一回讀斷其恰一。"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER = os.path.join(ROOT, u'ver38四分律_起心動念心智分析框架_修正版.md')
GO = u'--go' in sys.argv

MK234 = u'234. **第兩百三十四輪'
MK233 = u'量訖而不立之維（第 233 輪・款題之容器'

REC = [
    u'235. **第兩百三十五輪（附錄L『23 筆』與 F-3『19 列』本非一口徑：兩向相攝立為不變量 94，兼擭緊 r190f3 之丙桶）**',
    u'**一、所為與查證法**：第 234 輪如實落檔之待診一筆（外路謂附錄L 稱 23 筆俱開列於 F-3 而今列唯 19，差 4）本輪逐筆親配——以 F-3 各列『所在』欄括號內之法理位置，回指本表（F-1・F-2）之行首欄。得 23 筆散布 16 行、為 18 列所攝（第 12・18 兩列各攝三筆，第 15 列攝二筆），第 13 列明標『屬名相所出，非逐字引文』而不攝筆 ⇒ **筆筆有所列（遺 0）、列列無虛指（除 13）**，『差 4』乃以列數代筆數，非缺帳。',
    u'**二、隨動（俱在底冊與器，印面一字未動）**：`_tk.py` 新立 `f3_rows()`（取首欄序號自算 F-3 列數，今得 19）與 `f3_map()`（兩向相攝）；`_work/rows2.py` 遂於附錄L 之 F 列末補一句『該表以典籍·版本為列，一列可攝同段之數筆，故今 **19** 列與筆數本非一口徑』（+41 字，母數 13,764 不動、行內改寫）；`_tk.py check` 該列 want 加 `str(f3_rows())`，此數自此不許與表脫鉤。',
    u'**三、升閘一條**：不變量 93→**94**「附錄F-3 與本表兩向相攝（列有所指・筆有所列；列數不強等於筆數）」。植病三路俱抓退（甲·改一列之所在為虛構名目→列無所指、乙·刪整列→筆無所列、丙·改本表首欄之名→兩向俱退），陰性對照原檔 94/94；器留 `_work/r235gate.py`。',
    u'**四、器瘡一樁**：`_work/r190f3.py` 之丙桶舊唯問『行內有宣稱語而無《》』，遂把揭露之器自身的自述撈入 11 筆（F-3 篇題與表列、附錄F 與附錄E 篇首凡例、卷首目錄）。今立三層豁免（附錄F 篇內不較・行內須有八字以上「」之逐字形貌而所引非篇目職分・已以〔案〕就地標界者不較），丙 11→**0**；負測一枚陽性（自陳未收而具逐字形貌）仍被抓、兩枚陰性不復報 ⇒ **尺可緊而眼不可盲，緊尺之驗在陽性猶現**。',
    u'**五、終測**：`_tk.py check` **94/94**、`battery` **51 軸零病**、`ledger` 差 0、`verify bqa` 87／0／11／26（百分之百，附錄L 無須隨動）、三掃俱淨；印面含圍欄 346,671・剔圍欄 333,870・圍欄內 12,801 三數俱不動（刀唯在底冊）；`syncchk` 仍 418／366 ⇒ **四式候令如故**（仍屬第 223 輪之冊 406／279）。',
]
REC = [l.replace(u'・', u'·') for l in REC]   # 主檔通例作 U+00B7（・入主檔即犯隔號之檢）

LOG = [
    u'235. **第兩百三十五輪（F-3 之列與本表之筆兩向相攝，立為不變量 94；r190f3 之丙桶擭緊）**',
    u'**所為**：第 234 輪待診一筆今以逐筆配列斷訖——23 筆散布 16 行、為 18 列所攝（一列攝三筆・二筆各有），第 13 列名相不攝筆，故 19 列與 23 筆本非一口徑，外路之『差 4』是以列數代筆數。',
    u'**器與帳**：`_tk.py` 立 `f3_rows()`・`f3_map()`；`rows2.py` 於附錄L 之 F 列末補列數一句（+41 字，母數不動）；該列 want 收 `f3_rows()`。不變量 93→**94**，植病三路俱退、陰性 94/94。',
    u'**擭尺**：`r190f3` 之丙桶 11→**0**（三層豁免：附錄F 篇內・無逐字形貌・案語已標界），陽性負測仍抓——**擭緊之驗在陽性猶現，非在其數歸零**。',
    u'**終測**：94/94・51 軸零病・台帳差 0・bqa 百分之百；印面三數不動（刀唯在底冊），`syncchk` 418／366 如故 ⇒ 四式候令（仍屬 223 之 406／279）。',
    u'',
]

NOTE = [
    u'量訖而不立之維（第 235 輪・筆列兩口徑之攝、擭尺之驗）',
    u' ① **一數兩式者不以對齊其數為治，以立其相攝為治**——附錄L 之 23（未標界 14＋已標界 9）與 F-3 之 19 本非同物：列以典籍·版本為單位，一列可攝同段數筆，另有名相列不攝筆。今不改兩數以求等（改則虛報），而立 `f3_map()` 校其相攝（列列須有所指、筆筆須有所列），脫節方退——**兩口徑之債以映射封之，不以數字封之**。',
    u' ② **擭緊驗器之尺，其驗在陽性猶現**——`r190f3` 丙桶之 11 筆俱是揭露之器自己的自述（篇題・凡例・目錄・表列），豁免三層後歸 0；然歸零本身不證尺良，須另植一枚陽性（行內自陳未收而具「」八字以上逐字形貌）仍被抓，方知緊尺未盲。',
    u' ③ **底冊之改不動印面三數**——本輪刀唯附錄L 一行（底冊），故含圍欄 346,671・剔圍欄 333,870・圍欄內 12,801 三數俱不動，`syncchk` 亦仍 418／366；凡刀全在底冊之輪，終測應報『三數不動』而非『同差 +N』。',
    u'',
]

SOP = [
    u'- **一數兩式之債，立相攝不立等式（第 235 輪）**：全書常有同一事物之兩式計數（附錄L 之『23 筆』對 F-3 之『19 列』、外路遂報『差 4』）。**不得改其數字以求等**（改即虛報），亦不得只記『口徑不同』而無驗——應以自算器立**兩向相攝**（列列須有所指、筆筆須有所列），並把兩式之數各收進 want 與不變量，使任何一方增刪而未隨動者當場退。參第 105 輪『不復手載死數』、第 231 輪『兩口徑同差之律有界』。',
    u'',
]


def load(p):
    return io.open(p, encoding='utf-8').read().split(u'\n')


sys.path.insert(0, os.path.join(ROOT, u'_work'))
import recordsimp as _ri  # noqa: E402  （簡形名單以記錄檔自掃器為法源；主檔另有其閘）

_SIMP = set(_ri.S)
for _nm, _blk, _gate in ((u'校勘記', REC, True), (u'編年', LOG, False),
                         (u'readchk 註', NOTE, False), (u'SOP', SOP, False)):
    _txt = u'\n'.join(_blk)
    _bad = sorted({c for c in _txt if c in _SIMP})
    assert not _bad, u'%s 含簡形 %s' % (_nm, _bad)
    assert u'\\' not in _txt, u'%s 含反斜線' % _nm
    for _l in _blk:
        assert _l == _l.rstrip(), u'%s 行末有空白' % _nm
        assert _l.count(u'*') % 2 == 0, u'%s 星成對有缺：%s' % (_nm, _l[:40])
        if _gate:
            assert u'\u30fb' not in _l, u'%s 主檔禁日式隔號 U+30FB' % _nm
print(u'刀前自查四層（簡形・反斜線・星成對・行末・主檔隔號）俱淨 ✓')


def save(p, lines):
    io.open(p, 'w', encoding='utf-8', newline=u'\n').write(u'\n'.join(lines))


def ins_after(lines, marker, block, which):
    i = next((k for k, l in enumerate(lines) if l.startswith(marker)), None)
    assert i is not None, u'未尋得錨點：%s（%s）' % (marker[:24], which)
    assert sum(1 for l in lines if l.startswith(marker)) == 1, u'錨點非恰一：%s' % which
    j = i
    while j + 1 < len(lines) and lines[j + 1].strip():
        j += 1
    return lines[:j + 1] + block + lines[j + 1:], j + 1


rep = {}
ml = load(MASTER)
new_ml, at = ins_after(ml, MK234, [u''] + REC, u'校勘記 234 條之末')
assert sum(1 for l in new_ml if l.startswith(u'235. **第兩百三十五輪')) == 1
assert len(new_ml) - len(ml) == len(REC) + 1, u'校勘記應 +%d 行' % (len(REC) + 1)
rep[u'校勘記'] = (len(ml), len(new_ml), at + 1)

lg = load(os.path.join(ROOT, u'_archive', u'編年工程日誌.md'))
while lg and not lg[-1].strip():
    lg.pop()
new_lg = lg + [u''] + LOG
rep[u'編年'] = (len(lg), len(new_lg), 0)

rc = load(os.path.join(ROOT, u'_work', 'readchk.py'))
new_rc, rat = ins_after(rc, u' ③ **新增指針之副作用在證源之範圍**', NOTE, u'readchk ③ 指針之末')
rep[u'readchk'] = (len(rc), len(new_rc), rat + 1)

sp = load(os.path.join(ROOT, u'列印SOP.md'))
tail = [l for l in sp if l.startswith(u'- **加指針之前先問證源之範圍')]
assert len(tail) == 1, u'SOP 錨點非恰一'
i = next(k for k, l in enumerate(sp) if l.startswith(u'- **加指針之前先問證源之範圍'))
new_sp = sp[:i + 1] + [u''] + SOP + sp[i + 1:]
rep[u'SOP'] = (len(sp), len(new_sp), i + 1)

for k, (a, b, c) in rep.items():
    print(u'%-6s %d → %d 行（插於 L%d 之後）' % (k, a, b, c))

if not GO:
    print(u'（未寫檔：加 --go）')
    sys.exit(0)

save(MASTER, new_ml)
save(os.path.join(ROOT, u'_archive', u'編年工程日誌.md'), new_lg)
save(os.path.join(ROOT, u'_work', 'readchk.py'), new_rc)
save(os.path.join(ROOT, u'列印SOP.md'), new_sp)

# 回讀自證：逐檔斷其恰一
for f, blk in ((MASTER, REC), (os.path.join(ROOT, u'_archive', u'編年工程日誌.md'), LOG),
               (os.path.join(ROOT, u'_work', 'readchk.py'), NOTE),
               (os.path.join(ROOT, u'列印SOP.md'), SOP)):
    t2 = u'\n'.join(load(f))
    for line in blk:
        if not line.strip():
            continue
        n = t2.count(line[:60])
        assert n >= 1, u'%s 缺：%s' % (os.path.basename(f), line[:40])
    print(u'回讀 %-22s 俱在 ✓（%d 行）' % (os.path.basename(f), len(load(f))))
bom = open(MASTER, 'rb').read()
print(u'主檔母數 %d・CR %d' % (len(load(MASTER)), bom.count(b'\r')))
