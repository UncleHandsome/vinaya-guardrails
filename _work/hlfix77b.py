# -*- coding: utf-8 -*-
"""第 77 輪・己刀：二不定法第 2 條之條文欄補足（新目⑥自逮之病，非外路所報）。
同丙丁之法：文取附錄（產生器之逐字法源），『』改「」以從書中成例，行尾硬換行一仍其舊；先自證連寫於語料。"""
import hashlib
import io
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "_work"))
import hulan_path as HP  # noqa: E402
import lane  # noqa: E402
import _simpmap  # noqa: E402

GO = u"--go" in sys.argv
raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
L = raw.split(u"\r\n")
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
errs = []
APX = next(i for i, s in enumerate(L) if s.startswith(u"# 附錄"))
CF = lane.corpus_flat()

st = None
rt = None
for i in range(APX, len(L)):
    if L[i].startswith(u"## ") and u"二不定" in L[i]:
        st = i
    elif st is not None and L[i].startswith(u"## "):
        break
    elif st is not None:
        m = re.match(u"^2\\. 「(.+?)」\\s*｜書中：", L[i])
        if m:
            rt = m.group(1).replace(chr(0x300E), chr(0x300C)).replace(chr(0x300F), chr(0x300D))
            break
if not rt:
    sys.exit(u"附錄查無二不定法第2條")
print(u"附錄全文（%d 字）：%s" % (len(rt), rt))
if lane.flat(rt) not in CF:
    sys.exit(u"補入之文非語料連寫，不可掛逐字")

hit = [i for i, s in enumerate(L) if u"**【不定法第2條 條文】：**" in s]
if len(hit) != 1:
    sys.exit(u"靶命中 %d" % len(hit))
i = hit[0]
old = L[i]
print(u"書中今形：%s" % old[:180])
if u"……" not in old:
    sys.exit(u"今行本無『……』")
new = old.split(u"：**")[0] + u"：** " + rt + old[len(old.rstrip()):]
L[i] = new
for c in set(rt):
    if c in _simpmap.MAP:
        errs.append(u"新文簡形 %s➔%s" % (c, _simpmap.MAP[c]))
now = u"\r\n".join(L)
for a, b in ((u"「", u"」"), (u"『", u"』")):
    if now.count(a) - now.count(b) != raw.count(a) - raw.count(b):
        errs.append(u"引號之衡已變 %s%s" % (a, b))
if len(L) != len(raw.split(u"\r\n")):
    errs.append(u"行數不應變")
print(u"改後：%s" % new[:200])
if errs:
    for e in errs:
        print(u"✗ " + e)
    sys.exit(1)
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
BK = HP.bakpath(u"77b")
io.open(BK, "wb").write(raw.encode("utf-8"))
out = u"\r\n".join(L)
for k in range(3):
    try:
        io.open(HP.SRC, "wb").write(out.encode("utf-8"))
        break
    except OSError as e:
        print(u"  寫檔重試 %d：%s" % (k + 1, e))
        time.sleep(2)
chk = io.open(HP.SRC, "rb").read().decode("utf-8")
print(u"已寫檔｜sha %s→%s｜回讀%s｜備份 %s" % (
    sha0, hashlib.sha256(chk.encode("utf-8")).hexdigest()[:12], u"全等" if chk == out else u"不等!",
    os.path.relpath(BK, ROOT)))
