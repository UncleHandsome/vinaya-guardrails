# -*- coding: utf-8 -*-
"""去現代法令·第九刀（壬・殘語之補）：庚辛二刀後仍不順之語，逐句歸律；並除三處『失指』。

庚辛既去其殼，間有句意不接・圖號不稱・指針無家者，此刀補之。
護五道：唯一錨・不跨界・簡形閘・備份＋SHA・圍欄內換字須自動補格保欄。
new 內之 '\\n' 許作換行（補句之用）；落盤一律以 \\r\\n 歸一，絕不產生 CR-CRLF 之疊。

失指之源（實測）：ver39 第三章『照鏡察心：六重心智閘門』544 行・15,182 字（約 22 頁），
Split 時未入任何一冊，故『第三章閘門二／四』於兩冊俱無落點。本刀只除其虛指，不代作者裁迎回與否。
  F1 L3114『六重心智門』・L3139『六重閘門』同因之宣稱，留待乙組之裁（報而不治）。

用法：python -X utf8 _work/pairdelaw4.py          # 試跑
      python -X utf8 _work/pairdelaw4.py --write  # 落盤
"""
import hashlib
import importlib
import pairsimp as PS  # noqa: E402
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
m = importlib.import_module("pairdelaw")
_simpmap = importlib.import_module("_simpmap")
_simpdict = importlib.import_module("_simpdict")

F2 = "如法推尋：僧伽憲政、法權審理與修復正義.txt"
F1 = "起心動念：四分律的心智顯微鏡與唯識解剖.txt"
FILES = [F2, F1]

# (檔, 圍欄內?, old, new)
FIX = [
    (F2, False, "> 當要求奉獻時，長老高談「出家無我、發心消業」，隨意延長工時、扣減津貼；",
     "> 當要求奉獻時，長老高談「出家無我、發心消業」，隨意延長工時、扣減津貼；\n"
     "> 當爆發違紀糾紛時，長老又突然搬出「出家清規」，未經白眾當下將人擯出、逐出道場，令常住蒙羞。"),
    (F2, False, "而應依第三章閘門四轉軌啟動「作不見罪舉羯磨」",
     "而應依『見罪防衛』之軌轉軸啟動「作不見罪舉羯磨」"),
    (F2, False, "（詳見第三章閘門四與第六章〔案例 21〕）。然而，若將出世默擯隨意挪用至現代世俗人事管理，將直接引爆毀滅性的法律災難。",
     "（其事之全貌，見心法卷《起心動念》【案卷 21】闡陀連環抗拒）。然而，若將出世默擯隨意挪用至道場人事，"
     "便是以戒法作壓人之具，直接傷及他人慧命與僧團和合。"),
    (F2, True, "【默擯之現代勞動法防禦防火牆】", "【默擯之界：出世自治與白衣禁區】"),
    (F2, True, "【出世自治合憲領域（比丘對比丘）】", "【出世如法自治領域（比丘對比丘）】"),
    (F2, True, "【世俗勞僱絕對禁區（受薪員工/在家人）】", "【白衣任事絕對禁區（受薪職工/在家人）】"),
    (F2, True, "· ★ 世俗法直接定性為：【違法職場霸凌】！", "· ★ 直接定性為：【惡意職場霸凌】！"),
    (F2, True, "· 雇主負侵權損害賠償與給付資遣費責任！", "· 主事者自負其咎，如法賠償其損！"),
    (F2, False, "#### 二、挪用默擯於世俗勞僱之律制定性：違法職場霸凌（Workplace Bullying）",
     "#### 二、挪用默擯於白衣任事之咎：職場霸凌（Workplace Bullying）"),
    (F2, False, "本節圍繞全書核心演繹判例〔案例 現04〕，建立防禦大廈：",
     "本節圍繞全書核心演繹判例〔案例 現04〕，立名實之辨："),
    (F1, False, "（如閘門二之生疑妄動，不免其責）", "（心生疑而妄動，不免其責）"),
]
FALSE_SIMP = set("几")          # 繁簡同形之正字（案几）


