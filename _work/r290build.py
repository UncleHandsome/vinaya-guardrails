# -*- coding: utf-8 -*-
r"""290 補・重建入帳：SOP 印面行、記憶兩檔、日誌補一行。"""
import hashlib
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKP = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
B = io.open(BOOKP, 'rb').read()
T = B.decode('utf-8').replace('\r\n', '\n')
SHA = hashlib.sha256(T.encode('utf-8')).hexdigest()[:12]
N = len(T.split('\n'))
print(u'冊：%d 行・sha %s' % (N, SHA))

S = os.path.join(ROOT, u'列印SOP.md')
sop = io.open(S, encoding='utf-8').read()
A = (u'- **印面**：**積輪 2**（289・290 兩輪之刀俱未出冊，奉令方建；上一次重建為 288：'
     u'完整版影印與螢幕**各 261 頁**・大綱 146＝目錄印出 146・定位失敗 0；'
     u'今冊 %d 行・sha256（LF 形）`%s`；' % (N, SHA))
assert sop.count(A) == 1, u'錨 A：%d' % sop.count(A)
sop = sop.replace(A, u'- **印面**：**積輪 0**（290 奉令重建：完整版影印與螢幕**各 262 頁**（原 261，'
                     u'+1 頁來自本輪地標拆段與附錄六立界之兩行）・大綱 146＝目錄印出 146・定位失敗 0；'
                     u'今冊 %d 行・sha256（LF 形）`%s`；' % (N, SHA))
io.open(S, 'wb').write(sop.encode('utf-8'))
print(u'SOP 印面行已改')

D = os.path.join(ROOT, u'_archive', u'編年工程日誌.md')
raw = io.open(D, 'rb').read().decode('utf-8').replace('\r\n', '\n')
END = u'備份 `_archive/備份/ver39.pre291.md`。'
assert raw.count(END) == 1
raw = raw.rstrip('\n') + '\n' + (
    u'**290 補・奉令重建**：影印・螢幕**各 262 頁**（原 261，+1 頁正應本輪新增之兩行）'
    u'・目錄印出 146＝大綱入 146・定位失敗 0・頁腳相符 261／不合 0・圍欄 75 段俱同頁・超閾 0、'
    u'最細 9.33pt、9pt 以下 0 段・`verify39` 兩軌『不合格 0 處』➔**印面五量全中・積輪 0**'
    u'（冊 %d 行・`%s`，印晚於冊 85 分鐘，同期可鑑）。' % (N, SHA)).replace('\n', '\r\n')
io.open(D, 'wb').write(('\r\n'.join(raw.split('\r\n')) if False else raw).encode('utf-8'))
print(u'日誌補一行：%d 行' % len(raw.split('\r\n')))

MEM = u'C:/Users/lionc/.qoder/projects/C--Users-lionc-OneDrive-----------------/memory'
P = os.path.join(MEM, u'project-round31-state.md')
raw = io.open(P, encoding='utf-8').read()
X = u'**積輪 2（289・290 兩輪俱未出冊，奉令方建；288 重建'
assert raw.count(X) == 1, u'X：%d' % raw.count(X)
raw = raw.replace(X, u'**積輪 0（290 奉令重建：影印・螢幕各 262 頁（原 261）・大綱 146＝目錄 146・印面五量全中・9pt 以下 0 段；288 重建')
Y = u'**印面今制（276 建・284〜288 五度重建・今積輪 2＝289・290 兩輪未出冊）**'
assert raw.count(Y) == 1, u'Y：%d' % raw.count(Y)
raw = raw.replace(Y, u'**印面今制（276 建・284〜290 六度重建・積輪 0）**')
Z = u'288＝261（146）、289 未建。'
if raw.count(Z) == 1:
    raw = raw.replace(Z, u'288＝261（146）、290＝262（146）。')
else:
    W = u'287＝261（146）、288＝261（146）。'
    assert raw.count(W) == 1, u'W：%d' % raw.count(W)
    raw = raw.replace(W, u'287＝261（146）、288＝261（146）、290＝262（146）。')
io.open(P, 'wb').write(raw.encode('utf-8'))
print(u'狀態檔：印面之帳已改')

Q = os.path.join(MEM, u'MEMORY.md')
s = io.open(Q, encoding='utf-8').read()
U1 = u'・**積輪 2**（289・290 兩輪未出冊；上一次 288 重建：影印・螢幕各 **261 頁**'
assert s.count(U1) == 1, u'U1：%d' % s.count(U1)
s = s.replace(U1, u'・**積輪 0**（290 奉令重建：影印・螢幕各 **262 頁**（原 261）・大綱 146＝目錄 146')
U2 = u'。290 收外路第十七報告'
assert s.count(U2) == 1
s = s.replace(U2, u'。印面：262 頁・五量全中。290 收外路第十七報告')
io.open(Q, 'wb').write(s.encode('utf-8'))
print(u'索引：印面之帳已改')
