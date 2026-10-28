# -*- coding: utf-8 -*-
"""SOP 入帳（第七波・收外路第九報告八項）：新段插於第六波之後；簡形閘只掃自加之行。
用法：python -X utf8 _work/pairlog_sop7.py [--write] <螢幕 trio> <影印 trio> <字面標記之殘>"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import pairsimp as PS  # noqa: E402

W = "--write" in sys.argv
nums = [a for a in sys.argv[1:] if not a.startswith("--")]
S = nums[0] if nums else "112／162／275"
P = nums[1] if len(nums) > 1 else "112／162／275"
STAR = nums[2] if len(nums) > 2 else "圍欄外與圍欄內之字面 `**` 俱 0"

BLOCK = [
    "",
    "- **外路第九報告之收（第七波・2026-10-27・八項俱先量）**：真病六・已改；屬設計一；自犯一。",
    "  治於 `_work/pairfix9.py`（六條俱唯一錨・試跑印名・`--write` 落盤・備 `.pre_fix9`）："
    "① **正文截斷**——法制卷第四章第五節『原則三』只餘一條而以『；』收尾（一輪去法令所遺之脫），"
    "今依律制之語補回二條（追還之責不隨身分而息・管轄之歸處），不取世俗法名；"
    "② **引證之誤**——『律典《四分律》卷一中，此戒之恩給僅見於難提比丘一人』："
    "本地語料實證『與難提比丘波羅夷戒』之文見於『31-37 原文』與『50-60 原文』兩檔（卷三十一〜三十七段・卷五十〜六十段），"
    "卷一唯勿力伽難提殺雇之因緣，遂改如實之稱（此即本專案『本地卷段』之口徑）；"
    "③ **跨冊之引**——心法卷兩處〔調部專題〕冠以《如法推尋》；⑤ **巴利文法之性別誤**——"
    "『與學羯磨（與波羅夷戒·Sikkhamānā）』之 Sikkhamānā 乃陰性名詞（專指式叉摩那），"
    "本地語料亦無『與學』之轉寫可據，故去其標音，唯留漢語；⑥ **虛數之膨脹**——"
    "『三十萬字／三十二萬言／三十餘萬言』三處改『近二十萬言』（實測兩冊都計漢字 198,107）；"
    "⑦ **語意筆誤**——自序『天下林下，風清月朗』改『歸向林下，風清月朗』；"
    "⑧ **表頭擠斷**——二部僧換算矩陣之『比丘尼僧初審院法定人數』被欄寬折為『法／定人數』，"
    "今於表頭立刻意之兩行（<br>），使『法定人數』整詞不破。",
    "  **新器 `_work/pairfencestar.py`（等寬淨圍欄內之殘標記）**：印面字面 `**` 六處俱在 ```text 圍欄之內"
    "（流程圖・框線圖），pandoc 於 <pre> 內本不解析標記，故 `**` 直出；**前一步我以 `<strong>` 代之，於圍欄內同樣不解析，"
    "仍是洩漏**——今一律以等寬之空格淨之（`**`／`<strong>`／`</strong>` → 兩格），框線欄位分毫不動，"
    "器並自證『逐行寬度必等』（不等即擲）。屬設計者：報告所稱『幽靈案號』——自第四波迎回附錄二《判例原典逐條回查索引》"
    "並立凡例第七律『跨冊案號之索』後，18 個抽驗案號俱可循檢 ✓ 非病。",
    f"  **今量**：螢幕版 {S}・影印版 {P}・{STAR}。",
]


def main():
    p = ROOT / "列印SOP.md"
    raw = p.read_bytes().decode("utf-8")
    NL = "\r\n" if "\r\n" in raw else "\n"
    L = raw.split(NL)
    if any("外路第九報告之收" in l for l in L):
        i = next(k for k, l in enumerate(L) if "今量**：螢幕版" in l)
        L[i] = L[i].split("  **今量**")[0].rstrip() + chr(10) + BLOCK[-1].strip()
        print("（第七波已在帳，更新今量一行）")
    else:
        j = next(k for k, l in enumerate(L) if "外路第八報告之收" in l)
        x = next(k for k in range(j, len(L)) if "今量**：螢幕版" in L[k])
        L[x + 1:x + 1] = BLOCK
    bad = sorted({c for l in BLOCK for c in PS.hits(l)})
    print(f"新文簡形 {len(bad)} 枚 {bad}｜SOP {len(raw.split(NL))} → {len(L)} 行")
    if bad:
        raise SystemExit("帶簡形，不落盤")
    if W:
        p.write_bytes(NL.join(L).encode("utf-8"))
        print("● 落盤")


main()
