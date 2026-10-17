# -*- coding: utf-8 -*-
"""第 227 輪新軸 r227tie 之負測（留檔）：四路分擊其口徑，各中其目。
   主檔唯讀——TKSRC 指副本、用完即除，並斷主檔哈希前後相同。
   陰性對照兩路：名目短標跨條次（勿報）、底冊植同句兩條次（轉述非宣稱・勿報）。"""
from __future__ import unicode_literals
import hashlib
import io
import os
import subprocess
import sys

NL = chr(10)
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MD = u'ver38四分律_起心動念心智分析框架_修正版.md'
NEW = u'_work/_r227neg.md'
raw = io.open(MD, encoding=u'utf-8').read()
H0 = hashlib.sha256(raw.encode(u'utf-8')).hexdigest()
BASE = raw.split(NL)
AXIS = u'_work/r227tie.py'

A1 = u'律文原句作「若比丘不受諫者，波逸提」'
A2 = u'**殺、盜、婬、妄四根本性罪絕不適用此級差'
A3 = u'『不敬語／違諫戒』（第五十四條）標為本書歸名並附律文原句'


def run(lines, want_rc, wants, tag, clean=False):
    io.open(NEW, u'w', encoding=u'utf-8', newline=NL).write(NL.join(lines))
    env = dict(os.environ)
    env[u'TKSRC'] = NEW
    env[u'PYTHONIOENCODING'] = u'utf-8'
    p = subprocess.Popen([sys.executable, u'-X', u'utf8', AXIS],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    out = p.communicate()[0].decode(u'utf-8', u'replace')
    rc = p.returncode
    ok = rc == want_rc and all(w in out for w in wants)
    if clean:
        ok = ok and (u'條次衝突 0 處' in out)
    print(u'%-40s rc=%d（期 %d）%s' % (tag, rc, want_rc, u'中' if ok else u'不中'))
    if not ok:
        for l in out.strip().split(NL)[-4:]:
            print(u'      · %s' % l[:120])
    return ok


def swap(old, new, frm=None):
    a = list(frm if frm is not None else BASE)
    hits = [i for i, l in enumerate(a) if old in l]
    assert len(hits) == 1, u'植病之錨非恰一：%s（%d 見）' % (old[:22], len(hits))
    a[hits[0]] = a[hits[0]].replace(old, new, 1)
    return a


cases = []
cases.append(run(list(BASE), 0, [u'條次衝突 0 處'], u'⓪ 淨本（同條不同句・勿報）', clean=True))
cases.append(run(swap(A1, A1 + u'（第十二條別說）'), 1, [u'若比丘不受諫者波逸提', u'掛'],
                 u'① 同一原句掛兩條次（當報）'))
cases.append(run(swap(A2, u'第十二條云：' + A2), 0, [u'條次衝突 0 處'],
                 u'② 名目短標掛條次（制辭式過濾・勿報）', clean=True))
# ③ 底冊之同句易條次：乃修訂誌轉述刀前之形，屬豁免（218／226 之裁）——若不豁免，此植即衝突
cases.append(run(swap(A3, A3.replace(u'第五十四條', u'第九十九條')),
                 0, [u'條次衝突 0 處'], u'③ 底冊轉述易條次（豁免・勿報）', clean=True))

if os.path.exists(NEW):
    os.remove(NEW)
H1 = hashlib.sha256(io.open(MD, encoding=u'utf-8').read().encode(u'utf-8')).hexdigest()
print(u'主檔哈希前後相同：%s｜副本已除：%s' % (u'是' if H0 == H1 else u'否（大害！）',
                                               u'是' if not os.path.exists(NEW) else u'否'))
ok = all(cases) and H0 == H1
print(u'負測：%s（四路俱中且主檔無染方過）' % (u'過' if ok else u'不過'))
sys.exit(0 if ok else 1)
