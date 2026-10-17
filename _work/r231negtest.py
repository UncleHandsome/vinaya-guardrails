# -*- coding: utf-8 -*-
# r231negtest　新閘 93 之負測（淨本・植問・植嘆・底冊豁免；末斷主檔哈希不變）
import hashlib
import io
import os
import subprocess
import sys

NL = chr(10)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
MD = u'ver38四分律_起心動念心智分析框架_修正版.md'
NEW = u'_work/_r231plant.md'
GATE = u'印面引號之問嘆號後不重疊句號'
ANCH = u'第一章佛陀開庭唯一之千古垂問——**「汝以何心？」**，樹幹貫穿全樹，'

BASE = io.open(MD, encoding=u'utf-8').read().split(NL)
H0 = hashlib.sha256(io.open(MD, encoding=u'utf-8').read().encode(u'utf-8')).hexdigest()
assert sum(1 for s in BASE if ANCH in s) == 1, u'植病之錨非恰一'
D = [i for i, s in enumerate(BASE) if s.startswith(u'**六、補記（記訖方犯')]
assert len(D) == 1, u'底冊之錨非恰一'


def swap(newseg):
    a = list(BASE)
    k = [i for i, s in enumerate(a) if ANCH in s][0]
    a[k] = a[k].replace(ANCH, newseg, 1)
    return a


def run(lines, want_rc, wants, tag, clean=False):
    io.open(NEW, u'w', encoding=u'utf-8', newline=NL).write(NL.join(lines))
    env = dict(os.environ)
    env[u'TKSRC'] = os.path.abspath(NEW)
    env[u'PYTHONIOENCODING'] = u'utf-8'
    p = subprocess.Popen([sys.executable, u'-X', u'utf8', u'_tk.py', u'check'],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env, cwd=ROOT)
    out = p.communicate()[0].decode(u'utf-8', u'replace')
    rc = p.returncode
    bad = [l for l in out.split(NL) if l.strip().startswith(u'FAIL')]
    ok = rc == want_rc and all(w in out for w in wants)
    if clean:
        ok = ok and not bad and (u'不變量 93/93 PASS' in out)
    else:
        ok = ok and len(bad) == 1 and GATE in bad[0]
    print(u'%-42s rc=%d（期 %d）%s%s' % (tag, rc, want_rc, u'中' if ok else u'不中',
                                        u'｜FAIL %d 條' % len(bad) if not clean else u''))
    if not ok:
        for l in (bad[:3] if bad else out.strip().split(NL)[-3:]):
            print(u'      · %s' % l[:126])
    return ok


cases = []
cases.append(run(BASE, 0, [GATE], u'⓪ 淨本（93/93 且全綠）', clean=True))
cases.append(run(swap(u'第一章佛陀開庭唯一之千古垂問——**「汝以何心？」**。樹幹貫穿全樹，'),
                 1, [GATE, u'L8362'], u'① 印面植「？」＋句號（當報并中其行）'))
cases.append(run(swap(u'第一章佛陀開庭唯一之千古垂問——**「汝以何心！」**。樹幹貫穿全樹，'),
                 1, [GATE, u'L8362'], u'② 印面植「！」＋句號（當報，證嘆號一支有牙）'))
planted = list(BASE)
planted[D[0]] = planted[D[0]] + u'（示例形：『汝以何心？』。此乃底冊自述，非印面宣稱）'
cases.append(run(planted, 0, [GATE], u'③ 底冊植同款形（豁免側・勿報）', clean=True))

if os.path.exists(NEW):
    os.remove(NEW)
H1 = hashlib.sha256(io.open(MD, encoding=u'utf-8').read().encode(u'utf-8')).hexdigest()
print(u'主檔哈希前後相同：%s｜副本已除：%s' % (u'是' if H0 == H1 else u'否（大害！）',
                                              u'是' if not os.path.exists(NEW) else u'否'))
ok = all(cases) and H0 == H1
print(u'負測：%s（四路俱中且主檔無染方過）' % (u'過' if ok else u'不過'))
sys.exit(0 if ok else 1)
