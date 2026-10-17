# -*- coding: utf-8 -*-
# 第 192 輪·負測：證 r185orphan 擴尺之後『短式有牙、問句與括注名目不誤傷、長式舊徑未壞』。
# 只寫副本、不動主檔；植病同位換字、不增不刪行（180 輪之制）。
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
COP = u'_work/r192neg.md'
env = dict(os.environ)
env['PYTHONIOENCODING'] = 'utf-8'
env['PYTHONPATH'] = '.'

GOOD = u'「維護僧譽、顧全大局、學會包容」'          # 印面恰一之錨（185 輪負測同錨）
PLANTS = [
    (u'短式·制辭（應報）', u'「聽與受具足戒」', 1),
    (u'短式·問句（應擯）', u'「彼豈非犯波羅夷耶？」', 0),
    (u'短式·括注名目（應擯）', u'「與僧殘戒（與波羅夷戒）」', 0),
    (u'長式·罪相名（應報）', u'「若比丘以妄語覆藏麁罪，其覆即成波羅夷」', 1),
]
PAT = re.compile(u'甲·律文形貌（本軸之的）(\\d+)')


def run(path):
    q = subprocess.run([sys.executable, u'-X', u'utf8', u'_work/r185orphan.py', path, u'require-hit'],
                       capture_output=True, text=True, encoding=u'utf-8', env=env)
    m = PAT.search(q.stdout)
    assert m, q.stdout[:400]
    return int(m.group(1)), q.returncode


def unfound(s):
    st, _ = t.classify(s)
    return not (st in (u'hit', u'skip') or st.startswith(u'other:'))


for name, bad, want in PLANTS:
    assert unfound(bad.strip(u'「」')), u'植病之語竟於語料可查得：%s' % name
a0, rc0 = run(MASTER)
print(u'正路：甲 %d（須 0）｜退 %d（須 1）' % (a0, rc0))
assert a0 == 0 and rc0 == 1

base = io.open(MASTER, encoding=u'utf-8').read().split(u'\n')
idx = [k for k, l in enumerate(base) if GOOD in l]
assert len(idx) == 1, u'植病錨非恰一：%s' % idx
n0 = len(base)
fails = []
for name, bad, want in PLANTS:
    lines = list(base)
    lines[idx[0]] = lines[idx[0]].replace(GOOD, bad, 1)
    assert len(lines) == n0, u'植病改動行數'
    io.open(COP, 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(lines))
    try:
        a1, rc1 = run(COP)
    finally:
        if os.path.exists(COP):
            os.remove(COP)
    ok = (a1 == want)
    if not ok:
        fails.append(name)
    print(u'%-24s 植後甲 %d（須 %d）｜退 %d ｜ %s' % (name, a1, want, rc1, u'中' if ok else u'不中'))

mt = io.open(MASTER, encoding=u'utf-8').read()
print(u'主檔：%s' % (u'如舊' if GOOD in mt and all(p[1] not in mt for p in PLANTS) else u'已臟！'))
ok = not fails and GOOD in mt
print(u'結果斷：%s' % (u'擴尺有牙——短式制辭即報，問句與名目不誤傷，長式舊徑仍在' if ok else u'負測不合：%s' % fails))
sys.exit(0 if ok else 1)
