# -*- coding: utf-8 -*-
"""尺（simp_sweep）——全書簡形大掃除（緊口徑）：只收「繁體正書中不會出現」的簡體專用字，
引號內豁免（原典轉寫從舊形）。加第二參數 fix 即就地替換並報每字處數。

退出碼今制（第 56 輪）：本尺歷輪只印病不報紅——實測書中三枚『错』連印兩輪而 rc 仍 0，
    跑批器遂照樣綠（『殭尺之綠』之典型：判式在，退出碼不在）。今覆核模式有殘留即退 1；
    fix 模式以『改後回讀』之殘留定退碼——改完即綠才算真改。
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import glob
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
from _simpdict import MAP as SIMP  # 單一法源，勿在此重抄
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lane  # noqa: E402  律文欄（條文／律制）之保護區與草稿閘同法源

# 豁免自算，不靠手工名册：凡該簡形確實見於《四分律》語料者（如『并』『谷』『余』），
# 只在引號外追查；語料中根本不存在的形體（如『还』『刚』『内』）則引號內外一律查。
CORP = set()
for f in glob.glob(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "原文", "*.txt")):
    CORP |= set(io.open(f, encoding="utf-8", errors="ignore").read())
RISKY = {k for k in SIMP if k in CORP}


def inq_factory(t):
    """保護區＝『「…」』逐行引號 ＋ CBETA 組字碼『[X-Y+Z]』 ＋ 經語料對勘之律文欄。
    組字碼（如『[袖-由+宁]』＝衣旁宁）乃原檔之合字構形，其中部件偶與簡形同形（宁），
    此類一律非簡形，否則尺會『好心』把缺字標記改成寧，毀掉可回溯性。
    律文欄不入引號而實為逐字（『食并餘物』之『并』即語料原形），故保護須以對勘得之，非以名目得之。"""
    spans = [m.span() for m in re.finditer(u"「[^」\n]*」", t)]
    spans += [m.span() for m in re.finditer(u"\\[[^\\]\\n]{1,14}\\]", t)]
    spans += lane.spans(t)[0]
    return lambda i: any(a <= i < b for a, b in spans)


def find_hits(t):
    """口徑只此一條（查與改共用）：語料無此形者引號內外一律查，見於語料者唯引號外才查。
    不另立『Big5 可編性』之自動判別：實測 python 之 big5 編碼器缺 鉢・鬪・鈎・隥・飤・麨
    等正字（且把『～」也報為不可編），假陽性成山，反足掩真病。字典之漏，改以 hl_unseen
    對照本輪開工前之備檔來兜，並依此尺報出之真簡形逐枚回填 _simpdict。"""
    inq = inq_factory(t)
    hits = {}
    for i, c in enumerate(t):
        if c not in SIMP or (c in RISKY and inq(i)):
            continue
        hits.setdefault(c, []).append((t[:i].count("\n") + 1,
                                       t[max(0, i - 14):i + 14].replace("\r", "").replace("\n", "/")))
    return hits


def report(tag, hits):
    print(u"%s簡形殘留（引號外）：%d 種 %d 處"
          % (tag, len(hits), sum(len(v) for v in hits.values())))
    for c, v in sorted(hits.items()):
        for ln, ctx in v[:4]:
            print(u"  L%-5d %s→%s｜%s" % (ln, c, SIMP[c], ctx))


t = io.open(BOOK, encoding="utf-8", newline="").read()
hits = find_hits(t)
report(u"", hits)
rc = 1 if hits else 0

if len(sys.argv) > 1 and sys.argv[1] == "fix":
    inq = inq_factory(t)
    cut = {}
    out, pos = [], 0
    for i, c in enumerate(t):
        if c in SIMP and not (c in RISKY and inq(i)):
            out.append(t[pos:i]); out.append(SIMP[c]); pos = i + 1
            cut[c] = cut.get(c, 0) + 1
    out.append(t[pos:])
    new = u"".join(out)
    assert new.count("\r\n") == t.count("\r\n"), u"CRLF 變形"
    assert len(new) == len(t), u"字數變形"
    io.open(BOOK, "w", encoding="utf-8", newline="").write(new)
    print(u"已改：%s｜共 %d 處"
          % (" ".join(u"%s→%s×%d" % (k, SIMP[k], v) for k, v in sorted(cut.items())), sum(cut.values())))
    left = find_hits(io.open(BOOK, encoding="utf-8", newline="").read())
    report(u"改後回讀：", left)
    rc = 1 if left else 0
sys.exit(rc)
