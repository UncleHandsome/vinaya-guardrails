# -*- coding: utf-8 -*-
"""第 57 輪・己：案例出處之『篇聚名』歸正（依本地語料實位，非依外來說）。
病：新稿與十線地圖以『結界／和尚／瞻病／授戒犍度』為篇題——本地《四分律》二十犍度無此四目；
    另兩處歸屬與語料所居不符（案例十二之『五法應授人大戒』實在雜犍度；案例十九之象師黑石蜜緣起實在戒本三十捨墮法）。
證：見 _work/hlkan57.py 之輸出（片段→檔→行→其上篇題）。
用法：python -X utf8 _work/hlpin57.py [--go]
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert raw.count(u"\r") == raw.count(u"\n"), u"入口 CRLF 已傷"
L = raw.split(u"\r\n")

# （正本页，舊串，新串，語料之證）
FIX = [
    (3959, u"【案發現場（結界犍度）】", u"【案發現場（說戒犍度）】",
     u"31-37 檔 L229『聽結界白二羯磨』，上下 L223-233 俱說戒／布薩之制"),
    (4089, u"【案發現場（和尚犍度、受戒犍度）】", u"【案發現場（受戒犍度）】",
     u"31-37 檔 L162『自今已去制和尚法如是』在受戒犍度"),
    (4106, u"【案發現場（受戒犍度）】", u"【案發現場（雜犍度）】",
     u"50-60 檔 L1495『調順無畏堪能語言…應授人大戒』，其上篇題『雜揵度之三』"),
    (4217, u"【案發現場（藥犍度）】", u"【案發現場（三十捨墮法·七日藥戒）】",
     u"01-10 檔 L1354 象師五百乘車之緣起（藥犍度所記者乃私呵居士版，文異）"),
    (4254, u"【案發現場（受戒犍度、瞻病犍度）】", u"【案發現場（受戒犍度、雜犍度）】",
     u"50-60 檔 L957『瞻病者厭患…波羅夷』，其上篇題『雜揵度之三』"),
    (4333, u"【案發現場（受戒犍度、藥犍度）】", u"【案發現場（藥犍度）】",
     u"38-49 檔 L831『先尼楗外道…如取泉水』與『汝為國之大臣』俱在藥揵度之一段"),
    (511, u"| 第十一章案例二十四 | 瞻病犍度 |", u"| 第十一章案例二十四 | 衣犍度 |",
     u"38-49 檔 L582『有五法看病人不應取病人衣物』，其上篇題『衣揵度之三』"),
    (512, u"| 第十一章案例二十五 | 瞻病犍度 |", u"| 第十一章案例二十五 | 藥犍度 |",
     u"38-49 檔 L773 蘇卑割髀肉，其上篇題『藥揵度之一』"),
    (573, u"| 第十一章案例十二 | 授戒犍度 |", u"| 第十一章案例十二 | 雜犍度 |",
     u"同 L4106：『五法應授人大戒』在雜揵度"),
    (574, u"| 第十一章案例十一 | 和尚犍度 |", u"| 第十一章案例十一 | 受戒犍度 |",
     u"同 L4089：和尚法在受戒犍度"),
    (590, u"| 第十一章案例四 | 結界犍度 |", u"| 第十一章案例四 | 說戒犍度 |",
     u"同 L3959"),
]

for n, old, new, why in FIX:
    c = L[n - 1].count(old)
    assert c == 1, u"L%d 錨命中 %d：%s" % (n, c, old[:30])
    L[n - 1] = L[n - 1].replace(old, new)
    print(u"  L%-5d %s → %s" % (n, old[:34], new[:34]))
    print(u"        證：%s" % why)
txt = u"\r\n".join(L)
assert txt.count(u"\r") == txt.count(u"\n"), u"出口 CRLF 變形"
for bad in [u"結界犍度", u"和尚犍度", u"瞻病犍度", u"授戒犍度"]:
    assert bad not in txt, u"猶殘留：%s" % bad
print(u"歸正 %d 處｜四名目俱不復見於冊" % len(FIX))
if u"--go" in sys.argv:
    io.open(BOOK, "w", encoding="utf-8", newline=u"").write(txt)
    print(u"已寫檔")
else:
    print(u"（乾跑：加 --go 始寫）")
