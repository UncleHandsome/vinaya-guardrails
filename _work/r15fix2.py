# -*- coding: utf-8 -*-
"""第 48 輪糾補：本律實記七百集法毘尼與十事——削去我新寫之誤句，改從律文；並正「心所」之說。"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import re
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "_work")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import _tk  # noqa: E402

BOOK = HP.SRC
NL = chr(13) + chr(10)
GO = u"--go" in sys.argv
raw = io.open(BOOK, encoding="utf-8", newline="").read()
L = raw.split(NL)
n0 = len(L)
NEWTXT = []


def sub_once(old, new, tag):
    ns = [i for i, t in enumerate(L) if old in t]
    assert len(ns) == 1, (u"命中數：" + tag, len(ns))
    assert L[ns[0]].count(old) == 1, (u"行內多命中：" + tag)
    L[ns[0]] = L[ns[0]].replace(old, new)
    NEWTXT.append(new)
    print(u"改 %s @L%d（-%d ＋新 %d 字）" % (tag, ns[0] + 1, len(old), len(new)))


OLD_A = (u"此事本電子化《四分律》不記：『結集』二字在此律 0 見，『七百』九見俱屬車乘之數，部派之名亦不出律文；"
         u"故本書只作史家之說引之，不作律據。")
NEW_A = (u"此事不必假外求——本律自己就記著：**「爾時世尊般涅槃後百歲，毘舍離跋闍子比丘行十事，言是法清淨佛所聽。」**"
         u"又記其結：**「在毘舍離七百阿羅漢集論法毘尼，故名七百集法毘尼。」**"
         u"十事之名目在律一一可舉：兩指抄食、聚落間、寺內、後聽可、常法、和、與鹽共宿、飲闍樓羅酒、畜不截坐具、受金銀；"
         u"而爭的正是佛陀般涅槃百年之後還動不動得細行。律甚至留下分張之形（**「後五部分張，各據所傳」**）。"
         u"至於上座、大眾二分之名與因果之判，出後世史家與部派之書，非此文逐字，本書不作律據。")
sub_once(OLD_A, NEW_A, u"第十六章・誤句改律據")

OLD_B = u"（此律中『心所』之形雖有，皆作『心之所念』用，不作為術語）"
NEW_B = u"（『心所』在此律不作為術語，其字面之見皆屬『心所樂』『心所念』或跨詞的『心／所謂』）"
sub_once(OLD_B, NEW_B, u"第十九章・心所之說歸實")

# 三枚逐字先驗連写（本律以「集法毘尼」語此事，不作「結集」之形）
for q in [u"爾時世尊般涅槃後百歲", u"在毘舍離七百阿羅漢集論法毘尼", u"後五部分張",
          u"毘舍離跋闍子比丘行十事"]:
    print(u"  語料验 %s → %s" % (q, u"相連" if _tk.VINAYA.find(_tk.norm(q)) >= 0 else u"不連"))
for t in NEWTXT:
    for m in re.finditer(u"「\\*\\*([^」\\n]*)\\*\\*」", t):
        ok = _tk.VINAYA.find(_tk.norm(m.group(1))) >= 0
        print(u"  逐字閘 %s ｜ %s" % (u"中" if ok else u"無據", m.group(1)[:28]))
        assert ok, (u"新逐字無據", m.group(1)[:24])

assert len(L) == n0, (u"行數須不變", len(L), n0)
out = NL.join(L)
assert out.count(chr(13)) == len(L) - 1
from _simpdict import MAP as SIMP  # noqa: E402
bad = sorted({c for t in NEWTXT for c in t if c in SIMP})
print(u"簡形命中：%s" % ([(c, SIMP[c]) for c in bad] or 0))
print(u"行數 %d → %d" % (n0, len(L)))
if GO:
    io.open(BOOK, "w", encoding="utf-8", newline="").write(out)
    print(u"已寫入")
else:
    print(u"（試跑，未寫入）")
