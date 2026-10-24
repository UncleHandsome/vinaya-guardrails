# -*- coding: utf-8 -*-
"""265 輪・行號尺之負測：三道（植错位→報不合退 1・植越界→報未證而不挡・還原→退 0）。

戒：凡 rc 為閘，須把『當掉』列為一種必被排除的紅（261 輪之教）——故三道俱核 stderr。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r265neg.py
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
TMP = os.path.join(ROOT, u'_work', u'_neglin.md')
TOOL = os.path.join(ROOT, u'_work', u'v39linchk.py')

base = io.open(SRC, encoding=u'utf-8').read()
OLD = u'卷三十八（大正藏卷段 38-49，L137、L423、L427）'
WRONG = u'卷三十八（大正藏卷段 38-49，L137、L900、L427）'      # 900 行不hosting 本卡片段
OOB = u'卷三十八（大正藏卷段 38-49，L137、L99999、L427）'      # 越界，須判未證而不崩
assert base.count(OLD) == 1, u'錨命中 %d（須恰 1）' % base.count(OLD)


def run(tag):
    env = dict(os.environ, PYTHONIOENCODING=u'utf-8', TKSRC=TMP)
    p = subprocess.run([sys.executable, u'-X', u'utf8', TOOL],
                       capture_output=True, text=True, encoding=u'utf-8', env=env)
    say = [ln for ln in (p.stdout or u'').split(u'\n') if u'————' in ln or u'✗' in ln or u'△' in ln]
    print(u'%-10s rc=%d｜%s' % (tag, p.returncode, u' | '.join(s.strip()[:76] for s in say[:2])))
    err = (p.stderr or u'').strip()
    if err:
        print(u'   ⚠ stderr（假紅之形）：%s' % err.split(u'\n')[-1][:100])
    return p.returncode, say, err


shutil.copyfile(SRC, TMP)
io.open(TMP, 'w', encoding=u'utf-8', newline=u'\n').write(base.replace(OLD, WRONG, 1))
rc1, s1, e1 = run(u'植錯位')
bite1 = any(u'✗' in x for x in s1) and any(u'不合' in x for x in s1)
io.open(TMP, 'w', encoding=u'utf-8', newline=u'\n').write(base.replace(OLD, OOB, 1))
rc2, s2, e2 = run(u'植越界')
bite2 = any(u'未證' in x for x in s2)
io.open(TMP, 'w', encoding=u'utf-8', newline=u'\n').write(base)
rc0, s0, e0 = run(u'還原')
os.remove(TMP)
ok = (rc1 == 1 and bite1 and rc2 == 0 and not e2 and rc0 == 0 and not e1 and not e0)
print(u'———— 判定：%s（須 植位→1 報不合・越界→0 報未證不挡・還原→0，三道俱不因崩而紅）'
      % (u'中' if ok else u'不中'))
sys.exit(0 if ok else 1)
