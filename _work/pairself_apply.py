# -*- coding: utf-8 -*-
"""兩事一氣：① pairreflow 立 SELF 之表（他日自重放者同果）；② 今檔之迎回區補自稱歸位
   （本章→本附錄・本節→本附錄・本篇→《如法推尋》），落盤前先存 .pre_self＋SHA。
用法：python -X utf8 _work/pairself_apply.py [--write]"""
import ast
import hashlib
import shutil
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import _simpdict  # noqa: E402
import _simpmap  # noqa: E402

W = "--write" in sys.argv
F1 = "起心動念：四分律的心智顯微鏡與唯識解剖.txt"
F2 = "如法推尋：僧伽憲政、法權審理與修復正義.txt"
BAK = ROOT / "_archive/備份/AI清理前"
SELF = {F1: [("本節借用當代認知心理學、臨床精神醫學與社會心理學語彙", "本附錄借今時治病用人之常言作對位"),
            ("本章將佛陀那一聲千古垂問", "本附錄將佛陀那一聲千古垂問"),
            ("貫穿本章的導航工具", "貫穿本附錄的導航工具"),
            ("本章專司其動機與構成要件之定性，後續處分階梯各依本篇軌道分流",
             "本附錄專司其動機與構成要件之定性，後續處分階梯各依《如法推尋》之軌分流")],
        F2: []}
SIMPLE = (set(_simpmap.MAP) | set(_simpdict.MAP)) - set("几")

# ── ① 產生器立表（縮進四格，落於 build() 之 rewrite 與 apply_pointers 之間）──
p = ROOT / "_work/pairreflow.py"
s = p.read_bytes().decode("utf-8")
TBL = '''# 甲・自稱歸位（唯施於該件之內：形如 (冊, 件) → [(舊, 新)]）
SELF = {
    (F1, "附錄二"): [(k, v) for k, v in [
        ("本節借用當代認知心理學、臨床精神醫學與社會心理學語彙", "本附錄借今時治病用人之常言作對位")]],
    (F1, "附錄四"): [(k, v) for k, v in [
        ("本章將佛陀那一聲千古垂問", "本附錄將佛陀那一聲千古垂問"),
        ("貫穿本章的導航工具", "貫穿本附錄的導航工具"),
        ("本章專司其動機與構成要件之定性，後續處分階梯各依本篇軌道分流",
         "本附錄專司其動機與構成要件之定性，後續處分階梯各依《如法推尋》之軌分流")]],
}

'''
anchor = "# 整行改寫（唯一前錨"
if "SELF = {" not in s:
    assert s.count(anchor) == 1, "無插入錨"
    s = s.replace(anchor, TBL + anchor, 1)
    old = "    seg = rewrite(seg, dst, tag)\n    seg = apply_pointers(seg, dst, tag)"
    assert s.count(old) == 1, "無施用點"
    s = s.replace(old, "    seg = rewrite(seg, dst, tag)\n"
                       "    seg = selfwords(seg, dst, tag)\n"
                       "    seg = apply_pointers(seg, dst, tag)", 1)
    s = s.replace("def build(dst, tag, a, b, new_head):",
                  "def selfwords(seg, dst, tag):\n"
                  "    for o, nw in SELF.get((dst, tag), []):\n"
                  "        seg = [l.replace(o, nw) for l in seg]\n"
                  "    return seg\n\n\n"
                  "def build(dst, tag, a, b, new_head):", 1)
    ast.parse(s)
    if W:
        p.write_bytes(s.encode("utf-8"))
    print("① pairreflow 立 SELF・ast OK")

# ── ② 今檔就地歸位（同一字表，刀尺同源）──
for fn, rules in SELF.items():
    fp = ROOT / fn
    raw = fp.read_bytes()
    L = raw.decode("utf-8").split("\r\n")
    k = max(i for i, l in enumerate(L) if l.startswith("## 附錄一"))
    n = 0
    for o, nw in rules:
        for i in range(k, len(L)):
            if o in L[i]:
                L[i] = L[i].replace(o, nw)
                n += 1
        if not any(o in l for l in L[k:]):
            pass
    bad = sorted({c for l in L[k:] for c in l if c in SIMPLE})
    print(f"② {fn[:6]}・迎回區 {len(L) - k} 行・歸位 {n}/{len(rules)} 條・簡形 {len(bad)} 枚 {bad}")
    if W and n:
        BAK.mkdir(parents=True, exist_ok=True)
        (BAK / (fn + ".pre_self")).write_bytes(raw)
        data = "\r\n".join(L).encode("utf-8")
        fp.write_bytes(data)
        print(f"    落盤：SHA {hashlib.sha256(raw).hexdigest()[:12]} → {hashlib.sha256(data).hexdigest()[:12]}"
              f"・備份 .pre_self")
