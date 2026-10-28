# -*- coding: utf-8 -*-
"""第九波・凡例第八律『子案之號』之安裝（兩冊同立，文出共器 paircase_lib.NOTE_SUB）。

承第五波之成例：標題之數（七律→八律）**與文中自指之稱須同時歸位**，否則自指老化。
器可重入：已立者跳過（`CL.sub_declared`）。

用法：python -X utf8 _work/pairsublaw.py          # 試跑
      python -X utf8 _work/pairsublaw.py --write  # 落盤（備 .pre_sublaw）
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import paircase_lib as CL  # noqa: E402
import pairsimp as PS  # noqa: E402

W = "--write" in sys.argv
BOOKS = [ROOT / CL.F1, ROOT / CL.F2]
HEAD = re.compile(r"^(###\s*一、文獻底冊與引文承諾)(七律)(\s*)$")
SELF = re.compile(r"【文獻底冊與引文承諾七律】")
SEVEN = re.compile(r"^7\.\s+\*\*跨冊案號之索\*\*")

DECL8 = re.compile(r"^8\.\s+\*\*子案[與之]")     # 舊稱『子案之號』・新稱『子案與新增案之號』俱認

for src in BOOKS:
    raw = src.read_bytes().decode("utf-8-sig")
    nl = "\r\n" if "\r\n" in raw else "\n"
    lines = raw.replace("\r\n", "\n").split("\n")
    print("=" * 70)
    print("■", src.name[:12])
    item = CL.NOTE_SUB[src.name]
    if CL.sub_declared(lines):
        cur = [i for i, l in enumerate(lines) if DECL8.match(l.strip())]
        if len(cur) != 1:
            raise SystemExit("第八律已宣稱而條文不可求（%d 處）——硬退" % len(cur))
        if lines[cur[0]] == item:
            print("  已竟（第八律已在檔且與共器合——重入之護）")
            continue
        if PS.flag(item):
            raise SystemExit("簡形閘攔下：『%s』" % PS.hits(item))
        out = list(lines)
        out[cur[0]] = item                      # 歸文：以共器之文覆舊條（一字之位，行數不動）
        print("  歸文第八律於 L%d（共器之文已改，此行隨之）" % (cur[0] + 1))
    else:
        k7 = [i for i, l in enumerate(lines) if SEVEN.match(l.strip())]
        hh = [i for i, l in enumerate(lines) if HEAD.match(l.strip())]
        sl = [i for i, l in enumerate(lines) if SELF.search(l)]
        print("  錨：第七律 %d・凡例標題 %d・自指之稱 %d" % (len(k7), len(hh), len(sl)))
        if len(k7) != 1 or len(hh) != 1 or len(sl) < 1:
            raise SystemExit("錨點不合（第七律/標題須各一，自指至少一）——硬退")

        if PS.flag(item):
            raise SystemExit("簡形閘攔下：『%s』" % PS.hits(item))
        out = list(lines)
        i = k7[0] + 1                                  # 接於第七律之下（插入，絕非取代）
        out.insert(i, item)
        if out[i + 1].strip():
            out.insert(i + 1, "")                      # 段落界須有空行（管線啟 blank_before_header）
        h = hh[0] + (1 if hh[0] >= i else 0)
        out[h] = HEAD.sub(r"\g<1>八律\g<3>", out[h])
        for x in sl:
            j = x + (1 if x >= i else 0)
            out[j] = SELF.sub("【文獻底冊與引文承諾八律】", out[j])
        print("  立第八律於 L%d・標題『八律』L%d・自指歸位 %d 處" % (i + 1, h + 1, len(sl)))
    n8 = sum(1 for l in out if l.startswith("8. **子案與新增案之號**"))
    n7 = sum(1 for l in out if l.startswith("7. **跨冊案號之索**"))
    if (n8, n7) != (1, 1):
        raise SystemExit("自證失敗：第八律 %d 條・第七律仍在 %d 條" % (n8, n7))
    print("  行數 %d ➔ %d" % (len(lines), len(out)))
    if not W:
        print("  （試跑：未落盤）")
        continue
    bak = ROOT / "_archive/備份/AI清理前" / (src.name + ".pre_sublaw")
    bak.write_bytes(raw.encode("utf-8"))
    body = nl.join(out).encode("utf-8")
    src.write_bytes(body)
    print("  落盤：%s・SHA %s ➔ %s" % (src.name[:8], hashlib.sha256(raw.encode()).hexdigest()[:12],
                                       hashlib.sha256(body).hexdigest()[:12]))
