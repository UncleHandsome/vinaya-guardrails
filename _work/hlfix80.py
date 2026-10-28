# -*- coding: utf-8 -*-
"""第 80 輪・換入作者新版十線地圖：舊塊之軀幹（H1 之下、末段之後）整段換為 _work/mp80_new.md。

形制不動者：H1 一行（「# 十線地圖　跨章合併閱讀指引」，目錄條與書籤之靶）、其前後之 `---`、
            十一個 H2 之題（新舊兩稿逐字相同）、目錄條之座（79 輪已還於尾聲之下）。
所換者唯軀幹：導言三段・十線之表與按語・附記・結語。

先自證（乾跑）：舊塊之首末錨、新稿之首末錨、新稿之表數與資料行、案名是否俱在戶口。
"""
import hashlib
import io
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import hulan_path as HP                                        # noqa: E402

GO = u"--go" in sys.argv
NEW = os.path.join(ROOT, "_work", "mp80_new.md")
raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
L = raw.split(u"\r\n")
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
N = io.open(NEW, encoding="utf-8").read().replace(u"\r\n", u"\n").split(u"\n")
while N and not N[-1].strip():
    N.pop()

errs = []
i0 = [i for i, s in enumerate(L) if s.startswith(u"# ") and u"十線地圖" in s]
i1 = [i for i in range(i0[0] + 1, len(L)) if L[i].startswith(u"# ")] if i0 else []
if len(i0) != 1:
    errs.append(u"H1『十線地圖』命中 %d（宜 1）" % len(i0))
elif not i1:
    errs.append(u"其後無 H1（【第一部】）")
if errs:
    for e in errs:
        print(u"✗ " + e)
    sys.exit(1)
a, b = i0[0], i1[0]
body = L[a + 2:b - 3]                       # 軀幹：H1 之空行後 → 末段（其後為 ''・'---'・''・次 H1）
head_a, tail_a = body[0], body[-1]
checks = [
    (L[a + 1].strip() == u"", u"H1 後非空行"),
    (head_a.startswith(u"以下十線不是新的一章"), u"舊塊之首非導言：%s" % head_a[:24]),
    (tail_a.startswith(u"十線之間必有大段重疊"), u"舊塊之末非結語：%s" % tail_a[:24]),
    (L[b - 3].strip() == u"" and L[b - 2].strip() == u"---", u"末段之後非『空行＋---』"),
    (N[0].startswith(u"以下十線不是新的一章"), u"新稿之首非導言：%s" % N[0][:24]),
    (N[-1].startswith(u"十線之間必有大段重疊"), u"新稿之末非結語：%s" % N[-1][:24]),
]
for ok, msg in checks:
    if not ok:
        errs.append(msg)
rows = [s for s in N if s.startswith(u"|") and not re.match(u"^\\|[\\s\\-:|]+\\|$", s)]
seps = [s for s in N if re.match(u"^\\|[\\s\\-:|]+\\|$", s)]
heads = [s for s in rows if u"書中位置" in s or u"想談的事" in s]
print(u"舊塊 L%d–L%d（H1 L%d・軀幹 %d 行）｜次 H1（第一部）L%d"
      % (a + 1, b, a + 1, len(body), b + 1))
print(u"新稿 %d 行｜表列 %d・分隔 %d・十線之表頭 %d・資料行 %d（含附記表 6 行）"
      % (len(N), len(rows), len(seps), len(heads), len(rows) - len(heads)))
print(u"新稿之 H2：%d 枚" % sum(1 for s in N if s.startswith(u"## ")))
if len(heads) != 11 or len(rows) - len(heads) != 86:
    errs.append(u"表之戶口不合：表頭 %d（宜 10）・資料行 %d（宜 80＋6）" % (len(heads), len(rows) - len(heads)))

if errs:
    for e in errs:
        print(u"✗ " + e)
    sys.exit(1)

out_L = L[:a + 2] + N + L[b - 3:]
print(u"── 接縫（前）：%s" % u" ｜ ".join(repr(x)[:22] for x in out_L[a:a + 3]))
print(u"── 接縫（後）：%s" % u" ｜ ".join(repr(x)[:22] for x in out_L[a + 2 + len(N) - 1:a + 2 + len(N) + 3]))
print(u"行數 %d → %d" % (len(L), len(out_L)))
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
BK = HP.bakpath(u"80a")
io.open(BK, "wb").write(raw.encode("utf-8"))
out = u"\r\n".join(out_L)
for k in range(3):
    try:
        io.open(HP.SRC, "wb").write(out.encode("utf-8"))
        break
    except OSError as e:
        print(u"  寫檔重試 %d：%s" % (k + 1, e))
        time.sleep(2)
chk = io.open(HP.SRC, "rb").read().decode("utf-8")
print(u"已寫檔｜sha %s→%s｜回讀%s｜備份 %s" % (
    sha0, hashlib.sha256(chk.encode("utf-8")).hexdigest()[:12],
    u"全等" if chk == out else u"不等!", os.path.relpath(BK, ROOT)))
