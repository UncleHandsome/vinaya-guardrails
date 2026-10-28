# -*- coding: utf-8 -*-
"""清理後之驗收尺：量產物（非量口徑），並自量宣稱與實測之對合。

用法：python -X utf8 _work/ai_sweep_check.py
六目：
  1 正文無改：新檔每一行必出自原檔（子序列比對，逐行點名例外）
  2 交談殘跡歸零：脚手標題／客套語／輪次自指／指令句
  3 結構對合：書名横幅・篇・章之實測數 vs 卷首宣稱
  4 章不重複：同名章標題唯一（異文者點名）
  5 markdown 安全：圍欄成雙・分隔線不黏正文（防 setext 誤升）
  6 尺之自證：負測——餵入已知有病之樣本，須點名真答案
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ai_sweep_clean as C   # 刀尺同源：脚手之判一律取清理器之定義

ROOT = Path(__file__).resolve().parents[1]
PAIRS = [
    ("起心動念：四分律的心智顯微鏡與唯識解剖.txt",
     dict(pian=4, zhang=12, book="《起心動念：四分律的心智顯微鏡與唯識解剖》")),
    ("如法推尋：僧伽憲政、法權審理與修復正義.txt",
     dict(pian=5, zhang=20, book="《如法推尋：僧伽憲政、法權審理與修復正義》")),
]
BAK = ROOT / "_archive" / "備份" / "AI清理前"

HEADING = re.compile(r"^#{1,6}\s")
FENCE = re.compile(r"^\s*```")
RULE = re.compile(r"^\s*(?:-{3,}|\*{3,})\s*$")
# 交談殘跡之硬判式（不含「這是一場」等可与正文撞車者；輪次自指另由 C.CHAT_LINE 守）
HARD = re.compile(
    r"請發出指令|請在準備好時隨時輸入指令|下達指令|發布矩陣|推進路線表|對話推進"
    r"|交付完畢|圓滿交付|已全線圓滿呈交|/ ?21】|第 ?\d+ ?次對話|第[一二三四五六七八九十]+講 ?/ ?21")
NUM = re.compile(r"第[〇一二三四五六七八九十百]+章[　 ]")
PIAN = re.compile(r"第[一二三四五六七八九十]+篇[:：]")
errs, notes = [], []


def read(p):
    return p.read_bytes().decode("utf-8").split("\r\n")


def fence_mask(lines):
    inside, mask = False, []
    for l in lines:
        if FENCE.match(l):
            mask.append(inside)
            inside = not inside
        else:
            mask.append(inside)
    return mask


def check_file(name, spec):
    new = read(ROOT / name)
    old = read(BAK / (name + ".before"))
    nm = [l for l in new]
    om = fence_mask(new)
    print(f"\n■ {name}    {len(old)} 行 → {len(new)} 行（-{len(old) - len(new)}）")

    # 目 1・正文無改（子序列）
    it2 = iter(old)
    bad = []
    for l in new:
        if not l.strip():
            continue
        ok = False
        for x in it2:
            if x == l:
                ok = True
                break
        if not ok:
            bad.append(l)
    print(f"  1 正文無改：新檔非空行 {sum(1 for l in new if l.strip())}・不在原檔者 {len(bad)}")
    if bad:
        for l in bad[:5]:
            print(f"     ⚠ 改動行：{l[:70]}")
        errs.append(f"{name}：新檔有 {len(bad)} 行非原檔之字（清理器不得改字）")

    # 目 2・殘跡歸零（判式取自清理器）
    h = [l for l in new if HEADING.match(l)]
    scaf = [(i + 1, l) for i, l in enumerate(new) if C.is_scaffold(l)]
    chat = [(i + 1, l) for i, l in enumerate(new)
            if not om[i] and (any(rx.match(l.strip()) for rx in C.CHAT_LINE) or HARD.search(l))]
    print(f"  2 殘跡：標題 {len(h)} 行全掃・脚手殘留 {len(scaf)}・交談殘留 {len(chat)}")
    for i, l in scaf[:6]:
        print(f"     ⚠ L{i} {l.strip()[:60]}")
    for i, l in chat[:12]:
        print(f"     ⚠ L{i} {l.strip()[:60]}")
    if scaf:
        errs.append(f"{name}：脚手標題殘留 {len(scaf)} 枚（首見 L{scaf[0][0]}）")
    if chat:
        errs.append(f"{name}：交談語殘留 {len(chat)} 行（首見 L{chat[0][0]}）")

    # 目 3・結構對合
    book = [i + 1 for i, l in enumerate(new) if HEADING.match(l) and l.strip().lstrip("#").strip() == spec["book"]]
    pian = [(i + 1, l.strip()) for i, l in enumerate(new) if HEADING.match(l) and PIAN.search(l)]
    zhang = [(i + 1, l.strip()) for i, l in enumerate(new) if HEADING.match(l) and NUM.search(l.strip().lstrip("#").strip())]
    print(f"  3 結構：書名横幅 {len(book)}（宣稱 1）・篇 {len(pian)}（宣稱 {spec['pian']}）・章 {len(zhang)}（宣稱 {spec['zhang']}）")
    if len(book) != 1:
        errs.append(f"{name}：書名横幅 {len(book)} 條，應恰 1（見 L{book}）")
    if len(pian) != spec["pian"]:
        errs.append(f"{name}：篇横幅實測 {len(pian)} ≠ 宣稱 {spec['pian']}（{[p[0] for p in pian]}）")
    if len(zhang) != spec["zhang"]:
        errs.append(f"{name}：章標題實測 {len(zhang)} ≠ 宣稱 {spec['zhang']}（{[z[0] for z in zhang]}）")
    pn = [re.search(r"第([一二三四五六七八九十]+)篇", p[1]).group(1) for p in pian]
    if len(set(pn)) != len(pn):
        errs.append(f"{name}：篇名重複 {pn}")
    # 章必在其篇之後且篇序單調
    seq = [i for i, _ in pian] + [len(new)]
    zpos = [i for i, _ in zhang]
    assign = [max([k for k in range(len(pian)) if pian[k][0] <= z], default=-1) for z in zpos]
    if any(a < 0 for a in assign):
        errs.append(f"{name}：有章在首篇之前（章行 {zpos[assign.index(-1)]}）")
    print(f"     章→篇之歸屬：{[pn[a] if a >= 0 else '?' for a in assign]}")

    # 目 4・章不重複
    seen = {}
    for i, t in zhang:
        seen.setdefault(t, []).append(i)
    dup = {t: v for t, v in seen.items() if len(v) > 1}
    print(f"  4 章不重複：同名章 {len(dup)} 組")
    for t, v in dup.items():
        errs.append(f"{name}：章標題重複 {t[:24]}… 見 L{v}")

    # 目 5・markdown 安全
    fences = sum(1 for i, l in enumerate(new) if FENCE.match(l))
    glued = [(i + 1, new[i - 1][:40]) for i in range(1, len(new))
             if not om[i] and RULE.match(new[i]) and new[i - 1].strip() and not om[i - 1]
             and not FENCE.match(new[i - 1])]
    glued_h = [(i + 1, new[i - 1][:40]) for i in range(1, len(new))
               if not om[i] and HEADING.match(new[i]) and new[i - 1].strip() and not om[i - 1]
               and not FENCE.match(new[i - 1]) and not RULE.match(new[i - 1])]
    threeblank = sum(1 for i in range(2, len(new))
                     if not new[i].strip() and not new[i - 1].strip() and not new[i - 2].strip())
    print(f"  5 md 安全：圍欄標記 {fences}（{'成雙' if fences % 2 == 0 else '★落單'}）"
          f"・黏正文之分隔線 {len(glued)}・黏正文之標題 {len(glued_h)}・三连空行 {threeblank}")
    for i, s in glued[:5]:
        print(f"     ⚠ L{i} 上一行「{s}」將被 pandoc 讀成 setext 標題")
    if fences % 2:
        errs.append(f"{name}：圍欄落單（{fences} 個 ```）")
    if glued:
        errs.append(f"{name}：{len(glued)} 处分隔線紧贴正文（setext 之危）")
    if glued_h:
        errs.append(f"{name}：{len(glued_h)} 处標題紧贴正文")

    # 形制疑義（不計錯，供後輪）
    lv = {}
    for i, l in enumerate(new):
        if HEADING.match(l):
            lv.setdefault(re.match(r"^(#+)", l).group(1), 0)
            lv[re.match(r"^(#+)", l).group(1)] += 1
    notes.append(f"{name} 標題階梯 {dict(sorted(lv.items()))}・★ {sum(l.count('★') for l in new)} 枚"
                 f"・✅❌ {sum(l.count('✅') + l.count('❌') for l in new)} 枚（俱在圖文／表內，未動）")


def negative_selftest():
    """尺之自證：已知有病之樣本須點名真答案；已知之正文不得誤傷。"""
    cases = [
        ("脚手", "### 【第 7 次交付完畢說明】", True),
        ("指令", "請發出指令：「**推進第八講**」，我們即刻開闢第七章！", True),
        ("輪標", "👉 **【第十一章 行者夜半四照自省手冊】**", True),
        ("正文", "這是一場由**「慢心（種姓傲慢）」引發「瞋恚（極度羞恥反彈）」**的人間慘劇。", False),
        ("正文", "## 【開卷總綱：僧伽憲政五大基石宣言】", False),
        ("正文", "> 念起即覺，覺已便放。", False),
    ]
    print("\n■ 目 6・尺之自證（病樣本須命中・正文樣本須不命中）：")
    allok = True
    for lbl, s, want in cases:
        got = bool(C.is_scaffold(s) or any(rx.match(s) for rx in C.CHAT_LINE) or HARD.search(s))
        ok = (got == want)
        allok &= ok
        print(f"     {lbl}：{'病' if want else '正文'} 命中={got} 期望={want} {'✓' if ok else '⚠ 判錯'}")
    if not allok:
        errs.append("驗收尺失靈：自證樣本判定與期望不符（刀尺同源亦隨錯）")
    return allok


def main():
    for name, spec in PAIRS:
        check_file(name, spec)
    negative_selftest()
    print("\n" + "=" * 60)
    for n in notes:
        print("・", n)
    if errs:
        print(f"\n✗ 紅 {len(errs)} 條：")
        for e in errs:
            print("   ⚠", e)
        sys.exit(1)
    print("\n✓ 全綠：兩檔之脚手與重複交付已除，正文未改一字，結構與宣稱對合。")


if __name__ == "__main__":
    main()
