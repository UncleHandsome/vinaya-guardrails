# -*- coding: utf-8 -*-
r"""290・三層入帳：日誌（掃簡形・純附加）、SOP（印面行＋新條）、記憶（狀態檔＋索引）、備份。"""
import hashlib
import io
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, u'_work'))
sys.path.insert(0, ROOT)
import _simpmap as SM                                    # noqa: E402
import _simpdict as SD                                   # noqa: E402

SIMPS = set(getattr(SM, 'MAP', {})) | set(getattr(SD, 'MAP', {}))
BOOKP = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
BOOK = io.open(BOOKP, encoding='utf-8').read()
SHA = hashlib.sha256(BOOK.replace('\r\n', '\n').encode('utf-8')).hexdigest()[:12]
LINES = len(BOOK.replace('\r\n', '\n').split('\n'))
print(u'冊：%d 行・sha %s' % (LINES, SHA))

para = io.open(os.path.join(ROOT, u'_work', u'r290para.txt'), encoding='utf-8').read()
para = para.replace(u'目連公養', u'目連公案').replace(u'4cb4061a354b', SHA)
para = para.replace(u'今冊 **8,274 行（+2：地標拆段＋1・附錄六立界＋1）・`e56b9f4dce8e`**',
                    u'今冊 **%d 行（+2：地標拆段＋1・附錄六立界＋1）・`%s`**' % (LINES, SHA))
bad = sorted({c for c in para if c in SIMPS and c not in BOOK})
print(u'日誌稿簡形：%s' % (u''.join(bad) or u'無'))
for c in bad:
    j = para.find(c)
    print(u'   %s U+%04X｜…%s…' % (c, ord(c), para[max(0, j - 22):j + 12].replace(u'\n', u' ')))
assert not bad, u'簡形未淨，先改'
io.open(os.path.join(ROOT, u'_archive', u'備份', u'ver39.pre291.md'), 'wb').write(
    io.open(BOOKP, 'rb').read())
D = os.path.join(ROOT, u'_archive', u'編年工程日誌.md')
raw = io.open(D, 'rb').read().decode('utf-8').replace('\r\n', '\n')
before = raw
out = (raw.rstrip('\n') + '\n' + para).replace('\n', '\r\n').encode('utf-8')
io.open(D, 'wb').write(out)
print(u'日誌：%d 行・%dB｜純附加：%s' % (len(out.decode('utf-8').split('\r\n')), len(out),
      before.replace('\r\n', '\n').rstrip('\n') in raw.replace('\r\n', '\n')))

# ── SOP ──────────────────────────────────────────────────────────
S = os.path.join(ROOT, u'列印SOP.md')
sop = io.open(S, encoding='utf-8').read()
A = (u'- **印面**：**積輪 1**（289 之八刀未出冊，奉令方建；上一次重建為 288：完整版影印與螢幕**各 261 頁**・'
     u'大綱 146＝目錄印出 146・定位失敗 0；今冊 8,272 行・sha256（LF 形）`152486628736`；')
assert sop.count(A) == 1, u'錨 A：%d' % sop.count(A)
sop = sop.replace(A, u'- **印面**：**積輪 2**（289・290 兩輪之刀俱未出冊，奉令方建；上一次重建為 288：'
                     u'完整版影印與螢幕**各 261 頁**・大綱 146＝目錄印出 146・定位失敗 0；'
                     u'今冊 %d 行・sha256（LF 形）`%s`；' % (LINES, SHA))
C = u'- **第 289 輪・法理穿透校勘之文獻歸真**'
Creal = u'- **第 289 輪'
assert sop.count(Creal) == 1, u'錨 C：%d' % sop.count(Creal)
NEW = (u'- **第 290 輪・外路第十七報告（CBETA 深層覆核）・本地篇聚序之發現**：'
       u'量得二十二至三十卷分段檔內有『一百七十八單提法之一〜七』之序，且一行題『四分律卷第二十七・二分之六・明尼戒法』'
       u'正在『之四』之上 ➔ 之四⇔卷廿七、之六⇔卷廿九、之七⇔卷三十，**本地可推卷次之一路由此開**；'
       u'案 86 之引文在『之六』段 ➔ 卷二十七改**卷二十九**（矩陣與附錄四兩載體，旁證為本冊自引案 92 之卷三十恰應『之七』）。'
       u'地標 05 一段冠『卷四十五』而前段唯見 11-21 檔 ➔ **拆為兩出處**（前歸卷十二・波逸提第十二條，與本章同戒之既有引卷歸一；'
       u'後段兩說俱相容，留卷四十五並存外來說卷四十三）。附錄六『L###』之冠稱由『大正藏卷段』改『本地卷段』（11 枚）'
       u'並**立界說**（L＝檔內行號，非 T22 冊頁欄行；v39linchk 之 36 號 15 行俱仍中，因 RNG2 只認『卷段 50-60』之體）。'
       u'『有難教與不受訓導』判為**偽病灶**——本地正作『一有難教二不受訓導』，冊文一仍本地，只記異文不改字。'
       u'結小界／解界兩段各存外來說之卷三十五／卷三十四（『受戒犍度』本地實見、『說戒犍度』本地無之）。'
       u'今量：核卷 **137** 合／0 不合／18 未證・宣稱 155 處・十尺全綠。**積輪 2**。'
       u'⚠自犯：新文註內混入英文亂碼一枚，由自查目視得之——**簡形掃不得代目視**。\n')
