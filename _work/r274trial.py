# -*- coding: utf-8 -*-
"""274 輪・試跑：以「卷首＋新稿 ch1–3＋第四章以後」組成**假冊**，未動正本而先讓九尺量之。

用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r274trial.py [--swap]
不帶 --swap＝只產 `_work/r274trial.md` 並逐尺試跑；帶 --swap＝先备份正本（含 SHA 一步回退）再入冊。
"""
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_work')
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
SRC = os.path.join(ROOT, NAME)
BL = io.open(SRC, encoding=u'utf-8').read().split(u'\n')
NEW = io.open(os.path.join(WORK, u'r274new3.md'), encoding=u'utf-8-sig').read().rstrip(u'\n').split(u'\n')
L = BL
A = next(i for i, l in enumerate(L, 1) if l.startswith(u'# \u7b2c\u4e00\u7ae0'))
Z = next(i for i, l in enumerate(L, 1) if l.startswith(u'# \u7b2c\u56db\u7ae0')) - 1
print(u'\u4eca\u518a ch1-3 \u754c\uff1aL%d\uff5eL%d' % (A, Z))
assert BL[A - 1].startswith(u'# \u7b2c\u4e00\u7ae0') and BL[Z].startswith(u'# \u7b2c\u56db\u7ae0'), u'界不合'
assert NEW[0].startswith(u'# ') and NEW[-1].strip() != u'', u'新稿首尾不合\uff08首 %r 尾 %r\uff09' % (
    NEW[0][:12], NEW[-1][:12])
assert NEW[-1].startswith(u'|') or NEW[-1].startswith(u'##') or NEW[-1].strip(u'#')
TRIAL = BL[:A - 1] + NEW + BL[Z:]
TP = os.path.join(WORK, u'r274trial.md')
io.open(TP, 'w', encoding=u'utf-8').write(u'\n'.join(TRIAL))
print(u'假冊 %d 行（正本 %d・新稿 %d・舊 ch1-3 %d）' % (len(TRIAL), len(BL), len(NEW), Z - A + 1))
env = dict(os.environ, PYTHONIOENCODING=u'utf-8')
for tool, needs_path in [(u'v39chk.py', True), (u'v39quote2.py', True), (u'v39volchk.py', True),
                         (u'v39volrange.py', True), (u'v39secref.py', True)]:
    args = [sys.executable, u'-X', u'utf8', os.path.join(WORK, tool)] + ([TP] if needs_path else [])
    q = subprocess.run(args, capture_output=True, text=True, encoding=u'utf-8', env=env, cwd=ROOT)
    out = (q.stdout or u'').rstrip().split(u'\n')
    print(u'\n【%s】rc=%d' % (tool, q.returncode))
    if q.returncode:
        for l in out:
            if u'\u2717' in l or u'FAIL' in l or u'\u932f' in l or u'\u672a\u4e2d' in l:
                print(u'   ' + l[:132])
        print(u'   末行｜%s' % out[-1][:130])
    else:
        print(u'   ' + out[-1][:130])
    if (q.stderr or u'').strip():
        print(u'   stderr｜%s' % q.stderr.strip()[:200])
if u'--swap' in sys.argv:
    import hashlib
    bak = os.path.join(WORK, u'r274swap.bak')
    raw = io.open(SRC, 'rb').read()
    io.open(bak, 'wb').write(raw)
    print(u'\u5907\u6848 %s\uff5c\u6b63\u672c SHA %s' % (os.path.basename(bak),
                                                      hashlib.sha256(raw).hexdigest()[:12]))
    io.open(SRC, 'w', encoding=u'utf-8').write(u'\n'.join(TRIAL))
    h2 = hashlib.sha256(io.open(SRC, 'rb').read()).hexdigest()[:12]
    print(u'\u5165\u518a\u5b8c\u6210\uff5c\u65b0 SHA %s\uff5c%d \u884c' % (h2, len(TRIAL)))
