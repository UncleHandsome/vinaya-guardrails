# -*- coding: utf-8 -*-
"""第 69 輪・丁刀：《摩奴法典》之引形歸制（去 Markdown 斜體・迎回舊章『非逐字』之如實標記）。
病：新稿作「法典之義如此：*女子幼年從父…自主。*」——以 Markdown 斜體冒充引文，
    既落單星號（`starbal` 行級紅），又把『通說之譯』寫成似逐字；舊章此處明文『（非逐字）』，乃第 56 輪
    『未經逐字覆核者不掛引號』之終制，換章不可佚。治法全句自備檔 .bak69a 截出，不假重打。
用法：python -X utf8 _work/hlfix69d.py [--go]
"""
import os as _hp_os, sys as _hp_sys
_hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__))))
import hulan_path as HP
import hashlib
import io
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
BAK = HP.bakpath("69d")
SRC_BAK = HP.bakpath("69a")                 # 入冊前之本：舊第十二章尚在其內
GO = u"--go" in sys.argv

old = io.open(SRC_BAK, encoding="utf-8", newline=u"").read().split(u"\r\n")
lead = [l for l in old if u"《摩奴法典》" in l and u"法典之義如此" in l]
assert len(lead) == 1, u"舊章之『法典之義』行見 %d 處" % len(lead)
QUOTE = [l for l in old if l.startswith(u"> 女子幼年從父")]
assert len(QUOTE) == 1, u"舊章之引框行見 %d 處" % len(QUOTE)
TAG = lead[0][lead[0].index(u"（今依其通說"):]
assert TAG.startswith(u"（今依其通說譯為漢言，非逐字）"), u"如實標記之形異：%r" % TAG[:30]
Q = QUOTE[0][2:].rstrip()
assert u"。" not in Q[:-1], u"引框行之內有句號，形制異：%r" % Q[-20:]

raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert raw.count(u"\r") == raw.count(u"\n") == raw.count(u"\r\n"), u"入口 CRLF 已傷"
L = raw.split(u"\r\n")
N0, sha0 = len(L), hashlib.sha256(raw.encode("utf-8")).hexdigest()

a = [i for i, l in enumerate(L) if l.startswith(u"在古印度的婆羅門教法典")]
assert len(a) == 1, u"今章之『法典之義』行見 %d 處" % len(a)
i = a[0]
assert L[i].count(u"*") == 2 and L[i].endswith(u"*"), u"target 之斜體形不认得：%r" % L[i][-24:]
NEW = [u"在古印度的婆羅門教法典（如著名的《摩奴法典》）中，女性是完全沒有獨立人格與法律權利的"
       u"「附屬品」。法典之義如此" + TAG + u"：  ", u"> " + Q]
L[i:i + 1] = NEW
print(u"  L%-5d 一行斜體 → 兩行（標記＋引框）：%s" % (i + 1, NEW[0][:70]))
print(u"                              %s" % NEW[1])
for k in (i, i + 1):
    assert L[k].count(u"*") % 2 == 0, u"仍落單星號 L%d" % (k + 1)

# 貳・副標題之『（上篇）（下篇）』歸舊式：一 H1 只配一枚 H2（第 68 輪已裁此形，全書今唯第十一章合式）。
#     新稿係兩篇分寫，故篇名各帶標記；目錄之章條向來只作『——古印度社會處境與女性心理防護』，
#     篇名留於正文即與目錄相左，遂除之；『深度案例解碼（上）（下）』兩節題自足，讀者不失其界。
UP = u"## ——古印度社會處境與女性心理防護（上篇）"
DN = u"## ——古印度社會處境與女性心理防護（下篇）"
u_, d_ = [k for k, l in enumerate(L) if l == UP], [k for k, l in enumerate(L) if l == DN]
assert len(u_) == 1 and len(d_) == 1, u"上篇 %d・下篇 %d（欲各 1）" % (len(u_), len(d_))
L[u_[0]] = UP[:-4]
print(u"  L%-5d 除『（上篇）』→ %s" % (u_[0] + 1, L[u_[0]]))
j = d_[0]
assert L[j - 2] == u"---" and L[j - 1] == u"" and L[j + 1] == u"" and L[j + 2] == u"---" \
    and L[j + 3] == u"" and L[j + 4].startswith(u"### 六、"), u"下篇界之形不认得：%r" % [L[j - 2:j + 5]]
del L[j:j + 4]                           # 『下篇題・空・---・空』四行削去，前之『---・空』留為界
assert L[j - 2] == u"---" and L[j - 1] == u"" and L[j].startswith(u"### 六、"), \
    u"併界之後形異：%r" % [L[j - 2:j + 1]]
print(u"  L%-5d 除『（下篇）』一行並併其後之分隔線（净減 4 行）" % (j + 1))

assert len(L) == N0 + 1 - 4, u"行數之變非 +1-4：%d→%d" % (N0, len(L))
txt = u"\r\n".join(L)
assert txt.count(u"\r") == txt.count(u"\n") == len(L) - 1, u"CRLF 變形"
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
if not os.path.exists(BAK):
    shutil.copy2(BOOK, BAK)
with open(BOOK, "wb") as fh:
    fh.write(txt.encode("utf-8"))
chk = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert chk == txt, u"回讀不符"
print(u"已寫檔｜行數 %d→%d｜sha %s→%s｜備份 %s" % (
    N0, len(L), sha0[:12], hashlib.sha256(chk.encode("utf-8")).hexdigest()[:12], os.path.basename(BAK)))
