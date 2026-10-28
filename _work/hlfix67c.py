# -*- coding: utf-8 -*-
"""第 67 輪・丙：兩處引號內之無標削語補『……』，一处改回已覆核之全形（引文形制之嚴）。"""
import os as _hp_os, sys as _hp_sys
_hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__))))
import hulan_path as HP
import hashlib
import io
import os
import re
import shutil
import sys

sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.abspath(__file__)))
import _tk

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
BAK = BOOK + ".bak67d"
GO = "--go" in sys.argv
PUNC = re.compile(u"[，、；：！？「」『』（）()《》〈〉·．。\\-—…﹑＂\"'*＿　\\s]")

raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert raw.count(u"\r") == raw.count(u"\n") == raw.count(u"\r\n"), u"入口 CRLF 已傷"
L = raw.split(u"\r\n")
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()

FIX = [
    (u"甲 補削語記號", u"雙方長老共同承認「多犯眾戒、亦作亦說」", u"雙方長老共同承認「多犯眾戒……亦作亦說」"),
    (u"乙 歸全形", u"若兩位當事人能夠「現前好言教語，如法如律」", u"若兩位當事人能夠「現前好言教語，如法、如毘尼、如佛所教」"),
]
for tag, old, new in FIX:
    hits = [i for i, l in enumerate(L) if old in l]
    assert len(hits) == 1, u"%s｜命中 %d（欲 1）：%s" % (tag, len(hits), old[:24])
    L[hits[0]] = L[hits[0]].replace(old, new)
    for frag in re.split(u"……", new[new.find(u"「"):new.find(u"」", new.find(u"「"))]):
        nb = _tk.norm(PUNC.sub(u"", frag))
        assert len(nb) < 4 or nb in _tk.VINAYA, u"%s｜補後之『%s』語料無連寫" % (tag, frag[:20])
    print(u"  %s L%-5d ✓（分段俱連寫）" % (tag, hits[0] + 1))

txt = u"\r\n".join(L)
assert txt.count(u"\r") == txt.count(u"\n") == len(L) - 1, u"CRLF 變形"
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
assert not os.path.exists(BAK) or io.open(BAK, encoding="utf-8", newline=u"").read() == raw, u"備份不同本"
if not os.path.exists(BAK):
    shutil.copy2(BOOK, BAK)
with open(BOOK, "wb") as fh:
    fh.write(txt.encode("utf-8"))
chk = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert chk == txt, u"回讀不符"
print(u"已寫檔｜sha %s→%s｜備份 %s" % (
    sha0[:12], hashlib.sha256(chk.encode("utf-8")).hexdigest()[:12], os.path.basename(BAK)))
