# -*- coding: utf-8 -*-
"""第 57 輪・庚之單一法源：『印面單段過長』之名單與切段函數（hlsplit57 用之、hlunjoin57 亦用之）。
切點口徑：只給純漢字錨（免手抄標點之誤），自錨末字向後找第一個句末符（。！？），並吞其後之閉引號／粗體星號。
年表：原單 15 處；L4730『十一條如次』經 h4seq 現形為錯切（連綴列舉一經換段，散文手寫序號即成 5→7 斷鏈），
      故 hlsplit57 之口徑除之以外；本單仍留全數，退刀器須認得它。
"""
import re

TAIL = u"」』）】**"          # 句末之後可一併吞去的閉合符
FLOOR = 34                   # 收束之短段可留；再短即切點選錯，如實報出不寫
CN = lambda s: len(re.sub(u"[^一-龥]", u"", s))

SPL_ALL = [
    (73,   [u"凡案例俱在四分律六十卷之內", u"凡不可指認今人者一概不寫"]),
    (920,  [u"第一句便是最初未制戒者不犯"]),
    (1303, [u"門檻前三條免責被寫得一模一樣", u"不是那一樁行為的果"]),
    (1320, [u"此段本書已見下文", u"今甚樂梵行修無上道", u"佛未制戒前不見欲穢"]),
    (1343, [u"我都不自憶以材與人", u"於是無數方便訶責之後放人", u"無使入村勿復安止"]),
    (1352, [u"佛陀寧可交給團體之外的共識", u"原則不可外包僧團不自訂與社會秩序相左之刑"]),
    (1388, [u"兩組都答住止安樂", u"得到的回答是律藏中罕見的坦承"]),
    (3465, [u"因為下一次未必有人這樣答", u"入豪貴長者家過門閾盡突吉羅"]),
    (4449, [u"引發了對尼僧人身安全的極大恐慌"]),
    (4730, [u"四字是授權的最短形式", u"並見第七章案例八"]),
    (5079, [u"使彼慚愧休道", u"若閉戶使不得入突吉羅"]),
    (5360, [u"而不即縫成", u"留難不作衣供養"]),
    (5395, [u"我正可守視而已耳", u"即時現園蒜取盡"]),
    (5999, [u"故名七百集法毘尼", u"本書不作律據"]),
    (6365, [u"本書不混", u"說見第一章"]),
]
NO_CUT = {4730}              # 連綴式列舉，分段即斷鏈（h4seq 之誡）
SPL = [x for x in SPL_ALL if x[0] not in NO_CUT]


def cut(line, anchors):
    """回 [片段…]（未加縮排）；錨只對『純漢字骨幹』定位，故原行序由骨幹序一一回推。"""
    if not anchors:
        raise AssertionError(u"無錨")
    cpos = [i for i, ch in enumerate(line) if u"一" <= ch <= u"龥"]
    cjk = u"".join(line[i] for i in cpos)
    cuts = []
    for a in anchors:
        c = cjk.count(a)
        assert c == 1, u"錨於本行命中 %d：%s" % (c, a[:16])
        k = cpos[cjk.index(a) + len(a) - 1]
        q = next(i for i in range(k, len(line)) if line[i] in u"。！？")
        while q + 1 < len(line) and line[q + 1] in TAIL:
            q += 1
        cuts.append(q + 1)
    cuts = sorted(set(cuts))
    assert len(cuts) == len(set(cjk.index(a) for a in anchors)), u"切點重複"
    parts, prev = [], 0
    for c in cuts:
        parts.append(line[prev:c])
        prev = c
    parts.append(line[prev:])
    out = []
    for idx, x in enumerate(parts):
        x = x.rstrip(u"　")                            # 假分段之全形空格一律清掉
        if idx < len(parts) - 1:
            x = x.rstrip()                             # 唯末段之行尾兩空格（硬換行）須留
        if x.strip(u"　 "):
            out.append(x)
    return out


def indent_of(line):
    ind = re.match(u"^\\s*", line).group(0)
    if re.match(u"^\\s*\\*\\s", line):
        return ind + u"  "                             # 無序清單之內容欄
    if re.match(u"^\\s*\\d+\\.\\s", line):
        return ind + u"   "                            # 有序清單之內容欄
    return ind
