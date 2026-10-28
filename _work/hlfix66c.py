# -*- coding: utf-8 -*-
"""第 66 輪・丙：第八章／第九章換稿後之指針歸位與總數宣稱改約。

法源＝條號：新章案例標題自帶條號，故以（章・條→新案例）之索引重算每處指針應指何方，
　　　　　不憑印象、不抄舊表；無條號可據者（散文中之概念性指針）另立明表逐條判定。
硬斷言：改後 refchk 須疑點 0；全書案例實數 134 與十線地圖導言之自報同步。
用法：python -X utf8 _work/hlfix66c.py [--go]
"""
import hashlib
import io
import os
import re
import shutil
import sys

BOOK = u"佛陀的護欄 四分律比丘與比丘尼戒的行為心理學解析.txt"
BAK = BOOK + u".bak66c"
GO = u"--go" in sys.argv
raw = io.open(BOOK, "rb").read()
sha0 = hashlib.sha256(raw).hexdigest()
L = raw.decode("utf-8").split(u"\r\n")
N0 = len(L)
assert raw.count(b"\r") == raw.count(b"\n"), u"入口 CRLF 已傷"
U = u"零一二三四五六七八九十"
def cn2int(s):
    if s.isdigit():
        return int(s)
    if s == u"十":
        return 10
    if s.startswith(u"十"):
        return 10 + U.index(s[1])
    if len(s) == 3 and s[1] == u"十":
        return U.index(s[0]) * 10 + U.index(s[2])
    if s.endswith(u"十"):
        return U.index(s[0]) * 10
    return U.index(s) if s else 0


