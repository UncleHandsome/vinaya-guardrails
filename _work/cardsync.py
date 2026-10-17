# -*- coding: utf-8 -*-
"""cardsync.py —— 三印卡兩處（第八章『速覽』與結語『全本』）之共有句須逐字相同（第 148 輪立）。

緣起：一卡兩載而無器校之，則字句必 drift——本輪實測九處各說一例（『看錯沒』與『看錯沒看錯』、
二鏡括目二與四、『便有生路』與『步步有路』、『和』與『和合』、『歇息』與『吹風』、語序倒順、
三鏡結句之闕一腿……），行者影印兩卡遂成兩個版本。

口徑：唯校兩卡共有之骨架——【體·】【用·】【息·】三標之括號副題，及『一鏡／二鏡／三鏡』三條
（各條取其內全部續行，折去空白後逐字對校）。體印之『心印』一行與息印之正文屬速覽與全本之分，
兩存不較（一從其全、一存其簡，此書之制）。
退出碼：漂移 > 0 即退 1；`argv[1]` 可注副本以供負測。
"""
import io, os, re, sys
if len(sys.argv) > 1:
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    L = io.open(sys.argv[1], encoding='utf-8').read().split(u'\n')
else:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import _tk as t
    L = t.LINES
HEADS = (u'【隨身三印卡·速覽', u'【體·略戒無事印】')


def grab(key):
    """取該卡內文：自 key 之後第一行含『【體·』者起，至圍欄閉管止。"""
    i = next((k for k, l in enumerate(L) if key in l), None)
    if i is None:
        return None
    j = next((k for k in range(i, min(i + 12, len(L))) if u'【體·' in L[k]), None)
    if j is None:
        return None
    out = []
    for k in range(j, len(L)):
        line = L[k]
        if line.strip() == u'```':
            break
        if set(line.strip()) <= set(u'=⏎'):
            continue
        out.append(line.rstrip())
    return out or None


def blocks(rows):
    """拆為 {標: 折白後之文}——標含三印副題與一／二／三鏡。"""
    res, cur, buf = {}, None, []

    def flush():
        if cur:
            res[cur] = re.sub(u'\\s+', u'', u''.join(buf))
    for line in rows:
        s = line.strip()
        m = re.match(u'^【([體用息])·[^】]*】（([^）]*)）', s)
        n = re.match(u'^([一二三]鏡)', s)
        if m or n:
            flush()
            cur = u'%s|%s' % (m.group(1) if m else n.group(1), m.group(2) if m else u'')
            if m:
                res.setdefault(u'印標' + m.group(1), m.group(2))
                cur = None
                continue
            buf = [s]
        elif cur:
            buf.append(s)
    flush()
    return res


A = grab(u'【隨身三印卡·速覽')
B = grab(u'### 五、行者隨身三印卡')
if not A or not B:
    print(u'查無兩卡（速覽或結語全本）——請先查檔，勿綠燈而過')
    sys.exit(1)
ba, bb = blocks(A), blocks(B)
keys = sorted(set(ba) & set(bb))
bad = [(k, ba[k], bb[k]) for k in keys if ba[k] != bb[k]]
print(u'三印卡兩處對校：共骨架 %d 條（速覽 %d／全本 %d）｜漂移 %d 處' % (len(keys), len(ba), len(bb), len(bad)))
for k, x, y in bad:
    print(u'  %-14s 速覽=%s' % (k, x[:70]))
    print(u'  %-14s 全本=%s' % (u'', y[:70]))
if len(keys) < 3:
    print(u'警告：可比之條目過少（%d），取卡式或已失效——此綠不可信' % len(keys))
    sys.exit(1)
sys.exit(1 if bad else 0)
