# -*- coding: utf-8 -*-
"""292・丙組刀（現代四境演繹判例正名與位階・出堂洗心三事之職能歸一・目錄幽靈名）。

口徑：逐字之句不重打——第四章舊款內『**「…」…**』一語自原行摘出，原樣移入新款；
      改段以行範圍整替（先斷言起訖之錨），寫檔之換行只在一處；簡形新增須為零。
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
            LOG.append(u'%-22s L%-5d ×%d' % (label, i + 1, x.count(old)))


def rep_pat(pat, repl, label, expect):
    n = 0
    for i, x in enumerate(L):
        y, k = re.subn(pat, repl, x)
        if k:
            L[i] = y
            n += k
    assert n == expect, u'%s：正則命中 %d 枚（須 %d）' % (label, n, expect)
    LOG.append(u'%-22s 正則 ×%d' % (label, n))


# ── 一・現碼之形制：J-1 ➔ 現-1 ➔ 現01（去連字號之工程跡），並正集体之名 ──
rep_pat(u'現代演繹案 現-([1-4])', u'四境演繹判例 現0\\1', u'題・四境演繹判例', 5)
rep_pat(u'現-([1-4])', u'現0\\1', u'全書・現碼補零', 11)

# ── 二・凡例：去『次等』之語，立四境之義 ────────────────────────────
rep(u'：此四案乃本書依今時因緣所推演，非律藏原生之判例，故不占第六章 102 案之純數字號，'
    u'亦不與古典判例同列既證之位——升格則混『既證』與『推演』為一類，壞判例底冊之文獻性，'
    u'今一仍其舊而明其義。',
    u'：此四案者，本書總名之曰**【現代四境演繹判例】**，分嵌第八章第二・三・四節。'
    u'乃依佛陀『隨犯隨制、因病與藥』之立法本懷，就今時道場之四深境——精神控制・數位冷暴力・'
    u'財務假帳・長照耗竭——所作之法相推演。其所異於古典判例者，在『未經歷代既證』，'
    u'不在『位階尊卑』：故不占第六章 102 案之純數字號，別立『現』字之次，自成一類。'
    u'立次所以可引可據，非編外次等之謂；引此四案者得據其理，**不得援為佛言**。',
    u'凡例・四境判例之義')

# ── 三・第八章開卷導航立【現代四境演繹判例之義】 ──────────────────────
i = [k for k, x in enumerate(L) if x.startswith(u'> 本章所引三線模型、法人治理、除斥期間')]
assert len(i) == 1, u'第八章導航錨命中 %d' % len(i)
i = i[0]
if not L[i].endswith(u'  '):
    L[i] = L[i] + u'  '
BLK = [
    u'>',
    u'> **【現代四境演繹判例之義】**  ',
    u'> 本章另立四案，總名**【現代四境演繹判例】**（〔現01〕〜〔現04〕，分嵌本章第二・三・四節）：'
    u'〔現01〕以消業為名之靈性壓榨、〔現02〕長照耗竭之冷漠轉身、〔現03〕通訊同溫層之群體孤立案、'
    u'〔現04〕以『法尚應捨』掩蓋帳目不清案。四案非律藏原生之判，乃本書依佛陀『隨犯隨制、因病與藥』'
    u'之立法本懷，就二十一世紀道場四深境所作之**法相推演**——其證不取於古代律文，取於今時因緣之結構'
    u'與制戒之理。其所異於古典 102 案者，在『未經歷代既證』，不在『位階尊卑』；引之者得據其理，'
    u'**不得援為佛言**，亦不得徑入戒相主文。',
]
L[i + 1:i + 1] = BLK
LOG.append(u'%-22s L%-5d 插 %d 行（第八章導航）' % (u'八章・四境之義', i + 1, len(BLK)))

# ── 四・第四章第七節第二款：三事儀軌交還第七章，此款只立程序法定終結 ──
a = [k for k, x in enumerate(L) if x.startswith(u'#### 二、程序終結之消磁宣告')]
assert len(a) == 1, u'第四章款題錨命中 %d' % len(a)
a = a[0]
QUOTE = re.search(u'\\*\\*「[^」]*」\\*\\*', u'\n'.join(L[a:a + 20]))
assert QUOTE, u'第四章之逐字句不得見'
QUOTE = QUOTE.group(0)
end = a
while L[end].strip() != u'---':
    end += 1
    assert end < a + 40, u'第四章款之終界不可求（逾 40 行）'
NEW = [
    u'#### 二、程序終結之法定宣告（一裁不翻・卷宗歸檔）',
    u'',
    u'白四羯磨宣告結案之後，裁判卷宗即刻落鎖封存，送入機密檔案庫；法庭當日依律作三重法定宣告：',
    u'',
    u'1. **語業歸零（口業之禁）**：全體參與者嚴禁在寮房、走廊、茶席間私下議論案情半句。律有明敕：'
    + QUOTE + u'口舌蔓延即是犯罪，再翻舊帳者本人結波逸提。',
    u'2. **法庭關閉（一事不再理）**：同一案情，非依四瑕疵非常平反之道，不得重啟調查、複議或再舉；'
    u'卷宗銷號歸檔，程序之確定力自此成立。',
    u'3. **身意還虛非本章之職**：至何時換衣、執何器具、睡前誦何辭句——『出堂洗心三事』之身心儀軌'
    u'具在第七章第五節，一制兩面，不復重出。',
    u'',
]
LOG.append(u'%-22s L%-5d〜%-5d 整款換作 %d 行（逐字句原樣移入）'
           % (u'四章・程序終結歸職', a + 1, end, len(NEW)))
L[a:end] = NEW
# 流程圖之尾標與目錄之括註同步
rep(u'（出堂洗心三事：退回阿蘭若）', u'（案卷封存・銷號歸檔・退回阿蘭若）', u'四章・流程圖尾標')
rep(u'（訴訟全流程圖、消磁宣告：出堂洗心三事）',
    u'（訴訟全流程圖、程序終結之法定宣告）', u'目錄・第四章第七節')
rep(u'反靈性煤氣燈操縱令', u'反靈性煤氣燈操縱防護禁約', u'目錄・幽靈令名')

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
print(u'行數 %d ➔ %d｜刀數 %d' % (len(T.split(u'\n')), len(L), len(LOG)))
for x in LOG:
    print(u'  ' + x)
print(u'—— 新插・改寫之文（目視）——')
for anchor in (u'> **【現代四境演繹判例之義】**', u'#### 二、程序終結之法定宣告'):
    k = [q for q, x in enumerate(L) if x.startswith(anchor)][0]
    for q in range(k - 1, min(k + 6, len(L))):
        print(u'  L%d｜%s' % (q + 1, L[q][:300]))
    print(u'  …')
if not APPLY:
    print(u'（乾跑・未寫檔。）')
    sys.exit(0)
assert not newbad, u'簡形未淨'
B = OUT.replace(u'\n', u'\r\n').encode('utf-8')
io.open(SRC, 'wb').write(B)
print(u'寫畢：%dB｜CRLF %d｜bareCR %d｜sha %s ➔ %s' % (
    len(B), B.count(b'\r\n'), B.count(b'\r') - B.count(b'\r\n'), SHA0,
    hashlib.sha256(OUT.encode('utf-8')).hexdigest()[:12]))
