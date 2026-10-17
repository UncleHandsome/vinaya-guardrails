# -*- coding: utf-8 -*-
"""式樣歸屬尺（sigchk・第 49 輪立）：查「粗體＋引號」之逐字式樣是否對得上其歸屬。

法源：卷首【凡例】本書引文之四例之第一例——引號與粗體相合者＝本書標為律文原句之文。
口徑：取全書所有 「**X**」 與 **「X」** 之式樣（X 為 3～26 字、內不含 ：。），
      以 `_tk.norm` 查 X 是否為漢譯《四分律》語料之相連子串。
分類：甲＝同句另有署名或出處之跡（律師／祖師／《…》／阿含／曰／所稱…）——此類最壞，
          它把「某人說過此語」掛成逐字，須去式樣或加如實標記，故為硬檢（目標 0）。
      乙＝同句無署名——多為本書之戒名・喻名・術語・評語，由凡例新款之判別句涵蓋，只報不判。
用法：python -X utf8 _work/sigchk.py [-v]
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import os
import re
import sys

sys.path.insert(0, ".")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import _tk  # noqa: E402

BOOK = os.environ.get("HULAN_SRC") or (
    HP.SRC)
V = io.open(BOOK, encoding="utf-8", newline="").read().split("\r\n")
PAT = re.compile(u"「\\*\\*([^」\\n]{2,60})\\*\\*」|\\*\\*「([^」\\n]{2,60})」\\*\\*")
NAME = re.compile(u"律師|祖師|古德|先德|歷代|阿含|《|弘一|元照|道宣|律云|經云|所說|所稱|之言|曰|大師|論云|毘婆沙")
VERB = re.compile(u"[說言稱謂曰云]")

jia, yi, ok, ell = [], [], 0, 0
for n, t in enumerate(V):
    for m in PAT.finditer(t):
        s = m.group(1) or m.group(2)
        if len(s) < 3 or u"：" in s or u"。" in s:
            continue
        # 口徑須同 `hlchk` 戊：以「……」拼接之引文，其各段各自相連即合法（省略號不是錯）
        segs = [x.strip() for x in re.split(u"\\*\\*……\\*\\*|……", s)]
        segs = [x for x in segs if len(x) >= 3 and u"：" not in x and u"。" not in x]
        if len(segs) > 1:
            ell += 1
        hit = bool(segs) and all(_tk.VINAYA.find(_tk.norm(x)) >= 0 for x in segs)
        if hit:
            ok += 1
            continue
        (jia if NAME.search(t) else yi).append((n + 1, s, t))

print(u"式樣歸屬尺（sigchk）｜中用式樣者：語料相連 %d 處（其中 …… 拼接者 %d 處，分段核）" % (ok, ell))
print(u"乙（無署名・凡例新款涵蓋，只報不判）：%d 處" % len(yi))
print(u"甲（同句有署名／出處而語料不連寫）：**%d 處**" % len(jia))
if jia or u"-v" in sys.argv:
    for n, s, t in jia:
        print(u"  L%-5d %s ｜ %s" % (n, s, t[:78]))
print(u"判：甲類須為 0（此類把『某人說過』掛成逐字，是凡例款①所禁）｜今 %s" % (u"合格" if not jia else u"不合格"))
sys.exit(1 if jia else 0)
