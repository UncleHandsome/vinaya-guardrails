# -*- coding: utf-8 -*-
r"""292・甲組刀（去撞車・兩軌化・正名 J 案・第一章淨空四奪・附錄六定位）。

口徑：rep 逐錨須命中數相符；rep_pat 以正則計數；del_line／ins_after 以行定位。
乾跑只印不寫；寫檔之換行只在一處（內容 LF，落盤一次轉 CRLF）。
"""
import hashlib
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
APPLY = u'--apply' in sys.argv

RAW = io.open(SRC, 'rb').read()
SHA0 = hashlib.sha256(RAW.replace(b'\r\n', b'\n')).hexdigest()[:12]
T = RAW.decode('utf-8').replace(u'\r\n', u'\n')
L = T.split(u'\n')
LOG = []


def rep(old, new, label, expect=1):
    n = sum(x.count(old) for x in L)
    assert n == expect, u'%s：命中 %d 枚（須 %d）➔ %s' % (label, n, expect, old[:24])
    for i, x in enumerate(L):
        if old in x:
            L[i] = x.replace(old, new)
            LOG.append(u'%-24s L%-5d ×%d' % (label, i + 1, x.count(old)))


def rep_pat(pat, repl, label, expect):
    n = 0
    for i, x in enumerate(L):
        y, k = re.subn(pat, repl, x)
        if k:
            L[i] = y
            n += k
            LOG.append(u'%-24s L%-5d ×%d' % (label, i + 1, k))
    assert n == expect, u'%s：正則命中 %d 枚（須 %d）' % (label, n, expect)


def one_idx(anchor, k=0):
    idx = [i for i, x in enumerate(L) if anchor in x]
    assert len(idx) > k, u'錨不見：%s' % anchor[:20]
    return idx[k]


def one_line(anchor):
    idx = [i for i, x in enumerate(L) if anchor in x]
    assert len(idx) == 1, u'錨非一：%s（%d 處）' % (anchor[:20], len(idx))
    return idx[0]


# ── 一・雙重八項之解撞（卷首）────────────────────────────────────
rep(u'這三十二字，即是統攝全書的**八重憲綱**：',
    u'這三十二字是行者**修己之鏡**，本書稱作**略戒心印（八句）**；統攝全書法度之尺則**唯有一組**，'
    u'即第一章第二節之**八大正理**。鏡與尺分屬兩軌，**不得合讀為十六條根本原則**：',
    u'卷首・鏡尺分軌宣告')
rep(u'8. **法庭關閉（常樂空閑）**：知足止足；', u'8. **案結人歸（常樂空閑）**：知足止足；', u'八目・案結人歸')
rep(u'3. **最小侵害（蜂採其華）**：', u'3. **如蜂採華（不損一枝）**：', u'八目・如蜂採華')
rep(u'5. **前瞻避險（明眼避險）**：', u'5. **明眼先避（上醫治未病）**：', u'八目・明眼先避')
# 八目清單之後立界說
i = one_line(u'8. **案結人歸（常樂空閑）**')
L.insert(i + 1, u'')
L.insert(i + 2, u'> **【此八目之界說】**：八目者，三十二字心印之別名也，**非與八大正理並立之法度**。'
                u'名雖近法，義在修己——開庭稱量唯用八大正理，平日內照唯誦此三十二字；'
                u'八目與八理之間有親有疏，取其義近，不取其一對一之形。')
LOG.append(u'%-24s L%-5d 插 2 行' % (u'卷首・八目界說', i + 1))
rep(u'體上之每一句，即用上之每一尺；鏡與尺，一物也。',
    u'體上之每一句，為用上之每一尺所自出之源；源不必逐字譯為尺——八句是大地，八尺是急診，'
    u'兩兩相形唯取其近（自淨其意之於正理五、不惱他人之於正理六，皆義近而非同項）。',
    u'第一章・去同一性')
# 卷首導航・三十二字略戒憲綱之名保留為「體」，惟加口訣於詩偈之下
i = one_idx(u'> **善護三業，但自觀行；蜂採其華，不惱他人；**')   # 卷首第一處
L.insert(i + 3, u'> 〔定錨口訣〕修己之鏡，斷案之尺；平日但持三十二字，公堂唯依八大正理。'
                u'**鏡不量人，尺不離案。**')
L.insert(i + 4, u'')
LOG.append(u'%-24s L%-5d 插 2 行' % (u'卷首・定錨口訣', i + 3))

# ── 二・隨身三鏡併入夜半四照（第三章定義・第八章四塊・結語印卡・目錄括註）──
rep(u'#### 三、隨身三鏡（腳下三問）', u'#### 三、腳下三問（夜半四照之收攝）', u'三章・三鏡題')
rep(u'六閘門是給審理者的詳圖，三鏡則是行者日用經行時的隨身尺：',
    u'六閘門是給審理者的詳圖，腳下三問則是行者日用經行時的隨身尺——此三問乃第七章【夜半四照】之收攝'
    u'（省其第二照・動機一步），不另立一套口訣：', u'三章・三鏡句')
