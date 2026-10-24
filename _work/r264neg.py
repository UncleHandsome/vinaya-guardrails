# -*- coding: utf-8 -*-
"""264 輪・範圍引卷尺之負測：把一枚『卷一至十』改成他卷段，驗尺報『不合』而退 1（三道）。

戒（承 261／263 輪）：以例外退出之 rc 乃假紅，非判決——stderr 必取空方算逮得；
  錨須先斷言恰中一次，否則『未報』可能只是『未植』。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r264neg.py
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
TMP = os.path.join(ROOT, u'_work', u'_negrng.md')
TOOL = os.path.join(ROOT, u'_work', u'v39volrange.py')

base = io.open(SRC, encoding=u'utf-8').read()
OLD = u'初離處波羅夷」（卷一至十）'
NEW = u'初離處波羅夷」（卷三十一至三十七）'
assert base.count(OLD) == 1, u'錨命中 %d（須恰 1，不得空跑負測）' % base.count(OLD)


def run():
    env = dict(os.environ, PYTHONIOENCODING=u'utf-8', TKSRC=TMP)
    p = subprocess.run([sys.executable, u'-X', u'utf8', TOOL],
                       capture_output=True, text=True, encoding=u'utf-8', env=env)
    say = [ln for ln in (p.stdout or u'').split(u'\n') if u'————' in ln or u'✗' in ln]
    return p.returncode, say, (p.stderr or u'').strip()


shutil.copyfile(SRC, TMP)
io.open(TMP, 'w', encoding=u'utf-8', newline=u'\n').write(base.replace(OLD, NEW, 1))
rc1, say1, err1 = run()
io.open(TMP, 'w', encoding=u'utf-8', newline=u'\n').write(base)
rc0, say0, err0 = run()
os.remove(TMP)

bite = any(u'不合' in s for s in say1) and any(u'✗' in s for s in say1)
print(u'植錯（卷一至十 ➔ 卷三十一至三十七）：rc=%d・報不合=%s・stderr=%r' % (rc1, bite, err1[:80]))
for s in say1[:3]:
    print(u'   ', s.strip()[:108])
print(u'還原：rc=%d・stderr=%r｜%s' % (rc0, err0[:80], (say0[0].strip()[:80] if say0 else u'')))
ok = (rc1 == 1 and rc0 == 0 and bite and not err1 and not err0)
print(u'———— 判定：%s（須 植→報不合而 rc=1・還原→rc=0・兩道俱不因崩而紅）' % (u'中' if ok else u'不中'))
sys.exit(0 if ok else 1)
