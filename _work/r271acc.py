# -*- coding: utf-8 -*-
"""271 輪・帳二：SOP 今制＋本輪案內、記憶兩檔（現況快照與索引）。一錨一斷言，附加式之期望＝new.count(old)。"""
import hashlib
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
raw = open(os.path.join(ROOT, NAME), 'rb').read()
SHA = hashlib.sha256(raw).hexdigest()[:12]
NL = raw.decode(u'utf-8-sig').count(u'\n') + 1
NLS, NBS = format(NL, u',d'), format(len(raw), u',d')
MEM = os.path.join(os.path.expanduser(u'~'), u'.qoder', u'projects',
                   u'C--Users-lionc-OneDrive-----------------', u'memory')
SOP, ST, IX = (os.path.join(ROOT, u'列印SOP.md'),
               os.path.join(MEM, u'project-round31-state.md'),
               os.path.join(MEM, u'MEMORY.md'))

ENTRY = (u'\n  **第 271 輪・附錄子靶以量結案，本律篇名以尺補闕**——承 268 債⑥。'
         u'① **附錄級子靶今冊不作此宣稱**（`_work/r271ctx.py`：『附錄N・X』0・『附錄N（X）』0・『附錄N之X』2 見俱經文），'
         u'故**以量結案而非以尺結案**——強立一尺則名單為空（空名單即無尺）。'
         u'② **本律篇名有尺**（`_work/r271probe2.py`・`_work/r271titles.py`）：全書《X》35 形 229 見，含『犍度』者 11 形，'
         u'對本地六十卷須**折異體**（冊作『犍度』、語料作『揵度』，不折則全成偽缺）——得《僧殘犍度》（L3121）**語料 0 見**，'
         u'而《覆藏犍度》2 見且『竟覆藏犍度…知我行摩那埵覆藏犍度』正證四種治法之摩那埵屬焉（語料『若弟子犯僧殘…應與波利婆沙…'
         u'應與本日治…應與摩那埵…應與出罪』具在）；僧殘乃『分』攝，非犍度。'
         u'**刀**（`_work/r271fix.py` 1 項）：刪『《僧殘犍度》與』四字，四法之義俱存。'
         u'**器・不變量第 30 目『書名號內之本律篇名須見於語料』**：只認含『犍度』之《X》，先剝『書名・』前綴'
         u'（中點兼收 U+00B7 與『・』——初版只認其一，遂把《四分律·呵責犍度》誤判為虛，'
         u'**此乃『以錯字為紅』之假紅**）、折異體、擲『二十犍度』之總數稱；他典品名不在此軸（本地不儲其檔，'
         u'強校即偽缺，其界由凡例『未收之典須自標其界』守）；語料必經 `_tk.VINAYA`。今 11 形・0 虛。'
         u'**負測 `_work/r271neg.py` 兩道各證一枝**：原樣植回所刪之虛篇名→點名『《僧殘犍度》語料無此連綴』退 1；'
         u'植帶前綴之《四分律·偽說犍度》→點名『《偽說犍度》』退 1（**第二道專證『剝前綴』一支會響**，否則此枝永遠無聲）。'
         u'自犯三則：① **舊負測之對照道寫死『29/29』**，本輪增一目遂兩支同時假紅——正合『驗收器硬編今制＝手工帳必腐』之誡，'
         u'今改**自比 N/N**（r269／r270／r271 三支同制），**自此新增一目不必追改負測**；② 逃字逐層降級（heredoc→檔內字串→常數）'
         u'生 SyntaxWarning，**改畢以『stderr 空』為準驗，不可只看 rc=0**；③ 附錄級一軸量後知其名單為空，'
         u'幸依『名單須斷非空』作罷——**貿然立之即得一枝永遠綠的尺**。'
         u'**今量：%s 行・%s B・SHA `%s`｜八尺全綠・不變量 30/30**（…同 270 諸數…・**篇名 11 形 0 虛**）｜負測十二支俱中且 stderr 俱空。'
         u'⚠ 本輪動印面（一字之刪），**積輪 21**。' % (NLS, NBS, SHA))

