# -*- coding: utf-8 -*-
"""271 輪・負測：新不變量第 30 目『書名號內之本律篇名須見於語料』之兩道植病。

第一道＝**原樣植回本輪所刪之虛篇名**（《僧殘犍度》，語料 0 見）；
第二道＝植一枚**帶書名前綴**之虛篇名（《四分律·偽說犍度》）——專證『剝前綴』一支會響，
        否則剝錯或根本沒剝，尺會永遠無聲（第十八度『植錯→不退就是該檢不存在』）。
判式四件：退 1・該目 FAIL・✗ 行點名被植之篇名・stderr 空；另以正本為第三道對照（須 30/30）。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r271neg.py
"""
import io
import os
import shutil
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
SRC = os.path.join(ROOT, NAME)
TMP = os.path.join(ROOT, u'_work', u'_neg271.md')
TOOL = os.path.join(ROOT, u'_work', u'v39chk.py')
ITEM = u'篇名須見於語料'

CASES = [
    (u'植回本輪所刪之虛篇名', u'律典於《覆藏犍度》中，立四種治法羯磨',
     u'律典於《僧殘犍度》與《覆藏犍度》中，立四種治法羯磨', u'僧殘犍度'),
    (u'植帶書名前綴之虛篇名（證剝前綴之支會響）', u'《四分律·呵責犍度》原生立',
     u'《四分律·偽說犍度》原生立', u'偽說犍度'),
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
        print(u'%-38s rc=%d・FAIL=%d・點名=%d・stderr=%r ➔ %s'
              % (tag, rc, len(fail), len(named), err[:30], u'逮' if ok else u'不逮'))
        for x in (named or det)[:1]:
            print(u'       ', x.strip()[:96])
    finally:
        if os.path.exists(TMP):
            os.remove(TMP)

rc, fail, det, err, tally = run(SRC)
ok0 = rc == 0 and not fail and not err and any((lambda mm: bool(mm) and mm.group(1) == mm.group(2))(re.search(u'不變量 (\\d+)/(\\d+) 全綠', x)) for x in tally)
allok = allok and ok0
print(u'正本對照：rc=%d・FAIL=%d・stderr=%r｜%s' % (rc, len(fail), err[:30],
      (tally[-1].strip()[:40] if tally else u'')))
print(u'———— 總判：%s（兩道須各點其名，還原須 30/30，且不以崩為紅）'
      % (u'全逮' if allok else u'有未逮'))
sys.exit(0 if allok else 1)
