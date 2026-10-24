# -*- coding: utf-8 -*-
"""277 輪・尺十（v39ladder）之負測：三針須『因判決而紅』並『點名真答案』。

甲・移一无犯之案入極刑階 ➔ 須點名该案並退 1（此即外路報告所逮之荒謬錯配）。
乙・改一階之自報數（唯一案號不变）➔ 須報『宣稱≠唯一』並退 1。
丙・把已入 EXEMPT 之案移入不相刑之階 ➔ 亦須紅（證 EXEMPT 只免『同一案之他支』之證，開一處新錯仍擋）。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r277laneg.py
退碼：三針俱中即 0。
"""
import io
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, u'_work')
sys.path.insert(0, ROOT)
sys.path.insert(0, WORK)
import _tk                                                     # noqa: E402

env = dict(os.environ, PYTHONIOENCODING=u'utf-8')
TMPD = tempfile.mkdtemp(prefix=u'r277laneg_')
BASE = _tk.MAIN_LINES
TOOL = os.path.join(WORK, u'v39ladder.py')


def run(lines, tag):
    p = os.path.join(TMPD, tag + u'.md')
    io.open(p, u'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(lines))
    q = subprocess.run([sys.executable, u'-X', u'utf8', TOOL, p],
                       capture_output=True, text=True, encoding=u'utf-8', env=env)
    return q.returncode, (q.stdout or u'') + (q.stderr or u'')


def head_of(lines, key):
    rx = re.compile(u'共 \d+ 案')
    return next(i for i, l in enumerate(lines)
                if l.startswith(u'* **第') and key in l and rx.search(l))


def body_of(lines, key):
    return head_of(lines, key) + 1


# 甲・無犯之案入極刑階
A = list(BASE)
h = head_of(A, u'第一階')
A[body_of(A, u'第一階')] = A[body_of(A, u'第一階')].rstrip()[:-1] + u'、〔案例13〕落水救拔。'
A[h] = re.sub(u'共 \\d+ 案', u'共 12 案', A[h])
rc1, o1 = run(A, u'jia')
ok1 = rc1 == 1 and u'案013' in o1 or rc1 == 1 and u'[13' in o1
print(u'甲｜無犯入極刑階➔退%d・點名13=%s' % (rc1, bool(ok1)))

# 乙・只改自報之數
B = list(BASE)
h2 = head_of(B, u'第七階')
B[h2] = re.sub(u'共 \\d+ 案', u'共 30 案', B[h2])
rc2, o2 = run(B, u'yi')
ok2 = rc2 == 1 and u'宣稱30' in o2
print(u'乙｜自報數➔30｜退%d・報數不合=%s' % (rc2, ok2))

# 丙・EXEMPT 之案移入他不相刑之階（13 已用；今以 EXEMPT 之 102 移入極刑階，其據乃突吉羅）
C = list(BASE)
c = [x for x in C]
h3 = head_of(c, u'第一階')
c[body_of(c, u'第一階')] = c[body_of(c, u'第一階')].rstrip()[:-1] + u'、〔案例99〕難民借衣遣使。'
c[h3] = re.sub(u'共 \\d+ 案', u'共 12 案', c[h3])
rc3, o3 = run(c, u'bing')
ok3 = rc3 == 1 and u'[99' in o3
print(u'丙｜非豁免之開許案入極刑階➔退%d・點名99=%s' % (rc3, ok3))

for f in os.listdir(TMPD):
    os.remove(os.path.join(TMPD, f))
os.rmdir(TMPD)
allok = ok1 and ok2 and ok3
print(u'———— 尺十負測：三針%s' % (u'俱中' if allok else u'有未中'))
sys.exit(0 if allok else 1)
