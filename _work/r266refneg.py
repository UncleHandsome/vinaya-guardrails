# -*- coding: utf-8 -*-
"""266 輪補・第 27 目『案號與案名對合』之負測：植一枚誤號 → 須點名該處而退 1；還原 → 退 0。

必察 stderr（以崩為紅者不算逮得）。判式：**逐行找『✗』且含被植之案名**，
不可拿摘要行充數（本輪初測即因濾行過寬而誤判『不中』——負測之器亦屢次自犯，263／265 同科）。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r266refneg.py
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
TMP = os.path.join(ROOT, u'_work', u'_negref.md')
TOOL = os.path.join(ROOT, u'_work', u'v39chk.py')

base = io.open(SRC, encoding=u'utf-8').read()
OLD = u'〔案例93〕目連神足遭控大妄語'
NEW = u'〔案例100〕目連神足遭控大妄語'          # 100 之卡題乃『涅槃日哀慟』，目連神足實屬 93
assert base.count(OLD) == 1, u'錨命中 %d（須恰 1，不得空跑）' % base.count(OLD)


def run(path):
    r = subprocess.run([sys.executable, u'-X', u'utf8', TOOL, path],
                       capture_output=True, text=True, encoding=u'utf-8')
    out = r.stdout or u''
    lines = out.split(u'\n')
    fail = [x for x in lines if u'案號與案名對合' in x and u'FAIL' in x]
    detail = [x for x in lines if x.strip().startswith(u'\u2717') and u'目連' in x]
    tally = [x for x in lines if u'不變量' in x]
    return r.returncode, fail + detail + tally, (r.stderr or u'').strip()


shutil.copyfile(SRC, TMP)
planted = io.open(TMP, encoding=u'utf-8').read().replace(OLD, NEW, 1)   # 先讀再寫：`open(w)` 會在求值 `obj.method(arg)` 之 obj 時即截檔
assert planted.count(NEW) == 1 and planted.count(OLD) == 0, u'植入未生效'
io.open(TMP, 'w', encoding=u'utf-8', newline=u'\n').write(planted)
rc1, s1, e1 = run(TMP)
os.remove(TMP)
rc0, s0, e0 = run(SRC)
print(u'植誤號：rc=%d・該目 FAIL=%d・點名=%d・stderr=%r' % (
    rc1, len([x for x in s1 if u'FAIL' in x]), len([x for x in s1 if x.strip().startswith(u'\u2717')]), e1[:60]))
for x in s1[:3]:
    print(u'   ', x.strip()[:112])
print(u'還原：rc=%d・stderr=%r｜%s' % (rc0, e0[:60], (s0[-1].strip()[:52] if s0 else u'')))
ok = (rc1 == 1 and any(u'FAIL' in x for x in s1) and any(x.strip().startswith(u'\u2717') for x in s1)
      and not e1 and rc0 == 0 and not e0)
print(u'———— 判定：%s（須植誤號即點名而退 1・還原退 0・兩道俱不因崩而紅）' % (u'中' if ok else u'不中'))
sys.exit(0 if ok else 1)
