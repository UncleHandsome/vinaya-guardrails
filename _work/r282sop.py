# -*- coding: utf-8 -*-
"""282・帳（補四）：SOP 之『印面』條自 278 之『積輪 2』歸實為『積輪 6』，並補一行本輪之制。"""
import hashlib
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, u'列印SOP.md')
S = io.open(P, encoding=u'utf-8-sig').read()
OLD = (u'- **印面**：**積輪 2**（印面四式仍出於 276 換入之初之 8,146 行／251 頁冊形）。'
       u'奉令方重建：`python _print/build39.py full`（＋ `full screen`），'
       u'覆核 `_work/r273face.py 列印`（〇・同期之檢：冊新於印退 2，`--stale` 退 3）。')
NEW = (u'- **印面**：**積輪 6**（277・278・279・280・281・282 六輪之改俱未出冊；'
       u'印面四式仍出於 276 換入之初之 8,146 行／251 頁冊形，今冊已 8,166 行・sha256（LF 形）`9e5061bef780`）。'
       u'奉令方重建：`python _print/build39.py full`（＋ `full screen`），'
       u'覆核 `_work/r273face.py 列印`（〇・同期之檢：冊新於印退 2，`--stale` 退 3）。')
print(u'命中：%d' % S.count(OLD))
assert S.count(OLD) == 1, S.count(OLD)
S = S.replace(OLD, NEW, 1)
TAIL = (u'\n- **第 282 輪・速查表之式（本輪只動冊身與尺，印面候重建）**：第六章五張集群矩陣之廿五行改鑄'
        u'（爭點欄去『犯緣與開緣』式套語、處斷欄改 **【刑名（定位）】＋構成阻卻斷點**、所貼戒句撤出速查表——'
        u'其全文俱在附錄四該案之卡）；**此約今由 v39chk 新增之第 33 目『集群矩陣速查之式』守**'
        u'（五張表頭定管轄・行須七欄・表頭非五張該目自喊停；牙列配針 33・單軸無連帶），'
        u'不變量遂自 33 ➔ **34 目**，『目數自對合』順移為第 34。印面之影響：第六章五行表列之兩欄文字變長，'
        u'重建後須覆看該五表之字級與換行（`r273face` 丙・圍欄同頁不受影響，因表非圍欄）。\n')
assert S.count(u'第 282 輪・速查表之式') == 0, u'已記過'
S = S.rstrip(u'\n') + u'\n' + TAIL
io.open(P, 'w', encoding=u'utf-8').write(S)
back = io.open(P, encoding=u'utf-8-sig').read()
print(u'SOP 今 %d 行・sha %s・積輪 6：%s・282：%s' % (
    len(back.split(u'\n')), hashlib.sha256(back.encode(u'utf-8')).hexdigest()[:12],
    u'積輪 6' in back, u'第 282 輪' in back))
