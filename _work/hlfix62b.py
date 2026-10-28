# -*- coding: utf-8 -*-
"""第 62 輪・刀二（自抓，非外路所報）：兩處『粗體＋引號』之律文宣稱有**無標之脫字**。
款①之约：引號與粗體相合者，文字一皆出自漢譯《四分律》，省字須標『……』。今以全書式樣掃（59 段無據）
落網兩段確係律句而脫字：
  L5378 書作「諸比丘尼勸汝，而不從語，遂令命終。」——律文實作「諸比丘尼勸汝而不從語瞻視遂令命終」，
        脫『瞻視』二字，而那正是『不作為』之罪名所在（不瞻視＝不照護），脫之反弱其論。
  L5955 書作「一下刀，一波逸提；一匝纏，一波逸提。」——律文實作「不白眾使男子破一下刀一波逸提
        若裹時一匝纏一波逸提」，脫『若裹時』三字，對仗遂成自造。
治：俱補回原字（只加不減，義理不動）。自證：補後兩段必於語料連寫・行數/CRLF 不動・備份 .bak62b。
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
BAK = BOOK + u".bak62b"
NV = re.sub(u"[^一-鿿]", u"", _tk.norm(_tk.VINAYA))
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()
assert raw.count(u"\r") == raw.count(u"\n")
L = raw.split(u"\r\n")
PAIR = [(u"**「諸比丘尼勸汝，而不從語，遂令命終。」**",
         u"**「諸比丘尼勸汝而不從語，瞻視，遂令命終。」**"),
        (u"**「一下刀，一波逸提；一匝纏，一波逸提。」**",
         u"**「一下刀，一波逸提；若裹時，一匝纏，一波逸提。」**")]
for old, new in PAIR:
    ns = [i for i, x in enumerate(L) if old in x]
    assert len(ns) == 1, u"靶命中 %d（須 1）：%s｜%s" % (len(ns), [n + 1 for n in ns], old[:22])
    seg = new.strip(u"*").strip(u"「」")
    t = re.sub(u"[^一-鿿]", u"", _tk.norm(seg))
    assert t in NV, u"補後仍不連寫（口徑須再核）：%s" % seg[:26]
    L[ns[0]] = L[ns[0]].replace(old, new)
    print(u"L%-5d 補字 ✓｜舊 %d 字 → 新 %d 字" % (ns[0] + 1, len(old), len(new)))
new_raw = u"\r\n".join(L)
if not os.path.exists(BAK):
    shutil.copyfile(BOOK, BAK)
io.open(BOOK, "w", encoding="utf-8", newline=u"").write(new_raw)
chk = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert chk == new_raw and chk.count(u"\r") == chk.count(u"\n") == len(L) - 1
print(u"行數：%d（不變）・字數 %+d" % (len(L), len(new_raw) - len(raw)))
print(u"SHA：%s → %s（備份 %s）" % (sha0[:12], hashlib.sha256(new_raw.encode("utf-8")).hexdigest()[:12],
                                    os.path.basename(BAK)))
