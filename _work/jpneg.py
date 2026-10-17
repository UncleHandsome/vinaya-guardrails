# -*- coding: utf-8 -*-
# 負測：新檢第 57 條（印面無日新字体）——印面植病須 FAIL，底冊植病須不報
import io, os, shutil, subprocess, sys, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, u'ver38四分律_起心動念心智分析框架_修正版.md')
BAK = os.path.join(ROOT, u'_work', u'_jpbak.md')
shutil.copy(MD, BAK)
h0 = hashlib.sha256(io.open(BAK, 'rb').read()).hexdigest()
env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONPATH=ROOT)
JP = u'缽'


def chk(tag):
    r = subprocess.run([sys.executable, '_tk.py', 'check'], capture_output=True,
                       text=True, encoding='utf-8', env=env, cwd=ROOT)
    hit = [x for x in r.stdout.split('\n') if u'日新字体' in x]
    print(u'%s ｜ rc=%d ｜ %s' % (tag, r.returncode, hit[0].strip() if hit else u'<無此檢>'))
    return r.returncode, (hit[0] if hit else u'')


lines = io.open(MD, encoding='utf-8').read().split('\n')
i1 = next(k for k, l in enumerate(lines) if l.startswith(u'# 第四章'))
i2 = next(k for k, l in enumerate(lines) if l.startswith(u'# 附錄C'))
p1 = next(k for k in range(i1 + 1, len(lines)) if u'文憑鉢具' in lines[k])
lines[p1] = lines[p1].replace(u'文憑鉢具', u'文憑' + JP + u'具', 1)
io.open(MD, 'w', encoding='utf-8', newline='\n').write(u'\n'.join(lines))
rc1, s1 = chk(u'印面植『缽』')
lines[p1] = lines[p1].replace(JP, u'鉢', 1)
lines[i2] = lines[i2] + u'（底冊植' + JP + u'形自述）'
io.open(MD, 'w', encoding='utf-8', newline='\n').write(u'\n'.join(lines))
rc2, s2 = chk(u'底冊植『缽』')
shutil.copy(BAK, MD)
os.remove(BAK)
h1 = hashlib.sha256(io.open(MD, 'rb').read()).hexdigest()
rc3, s3 = chk(u'復原')
ok = rc1 == 1 and rc2 == 0 and rc3 == 0 and h0 == h1
print(u'復原哈希=%s  判定=%s' % (h1[:8], 'PASS' if ok else 'FAIL'))
