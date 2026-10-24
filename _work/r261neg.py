# -*- coding: utf-8 -*-
"""261 輪立・核卷尺之負測（276 續再製：第六章改製後『### 〔案例 NN〕』卡與『#### 【律典原典】』欄俱廢，
旧錨不可求 ➔ 改落在原典欄『> **《四分律》卷X（…）**』之出處行；三道仍舊：基線→植錯→還原）。

驗：① 基線 rc=0；② 植一枚『可讀而錯』之卷號（五十七，落 50–60 檔，出本書此欄卷段之外）須 rc=1 且報『不合』；
    ③ 還原 rc=0。以例外退出之 rc＝假紅，不算紅燈（263 之誡）。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r261neg.py
"""
import io
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, u'_work')
for _p in (ROOT, WORK):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import _tk                                                     # noqa: E402

env = dict(os.environ, PYTHONIOENCODING=u'utf-8')
L0 = _tk.MAIN_LINES
CN = set(u'一二三四五六七八九十百')
i0 = next(k for k, l in enumerate(L0) if l.startswith(u'> **《四分律》卷'))
CITE = L0[i0]
assert u'卷' in CITE, u'落點非卷引行'
NUM57 = u'五十七'
WRONG = re.sub(u'卷[%s]{1,4}' % u''.join(sorted(CN)),
               lambda m: u'卷' + NUM57, CITE)                   # 可讀而錯之卷號（非『不可解』故不落未證）
assert WRONG != CITE and NUM57 in WRONG
print(u'落點｜%s' % CITE[:60])
print(u'錯引｜%s' % WRONG[:60])

TMPD = tempfile.mkdtemp(prefix=u'r261neg_')
TMP = os.path.join(TMPD, u'book.md')


def run(text):
    io.open(TMP, u'w', encoding=u'utf-8', newline=u'\n').write(text)
    q = subprocess.run([sys.executable, u'-X', u'utf8', os.path.join(WORK, u'v39volchk.py'), TMP],
                       capture_output=True, text=True, encoding=u'utf-8', env=env)
    tail = [ln for ln in (q.stdout or u'').split(u'\n') if u'————' in ln or u'✗' in ln]
    if (q.stderr or u'').strip():                               # 以例外退出之 rc＝假紅，非判決
        tail.append(u'stderr:' + q.stderr.strip().split(u'\n')[-1][:90])
    return q.returncode, tail


base = u'\n'.join(L0)
rc0, out0 = run(base)
rc1, out1 = run(base.replace(CITE, WRONG, 1))
rc2, out2 = run(base)
try:
    os.remove(TMP)
    os.rmdir(TMPD)
except OSError:
    pass
print(u'基線：rc=%d・%s' % (rc0, u' | '.join(out0)[:120]))
print(u'植錯：rc=%d・%s' % (rc1, u' | '.join(out1)[:150]))
print(u'還原：rc=%d・%s' % (rc2, u' | '.join(out2)[:120]))
ok = rc0 == 0 and rc1 == 1 and rc2 == 0 and u'不合 1' in u''.join(out1)
print(u'———— 核卷負測：%s' % (u'三道如所期' if ok else u'✗ 不如所期'))
sys.exit(0 if ok else 1)
