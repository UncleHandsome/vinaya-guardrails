# -*- coding: utf-8 -*-
"""精簡本減重之獨立覆核（第 112 輪立）：讀成品 PDF 文字層，查削塊是否真削、隨改是否真隨。

口徑刻意與 build38 之清單**各自獨立書寫**（不共用常數），使本軸能反駁生成器：
  甲、已削之三款標題（及其專屬語）不得再見於印面；
  乙、隨改之新語須恰見於印面（否則改而未動）；
  丙、舊語（死指之源）不得殘留；
  丁、頁數不寫死常數（手填之數每削一塊即須追改，是債不是檢）——改與完整冊同測，
      只斷「精簡必少於完整」，實數一率印出，今制作廢另見 列印SOP.md。
用法：python _work/slimchk.py
"""
import io, os, re, sys
import pymupdf as fitz

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P = os.path.join(ROOT, '_print')
PDF = os.path.join(P, 'ver38四分律_起心動念心智分析框架_第三十八版_列印版_精簡本.pdf')
HTML = os.path.join(P, 'final38_精簡本.html')

GONE = [u'五維立體檢索樞紐', u'全書百則基準檢索總表', u'司法天平稱重法式',
        u'心所病相軸檢索指南', u'生活領域軸檢索指南', u'四諍衝突學軸檢索指南',
        u'可懺處分軸檢索指南', u'八大正理速查軸', u'次握', u'五維速查',
        u'第七章總表是', u'天平稱重之法（第三節）', u'百則基準台帳（第五節）',
        u'深水稱重法式', u'法益重力標記說明', u'矩陣歸格與法益附註',
        u'三十格檢索總表（並附各格法益輕重']
HERE_ = [u'生命之樹生態全景與實體收束閉環', u'八大正理統攝矩陣與 29 則複統攝',
         u'第七章綁定台帳是', u'第七章的『正理對位台帳』',   # 第 200 輪換裝歸『』，錨隨之（至第 208 輪重建之新冊方現形）
         u'八大正理統攝之矩陣（第三節）', u'消融於三十二字略戒。',
         u'壹·照破執念', u'八大正理功能、十句義原生母源與三環咬合總表',
         u'精簡本唯留座標與空格', u'六領域之空格（凡六處）']
PDF_FULL = os.path.join(P, 'ver38四分律_起心動念心智分析框架_第三十八版_列印版.pdf')
BODY = u'<!--BODY-ANCHOR-->'

doc = fitz.open(PDF)
txt = re.sub(u'\\s+', u'', u''.join(doc[i].get_text() for i in range(len(doc))))
bad = []
for k in GONE:
    n = txt.count(re.sub(u'\\s+', u'', k))
    if n:
        bad.append(u'甲 殘留：%s（%d 見）' % (k, n))
for k in HERE_:
    n = txt.count(re.sub(u'\\s+', u'', k))
    if n == 0:
        probe = re.sub(u'\\s+', u'', k)[-6:]
        j = txt.find(probe)
        bad.append(u'乙 不見：%s（末六字「%s」%s）' % (
            k, probe, u'印面實作「%s」' % txt[max(0, j - 12):j + 18] if j >= 0 else u'亦無蹤'))
n_slim = len(doc)
doc.close()
if os.path.exists(PDF_FULL):
    n_full = len(fitz.open(PDF_FULL))
    if n_slim >= n_full:
        bad.append(u'丁 精簡 %d 頁未少於完整 %d 頁' % (n_slim, n_full))
    pages = u'%d（完整 %d，少 %d）' % (n_slim, n_full, n_full - n_slim)
else:
    pages = u'%d（缺完整冊，丁軸未行）' % n_slim
print(u'精簡本減重覆核：頁 %s｜甲 查死指 %d 項｜乙 查隨改 %d 項 → %s' % (
    pages, len(GONE), len(HERE_), u'全合' if not bad else u'有恙'))
for b in bad:
    print(u'   %s' % b)
sys.exit(1 if bad else 0)
