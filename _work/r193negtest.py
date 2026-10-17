# -*- coding: utf-8 -*-
# 第 193 輪·負測：鏡像軸短 band 之『引述框架』判準——該報者報、該擯者不報。
# 只寫副本、不動主檔；植病同位換字、不增不刪行。
import io
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as t

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
MASTER = u'ver38四分律_起心動念心智分析框架_修正版.md'
COP = u'_work/r193neg.md'
env = dict(os.environ)
env['PYTHONIOENCODING'] = 'utf-8'
env['PYTHONPATH'] = '.'

VERB = u'妄作異語惱他'                      # 本律逐字（6 字）：「若比丘妄作異語惱他者波逸提」
PLANTS = [
    (u'短式·有引述框架（應報）', u'依『' + VERB + u'』', u'律聽『' + VERB + u'』', u'甲'),
    (u'短式·無框架之名目（應擯）', u'僅存『戒品第十之一』', u'僅存『' + VERB + u'』', u'己'),
]
PAT = re.compile(u'甲·本律逐字（本軸之的）(\\d+)')
PATE = re.compile(u'己·短式名目引用（無框架，報而不治）(\\d+)')


def run(path):
    q = subprocess.run([sys.executable, u'-X', u'utf8', u'_work/r186mirror.py', path, u'require-hit'],
                       capture_output=True, text=True, encoding=u'utf-8', env=env)
    a = PAT.search(q.stdout)
    e = PATE.search(q.stdout)
    assert a and e, q.stdout[:400]
    lst = io.open(u'_work/r186list.txt', encoding=u'utf-8').read()
    return int(a.group(1)), int(e.group(1)), q.returncode, lst


base = io.open(MASTER, encoding=u'utf-8').read().split(u'\n')
a0, e0, rc0, _ = run(MASTER)
print(u'正路：甲 %d（須 0）｜己 %d（須 2）｜退 %d（須 1）' % (a0, e0, rc0))
assert a0 == 0 and rc0 == 1

n0 = len(base)
fails = []
for name, old, new, want_bucket in PLANTS:
    idx = [k for k, l in enumerate(base) if old in l]
    assert len(idx) == 1, u'錨非恰一：%s → %s' % (name, idx)
    lines = list(base)
    lines[idx[0]] = lines[idx[0]].replace(old, new, 1)
    assert len(lines) == n0, u'植病改動行數'
    io.open(COP, 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(lines))
    try:
        a1, e1, rc1, lst = run(COP)
    finally:
        if os.path.exists(COP):
            os.remove(COP)
    # 判其落桶：清冊內該植語之行首碼即其所屬桶（同位植字故計數未必變，須看落點而非總數）
    row = [l for l in lst.split(u'\n') if (u'\t' + VERB + u'\t') in l]
    got = row[0][0] if row else u'？'
    ok = got == want_bucket
    if not ok:
        fails.append(name)
    print(u'%-26s 甲 %d｜己 %d｜落桶 %s（須 %s）｜%s' % (name, a1, e1, got, want_bucket, u'中' if ok else u'不中'))

mt = u'\n'.join(io.open(MASTER, encoding=u'utf-8').read().split(u'\n'))
print(u'主檔：%s' % (u'如舊' if u'律聽『妄作異語惱他』' not in mt else u'已臟！'))
ok = not fails and u'律聽『妄作異語惱他』' not in mt
print(u'結果斷：%s' % (u'鏡像短 band 有牙——有框架即報，名目引用不誤傷' if ok else u'負測不合：%s' % fails))
sys.exit(0 if ok else 1)