sop = sop.replace(Creal, NEW + Creal)
io.open(S, 'wb').write(sop.encode('utf-8'))
print(u'SOP：%d 行' % len(sop.split('\n')))

# ── 記憶・狀態檔 ───────────────────────────────────────────────────
MEM = u'C:/Users/lionc/.qoder/projects/C--Users-lionc-OneDrive-----------------/memory'
P = os.path.join(MEM, u'project-round31-state.md')
raw = io.open(P, encoding='utf-8').read()
A1 = u'description: 戒律分析專案現況（第 289 輪・外路第十六報告 CBETA 逐字比對）'
assert raw.count(A1) == 1
raw = raw.replace(A1, u'description: 戒律分析專案現況（第 290 輪・外路第十七報告＋本地篇聚序之發現）')
A2 = u'**8,272 行・sha256 152486628736**・**積輪 1（289 八刀未出冊，奉令方建；'
assert raw.count(A2) == 1, raw.count(A2)
raw = raw.replace(A2, u'**8,274 行・sha256 %s**・**積輪 2（289・290 兩輪俱未出冊，奉令方建；' % SHA)
H = u'# 現況快照（截至 2026-10-26・第 289 輪）'
assert raw.count(H) == 1
raw = raw.replace(H, u'# 現況快照（截至 2026-10-26・第 290 輪）')
ANCH = u'**第 289 輪・外路第十六報告（CBETA 逐字比對六事）之文獻歸真**'
assert raw.count(ANCH) == 1
NEWP = (u'**第 290 輪・外路第十七報告（CBETA 深層覆核五事）與本地篇聚序之發現**（起點 `152486628736`・'
        u'今 **%d 行・`%s`**；報告五事：實病三・偽病灶一・精確化一；刀十四＋補刀一）。'
        u'**本地新證（最重要）**：22-30 檔內有『一百七十八單提法之一〜七』之序，且 running head'
        u'『四分律卷第二十七・二分之六・明尼戒法』恰在『之四』之上 ➔ **之四⇔卷廿七・之六⇔卷廿九・之七⇔卷三十，'
        u'本地可推卷次之一路開**；案 86 之引文在『之六』段 ➔ 冊作卷二十七為實誤，兩載體俱改卷二十九'
        u'（旁證：本冊自引案 92 作卷三十，恰應『之七』）；**並立約於附錄四導言**：引文落於可推之篇聚段內者，其卷隨段定'
        u'（此屬本地可推，與外來校語之『存其說』有別）。⚠帳上之債：287・288 之『六檔唯見兩卷題』仍真，'
        u'然余只數卷題未查篇聚序，致一處真誤活了十餘輪。'
        u'**地標 05**：一段冠『卷四十五』而前段『我不見罪…當名作餘語』**唯見 11-21 檔**（本地正面可駁）➔拆兩出處，'
        u'前歸『卷十二・波逸提第十二條』（與本章 L4670 同戒引卷歸一），後段兩說俱相容故留卷四十五並存外來說卷四十三。'
        u'**附錄六 L 標法**：『大正藏卷段』11 枚改『本地卷段』＋導言立界說（L###＝檔內行號，非 T22 冊頁欄行）；'
        u'v39linchk 36 號／15 行俱仍中（其 RNG2 只認『卷段 50-60』之體）。'
        u'**偽病灶**：『有難教』——本地五十至六十檔正作『一有難教二不受訓導』，冊一仍本地，只記異文不改字'
        u'（同族：『狂性自歇』有『復』、『婆裘河』）。**結小界／解界**兩段各存外來說卷三十五／卷三十四'
        u'（『受戒犍度』本地實見 1、『說戒犍度』0）。**無誤清單復核**：案 89・03・94・98・06 之卷次與本地檔段俱相容。'
        u'**今量**：宣稱 155 處・核卷 **136➔137**／0／18 如舊・十尺全綠（牙列 40 針俱逮）・**積輪 2**。'
        u'**自犯**：新文註內混入英文亂碼一枚（『之headsequentially』），簡形掃與諸尺俱不識，由自查目視得之'
        u'——**長括註新文寫畢須印全文目視一過；器只擋它认得的病**。'
        u'**檔**：r290cuts・r290cuts2・r290probe1/2/3・備份 ver39.pre291.md。\n\n') % (LINES, SHA)
