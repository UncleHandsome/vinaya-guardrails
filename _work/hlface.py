# -*- coding: utf-8 -*-
"""護欄書之印面與結構度量器（第四十一輪立，代歷輪之手算）。
   口徑：源檔 CJK（含附錄／不含附錄兩式）；行數＝CRLF 切分之元素數；CR／LF 計數須相等；
   案例＝『#### 案例』行；指針＝『第N章案例M』式之引針（與 apxchk 之『書中案例數』同口徑）。
   用法：python -X utf8 _work/hlface.py [--go]（--go 即把所測寫入 _work/hlface.last，供下輪對勘）
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
import os
LAST = os.path.join(os.path.dirname(os.path.abspath(__file__)), u"hlface.last")
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
L = raw.split(u"\r\n")
CJK = re.compile(u"[一-鿿]")     # 與 facecount.py（母數冊）同一口徑，歷輪之數方可比
REF = re.compile(u"第([〇零一二三四五六七八九十百]{1,3})章案例([〇零一二三四五六七八九十百]{1,3})")
ai = [i for i, s in enumerate(L) if s.startswith(u"# 附錄")]
assert len(ai) == 1, u"附錄起點 %d 處" % len(ai)
allh = sum(len(CJK.findall(s)) for s in L)
body = sum(len(CJK.findall(s)) for s in L[:ai[0]])
ncase = sum(1 for s in L if s.startswith(u"#### 案例"))
nref = len(REF.findall(raw))
cr, lf = raw.count(u"\r"), raw.count(u"\n")
s = u"行 %d｜CR %d LF %d｜案例 %d｜引針字樣 %d（全檔凡『第N章案例M』，含附錄・指針之數以 apxchk 為法源）｜印面漢字 含附錄 %d／不含附錄 %d" % (
    len(L), cr, lf, ncase, nref, allh, body)
assert cr == lf == len(L) - 1, u"CRLF 變形"
print(s)
try:
    prev = io.open(LAST, encoding="utf-8").read().strip()
except IOError:
    prev = u""
if prev:
    print(u"上輪：%s" % prev)
    print(u"今昔之差：行 %+d｜含 %+d｜不含 %+d" % (
        len(L) - int(re.search(u"行 (\\d+)", prev).group(1)),
        allh - int(re.search(u"含附錄 (\\d+)", prev).group(1)),
        body - int(re.search(u"不含附錄 (\\d+)", prev).group(1))))
if u"--go" in sys.argv:
    io.open(LAST, "w", encoding="utf-8", newline=u"").write(s + u"\n")
    print(u"已記 _work/hlface.last")
