# -*- coding: utf-8 -*-
"""回流前之逐字閘：迎回區內凡『「…」』式樣（本書之逐字承諾形）須先於本地語料見形。
   分段口徑：以『……』『…』斷段，段長 ≥6 字者逐段求；全段無形者列紅，候裁（降式樣或除引號）。
用法：python -X utf8 _work/pairreflow_verbatim.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import _tk  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "ver39四分律_起心動念心智分析框架_修正版.md"

def _plain(s):
    """語料全形無標點，比對兩側俱只留漢字並依 _tk.FOLD 折異文（此即本專案『逐字閘』之口岸）。"""
    return "".join(_tk.FOLD.get(c, c) for c in re.sub(r"[^\u4e00-\u9fff]", "", s))

CORPUS = _plain(_tk.VINAYA)
for v in _tk.OTHER.values():
    CORPUS += _plain(v)
print("語料口岸：漢字 %d（VINAYA＋他部 %d 件）" % (len(CORPUS), len(_tk.OTHER)))


def norm(s):
    return _plain(s)

BLOCKS = [("F1 凡例", 241, 312), ("F1 附一 宗門心法", 7352, 7452), ("F1 附二 心相病相", 7453, 7512),
          ("F1 附三 境想", 7513, 7529), ("F1 附四 六重閘門", 1531, 2074),
          ("F2 附一 四維矩陣", 6281, 6420), ("F2 附二 回查索引", 7625, 7804),
          ("F2 附三 名相梵巴", 7530, 7624), ("F2 附四 經論互證", 7805, 7839)]
MIN = 6


def main():
    lines = SRC.read_bytes().decode("utf-8").replace("\r\n", "\n").split("\n")
    tot = bad = 0
    for tag, a, b in BLOCKS:
        seg = lines[a - 1:b]
        reds = []
        n = 0
        for k, l in enumerate(seg):
            if l.strip().startswith("```"):
                continue
            for q in re.findall(r"「([^」]{4,})」", l):
                n += 1
                for part in re.split(r"…+|⋯+", q):
                    p = norm(part)
                    if len(p) < MIN:
                        continue
                    if p not in CORPUS:
                        reds.append((a + k, part[:40]))
                        break
        tot += n
        bad += len(reds)
        print(f"■ {tag:<18} 引號 {n:<4} 語料無形 {len(reds)}")
        for ln, t in reds[:10]:
            print(f"     L{ln:<6}✗ {t}")
        if len(reds) > 10:
            print(f"     …其餘 {len(reds) - 10} 條")
    print("=" * 60)
    print(f"合計：引號 {tot}・未見形 {bad}")


main()
