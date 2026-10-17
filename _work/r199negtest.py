# -*- coding: utf-8 -*-
"""r199negtest.py —— 第 41 軸 `r199ellipsis.py` 之負測（四植證其擴到・三植證其不誤傷）。

『凡擴級之閘，必以同級植病證其擴到』（189 輪之誡）。本軸之擴級有兩：**層別**（戊A 唯較印面散文，
本軸散文・引塊・表列・標題四層俱較）與**字級**（不再要求律文形貌，唯取『片段俱可查得』者）。
故陽性四植分落四個層別——**若只植散文，層別之擴等於未證**。
陰性三植俱取『形似而實合法』者：已標刪節號・全串連續可查得・片段亦查無（那是冒充族，归 185 之甲）——
證本軸不越界、不誤傷。植字一律**附於行尾**（同位插句會撞進既有引號之巢，成植字不淨）。
"""
import io, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
MASTER = u'ver38四分律_起心動念心智分析框架_修正版.md'
COP = u'_work/_r199cop.md'
BASE = io.open(MASTER, encoding=u'utf-8').read()
PAT = re.compile(u'甲·節引未標（本軸之的）(\\d+)')


def save(lines):
    io.open(COP, 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(lines))


def put(n, old, new):
    ls = BASE.split(u'\n')
    assert ls[n - 1].count(old) == 1, u'錨點非恰一：L%d %r' % (n, old)
    ls[n - 1] = ls[n - 1].replace(old, new)
    save(ls)


def tail(n, s):
    ls = BASE.split(u'\n')
    ls[n - 1] = ls[n - 1].rstrip() + s
    save(ls)


def run(req):
    cmd = [sys.executable, u'-X', u'utf8', u'_work/r199ellipsis.py', COP]
    if req:
        cmd.append(u'require-hit')
    env = dict(os.environ, PYTHONPATH=u'.', PYTHONIOENCODING=u'utf-8')
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    out = p.communicate()[0].decode(u'utf-8', u'replace')
    m = PAT.search(out)
    return (int(m.group(1)) if m else -1), p.returncode


STITCH = u'「難調者令調順、慚愧者得安樂」'          # 兩句俱查得而不相鄰（中隔篇次之『七』）
MARKED = u'「難調者令調順……慚愧者得安樂」'          # 如法：已標節引
WHOLE = u'「若有舉我者，我當多與物」'                # 如法：全串連續可查得
ORPHAN = u'「最初未制戒不為罪」'                     # 非本軸：片段亦查無（冒充族，归 185）

CASES = [
    (u'陽·散文（L610 削其刪節號）', 1, 1, lambda: put(610, u'斷現在有漏……斷未來有漏', u'斷現在有漏、斷未來有漏')),
    (u'陽·引塊（L406 行尾拼接）',   1, 1, lambda: tail(406, STITCH)),
    (u'陽·表列（L3091 行尾拼接）',  1, 1, lambda: tail(3091, STITCH)),
    (u'陽·標題（L543 題尾拼接）',   1, 1, lambda: tail(543, STITCH)),
    (u'陰·已標節引者不較（L406）',  0, 0, lambda: tail(406, MARKED)),
    (u'陰·全串查得者不較（L3091）', 0, 0, lambda: tail(3091, WHOLE)),
    (u'陰·片段查無者不較（L543）',  0, 0, lambda: tail(543, ORPHAN)),
]

bad = []
for name, req, want, act in CASES:
    act()
    n, rc = run(bool(req))
    ok = (n == want and rc == 0) if req else (n == 0 and rc == 0)
    print(u'%-28s require-hit=%d 甲=%-3d rc=%d ⇒ %s' % (name, req, n, rc, u'中' if ok else u'✗不中'))
    if not ok:
        bad.append(name)

os.remove(COP)
print(u'負測：%d 路，不中 %d。' % (len(CASES), len(bad)))
sys.exit(1 if bad else 0)
