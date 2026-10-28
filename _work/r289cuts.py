# -*- coding: utf-8 -*-
r"""第 289 輪・外路第十六報告（CBETA 逐字比對六事）之落刀。

口徑：逐刀 rep(old,new,label[,expect]) 須命中數相符；先乾跑印錨，--apply 方落盤。
寫檔換行只在一處換（內容一律 LF，落盤一次轉 CRLF）；新文俱以直書漢字，寫畢掃簡形。
"""
import hashlib
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
APPLY = u'--apply' in sys.argv

RAW = io.open(SRC, 'rb').read()
SHA0 = hashlib.sha256(RAW.replace(b'\r\n', b'\n')).hexdigest()
TEXT = RAW.decode('utf-8').replace(u'\r\n', u'\n')
L = TEXT.split(u'\n')
LOG = []


def rep(old, new, label, expect=1):
    n = sum(x.count(old) for x in L)
    assert n == expect, u'%s：命中 %d 枚（須 %d）➔ %s' % (label, n, expect, old[:26])
    for i, x in enumerate(L):
        if old in x:
            L[i] = x.replace(old, new)
            LOG.append(u'%-22s L%-5d 命中 %d' % (label, i + 1, x.count(old)))
    return n


# ── 一・目連牽臂公案：混合引文歸真（報告一之 1，本地語料俱證）────────────
rep(u'> 佛陀當場宣示：「**怪哉目連！何乃造次！自今已去我更不說戒，汝等自共說戒……'
    u'自今已去聽作自言治，若不自言不應治。**」（《四分律》卷三十五·說戒犍度）',
    u'> 佛陀當場宣示：「汝今不應為，後亦不應為。目連！自今已去，聽作自言治，若不自言不應治。'
    u'自今已去，汝等自作羯磨說戒。」（《四分律》文在本地三十一至三十七卷分段檔・瞻婆國伽伽河側布薩之段；'
    u'卷次據外來校語作卷三十六，說戒犍度乃外來篇題，本地文本無此題。'
    u'舊稿此引嘗混『怪哉目連』『何乃造次』『我更不說戒』『汝等自共說戒』四語——'
    u'本地六十卷分段檔核無此文，前一句或出他部之律，後三語今俱無從指實，故削，不充逐字之數）',
    u'目連引文歸真')

# ── 二・波逸提第六十六條之卷次（報告一之 2；本冊他載體已證 64・67 兩條俱作卷十七）──
rep(u'（《四分律》卷十九·波逸提法第六十六條）',
    u'（《四分律》卷十七·波逸提法第六十六條，文在本地十一至二十一卷分段檔）',
    u'第六十六條卷次歸一')

# ── 三・閘門六『原典卷次未標』之補齊（報告二之 2；本地 50-60 檔俱證，篇題毘尼增一實見語料）──
rep(u'《四分律》（原典卷次未標）列『不受』於不得解脫之法：',
    u'《四分律》卷五十七·毘尼增一（文在本地五十至六十卷分段檔）列『不受』於不得解脫之法：',
    u'未標卷次補齊')

# ── 四・兩案『卷次未細核』存其說（報告三・二事；俱與本地檔段相容，唯無逐卷之題）──────
rep(u'（外來校語謂在卷三十八，與此檔段相容，惜無逐卷之題可證） |',
    u'（外來說有二：一謂卷三十八，一謂卷四十五・人犍度，俱與此檔段相容，惜本地無逐卷之題，故仍標未細核） |',
    u'案二十五存二說')
MID, DOT = chr(0x30FB), chr(0x00B7)
A69 = (u'| **〔案例 69〕誤入眠婦室看門相** | 卷次未細核' + MID +
       u'文在本地三十八至四十九卷分段檔（另有外來卷次之說，與此檔段不相容，故不取） |')
rep(A69, A69.replace(u'（另有外來卷次之說，與此檔段不相容，故不取）',
                     u'（外來說有二：前說與此檔段不相容，故不取；'
                     u'今說作卷四十九・法犍度，與此檔段相容，存其說，'
                     u'唯本地無逐卷之題，故仍標未細核）'),
    u'案六十九存新說')
rep(u'> **《四分律》卷次未細核（文在本地三十八至四十九卷分段檔' + DOT + u'僧殘治法羯磨之段）' + DOT + u'大正藏 No. 1428**',
    u'> **《四分律》卷次未細核（文在本地三十八至四十九卷分段檔' + DOT +
    u'僧殘治法羯磨之段；外來說有二，俱與檔段相容，唯無逐卷之題可證）' + DOT + u'大正藏 No. 1428**',
    u'正文羯磨段之界')

# ── 五・《五支物主經》：撮述之句去單層引號＋自標未覆核之界（報告二之 1；本地未收此典）──
rep(u'此「漏」字之法相，佛陀於阿含早期經卷中早有清澈開示。《中阿含經》第 179《五支物主經》云：',
    u'此「漏」字之法相，佛陀於阿含早期經卷中早有清澈開示。《中阿含經》第 179《五支物主經》云'
    u'（此經為本地語料所未收，二段依通行本照錄、未及就地覆核，其次第亦依本書義理之便而非經文之次）：',
    u'中阿含自標其界')
rep(u'> 「如異學沙門文祁子所說，若當爾者，嬰孩童子支節柔軟，仰向臥眠，亦當成就善、第一善、無上士，'
    u'得第一義、質直沙門。何以故？嬰孩童子未有身、口、意業，何況有罪！」',
    u'> 「如異學沙門文祁子所說，若當爾者，嬰孩童子支節柔軟，仰向臥眠，亦當成就善、第一善、無上士，'
    u'得第一義、質直沙門。」——其義撮之曰『嬰孩童子未有身口意業，何況有罪』，非經文之逐字，'
    u'故依凡例第二律，別以雙層角引號出之。',
    u'撮述之句降層')

# ── 校驗 ──────────────────────────────────────────────────────────
OUT = u'\n'.join(L)
sys.path.insert(0, os.path.join(ROOT, u'_work'))
import _simpmap as SM                                   # noqa: E402
import _simpdict as SD                                   # noqa: E402
SIMPS = set(getattr(SM, 'MAP', {})) | set(getattr(SD, 'MAP', {}))
before = sorted({c for c in TEXT if c in SIMPS})
after = sorted({c for c in OUT if c in SIMPS})
print(u'簡形：起點『%s』➔ 今『%s』' % (u''.join(before) or u'無', u''.join(after) or u'無'))
newbad = sorted(set(after) - set(before))
print(u'新增簡形：%s' % (u''.join(newbad) or u'無'))
print(u'刀數：%d｜行數 %d ➔ %d' % (len(LOG), len(TEXT.split(u'\n')), len(L)))
for x in LOG:
    print(u'  ' + x)
if not APPLY:
    print(u'（乾跑・未寫檔。加 --apply 方落盤。）')
    sys.exit(0)
assert not newbad, u'簡形新增：%s' % newbad
B = OUT.replace(u'\n', u'\r\n').encode('utf-8')
io.open(SRC, 'wb').write(B)
print(u'寫畢：%dB｜CRLF %d｜CR %d｜sha256(LF) %s（起點 %s）'
      % (len(B), B.count(b'\r\n'), B.count(b'\r'),
         hashlib.sha256(OUT.encode('utf-8')).hexdigest()[:12], SHA0[:12]))
io.open(os.path.join(ROOT, u'_work', u'r289cutlog.txt'), 'w', encoding='utf-8', newline='\n').write(
    u'\n'.join(LOG) + u'\n')
