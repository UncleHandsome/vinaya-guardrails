# -*- coding: utf-8 -*-
"""第 57 輪・丙：新第十一章之案例次序全變，書中『第十一章案例N』指針須逐條歸位。
法源＝案例主題之對照（舊→新），非行號；每條須同時命中『舊號（取最長者）』與『該行語義鑰』，否則不動。
印：管轄 21 條（改 19・不動 2）｜改前後各量『第十一章案例』之總數，須同。
用法：python -X utf8 _work/hlref57.py [--go]
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert raw.count(u"\r") == raw.count(u"\n"), u"入口 CRLF 已傷"
L = raw.split(u"\r\n")

CN = u"零一二三四五六七八九十"


def cn2int(s):
    if s == u"十":
        return 10
    if len(s) == 1:
        return CN.index(s)
    if s.startswith(u"十"):
        return 10 + CN.index(s[1])
    if len(s) == 3 and s[1] == u"十":
        return CN.index(s[0]) * 10 + CN.index(s[2])
    return CN.index(s[0]) * 10


def int2cn(n):
    if n <= 10:
        return CN[n] if n < 10 else u"十"
    if n < 20:
        return u"十" + CN[n - 10]
    if n == 20:
        return u"二十"
    return u"二十" + CN[n - 20]


# 舊編 → 新編（依案例主題配對；新章之『瞻病』二幕合一、『表決』三幕歸樞紐，故序盡變）
MAP = {1: 1, 2: 2, 3: 3, 4: 4, 5: 21, 6: 14, 7: 16, 8: 5, 9: 6, 10: 15, 11: 22,
       12: 23, 13: 17, 14: 18, 15: 13, 16: 7, 17: 8, 18: 11, 19: 24, 20: 25,
       21: 26, 22: 27, 23: 19, 24: 9, 25: 20, 26: 12, 27: 10}

# （正本页，舊號，語義鑰）——鑰須見於本行，防『同號異案』之誤改
WANT = [
    (506, 5, u"無人探視而死的病比丘"), (507, 19, u"一扶起"), (508, 20, u"割髀肉"),
    (524, 1, u"隔開坐"), (525, 17, u"三種投票與監票五法"), (526, 24, u"七種不如法的表決"),
    (569, 26, u"二十組五法"), (570, 18, u"兩張對稱的清單"), (586, 4, u"疲極"),
    (587, 15, u"中途遇賊"), (588, 16, u"知日數不知日數"), (589, 25, u"迦絺那衣"),
    (590, 27, u"自恣"), (735, 9, u"自習課"), (2086, 4, u"結界與賊難"),
    (2619, 9, u"行覆藏者"), (2642, 9, u"停權者不得再執務"), (2666, 9, u"授權與停權"),
    (2688, 9, u"敷座洗脚"), (2709, 9, u"職務停權"), (3464, 10, u"空間即護欄"),
    (3487, 9, u"判定權在當事人之外"), (6546, 9, u"行覆藏者之停權"),
]

TOK = re.compile(u"第十一章案例([一二三四五六七八九十]+)(?![一二三四五六七八九十])")
n_tot = sum(len(TOK.findall(x)) for x in L)
_cover = sum(len(TOK.findall(L[n - 1])) for n, _o, _k in WANT)
assert _cover == n_tot, u"名單只覆蓋 %d／全書 %d 處，必有漏指" % (_cover, n_tot)
print(u"書中『第十一章案例N』指針共 %d 處｜名單全覆蓋" % n_tot)
n_ch = n_stay = 0
for n, old, key in WANT:
    l = L[n - 1]
    hits = [int(cn2int(m.group(1))) for m in TOK.finditer(l)]
    assert hits, u"L%d 無指針，名單已老" % n
    assert hits.count(old) == 1, u"L%d 舊號『案例%s』命中 %d 次，不敢擅動" % (n, old, hits.count(old))
    assert key in l, u"L%d 語義鑰『%s』不在本行" % (n, key)
    new = MAP[old]
    if new == old:
        n_stay += 1
        print(u"  不動 L%-5d 案例%s（%s）｜序未變" % (n, int2cn(old), key))
        continue
    L[n - 1] = TOK.sub(lambda m: u"第十一章案例" + (int2cn(MAP[cn2int(m.group(1))])
                                                   if cn2int(m.group(1)) == old else m.group(1)), l)
    assert L[n - 1].count(u"第十一章案例" + int2cn(new)) == 1, u"L%d 替後未見新號" % n
    n_ch += 1
    print(u"  改  L%-5d 案例%s→案例%s｜%s" % (n, int2cn(old), int2cn(new), key))
print(u"名單 %d 條：改 %d・不動 %d" % (len(WANT), n_ch, n_stay))
assert sum(len(TOK.findall(x)) for x in L) == n_tot, u"指針總數變形"
if u"--go" in sys.argv:
    txt = u"\r\n".join(L)
    assert txt.count(u"\r") == txt.count(u"\n"), u"出口 CRLF 變形"
    io.open(BOOK, "w", encoding="utf-8", newline=u"").write(txt)
    print(u"已寫檔")
else:
    print(u"（乾跑：加 --go 始寫）")
