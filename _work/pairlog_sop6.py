# -*- coding: utf-8 -*-
"""SOP 入帳（第六波・收外路第八報告）：新段插於第五波之後；新文先過簡形閘，且只掃自加之行。
用法：python -X utf8 _work/pairlog_sop6.py [--write] <螢幕 trio＋隔頁> <影印 trio>"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import pairsimp as PS  # noqa: E402

W = "--write" in sys.argv
nums = [a for a in sys.argv[1:] if not a.startswith("--")]
S = nums[0] if nums else "112／162／275"
P = nums[1] if len(nums) > 1 else "112／162／275"

BLOCK = [
    "",
    "- **外路第八報告之收（第六波・2026-10-27，八項逐條量今檔）**：八項中**真病五**・**偽病灶一**・**前裁所駁一**・**屬設計者二**。",
    "  真病而治：① **目錄須從正文**——心法卷第三篇四章之案序與正文全錯（第七章 16 在 02/05 前、第八章 55 在 19 前、"
    "第九章 89 在 42 前、第十章 13 在 12 前），且雙聯卡之次號（案20）目錄漏列；治於 `_work/pairf1toc.py`"
    "（以正文卡序為法源重列，單號案保留作者短注，雙聯卡合為『〔案19&20〕卡題首語』，**重建後自覆核序合方落盤**）。"
    "② **法制卷向無逐節之目**——今印面唯結構全貌圖；治於 `_work/pairf2toc.py`（由正文自算篇/章/節/附錄/終卷，"
    "生成【全書標準總目錄】（五篇二十章・83節・附錄四篇）插於凡例之後、第一篇之前；舊『今冊附錄之目』隨之退場，名單不兩抄；"
    "**可重入**：再跑即整塊重建）。③ **失指四條**：「第五戰場」→第五篇・「第三章使作十九形態」→《起心動念》附錄四"
    "『十九形態使作連鎖』（連文非律之逐字，去「」式樣）・「第四章與第八章……舉罪五德」→第二章與第八章"
    "（實測：第二章差派五德長老・第八章行舍羅人五德具足）・心法卷「第四章確立雙軌分流」→附錄四（雙軌今實見於迎回之六重閘門）。"
    "④ **提撕跳票**：法制卷第十五章章首許『出世除名之無時效』而通章無其文；治於迎回 ver39 之律制句為一目"
    "（『三、出世除名之無時效』・自源檔截，不重打，並依口徑削去其世俗法對欄）。",
    "  偽病灶一：報告稱 p141 等處有 `\\[` `\\]` markdown escapes 字面 178 枚——今檔實測 **0**（語料與本冊俱作〔〕）。"
    "前裁所駁一：『現代演繹判例 現01→03→04→02 宜重編號』——作者 2026-10-26 已裁「J 序乃歷版之次」，不改號；"
    "改於凡例如實註『『現』之次乃歷版之序，非正文出現之序』。屬設計者二：**合冊兩卷頁碼各自起訖**（接排之本性如此，"
    "分卷檔俱在）與 **ASCII 圖於非等寬字體之縮排**（已由 `fit_pre_blocks`＋`refit_pre` 幾何回量，唯餘超寬圖一處安受）。",
    "  **合冊之隔頁（新制）**：`_print/build_pair.py` 之 `merge()` 今於兩卷間插『姊妹卷合璧說明』一頁（頁數自算，"
    "並列於書籤；後卷書籤隨之 +1），其文宣示『各卷頁碼自為起訖、檢索以書籤與章號為準、跨卷之引依第七律以號索之』。"
    f"  **今量**：螢幕版 {S}・影印版 {P}（書籤 416／433／850）。",
]


def main():
    p = ROOT / "列印SOP.md"
    raw = p.read_bytes().decode("utf-8")
    NL = "\r\n" if "\r\n" in raw else "\n"
    L = raw.split(NL)
    if any("外路第八報告之收" in l for l in L):
        i = next(k for k, l in enumerate(L) if "今量**：螢幕版" in l)
        L[i] = BLOCK[-1].replace("    ", "")
        print("（第六波已在帳，只更新今量一行）")
    else:
        j = next(k for k, l in enumerate(L) if "案號對合之刀法源" in l)
        x = next(k for k in range(j, len(L)) if L[k].startswith("  **兩式今量**"))
        L[x + 1:x + 1] = BLOCK
    bad = sorted({c for l in BLOCK for c in PS.hits(l)})
    print(f"新文簡形 {len(bad)} 枚 {bad}｜SOP {len(raw.split(NL))} → {len(L)} 行")
    if bad:
        raise SystemExit("帶簡形，不落盤")
    if W:
        p.write_bytes(NL.join(L).encode("utf-8"))
        print("● 落盤")


main()
