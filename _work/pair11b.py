# -*- coding: utf-8 -*-
"""第十一波・B 段：附錄二之『研發口吻』歸正（外路報告問題二）。

取證（本地語料實測，`原文/38-49 原文.txt`・`_tk.VINAYA`）：
  ・六檔正文之逐卷題唯見兩處——『四分律卷第一(初分之一)』與『四分律卷第二十七(二分之六明尼戒法)』；
    另二十二至三十檔之檔頭帶一筆『譯者：佛陀耶舍　竺佛念　卷第二　→』之導航標，非正文卷題。
    ➔ 舊導言宣稱『六檔之中唯見卷第一與卷第二十七兩題』，於『卷第二』一枚失之未舉（字面之稱不精）。
  ・『X揵度』之篇題則歷歷在文（全語料 54 見）；本地作『揵度』，本書作『犍度』，一語異寫。
  ・案 25 之文（452218）在『人揵度』境內：上界『具足竟人揵度』@451306、下界『具足竟覆藏揵度』@461521；
  ・案 69 之文（500699）在『法揵度』境內：上界『具足竟法揵度』@498006、下界『房舍揵度』@506004。
  ➔ 故二案之**篇聚就地可證**，可升為定稱；其**大正藏卷次**本地無題可定，外來說仍只『存其說』，不升主位。
     如此則『未細核』之口吻可除，而『不炫精確』之實不傷——改其口吻，不改其如實。

刀目：B1 導言（三段片段）・B2 案 25 出處欄・B3 案 69 出處欄。

用法：python -X utf8 _work/pair11b.py          # 試跑
      python -X utf8 _work/pair11b.py --write  # 落盤（備 .pre_a11b）
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import pairsimp as PS  # noqa: E402

W = "--write" in sys.argv
LF = chr(10)
CRLF = chr(13) + LF
MID = chr(0xB7)          # 『·』半形中點：出處欄內之卷／篇分隔（289 輪之誡：此符最易誤記為 U+30FB）
LAP = chr(0x30FB)        # 『・』全形連綴：長語之分隔
F2 = ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt"

# B1・導言三刀（皆以子句定錨，不用中點符）
B1 = [("表中自標『卷次未細核』者，因本地電子文本實無逐卷之題（六檔之中唯見卷第一與卷第二十七兩題），"
       "故唯記其分段檔所在，不作俱合之論；",
       "卷次之外，另有篇聚可證：本地六檔之正文既無逐卷之題（正文卷題唯見卷第一與卷第二十七兩處，"
       "另二十二至三十卷分段檔之檔頭有『譯者・卷第二』一筆導航標，非正文之卷題；"
       "而『X犍度』之篇題歷歷在文，本地文本作『揵度』，與本書之『犍度』乃一語異寫），"
       "故凡卷次無由而篇聚有據者，但標其分段檔與篇聚之名，不作俱合之論，亦不復以疑辭自居；"),
      ("不相容則仍標未細核，一不據以改判。",
       "不相容則擲之，一不據以改判。")]

# B2・B3・出處欄整欄重建（以案號定行，欄位以『|』拆，不重打原句）
CELLS = [("〔案例 25〕",
          "本地卷段%s三十八至四十九之檔%s人犍度（篇聚就地可證：本案之文在『人犍度』境內；外來說有二，"
          "一謂卷三十八、一謂卷四十五，俱與此檔段相容，存其說於案下，不升主位卷號）" % (MID, MID)),
         ("〔案例 69〕",
          "本地卷段%s三十八至四十九之檔%s法犍度（篇聚就地可證：本案之文在『法犍度』境內；外來說有二，"
          "前說與此檔段不相容，故擲之；今說卷四十九與此檔段相容，存其說於案下，不升主位卷號）" % (MID, MID))]


def clean(new, tag):
    if PS.flag(new):
        raise SystemExit("%s 簡形閘攔下：%s 於『%s』" % (tag, PS.hits(new), new[:40]))
    for wd in re.findall(r"[A-Za-z]{2,}", new):
        if wd not in ("text", "pre"):
            raise SystemExit("%s 夾英文『%s』" % (tag, wd))


def main():
    raw = F2.read_bytes().decode("utf-8-sig")
    nl = CRLF if CRLF in raw else LF
    L = raw.replace(CRLF, LF).split(LF)
    before = len(L)
    say = []

    for old, new in B1:
        k = [i for i, l in enumerate(L) if l.count(old) == 1]
        if len(k) != 1:
            raise SystemExit("B1 錨非唯一：%r → %d 行" % (old[:24], len(k)))
        clean(new, "B1")
        L[k[0]] = L[k[0]].replace(old, new)
        say.append("B1 導言歸正：%r➔%r" % (old[:12], new[:12]))

    for key, cell in CELLS:
        k = [i for i, l in enumerate(L) if l.startswith("|") and key in l]
        if len(k) != 1:
            raise SystemExit("B2/B3 案號行非唯一：%s → %d 行" % (key, len(k)))
        f = L[k[0]].split("|")
        if len(f) != 5:
            raise SystemExit("B2/B3 欄數異常：%s → %d 欄" % (key, len(f)))
        old_cell = f[2].strip()
        f[2] = " " + cell + " "
        line = "|".join(f)
        clean(cell, "B2")
        if len(line.split("|")) != 5 or "|" in cell:
            raise SystemExit("B2/B3 重建後欄數變：%s" % key)
        say.append("%s 出處欄重建（原 %d 字 ➔ %d 字）" % (key, len(old_cell), len(cell)))
        L[k[0]] = line

    print("\n".join("  " + s for s in say))
    for w in ("卷次未細核", "未細核", "惜本地"):
        n = sum(1 for l in L if w in l)
        print("  殘跡『%s』今 %d 見%s" % (w, n, "" if n == 0 else " ★未淨"))
    bad = [(i + 1, PS.hits(l)) for i, l in enumerate(L) if PS.flag(l)]
    if bad:
        raise SystemExit("簡形閘攔下：%s" % bad[:6])
    print("  行數 %d ➔ %d（應不變）・簡形 0 ✓" % (before, len(L)))
    if len(L) != before:
        raise SystemExit("行數變動，非本刀所許")
    if not W:
        print("  （試跑：未落盤）")
        return
    (ROOT / "_archive/備份/AI清理前" / (F2.name + ".pre_a11b")).write_bytes(raw.encode("utf-8"))
    data = nl.join(L).encode("utf-8")
    F2.write_bytes(data)
    print("  落盤：SHA %s ➔ %s" % (hashlib.sha256(raw.encode()).hexdigest()[:12],
                                    hashlib.sha256(data).hexdigest()[:12]))


if __name__ == "__main__":
    main()
