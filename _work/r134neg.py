# -*- coding: utf-8 -*-
# 負測： planting a malformed table row must trip invariant #56
import io, os, shutil, subprocess, hashlib, sys

MD = u'ver38四分律_起心動念心智分析框架_修正版.md'
BAK = u'_work/_r134bak.md'
shutil.copy(MD, BAK)
h0 = hashlib.sha256(io.open(BAK, 'rb').read()).hexdigest()

L = io.open(MD, encoding='utf-8').read().split('\n')
i = 11467  # 0-based for L11468
assert L[i].startswith(u'| **第二章·持戒慢'), L[i][:30]
L[i] = L[i].rstrip()[:-1]          # 去掉尾管
io.open(MD, 'w', encoding='utf-8', newline='\n').write(u'\n'.join(L))

env = dict(os.environ, PYTHONIOENCODING='utf-8')
r = subprocess.run([sys.executable, '_tk.py', 'check'], capture_output=True,
                   text=True, encoding='utf-8', env=env)
hit = [x for x in r.stdout.split('\n') if u'表格欄數' in x]
print(u'rc=%d' % r.returncode)
print((hit[0] if hit else u'<無此檢>'))

shutil.copy(BAK, MD)
os.remove(BAK)
h1 = hashlib.sha256(io.open(MD, 'rb').read()).hexdigest()
print(u'復原=%s' % ('OK' if h0 == h1 else 'FAIL'))
print(u'負測判定=%s' % ('PASS' if r.returncode == 1 and hit and u'FAIL' in hit[0] and h0 == h1 else 'FAIL'))
