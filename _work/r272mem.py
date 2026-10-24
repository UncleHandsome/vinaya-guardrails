# -*- coding: utf-8 -*-
"""272 輪・現況快照之改帳（五事）。含反引號之字串一律落檔，不走 shell（354／269／272 三度之誡）。"""
import io
import os

P = os.path.join(os.path.expanduser(u'~'), u'.qoder', 'projects',
                 u'C--Users-lionc-OneDrive-----------------', 'memory',
                 'project-round31-state.md')
t = io.open(P, encoding=u'utf-8').read()
EDITS = [
    (u'**今量：30/30・', u'**今量：31/31・'),
    (u'積輪 21・候令出冊', u'積輪 22・候令出冊'),
    (u'截至 2026-10-20・第 267 輪', u'截至 2026-10-20・第 272 輪'),
    (u'v39chk **29 目**', u'v39chk **31 目**'),
    (u'附錄四）。', u'附錄四／**r272teeth 牙列矩陣（尺之尺）**）。'),
    (u'、`r256bal.py`',
     u'、**`r272teeth.py`（第九尺：逐目植病，四則自約見檔首）、`r272neg.py`'
     u'（鈍針／失錨／病基三針）、`r272probe.py`（chk() 源印之量）、`r272sop2.py`'
     u'（SOP 改帳，兩面之刃見檔首）**、`r256bal.py`'),
    (u'**第 30 目『《X犍度》須見於語料（折揵→犍、剝書名前綴）』11 形 0 虛**；',
     u'**第 30 目『《X犍度》須見於語料（折揵→犍、剝書名前綴）』11 形 0 虛**、'
     u'**第 31 目『目數自對合（名常量・try/except 同名・源唯一名數＝實印目數）』源 31／印 31**；'
     u'**第九尺牙列矩陣：三十二針逐目植病・逮 32・欠 0**（基線副本先全綠，否則整盤作廢退 2；'
     u'目數自基線推得，增目無針即未植、廢目針存即殭針）；'),
]
for old, new in EDITS:
    n = t.count(old)
    assert n == 1, u'錨非一（%d）：%s' % (n, old[:28])
    t = t.replace(old, new)
io.open(P, 'w', encoding='utf-8').write(t)
print(u'改帳五事入檔｜檔長 %d 字' % len(t))
