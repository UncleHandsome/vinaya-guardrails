# -*- coding: utf-8 -*-
# 第 183 輪·批三之負測：以副本**同位抽橋**（導言兩行改留空、縫合線改回原句），
# 戊・己兩目須報起（今制 戊『真無一字』17／己 0 → 18／1）。行數不動以保底冊豁免之準。
import io
import os
import re
import subprocess
import sys

MASTER = u'ver38四分律_起心動念心智分析框架_修正版.md'
COP = u'_work/_r183neg.md'
env = dict(os.environ)
env[u'PYTHONIOENCODING'] = u'utf-8'

LEAD = u'法權之空間與主體既備（前節所明結界、四種僧與說白僧）'
JOIN_OLD = u'另有比丘往毘舍離，遇賈客欲走私逃稅'
JOIN_NEW_PRE = u'由圍觀兵威，進而同涉商賈之險——'

lines = io.open(MASTER, encoding=u'utf-8').read().split(u'\n')
n0 = len(lines)
i = [k for k, l in enumerate(lines) if l.startswith(LEAD)]
assert len(i) == 1 and lines[i[0] - 1].strip() == u'', u'導言定位不合：%s' % i
j = [k for k, l in enumerate(lines) if l.startswith(JOIN_NEW_PRE + JOIN_OLD)]
assert len(j) == 1, u'縫合線定位不合：%s' % j
lines[i[0]] = u''                                    # 同位抽橋（行數不動）
lines[j[0]] = lines[j[0]].replace(JOIN_NEW_PRE, u'', 1)
io.open(COP, 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(lines))
assert len(u'\n'.join(lines).split(u'\n')) == n0

p = subprocess.run([sys.executable, u'-X', u'utf8', u'_work/r180voice.py', COP],
                   capture_output=True, text=True, encoding=u'utf-8', env=env)
out = p.stdout
wu = re.search(u'節下即款·真無一字., (\\d+).', out)
ji = re.search(u'己·合編案例起首機械堆疊：(\\d+)', out)
os.remove(COP)
subprocess.run([sys.executable, u'-X', u'utf8', u'_work/r180voice.py'],
               capture_output=True, text=True, encoding=u'utf-8', env=env)
a = int(wu.group(1)) if wu else -1
b = int(ji.group(1)) if ji else -1
print(u'抽橋後：戊·真無一字 %d（須 18）｜己 %d（須 1）' % (a, b))
print(u'分式：%s' % (re.search(u'分式 (\\[[^\\n]*)', out).group(1)[:120] if re.search(u'分式 (\\[[^\\n]*)', out) else u'?'))
ok = (a == 18 and b == 1)
print(u'結果斷：%s（今制 戊 17／己 0，抽橋即報——補橋乃實效）' % (u'器有牙' if ok else u'負測不合'))
sys.exit(0 if ok else 1)
