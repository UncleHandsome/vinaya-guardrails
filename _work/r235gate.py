# -*- coding: utf-8 -*-
"""第 235 輪植病負測：新不變量『附錄F-3 與本表兩向相攝』須真能抓病（三路）＋陰性對照（原檔）。"""
import io
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER = os.path.join(ROOT, u'ver38四分律_起心動念心智分析框架_修正版.md')
NAME = u'附錄F-3 與本表兩向相攝'
src = io.open(MASTER, encoding='utf-8').read()
lines = src.split(u'\n')

i8 = next(i for i, l in enumerate(lines) if l.startswith(u'| 8 | F-2（性戒）行'))
f2 = next(i for i, l in enumerate(lines) if l.strip().startswith(u'| **性戒**'))
print(u'F-3 第 8 列 = L%d｜本表性戒行 = L%d' % (i8 + 1, f2 + 1))

CASES = [
    (u'甲·列無所指', lambda ls: ls.__setitem__(i8, ls[i8].replace(u'F-2（性戒）行', u'F-2（虛構名目）行'))),
    (u'乙·筆無所列', lambda ls: ls.pop(i8)),
    (u'丙·首欄改名', lambda ls: ls.__setitem__(f2, ls[f2].replace(u'| **性戒**', u'| **自性戒**'))),
]


def run(text, tag):
    tmp = os.path.join(ROOT, u'_work', u'_r235neg_%s.md' % tag)
    io.open(tmp, 'w', encoding='utf-8', newline=u'\n').write(text)
    env = dict(os.environ, PYTHONPATH=ROOT, PYTHONIOENCODING='utf-8',
               TKSRC=os.path.join(u'_work', u'_r235neg_%s.md' % tag))
    r = subprocess.run([sys.executable, u'-X', u'utf8', u'_tk.py', 'check'],
                       cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf-8')
    os.remove(tmp)
    out = r.stdout or u''
    hit = [l for l in out.split(u'\n') if NAME in l]
    fail = any(l.strip().startswith(u'✗') for l in hit)
    tot = next((l for l in out.split(u'\n') if u'不變量' in l), u'')
    return fail, tot, (hit[0].strip()[:120] if hit else u'（無此行）')


bad, tot, first = run(src, u'ctl')
print(u'陰性對照（原檔）：%s｜%s' % (u'✗ 原檔即退（器有瘡）' if bad else u'PASS ✓', tot))
ok = not bad
for nm, fn in CASES:
    ls = src.split(u'\n')
    fn(ls)
    fail, t2, detail = run(u'\n'.join(ls), u'c%d' % CASES.index((nm, fn)))
    print(u'%s：%s｜%s' % (nm, u'抓退 ✓' if fail else u'✗ 未抓（檢為假）', detail))
    ok = ok and fail
print(u'負測三路＋陰性：%s' % (u'俱合 ✓' if ok else u'有未合者 ✗'))
sys.exit(0 if ok else 1)
