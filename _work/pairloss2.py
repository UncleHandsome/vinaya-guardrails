# -*- coding: utf-8 -*-
"""四筆細量：四維矩陣體積・梵網見好相之本地逐字可證性・F2 命中行之實形。

用法：PYTHONPATH=. python -X utf8 _work/pairloss2.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import _tk                                            # noqa: E402

V = [l.rstrip("\r") for l in sorted(ROOT.glob("ver39*.md"))[0].read_bytes().decode("utf-8").split("\n")]
F2 = (ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt").read_bytes().decode("utf-8").split("\r\n")
F1 = (ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt").read_bytes().decode("utf-8").split("\r\n")


def cjk(s):
    return sum(1 for c in s if "\u4e00" <= c <= "\u9fff")


print("■ 四維檢索矩陣（ver39 第七章第二節）之體積")
a = next(i for i, l in enumerate(V) if l.strip().startswith("### 第二節　判例四維"))
b = next(i for i in range(a + 1, len(V)) if re.match(r"^#{2,3}\s", V[i].strip()))
seg = V[a:b]
print(f"   L{a+1}〜L{b}・{b-a} 行・漢字 {cjk(chr(10).join(seg)):,}・表行 {sum(1 for l in seg if l.strip().startswith('|'))}")
print("   首四行：")
for l in seg[:6]:
    print("      ", l.strip()[:92])

print("\n■ 三階懺悔一節（ver39 第五章第六節）之體積")
c = next(i for i, l in enumerate(V) if l.strip().startswith("### 第六節　三階懺悔"))
d = next(i for i in range(c + 1, len(V)) if re.match(r"^#{1,3}\s", V[i].strip()))
print(f"   L{c+1}〜L{d}・{d-c} 行・漢字 {cjk(chr(10).join(V[c:d])):,}")

print("\n■ 四大行動卡＋治理自檢表（ver39 第八章末）之體積")
e = next(i for i, l in enumerate(V) if "【四大隨身自律行動卡】" in l and l.startswith("###"))
f = next(i for i in range(e + 1, len(V)) if re.match(r"^#\s", V[i].strip()))
print(f"   L{e+1}〜L{f}・{f-e} 行・漢字 {cjk(chr(10).join(V[e:f])):,}（含卡四張與自檢表）")

print("\n■ 今時五病灶對讀索引（ver39 卷首）之體積")
g = next(i for i, l in enumerate(V) if "【今時五病灶對讀索引】" in l)
h = next(i for i in range(g + 1, len(V)) if re.match(r"^#{3,4}\s", V[i].strip()))
print(f"   L{g+1}〜L{h}・{h-g} 行・漢字 {cjk(chr(10).join(V[g:h])):,}")

print("\n■ 《梵網經》『見好相』本地逐字可證性（ver39 自標『本地語料未收』是否已過時）")
for k, v in _tk.OTHER.items():
    if "梵網" in k:
        nv = _tk.norm(v)
        for w in ["見好相", "好相", "千佛大劫中"]:
            print(f"   {k}｜norm 含『{w}』：{w in nv}")
print("   本地檔名：", [k for k in _tk.OTHER if "梵網" in k])

print("\n■ F2 之命中實形（判準層級・自檢表・四維）")
for n in (111, 157, 1380, 1550, 1728, 3253, 3260):
    print(f"   F2 L{n}: {F2[n-1].strip()[:96]}")
print("\n■ F1 L2937・F2 L2861 之實形")
print("   F1 L2937:", F1[2936].strip()[:96])
print("   F2 L2861:", F2[2860].strip()[:96])
