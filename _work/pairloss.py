# -*- coding: utf-8 -*-
"""『六大流失資產』清單之實測：ver39 之體積與兩冊之有無（只讀）。

用法：python -X utf8 _work/pairloss.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V = [l.rstrip("\r") for l in sorted(ROOT.glob("ver39*.md"))[0].read_bytes().decode("utf-8").split("\n")]
F1 = (ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt").read_bytes().decode("utf-8").split("\r\n")
F2 = (ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt").read_bytes().decode("utf-8").split("\r\n")


def cjk(s):
    return sum(1 for c in s if "\u4e00" <= c <= "\u9fff")


def h1(pat):
    return [i for i, l in enumerate(V) if re.match(r"^#\s+" + pat, l.strip())]


def seg(a, b):
    return "\n".join(V[a:b])


def where(pat, lines):
    return [i + 1 for i, l in enumerate(lines) if re.search(pat, l)]


def probe(title, vpat, fpat):
    print(f"\n◆ {title}")
    a = where(vpat, V)
    print(f"   ver39：{len(a)} 行", "・首見 " + "、".join("L%d" % x for x in a[:6]))
    for i in a[:4]:
        print(f"      L{i}: {V[i-1].strip()[:80]}")
    for nm, L in (("F1", F1), ("F2", F2)):
        h = where(fpat, L)
        print(f"   {nm}：{len(h)} 行 " + ("・".join("L%d" % x for x in h[:5]) if h else "（無）"))


print("■ ver39 章界與六筆資產之所在節")
for i, l in enumerate(V, 1):
    if re.match(r"^#{2,3}\s*(第[一二三四五六七八九十]+節|【)", l.strip()) and i < 2200:
        pass
for nm, pat in (("三章", r"第三章"), ("五章", r"第五章"), ("七章", r"第七章"), ("八章", r"第八章")):
    a = h1(pat)
    print(f"   {nm}：L{a[0]+1}" if a else f"   {nm}：無")
c3, c4 = h1(r"第三章")[0], h1(r"第四章")[0]
c5, c6 = h1(r"第五章")[0], h1(r"第六章")[0]
c7, c8 = h1(r"第七章")[0], h1(r"第八章")[0]
c9, jg = h1(r"第八章")[0], h1(r"結語")[0]
print(f"   第三章 {c4-c3} 行・{cjk(seg(c3,c4)):,} 字｜第五章 {c6-c5} 行・{cjk(seg(c5,c6)):,} 字｜第七章 {c8-c7} 行・{cjk(seg(c7,c8)):,} 字｜第八章 {jg-c8} 行・{cjk(seg(c8,jg)):,} 字")

probe("一・六重心智閘門之『形』（門名與序）", r"閘門[一二三四五六]|六重心智閘門|六閘門",
      r"閘門[一二三四五六]|六重心智閘門|六閘門")
probe("一・閘門之『實』（各門判准之詞）", r"境想雙矩陣|使作十九|大悲商主|防衛五階|三勸三諫|污他家|破僧定性|臨界但書|解脫閉環|執行轉軌",
      r"境想|使作|大悲商主|五階光譜|防衛姿態|三勸|污他家|破僧|臨界|解脫閉環|執行轉軌")
probe("一・全流程實檢卡", r"實檢卡|全流程", r"實檢卡|全流程")

probe("二・三階懺悔（作法・取相・無生）", r"作法懺|取相懺|無生.{0,4}懺|三階懺", r"作法懺|取相懺|無生.{0,4}懺|三階懺")
probe("二・梵網見好相之辨", r"見好相|好相|梵網", r"見好相|梵網|驗相")

probe("三・四大隨身自律行動卡", r"行動卡|隨身自律", r"行動卡|隨身自律")
probe("三・合規自檢表（15 項）", r"合規自檢|自檢表|15 項|十五項", r"合規自檢|自檢表|剛性指標")

probe("四・今時五病灶對讀索引", r"五病灶|對讀索引", r"五病灶|對讀索引")

probe("五・判準層級與三大禁令", r"判準層|實體閘門層|母法總綱層|舉報自察層|除偏鏡|惡取空|反咬|抽象扣帽", r"判準層|實體閘門層|母法總綱層|舉報自察層|除偏鏡|惡取空|反咬|扣帽")

probe("六・四維檢索矩陣", r"四維|檢索樞紐|檢索矩陣|极速|極速檢索", r"四維|檢索矩陣|極速檢索|檢索樞紐")

print("\n■ 兩冊現有之『表／卡／清單』類產物（看工具屬性是否已被別形承接）")
for nm, L in (("F1", F1), ("F2", F2)):
    chk = where(r"^\s*-\s*\[\s\]", L)
    tbl = where(r"^\s*\|\s*:?-{3,}", L)
    print(f"   {nm}：勾選框行 {len(chk)}・表分隔行 {len(tbl)}（≈表 {len(tbl)} 張）")
    for i in chk[:3]:
        print(f"      L{i}: {L[i-1].strip()[:64]}")
