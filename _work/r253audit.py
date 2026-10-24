# -*- coding: utf-8 -*-
"""第 253 輪：外路兩份 ver39 審查報告之逐條量尺（先量後刀，報告之數非證據）。

用法：PYTHONPATH=. PYTHONIOENCODING=utf-8 python -X utf8 _work/r253audit.py
"""
import io
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
SRCF = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
OLD38 = os.path.join(ROOT, u'ver38四分律_起心動念心智分析框架_修正版.md')
L = io.open(SRCF, encoding=u'utf-8').read().split(u'\n')
T = u'\n'.join(L)
O = io.open(OLD38, encoding=u'utf-8').read()

# 篇界（以 H1 為牢）
H1 = [(i, l[2:].strip()) for i, l in enumerate(L) if l.startswith(u'# ')]


def sec(pat):
    a = next((i for i, t in H1 if re.search(pat, t)), None)
    if a is None:
        return None, None
    b = next((i for i, t in H1 if i > a), len(L))
    return a, b


def rng(pat):
    a, b = sec(pat)
    return L[a:b] if a is not None else []


def where(lines, rx, cap=6):
    out = []
    for i, l in enumerate(lines):
        if re.search(rx, l):
            out.append((i + 1, l.strip()[:70]))
    return out[:cap], len(out)


def hdr(t):
    print(u'\n' + u'=' * 12 + u' %s ' % t + u'=' * 12)


hdr(u'⓪ 全書骨架（H1）')
for i, t in H1:
    print(u'  L%-6d %s' % (i + 1, t[:48]))

hdr(u'① 舊案號〔遮/開/僧/遺〕與新案號〔案例NN〕之兩轨')
old = Counter()
for m in re.finditer(u'〔(遮|開|僧|遺)\\s*(\\d+)〕', T):
    old[m.group(1)] += 1
print(u'  舊式引用合计：%d｜%s' % (sum(old.values()), dict(old)))
print(u'  新式〔案例NN〕：%d' % len(re.findall(u'〔案例\\s*\\d+〕', T)))
print(u'  案例卡片標題：### 〔案例NN〕%d 枚｜### 〔補遺NN〕%d 枚'
      % (len(re.findall(u'(?m)^### 〔案例', T)), len(re.findall(u'(?m)^### 〔補遺', T))))
# 逐章計舊式引用
marks = [(i, t) for i, t in H1]
def chapter_of(idx):
    cur = u'卷首'
    for i, t in marks:
        if i > idx:
            break
        cur = t[:12]
    return cur
cnt = Counter()
for i, l in enumerate(L):
    for m in re.finditer(u'〔(遮|開|僧|遺)\\s*\\d+〕', l):
        cnt[chapter_of(i)] += 1
for k, v in cnt.most_common():
    print(u'    %-14s %d' % (k, v))

hdr(u'② 報告所稱『失蹤之 16 則骨架大案』今在第六章與否（以事相關鍵詞搜）')
cases = [(u'原開3 糞掃衣想', u'糞掃'), (u'原開1 跋提塚間甚樂', u'塚間'),
         (u'原開4 親洗病僧屎尿', u'屎尿'), (u'原開10 難民借衣遣使受戒', u'遣使|借衣'),
         (u'原開13 三辭共治', u'三辭'), (u'原開14 落水救拔伸手', u'落水'),
         (u'原開15 毘舍佉遺寶代遮羞', u'毘舍佉|畏輸|失宝|遺宝|遺寶'),
         (u'原開16 出鉢示之透明避嫌', u'出鉢'),
         (u'原開25 金布祇園共享', u'祇樹|金布|八地'),
         (u'原遮11 塔下坐臥輕慢 SPACE', u'佛塔|塔中|塔下'),
         (u'原遮14 詐病濫用開許', u'革履|穿皮鞋|詐病|皮鞋'),
         (u'原遮33 泉水停供反被舉', u'泉水|我共汝'),
         (u'原遮42 僧地入己', u'僧地'),
         (u'原僧4 四姓出家大海一味', u'四姓|大海'),
         (u'原僧6 四諍七滅諍', u'四諍'),
         (u'原僧25 佛陀選擇性沉默', u'選擇性沉默|不記|默然不答|置記')]
c6 = rng(u'^第六章')
c6t = u'\n'.join(c6)
for name, kw in cases:
    insix = [c6t.index(m.group(0)) for m in [re.search(kw, c6t)] if m]
    cards = [l.strip()[:60] for i, l in enumerate(c6)
             if l.startswith(u'### 〔案例') and re.search(kw, u'\n'.join(c6[i:i + 40]))]
    print(u'  %-26s 第六章%3s｜卡片：%s'
          % (name, u'有' if insix else u'無', (cards[0] if cards else u'—')))

hdr(u'③ 『第九章』死鏈（ver39 唯八章）')
p, n = where(L, u'第九章', 40)
print(u'  全書『第九章』%d 見' % n)
for i, s in p:
    print(u'    L%-6d %s' % (i, s))
print(u'  『第十章』%d 見｜『第十一章』%d 見' % (T.count(u'第十章'), T.count(u'第十一章')))

hdr(u'④ 工程代碼標籤殘留（報告稱已承諾刪除）')
for k in [u'【道岔', u'〔◈跨章精準導流〕', u'〔◈本書法式', u'〔◈', u'YAML', u'定位行',
          u'問[1]', u'問[16]', u'閘門三第', u'slim', u'SLIM']:
    print(u'  %-18s %d' % (k, T.count(k)))
