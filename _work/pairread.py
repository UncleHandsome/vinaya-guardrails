# -*- coding: utf-8 -*-
"""三冊可讀性之同尺體檢：《護欄》vs《起心動念》vs《如法推尋》（只讀）。

口徑（與護欄冊 hlannot ④ 同制）：印面段落＝圍欄與表列之外、相鄰之非空行併為一段
（行尾雙空格乃硬換行，不另起段——pandoc 之實形）。
用法：python -X utf8 _work/pairread.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS = [("護欄", "佛陀的護欄 四分律比丘與比丘尼戒的行為心理學解析.txt"),
         ("起心動念", "起心動念：四分律的心智顯微鏡與唯識解剖.txt"),
         ("如法推尋", "如法推尋：僧伽憲政、法權審理與修復正義.txt")]

TERM = ["作意", "審慮思", "決定思", "動發勝思", "五遍行", "三時心", "勝解", "行捨", "末那識",
        "阿賴耶", "心所", "闕緣", "境想", "五受", "覆心所", "二諦", "正理", "羯磨", "波羅夷",
        "偷蘭遮", "突吉羅", "提舍尼", "除斥期間", "既判力", "信託", "管轄", "證據能力", "三線模型"]
LIVELY = ["紅隊", "資本家", "由旬", "洗澡水", "貨郎", "防空洞", "冷汗", "心跳", "狂跳", "胃"]


def cjk(s):
    return sum(1 for c in s if "\u4e00" <= c <= "\u9fff")


def blocks(lines):
    out, cur, inf = [], [], False
    for l in lines:
        if re.match(r"^\s*```", l):
            inf = not inf
            if cur:
                out.append("\n".join(cur))
                cur = []
            continue
        if inf:
            continue
        if not l.strip() or l.strip().startswith(("#", "|", ">", "* ", "- ", "1.", "2.", "3.")):
            if cur:
                out.append("\n".join(cur))
                cur = []
            continue
        cur.append(l)
    if cur:
        out.append("\n".join(cur))
    return out


for nm, fn in BOOKS:
    p = ROOT / fn
    raw = p.read_bytes().decode("utf-8-sig").replace("\r\n", "\n")
    lines = raw.split("\n")
    n = cjk(raw)
    bs = blocks(lines)
    lens = sorted(cjk(b) for b in bs if cjk(b) > 0)
    med = lens[len(lens) // 2] if lens else 0
    over = [x for x in lens if x > 320]
    dialog = sum(len(re.findall(r"「[^」]{6,}」", l)) for l in lines)
    qm = sum(l.count("？") for l in lines)
    sec = sum(1 for l in lines if re.match(r"^#{1,6}\s", l.strip()))
    print("=" * 72)
    print(f"■ {nm}｜{len(lines)} 行・印面漢字 {n:,}・標題 {sec} 枚")
    print(f"   段落 {len(lens)}・中位 {med} 字・最長 {lens[-1] if lens else 0} 字・>320 字者 {len(over)} 段")
    print(f"   語話「」每千字 {dialog / n * 1000:.2f}・問號每千字 {qm / n * 1000:.2f}・"
          f"第二人稱（你／汝）每千字 {sum(l.count('你') + l.count('汝') for l in lines) / n * 1000:.2f}")
    top = sorted(((t, sum(l.count(t) for l in lines)) for t in TERM), key=lambda x: -x[1])
    print("   術語密度（每千字）：" + "・".join(f"{t} {c / n * 1000:.1f}" for t, c in top[:10]))
    print("   全術語表命中合计每千字 %.1f" % (sum(c for _t, c in top) / n * 1000))
    lv = [(t, sum(l.count(t) for l in lines)) for t in LIVELY]
    print("   生動語彙：" + "・".join(f"{t}{c}" for t, c in lv if c))

print("\n" + "=" * 72)
print("■ 報告所舉《護欄》之例，是否實有其文")
hl = (ROOT / BOOKS[0][1]).read_bytes().decode("utf-8-sig").split("\n")
for w in ["紅隊", "宗教資本家", "三由旬", "羊毛", "洗澡水", "職場", "反性騷擾"]:
    hit = next(((i + 1, l.strip()[:66]) for i, l in enumerate(hl) if w in l), None)
    print(f"   『{w}』：", "L%d %s" % hit if hit else "★ 護欄無此語（報告舉例不實）")

print("\n■ 心法卷各章之『章首提撕盒』與『第一篇之抽象度』")
f1 = (ROOT / BOOKS[1][1]).read_bytes().decode("utf-8-sig").split("\n")
ts = [(i + 1, l.strip()[:56]) for i, l in enumerate(f1) if "提撕" in l and l.strip().startswith("#")]
print(f"   章首提撕（標題形）{len(ts)} 枚")
for i, s in ts[:6]:
    print(f"      L{i}: {s}")
first_case = next((i + 1 for i, l in enumerate(f1) if re.match(r"^#{1,6}\s*第七章", l.strip())), 0)
print(f"   第七章（案卷首章）起於 L{first_case}／全書 {len(f1)} 行 → 讀者須先讀 {first_case / len(f1) * 100:.0f}% 之框架")
