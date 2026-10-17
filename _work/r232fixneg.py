# -*- coding: utf-8 -*-
# r232fixneg　修尺之負測：淨本・印面植一枚（當報）・底冊植一枚（勿報）；末斷主檔哈希不變
import hashlib
import io
import os
import subprocess
import sys

NL = chr(10)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
MD = u'ver38四分律_起心動念心智分析框架_修正版.md'
NEW = u'_work/_r232fplant.md'
GATE = u'第八章捫心自省=16'
ALL = u'不變量 94/94 PASS'
IP_ANCH = u'* **表業延伸認定**'
BOT_ANCH = u'**六、補記（記訖方犯'

BASE = io.open(MD, encoding=u'utf-8').read().split(NL)
H0 = hashlib.sha256(io.open(MD, encoding=u'utf-8').read().encode(u'utf-8')).hexdigest()
assert sum(1 for s in BASE if s.startswith(IP_ANCH)) == 1, u'印面之錨非恰一'
assert sum(1 for s in BASE if s.startswith(BOT_ANCH)) == 1, u'底冊之錨非恰一'


def plant(head, tail):
    a = list(BASE)
    k = [i for i, s in enumerate(a) if s.startswith(head)][0]
    a[k] = a[k] + tail
    return a


def run(lines, want_rc, tag, clean=False):
    io.open(NEW, u'w', encoding=u'utf-8', newline=NL).write(NL.join(lines))
    env = dict(os.environ)
    env[u'TKSRC'] = os.path.abspath(NEW)
    env[u'PYTHONIOENCODING'] = u'utf-8'
    p = subprocess.Popen([sys.executable, u'-X', u'utf8', u'_tk.py', u'check'],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env, cwd=ROOT)
    out = p.communicate()[0].decode(u'utf-8', u'replace')
    rc = p.returncode
    bad = [l for l in out.split(NL) if u'\u2717 ' in l]
    hit = [l for l in bad if GATE in l]
    ok = rc == want_rc and bool(hit) if not clean else (rc == 0 and not bad and ALL in out)
    print(u'%-40s rc=%d（期 %d）｜FAIL %d・中閘 %d → %s' % (tag, rc, want_rc, len(bad), len(hit),
                                                           u'中' if ok else u'不中'))
    if not ok:
        for l in (bad[:3] if bad else out.strip().split(NL)[-2:]):
            print(u'      · %s' % l[:120])
    return ok


cases = [run(BASE, 0, u'⓪ 淨本（94/94 且全綠）', clean=True),
         run(plant(IP_ANCH, u'（示例：**捫心自省** 印面別處冒出一枚）'), 1,
             u'① 第九章植印面一枚（當報）'),
         run(plant(BOT_ANCH, u'（示例：底冊自述引『捫心自省』一枚，不較）'), 0,
             u'② 校勘記植底冊一枚（豁免側・勿報）', clean=True)]
if os.path.exists(NEW):
    os.remove(NEW)
H1 = hashlib.sha256(io.open(MD, encoding=u'utf-8').read().encode(u'utf-8')).hexdigest()
print(u'主檔哈希前後相同：%s｜副本已除：%s' % (u'是' if H0 == H1 else u'否（大害！）',
                                              u'是' if not os.path.exists(NEW) else u'否'))
ok = all(cases) and H0 == H1
print(u'負測：%s（三路俱中且主檔無染方過）' % (u'過' if ok else u'不過'))
sys.exit(0 if ok else 1)
