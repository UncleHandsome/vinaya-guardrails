# -*- coding: utf-8 -*-
"""276 輪・第六章補案器：新稿自稱『一百零二片』而實收 63 號＋地標 19 事，缺 20 餘案——
**一律自舊卡欄位與附錄四機械抽出**，補入各戰場之集群矩陣；地標／雙螺旋各補一枚『案號』列，俾全書指針有歸。

鐵則：
  一・**不自創語**——五欄之位：案號與案名←舊卡題・起心動念←卡之『病相』・核心爭點←卡之『戒條＋正理』、
      佛陀處斷←附錄四逐字之結戒句（原句截取）、律典出處←附錄四卷段篇聚（已核）。
  二・**戰場之歸屬**由人定（下表 FIELD），規則僅供參考；歸錯即義理之錯，故須逐枚親閱印出之對照。
  三・冪等：一律自 `r276d.md` 重敷 ➔ `r276e.md`；改動全數印出。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r276rows.py [--go]
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, u'_work', u'r276d.md')
DST = os.path.join(ROOT, u'_work', u'r276e.md')
BOOK = io.open(os.path.join(ROOT, [q for q in os.listdir(ROOT) if q.startswith(u'ver39')
                                   and q.endswith(u'.md') and u'列印' not in q][0]),
               encoding=u'utf-8-sig').read().split(u'\n')
GO = u'--go' in sys.argv

# ── 一・舊卡欄位抽出
def cards():
    out = {}
    for i, l in enumerate(BOOK):
        m = re.match(u'^### 〔案例 (\\d+)〕(.*)', l)
        if not m:
            continue
        n = int(m.group(1))
        if n in out:
            continue
        title = m.group(2).strip()
        front = title.split(u'——')[0].strip()
        nav = next((BOOK[j] for j in range(i + 1, min(i + 6, len(BOOK))) if u'法相導航' in BOOK[j]), u'')
        body = u'\n'.join(BOOK[i + 1:i + 60])
        bing = re.search(u'病相：([^｜]*)', nav)
        zheng = re.search(u'正理天平：(.*)', nav)
        tie = re.match(u'([^｜]*)', nav.replace(u'* **法相導航**：', u'').strip())
        out[n] = {u'名': front, u'戒': (tie.group(1).strip() if tie else u''),
                  u'病': (bing.group(1).strip() if bing else u''),
                  u'正': (zheng.group(1).strip() if zheng else u'')}
    return out


# ── 二・附錄四之行（卷段篇聚＋逐字結戒句）
def apx4():
    a = next(i for i, l in enumerate(BOOK) if l.startswith(u'# 附錄四'))
    out = {}
    for j in range(a, len(BOOK)):
        l = BOOK[j]
        m = re.match(u'^\\| \\*\\*〔案例 (\\d+)〕([^*]+)\\*\\* \\| ([^|]+) \\| ([^|]+) \\|$', l)
        if m:
            out[int(m.group(1))] = (m.group(3).strip(), m.group(4).strip())
    return out


CARDS, APX = cards(), apx4()

# ── 三・戰場歸屬（人定；1＝深淵之線 2＝自尊的迷津 3＝長物的枷鎖 4＝微境的暗流 5＝權力的試煉）
FIELD = {3: 1, 35: 1, 71: 1, 73: 1,
         28: 3, 60: 3, 68: 3, 70: 3, 72: 3, 96: 3, 99: 3,
         40: 4, 59: 4, 61: 4, 62: 4, 64: 4, 65: 4, 66: 4, 67: 4, 69: 4, 92: 4, 94: 4, 100: 4,
         58: 5, 17: 1, 95: 4}   # 81 拘睒彌撤離：新稿已併入地標 12 之題，此處僅備分派
WAR = {1: u'第一戰場', 2: u'第二戰場', 3: u'第三戰場', 4: u'第四戰場', 5: u'第五戰場'}

D = io.open(SRC, encoding=u'utf-8-sig').read().replace(u'\r\n', u'\n').rstrip(u'\n').split(u'\n')
have = {int(m) for m in re.findall(u'案例\\s*0?(\\d{1,3})', u'\n'.join(D))}
PU = re.compile(u'[\\s\\u3000，、；：？！。「」『』（）()〔〕\\[\\]·／/#*>|:—\\-➔╳X]')
norm = lambda s: PU.sub(u'', s)
LAND = [(i, l) for i, l in enumerate(D) if re.match(u'^### 【(經典地標深描|雙螺旋對照專題)', l)]
assign = {}
for i, l in LAND:
    h = norm(l)
    hits = [n for n, c in CARDS.items() if n not in have
            and sum(1 for k in range(max(1, len(norm(c[u'名'])) - 2))
                    if norm(c[u'名'])[k:k + 3] in h) >= 2]
    if hits:
        assign[i] = sorted(hits)
print(u'地標／雙螺旋 依名核得之案號：')
for i, ns in assign.items():
    print(u'   L%-5d %s ➔ %s' % (i + 1, D[i][4:34], u'・'.join(u'案例%02d' % n for n in ns)))

# 手補：新稿以副題承事而無名可核者（地標 07『與長衣過十日』➔ 案例28；地標 12『與佛陀深林撤離』➔ 案例81）
HAND = [(u'長衣過十日', [28]), (u'深林撤離', [81])]
for phrase, ns in HAND:
    hit = [i for i, l in LAND if phrase in l]
    assert len(hit) == 1, u'%s｜地標錨非一' % phrase
    assign.setdefault(hit[0], [])
    for n in ns:
        if n not in assign[hit[0]]:
            assign[hit[0]].append(n)
    print(u'手補｜%s ➔ %s' % (phrase, u'・'.join(u'案例%02d' % x for x in assign[hit[0]])))

# 地標块內若全無〔案例 NN〕可追（如 02 檀尼迦＝案例02、09 六群二案＝37・38），一律補案號列
for i, l in LAND:
    j = next((k for k in range(i + 1, len(D)) if D[k].startswith(u'### ')), len(D))
    if any(u'案例' in x for x in D[i:j]):
        continue
    h = norm(l)
    hits = [n for n, c in CARDS.items()
            if sum(1 for k in range(max(1, len(norm(c[u'名'])) - 2)) if norm(c[u'名'])[k:k + 3] in h) >= 2]
    hits = sorted(set(hits) | set(assign.get(i, [])))
    assert hits, u'地標 L%d 無案可配：%s' % (i + 1, l[:30])
    assign[i] = hits
    print(u'補案號列｜L%d %s ➔ %s' % (i + 1, l[4:26], u'・'.join(u'案例%02d' % n for n in assign[i])))

todo = sorted(n for n in CARDS if n not in have and not any(n in v for v in assign.values()))
print(u'\n未收而須補矩陣者 %d 案：%s' % (len(todo), todo))
print(u'戰場分佈：%s' % u'・'.join(u'%s %d' % (WAR[k], sum(1 for n in todo if FIELD.get(n) == k))
                                 for k in sorted({FIELD[n] for n in todo})))
unplaced = [n for n in todo if n not in FIELD]
assert not unplaced, u'未定戰場之案：%s' % unplaced


def jieji(quote):
    """附錄四逐字之截取：取結戒／制戒句（『欲說戒者…』或『自今已去…』），無則取尾句。"""
    for pat in (u'欲說戒者當如是說[^」]*', u'自今已去[^」]*', u'若比丘[^」]*波逸提[^」]*', u'[^」]*突吉羅[^」]*'):
        m = re.search(pat, quote)
        if m:
            s = m.group(0).strip().replace(u'」', u'').replace(u'』', u'').replace(u'「', u'').replace(u'『', u'')
            return s[:78] + (u'…' if len(s) > 78 else u'')
    tail = quote.strip().replace(u'」', u'').replace(u'』', u'').replace(u'「', u'').replace(u'『', u'').split(u'……')[0].strip()
    return (tail[-60:] + u'…') if len(tail) > 60 else tail


def row(n):
    c = CARDS[n]
    vol, quote = APX.get(n, (u'卷段見附錄四', u''))
    zhang = c[u'正'].split(u'、')[0].strip() or u'正理天平見卡'
    claim = u'%s：犯緣與開緣之界如何判？' % (c[u'戒'] or c[u'名'])
    return (u'| **〔案例 %02d〕**<br>**%s** | %s | %s | %s | 《四分律》%s |' % (
        n, c[u'名'], c[u'病'] or u'（病相見卡）', claim,
        u'**%s**<br>%s' % (zhang, jieji(quote) if quote else u'原典見附錄四'), vol))


out, i, n_row_added, n_hdr = [], 0, 0, 0
while i < len(D):
    l = D[i]
    m = re.match(u'^(### )(第[一二三四五]戰場周邊案例集群矩陣速查（)(\d+)( 案）)$', l)
    if m:
        war = {u'第一': 1, u'第二': 2, u'第三': 3, u'第四': 4, u'第五': 5}[m.group(2)[:2]]
        grp = [n for n in todo if FIELD[n] == war]
        j = i + 1
        while j < len(D) and not D[j].startswith(u'### '):
            j += 1
        k = j - 1
        while k > i and not D[k].startswith(u'| **〔案例'):
            k -= 1
        new = D[i + 1:k + 1] + [row(n) for n in grp] + D[k + 1:j]
        cnt = int(m.group(3)) + len(grp)
        out.append(u'### %s%d 案）' % (m.group(2), cnt))
        out.extend(new)
        n_row_added += len(grp)
        n_hdr += 1
        print(u'補 L%-5d %s：+%d 行（宣 %s ➔ %d）｜案 %s' % (
            i + 1, m.group(2)[:6], len(grp), m.group(3), cnt, u','.join('%02d' % x for x in grp)))
        i = j
        continue
    if i in assign:
        out.append(l)
        k = i + 1
        while k < len(D) and D[k].strip() == u'':
            out.append(D[k])
            k += 1
        out.append(u'*   **案號**：%s' % u'・'.join(
            u'〔案例 %02d〕%s' % (n, CARDS[n][u'名']) for n in assign[i]))
        out.append(u'')
        i = k
        continue
    out.append(l)
    i += 1
print(u'矩陣補行 %d・表頭改 %d・地標加案號列 %d' % (n_row_added, n_hdr, len(assign)))
final = {int(m) for m in re.findall(u'案例\\s*0?(\\d{1,3})', u'\n'.join(out))}
miss = sorted(set(CARDS) - final)
print(u'全書案號 1..102 今見於新章者 %d 個｜猶缺：%s' % (len(final & set(CARDS)), miss))
if not GO:
    print(u'（dry-run｜加 --go 方落盤）')
    sys.exit(0)
io.open(DST, 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(out) + u'\n')
print(u'落盤 %s（%d 行）' % (DST, len(out)))
