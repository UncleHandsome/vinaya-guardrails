# -*- coding: utf-8 -*-
"""SOP 入帳（第五波・案號對合）：新段插於第四波之後；新文先過簡形閘（共器口徑）。
用法：python -X utf8 _work/pairlog_sop5.py [--write] <螢幕頁 trio> <影印頁 trio>"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import pairsimp as PS  # noqa: E402

W = "--write" in sys.argv
nums = [a for a in sys.argv[1:] if not a.startswith("--")]
SCREEN = nums[0] if nums else "113／159／272"
PRINT = nums[1] if len(nums) > 1 else "（影印版同數，另行覆核）"

BLOCK = [
    "",
    "- **案號對合之刀法源（第五波・2026-10-27）**：共器 `_work/paircase_lib.py`——『此冊能否找到某案』唯三形載體"
    "（卡題 `【案卷 NN】`・表行首格 `| **【案例 NN】…`・附錄索引行），`findable()` 與 `cites()` 俱現算，"
    "**刀・尺・產生器三處同取此一定義**（名單勿兩抄）；跨冊之約（凡例第七律）之文亦立於此。"
    "刀 `_work/paircite_note.py` 三事：立第七律『跨冊案號之索』並改標題六律→七律（**內引之舊稱須同時歸位**，"
    "兩冊各一處）、案號引用歸本冊成例（心法卷 `〔案NN〕`・法制卷 `〔案例 NN〕`帶空格，實治 438 處）、"
    "ver39 舊章次『詳見第六章〔案例 76〕』改『詳見第五篇』。"
    "尺 `_work/pairrefchk.py` 加『案號對合』一軸並自印管轄（今 645 條引・心法卷可檢 27／法制卷 102），"
    "立尺當日逮失指 30 處（含心法卷正文舊有之 案99・案84，非唯迎回區）。"
    "**裁**：逐行冠姊妹冊名之方案擲回——實測 530 枚會碎文氣，改卷首立約一行而足。",
    f"  **兩式今量**：螢幕版 {SCREEN}・影印版 {PRINT}。"
    "近空白頁（<40 字）：心法卷 7・法制卷 4・合冊 11，俱篇 Banner 與章末設計留白，非病。"
    "自犯一則：**同日兩度落盤者，同 tag 之備份僅存末次**（`.pre_cases` 被第二寫覆蓋，第一步回退之力遂失）"
    "——凡一日再動同一檔，備份名須帶輪號或時間戳。",
]


def main():
    p = ROOT / "列印SOP.md"
    raw = p.read_bytes().decode("utf-8")
    NL = "\r\n" if "\r\n" in raw else "\n"
    L = raw.split(NL)
    i = next(k for k, l in enumerate(L) if "案號對合之刀法源" in l) if any("案號對合之刀法源" in l for l in L) else None
    if i is not None:
        print("（第五波已在帳，更新其兩式今量一行）")
        L[i + 1] = BLOCK[2]
    else:
        j = next(k for k, l in enumerate(L) if "不迎回之項（依一・二・三令自裁" in l)
        k = next(x for x in range(j, len(L)) if L[x].startswith("  **回流後之字面刀"))
        L[k + 1:k + 1] = BLOCK
    bad = sorted({c for l in BLOCK for c in PS.hits(l)})
    print(f"新文簡形（引號外）{len(bad)} 枚 {bad}｜SOP {len(raw.split(NL))} → {len(L)} 行")
    if bad:
        raise SystemExit("新文帶簡形，不落盤")
    if W:
        p.write_bytes(NL.join(L).encode("utf-8"))
        print("● 落盤")


main()
