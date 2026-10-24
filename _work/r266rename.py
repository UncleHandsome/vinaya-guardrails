# -*- coding: utf-8 -*-
"""266 輪・刀一：『某某令』之命題降溫（對讀者曰警策・對事曰禁約）＋『出院儀軌四重奏』歸律語。

判準（已立為 v39chk 第 26 目）：
  · 主詞是**作者叮囑讀者**者 ➔ 『警策』（中斷令→暫止警策・消磁令→消磁警策・封存令→封存警策）；
  · 主詞是**僧團對事所立之制**者 ➔ 『禁約』（叢林原生語，《清規》有『禁約』一門），不作官府『禁令』；
  · 只改**專名**（16 種命題及其援引），文中泛指之『預防性禁令』『靜態禁令』等普通名詞不較——
    尺之單位須與病之單位同寬（220 輪之誡），名之別不在字之別。
用法：python -X utf8 _work/r267rename.py         # 乾跑
      python -X utf8 _work/r267rename.py apply
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')

# 一・十六種『令』之專名（含其目錄援引，故全域取代）
REN = [
    (u'急診即刻中斷令', u'急診即刻暫止警策'),
    (u'一道中斷令', u'一道暫止警策'),
    (u'結案消磁令', u'結案消磁警策'),
    (u'診斷詞彙封存令', u'診斷詞彙封存警策'),
    (u'口業封閉令', u'口業封閉禁約'),
    (u'反靈性煤氣燈操縱防護令', u'反靈性煤氣燈操縱防護禁約'),
    (u'反靈性煤氣燈操縱言辭禁令', u'反靈性煤氣燈操縱言辭禁約'),
    (u'受暴創傷知情阻卻與絕對盤詰禁令', u'受暴創傷知情阻卻與絕對盤詰禁約'),
    (u'受暴創傷知情禁令', u'受暴創傷知情禁約'),
    (u'盤詰生理反射之絕對禁令', u'盤詰生理反射之絕對禁約'),
    (u'絕對盤詰禁令', u'絕對盤詰禁約'),
    (u'數位冷暴力三大禁令', u'數位冷暴力三大禁約'),
    (u'四大言辭禁令', u'四大言辭禁約'),
    (u'二諦禁止逾越禁令', u'二諦不得逾越禁約'),
    (u'轉軌為遮戒禁令', u'轉軌為遮戒禁約'),
    (u'立法預防性禁令', u'立法預防性禁約'),
    (u'立法預防禁令', u'立法預防禁約'),
    (u'最高禁令', u'最高禁約'),
]
# 二・『出院儀軌四重奏』歸律語（四事＝出罪還淨四事）
REN += [
    (u'#### 十至十三、出罪復權之「出院儀軌四重奏」', u'#### 十至十三、出罪還淨四事'),
    (u'僧團依序執行**「出院儀軌四重奏」**：', u'僧團依序執行**『出罪還淨四事』**：'),
    (u'【出院儀軌四重奏（復權）】', u'【出罪還淨四事（復權）】'),
    (u'滿摩那埵位保護、出院儀軌四重奏、', u'滿摩那埵位保護、出罪還淨四事、'),
]

t = io.open(BOOK, encoding=u'utf-8-sig').read()
bad = []
for old, new in REN:
    n = t.count(old)
    if not n:
        bad.append((old, n))
print(u'合 %d 項' % len(REN))
for old, new in REN:
    print(u'  ×%d｜%s ➔ %s' % (t.count(old), old[:30], new[:30]))
if bad:
    print(u'!! 未命中：%s' % bad)
    sys.exit(2)
if u'apply' not in sys.argv:
    print(u'乾跑，未寫入。')
    sys.exit(0)
for old, new in REN:
    t = t.replace(old, new)
io.open(BOOK, 'w', encoding='utf-8', newline=u'').write(t)
chk = io.open(BOOK, encoding=u'utf-8-sig').read()
for old, _n in REN:
    assert chk.count(old) == 0, old
print(u'已寫入，回讀相符；剩『令』命題：見尺。')
