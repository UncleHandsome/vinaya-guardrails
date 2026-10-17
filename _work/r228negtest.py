# -*- coding: utf-8 -*-
"""第 228 輪新軸 r228self 之負測（留檔）：五路分擊其口徑，各中其目。
   主檔唯讀——TKSRC 指副本、用完即除，並斷主檔哈希前後相同。
   陰性對照三路：『本節第X款』之正格、跨節之指針、表列之自足指針俱勿報。"""
from __future__ import unicode_literals
import hashlib
import io
import os
import subprocess
import sys

NL = chr(10)
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MD = u'ver38四分律_起心動念心智分析框架_修正版.md'
NEW = u'_work/_r228neg.md'
raw = io.open(MD, encoding=u'utf-8').read()
H0 = hashlib.sha256(raw.encode(u'utf-8')).hexdigest()
BASE = raw.split(NL)
AXIS = u'_work/r228self.py'

A_SELF = u'依本節第四款『缺席管轄之例外』之則'
A_EXPL = u'（詳本章第四節第四、五款之憲政相容聲明與適用嚴限）'
A_TBL = u'（本格另有僧俗邊界之瞋通則：外道論戰之鬥勝心，說在第二章第五節治理通則）'


def run(lines, want_rc, wants, tag, clean=False):
    io.open(NEW, u'w', encoding=u'utf-8', newline=NL).write(NL.join(lines))
    env = dict(os.environ)
    env[u'TKSRC'] = NEW
    env[u'PYTHONIOENCODING'] = u'utf-8'
    p = subprocess.Popen([sys.executable, u'-X', u'utf8', AXIS],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    out = p.communicate()[0].decode(u'utf-8', u'replace')
    rc = p.returncode
    ok = rc == want_rc and all(w in out for w in wants)
    if clean:
        ok = ok and (u'自指之針 0 處' in out)
    print(u'%-42s rc=%d（期 %d）%s' % (tag, rc, want_rc, u'中' if ok else u'不中'))
    if not ok:
        for l in out.strip().split(NL)[-3:]:
            print(u'      · %s' % l[:118])
    return ok


def swap(old, new):
    a = list(BASE)
    hits = [i for i, l in enumerate(a) if old in l]
    assert len(hits) == 1, u'植病之錨非恰一：%s（%d 見）' % (old[:22], len(hits))
    a[hits[0]] = a[hits[0]].replace(old, new, 1)
    return a


cases = []
cases.append(run(list(BASE), 0, [u'自指之針 0 處'], u'⓪ 淨本（含表列自足指針・勿報）', clean=True))
cases.append(run(swap(A_SELF, u'依本章第一節『缺席管轄之例外』之則'), 1,
                 [u'自指之針 1 處', u'本章第一節'], u'① 植『本章第X節』原地打轉（當報）'))
cases.append(run(swap(A_SELF, A_SELF + u'（說在第四章第一節第二款）'), 1,
                 [u'第四章第一節'], u'② 植『第N章第X節』他稱自指（當報）'))
cases.append(run(swap(A_SELF, u'依本節第四款之缺席例'), 0, [u'自指之針'],
                 u'③ 本節款級自稱（正格・勿報）', clean=True))
cases.append(run(swap(A_TBL, A_TBL.replace(u'第二章第五節', u'第二章第六節')), 0, [u'自指之針'],
                 u'④ 表列改指他節（跨節指針・勿報）', clean=True))

if os.path.exists(NEW):
    os.remove(NEW)
H1 = hashlib.sha256(io.open(MD, encoding=u'utf-8').read().encode(u'utf-8')).hexdigest()
print(u'主檔哈希前後相同：%s｜副本已除：%s' % (u'是' if H0 == H1 else u'否（大害！）',
                                               u'是' if not os.path.exists(NEW) else u'否'))
ok = all(cases) and H0 == H1
print(u'負測：%s（五路俱中且主檔無染方過）' % (u'過' if ok else u'不過'))
sys.exit(0 if ok else 1)
