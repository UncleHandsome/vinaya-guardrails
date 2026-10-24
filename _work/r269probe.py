# -*- coding: utf-8 -*-
"""269 輪・量一：外路第四報告『四大維度八項』逐條對**今冊 ver39** 與**舊冊 ver38** 之實況。

法源：[[verify-audit-lists-against-source]]——**整份清單可能對舊版而發**，逐條先量今檔並寫明版次差。
      本報告八處標『Ver 38』三處標『Ver 38/39』，故ver38 之數列必並列。
用法：python -X utf8 _work/r269probe.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME39 = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
          and u'列印' not in q][0]
NAME38 = [q for q in os.listdir(ROOT) if q.startswith(u'ver38') and q.endswith(u'.md')
          and u'列印' not in q]
BOOK = io.open(os.path.join(ROOT, NAME39), encoding=u'utf-8-sig').read()
OLD = NAME38[0] if NAME38 else None
v38 = io.open(os.path.join(ROOT, OLD), encoding=u'utf-8-sig').read() if OLD else u''
print(u'今冊 %s｜舊冊 %s' % (NAME39[:22], OLD[:22] if OLD else u'查無'))
L = BOOK.split(u'\n')


def chap_of(i):
    ch = u'卷首'
    for k, l in enumerate(L[:i + 1]):
        m = re.match(u'^# (第.{1,3}章|結語|終卷|附錄.)', l)
        if m:
            ch = m.group(1)
    return ch


def where(kw, limit=6):
    out = []
    for i, l in enumerate(L):
        if kw in l:
            out.append((i + 1, chap_of(i), l.strip()[:70]))
        if len(out) >= limit:
            break
    return out


ITEMS = [
    (u'一之1・括號四制（凡例第六節）', [u'四制', u'六角', u'括號', u'［', u'〔◈', u'標簽']),
    (u'一之2・教誡分流碼', [u'分流碼', u'年號·序號', u'2026', u'登錄於公共日誌']),
    (u'一之3・解耦之濫', [u'解耦', u'雙軌解耦', u'Decoupling']),
    (u'二之4・實質受益人／UBO', [u'實質受益人', u'UBO', u'Ultimate Beneficial', u'穿透']),
    (u'二之5・甲乙丙三級與除偏鏡', [u'甲級', u'乙級', u'丙級', u'以丙代甲', u'除偏鏡', u'臨濟四奪']),
    (u'三之6・29 則複統攝深水案', [u'29 則', u'二十九則', u'複統攝', u'深水', u'稱重法式']),
    (u'四之7・終局裁決存檔卡一式三份', [u'一式三份', u'法裁', u'存檔卡', u'[ ]', u'☐', u'親簽']),
    (u'四之8・自省記錄無證據能力', [u'自省記錄', u'證據能力', u'修行日記', u'觀心自照卡', u'日記', u'禪修筆記']),
    (u'＊報告自報之數（115 則／100）', [u'一百則', u'115', u'102']),
]
for tag, kws in ITEMS:
    print(u'\n▶ %s' % tag)
    for kw in kws:
        n39, n38 = BOOK.count(kw), v38.count(kw)
        w = where(kw, 2)
        print(u'   「%s」今 %-4d 舊 %-4d %s' % (kw, n39, n38,
              u'｜' + u'；'.join(u'L%d(%s)：%s' % x for x in w)[:136] if w else u''))
