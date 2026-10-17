# -*- coding: utf-8 -*-
"""全書簡形大掃除（緊口徑）：只收「繁體正書中不會出現」的簡體專用字，
引號內豁免（原典轉寫從舊形）。加第二參數 fix 即就地替換並報每字處數。
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
from _simpdict import MAP as SIMP  # 單一法源，勿在此重抄

t = io.open(BOOK, encoding="utf-8", newline="").read()

# 豁免自算，不靠手工名册：凡該簡形確實見於《四分律》語料者（如『并』『谷』『余』），
# 只在引號外追查；語料中根本不存在的形體（如『还』『刚』『内』）則引號內外一律查。
import glob  # noqa: E402
CORP = set()
for f in glob.glob(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "原文", "*.txt")):
    CORP |= set(io.open(f, encoding="utf-8", errors="ignore").read())
RISKY = {k for k in SIMP if k in CORP}
spans = [m.span() for m in re.finditer(u"「[^」\n]*」", t)]
# CBETA 組字碼（如『[袖-由+宁]』＝衣旁宁）乃原檔之合字構形，其中部件偶與簡形同形（宁），
# 此類一律非簡形，故與引號同列保護區——否則尺會「好心」把缺字標記改成寧，毀掉可回溯性。
spans += [m.span() for m in re.finditer(u"\\[[^\\]\\n]{1,14}\\]", t)]
inq = lambda i: any(a <= i < b for a, b in spans)
hits, keep = {}, []
for i, c in enumerate(t):
    if c not in SIMP or (c in RISKY and inq(i)):
        continue
    hits.setdefault(c, []).append((t[:i].count("\n") + 1,
                                   t[max(0, i - 14):i + 14].replace("\r", "").replace("\n", "/")))
print(u"簡形殘留（引號外）：%d 種 %d 處" % (len(hits), sum(len(v) for v in hits.values())))
for c, v in sorted(hits.items()):
    for ln, ctx in v[:4]:
        print(u"  L%-5d %s→%s｜%s" % (ln, c, SIMP[c], ctx))
# 口徑只此一條，不另立「Big5 可編性」之自動判別：實測 python 之 big5 編碼器缺 鉢・鬪・鈎・隥・飤・麨
# 等正字（且把「～」也報為不可編），假陽性成山，反足掩真病。字典之漏，改以 hl_unseen 對照本輪開工前之
# 備檔來兜（凡語料與舊檔皆未見者一律列出），並依此尺報出之真簡形逐枚回填 _simpdict。
if len(sys.argv) > 1 and sys.argv[1] == "fix":
    cut = {}
    out, pos = [], 0
    for i, c in enumerate(t):
        # 口徑須與上方之「查」全等：語料無此形者，引號內外一律改；見於語料者（并・谷・余）唯引號外才改
        if c in SIMP and not (c in RISKY and inq(i)):
            out.append(t[pos:i]); out.append(SIMP[c]); pos = i + 1
            cut[c] = cut.get(c, 0) + 1
    out.append(t[pos:])
    new = u"".join(out)
    assert new.count("\r\n") == t.count("\r\n"), u"CRLF 變形"
    io.open(BOOK, "w", encoding="utf-8", newline="").write(new)
    print(u"已改：%s｜共 %d 處" % (" ".join(u"%s→%s×%d" % (k, SIMP[k], v) for k, v in sorted(cut.items())), sum(cut.values())))
