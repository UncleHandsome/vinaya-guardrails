# -*- coding: utf-8 -*-
"""anchorref.py —— 承接指稱有所承（第 136 輪立為長駐軸；第 145 輪擴其詞彙與所承之類）。

緣起：歷輪『降格式』之改動（保款題而削其表）最易留下**空指**——文中云『細審上表』『見下表』
『上圖』而所指之表／圖已不在其前後。舊軸皆校章·節·款之指針，唯此類**版面承接語**無人一問。

第 145 輪之擴：舊僅掌四式（上表／細審上表／下表／上圖），而書中實有 下圖・上列・下列・見上・
見下・本表・此表・是表・此圖・如圖 諸式向無一器問之（『名單之外』之又一例）。今全納之，且
所承者不限於表——**列表項與圍欄圖框同得為承**。
口徑：窗口 24 行；『上…』須其前有其所指之類，『下…』須其後有，『本／此／是／如』者前後任一
有即可（或本行自居表列）。不校『前案』——其於本書慣作法律術語（既定之先例），非版面承接。
底冊四篇與終卷不入印本，其區以 `_tk.bottom_lines()` 取之（改名不致失守）。
退出碼：落空 > 0 即退 1；`argv[1]` 可注副本以供負測。
"""
import io, os, sys, re
W = 24
if len(sys.argv) > 1:
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, ROOT)
    import _tk as _t
    L = io.open(sys.argv[1], encoding='utf-8').read().split('\n')
    # 副本亦須免掃底冊：以本檔自掃 H1 篇界（副本與母檔行數或有差異，故不取 _tk 之索引）。
    _heads = [i for i, l in enumerate(L) if l.startswith(u'# ')] + [len(L)]
    BOT = set()
    for a, b in zip(_heads, _heads[1:]):
        if any(nm in L[a] for nm in _t.BOTTOM_NAMES):
            BOT.update(range(a, b))
else:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import _tk as t
    L = t.LINES
    BOT = t.bottom_lines()
TAB = re.compile(u'^\\s*\\|')
GFX = re.compile(u'[┌│─└┘├┤┬┴┼►◄▼▲═]')
FENCE = re.compile(u'^\\s*```')
LIST = re.compile(u'^\\s*(?:[-*•]|\\d+[.)、]|[一二三四五六七八九十]+、)\\s?')


def _tab(lo, hi):
    return any(TAB.match(L[j]) for j in range(max(0, lo), min(len(L), hi)))


def _gfx(lo, hi):
    return any(GFX.search(L[j]) or FENCE.match(L[j]) for j in range(max(0, lo), min(len(L), hi)))


def _listy(lo, hi):
    return any((LIST.match(L[j]) or TAB.match(L[j])) for j in range(max(0, lo), min(len(L), hi)))


# (詞, 方向, 所承之類)：方向 up=其前、down=其後、any=前後任一
RULES = [
    (u'上表', 'up', 'tab'), (u'細審上表', 'up', 'tab'), (u'前表', 'up', 'tab'),
    (u'上列', 'up', 'list'), (u'見上', 'up', 'list'),
    (u'下表', 'down', 'tab'), (u'下列', 'down', 'list'), (u'見下', 'down', 'list'),
    (u'上圖', 'up', 'gfx'), (u'下圖', 'down', 'gfx'),
    (u'本表', 'any', 'tab'), (u'此表', 'any', 'tab'),
    (u'此圖', 'any', 'gfx'), (u'如圖', 'any', 'gfx'),
]
# 『是表』不入列：書中兩處實為『是＋表面／表決』之偶合，非版面承接語（詞彙須為詞，不得以二字硬湊）。

# ── 第 150 輪之擴：承接語而緊附『』或《》其名者，須於其向實見其名 ──
#   緣起：印面有『下開《非訟事件法》第64條』『上開「不得以減額規避極刑」』一類**以名相指稱他處之條目**，
#   舊 RULES 只問表／圖／列表之存否，無從驗其所指之名果否見於其向（名亡則指空，讀者按名求之而無著）。
#   唯取「帶名者」為判——裸形之『後目』『前開』『前說』書中實為「後＋目連」「現前＋開庭」「推翻＋前說」
#   之偶合，硬校必生假陽性（『是表』之覆轍），故不帶名者一律不校。
W2 = 40
NAME = re.compile(u'(上開|下開|前開|後開|上項|下項|前項|後項|上目|下目|前目|後目|'
                  u'上款|下款|前款|後款|上一款|下一款|上節|下節|前一節|下一節)'
                  u'[^』》]{0,10}[『《]([^』》]{2,26})[』》]')
bad = []
for key, d, kind in RULES:
    fn = {'tab': _tab, 'gfx': _gfx, 'list': _listy}[kind]
    for i, line in enumerate(L):
        if i in BOT or key not in line:
            continue
        if d == 'up':
            ok = fn(i - W, i)
        elif d == 'down':
            ok = fn(i + 1, i + W + 1)
        else:
            ok = (TAB.match(line) is not None) or fn(i - W, i) or fn(i + 1, i + W + 1)
        if not ok:
            j = line.index(key)
            bad.append((i + 1, key, line[max(0, j - 26):j + 22]))
n2 = 0
for i, line in enumerate(L):
    if i in BOT:
        continue
    for m in NAME.finditer(line):
        n2 += 1
        nm, up = m.group(2), m.group(1)[0] in (u'上', u'前')
        flat = lambda s: re.sub(u'[\\s，、：；。（）\'』「《》]', u'', s)
        key = flat(nm)
        if up:
            hay = u''.join(L[max(0, i - W2):i]) + line[:m.start(2)]
        else:
            hay = line[m.end(2):] + u''.join(L[i + 1:min(len(L), i + W2 + 1)])
        if key not in flat(hay):
            bad.append((i + 1, m.group(1), u'所指之名『%s』於其向 %d 行內（除其自身之引述外）不見' % (nm[:18], W2)))
bad.sort()
print(u'承接指稱落空：%d 處（窗口 %d 行；詞彙 %d 式；帶名之承接語 %d 處，窗口 %d 行；不校『前案』之法律義）'
      % (len(bad), W, len(RULES), n2, W2))
for ln, key, ctx in bad:
    print(u'  L%-6d 【%s】…%s…' % (ln, key, ctx))
sys.exit(1 if bad else 0)
