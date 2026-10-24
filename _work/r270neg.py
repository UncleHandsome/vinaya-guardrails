# -*- coding: utf-8 -*-
"""270 輪・負測：第 10 目新增之『蒙上省寫』網——兩道植病（落空・節制不合）＋正本對照。

判式四件：退碼 1・『章節指針可達』一行現 FAIL・✗ 明細點名被植之句・stderr 空。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r270neg.py
"""
import io
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
SRC = os.path.join(ROOT, NAME)
TMP = os.path.join(ROOT, u'_work', u'_neg270.md')
TOOL = os.path.join(ROOT, u'_work', u'v39chk.py')
ITEM = u'章節指針可達'


def _green(tally):
    """自比 N/N，不寫死今制之數。"""
    for x in tally:
        m = re.search(u'不變量 (\\d+)/(\\d+) 全綠', x)
        if m:
            return m.group(1) == m.group(2)
    return False

CASES = [
    (u'植省寫之落空（第八章無第九節）',
     u'（人事與勞動）與第四節（財產、數位與醫療）', u'（人事與勞動）與第九節（財產、數位與醫療）',
     u'第九節'),
    (u'植省寫於不以節為序之章（第三章）',
     u'詳見第八章第二節與第四節。', u'詳見第三章第二節與第五節。', u'第三章'),
]


def run(path):
    r = subprocess.run([sys.executable, u'-X', u'utf8', TOOL, path],
                       capture_output=True, text=True, encoding=u'utf-8')
    lines = (r.stdout or u'').split(u'\n')
    return (r.returncode, [x for x in lines if ITEM in x and u'FAIL' in x],
            [x for x in lines if x.strip().startswith(u'✗')],
            (r.stderr or u'').strip(), [x for x in lines if u'不變量' in x])


base = io.open(SRC, encoding=u'utf-8').read()
allok = True
for tag, old, new, want in CASES:
    assert base.count(old) == 1, u'%s：錨命中 %d（須恰 1）' % (tag, base.count(old))
    shutil.copyfile(SRC, TMP)
    try:
        txt = io.open(TMP, encoding=u'utf-8').read()
        p = txt.replace(old, new, 1)
        assert p.count(new) == 1 and p.count(old) == 0, u'%s：植入未生效' % tag
        io.open(TMP, 'w', encoding=u'utf-8', newline=u'\n').write(p)
        rc, fail, det, err, tally = run(TMP)
        named = [x for x in det if want in x]
        ok = rc == 1 and fail and named and not err
        allok = allok and ok
        print(u'%-34s rc=%d・FAIL=%d・點名=%d・stderr=%r ➔ %s'
              % (tag, rc, len(fail), len(named), err[:32], u'逮' if ok else u'不逮'))
        for x in (named or det)[:1]:
            print(u'       ', x.strip()[:104])
    finally:
        if os.path.exists(TMP):
            os.remove(TMP)

rc, fail, det, err, tally = run(SRC)
ok0 = rc == 0 and not fail and not err and _green(tally)
allok = allok and ok0
print(u'正本對照：rc=%d・FAIL=%d・stderr=%r｜%s' % (rc, len(fail), err[:32],
      (tally[-1].strip()[:42] if tally else u'')))
print(u'———— 總判：%s（省寫須點名其落空之節與不以節為序之章，還原須 29/29）'
      % (u'全逮' if allok else u'有未逮'))
sys.exit(0 if allok else 1)
