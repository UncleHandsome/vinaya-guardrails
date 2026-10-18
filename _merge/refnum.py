# -*- coding: utf-8 -*-
"""章節指針之尺（漢語序數・章界切塊・節級死鏈判定）——`merge_build` 與 `merge_check` 共用。

兩套各寫一套必漂移：第三十七輪校驗器以「裸序數」查節（`^#{2,6} 三`），遂把 H5 列項
「##### 三、大綱本懷」當成「第三節」，236 漢字之〔指針待判〕因此靜靜少掛——死鏈不掛標即無形。
今定：指針「第N章第M節」唯以該章實有以「第M節」起首之 H2～H6 標題為生，餘皆掛標候裁。
"""
import re

CN = {c: i for i, c in enumerate(u"零一二三四五六七八九")}
HEAD = re.compile(r"^# 第([一二三四五六七八九十]+)章　")
REF = re.compile(u"(第([一二三四五六七八九十]+)章)(第([一二三四五六七八九十]+)節)")
TAG = u"〔指針待判〕"


def cnum(s):
    """漢語序數轉整數：一→1、十→10、十七→17、二十一→21；不能解者返 0。"""
    if s in CN:
        return CN[s]
    if s == u"十":
        return 10
    if u"十" not in s:
        return 0
    a, _, b = s.partition(u"十")
    tens = 1 if a == u"" else CN.get(a, 0)
    return tens * 10 + CN.get(b, 0)


def chapter_blocks(text):
    """以「# 第N章　」為界，返 {章號: 該章全文}。"""
    lines = text.split("\n")
    idx = [(cnum(m.group(1)), i) for i, m in
           ((i, HEAD.match(l)) for i, l in enumerate(lines, 1)) if m]
    blocks = {}
    for k, (n, s0) in enumerate(idx):
        e0 = idx[k + 1][1] - 1 if k + 1 < len(idx) else len(lines)
        blocks[n] = "\n".join(lines[s0 - 1:e0])
    return blocks


def section_exists(block_text, sec_full):
    """該章之內確有以「第M節」起首之標題（H2～H6）；裸序數之列項不算。"""
    return bool(re.search(r"^#{2,6} " + re.escape(sec_full), block_text, re.M))


def dead_refs(text):
    """逐一產出 (match, 已掛標?)，只收「章在而節無」者。章本身不存在者不計（由章級死鏈掌之）。"""
    blocks = chapter_blocks(text)
    for m in REF.finditer(text):
        tg = blocks.get(cnum(m.group(2)))
        if not tg or section_exists(tg, m.group(3)):
            continue
        yield m, text[m.end():m.end() + len(TAG)].startswith(TAG)


def fanli_span(lines):
    """合編本卷首【合編凡例】之行的界 (起, 迄)；查無返 None。

    凡例自述帳標之形（〔待寫〕之類）會給自己的帳加一筆，故計帳・計死鏈須除此段；
    以「H2 起、下一 H2 迄」之結構劃界，改名即返 None 而由尺高報，不作靜默失效。
    """
    i = next((k for k, l in enumerate(lines) if l.startswith(u"## 【卷首・合編凡例】")), None)
    if i is None:
        return None
    j = next((k for k in range(i + 1, len(lines)) if lines[k].startswith(u"## ")), len(lines))
    return i, j


def no_fanli(lines):
    """去掉凡例段之册身（計帳之用）。查無凡例則原樣返（由尺另報其缺）。"""
    sp = fanli_span(lines)
    return "\n".join(lines if not sp else lines[:sp[0]] + lines[sp[1]:])

def tag_dead(text):
    """凡節級死鏈就地掛〔指針待判〕，返 (新文, 掛標數)。"""
    marks = {m.start() for m, _ in dead_refs(text)}
    n = [0]

    def one(m):
        if m.start() in marks:
            n[0] += 1
            return m.group(0) + TAG
        return m.group(0)

    return REF.sub(one, text), n[0]