int2cn = lambda n: U[n] if n < 10 else (u"十" if n == 10 else (
    u"十" + U[n - 10] if n < 20 else U[n // 10] + u"十" + (U[n % 10] if n % 10 else u"")))

# ── 一・（章・條）→新案例 之索引（自正文實算） ────────────────────────
H1 = [(i, l) for i, l in enumerate(L) if re.match(u"^# ", l)]


def span(name):
    k = [j for j, (i, l) in enumerate(H1) if l.startswith(name)][0]
    return H1[k][0], H1[k + 1][0]


MAP = {}
for ch, nm in ((8, u"# 第八章"), (9, u"# 第九章")):
    a, z = span(nm)
    for l in L[a:z]:
        if not l.startswith(u"#### 案例"):
            continue
        cas = cn2int(re.match(u"^#### 案例([〇零一二三四五六七八九十]+)：", l).group(1))
        nums = set()
        for grp in re.findall(u"（第([0-9、～]+?)條）", l):
            for part in grp.split(u"、"):
                if u"～" in part:
                    x, y = [int(v) for v in part.split(u"～")]
                    nums.update(range(x, y + 1))
                elif part.strip().isdigit():
                    nums.add(int(part))
        for n in nums:
            MAP[(ch, n)] = cas
print(u"索引：第八章 %d 條｜第九章 %d 條" % (
    sum(1 for k in MAP if k[0] == 8), sum(1 for k in MAP if k[0] == 9)))


def nums_near(t, p):
    seg = t[max(0, p - 70): p + 130]
    out = []
    for grp in re.findall(u"第([0-9、～]+?)條", seg):
        for part in grp.split(u"、"):
            part = part.strip()
            if u"～" in part:
                x, y = [int(v) for v in part.split(u"～")]
                out.extend(range(x, y + 1))
            elif part.isdigit():
                out.append(int(part))
    return out


REF = re.compile(u"(第([八九])章案例)([〇零一二三四五六七八九十]{1,3})")
n_auto = 0
for i in range(len(L)):
    if i >= span(u"# 第八章")[0] and i < span(u"# 第十章")[0]:
        pass
    changed, guard = True, 0
    while changed and guard < 6:
        guard += 1
        changed = False
        for m in REF.finditer(L[i]):
            ch = 8 if m.group(2) == u"八" else 9
            old = cn2int(m.group(3))
            ns = nums_near(L[i], m.start())
            want = sorted({MAP[(ch, n)] for n in ns if (ch, n) in MAP})
            if want and want != [old] and len(want) == 1:
                new = m.group(1) + int2cn(want[0])
                L[i] = L[i][:m.start()] + new + L[i][m.end():]
                print(u"  一 L%-5d 第%d章案例%s→%s｜條號 %s" % (
                    i + 1, ch, m.group(3), int2cn(want[0]), ns))
                n_auto += 1
                changed = True
                break
print(u"  一・自動歸位 %d 處（以條號為法源）" % n_auto)

# ── 二・無條號可據者：逐條判定（散文／欄內之概念指針） ───────────────
MAN = [
    (u"別見第九章案例二十七", u"別見第九章案例五"),        # 飲酒戒（51）
    (u"詳第九章案例二十七", u"詳第九章案例五"),            # 同上
    (u"（第八章案例十四）同一思路", u"（第八章案例五）同一思路"),   # 舒手得及戶＝第43條
    (u"同室與五六語見第八章案例二", u"同室與五六語見第八章案例四"),
    (u"屏處坐見第八章案例十四", u"屏處坐見第八章案例五"),
    (u"（第九章案例二、第八章案例二十）", u"（第九章案例六）"),  # 惡見一族今合為一案
    (u"不與欲而起去者事後被追責（第九章案例三）", u"不與欲而起去者事後被追責（第九章案例八）"),
    (u"聽諍語而向彼說者各結其罪（第九章案例二十三）", u"聽諍語而向彼說者各結其罪（第九章案例八）"),
    (u"不與欲而起去見第九章案例三", u"不與欲而起去見第九章案例八"),
]
for old, new in MAN:
    hits = [i for i, t in enumerate(L) if old in t]
    assert len(hits) == 1, u"明表錨『%s』命中 %d" % (old[:24], len(hits))
    assert L[hits[0]].count(old) == 1, u"明表錨於該行多見：%s" % old[:24]
    L[hits[0]] = L[hits[0]].replace(old, new)
    print(u"  二 L%-5d｜%s → %s" % (hits[0] + 1, old[-14:], new[-14:]))

# ── 三・總數宣稱：一百六十三則 → 一百三十四則 ─────────────────────────
KN = u"把全書一百六十三則案例"
hits = [i for i, t in enumerate(L) if KN in t]
assert len(hits) == 1, u"總數宣稱命中 %d" % len(hits)
L[hits[0]] = L[hits[0]].replace(KN, u"把全書一百三十四則案例")
print(u"  三 L%d｜一百六十三則 → 一百三十四則" % (hits[0] + 1))

# ── 出口自證 ─────────────────────────────────────────────────────────
NCASE = sum(1 for l in L if l.startswith(u"#### 案例"))
assert NCASE == 134, u"全書案例實數 %d ≠ 134" % NCASE
assert u"一百六十三" not in u"".join(L), u"仍殘舊總數之自報"
bad = []
for i, t in enumerate(L):
    for m in REF.finditer(t):
        ch = 8 if m.group(2) == u"八" else 9
        old = cn2int(m.group(3))
        a, z = span(u"# 第%s章" % (u"八" if ch == 8 else u"九"))
        if i >= a and i < z:
            continue                          # 章內不引自己
        ns = nums_near(t, m.start())
        want = sorted({MAP[(ch, n)] for n in ns if (ch, n) in MAP})
        if want and old not in want:
            bad.append(u"L%d 第%d章案例%s｜條 %s 應指 %s" % (
                i + 1, ch, m.group(3), ns, want))
print(u"  覆核｜殘留可疑指針 %d 處" % len(bad))
for b in bad[:12]:
    print(u"      ？ %s" % b)
txt = u"\r\n".join(L)
assert txt.count(u"\r") == txt.count(u"\n") == len(L) - 1, u"CRLF 變形"
assert len(L) == N0, u"行數變形"
print(u"行數 %d｜正本 sha（改前）%s" % (N0, sha0[:12]))
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
assert not os.path.exists(BAK), u"備份已存在：%s" % BAK
shutil.copy2(BOOK, BAK)
io.open(BOOK, "w", encoding="utf-8", newline=u"").write(txt)
chk = io.open(BOOK, "rb").read()
print(u"已寫檔｜sha %s→%s｜%d B｜備份 %s" % (
    sha0[:12], hashlib.sha256(chk).hexdigest()[:12], len(chk), os.path.basename(BAK)))
