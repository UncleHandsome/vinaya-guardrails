# -*- coding: utf-8 -*-
"""第二輪細量：刀一至刀六之落點邊界（含審計表之内瓤與警示語之逐章分布）。"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import importlib                                            # noqa: E402
m = importlib.import_module("pairdelaw")

F2 = (ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt").read_bytes().decode("utf-8").split("\r\n")
F1 = (ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt").read_bytes().decode("utf-8").split("\r\n")


def han(s):
    return sum(1 for c in s if "\u4e00" <= c <= "\u9fff")


def block(lines, i):
    lv = m.level(lines[i].strip())
    j = i + 1
    n = len(lines)
    while j < n:
        s = lines[j].strip()
        if m.ANY_HEAD.match(s) and m.level(s) <= lv:
            break
        j += 1
    return j


def heads(lines):
    return [i for i, l in enumerate(lines) if m.ANY_HEAD.match(l.strip())]


print("【一・卷首三塊之邊界（F2）】")
for pat in (r"四大決策群體", r"修辭範式", r"受眾", r"凡例"):
    for i in [k for k in heads(F2) if re.search(pat, F2[k])]:
        j = block(F2, i)
        print(f"  L{i + 1}〜{j - 1}（{j - i} 行・{han(chr(10).join(F2[i:j])):,} 字・約 {(j - i) / 34:.1f} 頁）{F2[i].strip()[:48]}")

print("\n【二・作者自辯語之實存檢（刀一之靶是否已在書中兌現）】")
for rx in (r"無意立某制", r"讀者切勿混淆", r"並非要讀者", r"不是要拿", r"本章不是要", r"作者在此"):
    for tag, lines in (("F2", F2), ("F1", F1)):
        hits = [(i + 1, l.strip()[:44]) for i, l in enumerate(lines) if re.search(rx, l)]
        if hits:
            print(f"  『{rx}』{tag} {len(hits)} 見 → {hits[:3]}")

print("\n【三・第二十章 第一節之內的層結構（審計表：哪些是問句、哪些是表格）】")
for i in [k for k in heads(F2) if re.search(r"公堂審計表|自律宣告|四署", F2[k].strip())]:
    j = block(F2, i)
    print(f"  ◆ L{i + 1}〜{j - 1}（{j - i} 行・{han(chr(10).join(F2[i:j])):,} 字）{F2[i].strip()[:46]}")
    for k in range(i, j):
        s = F2[k].strip()
        if m.SEC_HEADING.match(s) or s.startswith("```") or re.match(r"^\[\s*\]", s) or "法審字第" in s:
            print(f"      L{k + 1}|{s[:64]}")

print("\n【四・警示語之逐章分布（刀五）】")
GUARD = r"法規施虐|良知過載|以清淨自高|向外照人|施虐|酷吏|獵巫|濫用本書|不得用來打人"
for tag, lines in (("F2", F2), ("F1", F1)):
    cur = None
    tally = {}
    for i, l in enumerate(lines):
        mm = re.match(r"^#{1,6}\s*(第[〇一二三四五六七八九十]+章[　 ][^\n]{0,18})", l.strip())
        if mm:
            cur = mm.group(1)
        if cur and re.search(GUARD, l):
            tally.setdefault(cur, []).append(i + 1)
    print(f"  {tag}・涉警示之章 {len(tally)} 個・共 {sum(len(v) for v in tally.values())} 行")
    for k, v in tally.items():
        print(f"      {k}｜{len(v)} 行 {v[:6]}")

print("\n【五・變根（刀四）之殘跡與他處】")
for i, l in enumerate(F2):
    if re.search(r"變根|二形|轉依", l):
        print(f"  F2 L{i + 1}|{l.strip()[:72]}")

print("\n【六・商管潮流名相之窄口徑（刀二，不含自制之『矩陣・閉環』）】")
NARROW = [("KPI/標竿/賦能/落地/盤點/接口/場景/優化/量化/迭代", r"KPI|標竿|賦能|落地|盤點|接口|場景|優化|量化|迭代|反饋迴路"),
          ("打卡/考勤/工時/加班/績效/人資/辦公室", r"打卡|考勤|工時|加班|績效|人資|辦公室"),
          ("AI/演算法/深偽/大模型", r"AI|人工智慧|演算法|Deepfake|深偽|大模型"),
          ("特定軟體", r"Zoom|Teams|LINE|Slack|微信|WhatsApp|YouTube|臉書"),
          ("合規/風控/內部控制/稽核/董事/監察人/股東/執行長/法人",
           r"合規|風控|內部控制|稽核|董事|監察人|股東|執行長|法人")]
for tag, lines in (("F2", F2), ("F1", F1)):
    for lab, rx in NARROW:
        hits = [(i + 1, len(re.findall(rx, l))) for i, l in enumerate(lines) if re.search(rx, l)]
        print(f"  {tag}｜{lab[:26]:28s} 見 {sum(h[1] for h in hits):3d}・行 {len(hits):3d} "
              + " ".join(f"L{a}" for a, _ in hits[:10]))
