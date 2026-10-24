# -*- coding: utf-8 -*-
"""第 253 輪・量尺三：四案是否確佚・三事相今在何卡（以卡題與卡身求，不以全書關鍵詞概測）。"""
import io, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V39 = io.open(os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md'), encoding='utf-8').read()
V38 = io.open(os.path.join(ROOT, u'ver38四分律_起心動念心智分析框架_修正版.md'), encoding='utf-8').read()
i, j = V39.find(u'# 第六章'), V39.find(u'# 第七章')
c6 = V39[i:j]
cards = [(m.group(1), m.group(2).strip(), c6[m.start():m.start() + 6000])
         for m in re.finditer(u'(?m)^### 〔案例\\s*(\\d+)〕([^\\n]*)$', c6)]
print(u'第六章卡 %d 枚' % len(cards))


def find(kw, where=cards, col=2):
    return [n for n, t, b in where if kw in (t if col == 1 else b)]


print(u'—— 四案之確查（卡題・卡身）——')
for nm, kws in [(u'落水救拔〔開14〕', [u'救溺', u'溺水', u'漂', u'落水']),
               (u'涅槃哀慟〔開24〕', [u'哀慟', u'哭', u'啼']),
               (u'彈指避嫌〔遮7〕', [u'彈指', u'謦', u'咳']),
               (u'蓮華色覺醒〔僧16〕', [u'蓮華色'])]:
    t_hit = [n for n, t, b in cards if any(k in t for k in kws)]
    b_hit = find(kws[0]) + find(kws[1]) if len(kws) > 1 else find(kws[0])
    print(u'  %-16s｜卡題中：%s｜卡身『%s』：%s' % (nm, t_hit or u'無', kws[0], (b_hit[:6] or u'無')))

print(u'—— 三事相之確查（ver39 全書／第六章／ver38 何卡）——')
for nm, kw in [(u'私度關卡逃稅', u'度關'), (u'安居聞利背約', u'背約'),
               (u'藏他坐具針筒', u'藏坐具'), (u'金布買園', u'金布'),
               (u'僧地入己', u'僧地'), (u'泉水停供', u'泉水'),
               (u'病僧屎尿', u'屎尿'), (u'塚間甚樂', u'塚間'),
               (u'琴弦中道', u'琴'), (u'借衣', u'借衣'), (u'遣使受戒', u'遣使')]:
    v39 = find(kw)
    v38 = [n for n, t, b in [(m.group(1), m.group(2), V38[m.start():m.start() + 6000])
                             for m in re.finditer(u'(?m)^#### 〔((?:遮|開|僧)\\d+)〕([^\\n]*)$', V38)]
           if kw in b][:6]
    print(u'  「%-8s」 ver39 第六章：%s｜ver38：%s' % (nm, v39 or u'查無', v38 or u'查無'))
