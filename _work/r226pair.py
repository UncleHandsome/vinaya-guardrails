# -*- coding: utf-8 -*-
# r226pair　十一組二法之對位閉環（第 226 輪立，長駐・專軸）
#
#   所以立之：第二章第一節第二款列佛陀親宣之十一組二法，第二節五處〔原生二法對位〕逐款回報
#   其所統攝之組次，第三節末又以此十一組轉譯為「即時警報清單」。三處皆以「第N組＋組名」為字面之鍵，
#   歷二百餘輪無一器校其：① 組序與組名是否相符（錯序即錯引），② 每組有幾款认领（一組兩款全認即重報），
#   ③ 「分」之兩翼是否俱有主（一翼無主則閉環有缺），④ 「底層病根／枝葉面具」之雙層是否覆蓋全數二十二法。
#   第 226 輪外路報「第二節第五款之對位誤植」，親量所獲比報來者更重：第七組兩款俱認而第四款不標其分，
#   第八組唯貪分有主而恚分無歸，雙層清單遺七法而不為覆——皆非改一字可了，故立器守之。
#
#   口徑：法源＝第一款引文之bold 序列（十一組、二十二法，序數隨引文而移，不由本器假設）；
#   對位宣稱取印面凡「第N組」者（含「之X分」式）；警報清單取「七、日常煩惱」款表內「A ╳ B」格。
#   從寬：名之以「分」者容前綴（嫉 對 嫉妬）；他章若引組名而無組序者不校。
#   源檔隨 `_tk.SRC`（故 TKSRC 之植病副本可測）。
#   用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r226pair.py
from __future__ import unicode_literals
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as T

LINES = T.LINES
# 底冊（修訂誌・校勘記）不校：記錄必轉述組名與舊形，轉述非宣稱（218 輪『編年不回改』之裁；
#   第 226 輪自蹈——校勘記一句「第七組兩款全認而不標其分」遂被本軸讀成『組序空宣』）。
BOT = T.bottom_lines()
NL = chr(10)
CN = {u'一': 1, u'二': 2, u'三': 3, u'四': 4, u'五': 5, u'六': 6,
      u'七': 7, u'八': 8, u'九': 9, u'十': 10, u'十一': 11}
BOLD = re.compile(r'\*\*(.+?)\*\*')
PAIRREF = re.compile(u'第(十一|[一二三四五六七八九])組')
X = u' ╳ '

bad = []

# 一、法源：第一款引文之二十二法，兩兩成組
i0 = [i for i, l in enumerate(LINES) if l.startswith(u'#### 二、律典原生的煩惱清單')]
i1 = [i for i, l in enumerate(LINES) if l.strip().startswith(u'##### 律典原生')]
assert len(i0) == 1 and len(i1) == 1 and i1[0] > i0[0], u'第一款之篇界非恰一：%s %s' % (i0, i1)
names = []
for i in range(i0[0], i1[0]):
    if not LINES[i].lstrip().startswith(u'>'):
        continue
    for b in BOLD.findall(LINES[i]):
        names.append(b.strip())
GROUPS = [(names[k], names[k + 1]) for k in range(0, len(names) - 1, 2)]
if len(names) % 2 or len(GROUPS) != 11:
    bad.append((u'法源', i0[0] + 1, u'引文所得 %d 法，非十一組二十二法' % len(names)))


def same(a, b):
    return a == b or a.startswith(b) or b.startswith(a)


def in_group(part, g):
    return [k for k, m in enumerate(GROUPS[g]) if same(part, m)]


# 二、對位宣稱（印面凡「第N組」者）
claims = {}          # 組序 -> [(行號, 型別, 覆蓋之翼 index 集合)]
table_rows = []      # 警報清單內之「A ╳ B」對
for i, l in enumerate(LINES):
    if i in BOT or u'第' not in l:
        continue
    for m in PAIRREF.finditer(l):
        g = CN[m.group(1)] - 1
        tail = l[m.end():m.end() + 60]
        p = re.match(u'「(.+?)%s(.+?)」' % X, tail)
        if p:
            a, b = p.group(1).strip(), p.group(2).strip()
            if g >= len(GROUPS) or {a, b} != set(GROUPS[g]):
                bad.append((u'組序與組名不符', i + 1,
                            u'宣「第%s組『%s%s%s』」而法源第%s組乃『%s%s%s』'
                            % (m.group(1), a, X, b, m.group(1), GROUPS[g][0], X, GROUPS[g][1])))
                continue
            after = tail[p.end():]
            f = re.match(u'（(.{1,6}?)分）', after) or re.match(u'中「(.{1,6}?)」之一分', after)
            if f:
                part = f.group(1).strip()
                w = in_group(part, g)
                if not w:
                    bad.append((u'分無所屬', i + 1, u'第%s組標『%s』而二翼俱不相應' % (m.group(1), part)))
                    continue
                claims.setdefault(g, []).append((i + 1, u'分', set(w)))
            else:
                claims.setdefault(g, []).append((i + 1, u'全', set([0, 1])))
            continue
        q = re.match(u'之(.{1,6}?)分', tail)
        if q:
            part = q.group(1).strip()
            w = in_group(part, g)
            if not w:
                bad.append((u'分無所屬', i + 1, u'第%s組之『%s』而二翼俱不相應' % (m.group(1), part)))
                continue
            claims.setdefault(g, []).append((i + 1, u'分', set(w)))
            continue
        bad.append((u'組序空宣', i + 1, u'稱『第%s組』而後無組名亦無分' % m.group(1)))

