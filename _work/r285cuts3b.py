# -*- coding: utf-8 -*-
"""285・批三乙：#8 附錄三・一名相釋義立四大板塊之 H4 小標（56 詞逐條歸組，詞文一字不動）
   ＋#41 三名相補巴利（Abbhāna／Parivāsa／Mānatta，凡例已列故可徑補）。
   用法：python -X utf8 _work/r285cuts3b.py [--apply]"""
import io
import re
import sys

P = u'ver39四分律_起心動念心智分析框架_修正版.md'
APPLY = u'--apply' in sys.argv
S = io.open(P, encoding=u'utf-8').read()
NL = u'\r\n' if u'\r\n' in S else u'\n'
T = S.replace(u'\r\n', u'\n')
L = T.split(u'\n')

GROUPS = [
    (u'#### 一、境想與心識之判（故意之有無）',
     [u'如實想', u'差誤想（想差）', u'生疑', u'失念', u'故作', u'誤作',
      u'三時心', u'境差／緣差／心差', u'境想六句', u'使作']),
    (u'#### 二、罪性與刑名之階（犯相之輕重）',
     [u'性罪（自性罪）', u'遮罪（制止罪）', u'作犯與止犯', u'作持', u'止持', u'有漏',
      u'僧伽婆尸沙', u'偷蘭遮', u'波逸提', u'尼薩耆波逸提', u'波羅提提舍尼', u'突吉羅',
      u'賊住', u'犯邊罪', u'與波羅夷戒']),
    (u'#### 三、羯磨・法權與滅諍（程序之成就）',
     [u'自言治', u'現前毘尼', u'求聽羯磨', u'舉罪五德', u'下意羯磨', u'捨置驅棄（默擯）',
      u'結小界', u'五如法', u'四瑕疵', u'三種舉羯磨', u'憶念毘尼', u'不癡毘尼',
      u'四諍', u'七滅諍法', u'三重護念', u'四清淨']),
    (u'#### 四、行治階序與律事名物（出罪之路・制中之人相時相）',
     [u'別住（波利婆沙）', u'本日治', u'修合別住', u'失宿（八事失夜）', u'摩那埵（意喜）',
      u'滿摩那埵位', u'出罪（阿浮呵那）', u'善逝推定', u'離處', u'明相', u'自恣',
      u'式叉摩那', u'淨人', u'守園人', u'白衣']),
]

a = next(i for i, x in enumerate(L) if x.startswith(u'### 一、律典原生核心名相法意釋義'))
b = next(i for i, x in enumerate(L) if x.startswith(u'### 二、律典原生人名與巴利對照表'))
terms = {}
order = []
for i in range(a + 1, b):
    m = re.match(u'^\\*   \\*\\*([^*]+)\\*\\*：', L[i])
    if m:
        nm = m.group(1)
        assert nm not in terms, u'名相重題：%s' % nm
        terms[nm] = L[i]
        order.append(nm)
print(u'今量：詞 %d・首 L%d・末 L%d' % (len(order), a + 1, b))

plan = [x for g in GROUPS for x in g[1]]
assert sorted(plan) == sorted(order), u'歸組清單與冊身之詞不合：缺 %s／多 %s' % (
    sorted(set(order) - set(plan)), sorted(set(plan) - set(order)))
for g in GROUPS:
    assert len(g[1]) >= 8, g[0]

# 巴利三名（徑入詞題，不動釋義之文）
PALI = {u'別住（波利婆沙）': u'別住（波利婆沙·Parivāsa）',
        u'摩那埵（意喜）': u'摩那埵（意喜·Mānatta）',
        u'出罪（阿浮呵那）': u'出罪（阿浮呵那·Abbhāna）'}
for k, v in PALI.items():
    assert k in terms, u'巴利之靶不在：%s' % k
    terms[k] = terms[k].replace(u'**' + k + u'**', u'**' + v + u'**', 1)
print(u'巴利補 %d 名' % len(PALI))

NEW = [L[a]]
for head_t, names in GROUPS:
    NEW.append(u'')
    NEW.append(head_t)
    NEW.append(u'')
    for nm in names:
        NEW.append(terms[nm])
body = NEW + [u'', u'---', u''] + L[b:]
T2 = u'\n'.join(L[:a] + body)
print(u'行數 %+d' % (len(T2.split(u'\n')) - len(L)))
assert T2.count(u'#### 一、境想與心識之判') == 1
for nm in plan:
    assert terms[nm] in T2, u'詞失落：%s' % nm
print(u'校：%d 詞俱在・四標各一' % len(plan))

if APPLY:
    io.open(u'_archive/備份/ver39.pre285d.md', 'w', encoding=u'utf-8', newline=u'\n').write(T)
    io.open(P, 'w', encoding=u'utf-8', newline=NL).write(T2)
    print(u'已寫入')
else:
    print(u'（試跑・未寫檔）')
