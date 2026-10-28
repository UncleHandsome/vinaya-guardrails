# -*- coding: utf-8 -*-
"""第 63 輪・刀：外路第二十六報之真病二事（名相衍字・題記黏合）。
  一・真病（但外路之方亦誤）：第八章案例三 L2342 括注之第七開緣作『沙門果食時』——
      本地《四分律》兩處累計之『餘時者』俱作『**沙門施食時**』：
        比丘：「餘時者病時作衣時施衣時道行時乘船時大眾集時沙門施食時此是時」
        比丘尼：「…大會時沙門施食時此是時」
      語料『沙門果食時』0 見、『沙門食時』亦 0 見（外路所擬之方同無據）；『果食』在律中別指
      佉闍尼食之『根食乃至果食油食』，與此無關。故從律改『沙門施食時』。
  五・真病（題記黏合）：第二章 L795-798、第三章 L951-954 之『「」＋署名＋冊號』題記之下，
      同段引框內又接一行本書自製之駢語，讀者必併歸古德——正犯 56 輪終制。
      書中已有成例（L1088『此段乃本書效古德語氣自為之文…』），故只補標記，不動其文。
擯回：二・第十六章之註已於 60 輪改畢（報告所引乃舊文，其『偷蘭難陀』式字形亦證對的是舊檔）；
      三・第十二章『#### 4. 前四波羅夷』並非跳軌——其上是 H3『### 三、 解碼比丘尼八波羅夷』之
          1..4 解讀列，案例一～四在下一節『### 四、 深度案例解碼』之下；『#### N.』乃全書通行
          之式（43 處），非此處獨異。四・第十四章噉蒜戒歸位屬案例歸組＝案四，牽 22 案編號與全鏈指針，候裁。
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
import _tk                                            # noqa: E402

BOOK = os.path.join(HERE, [f for f in os.listdir(HERE)
                           if f.startswith(u"佛陀的護欄") and f.endswith(u".txt")][0])
BAK = BOOK + u".bak63a"
NV = re.sub(u"[^" + chr(0x4E00) + u"-" + chr(0x9FFF) + u"]", u"", _tk.norm(_tk.VINAYA))
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
        log.append(u"%-12s L%-5d｜%s" % (tag, n + 1, L[n][:62]))


# ── 律據自證：新詞須在語料連寫，舊詞須不在 ──────────────────────────────
def nq(s):
    return re.sub(u"[^" + chr(0x4E00) + u"-" + chr(0x9FFF) + u"]", u"", _tk.norm(s))


assert nq(u"沙門施食時") in NV, u"律據不立（沙門施食時不在語料）"
assert nq(u"沙門果食時") not in NV and nq(u"沙門食時") not in NV, u"舊詞／外路方竟在語料，口徑須再核"
rep(u"名相·歸律", u"大眾集時、沙門果食時", u"大眾集時、沙門施食時")

# ── 題記黏合：補『本書效古德語氣』之標記（依 L1088 成例）────────────────
rep(u"題記·標本書語", u"> 性惡本重，遮過附生；",
    u"> （本書效古德語氣自為之文，非道宣之句）性惡本重，遮過附生；")
rep(u"題記·標本書語", u"> 譬如國王邊城，牢固險阻，",
    u"> （本書效《城喻經》語氣自為之文，非經之句）譬如國王邊城，牢固險阻，")
# 自證（口徑須對）：病在『署名行之後又接本書語而同在一引框內』——獨立之本書題記無從誤會，不在此限。
bad = []
i = 0
while i < len(L):
    if not L[i].startswith(u"> "):
        i += 1
        continue
    j = i
    while j < len(L) and L[j].startswith((u"> ", u">")):
        j += 1
    blk = L[i:j]
    k = next((x for x, t in enumerate(blk) if t.lstrip(u"> ").startswith(u"——")), None)
    if k is not None:
        for t in blk[k + 1:]:
            s = t.lstrip(u"> ").strip()
            if len(s) > 20 and not s.startswith(u"（本書") and not s.startswith(u"（"):
                bad.append(u"L%d｜%s" % (i + 1 + blk.index(t), s[:40]))
    i = j
assert not bad, u"署名題記之下尚有未標之本書附語：%s" % bad
print(u"題記黏掃：全書引框逐框核（署名行之後不得有未標之本書語）・病 0 ✓")

new_raw = u"\r\n".join(L)
if not os.path.exists(BAK):
    shutil.copyfile(BOOK, BAK)
io.open(BOOK, "w", encoding="utf-8", newline=u"").write(new_raw)
chk = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert chk == new_raw and chk.count(u"\r") == chk.count(u"\n") == len(L) - 1
print(u"行數：%d（不變）・字數 %+d" % (len(L), len(new_raw) - len(raw)))
for z in log:
    print(u"  " + z)
print(u"SHA：%s → %s（備份 %s）" % (sha0[:12], hashlib.sha256(new_raw.encode("utf-8")).hexdigest()[:12],
                                    os.path.basename(BAK)))
