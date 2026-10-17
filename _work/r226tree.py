# -*- coding: utf-8 -*-
# r226tree　大樹七層之層序與土壤定義，三處俱須同（第 226 輪立，長駐・專軸）
#
#   所以立之：第二章導言第一款自稱『全書大樹隱喻嚴整對應為七層生命體系』，第七章第一節別有
#   拓撲圖、自然層序之句與『七層生克機制深描』七目——三處各立字面而無一器校之。第 226 輪外路報
#   『土壤』之定義兩處相左（第二章作正理二＋正理三『世間信心與護生不害』，第七章作『結界管轄權＋
#   世間信心防火牆』），親量得實；此與第 221／223 輪『以字面為鍵之表隨動須連宣稱』同族，故歸一之後
#   即立此軸，使三處之層序與土壤二翼再不能各說各話。
#
#   口徑：① 層名取各目之**領起詞**（第二章 bullet 之 `* **X（`、第七章深描之 `N. **X（`、
#   自然層序句之 `→` 鏈），不掃全段——掃全段則『社會信任土壤』『果實成熟』之屬必生假陽性；
#   ② 鏈上之異形（『六大領域主枝』『100 片法相之葉』）以其末字配 canon 之末字，末字七者各異，故無歧義；
#   ③ 土壤之兩翼唯斷其俱含『結界』與『世間信心』，不作全串逐字之較（兩處文氣本異，強校即假陽性）；
#   ④ 第二章須有歸法源之指針（『第七章第一節』四字在焉）。
#   源檔隨 `_tk.SRC`（故 TKSRC 之植病副本可測）。
#   用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r226tree.py
from __future__ import unicode_literals
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as T

LINES = T.LINES
BOT = T.bottom_lines()      # 底冊乃記錄，必轉述層名與舊說——轉述非宣稱，故不校（218 輪之裁）
CANON = [u'土壤', u'樹根', u'樹幹', u'主枝', u'樹葉', u'果實', u'種子']
BYLAST = dict((c[-1], c) for c in CANON)
assert len(BYLAST) == 7, u'末字有歧，不可為配'
bad = []


def seq_of(items, site):
    got = []
    for raw in items:
        t = raw.strip().strip(u'*').strip()
        t = re.split(u'（|·|:|：', t)[0].strip()
        c = BYLAST.get(t[-1]) if t else None
        if c is None:
            bad.append((u'非七層之名', site, u'領起詞『%s』不在七層之內' % t))
        else:
            got.append(c)
    if got != CANON:
        bad.append((u'層序不合', site, u'得 %s｜須 %s' % (u'→'.join(got), u'→'.join(CANON))))
    return got


def find_line(pat, want=1):
    hits = [i for i, l in enumerate(LINES) if i not in BOT and pat in l]
    assert len(hits) == want, u'錨『%s』得 %d 見（須 %d）' % (pat, len(hits), want)
    return hits[0]


# 一、第二章導言七層（bullet）
a = find_line(u'全書大樹隱喻嚴整對應為七層')
bul = []
i = a + 1
soil2 = u''
while i < len(LINES):
    s = LINES[i]
    if s.startswith(u'* **'):
        head = s[4:].split(u'：', 1)[0]
        bul.append(head)
        if head.startswith(CANON[0]):
            soil2 = s
    elif s.strip() and not s.startswith(u'*'):
        break
    i += 1
seq_of(bul, u'L%d 第二章導言' % (a + 1))
if u'第七章第一節' not in LINES[a]:
    bad.append((u'無法源之指針', a + 1, u'第二章自列七層而不歸其序於第七章第一節'))

# 二、第七章自然層序（→ 鏈）
b = find_line(u'自然層序')
m = re.search(r'\*\*([^*]*%s[^*]*)\*\*' % CANON[0], LINES[b])
assert m, u'自然層序句內無層鏈：L%d' % (b + 1)
seq_of(m.group(1).split(u'→'), u'L%d 自然層序' % (b + 1))

# 三、第七章七層生克機制深描（ numbered ）
c = find_line(u'#### 二、七層生克機制深描')
num, soil7 = [], u''
j = c + 1
while j < len(LINES):
    s = LINES[j]
    if s.startswith(u'#### ') or s.startswith(u'### '):
        break
    mm = re.match(r'^\d+\. \*\*(.+?)\*\*', s)
    if mm:
        num.append(mm.group(1))
        if mm.group(1).startswith(CANON[0]):
            soil7 = s + (LINES[j + 1] if j + 1 < len(LINES) else u'')
    j += 1
seq_of(num, u'L%d 七層深描' % (c + 1))

# 四、土壤之兩翼須兩處俱同
for tag, txt, ln in ((u'第二章', soil2, a + 1), (u'第七章', soil7, c + 1)):
    if not txt:
        bad.append((u'土壤之目缺', ln, u'%s七層之內無『土壤』一目' % tag))
        continue
    for wing in (u'結界', u'世間信心'):
        if wing not in txt:
            bad.append((u'土壤之翼不合', ln, u'%s之土壤無『%s』：%.24s…' % (tag, wing, txt)))

print(u'三處層序各 %d｜%d｜%d 目｜土壤兩翼俱校｜病 %d 處%s'
      % (len(bul), len(num), len(m.group(1).split(u'→')) if m else 0, len(bad), u' []' if not bad else u''))
for kind, ln, info in bad[:10]:
    print(u'   %s｜L%-6s %s' % (kind, ln, info))
sys.exit(1 if bad else 0)
