# -*- coding: utf-8 -*-
"""第 81 輪・外路第三十報之真病（十九處）：
   甲、條文框合併號之殘留（八枚）：『【第A、B條 條文】』之下唯首條之文，B 於同案另立單條標籤——
       標籤領不動它所宣的號。各改回首號。
   乙、疊字『與與』（二處，目錄與案例題同文）：『…三戒（第21、22、23條）與與比丘尼往來四戒…』
       ——第二個『與』是戒名之首字；改作頓號，與同章另一長題（『高床…、兜羅綿…』）之式一致。
"""
import hashlib
import io
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import hulan_path as HP                                        # noqa: E402

GO = u"--go" in sys.argv
raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
t = raw
REP = [
    (u"【第97、98條 條文】", u"【第97條 條文】"),
    (u"【第161～163條 條文】", u"【第161條 條文】"),
    (u"【第166、167條 條文】", u"【第166條 條文】"),
    (u"【第131～133條 條文】", u"【第131條 條文】"),
    (u"【第136、137條 條文】", u"【第136條 條文】"),
    (u"【第117、118條 條文】", u"【第117條 條文】"),
    (u"【第169、170條 條文】", u"【第169條 條文】"),
    (u"【第108～110條 條文】", u"【第108條 條文】"),
    (u"）與與比丘尼往來四戒", u"）、與比丘尼往來四戒"),
]
errs = []
for a, b in REP:
    n = t.count(a)
    print(u"%-24s 命中 %d → %s" % (a, n, b))
    if n == 0:
        errs.append(u"錨不中：%s" % a)
    t = t.replace(a, b)
if errs:
    sys.exit(1)
print(u"字數 %d → %d｜差 %d" % (len(raw), len(t), len(raw) - len(t)))
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
BK = HP.bakpath(u"81a")
io.open(BK, "wb").write(raw.encode("utf-8"))
for k in range(3):
    try:
        io.open(HP.SRC, "wb").write(t.encode("utf-8"))
        break
    except OSError as e:
        print(u"  寫檔重試 %d：%s" % (k + 1, e))
        time.sleep(2)
chk = io.open(HP.SRC, "rb").read().decode("utf-8")
print(u"已寫檔｜sha %s→%s｜回讀%s｜備份 %s" % (
    sha0, hashlib.sha256(chk.encode("utf-8")).hexdigest()[:12],
    u"全等" if chk == t else u"不等!", os.path.relpath(BK, ROOT)))
