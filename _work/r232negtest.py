# -*- coding: utf-8 -*-
# r232negtest　新閘 94（卡不空盒）之負測——**此閘已於第 233 輪撤廢**（修訂誌第 105 輪早駁『補行動卡三卡片框』，
#   卡三之兩行指針乃書中自制，非空盒之病），本器留檔為戒：跑之必報『今制 94/94 與 GATE 不在』，非器之壞。
#   教在『立閘之前必搜歷裁』（見 列印SOP.md 第 331 條與記憶 ⑯）。
import hashlib
import io
import os
import subprocess
import sys

NL = chr(10)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
MD = u'ver38四分律_起心動念心智分析框架_修正版.md'
NEW = u'_work/_r232plant.md'
GATE = u'行動卡之款必附圍欄實體卡框'
ALL = u'不變量 94/94 PASS'
HEAD3 = u'#### 三、行動卡三：禁語防護自律卡'
HEAD4 = u'#### 四、行動卡四：群組正命自律卡'
PROSE = u'（本卡之完整法理已立第九章第四節第五款，此處不重出。）'

BASE = io.open(MD, encoding=u'utf-8').read().split(NL)
H0 = hashlib.sha256(io.open(MD, encoding=u'utf-8').read().encode(u'utf-8')).hexdigest()
D = [i for i, s in enumerate(BASE) if s.startswith(u'**六、補記（記訖方犯')]
assert len(D) == 1, u'底冊之錨非恰一：%d' % len(D)


def hidx(lines, head):
    k = [i for i, s in enumerate(lines) if s.startswith(head)]
    assert len(k) == 1, u'款題非恰一：%s（%d）' % (head, len(k))
    return k[0]


def strip_card(head):
    a = list(BASE)
    h = hidx(a, head)
    f1 = [i for i in range(h + 1, len(a)) if a[i].startswith(u'```')][0]
    f2 = [i for i in range(f1 + 1, len(a)) if a[i].startswith(u'```')][0]
    out = a[:f1] + [PROSE] + a[f2 + 1:]
    return out, h + 1


def rename3():
    a = list(BASE)
    h = hidx(a, HEAD3)
    a[h] = u'#### 三、禁語防護自律卡（反靈性煤氣燈操縱防護令）'
    return a


def plant_bottom():
    a = list(BASE)
    a[D[0]] = (a[D[0]] + NL + u'#### 一、行動卡九：底冊自述之空款（非印面宣稱，須從寬）')
    return a


def run(lines, want_rc, wants, tag, clean=False):
    io.open(NEW, u'w', encoding=u'utf-8', newline=NL).write(NL.join(lines))
    env = dict(os.environ)
    env[u'TKSRC'] = os.path.abspath(NEW)
    env[u'PYTHONIOENCODING'] = u'utf-8'
    p = subprocess.Popen([sys.executable, u'-X', u'utf8', u'_tk.py', u'check'],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env, cwd=ROOT)
    out = p.communicate()[0].decode(u'utf-8', u'replace')
    rc = p.returncode
    bad = [l for l in out.split(NL) if l.strip().startswith(u'FAIL')]
    ok = rc == want_rc and all(w in out for w in wants)
    if clean:
        ok = ok and not bad and (ALL in out)
    else:
        ok = ok and len(bad) == 1 and GATE in bad[0]
    print(u'%-44s rc=%d（期 %d）%s%s' % (tag, rc, want_rc, u'中' if ok else u'不中',
                                         u'' if clean else u'｜FAIL %d 條' % len(bad)))
    if not ok:
        for l in (bad[:3] if bad else out.strip().split(NL)[-3:]):
            print(u'      · %s' % l[:130])
    return ok


p3, L3 = strip_card(HEAD3)
p4, L4 = strip_card(HEAD4)
cases = [run(BASE, 0, [GATE], u'⓪ 淨本（94/94 且全綠）', clean=True),
         run(p3, 1, [GATE, u'L%d' % L3], u'① 削卡三之圍欄（當報并中其款題行 %d）' % L3),
         run(p4, 1, [GATE, u'L%d' % L4], u'② 削卡四之圍欄（當報，證非只認一枚）%d' % L4),
         run(rename3(), 0, [GATE], u'③ 款題去『行動卡三：』形而留圍欄（陰性對照・勿報）', clean=True),
         run(plant_bottom(), 0, [GATE], u'④ 底冊植空款一枚（豁免側・勿報）', clean=True)]

if os.path.exists(NEW):
    os.remove(NEW)
H1 = hashlib.sha256(io.open(MD, encoding=u'utf-8').read().encode(u'utf-8')).hexdigest()
print(u'主檔哈希前後相同：%s｜副本已除：%s' % (u'是' if H0 == H1 else u'否（大害！）',
                                              u'是' if not os.path.exists(NEW) else u'否'))
ok = all(cases) and H0 == H1
print(u'負測：%s（五路俱中且主檔無染方過）' % (u'過' if ok else u'不過'))
sys.exit(0 if ok else 1)
