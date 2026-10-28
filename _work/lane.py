# -*- coding: utf-8 -*-
"""律文欄之保護區（共器：全書簡形尺 `simp_sweep`・草稿雜質閘 `gate_draft` 同源）。

形制：本書之戒文欄作「> **【第七僧殘·條文】：** 律文」或「**【律制】：** 律文」之形，
      其文不入「」，故與『「…」』同為逐字之體。語料自有之字形（并・谷・宁…）若落在此欄，
      簡形尺不得論為簡形——第 69 輪『食并餘物』即此案。
口徑：以「……」分段，每段去標點・歸簡後（>=4 字）俱見《四分律》語料者，全欄得保；
      有一段無據即不保，其簡形照報——保護出於實證，不出於名目。
自證：`spans()` 竝回（保護區間、管轄欄數），尺須印管轄之數，免墮『殭尺之綠』。
用法：from lane import spans;  sp, n = spans(t)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk  # noqa: E402

PUNC = re.compile(u"[，、；：！？「」『』（）()《》〈〉·．。\\-—…﹑＂\"'*＿　\\s]")
LANE = re.compile(u"\\*\\*【[^】]*(?:條文|律制|律文)[^】]*】：\\*\\*\\s*(.+)")
# 逐行之表（與 LANE 同認一形）：供 `ordchk` 以欄內之文對勘該序之律文。
ROW = re.compile(u"^\\s*>?\\s*\\*\\*【([^】]*(?:條文|律制|律文)[^】]*)】：\\*\\*\\s*(.+?)\\s*$")


def rows(lines):
    """回 {行號: (標籤, 欄內文)}。標籤如『第五波羅夷·條文』・『第26條 條文』・『律制』。"""
    out = {}
    for i, l in enumerate(lines):
        m = ROW.match(l)
        if m:
            out[i] = (m.group(1), m.group(2))
    return out


def verbatim(body):
    frags = [_tk.norm(PUNC.sub(u"", x)) for x in re.split(u"……|…", body)]
    frags = [f for f in frags if len(f) >= 4]
    return bool(frags) and all(f in _tk.VINAYA for f in frags)


def spans(t):
    """回（保護區間清單、管轄之欄數）。管轄內未經語料對勘者不入保護，故『護』必與『核』同數。"""
    out, n = [], 0
    for m in LANE.finditer(t):
        n += 1
        if verbatim(m.group(1)):
            out.append((m.start(1), m.end(1)))
    return out, n


# ── 款①式樣（粗體＋引號）之判別（第 74 輪立共器）─────────────────────────
#   病：`**「…」**`／`「**…**」` 在本書即『逐字出自漢譯《四分律》』之聲明；而本書評語偶借此式樣，
#       讀來像律文。`hlchk` 辛軸原判與『降式樣之刀』若各抄一份口徑，一處改則另一處即假綠（第 66 輪之教）。
#   治：判別只此一處——`pin_kind`，尺與刀同取。
PIN = re.compile(u"「\\*\\*(.+?)\\*\\*」|\\*\\*「([^」]+)」\\*\\*")
LIT = re.compile(u"若比丘|世尊|爾時|諸比丘|結戒|波逸提|婆尸沙|不共住|波羅夷|僧伽梨|"
                 u"式叉迦羅尼|突吉羅|羯磨|佛言|佛告")
_CJK_OUT = u"[^" + chr(0x4E00) + u"-" + chr(0x9FFF) + u"]"   # 以 chr() 築字類，免傳遞層歸簡破範疇
GLOSS = re.compile(u"（[^）]*）")


def flat(s):
    """norm（折異體・去括線）後只留中日韓字——供『是否連寫於語料』之判。"""
    return re.sub(_CJK_OUT, u"", _tk.norm(s))


def pin_kind(q, corpus_flat):
    """款①式樣之引語 ➔ (律句之未中片段, 評語之未中片段)。
       去括注、以『……』分段；已中語料或過短（<8 字）者兩不計（即屬真逐字，無須動刀）。"""
    lit, ping = [], []
    for frag in re.split(u"…+|\\.{3}", GLOSS.sub(u"", q)):
        t = flat(frag)
        if len(t) < 8 or t in corpus_flat:
            continue
        (lit if LIT.search(frag) else ping).append(frag)
    return lit, ping


def corpus_flat():
    return flat(_tk.VINAYA)
