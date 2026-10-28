# -*- coding: utf-8 -*-
"""第六波・收外路第八報告之刀（俱依今檔實測，非照單全收）。

六事（逐條先量，量得始動）：
 甲・F2『在第五戰場地標大案深描中』→ 第五篇（戰場乃 ver39 第六章之舊板塊名，今冊無此級）。
 乙・F2『構成第三章使作十九形態中之「身現相與身口俱現相」』→ 指向實載體《起心動念》附錄四
     『十九形態使作連鎖』；連文非律之逐字（語料唯各別見『若身現相』『若身口俱現相』），故去「」式樣。
 丙・F2『在第四章與第八章中……舉罪五德』→ 第二章與第八章（今冊實測：第二章 L639 差派五德長老・
     第八章 L1735 行舍羅人五德具足；第四章無五德之事）。
 丁・F1『本書在第四章確立了「審查與觀心的雙軌分流」』→ 附錄四（雙軌・軌道甲乙今實見於迎回之六重閘門）。
 戊・F2 第十五章提撕許『出世除名之無時效』而正文跳票 → 迎回 ver39 L6898 之律制句為一目（自源檔截，不重打）。
 己・F2 凡例『現』字之次 → 如實註明其次乃歷版之序，非正文出現之序（作者 288 輪已裁『J 序乃歷版之次』，不改號）。
用法：python -X utf8 _work/pairfix8.py [--write]
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import pairsimp as PS  # noqa: E402

F1 = "起心動念：四分律的心智顯微鏡與唯識解剖.txt"
F2 = "如法推尋：僧伽憲政、法權審理與修復正義.txt"
V = ROOT / "ver39四分律_起心動念心智分析框架_修正版.md"
BAK = ROOT / "_archive/備份/AI清理前"
W = "--write" in sys.argv

FIX = {
    F2: [
        ("在第五戰場地標大案深描中", "在第五篇地標大案深描中"),
        ("構成第三章使作十九形態中之**「身現相與身口俱現相」精神正犯**",
         "構成《起心動念》附錄四『十九形態使作連鎖』中之身現相與身口俱現相（二相律各別有文，連文非逐字），屬精神正犯"),
        ("在第四章與第八章中，佛陀親立之「舉罪五德", "在第二章與第八章中，佛陀親立之「舉罪五德"),
    ],
    F1: [("本書在第四章確立了「審查與觀心的雙軌分流」", "本書在附錄四確立了『審查與觀心的雙軌分流』")],
}
# 己・凡例之如實註（錨：『取「現代因緣所演」之義』之後添一短句）
DECL = ("乃依佛陀『隨犯隨制、因病與藥』之立法本懷", "乃依佛陀『隨犯隨制、因病與藥』之立法本懷",
        "（『現』之次乃歷版之序，非正文出現之序：今冊四境之現01〜現04 依次見於第十四・十五・十六・十六章）")


def doctrine():
    """自 ver39 截律制之句（不重打），並依口徑削去其世俗法之對欄。"""
    src = V.read_bytes().decode("utf-8").replace("\r\n", "\n").split("\n")
    line = next(l for l in src if l.startswith("*   **僧籍資格之剝奪**"))
    return ("#### 三、出世除名之無時效（戒體自壞不隨時日而滅）", "", line.strip(), "")


def main():
    books = {f: (ROOT / f).read_bytes().decode("utf-8").split("\r\n") for f in (F1, F2)}
    hit = {F1: 0, F2: 0}
    for f, rules in FIX.items():
        for old, new in rules:
            L = books[f]
            idx = [i for i, l in enumerate(L) if old in l]
            if len(idx) != 1:
                print(f"  ✗ {f[:6]}・錨命中 {len(idx)}：{old[:32]}")
                continue
            L[idx[0]] = L[idx[0]].replace(old, new)
            hit[f] += 1
            print(f"  ・{f[:6]} L{idx[0] + 1}・治（{old[:18]}…）")
    # 戊・迎回一目（插於第十五章第一節之末目之後）
    L2 = books[F2]
    k = next((i for i, l in enumerate(L2) if l.startswith("#### 二、挪用默擯於白衣任事之咎")), None)
    if k is None:
        print("  ✗ 第十五章第一節之末目求不得")
    else:
        j = next(i for i in range(k, len(L2)) if L2[i].startswith("---"))
        blk = list(doctrine())
        L2[j:j] = blk + [""]
        hit[F2] += 1
        print(f"  ・如法推尋 L{j + 1}・迎回『出世除名之無時效』一目（源 ver39・四行）")
    # 己・凡例如實註
    for i, l in enumerate(L2):
        if "乃依佛陀『隨犯隨制、因病與藥』之立法本懷" in l and "歷版之序" not in l:
            L2[i] = l.replace("之立法本懷", "之立法本懷（『現』之次乃歷版之序，非正文出現之序）", 1)
            hit[F2] += 1
            print(f"  ・如法推尋 L{i + 1}・凡例『現』次如實註")
            break
    bad = sorted({c for f in (F1, F2) for l in books[f] for c in PS.hits(l)})
    print(f"治：心法卷 {hit[F1]}・法制卷 {hit[F2]}・簡形 {bad}")
    if bad:
        raise SystemExit("帶簡形，不落盤")
    if not W:
        print("（試跑：未落盤）")
        return
    for f in (F1, F2):
        p = ROOT / f
        raw = p.read_bytes()
        new = "\r\n".join(books[f]).encode("utf-8")
        (BAK / (f + ".pre_fix8")).write_bytes(raw)
        p.write_bytes(new)
        print(f"  ● {f[:6]}・{len(new)} B・{new.decode('utf-8').count(chr(13)) + 1} 行・SHA "
              f"{hashlib.sha256(raw).hexdigest()[:12]} → {hashlib.sha256(new).hexdigest()[:12]}")


main()
