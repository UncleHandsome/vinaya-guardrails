# -*- coding: utf-8 -*-
"""r197card.py —— 判例卡片之四欄完備與欄序（第 197 輪立・第 37 軸・待診・恆退 0）。

緣起：第六章百則判例每則以四枚 H5 分欄（事相經過／心相照鏡／佛陀處斷／人間智慧），
此乃全書之骨架——`rows2` 校其行制、`caseref` 校其案名與編號相副、`claimnum` 校宣稱之數，
**而『某一則之四欄有缺、或欄序倒置重出』向無器**：歷輪削文與改卡片（如 119 輪降格式、
134 輪移大賊表、155–159 梳理期）皆以『則』為單位動手，一旦削掉半欄，讀者只得事相而失處斷。

口徑：① 卡片＝印面 H4『#### 〔遮N〕／〔開N〕／〔僧N〕』（補遺與〔遺〕另桶）；
      ② 四欄＝其下 H5 以『事相／心相／佛陀處斷／人間智慧』起首者，須**俱備、唯一、依序**；
      ③ 主卡片之總數須為 100（書中自稱『全書百則判例』，此數由器自算，不抄台帳）。
桶：甲·四欄有缺（本軸之的）｜乙·欄序倒置或重出｜丙·主卡片總數非 100｜丁·補遺式卡片（另有其式，報而不治）。
退出碼：**恆 0**（待診——卡片之欄名或有異形，升閘須先證其零假陽性；今丁桶已見另一式）。
用法：`PYTHONPATH=. PYTHONIOENCODING=utf-8 python -X utf8 _work/r197card.py [副本] [require-hit]`；
      副本自算底冊界（184 輪之戒）。清冊落 `_work/r197list.txt`。
"""
import io, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as t

COP = sys.argv[1] if len(sys.argv) > 1 else None
REQ = u'require-hit' in sys.argv

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

MAIN = re.compile(u'^#### *(?:\\*\\*)?〔([遮開僧]{1,2})[0-9]+〕')
SUP = re.compile(u'^#### *(?:\\*\\*)?〔補遺[0-9]+〕')
COLS = (u'事相經過', u'心相照鏡', u'佛陀處斷', u'人間智慧')
ANYCOL = re.compile(u'^##### *(事相|心相|佛陀處斷|人間智慧|處斷|智慧)')

cards = []
for i, l in enumerate(L):
    if i in BOT:
        continue
    s = l.strip()
    if MAIN.match(s):
        cards.append((i, s[:30], u'主'))
    elif SUP.match(s):
        cards.append((i, s[:30], u'補'))

rows = {u'甲': [], u'乙': [], u'丙': [], u'丁': []}
main_n = 0
for n, (i, title, kind) in enumerate(cards):
    end = cards[n + 1][0] if n + 1 < len(cards) else len(L)
    seq = []
    for k in range(i + 1, end):
        m = ANYCOL.match(L[k].strip())
        if m:
            seq.append(m.group(1))
    if kind == u'補':
        rows[u'丁'].append((i + 1, title, u'、'.join(seq) or u'（無四欄式子題）'))
        continue
    main_n += 1
    have = []
    for w in COLS:
        hit = [c for c in seq if c and w.startswith(c)]
        if not hit:
            rows[u'甲'].append((i + 1, title, u'缺『%s』｜實有：%s' % (w, u'、'.join(seq) or u'無')))
        else:
            have.append(seq.index(hit[0]))
    if len(seq) != len(set(seq)) or (have and have != sorted(have)):
        rows[u'乙'].append((i + 1, title, u'欄序=%s' % u'、'.join(seq)))

if main_n != 100:
    rows[u'丙'].append((0, u'主卡片總數', u'%d（書中自稱百則）' % main_n))

print(u'判例卡片：主 %d 則・補遺 %d 則｜甲·四欄有缺 %d｜乙·欄序倒置或重出 %d｜'
      u'丙·主卡片非百則 %d｜丁·補遺式（報而不治）%d'
      % (main_n, len(rows[u'丁']), len(rows[u'甲']), len(rows[u'乙']), len(rows[u'丙']), len(rows[u'丁'])))
for k in (u'甲', u'乙', u'丙'):
    for ln, title, why in rows[k]:
        print(u'  %s L%-6d %s ⟵ %s' % (k, ln, title, why))
with io.open(u'_work/r197list.txt', 'w', encoding=u'utf-8', newline=u'\n') as f:
    for k in (u'甲', u'乙', u'丙', u'丁'):
        f.write(u'═══ %s：%d ═══\n' % (k, len(rows[k])))
        for ln, title, why in rows[k]:
            f.write(u'%s\tL%d\t%s\t%s\n' % (k, ln, title, why))
print(u'清冊：_work/r197list.txt（%d 則）' % sum(len(v) for v in rows.values()))
if COP and REQ:
    sys.exit(0 if (rows[u'甲'] or rows[u'乙'] or rows[u'丙']) else 1)
sys.exit(0)
