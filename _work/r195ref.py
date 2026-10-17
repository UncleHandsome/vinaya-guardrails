# -*- coding: utf-8 -*-
"""r195ref.py —— 章節款級指針須有所至（第 195 輪立・第 196 輪擴至款級・待診・恆退 0）。

緣起：`termref`（149 輪）校『指向附錄D-2／D-3 之詞條名須實有其條』、`anchorref`（136／145 輪）校
『版面承接語（上表／見下）須有所承』；**而『見第N章第M節第K款』一類層級指針，其落點是否實有，全書無器**。
140 輪曾以手治一筆假回指（第四章第五節第一款之〔◈跨章精準導流〕）——正是款級，此後歷五十輪未再掃。
此類病之害在**讀者按圖索驥而撲空，且撲空無跡**。

口徑：① **結構層須当场量產物，不可假設**——本書**章乃 H1『# 第N章』、節乃 H3『### 第N節』、
      款乃 H4『#### N、』（H2 全書不用；195 輪初版誤按 H2 建章表，遂 59 筆盡報假陽性）**；
      卷首／結語／附錄X 亦 H1，遇之即斷章。逐行另建『該行所屬章／節』之上下文，以供『本章／本節』之指針解析。
   ② 取印面散文行內『詳見／具見／說見／並見／參照／參見／見／詳／如／依／準』＋
      『第N章』〔＋『第M節』〕〔＋『第K款』〕，亦收『本章／本節／前節』起首之款級指針。
   ③ 判：章不存在→甲；章在而全不用節序（第六章以 壹／貳／參 分部）→丙（待考不判）；
      章用節序而其數逾實有→乙；節在而該節全無 H4『N、』款題→戊（待考不判）；
      節用款序而其數逾實有→丁。
底冊（附錄C／K／L／M／終卷）不較；圍欄・表列・標題行不較（表內指針另有 `termref` 之詞條級校）。
退出碼：**恆 0**（待診——指針措辭千變，升閘必以常式為病，151 輪之戒）。
用法：`PYTHONPATH=. PYTHONIOENCODING=utf-8 python -X utf8 _work/r195ref.py [副本] [require-hit]`；
      副本自算底冊界（184 輪之戒）。清冊落 `_work/r195list.txt`。
"""
import io, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as t

COP = sys.argv[1] if len(sys.argv) > 1 else None
REQ = u'require-hit' in sys.argv

CN = {}
for _i, _s in enumerate(u'一 二 三 四 五 六 七 八 九 十 十一 十二 十三 十四 十五 十六 十七 十八 十九 二十 廿一 廿二 廿三 廿四 廿五'.split(), 1):
    CN[_s] = _i
for _i, _s in enumerate(u'廿一 廿二 廿三 廿四 廿五'.split(), 21):
    CN[_s] = _i


def num(s):
    return CN.get(s, -1)


if COP:
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(ROOT)
    L = io.open(COP, encoding=u'utf-8').read().split(u'\n')
    BOT, inb = set(), False
    for i, l in enumerate(L):
        if l.startswith(u'# '):
            inb = any(k in l for k in t.BOTTOM_NAMES)
        if inb:
            BOT.add(i)
else:
    L = t.LINES
    BOT = t.bottom_lines()

# ──  建表：章→節→款，並記每行之上下文 ─────────────────────────
chap_sec = {}                                    # 章 -> {節}
sec_kuan = {}                                    # (章,節) -> {款}
ctx = {}                                         # 行 -> (章,節)
cur_c = cur_s = None
for i, l in enumerate(L):
    if i in BOT:
        continue
    m = re.match(u'^# 第([一二三四五六七八九十]+)章', l)
    if m:
        cur_c, cur_s = num(m.group(1)), None
        chap_sec.setdefault(cur_c, set())
        continue
    if re.match(u'^# ', l):
        cur_c = cur_s = None
        continue
    m = re.match(u'^### 第([一二三四五六七八九十]+)節', l)
    if m and cur_c is not None:
        cur_s = num(m.group(1))
        chap_sec[cur_c].add(cur_s)
        sec_kuan.setdefault((cur_c, cur_s), set())
        continue
    m = re.match(u'^#### *([一二三四五六七八九十]+)(?:至([一二三四五六七八九十]+))?、', l)
    if m and cur_c is not None and cur_s is not None:
        a = num(m.group(1))
        b = num(m.group(2)) if m.group(2) else a
        # 複合款題（『#### 十至十三、出院儀軌四重奏』）一題而統數款——初版只取首號，
        # 遂使第五章第七節看似自第九款直跳第十四款（款 10–13 全『不存在』），假陽性由此而生。
        for x in range(a, (b if b >= a else a) + 1):
            sec_kuan[(cur_c, cur_s)].add(x)
    ctx[i] = (cur_c, cur_s)

