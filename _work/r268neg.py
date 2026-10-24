# -*- coding: utf-8 -*-
"""268 輪・負測：第八尺 `v39secref.py` 之三道植病（各證一軸），外加正本對照。

判式（逐道四件）：退碼 1・『✗』明細行存・**該行須點名真正之靶**（不只要報錯）・stderr 空。
第四道以正本跑，須 rc=0・錯靶 0・未證如實報（未證不挡——以『未證』冒充病者，即是放過真病之反面）。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r268neg.py
"""
import io
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
SRC = os.path.join(ROOT, NAME)
TMP = os.path.join(ROOT, u'_work', u'_neg268.md')
TOOL = os.path.join(ROOT, u'_work', u'v39secref.py')

CASES = [                                    # (名, 錨, 植入, 須點名之真靶, 須現之判語)
    (u'植回 267 之幽靈（本節一字不著）',
     u'第三章閘門三（衰竭型止犯・先醫後議暫免其責）',
     u'第二章第四節（衰竭型止犯免責）', u'第三章・閘門三', u'錯靶'),
    (u'移靶至他章（同名節在他章者）',
     u'第八章第二節（反靈性煤氣燈操縱防護禁約）、第五章',
     u'第七章第二節（反靈性煤氣燈操縱防護禁約）、第五章', u'第八章・第二節', u'錯靶'),
    (u'造不可求之靶（第九節本無）',
     u'第五章第五節（權勢合意', u'第五章第九節（權勢合意', u'靶不可求', u'靶不可求'),
]


def run(path):
    r = subprocess.run([sys.executable, u'-X', u'utf8', TOOL, path],
                       capture_output=True, text=True, encoding=u'utf-8')
    out = (r.stdout or u'').split(u'\n')
    return (r.returncode, [x for x in out if u'✗' in x],
            (r.stderr or u'').strip(), [x for x in out if x.startswith(u'————')])


base = io.open(SRC, encoding=u'utf-8').read()
allok = True
for tag, old, new, want, verdict in CASES:
    assert base.count(old) == 1, u'%s：錨命中 %d（須恰 1）' % (tag, base.count(old))
    shutil.copyfile(SRC, TMP)
    try:
        txt = io.open(TMP, encoding=u'utf-8').read()          # 先讀入再寫（266 補之誡）
        p = txt.replace(old, new, 1)
        assert p.count(new) == 1 and p.count(old) == 0, u'%s：植入未生效' % tag
        io.open(TMP, 'w', encoding=u'utf-8', newline=u'\n').write(p)
        rc, det, err, tally = run(TMP)
        named = [x for x in det if want in x and verdict in x]
        ok = rc == 1 and named and not err
        allok = allok and ok
        print(u'%-30s rc=%d・明細=%d・點名=%d・stderr=%r ➔ %s'
              % (tag, rc, len(det), len(named), err[:36], u'逮' if ok else u'不逮'))
        for x in (named or det)[:1]:
            print(u'       ', x.strip()[:104])
    finally:
        if os.path.exists(TMP):
            os.remove(TMP)

rc, det, err, tally = run(SRC)
ok0 = rc == 0 and not det and not err
allok = allok and ok0
print(u'正本對照：rc=%d・✗=%d・stderr=%r｜%s' % (rc, len(det), err[:36], (tally[-1].strip()[:60] if tally else u'')))
print(u'———— 總判：%s（四道俱須如式；點名真靶者才算逮，只報錯而指錯家者仍是不逮）'
      % (u'全逮' if allok else u'有未逮'))
sys.exit(0 if allok else 1)
