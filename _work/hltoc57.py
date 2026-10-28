# -*- coding: utf-8 -*-
"""第 57 輪・丁：目錄之第十一章三件事——①章題歸新（二十犍度→犍度精要・憲法→憲章）
②四樞紐入目（新章正文有此四條 H3，目錄不可無）③案例 27 條之縮排下沉一層（歸於各樞紐之下）。
案例之『題』由 _work/tocsync.py 以正文為法源覆蓋，本刀不動其文、只動其位與其數。
硬斷言：目錄案例項 27＝正文 27・樞紐入目 4＝正文 4・行數 +4・CRLF 不動。
用法：python -X utf8 _work/hltoc57.py [--go]
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert raw.count(u"\r") == raw.count(u"\n"), u"入口 CRLF 已傷"
L = raw.split(u"\r\n")
N0 = len(L)

# ── 正文之新形（法源）──────────────────────────────────────────────
H1 = u"# 第十一章 犍度精要"
H2 = u"## ——戒相背後的僧團憲章：誰說了算、怎麼算、算幾次"
assert L.count(H1) == 1 and L.count(H2) == 1, u"新章之 H1／H2 不在冊"
i_body = L.index(H1)
SHU = [l for l in L if re.match(u"^### 【第[一二三四]樞紐：.*】$", l)]
assert len(SHU) == 4, u"正文樞紐 H3 數 %d ≠ 4" % len(SHU)
CASES = {}
cur = None
for l in L[i_body:]:
    if l.startswith(u"# 第十二章") or l.startswith(u"# 【第三部"):
        break
    m = re.match(u"^### 【第(.)樞紐：.*】$", l)
    if m:
        cur = m.group(1)
    m = re.match(u"^#### 案例([一二三四五六七八九十]+)：", l)
    if m:
        assert cur, u"正文案例『%s』不在任何樞紐之下" % m.group(1)
        CASES.setdefault(cur, []).append(m.group(1))
print(u"正文：樞紐 %d｜各樞紐之案例數 %s｜合計 %d" % (
    len(SHU), [len(CASES[u"一二三四"[k]]) for k in range(4)], sum(len(v) for v in CASES.values())))
assert sum(len(v) for v in CASES.values()) == 27, u"正文第十一章案例數 ≠ 27"

# ── 目錄區內之第十一章段 ────────────────────────────────────────────
t0 = next(i for i, l in enumerate(L) if u"【全書詳細目錄】" in l)
t1 = next(i for i in range(t0 + 1, len(L)) if re.match(u"^# ", L[i]))
TOCH = re.compile(u"^\\* \\*\\*第([一二三四五六七八九十]{1,3})章")
mh = [(i, TOCH.match(L[i]).group(1)) for i in range(t0, t1) if TOCH.match(L[i])]
ia = next(i for i, c in mh if c == u"十一")
iz = next((i for i, c in mh if c == u"十二"), t1)
seg = L[ia:iz]
print(u"目錄之第十一章段：L%d–L%d（%d 行）" % (ia + 1, iz, len(seg)))

# ① 章題歸新
OLD_T = u"* **第十一章 二十犍度——戒相背後的僧團憲法：誰說了算、怎麼算、算幾次**"
NEW_T = u"* **第十一章 犍度精要——戒相背後的僧團憲章：誰說了算、怎麼算、算幾次**"
c = sum(1 for l in seg if l == OLD_T)
assert c == 1, u"目錄章題錨命中 %d" % c
seg = [NEW_T if l == OLD_T else l for l in seg]
print(u"① 章題：二十犍度→犍度精要・憲法→憲章")

# ②＋③ 案例行縮排下沉，並於各樞紐之首案例前插入樞紐條目
CROW = re.compile(u"^(    \\* )(案例[一二三四五六七八九十]+：.*)$")
n_case = sum(1 for l in seg if CROW.match(l))
assert n_case == 27, u"目錄案例行 %d ≠ 27" % n_case
first = {CASES[k][0]: SHU[n] for n, k in enumerate(u"一二三四")}
out, done = [], set()
for l in seg:
    m = CROW.match(l)
    if m:
        num = re.match(u"案例([一二三四五六七八九十]+)：", m.group(2)).group(1)
        for k, head in first.items():
            if k == num and head not in done:
                out.append(u"    * **%s**" % head[len(u"### "):])
                done.add(head)
                print(u"② 入目：%s" % head[4:44])
        out.append(u"      * " + m.group(2))
        continue
    out.append(l)
assert len(done) == 4, u"樞紐入目 %d ≠ 4" % len(done)
print(u"③ 案例 27 條縮排 4→6（歸於樞紐之下）")
assert len(out) == len(seg) + 4, u"段行數變化非 +4：%d→%d" % (len(seg), len(out))
n2 = sum(1 for l in out if re.match(u"^      \\* 案例[一二三四五六七八九十]+：", l))
assert n2 == 27, u"下沉後案例行 %d ≠ 27" % n2

L[ia:iz] = out
print(u"全書行數 %d→%d" % (N0, len(L)))
txt = u"\r\n".join(L)
assert txt.count(u"\r") == txt.count(u"\n"), u"出口 CRLF 變形"
if u"--go" in sys.argv:
    io.open(BOOK, "w", encoding="utf-8", newline=u"").write(txt)
    print(u"已寫檔（案例之題仍候 tocsync 以正文覆蓋）")
else:
    print(u"（乾跑：加 --go 始寫）")