PAIRS = [
    (SOP, u'270 之自查自除（269 新立『凡用之處須自註分界』乃不可驗之約➔改約以從實）與第 10 目加『蒙上省寫』之網）'
          u'）**而 PDF 未重建**——奉令『修正不即出冊』，**積輪 20** 待令。',
     u'270 之自查自除（269 新立『凡用之處須自註分界』乃不可驗之約➔改約以從實）與第 10 目加『蒙上省寫』之網、'
     u'271 之附錄子靶以量結案並立第 30 目『本律篇名須見於語料』（刪《僧殘犍度》之虛篇名））'
     u'）**而 PDF 未重建**——奉令『修正不即出冊』，**積輪 21** 待令。'),
    (SOP, u'今已自立（第 255～270 輪）', u'今已自立（第 255～271 輪）'),
    (SOP, u'⚠ 本輪動印面（凡例一句重寫），**積輪 20**。呈裁三項如 269，未動。',
     u'⚠ 本輪動印面（凡例一句重寫），**積輪 20**。呈裁三項如 269，未動。' + ENTRY),
    (ST, u'description: 戒律分析專案現況（第 270 輪）', u'description: 戒律分析專案現況（第 271 輪）'),
    (ST, u'**9,340 行・968,586 B・SHA `14802d4a6cdb`**・案例卡 102',
     u'**%s 行・%s B・SHA `%s`**・案例卡 102' % (NLS, NBS, SHA)),
    (ST, u'**積輪 20・候令出冊**', u'**積輪 21・候令出冊**'),
    (ST, u'**今量：29/29・卡身 116/116', u'**今量：30/30・卡身 116/116'),
    (ST, u'（本帳之簡形淨）」、',
     u'（本帳之簡形淨）**、**`r271ctx.py`／`r271probe2.py`／`r271titles.py`（附錄子靶以量結案・本律篇名之量）、'
     u'`r271fix.py`（刪虛篇名）、`r271neg.py`（兩枝負測）**、'),
    (ST, u'第 10 目今兼護『蒙上省寫』5 處 0 落空**；',
     u'**第 10 目今兼護『蒙上省寫』5 處 0 落空**・**第 30 目『《X犍度》須見於語料（折揵→犍、剝書名前綴）』11 形 0 虛**；'),
    (IX, u'**第 270 輪止（2026-10-20）**', u'**第 271 輪止（2026-10-20）**'),
    (IX, u'：ver39 正本 9,340 行・968,586 B・SHA `14802d4a6cdb`',
     u'：ver39 正本 %s 行・%s B・SHA `%s`' % (NLS, NBS, SHA)),
    (IX, u'不變量 29/29・卡身逐字 116/116', u'不變量 30/30・卡身逐字 116/116'),
    (IX, u'・積輪 20 候令重建',
     u'・**271 附錄子靶以量結案（名單為空即不立尺）＋立第 30 目『本律篇名須見於語料』（折揵→犍・剝書名前綴），'
     u'刪《僧殘犍度》之虛篇名；負測對照道改自比 N/N（增目不須追改）**・積輪 21 候令重建'),
]
FILES = {}
for p, _o, _n in PAIRS:
    if p not in FILES:
        FILES[p] = io.open(p, encoding=u'utf-8-sig').read()
bad = [(os.path.basename(p), old[:34], FILES[p].count(old)) for p, old, _n in PAIRS
       if FILES[p].count(old) != 1]
print(u'合 %d 項・錨不合 %d' % (len(PAIRS), len(bad)))
for x in bad:
    print(u'   命中 %d｜%s｜%s' % (x[2], x[0], x[1]))
if bad:
    sys.exit(2)
if u'apply' not in sys.argv:
    print(u'乾跑（冊 %s 行・%s B・%s）。' % (NLS, NBS, SHA))
    sys.exit(0)
for p, old, new in PAIRS:
    FILES[p] = FILES[p].replace(old, new, 1)
for p, txt in FILES.items():
    io.open(p, 'w', encoding=u'utf-8', newline=u'').write(txt)
back = {p: io.open(p, encoding=u'utf-8-sig').read() for p in FILES}
nok = [(os.path.basename(p), old[:24], back[p].count(old), new.count(old))
       for p, old, new in PAIRS
       if not (back[p].count(new) == 1 and back[p].count(old) == new.count(old))]
print(u'已寫入 %d 項・回讀不符 %d' % (len(PAIRS), len(nok)))
for x in nok:
    print(u'   %s｜舊實 %d／期望 %d｜%s' % x)
