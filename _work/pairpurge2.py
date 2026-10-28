# -*- coding: utf-8 -*-
"""第三波『去延伸名相』·丑寅二刀：現代學科之譯名歸律語（丑＝詞級通名，寅＝句級唯一錨）。

丑・詞級（一詞數見，全冊同換，須印前後之數）：所換之字須先經語料或兩冊已見形之覆核
    （`_work/pairpurge_terms.py`），外路所擬而語料無形者（見罪不遮・息諍・黨援・由博返約・
     如以破草覆糞・賊匿深穴・Coddaka・Samatha・勘問・有司・折慢・郁結）一概不採——
    『偽託律據』是本專案歷輪第五型之病，寧可用平實漢語，不造假古語。
寅・句級（一句一換，唯一錨，錨不唯一即拒寫）。

護六道同前两輪：唯一錨・不跨界・簡形閘・兩冊俱校畢方落盤・備份 .pre_purge2・清冊。

用法：python -X utf8 _work/pairpurge2.py           # 試跑
      python -X utf8 _work/pairpurge2.py --write   # 落盤
"""
import hashlib
import re
import pairsimp as PS  # noqa: E402
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import importlib                                            # noqa: E402
m = importlib.import_module("pairdelaw")
_simpmap = importlib.import_module("_simpmap")
_simpdict = importlib.import_module("_simpdict")

F2 = "如法推尋：僧伽憲政、法權審理與修復正義.txt"
F1 = "起心動念：四分律的心智顯微鏡與唯識解剖.txt"
FILES = [F2, F1]

# ── 丑・詞級 ──────────────────────────────────────────────────────────────
TOKEN = [
    (F2, "創傷知情調查", "體恤受暴之調查"),
    (F2, "靈性煤氣燈操縱", "借法誑惑之操縱"),
    (F2, "反煤氣燈操縱", "反誑惑操縱"),
    (F1, "煤氣燈操縱", "誑惑操縱"),
    (F2, "部落主義", "朋黨"),
    (F1, "靈性資本主義", "借法圖利養"),
    (F1, "文字尋租", "鑽文義之縫"),
    (F1, "尋租", "鑽文義之縫"),
    (F1, "五階心印漏斗", "五階心印・去枝取幹"),
    (F1, "漏斗", "收攝"),
    (F1, "目標致盲", "作意偏執"),
    (F1, "自尊的防空洞", "自尊的自蔽之窟"),
    (F1, "第二重防空洞", "第二重自蔽之窟"),
    (F1, "防空洞", "自蔽之窟"),
    (F2, "防空洞", "自蔽之窟"),
    (F2, "終局消磁", "終局平息"),
    (F2, "法庭消磁", "公堂平息"),
    (F2, "消磁儀軌", "平息儀軌"),
    (F2, "消磁", "平息"),
    (F1, "情感雷達", "正念照了"),
    (F1, "如雷達般", "如明鏡般"),
    (F2, "世俗公訴重罪", "世俗王法重罪"),
    (F2, "公訴重罪", "王法重罪"),
    (F2, "公訴刑案", "王法重案"),
    (F2, "專案調查官", "僧差舉罪之執事"),
    (F2, "專案調查小組", "所差舉罪之眾"),
    (F2, "專案小組", "所差舉罪之眾"),
    (F2, "專案組", "所差之眾"),
    (F2, "調查官", "勘事之執事"),
    (F2, "單次陳述", "一度陳辭"),
    (F2, "隔室視訊質證", "遣伴屏處質證"),
    (F2, "隔室視訊", "屏處獨對"),
    (F2, "南山三宗心理學", "南山三宗心法"),
    (F2, "既判力保護", "不復翻案之護"),
    (F2, "既判力擬制", "不復翻案之擬"),
    (F2, "既判力", "不復翻案"),
]
# ── 寅・句級（唯一錨） ────────────────────────────────────────────────────
LINE = [
    (F1, "* **動發勝思（驅役色身肌肉）**：神經脈衝穿透大腦前額葉，驅動骨骼肌運動",
     "* **動發勝思（驅役色身）**：意業才動，色身隨之"),
    (F1, "此時大腦迅速關閉對因果報應與世間譏嫌的宏觀感知",
     "此時心識頓失對因果報應與世間譏嫌的宏觀覺照"),
    (F2, "調查團隊必須深諳創傷神經生物學常識，受創者大腦杏仁核被極度恐懼劫持時，神經系統常出現三種本能防衛反應",
     "勘事之執事必須深諳受暴者心境之實況：其人為極度驚怖所制時，身心常現三種本能防衛之態"),
    (F1, "心智啟動了「資本增殖的多巴胺獎賞迴路」", "心智啟動了「利養增殖、貪愛相續之圈」"),
    (F1, "心理學上的**「作意偏執」**", "觀心者共見之病：**「作意偏執」**"),
    (F1, "**難教二法之心理學解剖**", "**難教二法之心識解剖**"),
    (F1, "別住折算的心理學病根", "別住折算之心識病根"),
    (F1, "在心理學上展現了驚人的治療智慧", "於心識之理展現驚人的對治智慧"),
    (F1, "心理學上的「破罐破摔」", "人情之「自棄」"),
    (F1, "為膨脹的自戀實施心理脫敏", "為膨脹之慢心施漸折之治"),
    (F1, "心理脫敏與爆破自戀", "漸折慢心與打破我慢"),
    (F1, "高強度的「心理脫敏治療」", "徹底之「漸折慢心對治」"),
    (F1, "自我強迫症的自戀", "自責成癖之慢心"),
    (F1, "怕犯戒的神經質恐懼（染污惡作）", "怕犯戒之疑悔恐懼（染污惡作）"),
    (F2, "這種盤詰在心理學上被證實會對受創神經系統造成慘烈的**「二次創傷」**",
     "這種盤詰於人情心識之實況屢經證實，會於已受創者**再添新傷**"),
    (F2, "#### 〔專題 10〕夢中失不淨：無意識生理現象與睡眠心理學",
     "#### 〔專題 10〕夢中失不淨：無意識之生理與心識"),
    (F2, "（如高清錄影、指紋血跡、無可推翻之金流流水）", "（如清晰之影像、身業之痕跡、無可推翻之金流流水）"),
    (F2, "#### 二、破戒大賊五相：高風險習氣識別指紋", "#### 二、破戒大賊五相：高風險習氣之識別"),
    (F2, "還是連夜清洗血跡、焚燒文件、更換電腦硬碟？", "還是連夜清洗血跡、焚燒文書、改易記錄之器？"),
    (F2, "通訊群組之截圖、語音留言、監視影像常被作為舉罪之憑",
     "通訊群組之截圖、語音留言、影音記錄常被作為舉罪之憑"),
    (F2, "啟動客觀外圍查證（調閱銀行流水、比對進出貨單據、公共監視",
     "啟動客觀外圍查證（調閱銀行流水、比對進出貨單據、公共影音"),
    (F2, "多瞞一月，心頭的傲慢與自戀就多修築一層自蔽之窟。",
     "多瞞一月，心頭的慢心就多修築一層自蔽之窟。"),
    (F2, "在當代道場治理與爭端審理中", "在今時道場治理與爭端審理中"),
]