# 三、警報清單（第三節末之表）：其「A ╳ B」格為未列對位者之歸所
j0 = [i for i, l in enumerate(LINES) if l.startswith(u'#### 七、日常煩惱')]
assert len(j0) == 1, u'警報清單之款界非恰一'
for i in range(j0[0], min(j0[0] + 30, len(LINES))):
    for p in re.findall(r'「(.+?)%s(.+?)」' % X, LINES[i]):
        table_rows.append(set(p))
for i in range(j0[0], min(j0[0] + 30, len(LINES))):
    for p in re.findall(r'([^\s|｜、（]*?)%s([^\s|｜、（<]*)' % X, LINES[i]):
        table_rows.append(set(p))


def in_table(g):
    return any(set(GROUPS[g]) <= t or all(any(same(x, y) for y in t) for x in GROUPS[g])
               for t in table_rows)


for g in range(11):
    cl = claims.get(g, [])
    if not cl:
        if not in_table(g):
            bad.append((u'無歸', 0, u'第%s組（%s）既無對位款，亦不見於警報清單'
                        % (g + 1, u'%s%s%s' % (GROUPS[g][0], X, GROUPS[g][1]))))
        continue
    whole = [c for c in cl if c[1] == u'全']
    if whole and len(cl) > 1:
        bad.append((u'重報', cl[0][0], u'第%s組既有全認（L%s），又別有认领 L%s'
                    % (g + 1, whole[0][0], u'、'.join(str(c[0]) for c in cl if c is not whole[0]))))
        continue
    if whole:
        continue
    got = set()
    for _, _, w in cl:
        got |= w
    if got != set([0, 1]):
        miss = [GROUPS[g][k] for k in (set([0, 1]) - got)]
        bad.append((u'分未齊', cl[0][0], u'第%s組唯逐分认领，一翼無主：%s' % (g + 1, u'、'.join(miss))))

# 四、雙層動力學是否覆蓋全數二十二法
d0 = [i for i, l in enumerate(LINES) if u'底層病根' in l and l.startswith(u'* **')]
d1 = [i for i, l in enumerate(LINES) if u'枝葉面具' in l and l.startswith(u'* **')]
assert len(d0) == 1 and len(d1) == 1, u'雙層清單之行数非恰一：%s %s' % (d0, d1)


def layer_members(l):
    body = l.split(u'：', 1)[1].split(u'——')[0]
    out = []
    for tok in body.split(u'、'):
        t = re.sub(u'（.*?）', u'', tok).strip()
        if t:
            out.append(t)
    return out


flat = []
for idx, ln in ((0, d0[0]), (1, d1[0])):
    for t in layer_members(LINES[ln]):
        hits = [(g, k) for g in range(min(len(GROUPS), 11)) for k in (0, 1)
                if g < len(GROUPS) and same(t, GROUPS[g][k])]
        if not hits:
            bad.append((u'雙層有名而无法源對應', ln + 1, u'『%s』不在十一組二十二法之內' % t))
        else:
            flat.append((t, hits[0]))
for g in range(min(len(GROUPS), 11)):
    for k in (0, 1):
        if not [1 for _, (gg, kk) in flat if (gg, kk) == (g, k)]:
            bad.append((u'雙層有遺法', d0[0] + 1, u'法源第%s組之『%s』不屬底層亦不屬枝葉' % (g + 1, GROUPS[g][k])))

print(u'法源 %d 組 %d 法｜對位宣稱 %d 款次（覆 %d 組）｜警報清單 %d 格對｜雙層列 %d 名｜病 %d 處%s'
      % (len(GROUPS), len(names), sum(len(v) for v in claims.values()), len(claims),
         len(table_rows), len(flat), len(bad), u' []' if not bad else u''))
for kind, ln, info in bad[:12]:
    print(u'   %s｜L%-6s %s' % (kind, ln or u'-', info))
sys.exit(1 if bad else 0)
