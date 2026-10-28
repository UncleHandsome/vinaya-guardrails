# -*- coding: utf-8 -*-
r"""289・日誌與 SOP 入帳（積輪如實記 1，不虛報 0）。"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, u'_work'))
import _simpmap as SM                                   # noqa: E402
import _simpdict as SD                                   # noqa: E402

SIMPS = set(getattr(SM, 'MAP', {})) | set(getattr(SD, 'MAP', {}))
BOOK = io.open(os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md'),
               encoding='utf-8').read()
para = io.open(os.path.join(ROOT, u'_work', u'r289para.txt'), encoding='utf-8').read()
bad = sorted({c for c in para if c in SIMPS and c not in BOOK})
print(u'日誌稿簡形：%s' % (u''.join(bad) or u'無'))
for c in bad:
    j = para.find(c)
    print(u'   %s U+%04X｜…%s…' % (c, ord(c), para[max(0, j - 22):j + 14].replace(u'\n', u' ')))
assert not bad, u'日誌稿有簡形，先改正再入帳'

D = os.path.join(ROOT, u'_archive', u'編年工程日誌.md')
raw = io.open(D, 'rb').read().decode('utf-8').replace('\r\n', '\n')
out = (raw.rstrip('\n') + '\n' + para).replace('\n', '\r\n').encode('utf-8')
io.open(D, 'wb').write(out)
print(u'日誌：%d 行・%dB' % (len(out.decode('utf-8').split('\r\n')), len(out)))

S = os.path.join(ROOT, u'列印SOP.md')
sop = io.open(S, encoding='utf-8').read()
A = (u'- **印面**：**積輪 0**（288 重建：完整版影印與螢幕**各 261 頁**・大綱 146＝目錄印出 146・'
     u'定位失敗 0；冊 8,272 行・sha256（LF 形）`7ce1dbbd806f`；')
B = (u'- **印面**：**積輪 1**（289 之八刀未出冊，奉令方建；上一次重建為 288：完整版影印與螢幕**各 261 頁**・'
     u'大綱 146＝目錄印出 146・定位失敗 0；今冊 8,272 行・sha256（LF 形）`152486628736`；')
assert sop.count(A) == 1, u'錨 A：%d' % sop.count(A)
sop = sop.replace(A, B)

C = u'- **第 288 輪・奉第四次親裁之收斂與立尺（甲乙丙丁四組逐項定奪）**：'
NEW = (u'- **第 289 輪・外路第十六報告（CBETA 逐字比對）之文獻歸真**：六事俱真，八刀俱中。'
       u'目連牽臂之引文係混合——「怪哉目連／何乃造次／我更不說戒／汝等自共說戒」四語本地六十卷分段檔全無，'
       u'報告所擬卷三十六原文四句俱各 1 見於 31-37 檔，故改引真逐字並記削語之由；'
       u'波逸提第六十六條引卷 卷十九➔卷十七（據本冊他載體之 64・67 兩條俱作卷十七，三條同群而 66 獨異，'
       u'屬自家不相容，非據外部分卷表炫精確）；閘門六『原典卷次未標』補作卷五十七・毘尼增一'
       u'（篇題『毘尼增一』本地語料實有 7 見，五句俱見 50-60 檔）；案 25・案 69 之『卷次未細核』各**存其說而不升為主位卷號**'
       u'（依 D3 前裁『不欺誑宣稱精確分卷』）；《五支物主經》末句依凡例第二律**降為義撮『』**並自標『本地未收・照錄未覆核』'
       u'（量得《中阿含》確不在本地收錄之列）。今量：逐字段 152➔153（命中 116）・核卷 134➔136・未證 18 如舊・十尺全綠。'
       u'⚠自犯：錨內分隔符又誤記（該行兩處俱 U+00B7，我以 U+30FB 打字而 0 命中）——'
       u'**凡帶『・／·』之錨先印碼位，或逕以 chr(0x00B7)／chr(0x30FB) 構造**。\n')
assert sop.count(C) == 1, u'錨 C：%d' % sop.count(C)
sop = sop.replace(C, NEW + C)
io.open(S, 'wb').write(sop.encode('utf-8'))
print(u'SOP：%d 行｜CRLF %d' % (len(sop.split('\n')), sop.count('\r')))
