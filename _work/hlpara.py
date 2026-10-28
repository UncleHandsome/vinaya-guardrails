# -*- coding: utf-8 -*-
"""印面段落之模型（單一法源）：源檔行 → pandoc 實際成段之區間。
規則：①空行分段 ②凡行首為清單符（『*』『-』『1.』）另起一段 ③行尾兩空格僅 <br>，不另起段
     ④標題（#）／表格（|）／引框（>）／圍欄（```）不計入散文段落 ⑤附錄另計（公具，非敘事）。
用者：`_work/hlannot.py` 之 ④ 段長上限、`_work/hlblank57.py` 之補空行。
教（第 57 輪）：上一版 ④ 尺按『源檔單行』計，實則欄內多行無空行即被併為一段——
              單行最長 559 而印面實則 841，**尺之單位錯，則綠亦非綠**。
"""
import re

LI = re.compile(u"^\\s*(?:[*+-]|\\d+[.)])\\s+")
FENCE = u"```"
CJK = re.compile(u"[^一-龥]")
# 中間層之形（一名即一制）：57 輪『樞紐』・65『陣地』・66『板塊』與『重鎮』——
# 新稱只加於此一支，使 `hlchk` 丙軸與 `tocsync` 同法源。
# （教：67 輪各抄一次無事，68 輪各自演化便露縫——同一形制之兩處抄本即是債。）
LAYER = u"【第[一二三四五六七八九十]+(?:樞紐|陣地|板塊|重鎮)："


def skip(l):
    return l.startswith((u"#", u"|", u">")) or l.startswith(FENCE)


def cn(s):
    return len(CJK.sub(u"", s))


def apx_of(lines, head=u"# 附錄"):
    return next((n for n, l in enumerate(lines) if l.startswith(head)), len(lines))


def blocks(lines, upto=None):
    """回 [(起, 迄)] 半開區間，每個區間＝一個印面段落。"""
    apx = upto if upto is not None else len(lines)
    out, i, inf = [], 0, False
    while i < apx:
        if lines[i].startswith(FENCE):
            inf = not inf
            i += 1
            continue
        if inf or not lines[i].strip() or skip(lines[i]):
            i += 1
            continue
        j = i + 1
        while j < apx and not inf and lines[j].strip() and not skip(lines[j]):
            if LI.match(lines[j]) or lines[j].startswith(FENCE):
                break
            j += 1
        out.append((i, j))
        i = j
    return out


def census(lines, upto=None):
    """回 [(漢字數, 起行 1 起)]，由長而短。"""
    return sorted(((cn(u"".join(x.strip() for x in lines[a:b])), a + 1)
                   for a, b in blocks(lines, upto)), reverse=True)
