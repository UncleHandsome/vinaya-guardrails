# -*- coding: utf-8 -*-
"""r172negtest.py —— 第 172 輪負測：證本軸有牙，且歸零非消音。

  一 回植：於副本在第六章中後段（其前最近之表已隔兩節以上）植入一句『上表之科判，於此可覆。』
     → 乙隔頁必報（器有牙）。
  二 非消音（同頁之寬）：把『逾一頁半方判』改為『凡越節即判』再掃主檔 → 病數必起（今 6 筆）。
  三 非消音（切位之豁免）：去 PRE_BAD（『說見表下…』）與 NEXT_BAD（『該表決』『上列表』）再掃 → 必報。
用法：`PYTHONPATH=. python -X utf8 _work/r172negtest.py`
"""
import io, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
AXIS = os.path.join(ROOT, '_work', 'r172point.py')
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = [f for f in os.listdir(ROOT) if f.startswith('ver38') and f.endswith('.md')][0]
SRCP = os.path.join(ROOT, SRC)
COPY = os.path.join(HERE, 'r172neg.md')
TMP1 = os.path.join(HERE, '_ax_allcross.py')
TMP2 = os.path.join(HERE, '_ax_nocut.py')


def run(script, path):
    env = dict(os.environ)
    env['PYTHONPATH'] = ROOT
    env['PYTHONIOENCODING'] = 'utf-8'
    out = subprocess.run([sys.executable, '-X', 'utf8', script, path],
                         capture_output=True, text=True, encoding='utf-8', env=env)
    tail = [l for l in out.stdout.splitlines() if l.startswith(u'== 合計')]
    assert tail, (out.stdout[-400:] + out.stderr[-400:])
    return tail[0]


def n(line, tag):
    return int(re.search(u'%s (\\d+)' % tag, line).group(1))


s = io.open(SRCP, encoding='utf-8').read()
r0 = run(AXIS, SRCP)
print(u'〇 今制：%s' % r0)

# 一 回植：於**本軸視為印面**之散文行中，取其前最近之表已隔兩節以上、且字距逾一頁半者
lines = s.split('\n')
BOT = set()
for nm in __import__('_tk').BOTTOM_NAMES:
    k = next((i for i, l in enumerate(lines) if l.startswith(u'# ') and nm in l), None)
    if k is None:
        continue
    j = next((i for i in range(k + 1, len(lines)) if lines[i].startswith(u'# ')), len(lines))
    BOT.update(range(k, j))
FEN = [False] * len(lines)
_in = False
for i, l in enumerate(lines):
    if l.strip().startswith(u'```'):
        _in = not _in
        FEN[i] = True
        continue
    FEN[i] = _in
cand = None
_chs = [i for i, l in enumerate(lines) if l.startswith(u'# 第')]
START = _chs[2] if len(_chs) > 2 else 0          # 避開卷首（目錄區本軸免掃）
for i, l in enumerate(lines[START:], START):
    if i in BOT or FEN[i] or not l.strip():
        continue
    if l[0] in u'|#>':
        continue
    if re.match(u'^\\s*([-*]|\\d+[.)、]|[①-⓿])', l):
        continue
    tab = max((j for j in range(i) if lines[j].strip().startswith(u'|')), default=None)
    if tab is None or u'上表' in l or u'本表' in l:
        continue
    head_between = sum(1 for j in range(tab, i) if lines[j].startswith(u'#'))
    zi = sum(len(re.findall(u'[\\u4e00-\\u9fff]', lines[j])) for j in range(tab, i))
    if head_between >= 2 and zi > 2000:
        cand = i
        break
assert cand is not None, u'找不到可植病之位置'
lines[cand] = u'上表之科判於此可覆。' + lines[cand]
io.open(COPY, 'w', encoding='utf-8', newline='').write(u'\n'.join(lines))
r1 = run(AXIS, COPY)
print(u'一 回植『上表』（L%d，其前之表隔兩節以上）：%s' % (cand + 1, r1))
assert n(r1, u'乙') >= n(r0, u'乙') + 1, u'回植未報，器無牙'
print(u'   PASS：乙 +1')

ax = io.open(AXIS, encoding='utf-8').read()
# 二 撤『同頁不判』：凡越節即判（須同撤近界之攔與遠界之閾，否則 if/elif 仍各守其位）
io.open(TMP1, 'w', encoding='utf-8').write(
    ax.replace(u"if PAGE_ZI and z <= 1.5 * PAGE_ZI:", u"if False:")
      .replace(u"elif PAGE_ZI and z > 1.5 * PAGE_ZI:", u"elif PAGE_ZI:"))
r2 = run(TMP1, SRCP)
print(u'二 改『凡越節即判』：%s' % r2)
assert n(r2, u'乙') + n(r2, u'甲') > n(r0, u'乙') + n(r0, u'甲'), u'撤寬仍零'
print(u'   PASS：病數由 0 起至 %d（同頁回指乃正格，故判在逾頁而非越節）'
      % (n(r2, u'乙') + n(r2, u'甲')))

# 三 撤切位豁免
io.open(TMP2, 'w', encoding='utf-8').write(
    ax.replace(u"if s[p + len(w):p + len(w) + 1] in NEXT_BAD.get(form, set()):", u"if False:")
      .replace(u"if s[max(0, p - 1):p] in PRE_BAD.get(w, set()):", u"if False:"))
r3 = run(TMP2, SRCP)
print(u'三 撤切位豁免：%s' % r3)
assert n(r3, u'乙') + n(r3, u'甲') > 0, u'撤切位仍零——即為消音'
print(u'   PASS：切位一除即報 %d 筆（『該表決』『上列表』『說見表下』之類）'
      % (n(r3, u'乙') + n(r3, u'甲')))

for f in (TMP1, TMP2):
    os.remove(f)
print(u'\n三測俱 PASS。')
