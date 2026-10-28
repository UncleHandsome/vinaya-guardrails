# -*- coding: utf-8 -*-
"""第八波・收官之整驗（只量不改）：立三軸，俱他尺不守之職。

  甲 相鄰重出之行——字面刀・插形之刀重跑或併行之敗必現此形（pairfix9 親踩：護一去失即三條變五條）。
  乙 截斷之徵——去殼後句意不接者，其形為『行末讀點（；／，）而下已是新標題／閉柵／卷盡』。
     口徑須緊（初版親踩反向之病：條件寫反，40 處俱為列點續行之正常形）：
     以『：』收尾者乃領起之式，全冊 196 處，非病；列點・表行・引文・圍欄之續以讀點收尾者，
     其下另有同塊之接文，亦非病。唯『一句未竟而下即另起一塊』方是脫文之形（第四章原則三即此）。

餘軸不重複立：簡形歸 `pairtrim_check`・案號失指歸 `pairrefchk`（跨冊第七律由其認）・
骨架與書籤歸 `pairface`（量的是產物，非源檔）。用法：python -X utf8 _work/pairclose.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import pairsimp as PS  # noqa: E402

BOOKS = [ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt",
         ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt"]
RX_STOP = re.compile(r"[\u4e00-\u9fff\)\]」』][；，][\s　]*$")
MARK = ("#", "```", "|", ">", "*", "-", "─", "═")     # 接文之形：列點・表行・引文・標題
HEAD = ("#", "```")                                    # 截斷之徵：下接標題或圍欄閉柵而句猶未竟


def fence_mask(lines):
    m, f = [], False
    for l in lines:
        if re.match(r"^\s*```", l):
            f = not f
            m.append(True)
            continue
        m.append(f)
    return m


tot = 0
for src in BOOKS:
    lines = src.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
    mask = fence_mask(lines)
    print("=" * 72)
    print("■", src.name[:12], "・行 %d（圍欄內 %d 行不入管轄）" % (len(lines), sum(mask)))

    dup = [(i + 1, lines[i][:44]) for i in range(1, len(lines))
           if lines[i].strip() and lines[i] == lines[i - 1] and not mask[i]
           and not re.match(r"^\s*[-—─═|｜*═]+\s*$", lines[i])]
    print("  甲 相鄰重出之行：%d" % len(dup))
    for k, s in dup:
        print("     · L%d「%s」" % (k, s))

    dang = []
    for i, l in enumerate(lines):
        if mask[i] or RX_STOP.search(l.rstrip()) is None:
            continue
        if l.lstrip().startswith(MARK):                 # 列點・表行之領起行本以讀點收尾，非病
            continue
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        nxt = lines[j].strip() if j < len(lines) else ""
        if nxt.startswith(HEAD) or j >= len(lines):      # 一句未竟而下已是新塊／卷盡＝截斷之徵
            dang.append((i + 1, l.strip()[-52:], nxt[:30]))
    print("  乙 截斷之徵（句末讀點而下接標題／閉柵／卷盡・管轄＝圍欄外之散文行）：%d" % len(dang))
    for k, s, x in dang[:14]:
        print("     · L%d「…%s」→ 下「%s」" % (k, s, x))

    # 丙 案列之跨行：同一列點之續行被折成兩行（其間句讀必錯置——前行之『。』落在系列之中）
    #    此軸不問句讀、只問形，故乙軸漏得之形（前事以『。』收者）由是現形（F2 附錄一親逮四處）。
    split = []
    for i in range(1, len(lines)):
        if mask[i] or mask[i - 1]:
            continue
        a, b = lines[i - 1], lines[i]
        if re.match(r"^\s{2,}〔案例", a) and re.match(r"^\s{2,}〔案例", b):
            split.append((i + 1, a.strip()[-24:], b.strip()[:26]))
    print("  丙 案列之跨行（同塊兩續行，句讀錯置之形）：%d" % len(split))
    for k, s, x in split[:12]:
        print("     · L%d 前行「…%s」→ 續「%s…」" % (k, s, x))
    tot += len(dup) + len(dang) + len(split)

print("\n三軸合點名 %d 處——只點名，不落一刀；逐條目驗後方定是否為病。" % tot)
