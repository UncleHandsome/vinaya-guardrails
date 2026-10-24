# -*- coding: utf-8 -*-
"""276 續・核卷尺負測：併欄求引文（跨行）之後，二針須如所期。

甲・改其出處之卷號 ➔ 必報『不合』並點名其欄（證尺有牙）。
乙・同改卷號，但把引文之中線鋸成兩行（一行不閉、次行方合）➔ 仍須報『不合』
   ——舊制逐行求引號，此植只得『未證』而綠（假綠），新制必須紅。**此針證的是coverage，不是判決。**

用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r276volneg.py
退碼：二針俱如所期方 0。
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
import _casedef as CD                                              # noqa: E402
import _tk                                                     # noqa: E402

env = dict(os.environ, PYTHONIOENCODING=u'utf-8')
L0 = _tk.MAIN_LINES
VOL = re.compile(u'卷\\s*([0-9]+|[一二三四五六七八九十]{1,4})')

# 落點：第一個原典欄之出處行（其內須有《…》與卷號）
i0 = next(k for k, l in enumerate(L0) if l.startswith(u'> **《四分律》卷'))
line = L0[i0]
num = VOL.search(line).group(1)
anchor = u'卷%s' % num
hb = next((k for k in range(i0, -1, -1) if L0[k].startswith(u'#')), i0)
lab = L0[hb].lstrip('#').strip()[:22] + u'｜' + line[:34]
print(u'落點｜%s' % lab)


def run(lines):
    p = os.path.join(tempfile.mkdtemp(prefix=u'r276vol_'), u'book.md')
    io.open(p, u'w', encoding=u'utf-8').write(u'\n'.join(lines))
    q = subprocess.run([sys.executable, u'-X', u'utf8', os.path.join(WORK, u'v39volchk.py'), p],
                       capture_output=True, text=True, encoding=u'utf-8', env=env)
    os.remove(p)
    os.rmdir(os.path.dirname(p))
    return q.returncode, (q.stdout or u'') + (q.stderr or u'')


def count(out):
    m = re.search(u'核合 (\\d+)・不合 (\\d+)・未證 (\\d+)', out)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else (None, None, None)


# ── 甲・改卷號
A = list(L0)
A[i0] = A[i0].replace(anchor, u'卷九十九（偽植）', 1)
rc, out = run(A)
a_ok = rc == 1 and count(out)[1] >= 1
print(u'甲｜改卷號➔期報不合・rc=%d・核/不合/未證=%s・%s' % (rc, count(out), u'中' if a_ok else u'✗'))

# ── 乙・改卷號＋鋸引文成跨行（舊制在此只得未證＝假綠）
B = list(A)
q1 = next(k for k in range(i0, i0 + 12) if L0[k].strip().startswith(u'> 「'))
mid = q1 + 30
B[q1] = L0[q1][:mid]
B.insert(q1 + 1, u'> ' + L0[q1][mid:])
rc2, out2 = run(B)
n_ok, b_ok, u_ok = count(out2)
b_hit = rc2 == 1 and b_ok >= 1                       # 須仍判『不合』而非退回未證
print(u'乙｜鋸成跨行➔期仍報不合（不退回未證）・rc=%d・核/不合/未證=%s・%s' % (
    rc2, count(out2), u'中' if b_hit else u'✗'))
# 對照：同一植法在『舊逐行口徑』下之果（以本器自量：把引文行首之『「』拆開即令同行無閉號）
print(u'對照｜乙之引文跨行形：起行 L%d・訖行 L%d（舊制逐行求號，此段不可得）' % (q1 + 1, q1 + 2))
sys.exit(0 if (a_ok and b_hit) else 1)