# ── ② 指針 ─────────────────────────────────────────────────
CN_ = u'[一二三四五六七八九十兩]+'
PTR = re.compile(u'(詳見|具見|說見|並見|參照|參見|見|詳|如|依|準)[^。；）]{0,12}?'
                 u'(?:第(' + CN_ + u')章)?'
                 u'(?:[^。；）章]{0,10}?(?:第|本|前|該)(' + CN_ + u')節)?'
                 u'(?:[^。；）節]{0,10}?(?:第|本|前|該)(' + CN_ + u')款)?')
rows = {u'甲': [], u'乙': [], u'丙': [], u'丁': [], u'戊': []}
NPTR = [0, 0, 0]                                 # 指針總數／帶節／帶款
fence, inf = [False] * len(L), False
for i, l in enumerate(L):
    if l.strip().startswith(u'```'):
        inf = not inf
        fence[i] = True
        continue
    fence[i] = inf

for i, line in enumerate(L):
    if i in BOT or fence[i]:
        continue
    s = line.strip()
    if not s or s.startswith((u'>', u'|', u'#')):
        continue
    for m in PTR.finditer(line):
        c = num(m.group(2)) if m.group(2) else None
        se = num(m.group(3)) if m.group(3) else None
        k = num(m.group(4)) if m.group(4) else None
        if c is None and se is None and k is None:
            continue
        # 『本章／本節／前節』之屬：從該行之上下文補章節
        mc, ms = ctx.get(i, (None, None))
        if c is None and re.search(u'第(' + CN_ + u')章', m.group(0)):
            c = num(re.search(u'第(' + CN_ + u')章', m.group(0)).group(1))
        if se is None and re.search(u'(本章|本節|前節|該節)', m.group(0)) and k is not None:
            se = ms
        if c is None and se is not None and k is None:
            c = mc
        if c is None:
            c = mc
        if se is None and k is not None:
            se = ms
        NPTR[0] += 1
        NPTR[1] += 1 if se is not None else 0
        NPTR[2] += 1 if k is not None else 0
        txt = m.group(0)[-40:]
        if c is not None and c not in chap_sec:
            rows[u'甲'].append((i + 1, txt, u'章不存在'))
            continue
        if se is not None and c is not None:
            if not chap_sec[c]:
                rows[u'丙'].append((i + 1, txt, u'第%d章全無節序' % c))
                continue
            if se not in chap_sec[c]:
                rows[u'乙'].append((i + 1, txt, u'第%d章實有節：%s' % (
                    c, u'、'.join(str(x) for x in sorted(chap_sec[c])))))
                continue
        if k is not None and c is not None and se is not None:
            ks = sec_kuan.get((c, se), set())
            if not ks:
                rows[u'戊'].append((i + 1, txt, u'第%d章第%d節無 H4 款題' % (c, se)))
            elif k not in ks:
                rows[u'丁'].append((i + 1, txt, u'實有款：%s' % u'、'.join(
                    str(x) for x in sorted(ks))))

print(u'層級指針 %d 處（帶節 %d・帶款 %d）對照建表（章 %d・節 %d・款 %d）：'
      u'甲·章不存在 %d｜乙·節不存在 %d｜丙·該章不用節序 %d｜丁·款不存在 %d｜戊·該節不用款序 %d'
      % (NPTR[0], NPTR[1], NPTR[2], len(chap_sec), sum(len(v) for v in chap_sec.values()),
         sum(len(v) for v in sec_kuan.values()),
         len(rows[u'甲']), len(rows[u'乙']), len(rows[u'丙']), len(rows[u'丁']), len(rows[u'戊'])))
for k in (u'甲', u'乙', u'丙', u'丁', u'戊'):
    for ln, txt, why in rows[k]:
        print(u'  %s L%-6d %s ⟵ %s' % (k, ln, txt, why))
with io.open(u'_work/r195list.txt', 'w', encoding=u'utf-8', newline=u'\n') as f:
    for k in (u'甲', u'乙', u'丙', u'丁', u'戊'):
        f.write(u'═══ %s：%d ═══\n' % (k, len(rows[k])))
        for ln, txt, why in rows[k]:
            f.write(u'%s\tL%d\t%s\t%s\n' % (k, ln, txt, why))
print(u'清冊：_work/r195list.txt（%d 則）' % sum(len(v) for v in rows.values()))
if COP and REQ:
    sys.exit(0 if (rows[u'甲'] or rows[u'乙'] or rows[u'丁']) else 1)
sys.exit(0)
