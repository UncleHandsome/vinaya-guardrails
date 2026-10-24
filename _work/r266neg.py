# -*- coding: utf-8 -*-
"""266 輪・第 26 目（印面命題不作『某某令』）之負測：植一命題→紅；還原→綠。

必查 stderr（以崩為紅者不算逮得）；並植一枚**對事**與一枚**對讀者**，證尺認形不認字。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r267neg.py
"""
import io
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
SRC = os.path.join(ROOT, NAME)
TMP = os.path.join(ROOT, u'_work', u'_negling.md')
TOOL = os.path.join(ROOT, u'_work', u'v39chk.py')

base = io.open(SRC, encoding=u'utf-8').read()
ANCH = u'# 第二章　心所動力與生活場域'
assert base.count(ANCH) == 1
P1 = u'\n\n**某某封口令**：負測植入，證尺能逮對眾之『令』。\n'
P2 = u'\n> **【負測消磁令：一判即了】**\n'


def run():
    env = dict(os.environ, PYTHONIOENCODING=u'utf-8')
    p = subprocess.run([sys.executable, u'-X', u'utf8', TOOL, TMP],
                       capture_output=True, text=True, encoding=u'utf-8', env=env)
    say = [ln for ln in (p.stdout or u'').split(u'\n') if u'某某令' in ln or u'不變量' in ln]
    return p.returncode, say, (p.stderr or u'').strip()


got = {}
for tag, add in ((u'植對眾令', P1), (u'植對讀者令', P2)):
    io.open(TMP, 'w', encoding=u'utf-8', newline=u'\n').write(base.replace(ANCH, ANCH + add, 1))
    rc, say, err = run()
    bite = any(u'FAIL' in x or u'✗' in x for x in say)
    got[tag] = (rc, bite, err)
    print(u'%-10s rc=%d・逮=%s・stderr=%r｜%s' % (tag, rc, bite, err[:60],
                                                 u' | '.join(x.strip()[:52] for x in say[:2])))
io.open(TMP, 'w', encoding=u'utf-8', newline=u'\n').write(base)
rc0, say0, err0 = run()
os.remove(TMP)
print(u'%-10s rc=%d・stderr=%r｜%s' % (u'還原', rc0, err0[:60], (say0[0].strip()[:52] if say0 else u'')))
ok = (rc0 == 0 and not err0 and all(g[0] == 1 and g[1] and not g[2] for g in got.values()))
print(u'———— 判定：%s（須兩植俱紅而還原綠，且不以崩為紅）' % (u'中' if ok else u'不中'))
sys.exit(0 if ok else 1)