def dwidth(s):
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F", "A") else 1 for c in s)


def main():
    write = "--write" in sys.argv
    SIMPLE = (set(_simpmap.MAP) | set(_simpdict.MAP)) - FALSE_SIMP
    errs, ledger = [], []
    books = {}
    for fn in FILES:
        raw = (ROOT / fn).read_bytes()
        books[fn] = [raw, raw.decode("utf-8").split("\r\n")]
    for fn, infence, old, new in FIX:
        for c in set(new.replace("\n", "")) & SIMPLE:
            errs.append(f"{fn[:8]}・新文簡形：{c}｜{new[:24]}")
        lines = books[fn][1]
        fence = m.fence_mask(lines)
        hits = [i for i, l in enumerate(lines) if old in l and fence[i] == infence]
        if not hits:
            continue                              # 已竟：舊錨為歷刀吞盡，刀可重入
        if len(hits) > 1:
            errs.append(f"{fn[:8]}・錨歧義（命中 {len(hits)}・欄{'內' if infence else '外'}）：{old[:32]}")
            continue
        if old in new and new.replace("\n", "\r\n") in "\r\n".join(lines):
            continue                              # 插形之刀（new 含 old）：new 今已在檔＝已竟，再落即重行
        i = hits[0]
        at = lines[i].index(old)
        head, tail = lines[i][:at], lines[i][at + len(old):]
        if infence:
            k = len(tail) - len(tail.lstrip(" "))
            last = new.split("\n")[-1]
            tail = " " * max(0, k + dwidth(old) - dwidth(last)) + tail.lstrip(" ")
        orig = lines[i]
        lines[i] = head + new + tail
        ledger.append((fn, i + 1, infence, orig, lines[i]))
    for fn, i, infence, o, w in ledger:
        print(f"  {fn[:6]}… L{i}［欄{'內' if infence else '外'}］")
        print(f"     故 {o.strip()[:86]}")
        print(f"     新 {w.strip()[:86]}")
    print("=" * 74)
    for e in errs:
        print("  ✗", e)
    if errs:
        print("★有誤 → 俱不落盤")
        return
    for fn in FILES:
        raw, lines = books[fn]
        flat = []
        for l in lines:
            flat.extend(l.split("\n"))
        simp = [(i + 1, PS.hits(l), l.strip()[:44])
                for i, l in enumerate(flat) if PS.flag(l)]
        b = raw.decode("utf-8").split("\r\n")
        print(f"■ {fn[:16]}…｜行 {len(b)} → {len(flat)}・法名 {sum(len(m.HAS_LAW.findall(x)) for x in b)}"
              f" → {sum(len(m.HAS_LAW.findall(x)) for x in flat)}・簡形 {len(simp)} 行 {simp[:2]}")
        if simp:
            print("  ✗ 刀後仍有簡形 → 不落盤")
            return
        if write:
            bak = ROOT / "_archive" / "備份" / "AI清理前" / (fn + ".pre_delaw4")
            bak.write_bytes(raw)
            data = "\r\n".join(flat).encode("utf-8")
            (ROOT / fn).write_bytes(data)
            print(f"   落盤：SHA {hashlib.sha256(raw).hexdigest()[:12]} → {hashlib.sha256(data).hexdigest()[:12]}"
                  f"・{len(data)} B・備份 {bak.relative_to(ROOT)}")
        else:
            print("   （試跑：未落盤）")
    (ROOT / "_work" / "pairdelaw4_cuts.txt").write_text(
        "\n".join(f"{f}\tL{i}\t欄{'內' if g else '外'}\t{o.strip()[:48]} → {w.strip()[:48]}"
                 for f, i, g, o, w in ledger) + "\n", encoding="utf-8")
    print(f"刀口清冊 {len(ledger)} 行 → _work/pairdelaw4_cuts.txt")


if __name__ == "__main__":
    main()
