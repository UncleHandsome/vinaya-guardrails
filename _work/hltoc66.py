# -*- coding: utf-8 -*-
"""第 66 輪・乙：第八、第九兩章目錄之重建（案例 24＋30 → 12＋13・各加『板塊／重鎮』中間層五行）。

形制承第 57／65 輪：正文『### 【第N板塊：…】』／『### 【第N重鎮：…】』在目錄作『    * **【…】**』，
其下案例再沉一層（六空格）。層名之式由 `hlchk.LAYER` 共器定（本輪已擴至板塊／重鎮）。
硬斷言：兩章之『節 5・層 5・案例 12／13』俱與正文同；兩章以外之檔一字不動。
用法：python -X utf8 _work/hltoc66.py [--go]
"""
import hashlib
import io
import os
import re
import shutil
import sys

GO = u"--go" in sys.argv
BOOK = u"佛陀的護欄 四分律比丘與比丘尼戒的行為心理學解析.txt"
BAK = BOOK + u".bak66b"
raw = io.open(BOOK, "rb").read()
sha0 = hashlib.sha256(raw).hexdigest()
L = raw.decode("utf-8").split(u"\r\n")
assert raw.count(b"\r") == raw.count(b"\n"), u"入口 CRLF 已傷"
N0 = len(L)

LAYER = re.compile(u"^### (【第[一二三四五六七八九十]+(?:樞紐|陣地|板塊|重鎮)：.*】)$")
SEC = re.compile(u"^### ([一二三四五六七八九十]+)、\\s*(.*)$")
CASE = re.compile(u"^#### (案例[〇零一二三四五六七八九十]+：)(.*)$")
CN = {u"八": u"第八章", u"九": u"第九章"}

TOCH = re.compile(u"^\\* \\*\\*第([一二三四五六七八九十]{1,3})章")
toc0 = next(i for i, l in enumerate(L) if u"【全書詳細目錄】" in l)
toc1 = next(i for i in range(toc0 + 1, len(L)) if re.match(u"^# ", L[i]))
tc = [(i, TOCH.match(L[i]).group(1)) for i in range(toc0, toc1) if TOCH.match(L[i])]
H1 = [(i, l) for i, l in enumerate(L) if re.match(u"^# ", L[i])]


def body_rows(name):
    k = [j for j, (i, l) in enumerate(H1) if l.startswith(u"# " + name)][0]
    a, z = H1[k][0], H1[k + 1][0]
    rows, nsec, nlay, ncase = [], 0, 0, 0
    for l in L[a:z]:
        m = SEC.match(l)
        if m:
            rows.append(u"  * %s、 %s" % (m.group(1), m.group(2).strip()))
            nsec += 1
            continue
        m = LAYER.match(l)
        if m:
            rows.append(u"    * **%s**" % m.group(1))
            nlay += 1
            continue
        m = CASE.match(l)
        if m:
            rows.append(u"      * %s%s" % (m.group(1), m.group(2).strip()))
            ncase += 1
    return rows, nsec, nlay, ncase


edits = []
for cn in (u"八", u"九"):
    name = CN[cn]
    rows, nsec, nlay, ncase = body_rows(name)
    print(u"正文 %s：節 %d｜層 %d｜案例 %d" % (name, nsec, nlay, ncase))
    assert (nsec, nlay) == (5, 5), u"%s 之節／層數不合" % name
    ia = next(i for i, c in tc if c == cn)
    iz = next(i for i, c in tc if c == (u"九" if cn == u"八" else u"十"))
    old = L[ia:iz]
    assert old[0].startswith(u"* **%s " % name), u"目錄章題之錨不正：%s" % old[0][:28]
    assert old[-1] == u"", u"目錄段之尾非空行"
    new = [old[0]] + rows + [u""]
    edits.append((ia, iz, new, name, ncase))
    print(u"目錄 %s 段：L%d–L%d（%d 行）→ %d 行" % (name, ia + 1, iz, len(old), len(new)))

for ia, iz, new, name, nc in sorted(edits, key=lambda e: -e[0]):
    L[ia:iz] = new

txt = u"\r\n".join(L)
assert txt.count(u"\r") == txt.count(u"\n") == len(L) - 1, u"CRLF 變形"
t2 = sum(1 for l in L if re.match(u"^      \\* 案例", l))
t3 = sum(1 for l in L if re.match(u"^    \\* \\*\\*【第", l))
print(u"全書目錄：三級案例項 %d｜中間層項 %d｜行數 %d→%d" % (t2, t3, N0, len(L)))
print(u"正本 sha（改前）%s" % sha0[:12])
if not GO:
    for ia, iz, new, name, nc in edits[:1]:
        for r in new[:7]:
            print(u"   »" + r[:80])
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
assert not os.path.exists(BAK), u"備份已存在：%s" % BAK
shutil.copy2(BOOK, BAK)
io.open(BOOK, "w", encoding="utf-8", newline=u"").write(txt)
chk = io.open(BOOK, "rb").read()
CL = chk.decode("utf-8").split(u"\r\n")
for ia, iz, new, name, nc in edits:
    pass
assert sum(1 for l in CL if re.match(u"^      \\* 案例", l)) == t2, u"覆讀三級案例不合"
print(u"已寫檔｜sha %s→%s｜%d B｜備份 %s" % (
    sha0[:12], hashlib.sha256(chk).hexdigest()[:12], len(chk), os.path.basename(BAK)))
