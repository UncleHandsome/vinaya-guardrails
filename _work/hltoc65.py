# -*- coding: utf-8 -*-
"""第 65 輪・乙：第七章目錄之重建（案例 19→18・新增『第N陣地』中間層五行）。

形制承第 57 輪之『第N樞紐』：正文 H3『### 【第N陣地：…】』在目錄作『    * **【…】**』，
其下之案例再沉一層（『      * 案例N：…』）——同層同字面，由 hlchk 丙軸與 tocsync 雙尺複核。
硬斷言：目錄之節項 5＝正文 5・陣地 5＝正文 5・案例項 18＝正文 18・第七章以外之檔一字不動。
用法：python -X utf8 _work/hltoc65.py [--go]
"""
import hashlib
import io
import os
import re
import shutil
import sys

GO = u"--go" in sys.argv
BOOK = u"佛陀的護欄 四分律比丘與比丘尼戒的行為心理學解析.txt"
BAK = BOOK + u".bak65b"

raw = io.open(BOOK, "rb").read()
sha0 = hashlib.sha256(raw).hexdigest()
L = raw.decode("utf-8").split(u"\r\n")
assert raw.count(b"\r") == raw.count(b"\n"), u"入口 CRLF 已傷"
N0 = len(L)

# ── 正文法源 ─────────────────────────────────────────────────────────
H1 = [(i, l) for i, l in enumerate(L) if re.match(u"^# ", l)]
i7 = [k for k, (i, l) in enumerate(H1) if l == u"# 第七章 三十捨墮"][0]
a, z = H1[i7][0], H1[i7 + 1][0]
SEC = re.compile(u"^### ([一二三四五六七八九十]+)、\\s*(.*)$")
LAY = re.compile(u"^### (【第[一二三四五六七八九十]+陣地：.*】)$")
CASE = re.compile(u"^#### (案例[〇零一二三四五六七八九十]+：)(.*)$")
rows, sec, lay = [], 0, 0
for l in L[a:z]:
    m = SEC.match(l)
    if m:
        rows.append(u"  * %s、 %s" % (m.group(1), m.group(2).strip()))
        continue
    m = LAY.match(l)
    if m:
        rows.append(u"    * **%s**" % m.group(1))
        lay += 1
        continue
    m = CASE.match(l)
    if m:
        rows.append(u"      * %s%s" % (m.group(1), m.group(2).strip()))
        sec += 1
print(u"正文第七章：節 5｜陣地 %d｜案例 %d" % (lay, sec))
assert lay == 5 and sec == 18, u"正文之形制不合（陣地 %d／案例 %d）" % (lay, sec)

# ── 目錄之第七章段 ───────────────────────────────────────────────────
TOCH = re.compile(u"^\\* \\*\\*第([一二三四五六七八九十]{1,3})章")
tc = [(i, TOCH.match(l).group(1)) for i, l in enumerate(L[:400]) if TOCH.match(l)]
ia = next(i for i, c in tc if c == u"七")
iz = next(i for i, c in tc if c == u"八")
old = L[ia:iz]
print(u"目錄第七章段：L%d–L%d（%d 行）→ 新 %d 行" % (ia + 1, iz, len(old), len(rows) + 1))
assert old[0].startswith(u"* **第七章 三十捨墮——"), u"目錄章題之錨不正：%s" % old[0][:30]
assert len(old) > 1 and old[-1] == u"", u"目錄段之尾非空行"
new = [old[0]] + rows + [u""]
pre, post = L[:ia], L[iz:]
L2 = pre + new + post
assert L2[:ia] == pre and L2[ia + len(new):] == post, u"第七章以外之檔動了"
n_c = sum(1 for l in new if re.match(u"^      \\* 案例", l))
n_l = sum(1 for l in new if re.match(u"^    \\* \\*\\*【第.陣地：", l))
n_s = sum(1 for l in new if re.match(u"^  \\* [一二三四五]、", l))
assert (n_s, n_l, n_c) == (5, 5, 18), u"目錄之形制不合：%s" % ((n_s, n_l, n_c),)
print(u"目錄新段：節 5｜陣地 5｜案例 18 ✓")

txt = u"\r\n".join(L2)
assert txt.count(u"\r") == txt.count(u"\n") == len(L2) - 1, u"CRLF 變形"
print(u"全書行數 %d→%d" % (N0, len(L2)))
if not GO:
    for r in new[:8]:
        print(u"   »" + r[:82])
    print(u"   …（共 %d 行）" % len(new))
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
assert not os.path.exists(BAK), u"備份已存在：%s" % BAK
shutil.copy2(BOOK, BAK)
io.open(BOOK, "w", encoding="utf-8", newline=u"").write(txt)
chk = io.open(BOOK, "rb").read()
CL = chk.decode("utf-8").split(u"\r\n")
assert CL[:ia] == pre and CL[ia:ia + len(new)] == new, u"覆讀不合"
print(u"已寫檔｜sha %s→%s｜備份 %s" % (
    sha0[:12], hashlib.sha256(chk).hexdigest()[:12], os.path.basename(BAK)))
