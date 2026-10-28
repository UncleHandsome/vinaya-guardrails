# -*- coding: utf-8 -*-
"""第 76 輪・目錄之二刀（自裁定奪：第廿七報之真病二事）。
甲・十線地圖之目錄條自目錄末移至【第一部】之前——書中它在目錄之後、第一部之前，目錄列於末章之後乃序位倒置。
乙・目錄之末補「附錄　全戒本歷條總表」一條——書中实有 422 行之附錄而目錄不錄，今因產物層之定位器已有字級門
    （不以目錄頁誤中同名條），故可補；附錄之題不自新造，直接取書中 H1 之原形，免碼位之險。
自查：二條之文俱取自檔內既有行（不重打）；並與 `append_appendix` 之撤條樣式對合（它日 --undo 方削得乾淨）；
目錄條目之數・區間之界・引號之衡俱印前後。
"""
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
import _simpmap  # noqa: E402

GO = u"--go" in sys.argv
DING_ERR = [u"后", u"台", u"据", u"毁", u"与", u"强", u"办", u"关", u"个", u"让", u"从", u"众", u"万"]
raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
L = raw.split(u"\r\n")
BEFORE = list(L)
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
errs = []

dlo = next(i for i, s in enumerate(L) if s.startswith(u"# 【全書詳細目錄】"))
dhi = next(i for i in range(dlo + 1, len(L)) if L[i].startswith(u"# 十線地圖"))
apx = next(i for i, s in enumerate(L) if s.startswith(u"# 附錄"))
h1 = L[apx]
X_TEXT = h1[2:].strip()
print(u"附錄之題取自檔內 H1：%r" % X_TEXT)


def find(sub, note=u""):
    hit = [i for i, s in enumerate(L) if sub in s]
    if len(hit) != 1:
        errs.append(u"%s｜靶命中 %d：%s" % (note, len(hit), sub[:26]))
        return None
    touched.add(hit[0])
    return hit[0]


touched = set()
NEWTEXT = []
# ── 甲・十線地圖之目錄條：取原行、削於末、插於第一部之前
i_x = find(u"（前置於第一部之前，全書之路標）", u"十線目錄條")
if i_x is not None:
    line_x = L[i_x]
    assert line_x.startswith(u"* **"), u"十線目錄條之形制已變"
    del L[i_x]
    i_bu = find(u"### **【第一部", u"第一部部題")
    if i_bu is not None:
        L[i_bu:i_bu] = [line_x, u""]
        NEWTEXT.append((u"十線移至目錄之首", line_x))
        print(u"甲・十線條 L%d ➔ 移於部題前（原第 %d 條之次）" % (i_x + 1, i_bu + 1))
# ── 乙・附錄之目錄條：補於目錄之末（尾聲條之後）
i_ws = find(u"* 尾聲：願你心中有一座金剛城郭", u"尾聲條")
bullet = u"* **" + X_TEXT + u"**（兩部戒本歷條逐號登記，唯全本有之）"
if i_ws is not None:
    L[i_ws + 1:i_ws + 1] = [bullet]
    NEWTEXT.append((u"附錄入目錄", bullet))
    print(u"乙・補目錄條：%s" % bullet)
# 與 `append_appendix` 之撤條樣式對合（它日 --undo 始削此條）
src = io.open(os.path.join(ROOT, "_work", u"append_appendix.py"), encoding="utf-8").read()
m = re.search(u'startswith\\(u"(\\* [^"]+)"\\)', src)
patt = m.group(1) if m else u""
print(u"append_appendix 之撤條樣式：%r｜今條合之：%s" % (patt[:26], bullet.startswith(patt)))
if patt and not bullet.startswith(patt):
    errs.append(u"目錄條與撤條樣式不合（--undo 將削不淨）")

# ── 覆核
items = [s for s in L[dlo + 1:dhi + 2] if re.match(u"^\\s*[*\\-] ", s)]
items0 = [s for s in BEFORE[dlo + 1:dhi] if re.match(u"^\\s*[*\\-] ", s)]
print(u"目錄條目 %d ➔ %d（宜 +1）｜行數 %d ➔ %d" % (len(items0), len(items), len(BEFORE), len(L)))
if len(items) != len(items0) + 1:
    errs.append(u"目錄條目之變不唯一（+1）")
if sum(1 for s in items if u"十線地圖" in s) != 1 or sum(1 for s in items if u"附錄" in s) != 1:
    errs.append(u"目錄內二條之數不是一")
inx = next(i for i, s in enumerate(L) if u"（前置於第一部之前" in s)
inb = next(i for i, s in enumerate(L) if s.startswith(u"### **【第一部"))
print(u"序位覆核：十線條 L%d ＜ 第一部題 L%d ➔ %s" % (inx + 1, inb + 1, u"正" if inx < inb else u"仍倒置"))
if inx > inb:
    errs.append(u"十線條仍在部題之後")
allnew = u"".join(s for _n, s in NEWTEXT) + bullet
sm = sorted({u"%s➔%s" % (c, _simpmap.MAP[c]) for c in set(allnew) if c in _simpmap.MAP})
ding = sorted({c for c in set(allnew) if c in DING_ERR})
print(u"新文簡形：MAP %s｜硬盯 %s" % (u"、".join(sm) or u"0", u"、".join(ding) or u"0"))
if sm or ding:
    errs.append(u"新文帶簡形")
out = u"\r\n".join(L)
if out.count(u"「") != out.count(u"」") or raw.count(u"「") - raw.count(u"」") != out.count(u"「") - out.count(u"」"):
    errs.append(u"引號之衡已變")
if out.count(u"\r\n") != len(L) - 1:
    errs.append(u"CRLF 變形")

if errs:
    print(u"✗ 擲不寫：")
    for e in errs:
        print(u"   " + e)
    sys.exit(1)
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
BK = HP.bakpath("76a")
io.open(BK, "wb").write(raw.encode("utf-8"))
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
