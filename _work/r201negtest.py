# -*- coding: utf-8 -*-
"""r201negtest.py —— `r188tail` 尺修之負測（第 201 輪）。

本輪之修在**收窄**甲目（引列式不再算『無末標』）。『凡擴級之閘，必以同級植病證其擴到』——
收窄亦須兩證：**真漏標仍須報**（陽性），**引列常式不得再報**（陰性對照，否則只是消音）。
另證己桶確能收到引列之數（新桶非虛設）。
"""
import io, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
MASTER = u'ver38四分律_起心動念心智分析框架_修正版.md'
COP = u'_work/_r201cop.md'
BASE = io.open(MASTER, encoding='utf-8').read()
PAT = re.compile(u'甲·有末標與無末標並存 (\\d+)｜乙·。與；並存 (\\d+)｜丙·其他混式 (\\d+)')
PAT2 = re.compile(u'己·引列領子列（破折號收，計數不判）(\\d+) 巢')


def save(lines):
    io.open(COP, 'w', encoding='utf-8', newline=u'\n').write(u'\n'.join(lines))


def run(req):
    cmd = [sys.executable, u'-X', u'utf8', u'_work/r188tail.py', COP]
    if req:
        cmd.append(u'require-hit')
    env = dict(os.environ, PYTHONPATH=u'.', PYTHONIOENCODING=u'utf-8')
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    out = p.communicate()[0].decode(u'utf-8', u'replace')
    a, b, c = [int(x) for x in PAT.search(out).groups()]
    d = int(PAT2.search(out).group(1))
    return a, b, c, d, p.returncode, out


def lines_of():
    return BASE.split(u'\n')


fails = []

# ① 陽性：本輪剛補句號之第七章巢（L8647『涉案正理…／天平衝突…？／稱重法式…。』三項並列），
#    還其旧形（刪去項一末標）⇒ 真漏標 ⇒ 甲須報（此即 201 輪所治之形，植回以證尺仍有牙）
ls = lines_of()
assert ls[8646].rstrip().endswith(u'（不可逆底線）。'), ls[8646][-24:]
ls[8646] = ls[8646].rstrip()[:-1]
save(ls)
a, b, c, d, rc, out = run(False)
ok = a >= 1
print(u'① 植真漏標（削一處句號）→ 甲=%d（須 ≥1）：%s' % (a, u'中' if ok else u'✗不中'))
if not ok:
    fails.append(u'真漏標未報')

# ② 陰性：引列式（『——』收＋其下 * 子項）不得算漏標
ls = lines_of()
assert ls[4736].rstrip().endswith(u'——'), ls[4736][-14:]
save(ls)
a, b, c, d, rc, out = run(False)
ok = (a == 0 and d == 92)
print(u'② 主檔現形（引列式 92 巢）→ 甲=%d・己=%d（須 0・92）：%s' % (a, d, u'中' if ok else u'✗不中'))
if not ok:
    fails.append(u'引列式仍誤報或己桶失數')

# ③ 陰性之極：引列項末之『——』改成句號 ⇒ 該巢應轉為純一式而不報
ls = lines_of()
ls[4736] = ls[4736].rstrip()[:-2] + u'。'
save(ls)
a2, b2, c2, d2, rc2, out2 = run(False)
ok = (d2 == 91)
print(u'③ 削一引列之破折號 → 己=%d（須 91，證己桶隨形而動）：%s' % (d2, u'中' if ok else u'✗不中'))
if not ok:
    fails.append(u'己桶不隨動')

# ④ 丁／戊 之路徑仍通（舊負測之植法：羅項末項未收句號）
ls = lines_of()
i = [k for k, l in enumerate(ls) if l.startswith(u'   * ') and l.rstrip().endswith(u'；')][0]
ls[i] = ls[i].rstrip()[:-1] + u'、'
save(ls)
a3, b3, c3, d3, rc3, out3 = run(True)
ok = rc3 == 0
print(u'⑤ 植項末誤頓號 → require-hit 退 %d（須 0＝有報）：%s' % (rc3, u'中' if ok else u'✗不中'))
if not ok:
    fails.append(u'戊路未逮')

if os.path.exists(COP):
    os.remove(COP)
print(u'負測：%d 路，不中 %d。' % (4, len(fails)))
sys.exit(1 if fails else 0)
