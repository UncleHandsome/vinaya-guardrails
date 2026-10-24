# -*- coding: utf-8 -*-
"""272 輪・SOP 改帳之第二器：自備份重敷（前器以 \\uXXXX 造句，反因**我記錯碼位**而生錯字：異➔鄧・綴➔編）。

今制：① 起點取 `_work/r272sop.bak`（改帳前之原檔），一律重敷，不在汙檔上補丁；
      ② **錨**仍以 ASCII 與 \\uXXXX 求（傳遞層無從更動），**插入之文**改回漢字直打；
      ③ 打完另次呼叫以 codepoint 掃（新出之字逐一認明），有錯字則帶錨單改——**器不靠目驗，亦不靠我記碼**。
"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, u'\u5217\u5370SOP.md')
BAK = os.path.join(ROOT, u'_work', u'r272sop.bak')
T = io.open(BAK, encoding=u'utf-8').read()
L = T.split(u'\n')
log = []


def must1(txt, plain, tag):
    assert txt.count(plain) == 1, u'%s｜錨非一（%d 中）' % (tag, txt.count(plain))
    return txt


# ══ ① 今制行：積輪 21➔22・272 之 clause
i0 = next(i for i, l in enumerate(L) if l.startswith(u'- **\u4e09\u5341\u4e5d\u7248\u4eca\u5236'))
s = must1(L[i0], u'21**', u'\u2460').replace(u'21**', u'22**')
j = s.rfind(u'\uff09', 0, s.index('PDF'))
assert j > 0, u'\u2460 括不可求'
CLAUSE = u'\u3001' + u'272 之立第 31 目『目數自對合』，並添第九尺『牙列矩陣』（逐目植病三十二針俱逮・冊身一字未動）'
L[i0] = s[:j] + CLAUSE + s[j:]
log.append(u'\u2460')

# ══ ② 公約行：輪號・三十一目・近六目・一行跑九尺・30/31 兩目之說・r272teeth 入列
i1 = next(i for i, l in enumerate(L) if l.startswith(u'- **') and u'\u67e5\u6838\u516c\u7d04' in l and i != i0)
s = L[i1]
cand = [p for p in range(len(s)) if s.startswith(u'271', p) and u'255' in s[max(0, p - 10):p]]
assert len(cand) == 1, u'\u2461a（%d 候選）' % len(cand)
p = cand[0]
s = s[:p] + u'272' + s[p + 3:]
for plain, new, tag in [(u'\u4e8c\u5341\u4e5d\u76ee', u'\u4e09\u5341\u4e00\u76ee', u'\u2461b'),
                        (u'\u8fd1\u56db\u76ee', u'\u8fd1\u516d\u76ee', u'\u2461c'),
                        (u'\u4e00\u884c\u8dd1\u516b\u5c3a', u'\u4e00\u884c\u8dd1\u4e5d\u5c3a', u'\u2461d')]:
    s = must1(s, plain, tag).replace(plain, new)
m1 = s.index(u'26\uff0f28\uff0f29')
DESC = (u'\u3001' + u'30『書名號內之本律篇名須見於語料』（271 輪立：只認含『犍度』之《X》，'
        u'前綴須剝、異體須折、總數之稱須擲）、'
        u'31『目數自對合』（272 輪立：逕讀 `__file__`，目名須常量、try/except 兩支同名、'
        u'源中唯一名數＝實印目數，『不變量 N/N』之 N 自此不再全憑尺之自報）、')
s = s[:m1] + DESC + s[m1:]
last = s.rindex('v39apx4chk') + len('v39apx4chk')
assert s[last] == u'\uff09', u'\u2461e 列未閉'
L[i1] = s[:last] + u'、**r272teeth**' + s[last:]
log.append(u'\u2461')

# ══ ③ 歷輪條目：於 271 條之後另起一行（272 之案內）
i2 = next(i for i, l in enumerate(L) if l.startswith(u'  **') and 'ec1bd4242914' in l)
E272 = (u'  **第 272 輪・尺之尺（牙列矩陣）：三十一目逐目植病**（本輪**純器**，印面一字未動，前後 SHA 同 `ec1bd4242914`）' +
        u'——承 271 債⑥。① **先量己帳**（`_work/r272probe.py`）：v39chk 內 `chk()` 33 呼・去重目名 31・'
        u'**源印不對合**，其因即第 30 目之 except 支偷改目名（try 長而 except 短），'
        u'故『不變量 30/30 全綠』之 30 本身是一項無人核過的宣稱；'
        u'② **立第 31 目『目數自對合』**：不另立名冊，逕讀 `__file__`——目名含 % 佔位即駁、'
        u'except 之名須見於 try、源中唯一名數＝實印目數（#10・#29・#30 之目名改回常量，計數移入 detail）；'
        u'③ **立第九尺 `_work/r272teeth.py`**：歷輪負測皆一輪一植，餘目之牙從未同時校過——'
        u'今逐目植一枚最小之病於**冊之副本**（tempdir，ROOT 不落新檔；24・31 兩目之病在產器與尺身，'
        u'故改**尺之副本**，跑畢即除），斷言該目必紅。四則自約：**基線副本必先全綠**' +
        u'（否則一切紅皆屬『因崩而紅』，整盤作廢退 2）・尺崩報『崩』不報『逮』・錨不可求報『未植』不許默過・'
        u'**目數不寫死**（N 自基線推得：增目而無針即『未植』退 1，廢目而針存即『殭針』退 1——增目有債、廢目有殭）。'
        u'**三十二針俱逮・欠 0**；連帶紅者如實列（一植多紅＝該針非針尖，只作記錄不作病）。'
        u'④ **矩陣之負測 `_work/r272neg.py`**：鈍針（29 目改空寫）➔『未逮』退 1・'
        u'失錨（26 目找不到落點）➔『未植』退 1・病基（基線副本先帶一枚黑話）➔『基線不綠』退 2，三針俱中、stderr 空。'
        u'⑤ 跑批今為**九尺**（`v39battery.py`：鑰欄正則加『牙列』，摘錄加『逮／植／針／崩』四形，'
        u'並明記『第九尺退碼非 0 時須補針，不可遽刪目』——刪目即自廢其牙）。'
        u'**自犯四則**：① Write 後立即執行又讀到半檔（r272neg 初報 format 錯，未改一字覆跑即中）；'
        u'② **矩陣初版把『31』寫死**——正是 271 債①在同日自犯，改自基線推 N；'
        u'③ 植病之注自落簡形二枚・英字脫漏一枚，由 codepoint 掃現形（目驗時顯示層亦會替我改字）；'
        u'④ **罕字之疑先查舊帳**：『鑰』（U+9470）本對，我依記憶改作 U+9430『鎰』反成錯字——' +
        u'幸前一道掃已證 U+9470 在舊檔凡 23 見；自此之治：**新文之罕字必先與舊帳比現，舊帳屢見者即我記錯碼位**，'
        u'且同因又以 \\uXXXX 造 SOP 之插入句生出『折鄧』『前編』兩錯（異 U+5F02・綴 U+7E6E）➔ '
        u'**記碼不如抄檔**：插入之文改回漢字直打，打完以『新出之字逐一認明』覆核。'
        u'**今量：9,340 行・968,565 B・SHA `ec1bd4242914`（印面未動）｜九尺齊跑全綠・不變量 31/31' +
        u'（源 31／印 31）・牙列矩陣 32 針逮 32 欠 0**｜負測十三支俱中且 stderr 俱空。'
        u'⚠ **積輪 22**（本輪未動冊）。**債之下一軸**：牙列只證『能紅』未證『紅得準』，'
        u'且一目只植一針（一目多枝者未逐枝植：8 目之簡形單・29 目之兩張名單・27 目之兩枝・10 目之兩枝）。')
L.insert(i2 + 1, E272)
log.append(u'\u2462')

io.open(P, 'w', encoding=u'utf-8').write(u'\n'.join(L))
t2 = io.open(P, encoding=u'utf-8').read()
assert u'\u4e09\u5341\u4e00\u76ee' in t2 and u'**r272teeth**' in t2 and t2.count(u'272 \u8f2b') >= 2
print(u'\u5df2\u843d\u5730\uff1a' + u' | '.join(log) + u'｜%d \u884c\uff08\u539f %d\uff09' % (len(t2.split(u'\n')), len(L) - 1))
