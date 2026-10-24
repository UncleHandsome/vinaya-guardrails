# -*- coding: utf-8 -*-
"""刀八～刀十 落檔後之覆核：編號連貫、指針不越界、迎回卡六欄齊備、合併卡合參俱在。"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = io.open(os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md'),
            encoding=u'utf-8').read()
L = T.split(u'\n')
nums = [int(m.group(1)) for m in re.finditer(u'(?m)^### 〔案例 (\\d+)〕', T)]
print(u'行數 %d｜案例卡 %d 枚｜連貫：%s' % (len(L), len(nums), nums == list(range(1, len(nums) + 1))))
refs = [int(m.group(1)) for m in re.finditer(u'〔案例 ?(\\d{1,2})〕', T)]
print(u'指針 %d 處｜越界：%s' % (len(refs), sorted(set(r for r in refs if r > len(nums))) or u'無'))
SECT = [u'事相經過', u'心相照鏡', u'佛陀處斷', u'人間智慧', u'律典原典']
heads = [(i, l) for i, l in enumerate(L) if re.match(u'^### 〔案例 \\d+〕', l)]
bad = []
for k, (i, l) in enumerate(heads):
    end = heads[k + 1][0] if k + 1 < len(heads) else i + 60
    seg = u'\n'.join(L[i:end])
    miss = [s for s in SECT if seg.count(u'#### 【%s】' % s) != 1]
    if miss:
        bad.append((re.match(u'^### 〔案例 (\\d+)〕(.*)', l).group(1), miss, l[:34]))
print(u'六欄不齊之卡：%d 枚 %s' % (len(bad), bad[:4]))
for lab in [u'跋提塚間', u'親洗病僧', u'琴弦', u'落水救拔', u'金布祇園', u'泉水停供',
            u'難民借衣', u'涅槃日哀慟', u'聽諍彈指', u'僧地入己', u'蓮華色創傷']:
    hit = [(i + 1, l[:52]) for i, l in enumerate(L)
           if l.startswith(u'### 〔案例') and lab in l]
    print(u'  迎回『%s』→ %s' % (lab, hit or u'✗ 未見'))
print(u'雙判合參：%d 條｜舊帳〔遮/開/僧N〕殘留：%d'
      % (T.count(u'雙判合參'), len(re.findall(u'〔(?:遮|開|僧)\\d+〕', T))))
print(u'『百則』類宣稱今存：%d 行（待刀十一隨動）'
      % len([l for l in L if re.search(u'百則|一百則|百個判例|一百個', l)]))