p, n = where(L, u'【道岔', 8)
for i, s in p:
    print(u'    L%-6d %s' % (i, s))

hdr(u'⑤ 金句首尾一次之承諾與實數')
for k in [u'感覺不到內臟', u'對簿公堂', u'吃茶去', u'首尾各', u'各出現一次', u'唯兩見',
          u'金句修辭脫水']:
    print(u'  %-18s %d' % (k, T.count(k)))
p, n = where(L, u'感覺不到內臟', 10)
for i, s in p:
    print(u'    L%-6d %s' % (i, s))
p, n = where(L, u'吃茶去', 10)
print(u'  『吃茶去』%d 見' % n)

hdr(u'⑥ 第七章之節實況（目録稱第三節為何、正文為何）')
c7 = rng(u'^第七章')
for i, l in enumerate(c7):
    if re.match(u'^#{2,3} ', l):
        print(u'  L%-6d %.66s' % (i + 1, l))
print(u'  『29 則』%d｜『複統攝』%d｜『稱重』%d（全書）'
      % (T.count(u'29 則'), T.count(u'複統攝'), T.count(u'稱重')))

hdr(u'⑦ 四大行動卡是否兩處重貼（正規化後比塊身）')
blocks = []
for i, l in enumerate(L):
    if re.search(u'四大.*(行動卡|自律)', l) and l.startswith(u'#'):
        blocks.append((i + 1, l.strip()[:60]))
for i, s in blocks:
    print(u'  標題 L%-6d %s' % (i, s))
def card_body(start):
    j = start - 1
    out = []
    while j < len(L) and not (L[j].startswith(u'#') and j > start - 1):
        out.append(L[j]); j += 1
    return re.sub(u'\\s+', u'', u''.join(out))[:400]
bodies = [(i, card_body(i)) for i, _ in blocks]
for a in range(len(bodies)):
    for b in range(a + 1, len(bodies)):
        s1, s2 = bodies[a][1], bodies[b][1]
        same = 100.0 * len([1 for x, y in zip(s1, s2) if x == y]) / max(1, min(len(s1), len(s2)))
        print(u'  L%-5d vs L%-5d 前400字同形率 %.0f%%' % (bodies[a][0], bodies[b][0], same))

hdr(u'⑧ 附錄三辭典詞目覆蓋（報告點名之詞）')
a3 = u'\n'.join(rng(u'^附錄三'))
for k in [u'五錢', u'離處', u'淨人', u'守園人', u'式叉摩那', u'自恣', u'明相', u'作持',
          u'止持', u'故作', u'誤作', u'使作', u'安居', u'羯磨']:
    print(u'  %-10s 附錄三%s｜全書%d' % (k, u'有' if k in a3 else u'無', T.count(k)))
print(u'  附錄三詞目行數（| 表行）：%d' % len([l for l in a3.split(u'\n') if l.strip().startswith(u'|')]))
seg = O[O.find(u'附錄D'):O.find(u'附錄E')] if u'附錄D' in O and u'附錄E' in O else u''
print(u'  ver38 附錄D 區段之表行數（對照）：%d' % len([l for l in seg.split(u'\n') if l.strip().startswith(u'|')]))

hdr(u'⑨ 附錄五經論互證條數與報告點名之典')
a5 = u'\n'.join(rng(u'^附錄五'))
print(u'  附錄五表行 %d｜其中 |--- 分隔 %d'
      % (len([l for l in a5.split(u'\n') if l.strip().startswith(u'|')]),
         len([l for l in a5.split(u'\n') if re.match(u'^\\|\\s*[:\\-]+$', l.strip())])))
for k in [u'俱舍', u'解深密', u'三十頌', u'寶性論', u'成唯識', u'大智度']:
    print(u'  %-8s 附錄五%s｜全書%d 見' % (k, u'有' if k in a5 else u'無', T.count(k)))
print(u'  ver38 附錄F 同詞：%s'
      % {k: O.count(k) for k in [u'俱舍', u'解深密', u'三十頌', u'寶性論']})

hdr(u'⑩ 案例 01／02 之文獻細節')
c1 = rng(u'^第六章')
i1 = next((i for i, l in enumerate(c1) if l.startswith(u'### 〔案例 01')), None)
i2 = next((i for i, l in enumerate(c1) if l.startswith(u'### 〔案例 02')), None)
for nm, idx in [(u'案例01', i1), (u'案例02', i2)]:
    body = u''.join(c1[idx:idx + 40]) if idx is not None else u''
    print(u'  %s 三度:%d 三道:%d 瓦:%d 燒:%d 砸:%d'
          % (nm, body.count(u'三度'), body.count(u'三道'), body.count(u'瓦'),
             body.count(u'燒'), body.count(u'砸')))
import _tk  # noqa  E402  語料唯一法源（原文/ 非 UTF-8，不得自讀）
print(u'  語料『共行三道』%d 見｜『三度行不淨行』%d 見｜『瓦屋』%d 見｜『糞掃衣』%d 見'
      % (_tk.VINAYA.count(u'共行三道'), _tk.VINAYA.count(u'三度行不淨行'),
         _tk.VINAYA.count(u'瓦屋'), _tk.VINAYA.count(u'糞掃衣')))
print(u'  （_tk.SRC 現指：%s）' % os.path.basename(_tk.SRC))
