# -*- coding: utf-8 -*-
"""第二輪『去匠氣』之六刀靶量（作者親裁 2026-10-26）：逐刀先量落點・行數・字數・句式重複，再定刀。

六刀之名：①寫作鷹架與自我說明 ②商管／科技潮流名相 ③官僚公文格式與勾選表格 ④經院死角（變根）
          ⑤疲勞轟炸之自我防禦免責宣告 ⑥模板化之章末抒情留白
用法：python -X utf8 _work/pairtrim_probe.py
"""
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import importlib                                            # noqa: E402
m = importlib.import_module("pairdelaw")

F2 = (ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt").read_bytes().decode("utf-8").split("\r\n")
F1 = (ROOT / "起心動念：四分律的心志顯微鏡與唯識解剖.txt".replace("志", "智")).read_bytes().decode("utf-8").split("\r\n")
BOOKS = [("F2 法制卷", F2), ("F1 心法卷", F1)]


def han(s):
    return sum(1 for c in s if "\u4e00" <= c <= "\u9fff")


def block(lines, start_idx):
    """自 start_idx（0 基）之標題起，至同級或更高級標題前。"""
    lv = m.level(lines[start_idx].strip())
    j = start_idx + 1
    n = len(lines)
    while j < n:
        s = lines[j].strip()
        if m.ANY_HEAD.match(s) and m.level(s) <= lv:
            break
        j += 1
    return j


def find_head(lines, pat):
    return [i for i, l in enumerate(lines) if re.match(r"^#{1,6}\s", l.strip()) and re.search(pat, l)]


def w(label, rx):
    tot = 0
    for name, lines in BOOKS:
        hits = [(i + 1, l.strip()) for i, l in enumerate(lines) if re.search(rx, l)]
        cnt = sum(len(re.findall(rx, l)) for _, l in hits)
        tot += cnt
        print(f"  {label:14s}｜{name} 見 {cnt:3d}・行 {len(hits):3d}  " + " ".join(f"L{a}" for a, _ in hits[:14]))
    return tot


print("=" * 78)
print("【刀一・寫作鷹架與自我說明】")
for name, lines in BOOKS:
    for pat in (r"修辭範式|寫作紀律|防禦性鷹架", r"作者|本冊之例|全書自制", r"本框架|本冊自建|本冊之"):
        hs = find_head(lines, pat)
        if pat.startswith("修辭"):
            print(f"  {name}｜『修辭範式』類標題 {len(hs)} 枚")
            for i in hs:
                j = block(lines, i)
                print(f"      L{i + 1}〜{j}（{j - i} 行・{han(chr(10).join(lines[i:j])):,} 字）{lines[i].strip()[:44]}")
for name, lines in BOOKS:
    n = sum(len(re.findall(r"本框架|本冊|本書|全書", l)) for l in lines)
    print(f"  {name}｜自指語（本框架／本冊／本書／全書）凡 {n} 見")

print("=" * 78)
print("【刀二・商管與科技潮流名相】")
for rx, lab in [(r"AI|人工智慧|演算法|Deepfake|深偽|大語言模型|大模型|生成式", "AI／演算法／深偽"),
                (r"Zoom|Teams|LINE|Slack|微信|WhatsApp|YouTube|Faceboo|臉書|釘釘", "特定軟體名"),
                (r"KPI|履約|標竿|賦能|流程優化|盤點|落地|矩陣|接口|閉環|場景|維度", "企管黑話"),
                (r"打卡|考勤|工時|加班費|績效|職缺|人資|員工|主管|办公室|辦公室", "職場語彙"),
                (r"SOP|合規|風控|內部控制|稽核|董事|監察人|股東|執行長", "治理黑話")]:
    w(lab, rx)

print("=" * 78)
print("【刀三・官僚公文格式與勾選表格】")
for rx, lab in [(r"法審字第|字〔?\d{0,4}〕?第", "案號『X審字第』"),
                (r"\[\s*\]|□|☑|❏", "勾選方框"),
                (r"戒臘.{0,4}夏|簽署|簽章|捺指|日期：?\s*年", "簽章欄"),
                (r"四階十六項|審計表|檢查表|表單|表格式", "表單字樣")]:
    w(lab, rx)
for name, lines in BOOKS:
    for i in find_head(lines, r"審計表|自律宣告|四署"):
        j = block(lines, i)
        print(f"  {name}｜L{i + 1}〜{j}（{j - i} 行・{han(chr(10).join(lines[i:j])):,} 字）{lines[i].strip()[:46]}")

print("=" * 78)
print("【刀四・經院死角：自然變根】")
for name, lines in BOOKS:
    hits = [(i + 1, l.strip()[:56]) for i, l in enumerate(lines) if re.search(r"變根", l)]
    print(f"  {name}｜『變根』{len(hits)} 行")
    for a, t in hits[:12]:
        print(f"      L{a}|{t}")
    for i in find_head(lines, r"變根"):
        j = block(lines, i)
        print(f"      ★塊 L{i + 1}〜{j}（{j - i} 行・{han(chr(10).join(lines[i:j])):,} 字）{lines[i].strip()[:46]}")

print("=" * 78)
print("【刀五・自我防禦之repeat 警示】")
for name, lines in BOOKS:
    ti = find_head(lines, r"章首提撕|提撕")
    yan = [(i + 1, l.strip()[:44]) for i, l in enumerate(lines) if re.search(r"嚴禁", l)]
    selfguard = [(i + 1, l.strip()[:52]) for i, l in enumerate(lines)
                 if re.search(r"不可(?:拿|用|把)|切勿|不許以此|向外照人|施虐|過載|自虐|以清淨自高", l)]
    print(f"  {name}｜提撕盒 {len(ti)} 枚・『嚴禁』{len(yan)} 行・自防語 {len(selfguard)} 行")
    for a, t in selfguard[:16]:
        print(f"      L{a}|{t}")
    for a in find_head(lines, r"心靈憲章|三十二字|法架自捨|出堂洗心"):
        print(f"      ○收束處 L{a}|{lines[a].strip()[:44]}")

print("=" * 78)
print("【刀六・章末留白／指針之模板度】")
for name, lines in BOOKS:
    kinds = Counter()
    rows = []
    for i, l in enumerate(lines):
        s = l.strip()
        mm = re.match(r"^#{1,6}\s*【(章末留白|本章留白|本章章末指針|林下留白|章末指針|出堂洗心)([^】]*)】", s)
        if mm:
            kinds[mm.group(1)] += 1
            rows.append((i + 1, s[:60]))
    print(f"  {name}｜章末之塊形制 {dict(kinds)}・共 {len(rows)} 枚")
    for a, t in rows:
        print(f"      L{a}|{t}")
    body = "\n".join(lines)
    for tok in ("吃茶去", "井邊", "流雲", "齋堂", "放下的法袍", "法袍", "挑水", "松風"):
        print(f"      句式之料『{tok}』{body.count(tok)} 見")
