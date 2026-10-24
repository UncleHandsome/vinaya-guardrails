# -*- coding: utf-8 -*-
"""第 253 輪・量尺二：第六章重整（合併・迎回・解綁・去定數）之落地前實測。

只量不改。四問：
  甲 ver39 百卡今制（號・題・組・卷段），八組合併對象是否確為同案正反支；
  乙 十一則請回案在 ver38 是否有完整卡（有則可移，無則須新撰——須另報）；
  丙 三組『大雜燩』在 ver39 今為合卡或分卡（外路所言係 ver38 之遮N）；
  丁 全書『百則／一百』式宣稱之數與落點（去定數則俱須隨動）。

用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r253census.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V39 = io.open(os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md'),
              encoding=u'utf-8').read()
V38 = io.open(os.path.join(ROOT, u'ver38四分律_起心動念心智分析框架_修正版.md'),
              encoding=u'utf-8').read()


def cards(txt, hpat, upto):
    ms = list(re.finditer(hpat, txt))
    out = []
    for m in ms:
        end = txt.find(u'\n#', m.end())
        end = len(txt) if end < 0 else min(end, txt.find(upto, m.end()) if txt.find(upto, m.end()) > 0 else len(txt))
        out.append((m.group(1).strip(), m.group(2).strip(), txt[m.end():m.end() + 4000]))
    return out


c39 = cards(V39, u'(?m)^### 〔案例\\s*(\\d+)〕([^\\n]*)$', u'# 第七章')
c38 = cards(V38, u'(?m)^#### 〔((?:遮|開|僧)\\d+)〕([^\\n]*)$', u'# 第七章')
print(u'〔甲〕ver39 案例卡 %d 枚｜ver38 舊卡 %d 枚' % (len(c39), len(c38)))
d39 = {n: (t, b) for n, t, b in c39}
d38 = {n: (t, b) for n, t, b in c38}

PAIRS = [(u'05', u'06'), (u'09', u'10'), (u'07', u'08'), (u'22', u'23'),
         (u'49', u'50'), (u'56', u'57'), (u'73', u'74'), (u'43', u'55'),
         (u'02', u'54'), (u'26', u'48'), (u'18', u'19'), (u'19', u'20')]
print(u'—— 合併對象今題（同組否・同卷段否）——')
grp = {}
for m in re.finditer(u'(?m)^## (第[一二三四五]組：[^\\n]*)', V39):
    pass
pos = [(m.start(), m.group(1)) for m in re.finditer(u'(?m)^## (第[一二三四五]組：[^\\n]*)', V39)]


def group_of(num):
    key = u'### 〔案例 %s〕' % num
    i = V39.find(key)
    g = u'（無組題）'
    for p, t in pos:
        if p < i:
            g = t[:22]
        else:
            break
    return g


for a, b in PAIRS:
    ta, ba = d39.get(a, (u'查無', u''))
    tb, bb = d39.get(b, (u'查無', u''))
    qa = re.findall(u'《四分律》卷([^（\\n]*)', ba)[:1]
    qb = re.findall(u'《四分律》卷([^（\\n]*)', bb)[:1]
    same = u'同人名' if any(x in bb for x in re.findall(u'[\\u4e00-\\u9fff]{3}', ta)[:2]) else u''
    print(u'  %s＋%s｜%s｜%s' % (a, b, ta[:22], tb[:22]))
    print(u'       組：%s／%s｜卷：%s／%s %s' % (group_of(a), group_of(b),
                                            qa[0] if qa else u'?', qb[0] if qb else u'?', same))

WANT = [
    (u'開1', u'跋提塚間甚樂', u'塚間'), (u'開4', u'親洗病僧屎尿', u'屎尿'),
    (u'遮16', u'守籠那調琴弦', u'琴弦'), (u'開14', u'落水救拔伸手無犯', u'水'),
    (u'開25', u'金布祇園名位共享', u'金布'), (u'遮33', u'泉水停供反被舉', u'泉水'),
    (u'開10', u'難民借衣與遣使受戒', u'借衣'), (u'開24', u'涅槃日哀慟哭了不犯', u'啼'),
    (u'遮7', u'聽諍彈指謦欬避嫌', u'謦'), (u'遮42', u'僧地入己更無有理', u'僧地'),
    (u'僧16', u'蓮華色創傷性覺醒', u'蓮華色'),
]
print(u'〔乙〕請回十一案：ver38 有無卡・ver39 有無卡・律文關鍵詞')
i39 = V39.find(u'# 第六章')
j39 = V39.find(u'# 第七章')
b39 = V39[i39:j39]
for lab, nm, kw in WANT:
    h38 = u'✓' if lab in d38 else u'✗'
    in39 = u'有' if kw in b39 else u'無'
    whole = u'有' if kw in V39 else u'無'
    print(u'  〔%-5s〕%-14s｜ver38 卡 %s %-22s｜第六章今：%s｜全書：%s'
          % (lab, nm, h38, (d38.get(lab, (u'—',))[0] or u'—')[:20], in39, whole))

print(u'〔丙〕三組大雜燩在 ver39 今制（搜關鍵詞所在卡）')
for kw in [u'私度', u'關', u'背約', u'安居', u'觀軍', u'賊', u'藏', u'坐具針', u'筒']:
    hits = [n for n, (t, b) in d39.items() if kw in (t + b)[:1200]]
    print(u'  「%s」→ 卡 %s' % (kw, u' '.join(hits[:8]) or u'查無'))

print(u'〔丁〕『百則／一百』宣稱之落點')
rows = [(i + 1, l.strip()[:64]) for i, l in enumerate(V39.split(u'\n'))
        if re.search(u'百則|一百則|百個|一百個|100 則|100則', l)]
print(u'  共 %d 行（列前 14）' % len(rows))
for i, s in rows[:14]:
    print(u'    L%-6d %s' % (i, s))
print(u'  『壹四十五／貳二十五／參三十』：%d｜『遮45』：%d｜『開25』：%d｜『僧30』：%d'
      % (V39.count(u'壹四十五'), V39.count(u'遮45'), V39.count(u'開25'), V39.count(u'僧30')))
