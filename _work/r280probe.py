# -*- coding: utf-8 -*-
"""280・外路第八報告（論第四・五章）逐條量今檔＋語料（量而不刀）。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r280probe.py
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, u'_work'))
import _tk                                                     # noqa: E402

BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
LINES = io.open(BOOK, encoding=u'utf-8-sig').read().split(u'\n')
V = _tk.VINAYA

H4 = next((i for i, l in enumerate(LINES) if l.startswith(u'# 第四章')), None)
H6 = next((i for i, l in enumerate(LINES) if l.startswith(u'# 第六章')), None)

CASES = [
    (u'甲一 戒格雖復', [u'戒格雖復', u'侵吞常住財物滿五錢', u'滿五錢者']),
    (u'甲二 僧物四名', [u'前三分', u'第四分', u'常住常住物', u'現前現前物', u'十方現前物', u'十方常住物']),
    (u'乙一 受別住法式', [u'單白告眾', u'受別住', u'白四羯磨']),
    (u'乙二 同罪相懺', [u'同罪相懺', u'急難同犯', u'推舉一人']),
    (u'乙三 出界說戒', [u'原大界管轄權凍結', u'步出爭議大界', u'結四方小界', u'另結小界']),
    (u'丙一 心證三級', [u'獨立偷蘭遮', u'客觀事相查驗明確', u'五階心證']),
    (u'丙二 不知犯', [u'不知犯', u'後知', u'不覆藏', u'覆藏時鐘', u'當日自首']),
    (u'丁一 非法足數', [u'身懷僧殘覆藏未發露', u'非法足數', u'善意信賴保護']),
    (u'丁二 解擯管轄', [u'解擯出羯磨', u'乞解', u'原處分', u'污他家']),
    (u'丁三 惡意不忍', [u'不忍', u'程序即告中止', u'一人當庭唱']),
    (u'戊一 責心對首', [u'對首或責心', u'責心自誓', u'對首發露即得']),
    (u'戊二 備案凍結', [u'口頭備案', u'三十日', u'副署', u'書面']),
    (u'戊三 自省特權', [u'不得作為指控', u'小參', u'私密行歷', u'重大危害']),
    (u'戊四 求聽豁免', [u'從彼求聽', u'第一階', u'性侵害', u'求聽']),
    (u'己一 自言治接口', [u'二種法定情事', u'三種法定情事', u'不自創免口供', u'客觀科學鐵證']),
    (u'己二 不見罪舉界', [u'唯施於認事不認罪', u'否認事實', u'全盤否認']),
    (u'庚一 小廟管轄', [u'微型', u'未滿四人', u'移轉管轄', u'服滿別住']),
    (u'庚二 邊地尼數', [u'二部僧', u'尼僧二十', u'不足二十', u'邊地']),
    (u'庚三 行治切結', [u'切結', u'自願中止', u'隨時中止', u'非法拘禁']),
    (u'庚四 與學身分', [u'與學比丘', u'志工', u'保險', u'法人']),
    (u'辛一 醫療代償', [u'代償', u'墊付', u'瞻病', u'醫藥']),
    (u'辛二 數位勘驗', [u'伺服器原始紀錄', u'實名', u'IP', u'設備']),
    (u'壬  接收羯磨', [u'受訴聲請', u'接收道場', u'白二羯磨裁定']),
]

for tag, keys in CASES:
    print(u'\n══ %s' % tag)
    for k in keys:
        hits = [i + 1 for i, l in enumerate(LINES) if k in l]
        in45 = [n for n in hits if H4 and H4 < n - 1 < (H6 or len(LINES))]
        print(u'  %-14s 全書 %2d 見｜四・五章 %2d%s' % (
            k, len(hits), len(in45),
            u'｜例 L%d' % in45[0] if in45 else (u'｜例 L%d' % hits[0] if hits else u'｜0 見')))

print(u'\n══ 語料核據（卷三十七・覆藏犍度與四種僧物之目）')
for k in [u'算入', u'應行十五日', u'不知犯', u'後知不覆藏', u'現前现前', u'常住常住',
          u'十方常住', u'亡僧', u'轻物']:
    print(u'  %-12s 語料 %d 見' % (k.encode('unicode_escape').decode(), V.count(k)))
