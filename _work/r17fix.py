# -*- coding: utf-8 -*-
"""第 50 輪修補：sigchk 分段口徑・喻名三處歸一・『第N重』歧義之辨・散文半形斜線歸全形。"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import os
import re
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "_work")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import _tk  # noqa: E402
from _simpdict import MAP as SIMP  # noqa: E402

BOOK = HP.SRC
NL = chr(13) + chr(10)
GO = u"--go" in sys.argv
raw = io.open(BOOK, encoding="utf-8", newline="").read()
L = raw.split(NL)
n0 = len(L)
NEWTXT = []
SLASH = chr(0x2F)
FS = chr(0xFF0F)


def sub(idx, old, new, tag):
    t = L[idx - 1]
    assert t.count(old) == 1, (u"命中數：" + tag, idx, t.count(old))
    L[idx - 1] = t.replace(old, new)
    NEWTXT.append(new)
    print(u"改 %s @L%d" % (tag, idx))


# ── 一・喻名歸一（「外城門」非五重之名，三處摘要今統一為「外城牆與內城門」） ──
sub(933, u"外城門（單提捨墮）", u"外城牆與內城門（單提、捨墮）", u"二章末・喻名")
sub(1222, u"外城牆（單提捨墮）", u"外城牆與內城門（單提、捨墮）", u"四章總結・喻名")
sub(1249, u"外城門（單提、捨墮）", u"外城牆與內城門（單提、捨墮）", u"五章卷端・喻名")

# ── 二・『第N重』兩義之辨（接在第三則按語之後） ──
i = next(n for n, t in enumerate(L) if u"同心圓外還有兩類法" in t)
assert L[i].endswith(u"說詳第十二章第三、五節。"), L[i][-40:]
ADD = (u"**另辨一名：本書兩處用『重』字不同義。** 城牆之『第N重』指五重陣地（第三重是三十捨墮、第四重是九十單提）；"
       u"各案例【防禦靶點】中所稱『第N重戒』或『第N重根本』，指四波羅夷之次（第三重戒是殺戒、第四重戒是大妄語）。"
       u"兩者數字相同而所指異，讀者據上下文自辨：言城牆者論職司，言波羅夷者論死罪。")
L[i + 1:i + 1] = [u"", ADD]
NEWTXT.append(ADD)
print(u"插入 重字兩義之辨 @L%d 後 +2 行" % (i + 1))

# ── 三・散文之半形斜線歸全形 ──
# 三不管區須讓路：①圍欄內（框線以 1 格計，半形為排版所需）；②附錄以下（附錄唯產生器是法源，
# 手改一行即造第二份真相）；③含 CBETA 組字碼之行（如『[真/心]』＝上真下心，斜線是構形的一部分，動之即毀可回溯性）。
APX = next(n for n, t in enumerate(L) if t.startswith(u"# 附錄"))
BRK = chr(0x5B)
inf = False
fixed = 0
for n, t in enumerate(L):
    if t.strip() == u"```":
        inf = not inf
        continue
    if inf or n >= APX or SLASH not in t or BRK in t:
        continue
    L[n] = t.replace(SLASH, FS)
    fixed += t.count(SLASH)
    NEWTXT.append(L[n])
    print(u"斜線歸全形 @L%d（%d 處）" % (n + 1, t.count(SLASH)))
skip = [i + 1 for i, x in enumerate(L) if i < APX and SLASH in x and (x.strip() == u"```" or BRK in x)]
print(u"散文斜線共改 %d 處｜圍欄內與組字碼行照例不動（附錄起於 L%d）" % (fixed, APX + 1))

# ── 自護 ──
bad = sorted({c for t in NEWTXT for c in t if c in SIMP})
assert not bad, [(c, SIMP[c], hex(ord(c))) for c in bad]
for i2, t in enumerate(L):
    assert t.count(u"**") % 2 == 0, (u"粗體不成對 @L%d" % (i2 + 1), t[:70])
    assert chr(0x30FB) not in t, (u"日式中黑 @L%d" % (i2 + 1))
out = NL.join(L)
assert out.count(chr(13)) == len(L) - 1
print(u"行數 %d → %d" % (n0, len(L)))
if GO:
    io.open(BOOK, "w", encoding="utf-8", newline="").write(out)
    print(u"已寫入")
else:
    print(u"（試跑，未寫入）")
