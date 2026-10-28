# -*- coding: utf-8 -*-
"""第七波・圍欄內之 markdown 殘標記歸零（等寬替換，不動框線）。

病：源檔之流程圖・框線圖（```text 圍欄內）混入粗體標記 `**…**`——pandoc 於 <pre> 內不解析標記，
    故印面直出字面星號（心法卷 6 行）；前一步誤以 <strong> 代之，於圍欄內同樣不解析，仍是洩漏。
治：圍欄內之 `**`、`<strong>`、`</strong>` 一律換成等寬之空格（2 格），
    使框線圖之欄位分毫不動而殘標記淨盡。圍欄外之粗體（1,397＋867 行）俱由 pandoc 正常渲染，不碰。
用法：python -X utf8 _work/pairfencestar.py [--write]
"""
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import pairsimp as PS  # noqa: E402

FILES = ["起心動念：四分律的心智顯微鏡與唯識解剖.txt",
         "如法推尋：僧伽憲政、法權審理與修復正義.txt"]
BAK = ROOT / "_archive/備份/AI清理前"
W = "--write" in sys.argv
FENCE = "```"
PADS = {"**": "  ", "<strong>": "  ", "</strong>": "  "}


def main():
    for fn in FILES:
        p = ROOT / fn
        raw = p.read_bytes()
        L = raw.decode("utf-8").split("\r\n")
        inside, n = False, 0
        for i, l in enumerate(L):
            if l.strip().startswith(FENCE):
                inside = not inside
                continue
            if not inside:
                continue
            s = l
            for k, v in PADS.items():
                s = s.replace(k, v)
            if len(s) != len(l):
                raise SystemExit(f"等寬之護破產：{fn} L{i + 1}（{len(l)}→{len(s)}）")
            if s != l:
                L[i] = s
                n += 1
                print(f"  ・{fn[:6]} L{i + 1}・淨殘標記（等寬）：{l.strip()[:56]}")
                print(f"      新 {s.strip()[:56]}")
        bad = sorted({c for l in L for c in PS.hits(l)})
        print(f"■ {fn[:6]}・治 {n} 行・簡形 {bad}")
        if bad:
            raise SystemExit("帶簡形，不落盤")
        if n and W:
            (BAK / (fn + ".pre_fstar")).write_bytes(raw)
            data = "\r\n".join(L).encode("utf-8")
            p.write_bytes(data)
            print(f"  ● SHA {hashlib.sha256(raw).hexdigest()[:12]} → {hashlib.sha256(data).hexdigest()[:12]}")


main()