def main():
    write = "--write" in sys.argv
    SIMPLE = (set(_simpmap.MAP) | set(_simpdict.MAP)) - set("几")
    errs, ledger, plans, done = [], [], [], []
    for f in FILES:
        raw = (ROOT / f).read_bytes()
        lines = raw.decode("utf-8").split("\r\n")
        fence = m.fence_mask(lines)
        print("=" * 74)
        print("■", f)
        # 丑・詞級
        for fn, old, new in [(x[0], x[1], x[2]) for x in TOKEN if x[0] == f]:
            before = sum(l.count(old) for l in lines)
            if not before:
                done.append(f"丑・{old}")          # 已竟：今冊 0 見，如實記而不以為誤
                continue
            for c in set(new) & SIMPLE:
                errs.append(f"{f[:6]}・新字簡形：{c}｜{new}")
            touched = 0
            for i, l in enumerate(lines):
                if old in l:
                    lines[i] = l.replace(old, new)
                    touched += 1
                    ledger.append(f"{f}\tL{i + 1}\t丑・詞級\t{old} → {new}｜{lines[i].strip()[:40]}")
            after = sum(l.count(old) for l in lines)
            print(f"  丑 『{old}』→『{new}』：{before} 見 → 餘 {after} 見・動行 {touched}")
        # 寅・句級
        for row in LINE:
            if not row or row[0] != f or not isinstance(row[1], str) or not row[1]:
                continue
            old, new = row[1], row[2]
            hits = [i for i, l in enumerate(lines) if old in l]
            if not hits:
                done.append(f"寅・{old[:24]}")      # 已竟：舊錨早為歷刀吞盡，非病
                continue
            if len(hits) > 1:
                errs.append(f"{f[:6]}・寅錨歧義（命中 {len(hits)}）：{old[:30]}")
                continue
            for c in set(new) & SIMPLE:
                errs.append(f"{f[:6]}・新字簡形：{c}｜{new[:20]}")
            i = hits[0]
            o = lines[i]
            lines[i] = o.replace(old, new)
            if fence[i]:
                k = len(o) - len(o.rstrip())
                lines[i] = lines[i].rstrip() + " " * max(0, k)
            ledger.append(f"{f}\tL{i + 1}\t寅・句級\t{o.strip()[:40]} → {lines[i].strip()[:40]}")
            print(f"  寅 L{i + 1}\n     故 {o.strip()[:72]}\n     新 {lines[i].strip()[:72]}")
        simp = [(i + 1, PS.hits(l), l.strip()[:40])
                for i, l in enumerate(lines) if PS.flag(l)]
        if simp:
            errs.append(f"{f[:6]}・刀後簡形 {len(simp)} 行：{simp[:2]}")
        plans.append((f, raw, lines))
    for e in errs:
        print("  ✗", e)
    if errs:
        print("★有誤 → 兩冊俱不落盤")
        return
    (ROOT / "_work" / "pairpurge2_cuts.txt").write_text("\n".join(ledger) + "\n", encoding="utf-8")
    print(f"\n刀口清冊 {len(ledger)} 行 → _work/pairpurge2_cuts.txt")
    for f, raw, lines in plans:
        out = "\r\n".join(lines).encode("utf-8")
        if not write:
            print(f"  {f[:12]}…・試跑未落盤（行 {len(lines)}）")
            continue
        bak = ROOT / "_archive" / "備份" / "AI清理前" / (f + ".pre_purge2")
        bak.write_bytes(raw)
        (ROOT / f).write_bytes(out)
        print(f"  落盤 {f[:12]}…：SHA {hashlib.sha256(raw).hexdigest()[:12]} → {hashlib.sha256(out).hexdigest()[:12]}・"
              f"行 {len(raw.decode('utf-8').split(chr(13) + chr(10)))} → {len(lines)}")


if __name__ == "__main__":
    main()
