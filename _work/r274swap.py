# -*- coding: utf-8 -*-
"""274 輪・換：假冊入正本（先備份＋記 SHA，一步可退）。

判式：① 換前必證假冊＝「卷首＋新稿＋第四章以後」三段拼成，且新章三題俱在、舊題『司法天平』已出正文；
      ② 換前現冊之 SHA 與行數入檔（回退之據）；③ 換後讀回校其字节與行數，再以 v39chk 覆核 31/31。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r274swap.py [--apply]
"""
import hashlib
import io
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_work')
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
SRC = os.path.join(ROOT, NAME)
TRIAL = os.path.join(WORK, u'r274trial.md')
BAK = os.path.join(WORK, u'r274swap.bak')
NEWC = io.open(os.path.join(WORK, u'r274new3.md'), encoding=u'utf-8-sig').read().rstrip(u'\n').split(u'\n')

cur = io.open(SRC, encoding=u'utf-8-sig').read().rstrip(u'\n').split(u'\n')
tri = io.open(TRIAL, encoding=u'utf-8-sig').read().rstrip(u'\n').split(u'\n')
A = next(i for i, l in enumerate(cur) if l.startswith(u'# \u7b2c\u4e00\u7ae0'))
Z = next(i for i, l in enumerate(cur) if l.startswith(u'# \u7b2c\u56db\u7ae0'))
SHA0 = hashlib.sha256(io.open(SRC, 'rb').read()).hexdigest()[:12]
print(u'\u73fe\u518a %d \u884c\uff5cSHA %s\uff5c\u65e7 ch1-3\uff1aL%d〜L%d\uff08%d \u884c\uff09' % (
    len(cur), SHA0, A + 1, Z, Z - A))
print(u'\u5047\u518c %d \u884c\uff5c\u65b0 ch1-3 %d \u884c' % (len(tri), len(NEWC)))

assert len(tri) == len(cur) - (Z - A) + len(NEWC), u'\u884c\u6578\u7b49\u5f0f\u4e0d\u7acb'
assert tri[:A] == cur[:A], u'\u5377\u9996\u4e4b\u524d\u6587\u88ab\u52d5'
assert tri[A + len(NEWC):] == cur[Z:], u'\u7b2c\u56db\u7ae0\u4ee5\u5f8c\u88ab\u52d5'
assert tri[A].startswith(u'# \u7b2c\u4e00\u7ae0') and tri[A + len(NEWC)].startswith(u'# \u7b2c\u56db\u7ae0')
t = u'\n'.join(tri)
for k in (u'\u300e\u53f8\u6cd5\u5929\u5e73\u7a31\u91cd\u6cd5', u'\u9598\u9580\u4e8c\uff08\u7e8c\uff09',
          u'\u6b21\u5c0d\u8a71', u'\u89e3\u8026', u'\u4ea4\u4ed8\u5b8c\u6bd5', u'\u5713\u6eff\u92ad\u5e55'):
    assert t.count(k) == 0, u'\u6b98\u8de1\u733a\u5728\u5047\u518c\uff1a%s' % k
print(u'\u4e09\u6bb5\u62fc\u88dd\u5df3\u9a57\uff5c\u5377\u9996\u8207\u7b2c\u56db\u7ae0\u4ee5\u5f8c\u4e00\u5b57\u672a\u52d5\uff5c\u6b98\u8de1\u9664\u5c3d')

if u'--apply' not in sys.argv:
    print(u'\u4e5f\u8dd1\uff5c\u672a\u52d5\u6b63\u672c')
    raise SystemExit(0)

io.open(BAK, 'w', encoding=u'utf-8').write(u'\n'.join(cur) + u'\n')
io.open(SRC, 'w', encoding=u'utf-8').write(u'\n'.join(tri) + u'\n')
after = io.open(SRC, encoding=u'utf-8').read().rstrip(u'\n').split(u'\n')
h = hashlib.sha256(io.open(SRC, 'rb').read()).hexdigest()[:12]
print(u'\u5165\u518a\uff5c%d \u884c\uff5cSHA %s \u2192 %s\uff5c\u5907\u6848 %s' % (
    len(after), SHA0, h, os.path.basename(BAK)))
q = subprocess.run([sys.executable, u'-X', u'utf8', os.path.join(WORK, u'v39chk.py')],
                   capture_output=True, text=True, encoding=u'utf-8', cwd=ROOT,
                   env=dict(os.environ, PYTHONIOENCODING=u'utf-8'))
print(u'\uff5bv39chk\uff5crc=%d｜%s' % (q.returncode, (q.stdout or u'').rstrip().split(u'\n')[-1][:70]))
if q.returncode:
    for l in (q.stdout or u'').split(u'\n'):
        if u'\u2717' in l or u'FAIL' in l:
            print(u'   ' + l[:126])
    print(u'   \u56de\u9000\u65b9\uff1apy _work/r274swap.py --undo')
