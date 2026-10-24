# -*- coding: utf-8 -*-
"""278・負測：核卷尺之第二管轄（同線冠卷次）與第十尺之名冊對合，須『因判決而紅・點名真答案』。

四道：
  甲 核卷・植假卷於附錄四表行（右欄有卷・左欄無卷）➔ 紅・點名該行・引卷為所植之數
  乙 核卷・『「文」（卷X至Y）』式之卷在引號之右 ➔ 紅・須點名**所植之卷數**（非鄰卷）＝最近歸屬之證
  丙 名冊・改一枝『共 N 案』之數 ➔ 紅・點名該枝之名
  丁 還原 ➔ 兩尺俱 rc=0（病各歸尺，不因崩而紅）
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r278neg.py
"""
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, u'_work')
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
TXT = io.open(BOOK, encoding=u'utf-8-sig').read()
ENV = dict(os.environ, PYTHONIOENCODING=u'utf-8')


def run(script, path):
    r = subprocess.run([sys.executable, u'-X', u'utf8', os.path.join(WORK, script), path],
                       capture_output=True, text=True, encoding=u'utf-8', env=ENV, cwd=ROOT)
    return r.returncode, (r.stdout or u'') + (r.stderr or u'')


def w(name, text):
    p = os.path.join(WORK, name)
    io.open(p, 'w', encoding=u'utf-8').write(text)
    return p


def rep(tag, rc, out, need, want_rc=1):
    hit = [k for k in need if k in out]
    ok = rc == want_rc and len(hit) == len(need)
    print(u'%s %s｜rc=%d（須 %d）・點名 %s%s' % (
        u'✗' if not ok else u'✓', tag, rc, want_rc, hit,
        u'' if ok else u'｜未逮之鍵：%s' % [k for k in need if k not in hit]))
    return ok


res = []

# 甲：附錄四某行・左欄之卷改為語料不落之卷
mA = re.search(u'^\\| \\*\\*〔案例 07〕[^\\n]*', TXT, re.M)
row = mA.group(0)
lnA = TXT[:mA.start()].count(chr(10)) + 1
newA = row.replace(u'卷五十六', u'卷九')
assert newA != row, u'甲・錨不中：%s' % row[:40]
pA = w(u'neg278a.md', TXT.replace(row, newA, 1))
rc, out = run(u'v39volchk.py', pA)
res.append(rep(u'甲｜植假卷於表行', rc, out, [u'L%d' % lnA, u'引卷9']))

# 乙：『「文」（卷X至Y）』式・卷在引號之右
mB = re.search(u'^\\*   \\*\\*離處\\*\\*[^\\n]*', TXT, re.M)
lineB = mB.group(0)
lnB = TXT[:mB.start()].count(chr(10)) + 1
newB = lineB.replace(u'（卷二十二至三十）', u'（卷五十二至五十三）')
assert newB != lineB, u'乙・錨不中：%s' % lineB[:40]
pB = w(u'neg278b.md', TXT.replace(lineB, newB, 1))
rc, out = run(u'v39volchk.py', pB)
res.append(rep(u'乙｜右屬之卷須正歸', rc, out, [u'L%d' % lnB, u'52']))

# 丙：名冊之數
mC = re.search(u'^#{5} 9\\.[^\\n]*共 (\\d+) 案[^\\n]*', TXT, re.M)
lineC = mC.group(0)
newC = lineC.replace(u'共 %s 案' % mC.group(1), u'共 %d 案' % (int(mC.group(1)) - 1))
pC = w(u'neg278c.md', TXT.replace(lineC, newC, 1))
rc, out = run(u'v39ladder.py', pC)
res.append(rep(u'丙｜名冊自報之數', rc, out, [u'不合 1 枝', u'非染污端']))

# 戊：一案兩說（同案之兩載體引卷異檔）——只改第六章矩陣行；其行內無 「」，故不觸第二路，病專歸第三路
mE = re.search(u'^\\| \\*\\*〔案例 66〕[^\\n]*', TXT, re.M)
rowE = mE.group(0)
newE = rowE.replace(u'卷十九至二十一', u'卷五十八至五十九')
assert newE != rowE, u'戊・錨不中：%s' % rowE[:40]
pE = w(u'neg278e.md', TXT.replace(rowE, newE, 1))
rc, out = run(u'v39volchk.py', pE)
res.append(rep(u'戊｜同案兩載體異檔', rc, out, [u'一案兩說 1', u'案66']))

# 丁：還原
pD = w(u'neg278d.md', TXT)
for script, tag in ((u'v39volchk.py', u'丁｜核卷還原'), (u'v39ladder.py', u'丁｜名冊還原')):
    rc, out = run(script, pD)
    res.append(rep(tag, rc, out, [u'不合 0'], want_rc=0))

for p in (pA, pB, pC, pD, pE):
    os.remove(p)
print(u'———— 278 負測：%d/%d 道中' % (sum(1 for x in res if x), len(res)))
sys.exit(0 if all(res) else 1)
