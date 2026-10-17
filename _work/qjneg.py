# -*- coding: utf-8 -*-
# 負測：quotejudge.py —— 印面植一筆「佛判：『○○』」之虛句須報病退 1；底冊植同句須不報；復原後哈希相同
import io, os, shutil, subprocess, sys, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, u'ver38四分律_起心動念心智分析框架_修正版.md')
BAK = os.path.join(ROOT, u'_work', u'_qjbak.md')
env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONPATH=ROOT)
FAKE = u'佛判：「汝今大得利益，永不復犯！」'


def run(tag):
    r = subprocess.run([sys.executable, '_work/quotejudge.py'], capture_output=True,
                       text=True, encoding='utf-8', env=env, cwd=ROOT)
    print(u'%s｜rc=%d｜%s' % (tag, r.returncode, r.stdout.strip().split('\n')[0]))
    return r


shutil.copy(MD, BAK)
h0 = hashlib.sha256(io.open(BAK, 'rb').read()).hexdigest()
L = io.open(MD, encoding='utf-8').read().split('\n')
i6 = next(k for k, l in enumerate(L) if u'佛判：「無犯。」——救拔人命' in l)
s6 = next(k for k, l in enumerate(L) if l.startswith(u'# 第六章'))
sm = next(k for k, l in enumerate(L) if l.startswith(u'# 附錄M'))
assert s6 < i6 < sm, (s6, i6, sm)

orig = L[i6]
L[i6] = orig.replace(u'佛判：「無犯。」', FAKE, 1)
io.open(MD, 'w', encoding='utf-8', newline='\n').write(u'\n'.join(L))
r1 = run(u'印面植虛佛判')
L[i6] = orig
L[sm] = L[sm] + FAKE            # 底冊（附錄M 篇題行）植同句——不入印本，故不應報
io.open(MD, 'w', encoding='utf-8', newline='\n').write(u'\n'.join(L))
r2 = run(u'底冊植虛佛判')
shutil.copy(BAK, MD)
os.remove(BAK)
h1 = hashlib.sha256(io.open(MD, 'rb').read()).hexdigest()
r3 = run(u'復原')
ok = (r1.returncode == 1 and u'永不復犯' in r1.stdout and r2.returncode == 0
      and r3.returncode == 0 and h0 == h1)
print(u'復原哈希=%s  判定=%s' % (h1[:8], 'PASS' if ok else 'FAIL'))
