# -*- coding: utf-8 -*-
"""第 236 輪植病負測：新不變量 95『附錄K 已回指之列須落點之內實見其指針』。
   甲·削一枚新指針 → 須退｜乙·指針改寫成範圍式 → 須不退（展開之功）｜
   丙·無指針之列翻作已回指 → 須退｜丁·原檔 → 須 95/95。"""
import io
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER = os.path.join(ROOT, u'ver38四分律_起心動念心智分析框架_修正版.md')
NAME = u'附錄K 已回指之列須落點之內實見其指針'
src = io.open(MASTER, encoding='utf-8').read()

CASES = [
    (u'甲·削指針', [(u'（庭上行使此碼之序次見第八章第二節第三款之道岔五）', u'')]),
    (u'乙·範圍式', [(u'即第八章第二節之公堂審計表', u'即第八章第一、二節之公堂審計表')]),
    (u'丙·虛翻牌', [(u'| 第四章第七節第二款 | 出堂洗心三事 | 第八章第五節第一款 | 未回指（存目待補） |',
                    u'| 第四章第七節第二款 | 出堂洗心三事 | 第八章第五節第一款 | 已回指 |')]),
]


def run(text, tag):
    tmp = os.path.join(ROOT, u'_work', u'_r236neg_%s.md' % tag)
    io.open(tmp, 'w', encoding='utf-8', newline=u'\n').write(text)
    env = dict(os.environ, PYTHONPATH=ROOT, PYTHONIOENCODING='utf-8',
               TKSRC=os.path.join(u'_work', u'_r236neg_%s.md' % tag))
    r = subprocess.run([sys.executable, u'-X', u'utf8', u'_tk.py', 'check'],
                       cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf-8')
    os.remove(tmp)
    # `_tk.py` 之 emit 只印末 2000 字，長帳須讀 _work/check.txt（stdout 裡根本看不見此檢）
    rep = io.open(os.path.join(ROOT, u'_work', 'check.txt'), encoding='utf-8').read().split(u'\n')
    line = next((l for l in rep if NAME[:9] in l), None)
    assert line, u'報內無此檢（器或崩）：%s' % tag
    tot = next((l for l in rep if l.startswith(u'不變量')), u'')
    return (line.strip().startswith(u'FAIL') or line.strip().startswith(u'✗')), tot.strip(), line.strip()[:104]


f0, tot0, l0 = run(src, u'ctl')
print(u'丁·陰性對照：%s｜%s' % (u'✗ 原檔即退（器有瘡）' if f0 else u'PASS ✓', tot0))
ok = not f0 and u'95/95' in tot0
for i, (nm, pairs) in enumerate(CASES):
    t2 = src
    for old, new in pairs:
        assert t2.count(old) == 1, u'%s 舊文命中 %d' % (nm, t2.count(old))
        t2 = t2.replace(old, new)
    fail, tot, line = run(t2, u'c%d' % i)
    want_fail = nm != u'乙·範圍式'
    verdict = (u'抓退 ✓' if fail else u'未退 ✓（範圍式已展開）') if want_fail == fail else u'✗ 判準不合'
    print(u'%s：%s｜%s' % (nm, verdict, line))
    ok = ok and (want_fail == fail)
print(u'負測：%s' % (u'四路俱合 ✓' if ok else u'有未合 ✗'))
sys.exit(0 if ok else 1)
