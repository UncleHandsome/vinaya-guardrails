# -*- coding: utf-8 -*-
# 第 219 輪・負測器（留檔）：不變量 89（引號內節引不作單枚『…』）與 90（標題不摻粗體）之五路
#   植病取『改前真形』——即本輪刀口所治之五處與標題一處，乃同級植病（非憑空造形）。
#   每路俱斷『中其目』：所報須為指名之閘，且病目之行號須含植字之行；別目代勞即判此路不合格。
#   ⓪ 現形（清淨）→ 89・90 俱綠
#   ① 「」內植單枚（L3081 改前形）→ 89 報該行；90 不報
#   ② 『』內植單枚（L11792 改前形）→ 89 報該行；90 不報
#   ③ 標題重摻粗體（L2240 改前形）→ 90 報該行；89 不報
#   ④ 豁免側（「」內只含〔…〕佔位式）→ 89・90 俱不報（陰性對照，證牙不誤傷）
#   用法：PYTHONPATH=. python -X utf8 _work/r219negtest.py
import hashlib
import io
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, u'ver38四分律_起心動念心智分析框架_修正版.md')
WORK = os.path.join(ROOT, u'_r219work.md')
G89 = u'印面引號內之節引不作單枚『…』'
G90 = u'印面標題行內不摻粗體記號'

BASE = io.open(MD, encoding=u'utf-8').read()
H0 = hashlib.sha256(BASE.encode(u'utf-8')).hexdigest()
L = BASE.split(u'\n')


def plant(ln, old, new):
    t = BASE.split(u'\n')
    assert t[ln - 1].count(old) == 1, u'植病錨點非恰一 L%d' % ln
    t[ln - 1] = t[ln - 1].replace(old, new)
    return u'\n'.join(t)


CASES = [
    (u'⓪ 現形（須俱綠）', None),
    (u'① 「」內單枚（須 89 報 L3081）',
     (3081, u'一曰「有五法名為大賊……何等五」（住無定處', u'一曰「有五法名為大賊…何等五」（住無定處',
      G89, u'L3081')),
    (u'② 『』內單枚（須 89 報 L11792）',
     (11792, u'有生滅心轉……』', u'有生滅心轉…』', G89, u'L11792')),
    (u'③ 標題摻粗（須 90 報 L2240）',
     (2240, u'##### 現相施壓與靈性勒索（以願景為高壓）',
      u'##### **現相施壓與靈性勒索（以願景為高壓）**', G90, u'L2240')),
    (u'④ 佔位式豁免（須俱不報）',
     (3081, u'一曰「有五法名為大賊……何等五」（住無定處',
      u'一曰「示例〔…〕之形」（住無定處', None, None)),
]


def gates(txt):
    io.open(WORK, u'w', encoding=u'utf-8', newline=u'\n').write(txt)
    env = dict(os.environ)
    env[u'TKSRC'] = WORK
    env[u'PYTHONPATH'] = ROOT
    p = subprocess.Popen([sys.executable, u'-X', u'utf8', os.path.join(ROOT, u'_tk.py'), u'check'],
                         cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.communicate()[0].decode(u'utf-8', u'replace')
    rows = {}
    for line in out.split(u'\n'):
        if line.startswith((u'PASS', u'FAIL')):
            st, _, title = line.partition(u' ')
            rows[title[:26]] = (st, line)
    return p.returncode, rows, out


ok = True
for name, spec in CASES:
    if spec is None:
        txt, want, wantln = BASE, None, None
    else:
        ln, old, new = spec[0], spec[1], spec[2]
        txt = plant(ln, old, new)
        want, wantln = spec[3], spec[4]
    rc, rows, out = gates(txt)
    hit89 = [v for k, v in rows.items() if k.startswith(G89[:20])]
    hit90 = [v for k, v in rows.items() if k.startswith(G90[:20])]
    st89, ln89 = hit89[0] if hit89 else (u'?', u'')
    st90, ln90 = hit90[0] if hit90 else (u'?', u'')
    if want is None:
        good = (st89 == u'PASS' and st90 == u'PASS')
        print(u'%-34s｜89 %s｜90 %s｜%s' % (name, st89, st90, u'中' if good else u'不中'))
    else:
        mine = (st89, ln89) if want == G89 else (st90, ln90)
        other = (st90, ln90) if want == G89 else (st89, ln89)
        good = (mine[0] == u'FAIL' and wantln in mine[1] and other[0] == u'PASS' and rc != 0)
        print(u'%-34s｜本目 %s（點名 %s：%s）｜對側 %s｜退出碼 %d｜%s'
              % (name, mine[0], wantln, wantln in mine[1], other[0], rc, u'中' if good else u'不中'))
    ok = ok and good

if os.path.exists(WORK):
    os.remove(WORK)
H1 = hashlib.sha256(io.open(MD, u'rb').read()).hexdigest()
print(u'哈希自證｜主檔 %s…｜%s' % (H1[:12], u'未損' if H1 == H0 else u'已損！'))
assert H1 == H0, u'主檔被動！'
print(u'結論｜五路%s' % (u'俱中' if ok else u'有不中——尺或口徑須復'))
sys.exit(0 if ok else 1)
