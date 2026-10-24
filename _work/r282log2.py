# -*- coding: utf-8 -*-
"""282・帳（補）：把本輪末所立之第 33 目（護『矩陣只作速查』之新口徑）補入日誌，並正末段之數。"""
import hashlib
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, u'_archive', u'編年工程日誌.md')
TXT = io.open(LOG, encoding=u'utf-8-sig').read()
ADD = u'''
**282 補・立新目護本輪之口徑（同輪）**：本輪把廿五行之戒句自矩陣撤出，定下『**集群矩陣只作速查，逐字之責全在附錄四**』——此約若無尺，後人（含我）必再把戒句貼回，而貼回之文不著「」，歷尺皆不識（同 281『生肉文字』之病族：宣稱在，量它的尺不在）。故立 **v39chk 第 33 目『集群矩陣速查之式』**：以五張表頭（案號與事相綱要・起心動念・核心爭點與邊界標尺・佛陀處斷與法效・律典原典出處）定其管轄，管內每行須①七欄②爭點欄不含『犯緣與開緣』式套語③處斷欄以 **【 起手；**且表頭張數須為五，管轄歸零即該目自己喊停**（五十二度・殭尺之綠之治）**。牙列配針 33（只把一枚行爭點欄植回套語，處斷欄不動➔針尖單軸・連帶紅 0），原『目數自對合』順移為第 34 目。**終檢今量：不變量 34/34・牙列 34 目・針 36・逮 36・欠 0；十尺齊跑全綠；冊仍 8,166 行・sha `9e5061bef780`（本補只動尺不動冊）。積輪 6 如故。**
'''
assert u'282 補・' not in TXT, u'已記過'
io.open(LOG, 'a', encoding=u'utf-8').write(ADD)
back = io.open(LOG, encoding=u'utf-8-sig').read()
print(u'日誌今 %d 行・sha %s・含 282 補：%s' % (
    len(back.split(u'\n')), hashlib.sha256(back.encode(u'utf-8')).hexdigest()[:12], u'282 補・' in back))
