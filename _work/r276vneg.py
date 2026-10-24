# -*- coding: utf-8 -*-
"""276 續・尺二負測：新管轄（原典欄・自標出處之段）之四道針，須「因判決而紅」且「點名真答案」。

針路：甲・原典欄內嵌跨行之偽引文 ➔ 尺二必點名；
      乙・補遺『◎原典』段內嵌偽引文 ➔ 尺二必點名（此區舊制全在尺外）；
      丙・摄述清單（冒號引出之條列）內嵌術語 ➔ 尺二必不點名（特異性：免把術語當偽供）；
      丁・同線冠出處之偽引文 ➔ 尺二讓給尺三，尺三必點名（兩尺之縫無逃逸）。

用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r276vneg.py
退碼：四針皆如所期方 0。
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
import _casedef as CD                                              # noqa: E402
import _tk                                                     # noqa: E402

env = dict(os.environ, PYTHONIOENCODING=u'utf-8')
TMPD = tempfile.mkdtemp(prefix=u'r276vneg_')
BASE = _tk.MAIN_LINES


def plant(old, new, tag, want=1):
    """以唯一錨改冊之副本；錨非一即擲（未植不許默過）。"""
    n = sum(x.count(old) for x in BASE)
    if n != want:
        raise AssertionError(u'%s｜錨見 %d 次（須 %d）' % (tag, n, want))
    return [x.replace(old, new) for x in BASE]


def run(tool, path):
    p = subprocess.run([sys.executable, u'-X', u'utf8', os.path.join(WORK, tool), path],
                       capture_output=True, text=True, encoding=u'utf-8', env=env)
    return p.returncode, (p.stdout or u'') + (p.stderr or u'')


def probe(lines, needle, tool, n):
    p = os.path.join(TMPD, u'p%d.md' % n)
    io.open(p, u'w', encoding=u'utf-8').write(u'\n'.join(lines))
    rc, out = run(tool, p)
    hit = needle in out
    try:
        os.remove(p)
    except OSError:
        pass
    return rc, hit, out


FAKE1 = u'此係負測偽造之律文語料必無可證'
FAKE2 = u'又此亦負測偽造之句語料必無'
FAKE3 = u'攝述清單內之術語負測不該入宣稱'
FAKE4 = u'同線冠出處之偽句負測須歸尺三'

VB = CD.verb_blocks(BASE)
if len(VB) < 2:
    raise AssertionError(u'原典欄不可見（負測無錨）')
_a, _b, _lab = VB[0]
PLANT_JIA = BASE[:_b - 1] + [u'> 「%s。」' % FAKE1] + BASE[_b - 1:]

CASES = [
    (u'甲｜欄內跨行（插於第一原典欄之末行前）',
     PLANT_JIA, FAKE1, u'v39quote.py', True),
    (u'乙｜補遺◎原典段',
     plant(u'> **「若夢中失，不犯。」**  ',
           u'> **「若夢中失，不犯。」**  \n> 「%s。」' % FAKE2, u'乙'),
     FAKE2, u'v39quote.py', True),
    (u'丙｜摄述清單之術語（特異性）',
     plant(u'給予當面質證對質之機會；',
           u'給予當面質證對質之機會；又「%s」乃本書之術語' % FAKE3, u'丙'),
     FAKE3, u'v39quote.py', False),
    (u'丁｜同線冠出處（讓於尺三）',
     plant(u'給予當面質證對質之機會；',
           u'給予當面質證對質之機會；《四分律》卷五十四云：「%s。」' % FAKE4, u'丁'),
     FAKE4, u'v39quote2.py', True),
]

bad = 0
for n, (tag, lines, needle, tool, expect) in enumerate(CASES, 1):
    rc, hit, out = probe(lines, needle, tool, n)
    ok = (hit == expect) and (rc == 1 if expect else rc == 0)
    if not ok:
        bad += 1
    print(u'%-22s %-13s｜期%s・得%s・rc=%d｜%s' % (
        tag, tool, u'點名' if expect else u'不點名', u'點名' if hit else u'不點名', rc,
        u'中' if ok else u'✗ 不如所期：' + u'　'.join(
            l for l in out.rstrip().split(u'\n') if re.search(u'非逐字|未標界|✗', l))[:150]))
try:
    os.rmdir(TMPD)
except OSError:
    pass
print(u'———— 尺二負測：%d 針中 %d' % (len(CASES), len(CASES) - bad))
sys.exit(1 if bad else 0)
