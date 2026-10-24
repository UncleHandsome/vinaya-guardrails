# -*- coding: utf-8 -*-
"""269 輪・負測：新不變量第 29 目『印面不作工程黑話與官僚代號』之三道植病（各證一詞類）。

判式四件：退碼 1・該目行現 FAIL・✗ 明细行點名**被植之詞**・stderr 空；另以正本為第四道對照（須 29/29）。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r269neg.py
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
TMP = os.path.join(ROOT, u'_work', u'_neg269.md')
TOOL = os.path.join(ROOT, u'_work', u'v39chk.py')
ITEM = u'印面不作工程黑話'


def _green(tally):
    """自比 N/N，不寫死今制之數（新增一目即假紅，本輪親見）。"""
    for x in tally:
        m = re.search(u'不變量 (\\d+)/(\\d+) 全綠', x)
        if m:
            return m.group(1) == m.group(2)
    return False

CASES = [
    (u'植工程黑話『解耦』', u'**3. 雙軌人事分立**', u'**3. 雙軌人事解耦**', u'解耦'),
    (u'植官僚代號『甲級』', u'| **實體閘門層** | **六重心智閘門**', u'| **甲級** | **六重心智閘門**', u'甲級'),
    (u'植公文形制『存檔卡』', u'自然人親簽？裁決登錄日誌？', u'自然人親簽？裁決存檔卡？', u'存檔卡'),
]

base = io.open(SRC, encoding=u'utf-8').read()


def run(path):
    r = subprocess.run([sys.executable, u'-X', u'utf8', TOOL, path],
                       capture_output=True, text=True, encoding=u'utf-8')
    lines = (r.stdout or u'').split(u'\n')
    return (r.returncode,
            [x for x in lines if ITEM in x and u'FAIL' in x],
            [x for x in lines if x.strip().startswith(u'✗')],
            (r.stderr or u'').strip(),
            [x for x in lines if u'不變量' in x])


allok = True
for tag, old, new, word in CASES:
    assert base.count(old) == 1, u'%s：錨命中 %d（須恰 1）' % (tag, base.count(old))
    shutil.copyfile(SRC, TMP)
    try:
        txt = io.open(TMP, encoding=u'utf-8').read()
        p = txt.replace(old, new, 1)
        assert p.count(new) == 1 and p.count(old) == 0, u'%s：植入未生效' % tag
        io.open(TMP, 'w', encoding=u'utf-8', newline=u'\n').write(p)
        rc, fail, det, err, tally = run(TMP)
        named = [x for x in det if word in x]
        ok = rc == 1 and fail and named and not err
        allok = allok and ok
        print(u'%-22s rc=%d・該目 FAIL=%d・點名『%s』=%d・stderr=%r ➔ %s'
              % (tag, rc, len(fail), word, len(named), err[:34], u'逮' if ok else u'不逮'))
        for x in (named or det)[:1]:
            print(u'       ', x.strip()[:96])
    finally:
        if os.path.exists(TMP):
            os.remove(TMP)

rc, fail, det, err, tally = run(SRC)
ok0 = rc == 0 and not fail and not err and _green(tally)
allok = allok and ok0
print(u'正本對照：rc=%d・FAIL=%d・stderr=%r｜%s' % (rc, len(fail), err[:34],
      (tally[-1].strip()[:44] if tally else u'')))
print(u'———— 總判：%s（三道植詞俱須點名其詞・還原須 29/29，且不以崩為紅）'
      % (u'全逮' if allok else u'有未逮'))
sys.exit(0 if allok else 1)
