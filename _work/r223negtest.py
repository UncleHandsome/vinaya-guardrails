# -*- coding: utf-8 -*-
"""第 223 輪留檔器之負測：`_work/closeout.py` 須在諸器有一敗時列名退 1。
   植形：印面一行末添恰一枚空格（不變量 86 所捕・零義之形）；副本走 TKSRC，用完即除。
   所斷五者：closeout 退非 0・結帳列名含 `_tk check`・`check.txt` 唯 FAIL 1 條且即『行末空白』
   （中其目）・『寫檔旗標俱去』之報現行（護主：ledger --go 曾於 TKSRC 下把副本寫回真主檔）
   ・主檔哈希前後相同（植病之測不得染主檔）。"""
from __future__ import unicode_literals
import io, os, subprocess, sys, hashlib

NL = chr(10)
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.getcwd())
MD = u'ver38四分律_起心動念心智分析框架_修正版.md'
raw = io.open(MD, encoding=u'utf-8').read()
L = raw.split(NL)

FENCE = set()
inf = False
for i, l in enumerate(L):
    if l.startswith(u'```'):
        inf = not inf
        FENCE.add(i)
    elif inf:
        FENCE.add(i)

BOT = set()
for nm in (u'附錄C', u'附錄K', u'附錄L', u'附錄M', u'終卷'):
    for i, l in enumerate(L):
        if l.startswith(u'# ' + nm) or l.startswith(u'# ' + nm):
            BOT.add(i)
            break
first_bot = min(BOT)
hit = None
for i in range(first_bot):
    if i in FENCE:
        continue
    l = L[i]
    if l.strip() and not l.endswith(u' ') and not l.startswith(u'|'):
        hit = i
        break
assert hit is not None, u'找不到可植之印面行'
L[hit] = L[hit] + u' '
NEW = u'_work/_r223neg.md'
io.open(NEW, u'w', encoding=u'utf-8', newline=NL).write(NL.join(L))
print(u'植形｜L%d 行末添一枚空格（印面・非圍欄・非底冊；主檔未動）' % (hit + 1))

env = dict(os.environ)
env[u'TKSRC'] = NEW
env[u'PYTHONIOENCODING'] = u'utf-8'
H0 = hashlib.sha256(io.open(MD, encoding=u'utf-8').read().encode(u'utf-8')).hexdigest()
p = subprocess.Popen([sys.executable, u'-X', u'utf8', u'_work/closeout.py', u'--brief'],
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
out = p.communicate()[0].decode(u'utf-8', u'replace')
rc = p.returncode
H1 = hashlib.sha256(io.open(MD, encoding=u'utf-8').read().encode(u'utf-8')).hexdigest()
io.open(u'_work/r223negtest.txt', u'w', encoding=u'utf-8', newline=NL).write(out)
os.remove(NEW)

chk = io.open(u'_work/check.txt', encoding=u'utf-8').read()
fails = [l for l in chk.split(NL) if l.startswith(u'FAIL')]
named = out.split(u'結帳：')[-1]
print(u'負測｜closeout rc=%d（須非 0）｜列名：%s' % (rc, named.strip()[:60]))
print(u'  中其目｜FAIL %d 條：%s' % (len(fails), [l[:26] for l in fails]))
print(u'  護主｜寫檔之器降只讀之報：%s｜主檔哈希不變：%s'
      % (u'有' if u'寫檔旗標俱去' in out else u'無', u'是' if H0 == H1 else u'否（大害！）'))
ok = (rc != 0 and u'_tk check' in named and len(fails) == 1 and u'行末空白' in fails[0]
      and u'寫檔旗標俱去' in out and H0 == H1)
print(u'判定：%s（五者俱真方過）' % (u'過' if ok else u'不過'))
sys.exit(0 if ok else 1)
