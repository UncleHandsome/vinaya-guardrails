# -*- coding: utf-8 -*-
"""第三探：拆分後之指針失指・閘門資產追跡・案卷卡精數（只讀）。"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = {"F1": "起心動念：四分律的心智顯微鏡與唯識解剖.txt",
        "F2": "如法推尋：僧伽憲政、法權審理與修復正義.txt"}
HAN = "〇一二三四五六七八九十百"
CN = re.compile(rf"^#{{1,6}}\s*第([{HAN}]+)章")
CNNUM = {1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八", 9: "九", 10: "十",
         11: "十一", 12: "十二", 13: "十三", 14: "十四", 15: "十五", 16: "十六", 17: "十七",
         18: "十八", 19: "十九", 20: "二十"}
UNI = {v: k for k, v in CNNUM.items()}


def cn2int(s):
    return UNI.get(s)


def spans(lines):
    """回傳 {章序: (起, 迄)}（行索引，半開）。"""
    idx = []
    for i, l in enumerate(lines):
        m = CN.match(l.strip())
        if m:
            n = cn2int(m.group(1))
            if n:
                idx.append((n, i))
    out = {}
    for k, (n, i) in enumerate(idx):
        j = idx[k + 1][1] if k + 1 < len(idx) else len(lines)
        out[n] = (i, j)
    return out


def anchors(text):
    return set(re.findall(r"〔(?:案|案例|制度案卷|案卷)\s*(\d{1,3})", text))


BOOK = {}
for tag, fn in NAME.items():
    lines = (ROOT / fn).read_bytes().decode("utf-8").split("\r\n")
    BOOK[tag] = dict(lines=lines, sp=spans(lines), full="\r\n".join(lines))

print("■ 章塊座標")
for tag, d in BOOK.items():
    print(f"  {tag}：章塊 {len(d['sp'])} 個・錨案號去重 {len(anchors(d['full']))} 個")

print("\n■ 案卷卡精數（#### 【案卷 NN】／【制度案卷 NN】式樣之標題卡）")
for tag, d in BOOK.items():
    cards = [(i + 1, l.strip()) for i, l in enumerate(d["lines"])
             if re.match(r"^#{4,6}\s*[【\[〔]?(?:制度)?案[卷例]", l.strip())]
    print(f"  {tag}：卡 {len(cards)} 張")
    for i, l in cards[:6]:
        print(f"        L{i} {l[:56]}")

print("\n■ 行內『第X章』指針 vs 本冊章塊（自指之可行性）")
for tag, d in BOOK.items():
    bad, ok, noref = [], [], 0
    for i, l in enumerate(d["lines"]):
        if CN.match(l.strip()):
            continue
        for m in re.finditer(rf"第([{HAN}]+)章", l):
            n = cn2int(m.group(1))
            if n is None or n not in d["sp"]:
                bad.append((i + 1, "章次不存在", l.strip()[:70]))
                continue
            a = {int(x) for x in anchors(l)}
            here = {int(x) for x in anchors("\r\n".join(d["lines"][d["sp"][n][0]:d["sp"][n][1]]))}
            miss = sorted(x for x in a if x not in here)
            if miss:
                bad.append((i + 1, f"所指章 {n} 內無案號 {miss}", l.strip()[:70]))
            else:
                ok.append(i + 1)
    print(f"  {tag}：指針命中 {len(ok)}・可疑 {len(bad)}")
    for i, why, s in bad[:14]:
        print(f"        L{i} 【{why}】 {s}")

print("\n■ 原 ver39 第三章『六重心智閘門』資產今落點（關鍵詞逐冊）")
KW = ["閘門一", "閘門二", "閘門三", "閘門四", "閘門五", "閘門六", "六重閘門",
      "境想雙矩陣", "使作十九", "大悲商主", "防衛五階", "三勸三諫", "污他家",
      "破僧定性", "一事不再理", "執行轉軌", "不見罪", "生疑妄動", "臨界但書"]
print(f"  {'關鍵詞':12} F1  F2")
for k in KW:
    print(f"  {k:12} {sum(1 for l in BOOK['F1']['lines'] if k in l):>3}  {sum(1 for l in BOOK['F2']['lines'] if k in l):>3}")

print("\n■ 指南派 F2 而兩冊俱無之案名（98 泉水／97 金布／91 高勝）＋派 F2 而今在 F1 之案")
for k in ["泉水", "金布", "高勝", "提婆達多", "拘睒彌", "富羅那", "大迦葉", "阿難"]:
    f1 = sum(1 for l in BOOK["F1"]["lines"] if k in l)
    f2 = sum(1 for l in BOOK["F2"]["lines"] if k in l)
    print(f"  {k:8} F1 {f1:>3}・F2 {f2:>3}")

print("\n■ F1 第二章第三節（四大神聖邊界・100 行）之首尾與 F2 之結界章對照")
s = BOOK["F1"]["sp"]
a, b = None, None
for i, l in enumerate(BOOK["F1"]["lines"]):
    if "公堂管轄的物理起點與四大神聖邊界" in l:
        a = i
    elif a and re.match(r"^#{1,6}\s*第四節", l.strip()):
        b = i
        break
print(f"  F1 L{a+1}..L{b}＝{b-a} 行")
for i in range(a, min(a + 14, b)):
    print(f"        {i+1}| {BOOK['F1']['lines'][i][:70]}")
