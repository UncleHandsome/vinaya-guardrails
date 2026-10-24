# -*- coding: utf-8 -*-
"""259 輪立・263／268／272 輪擴：三十九版查核之跑批，一行跑盡 ver39 之十支尺（形制・卡身逐字・卡外逐字・核卷・範圍引卷・行號對引文・節級指針對合・附錄四・階梯四諍名單・牙列矩陣），報退碼。

用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/v39battery.py
退碼：十尺俱 0 方為 0；任一非 0 即非 0（凡以 rc 為閘者須先負測——負測器 `_work/r255neg.py`・`_work/r263neg.py`・`_work/r268neg.py`；
      第九尺『牙列矩陣』即諸尺之負測本身，故其退碼非 0 時須補針而非刪目）。
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = (u'v39chk.py', u'v39quote.py', u'v39quote2.py', u'v39volchk.py', u'v39volrange.py',
         u'v39linchk.py', u'v39secref.py', u'v39apx4chk.py', u'v39ladder.py', u'r272teeth.py')
env = dict(os.environ, PYTHONIOENCODING=u'utf-8')
rc_all = 0
for t in TOOLS:
    p = subprocess.run([sys.executable, u'-X', u'utf8', os.path.join(ROOT, u'_work', t)],
                       capture_output=True, text=True, encoding=u'utf-8', env=env)
    out = (p.stdout or u'').rstrip().split(u'\n')
    key = [l for l in out if re.search(u'不變量|非逐字|核合|指針|宣稱|名單|名冊|牙列', l)]
    print(u'%-13s %s｜%s' % (t, u'rc=%d' % p.returncode, (key[-1] if key else
                                                          (out[-1] if out else u'（無出）'))))
    if p.returncode:
        rc_all = 1
        print(u'    ' + u'\n    '.join(
            l for l in out if u'✗' in l or u'FAIL' in l or re.search(u'逮|植|針|崩', l))[:1600])
    if (p.stderr or u'').strip():
        print(u'    stderr｜%s' % p.stderr.strip()[:200])
print(u'———— ver39 十尺齊跑：%s' % (u'全綠' if not rc_all else u'有紅'))
sys.exit(rc_all)