raw = raw.replace(ANCH, NEWP + ANCH)
A3 = (u'**正本**：根目錄 `ver39…修正版.md`（**8,272 行・sha256 前 12 碼 `152486628736`**；'
      u'289 前（＝288 末）8,272 行／`7ce1dbbd806f`')
assert raw.count(A3) == 1, u'錨 A3'
raw = raw.replace(A3, u'**正本**：根目錄 `ver39…修正版.md`（**%d 行・sha256 前 12 碼 `%s`**；'
                      u'290 前（＝289 末）8,272 行／`152486628736`，289 前（＝288 末）8,272 行／`7ce1dbbd806f`'
                      % (LINES, SHA))
A4 = u'**印面今制（276 建・284〜288 五度重建・今積輪 1＝289 八刀未出冊）**'
assert raw.count(A4) == 1
raw = raw.replace(A4, u'**印面今制（276 建・284〜288 五度重建・今積輪 2＝289・290 兩輪未出冊）**')
bad2 = sorted({c for c in raw if c in SIMPS and c not in BOOK})
print(u'狀態檔簡形（冊中所無）：%s' % (u''.join(bad2) or u'無'))
io.open(P, 'wb').write(raw.encode('utf-8'))
print(u'狀態檔：%d 行' % len(raw.split('\n')))

# ── 記憶・索引 ───────────────────────────────────────────────────
Q = os.path.join(MEM, u'MEMORY.md')
s = io.open(Q, encoding='utf-8').read()
B1 = u'**第 289 輪止（2026-10-26）**：ver39 正本 **8,272 行・sha256 `152486628736`**'
assert s.count(B1) == 1, u'B1：%d' % s.count(B1)
s = s.replace(B1, u'**第 290 輪止（2026-10-26）**：ver39 正本 **%d 行・sha256 `%s`**' % (LINES, SHA))
B2 = u'・**積輪 1**（289 八刀未出冊；'
assert s.count(B2) == 1
s = s.replace(B2, u'・**積輪 2**（289・290 兩輪未出冊；')
B3 = u'核卷 136/0/18'
assert s.count(B3) == 1
s = s.replace(B3, u'核卷 137/0/18')
B4 = u'289 收外路第十六報告'
assert s.count(B4) == 1
HEAD = (u'290 收外路第十七報告（五事：實病三・偽病灶一・精確化一）**並發現本地可推卷次之新路**：'
        u'22-30 檔存有『一百七十八單提法之一〜七』之序，running head『卷第二十七・二分之六・明尼戒法』正在『之四』上'
        u'➔之四⇔卷廿七、之六⇔卷廿九；案 86 引文落『之六』段 ➔ 卷二十七改**卷二十九**（兩載體；旁證案 92 作卷三十恰應『之七』），'
        u'並立約於附錄四導言（篇聚可推者其卷隨段定，與外來說之存其說有別）；地標 05 一段冠一卷（前段唯見 11-21 檔）➔拆兩出處，'
        u'前歸卷十二；附錄六『大正藏卷段』11 枚改『本地卷段』＋L### 立界說（檔內行號，非 T22 冊頁欄）；'
        u'『有難教』判偽病灶（本地正作『一有難教二不受訓導』，只記異文不改字）；結小界／解界各存卷三十五／卷三十四之說。'
        u'⚠自犯：新文混入英文亂碼一枚，器不識、由目視得之。')
s = s.replace(B4, HEAD + B4)
bad3 = sorted({c for c in s if c in SIMPS and c not in BOOK})
print(u'索引簡形：%s' % (u''.join(bad3) or u'無（錯字供狀除外則另計）'))
io.open(Q, 'wb').write(s.encode('utf-8'))
print(u'索引：%d 行' % len(s.split('\n')))
