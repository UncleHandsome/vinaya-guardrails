# -*- coding: utf-8 -*-
"""第 61 輪・刀：外路第二十四報之『自裁』二事（另四事候裁、一事已治於 60 輪）。
  一（P0・真病）第一章與第十七章之章首題記 36 字全同（L641／L6361，實測逐字相等）——
    第十七章第四節專論弘一大師『學戒先須明其制意』，其下又云「大師此語是全書的鑰匙」，
    故該句之家在第十七章；第一章乃無署名預支。治：第一章題記改本書語（不掛引號、不署名、
    不借他師之句——依 56 輪終制），第十七章一字不動。
  七（真病・語病）L1330「那一段（此段本書已見下文）」——『已見』與『下文』自相矛盾。
    實測其文全引於同章第四節 L1444（「### 四、 未制之前：佛陀為什麼不預先結戒」），
    故改為確指「其文全引於本章第四節」。
自證：兩靶各命中 1・改後全書無 36 字重出之題記（以題記行兩兩相比）・CRLF 等式・回讀合・
      備份 .bak61a＋SHA 可回退。
"""
import hashlib
import io
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BOOK = os.path.join(HERE, [f for f in os.listdir(HERE)
                           if f.startswith(u"佛陀的護欄") and f.endswith(u".txt")][0])
BAK = BOOK + u".bak61a"
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()
assert raw.count(u"\r") == raw.count(u"\n")
L = raw.split(u"\r\n")
log = []


def rep(tag, old, new, want=1):
    ns = [i for i, x in enumerate(L) if old in x]
    assert len(ns) == want, u"%s：命中 %d（須 %d）：%s" % (tag, len(ns), want, [n + 1 for n in ns][:6])
    for n in ns:
        L[n] = L[n].replace(old, new)
        log.append(u"%-14s L%-5d｜%s" % (tag, n + 1, L[n][:66]))


OLD1 = (u"> 學戒者，先須明其制意。若不知佛陀何以制此戒，則持戒流於形骸，"
        u"執事昧理，終無實益。  ")
NEW1 = (u"> 同一條戒，可以當規章背，也可以當判例讀。當規章背，讀到的是限制；"
        u"當判例讀，讀到的是那一樁事、那一個為什麼。本書通篇走第二條路。  ")
# 第一章題記：只動 L641（第一章 H1 之下），不動 L6361（第十七章）
ns1 = [i for i, x in enumerate(L) if x == OLD1]
assert len(ns1) == 2 and ns1[0] == 640, u"題記重出之實測：%s（須 L641 與 L6361）" % [n + 1 for n in ns1]
assert L[ns1[1]].strip() and u"學戒者" in L[ns1[1]], u"第二處非第十七章題記"
L[ns1[0]] = NEW1
log.append(u"%-14s L%-5d｜%s" % (u"題記·去撞車", ns1[0] + 1, NEW1[:60]))
assert [i for i, x in enumerate(L) if x == OLD1] == [ns1[1]], u"第十七章之題記被牽動"

rep(u"語病·確指", u"那一段（此段本書已見下文）", u"那一段（其文全引於本章第四節）")

# 全書題記互重之覆核：凡 > 起首之題記行，兩兩不得全同（署名／出處行「> ——…」不在此限，同典可屢引）
eps = [x for x in L if x.startswith(u"> ") and len(x.strip()) > 20 and not x.startswith(u"> 「")
       and not x.lstrip().startswith((u"> ——", u"> —", u"> （"))]
dup = {(a, b) for i, a in enumerate(eps) for b in eps[i + 1:] if a == b}
assert not dup, u"仍有重出之題記：%s" % [z[0][:40] for z in list(dup)[:2]]
print(u"題記互重覆核：%d 行入校・重出 0 ✓" % len(eps))

new_raw = u"\r\n".join(L)
if not os.path.exists(BAK):
    shutil.copyfile(BOOK, BAK)
io.open(BOOK, "w", encoding="utf-8", newline=u"").write(new_raw)
chk = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert chk == new_raw, u"回讀不合（疑半檔）"
assert chk.count(u"\r") == chk.count(u"\n") == len(L) - 1, u"CRLF 之計異"
print(u"行數：%d（不變）・字數：%d → %d（%+d）" % (len(L), len(raw), len(new_raw), len(new_raw) - len(raw)))
for z in log:
    print(u"  " + z)
print(u"SHA：%s → %s（備份 %s）" % (sha0[:12], hashlib.sha256(new_raw.encode("utf-8")).hexdigest()[:12],
                                    os.path.basename(BAK)))
