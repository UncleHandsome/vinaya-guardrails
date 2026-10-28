# -*- coding: utf-8 -*-
r"""第 290 輪・外路第十七報告（CBETA 深層覆核五事＋無誤清單）之落刀。

本地新證：22-30 檔內存『四分律卷第二十七（二分之六）明尼戒法』之 running head，且緊接
『一百七十八單提法之四』——之四↔卷廿七・之五↔卷廿八・之六↔卷廿九・之七↔卷三十 一一對應；
案 86 之引文在『之六』段（檔內 80985／之六起 78384），故冊作『卷二十七』為實誤，可就地判。
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


def rep_lines(anchor, block, label, take=None):
    """以唯一錨行起、連 take 行整段換作 block（塊內各行自帶行尾，不併行）。"""
    idx = [i for i, x in enumerate(L) if anchor in x]
    assert len(idx) == 1, u'%s：錨行見 %d 處' % (label, len(idx))
    k = take if take else len(block)
    assert L[idx[0] + k - 1].startswith(u'> ') or k == 1, u'%s：吞到非引文行' % label
    L[idx[0]:idx[0] + k] = block
    LOG.append(u'%-22s L%-5d 換 %d 行 ➔ %d 行' % (label, idx[0] + 1, k, len(block)))


# ── 一・案 86 卷次（本地篇聚序可證・兩載體俱改）────────────────────────
rep(u'《四分律》卷二十七<br>（比丘尼波逸提法）',
    u'《四分律》卷二十九<br>（明尼戒法·一百七十八單提法之六）', u'案八十六卷次（矩陣）')
rep(u'| **〔案例 86〕二部衝突持械圍攻** | 卷二十七·比丘尼波逸提法 |',
    u'| **〔案例 86〕二部衝突持械圍攻** | 卷二十九·明尼戒法'
    u'（本地檔內之篇聚序作『一百七十八單提法之六』；檔存『卷第二十七・二分之六・明尼戒法』之題恰在『單提法之四』上，故之四⇔卷廿七、之六⇔卷廿九，可推而證） |',
    u'案八十六卷次（附錄四）')

# ── 二・地標 05 一段冠一卷之混淆（前段本地唯見 11-21 檔，卷四十五正面違反）──────
rep_lines(u'> **《四分律》卷四十五（呵責犍度第十一之餘·作餘語與三舉）·大正藏 No. 1428**',
          [u'> **《四分律》卷十二（波逸提法第十二條·妄作異語惱他戒之因緣續文）·大正藏 No. 1428**'
           u'〔文在本地十一至二十一卷分段檔〕  ',
           u'> 「『我不見罪，云何言我有罪？』……『時世尊以無數方便呵責闡陀比丘已，告諸比丘：'
           u'自今已去聽白已，當名作餘語。』」  ',
           u'> **《四分律》卷四十五（呵責犍度之餘·三舉不同住）·大正藏 No. 1428**'
           u'〔文在本地三十八至四十九卷分段檔；外來說作卷四十三·拘睒彌犍度，兩說俱與檔段相容，'
           u'本地無逐卷之題，故存其說而不據以改判〕  ',
           u'> 「『云何僧與作不同住？僧與作不見犯羯磨、不懺悔羯磨、惡見不捨羯磨，'
           u'是為僧與作不同住。』」'],
          u'地標零五拆兩出處', take=3)

# ── 三・『有難教』——本地語料正作『一有難教』，判為偽病灶，惟記異文 ──────────
rep(u'邪見與邊見、有難教與不受訓導）。',
    u'邪見與邊見、有難教與不受訓導）——⚠異文如實記：本地五十至六十卷分段檔此處正作『一有難教二不受訓導』，'
    u'他校本或作『一難教』，今一仍本地之文，不隨外來校語改字。',
    u'難教之異文記帳')

# ── 四・附錄六 L 行號之標法（『大正藏卷段』易滋誤會，改『本地卷段』並立界說）──────
rep(u'大正藏卷段', u'本地卷段', u'卷段冠稱歸實', expect=11)
rep(u'> 每案皆完整保留**「原典文獻定位、事相因緣、佛陀判語、法理核心與心理動力學、法理要旨、正理參照」**六大維度，'
    u'為僧伽司法與現代法人治理提供最堅硬的法理底冊。  ',
    u'> 每案皆完整保留**「原典文獻定位、事相因緣、佛陀判語、法理核心與心理動力學、法理要旨、正理參照」**六大維度，'
    u'為僧伽司法與現代法人治理提供最堅硬的法理底冊。  \n'
    u'> 又一：『原典文獻定位』欄內之 **L###「乃本地六十卷分段檔之檔內行號」**，為編者就地覆核逐字之所慟；'
    u'**非大正藏之冊頁欄行號**（T22・頁・欄・行）。本地電子文本不具逐卷之題，故卷次之據外來校語而存其說者，'
    u'皆如實標明其界，不充『就地覆核已畢』之數。',
    u'附錄六立行號之界')

# ── 五・結小界與解界兩段之卷次（俱與本地 31-37 檔相容，依約存其說）───────────
rep(u'（《四分律》文在本地三十一至三十七卷分段檔・結小界之段；所附說戒犍度之題乃外來篇題，本地文本無此題）',
    u'（《四分律》文在本地三十一至三十七卷分段檔：結小界說戒之段，外來校語作卷三十五·說戒犍度初；'
    u'解界羯磨之段，外來校語作卷三十四·受戒犍度之四——『受戒犍度』之名本地語料實見，'
    u'『說戒犍度』之題本地文本無之；兩卷之說俱與檔段相容，唯本地無逐卷之題，故存其說而不據以改判）',
    u'結小界兩段存卷說')

# ── 校驗 ────────────────────────────────────────────────────────
OUT = u'\n'.join(L)
sys.path.insert(0, os.path.join(ROOT, u'_work'))
import _simpmap as SM                                   # noqa: E402
import _simpdict as SD                                   # noqa: E402
SIMPS = set(getattr(SM, 'MAP', {})) | set(getattr(SD, 'MAP', {}))
before = sorted({c for c in TEXT if c in SIMPS})
after = sorted({c for c in OUT if c in SIMPS})
newbad = sorted(set(after) - set(before))
print(u'簡形：起點『%s』➔ 今『%s』｜新增：%s' % (u''.join(before) or u'無',
      u''.join(after) or u'無', u''.join(newbad) or u'無'))
for c in newbad:
    j = OUT.find(c)
    print(u'   %s U+%04X｜…%s…' % (c, ord(c), OUT[max(0, j - 24):j + 14].replace(u'\n', u' ')))
print(u'刀數：%d｜行數 %d ➔ %d' % (len(LOG), len(TEXT.split(u'\n')), len(L)))
for x in LOG:
    print(u'  ' + x)
if not APPLY:
    print(u'（乾跑・未寫檔。加 --apply 方落盤。）')
    sys.exit(0)
assert not newbad, u'簡形新增，先改正'
B = OUT.replace(u'\n', u'\r\n').encode('utf-8')
io.open(SRC, 'wb').write(B)
print(u'寫畢：%dB｜CRLF %d｜CR %d｜sha256(LF) %s（起點 %s）'
      % (len(B), B.count(b'\r\n'), B.count(b'\r'),
         hashlib.sha256(OUT.encode('utf-8')).hexdigest()[:12], SHA0[:12]))
io.open(os.path.join(ROOT, u'_work', u'r290cutlog.txt'), 'w', encoding='utf-8', newline='\n').write(
    u'\n'.join(LOG) + u'\n')
