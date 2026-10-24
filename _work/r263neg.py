# -*- coding: utf-8 -*-
"""263 輪・卡外逐字尺之負測：三道（植一掛出處之假逐字 → 亡其一界 → 還原）。

戒（承 261 輪之教）：以例外退出之 rc 乃假紅，非判決——故 stderr 必取空方算逮得。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r263neg.py
"""
import io
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
SRC = os.path.join(ROOT, NAME)
TMP = os.path.join(ROOT, u'_work', u'_negq2.md')
TOOL = os.path.join(ROOT, u'_work', u'v39quote2.py')

base = io.open(SRC, encoding=u'utf-8').read()
lines = base.split(u'\n')
i1 = next(k for k, l in enumerate(lines) if l.startswith(u'# 第一章'))
PLANT = u'　《四分律》卷三云：「此句必不見於原典，負測之植。」'          # 植：掛出處之非逐字
BOUND = u'故俱屬**照錄未覆核**——'                                  # 界：附錄一之自標（凡例亦有此語，故取較長之錨）
assert base.count(BOUND) >= 1, u'界錨不在（不得空跑負測）'


def run():
    env = dict(os.environ, PYTHONIOENCODING=u'utf-8', TKSRC=TMP)
    p = subprocess.run([sys.executable, u'-X', u'utf8', TOOL],
                       capture_output=True, text=True, encoding=u'utf-8', env=env)
    say = [ln for ln in (p.stdout or u'').split(u'\n')
           if u'————' in ln or ln.strip().startswith(u'✗') or u'亡！' in ln]
    err = (p.stderr or u'').strip()
    return p.returncode, say, err


shutil.copyfile(SRC, TMP)
res = {}
# 一・植假逐字（附於第一章之一行敘事行尾，同線先有《四分律》之出處標記）
l1 = list(lines)
l1[i1 + 4] = l1[i1 + 4].rstrip() + PLANT
io.open(TMP, 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(l1))
res[u'植假逐字'] = run()
# 二・亡其界（於副本）
t = io.open(SRC, encoding=u'utf-8').read().replace(BOUND, u'照錄', 1)
assert t != io.open(SRC, encoding=u'utf-8').read(), u'亡界無效（錨未中）'
io.open(TMP, 'w', encoding=u'utf-8', newline=u'\n').write(t)
res[u'亡界'] = run()
# 三・還原
io.open(TMP, 'w', encoding=u'utf-8', newline=u'\n').write(base)
res[u'還原'] = run()
os.remove(TMP)

ok = True
for k, (rc, say, err) in res.items():
    print(u'%-8s rc=%d%s｜%s' % (k, rc, u'　⚠有 stderr（假紅）' if err else u'',
                                 u' | '.join(s.strip()[:78] for s in say[-2:])))
    if err:
        ok = False
want = (res[u'植假逐字'][0] == 1 and res[u'亡界'][0] == 1 and res[u'還原'][0] == 0)
print(u'———— 判定：%s（須 植→1・亡界→1・還原→0，且俱不因崩而紅）' % (u'中' if (want and ok) else u'不中'))
sys.exit(0 if (want and ok) else 1)
