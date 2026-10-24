# -*- coding: utf-8 -*-
"""第 278 輪・收口五刀（乾跑印命中數，帶參 --apply 方落盤；備份 _work/ver39.pre278.md）。

甲 L2704 引文換真逐字（語料 11-21 檔之結戒文，非 38-49 檔之犍度轉引）
乙 L7581 案例25 之卷次如實歸『未細核』（本地無逐卷之題，其文落 38-49 檔）
丙 L424 目錄之『繇諸卡自報』歸實（卡已廢，今為案號定義載體）
丁 非染污端之孤行歸組（清淨軌之續，報 38 案始合）
戊 附錄四指針補『卷次未細核』之界（不作俱合之論）
"""
import hashlib
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
BAK = os.path.join(ROOT, u'_work', u'ver39.pre278.md')
APPLY = u'--apply' in sys.argv

txt = io.open(BOOK, encoding=u'utf-8-sig').read()
LINES = txt.split(u'\n')


def sha(s):
    return hashlib.sha256(s.encode(u'utf-8')).hexdigest()[:12]


print(u'正本 %d 行・sha %s' % (len(LINES), sha(txt)))

# ── 甲：真逐字自語料切片（勿憑記憶重打）
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, u'_work'))
import _tk                                                     # noqa: E402
import v39align                                                # noqa: E402

GOLD = u''
for fn, raw, nt, nm in v39align.CORPUS:
    if not fn.startswith(u'11-21'):
        continue
    m = re.search(u'若比丘[^。]{0,20}如法滅已，後更發起者，波逸提。', raw)
    GOLD = m.group(0) if m else u''
assert GOLD and len(GOLD) <= 30, u'語料之候選結戒文不真：%r' % GOLD
OLD_A = LINES[2703]
assert u'若比丘如法諍事滅已，後更發起者，得波逸提。' in OLD_A, u'甲・錨不中：%s' % OLD_A[:60]
NEW_A = OLD_A.replace(u'「若比丘如法諍事滅已，後更發起者，得波逸提。」',
                      u'「%s」' % GOLD)
assert NEW_A != OLD_A and GOLD in NEW_A
LINES[2703] = NEW_A
print(u'甲｜L2704 引文 ➔ 語料作『%s』（%d 字）' % (GOLD, len(GOLD)))

# ── 乙：案例25 之卷次
OLD_B = LINES[7580]
assert OLD_B.startswith(u'| **〔案例 25〕') and u'卷三十六·說戒犍度下' in OLD_B, u'乙・錨不中'
NEW_B = OLD_B.replace(u'卷三十六·說戒犍度下',
                      u'卷次未細核・文在本地三十八至四十九卷分段檔·僧殘治法羯磨之段')
assert NEW_B != OLD_B
LINES[7580] = NEW_B
print(u'乙｜L7581 定位欄 ➔ 卷次未細核（分段檔）')

# ── 丙：目錄之卡形宣稱
OLD_C = LINES[423]
assert OLD_C.strip().startswith(u'* 附錄四') and u'繇諸卡自報' in OLD_C, u'丙・錨不中'
NEW_C = OLD_C.replace(u'繇諸卡自報', u'繇第六章案號定義載體匯出')
assert NEW_C != OLD_C and u'繇諸卡' not in NEW_C
LINES[423] = NEW_C
print(u'丙｜L424 目錄條 ➔ 案號定義載體匯出')

# ── 丁：孤行歸組（非染污端・清淨軌之續）
ORPH = 6291                                                     # 0-based ➔ L6292
assert LINES[ORPH].strip().startswith(u'〔案例13〕落水救拔'), u'丁・孤行錨不中：%s' % LINES[ORPH][:40]
assert LINES[6285].strip().startswith(u'* **清淨軌'), u'丁・清淨軌錨不中'
orphan = LINES[ORPH].strip().rstrip(u'。')
n_ref = len(re.findall(u'〔案例 ?0*(\\d+)(?![0-9])', orphan))
assert n_ref == 9, u'丁・孤行之案數非常（今 %d）' % n_ref
LINES[6285] = LINES[6285].rstrip()[: -1] + u'、' + orphan + u'；'
del LINES[ORPH]
print(u'丁｜孤行 9 枚併入清淨軌（原 L6292 除・區內行號自是而後上移一）')

# ── 戊：附錄四指針之界（戊在丁之後，故行號須重算）
i5 = next(k for k, l in enumerate(LINES) if u'凡原典逐字可證者' in l)
OLD_E = LINES[i5]
anchor = u'其標『律意』之攝述段，引卷未及復核，回查時姑存之。'
assert anchor in OLD_E, u'戊・錨不中'
NEW_E = OLD_E.replace(anchor, anchor[: -1] + u'；表中自標『卷次未細核』者，因本地電子文本無逐卷之題，'
                                        u'唯記其分段檔所在，不作俱合之論。')
assert NEW_E != OLD_E
LINES[i5] = NEW_E
print(u'戊｜L%d 附錄四指針 ➔ 補『卷次未細核』之界' % (i5 + 1))

out = u'\n'.join(LINES)
print(u'改後 %d 行・sha %s' % (len(LINES), sha(out)))
if not APPLY:
    print(u'（乾跑・未落盤。加 --apply 方寫入，備份在 _work/ver39.pre278.md）')
    sys.exit(0)
if not os.path.exists(BAK):
    io.open(BAK, 'w', encoding=u'utf-8').write(txt)
    print(u'備份 ➔ %s' % BAK)
io.open(BOOK, 'w', encoding=u'utf-8').write(out)
back = io.open(BOOK, encoding=u'utf-8-sig').read()
print(u'落盤訖・讀回 %d 行・sha %s・同 out=%s' % (
    len(back.split(chr(10))), sha(back), back == out))
