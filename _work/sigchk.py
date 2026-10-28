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

# ── 丙軸（第 56 輪・學術嚴謹版）：題詞之『形制』須與『歸屬』同 ─────────────────
# 凡例款①自約：引號與粗體相合者＝漢譯《四分律》原句。故章首題詞若作 `> **「…」 **`
# 而署名行所指非《四分律》（道宣、元照、弘一、法句經、摩奴法典、南傳諸典…），
# 即是以形制作不實之宣稱——舊甲軸漏此，因題詞級駢文含『。』『：』而被式樣閘擲棄。
BIQ = re.compile(u"^> \\*\\*「(.+?)」\\*\\*")
QOT = re.compile(u"^> 「(.+?)」")
SIGN = re.compile(u"^> *——(.*)$")
LV_SRC = re.compile(u"《四分律》|波羅夷法|僧殘法|犍度|五百集法毘尼|集比丘僧|呵責")
CANON = re.compile(u"T\\d{2,4}n\\d{3,4}")
bing = []
for n in range(len(V)):
    s = V[n].strip()
    if u"〔本書括旨〕" in s:                                   # 標籤不入印面（第 56 輪再制）
        bing.append((n + 1, u"印面殘留〔本書括旨〕標籤", s[:40]))
        continue
    m = BIQ.match(s) or QOT.match(s)
    if not m:
        continue
    sign = None
    for k in range(n + 1, min(n + 4, len(V))):
        t = V[k].strip()
        if not t or t == u">":
            continue
        ms = SIGN.match(t)
        if ms:
            sign = ms.group(1)
        break
    if sign is None:
        continue
    if u"未及逐覆" in sign and CANON.search(sign):
        bing.append((n + 1, u"自相矛盾：標『未及逐覆』卻附大正藏編號", sign[:44]))
    elif BIQ.match(s) and not LV_SRC.search(sign):
        bing.append((n + 1, u"粗體＋引號（款①專留律文）而署名非《四分律》", sign[:44]))
    elif QOT.match(s) and not LV_SRC.search(sign) and not CANON.search(sign):
        bing.append((n + 1, u"引號＋他師署名而無大正藏編號（未覆核不得掛號）", sign[:44]))

# ── 丁軸（第 56 輪附六）：正文之『括某書之旨』須可驗 ────────────────────
# 『本書括《X》之旨』是對 X 書內容的宣稱；本地語料唯漢譯《四分律》，他書無從證——
# 故此类宣稱一律視同未證（庚軸只列『須人工核』，不判真偽）。今制：改約為
# 『本書效古德語氣自為之文，非其書之文』——語氣仿作可驗，內容對應不可驗。
DING = []
KUO = re.compile(u"括《([^》]+)》之旨|本書括其旨|括其旨曰")
for n, t in enumerate(V):
    for m in KUO.finditer(t):
        book = m.group(1) or u"（未指書）"
        if u"四分律" not in book:
            DING.append((n + 1, book, t.strip()[:44]))

print(u"丁（正文『括他書之旨』——本地無從證，須改『自為之文』）：%d 處" % len(DING))
for n, bk, t in DING[:8]:
    print(u"  L%-5d 所稱之書：%s ｜ %s" % (n, bk, t))
print(u"丙（題詞形制與聲明不合：標籤入印面／款①形制掛他師／未覆核而附號）：%d 處" % len(bing))
for n, s, g in bing[:10]:
    print(u"  L%-5d %s ｜ 署：%s" % (n, s, g))
print(u"乙（無署名・凡例新款涵蓋，只報不判）：%d 處" % len(yi))
print(u"甲（同句有署名／出處而語料不連寫）：**%d 處**" % len(jia))
if jia or u"-v" in sys.argv:
    for n, s, t in jia:
        print(u"  L%-5d %s ｜ %s" % (n, s, t[:78]))
print(u"判：甲須 0・丙須 0・丁須 0（丙丁皆『形制即聲明』之檢，第 56 輪立）｜今 %s"
      % (u"合格" if not (jia or bing or DING) else u"不合格"))
sys.exit(1 if (jia or bing or DING) else 0)
