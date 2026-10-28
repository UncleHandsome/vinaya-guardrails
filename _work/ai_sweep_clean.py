# -*- coding: utf-8 -*-
"""清理兩份 AI 對話產物之交談殘跡・脚手架・重複交付。

用法：
  python -X utf8 _work/ai_sweep_clean.py          # 試跑：只印名與刀口，不落盤
  python -X utf8 _work/ai_sweep_clean.py --write  # 落盤：先備份＋記 SHA，再寫入

刀口（一律只刪整行，正文一字不改；存活行必與原檔逐字相同）：
  A 卷首交談起首（遵命／自誇段／以下正式進入）
  B 交付脚手架整塊（第N次交付完畢說明／第N次對話預告／第N講收束／下一次對話預告／
    收官報告／路線表／推進藍圖／案頭總圖／後續工作指示／全案大圓滿終局宣告／開卷總綱輪標）
  C 重複之書名横幅與篇级横幅（逐次交付之殘跡，同名牌僅留首見）
  D 整章重複交付（同名章塊逐字相同者，留首塊）
  E 段內自指尾語與殘留客套行
  F 空行與分隔線之正規化（圍欄內之 ASCII 圖文一字不動；行尾雙空格＝換行標記亦不動）
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    "起心動念：四分律的心智顯微鏡與唯識解剖.txt",
    "如法推尋：僧伽憲政、法權審理與修復正義.txt",
]

HEADING = re.compile(r"^#{1,6}\s")
RULE = re.compile(r"^\s*(?:-{3,}|\*{3,})\s*$")
FENCE = re.compile(r"^\s*```")

SCAFFOLD = [
    re.compile(r"^#{1,6}\s*【第\s*[0-9〇一二三四五六七八九十百]+\s*次(?:交付完畢說明|交付內容|對話預告[^】]*|：[^】]*)】\s*$"),
    re.compile(r"^#{1,6}\s*【第[〇一二三四五六七八九十百]+(?:講收束與後續推進|次對話收束與後續推進|講小結)[^】]*】\s*$"),
    re.compile(r"^#{1,6}\s*【下一次對話預告[^】]*】\s*$"),
    re.compile(r"^#{1,6}\s*【(?:第一|第二)本書[^】]*(?:收官報告|路線表|推進[^】]*)】\s*$"),
    re.compile(r"^#{1,6}\s*【後續工作指示】\s*$"),
    re.compile(r"^#{1,6}\s*【全案大圓滿終局宣告】\s*$"),
    re.compile(r"^#{1,6}\s*【著作者案頭[^】]*】\s*$"),
    re.compile(r"^#{1,6}\s*全書[^】]*推進藍圖.*$"),
    re.compile(r"^#{1,6}\s*開卷總綱：.*$"),
]
BANNERS = [
    re.compile(r"^《.+》$"),
    re.compile(r"^第[一二三四五六七八九十百]+篇[:：]"),
]
CHAPTER = re.compile(r"^第[〇一二三四五六七八九十百]+章[　 ]")
CHAT_LINE = [
    re.compile(r"^以下正式進入：?\s*$"),
    re.compile(r"^👉"),
    re.compile(r"^至此，(?:第|整部|全書).{0,40}(?:圓滿交付|交付完畢|全線圓滿呈交)"),
]
PREAMBLE = re.compile(r"^(遵命|好的！|沒問題|這是一場)")


def htxt(line):
    return line.strip().lstrip("#").strip()


def is_scaffold(line):
    s = line.strip()
    return bool(HEADING.match(s) and any(rx.match(s) for rx in SCAFFOLD))


def fence_mask(lines):
    """True＝該行在 ``` 圍欄內（圖文，不動）。"""
    inside, mask = False, []
    for l in lines:
        if FENCE.match(l):
            mask.append(inside)
            inside = not inside
        else:
            mask.append(inside)
    return mask


def plan(name, lines):
    n = len(lines)
    marks = [None] * n
    inm = fence_mask(lines)

    # A 卷首交談起首（首行非標題且屬客套語者，刪至首個脚手塊或首條分隔線）
    first = next((i for i, l in enumerate(lines) if l.strip()), 0)
    if not HEADING.match(lines[first]) and PREAMBLE.match(lines[first].strip()):
        j = first
        while j < n and not (is_scaffold(lines[j]) or (not inm[j] and RULE.match(lines[j]))):
            if not marks[j]:
                marks[j] = "A-卷首客套"
            j += 1
        if j < n and not inm[j] and RULE.match(lines[j]):
            marks[j] = "A-卷首分隔"

    # B 交付脚手架整塊
    blocks = 0
    for i, l in enumerate(lines):
        if marks[i] or not is_scaffold(l):
            continue
        blocks += 1
        j = i
        while j < n:
            if j > i and HEADING.match(lines[j]) and not is_scaffold(lines[j]):
                break
            if not marks[j]:
                marks[j] = "B-交付脚手架"
            j += 1

    # C 重複之書名/篇级横幅（僅留首見）
    seen, dup_banner = set(), 0
    for i, l in enumerate(lines):
        if marks[i] or not HEADING.match(l):
            continue
        t = htxt(l)
        if not any(rx.match(t) for rx in BANNERS):
            continue
        if t in seen:
            marks[i] = "C-重複横幅"
            dup_banner += 1
        else:
            seen.add(t)

    # E 段內自指尾語／殘留客套行
    stray = 0
    for i, l in enumerate(lines):
        if marks[i] or inm[i]:
            continue
        s = l.strip()
        if any(rx.match(s) for rx in CHAT_LINE):
            marks[i] = "E-段內自指尾語"
            stray += 1

    # D 整章重複交付
    idx = [i for i, l in enumerate(lines)
           if not marks[i] and HEADING.match(l) and CHAPTER.match(htxt(l))]
    spans = [(idx[k], idx[k + 1] if k + 1 < len(idx) else n) for k in range(len(idx))]

    def core(body):
        b = list(body)
        while b and (not b[-1].strip() or RULE.match(b[-1])
                     or HEADING.match(b[-1]) and any(rx.match(htxt(b[-1])) for rx in BANNERS)):
            b.pop()
        return b

    def is_banner(line):
        return bool(HEADING.match(line) and any(rx.match(htxt(line)) for rx in BANNERS))

    first_seen, dup_chapters = {}, []
    for a, b in spans:
        title = htxt(lines[a])
        body = [lines[k].rstrip("\r") for k in range(a, b) if not marks[k]]
        if title in first_seen:
            if first_seen[title] == core(body):
                dup_chapters.append(title)
                ks = [k for k in range(a, b) if not marks[k]
                      and lines[k].strip() and not RULE.match(lines[k]) and not is_banner(lines[k])]
                end = ks[-1] if ks else b - 1
                for k in range(a, end + 1):
                    if not marks[k]:
                        marks[k] = "D-整章重複交付"
            else:
                diff = next((p for p, (x, y) in
                             enumerate(zip(first_seen[title], core(body))) if x != y), None)
                dup_chapters.append(f"{title}【兩塊有異（第 {diff} 行起）・未刪】")
        else:
            first_seen[title] = core(body)

    kept = normalize([lines[i].rstrip("\r") for i in range(n) if not marks[i]])
    tally = {}
    for m in marks:
        if m:
            tally[m] = tally.get(m, 0) + 1
    return dict(name=name, lines=lines, n=n, marks=marks, kept=kept, tally=tally,
                blocks=blocks, dup_banner=dup_banner, dup_chapters=dup_chapters, stray=stray)


def normalize(lines):
    """圍欄外：多餘空行併一、相鄰分隔線併一、標題與分隔線前必留一空行、檔尾去空行。"""
    out, blank, prev_rule = [], 0, False
    inside = False
    for l in lines:
        s = l.strip()
        if FENCE.match(l):
            if blank and out:
                out.append("")
            blank, prev_rule = 0, False
            inside = not inside
            out.append(l)
            continue
        if inside:
            out.append(l)
            continue
        if not s:
            blank += 1
            continue
        if RULE.match(s):
            if not out or prev_rule:
                continue
            out.append("")          # 分隔線前必留空行，否則 pandoc 讀成 setext 標題
            out.append(s)
            blank, prev_rule = 0, True
            continue
        if HEADING.match(s) and out and blank == 0:
            out.append("")
        if blank > 1 and out:
            out.append("")
        elif blank == 1 and out:
            out.append("")
        elif blank and not out:
            pass
        out.append(l)
        blank, prev_rule = 0, False
    while out and not out[-1].strip():
        out.pop()
    if out and RULE.match(out[-1].strip()):
        out.pop()
    return out


def report(r, cutlist):
    print("=" * 74)
    print(f"{r['name']}  {r['n']} 行 → {len(r['kept'])} 行（淨刪 {r['n'] - len(r['kept'])}）")
    for k in sorted(r["tally"]):
        print(f"   {k}: {r['tally'][k]} 行")
    print(f"   脚手塊 {r['blocks']} 塊・重複横幅 {r['dup_banner']} 條・自指尾語 {r['stray']} 行")
    for t in r["dup_chapters"]:
        print(f"   整章重複交付：{t}")
    for i, m in enumerate(r["marks"], 1):
        if m:
            cutlist.append(f"{r['name']}\tL{i}\t{m}\t{r['lines'][i - 1].strip()[:120]}")
    print("   標刀首行樣本：")
    shown = 0
    for i, m in enumerate(r["marks"], 1):
        if m and shown < 8:
            print(f"      L{i:>5} [{m}] {r['lines'][i - 1].strip()[:56]}")
            shown += 1


def main():
    write = "--write" in sys.argv
    plans, cuts = [], []
    for name in FILES:
        raw = (ROOT / name).read_bytes()
        lines = raw.decode("utf-8").split("\n")
        r = plan(name, lines)
        plans.append((name, raw, r))
        report(r, cuts)
    (ROOT / "_work" / "ai_sweep_cuts.txt").write_text("\n".join(cuts) + "\n", encoding="utf-8")
    print(f"\n刀口清冊共 {len(cuts)} 行 → _work/ai_sweep_cuts.txt")
    if not write:
        print("\n（試跑：未落盤。加 --write 方寫入。）")
        return
    bakdir = ROOT / "_archive" / "備份" / "AI清理前"
    bakdir.mkdir(parents=True, exist_ok=True)
    for name, raw, r in plans:
        src = ROOT / name
        bak = bakdir / (name + ".before")
        bak.write_bytes(raw)
        out = ("\r\n".join(r["kept"]) + "\r\n").encode("utf-8")
        src.write_bytes(out)
        print(f"落盤 {name}  SHA前 {hashlib.sha256(raw).hexdigest()[:12]} → 後 "
              f"{hashlib.sha256(out).hexdigest()[:12]}  {len(out)} B  備份 {bak.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
