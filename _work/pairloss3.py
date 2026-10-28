# -*- coding: utf-8 -*-
"""第二波『六筆深水資產』之實測：ver39 之體與兩冊之有無（只讀）。

用法：python -X utf8 _work/pairloss3.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V = [l.rstrip("\r") for l in sorted(ROOT.glob("ver39*.md"))[0].read_bytes().decode("utf-8").split("\n")]
F1 = (ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt").read_bytes().decode("utf-8").split("\r\n")
F2 = (ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt").read_bytes().decode("utf-8").split("\r\n")


def cjk(s):
    return sum(1 for c in s if "\u4e00" <= c <= "\u9fff")


def hits(pat, lines):
    return [i + 1 for i, l in enumerate(lines) if re.search(pat, l)]


def probe(no, title, pat, cap=3):
    print(f"\n◆ {no}・{title}")
    for nm, L in (("ver39", V), ("F1", F1), ("F2", F2)):
        h = hits(pat, L)
        print(f"   {nm:>6}：{len(h):>3} 行  " + "・".join("L%d" % x for x in h[:cap]))
        if nm == "ver39" and h:
            for x in h[:cap]:
                print(f"          L{x}: {V[x-1].strip()[:82]}")


probe(1, "境想矩陣之詞族", r"境想|有主想|無主想|己有想|暫取想|與想|想差")
probe(1, "殺生客體／打擊錯誤", r"客體錯誤|打擊錯誤|目標看錯|箭矢偏|誤中")
probe(1, "五大臨界標尺（但書一至五）", r"但書[一二三四五]|臨界標尺|命難標尺|貞操標尺|妄語標尺|職守標尺|財產標尺")
probe(1, "言聲斷寄・斷彼心", r"言聲斷寄|言聲離處|斷彼心|彼心斷|賴寄|賴帳")
probe(2, "三調法", r"呵責羯磨|擯出羯磨|依止羯磨|三調|Tajjaniya|Pabbajaniya|Nissaya")
probe(2, "解依止五法・共犯拆散", r"解依止|五法解|拆散|隔離行治|同行不相")
probe(3, "五種邪命", r"邪命|詐現異相|自說功德|占相吉凶|高聲現威|說得供養|五種邪")
probe(3, "誑・諂二心所", r"【誑|【諂|誑（|諂（|隨煩惱.{0,8}誑|隨煩惱.{0,8}諂")
probe(4, "留說戒・急難互許", r"留說戒|互許|道斷|水陸道斷|無清淨僧|全寺同犯|全員同犯")
probe(5, "九則引橋範本", r"九則|引橋|範本|切結|代位追償|受訴聲請|前置約定")
probe(6, "三舉・法權凍結", r"三舉|作法別住|別住法權|凍結")

print("\n■ ver39 之相關節界與體積（供定價）")
for pat, nm in ((r"^### 第三節　組織調伏", "第五章第三節 組織調伏"),
                (r"^### 第六節　留說戒|^#### .*留說戒", "留說戒款"),
                (r"^### 第五節　現代道場", "第八章第五節"),
                (r"^## 第二節　持犯核心心所", "第二章第二節"),
                (r"^### 第二節　三階思", "第二章第二節(alt)")):
    h = hits(pat, V)
    print(f"   {nm}: {['L%d' % x for x in h] or '未以此形出現'}")
for kw in ["三調", "呵責", "留說戒", "邪命", "境想", "斷彼心", "九則"]:
    h = hits(kw, V)
    print(f"   ver39 含『{kw}』{len(h)} 行：{['L%d' % x for x in h[:6]]}")
