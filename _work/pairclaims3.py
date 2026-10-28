# -*- coding: utf-8 -*-
"""追補四查：律文上下文・名相可得性・書內既有之量化與熔斷語・ver39 是否本有其文。

用法：PYTHONPATH=. python -X utf8 _work/pairclaims3.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import _tk                                            # noqa: E402

V = _tk.VINAYA
print("■ 甲・『尼不得舉比丘』之律文上下文（norm 後之串，取前後 90 字）")
for w in ["不得舉比丘", "舉比丘罪"]:
    i = V.find(w)
    print(f"  「{w}」見於語料 norm 串第 {i} 字：…{V[max(0,i-90):i+70]}…")

print("\n■ 乙・書中所用名相之本地可得性（term_count）")
for w in ["八敬法", "敬法", "尼犍度", "犍度", "揵度", "隨王法", "王法", "法犍度", "調部"]:
    print(f"  {w:8} { _tk.term_count(w):>4} 見")

print("\n■ 丙・兩冊與 ver39 之『五錢算定／隨王法』既有論述")
V39 = sorted(ROOT.glob("ver39*.md"))[0].read_bytes().decode("utf-8").split("\r\n")
for nm, L in (("F1", (ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt").read_bytes().decode("utf-8").split("\r\n")),
              ("F2", (ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt").read_bytes().decode("utf-8").split("\r\n")),
              ("ver39", V39)):
    for rx in [r"隨王法|隨國法|從王法", r"五錢.{0,24}(折算|換算|算定|基準|今值|金額)", r"(折算|換算|算定|基準).{0,18}五錢",
               r"疑罪從無|疑罪從輕|自疑不罰|生疑妄動"]:
        hits = [(i + 1, l.strip()[:72]) for i, l in enumerate(L) if re.search(rx, l)]
        if hits:
            print(f"  [{nm}] /{rx}/ → {len(hits)}")
            for i, s in hits[:4]:
                print(f"        L{i}: {s}")

print("\n■ 丁・F1 第十一章之現行時限語（有無『分鐘／計時／停』）")
L = (ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt").read_bytes().decode("utf-8").split("\r\n")
start = next(i for i, l in enumerate(L) if l.startswith("# 第十一章"))
end = next(i for i, l in enumerate(L) if l.startswith("# 第十二章"))
print(f"  第十一章＝L{start+1}〜L{end}（{end-start} 行）")
for rx in [r"分鐘|四分|十分|一時辰|時間|計時|沙漏|鐘", r"停|止觀|不復|勿再|即止|便放|即覺", r"醫療|醫師|病|藥"]:
    hits = [(i + 1, L[i].strip()[:70]) for i in range(start, end) if re.search(rx, L[i])]
    print(f"   /{rx}/ → {len(hits)}")
    for i, s in hits[:5]:
        print(f"        L{i}: {s}")
