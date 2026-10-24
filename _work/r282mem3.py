# -*- coding: utf-8 -*-
"""282・帳（補二）：正 project 記憶之末數（33/35 ➔ 34/34・36 針），並記新立之第 33 目。"""
import hashlib
import io
import os

P = os.path.join(u'C:', u'\\', u'Users', u'lionc', u'.qoder', u'projects',
                 u'C--Users-lionc-OneDrive-----------------', u'memory',
                 u'project-round31-state.md')
S = io.open(P, encoding=u'utf-8').read()
OLD = u'不變量 33/33・牙列 35/35'
NEW = u'不變量 34/34・牙列 34 目 36 針 逮 36'
print(u'命中：%d' % S.count(OLD))
assert S.count(OLD) == 2, S.count(OLD)
S = S.replace(OLD, NEW)
TAIL = u'器之綠與器之啞先分清。'
ADD = (TAIL + u'**又：數不可自證即不報**（附錄六導言一度自報『其七則』，以卷段正则點之只逮五則，遂去其數而只列實名之卷段）。'
       u'**末立 v39chk 第 33 目『集群矩陣速查之式』**：五張表頭定管轄・行須七欄・爭點欄禁『犯緣與開緣』套語・'
       u'處斷欄須以 **【 起手・表頭非五張該目即自喊停（殭尺之綠之治）；牙列配針 33（單軸・連帶紅 0），'
       u'自對合目順移為 34。此目專護本輪新口徑『矩陣只作速查，逐字之責全在附錄四』——'
       u'後人若再把戒句貼回速查表，其文不著「」而歷尺皆不識，唯此目能紅。')
assert S.count(TAIL) == 1, S.count(TAIL)
S = S.replace(TAIL, ADD, 1)
io.open(P, 'w', encoding=u'utf-8').write(S)
back = io.open(P, encoding=u'utf-8-sig').read()
print(u'今 %d 行・sha %s・34/34：%d・新目：%s' % (
    len(back.split(u'\n')), hashlib.sha256(back.encode(u'utf-8')).hexdigest()[:12],
    back.count(u'34/34'), u'第 33 目『集群矩陣速查之式』' in back))