rep(u'* **第一鏡·照境想（初環見真實）**', u'* **照境想（初環見真實）**', u'三章・照境想')
rep(u'* **第二鏡·照邊界（次環安僧伽）**', u'* **照邊界（次環安僧伽）**', u'三章・照邊界')
rep(u'* **第三鏡·照解脫（終環入無事）**', u'* **照解脫（終環入無事）**', u'三章・照解脫')
rep(u'###### 【法相診斷與三鏡分判】', u'###### 【法相診斷與腳下三問】', u'八章・診斷題', expect=4)
B7 = chr(0x00B7)
rep(u'**第一鏡（照境想' + B7 + u'初環見真實）**', u'**照境想（初環見真實）**', u'八章・照境想', expect=4)
rep(u'**第二鏡（照邊界' + B7 + u'次環安僧伽）**', u'**照邊界（次環安僧伽）**', u'八章・照邊界', expect=4)
rep(u'**第三鏡（照解脫' + B7 + u'終環入無事）**', u'**照解脫（終環入無事）**', u'八章・照解脫', expect=4)
rep(u'三鏡、諸問與諸口訣，皆此兩軌之枝目', u'諸問與諸口訣，皆此兩軌之枝目', u'七章・枝目句')
rep(u'三鏡作隨身速查', u'三問作隨身速查', u'三章・導航句')
rep(u'檢查六門、隨身三鏡、', u'檢查六門、腳下三問、', u'目錄・第三章括註')
rep(u'【用·三鏡照心印】（臨事急診·三環照鏡）', u'【用·四照察心印】（臨事急診·夜半四照）', u'結語・用印名')
rep(u'一鏡照境想（心事相應、無心不罪）', u'照境想（心事相應、無心不罪）', u'結語・照境想')
rep(u'二鏡照邊界（世間信心', u'照邊界（世間信心', u'結語・照邊界')
rep(u'三鏡照解脫（更生復權', u'照解脫（更生復權', u'結語・照解脫')

# ── 三・現代案例正名：J ➔ 現（先改凡例，後洗次碼，免錨隨改名而漂移）──
rep(u'又 `〔案例 J-1〕`〜`〔案例 J-4〕` 之 J，乃本書歷版編列**現代深水案例**一錄之次'
    u'（舊稿作附錄 J，自標『研讀備查，不計入百則』）：',
    u'又 `〔案例 現-1〕`〜`〔案例 現-4〕` 之『現』，乃本書**現代演繹案例**（四境）之次'
    u'（三十九版以前作附錄 J，自標『研讀備查，不計入百則』；今去其字母之跡，'
    u'正名曰『現』，取『現代因緣所演』之義，非律藏原生之號）：', u'凡例・現字之義')
rep(u'演繹現代深水案例 ', u'現代演繹案 ', u'八章・深水易名', expect=5)
rep_pat(u'J-([1-4])', u'現-\\1', u'全書・J 碼➔現碼', expect=14)

# ── 四・第一章判準層級表淨空四奪（列移出表外，另立明橋）───────────────
i = one_line(u'除偏鏡（不入判準層級）')
LOG.append(u'%-24s L%-5d 除表列 1 行' % (u'一章・四奪列表外', i + 1))
del L[i]
rep(u'| **舉報自察層** | **舉罪五德** |', u'| **舉報自察層** | **舉罪五德** |', u'錨校（表末行仍在）')
i = one_line(u'第八章調查實務指針 |')
L.insert(i + 1, u'')
L.insert(i + 2, u'> **除偏鏡不入表**：臨濟四奪（奪人不奪境之屬）**無規範拘束力，不與上三層同列**，'
                u'故不載於此表；其為審理者臨場磨刀之心理衛生指針，具見本節第二款與附錄一『臨濟四奪行持矩陣』。')
LOG.append(u'%-24s L%-5d 插明橋 2 行' % (u'一章・除偏鏡明橋', i + 1))

# ── 五・附錄六與第六章之關係句加嚴（消『次等附錄』之感）──────────────────
rep(u'故本書只有**一座**判例法典（第六章），此篇是其深描層，非別立一庫。',
    u'故本書只有**一座**判例法典（第六章），此篇是其深加工之層——**非別立一庫，亦非次等之附錄**：'
    u'欲窮一案之原典，看附錄四；欲窮一理之隱微，看此十五題。十五則之編次止於『深描』之序，'
    u'不另立案號，亦不與 102 案爭數。', u'附錄六・非次等')

OUT = u'\n'.join(L)
sys.path.insert(0, os.path.join(ROOT, u'_work'))
import _simpmap as SM                                   # noqa: E402
import _simpdict as SD                                   # noqa: E402
SIMPS = set(getattr(SM, 'MAP', {})) | set(getattr(SD, 'MAP', {}))
newbad = sorted(({c for c in OUT if c in SIMPS} - {c for c in T if c in SIMPS}))
print(u'簡形新增：%s' % (u''.join(newbad) or u'無'))
for c in newbad:
    j = OUT.find(c)
    print(u'   %s U+%04X｜…%s…' % (c, ord(c), OUT[max(0, j - 22):j + 12].replace(u'\n', u' ')))
print(u'刀數：%d｜行數 %d ➔ %d' % (len(LOG), len(T.split(u'\n')), len(L)))
for x in LOG:
    print(u'  ' + x)
if not APPLY:
    print(u'（乾跑・未寫檔。）')
    sys.exit(0)
assert not newbad, u'簡形未淨'
B = OUT.replace(u'\n', u'\r\n').encode('utf-8')
io.open(SRC, 'wb').write(B)
print(u'寫畢：%dB｜CRLF %d｜sha %s ➔ %s' % (len(B), B.count(b'\r\n'), SHA0,
      hashlib.sha256(OUT.encode('utf-8')).hexdigest()[:12]))
io.open(os.path.join(ROOT, u'_work', u'r292cutlogA.txt'), 'w', encoding='utf-8', newline='\n').write(
    u'\n'.join(LOG) + u'\n')
