# -*- coding: utf-8 -*-
"""第八波・案列跨行之歸一（器 `_work/pairfix10.py`）。

病形（`pairclose` 丙軸現形，F2 附錄一『心所病相軸』四處・承自 ver39 同形）：一列點之案群
被折作兩行續文，其間句讀錯置——前行之『。』落在系列之中，末行又以『；』收而直接新標目。
印面因 lazy continuation 本併為一條，故紙上所見即『……吹哨人。〔案例 98〕……衣鉢；』之誤讀。

治：併為一行（不削一案、不添一字，唯移行首之縮排與系列中之句讀）。
    前行之句末『。／；』改『、』；末行若以『；』收，則依其下是否另有同組列點定『；』或『。』。

用法：python -X utf8 _work/pairfix10.py          # 試跑印名，不落盤
      python -X utf8 _work/pairfix10.py --write  # 落盤（備份 .pre_fix10・清冊 pairfix10_cuts.txt）
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import pairsimp as PS  # noqa: E402

W = "--write" in sys.argv
BOOKS = [ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt",
         ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt"]
CONT = re.compile(r"^\s{2,}〔案例")
CIT = re.compile(r"〔案例\s*[0-9]{1,3}〕")


def fence_mask(lines):
    m, f = [], False
    for l in lines:
        if re.match(r"^\s*```", l):
            f = not f
            m.append(True)
            continue
        m.append(f)
    return m


def next_nonblank(lines, j):
    while j < len(lines) and not lines[j].strip():
        j += 1
    return lines[j].strip() if j < len(lines) else ""


def fix(lines):
    """相鄰之同縮排案列續行，幾何併為一行（三行相連者亦只一併）。"""
    mask = fence_mask(lines)
    out, cuts = [], []
    i = 0
    while i < len(lines):
        j = i + 1
        grp = [lines[i]]
        if not mask[i] and CONT.match(lines[i]):
            while j < len(lines) and not mask[j] and CONT.match(lines[j]):
                grp.append(lines[j])
                j += 1
        if len(grp) > 1:
            tail = next_nonblank(lines, j)
            term = "；" if tail.startswith("*") else "。"
            merged = grp[0].rstrip()
            for k, p in enumerate(grp[1:]):
                if merged[-1] in "。；，":
                    merged = merged[:-1] + "、"
                b = p.strip()
                if k == len(grp) - 2 and b[-1] == "；":
                    b = b[:-1] + term
                merged += b
            cuts.append((len(out) + 1, len(grp), grp[0].strip()[-18:],
                         grp[-1].strip()[-18:], merged[-22:]))
            out.append(merged)
            i = j
            continue
        out.append(lines[i])
        i = j
    return out, cuts


for src in BOOKS:
    raw = src.read_bytes().decode("utf-8-sig")
    nl = "\r\n" if "\r\n" in raw else "\n"
    lines = raw.replace("\r\n", "\n").split("\n")
    before = len(CIT.findall("\n".join(lines)))
    new, cuts = fix(lines)
    after = len(CIT.findall("\n".join(new)))
    print("=" * 70)
    print("■", src.name[:12], "・行 %d ➔ %d・案號之引 %d ➔ %d・換行 %s"
          % (len(lines), len(new), before, after, "CRLF" if nl == "\r\n" else "LF"))
    if not cuts:
        print("  已竟（丙軸之形 0 處）")
        continue
    for k, ng, x, y, z in cuts:
        print("  · L%-5d %d 行併一：前『…%s』末『…%s』➔ 尾『…%s』" % (k, ng, x, y, z))
    assert before == after, "案號之引有增損，硬退"
    bad = [(n, PS.hits(l)) for n, l in enumerate(new, 1) if PS.flag(l)]
    if bad:
        raise SystemExit("簡形閘攔下：%s" % bad[:6])
    if not W:
        print("  （試跑：未落盤）")
        continue
    bak = ROOT / "_archive/備份/AI清理前" / (src.name + ".pre_fix10")
    bak.parent.mkdir(parents=True, exist_ok=True)
    bak.write_bytes(raw.encode("utf-8"))
    log = ROOT / "_work/pairfix10_cuts.txt"
    body = nl.join(new).encode("utf-8")            # 換行只在這一處定（全檔依其原慣例）
    with log.open("a", encoding="utf-8") as fh:
        fh.write("%s\t%s\t%d 處\t%s\n" % (src.name, "併案列跨行", len(cuts),
                                          ";".join("L%d" % c[0] for c in cuts)))
    src.write_bytes(body)
    print("  落盤：%s・%d B・SHA %s ➔ %s（備份 %s）"
          % (src.name[:8], len(body), hashlib.sha256(raw.encode()).hexdigest()[:12],
             hashlib.sha256(body).hexdigest()[:12], bak.name))
