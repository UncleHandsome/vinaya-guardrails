# -*- coding: utf-8 -*-
"""寅刀之靶量：待換之現代譯名，逐詞印兩冊之見數・行數・是否在標題・例句一條。"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import importlib
m = importlib.import_module("pairdelaw")

F2 = (ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt").read_bytes().decode("utf-8").split("\r\n")
F1 = (ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt").read_bytes().decode("utf-8").split("\r\n")
TERMS = ["創傷知情", "煤氣燈", "目標致盲", "多巴胺", "杏仁核", "前額葉", "神經脈衝", "骨骼肌",
         "破罐破摔", "自暴自棄", "適應障礙", "靈性資本主義", "部落主義", "尋租", "漏斗",
         "防空洞", "消磁", "雷達", "公訴", "調查官", "專案小組", "專案組", "指紋", "血跡",
         "監視器", "監視影像", "隔室視訊", "單次陳述", "維度", "斜體英文", "創傷後", "心理學",
         "神经|神經", "免責", "霸凌", "吹哨人", "合規", "稽核", "風控", "非營利組織", "治理"]
for t in TERMS:
    if t == "斜體英文":
        for tag, ls in (("F2", F2), ("F1", F1)):
            hits = [i + 1 for i, l in enumerate(ls) if re.search(r"\*[A-Za-z][A-Za-z ,\-')(&]{2,}\*", l)
                    and not re.search(r"[àāēīūṃṇṭśñ]", l)]
            print(f"  {'*(英文斜體)*':10s}｜{tag} 行 {len(hits):3d} " + " ".join(f"L{a}" for a in hits[:12]))
        continue
    for tag, ls in (("F2", F2), ("F1", F1)):
        hits = [(i + 1, l) for i, l in enumerate(ls) if re.search(t, l)]
        n = sum(len(re.findall(t, l)) for _, l in hits)
        heads = [i for i, l in hits if m.ANY_HEAD.match(l.strip())]
        if hits:
            ex = next((l.strip()[:46] for _, l in hits), "")
            print(f"  {t:8s}｜{tag} 見 {n:3d}・行 {len(hits):3d}"
                  + (f"・標題 {len(heads)}:{heads[:6]}" if heads else "") + f"　例：{ex}")
