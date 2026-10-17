# -*- coding: utf-8 -*-
"""第 41 輪补丁（批八之一～四）：犍度歸屬三處、兩張板塊圖之漏號重號、案例二十一補第118條、
   阿姨／故二 隨文註。全用行內替換，每處必斷言命中 1；新增逐字引號先過語料閘。
用法：python -X utf8 _work/r8patch.py [--go]"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
GO = u"--go" in sys.argv
BOOK = HP.SRC
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
L = raw.split(u"\r\n")
V = _tk.VINAYA
nsub = 0


def sub(old, new, want=1):
    """行內替換：old 須在全書命中 want 處（預設 1），否則擡槓。"""
    global nsub
    hits = [i for i, s in enumerate(L) if old in s]
    tot = sum(L[i].count(old) for i in hits)
    assert tot == want, u"命中 %d（應 %d）：%s" % (tot, want, old[:60])
    for i in hits:
        L[i] = L[i].replace(old, new)
        print(u"  ✓ L%-5d｜%s" % (i + 1, old[:34]))
    nsub += len(hits)


def verbatim(t):
    """逐字閘：去標點後須為語料之連續子串。"""
    s = _tk.norm(t)
    assert s and s in _tk.norm(V), u"語料無此連写：%s" % t[:40]
    return t


def dw(s):
    return sum(2 if ord(c) > 0x2000 else 1 for c in s)


def render(pairs):
    """依欄位起始之顯示寬重排一行：pairs = [(start, text), ...]（須升冪）。"""
    out, w = [], 0
    for idx, (st, c) in enumerate(pairs):
        nxt = pairs[idx + 1][0] if idx + 1 < len(pairs) else None
        assert w <= st, u"欄位溢位：格起點 %d＜已排 %d" % (st, w)
        if nxt is not None:
            assert st + dw(c) <= nxt, u"格逾欄寬：%s（%d＋%d＞%d）" % (c, st, dw(c), nxt)
        out.append(u" " * (st - w) + c)
        w = st + dw(c)
    return u"".join(out)


def regrid(ln, cells, starts):
    """改圖一行：原有欄位之起始不得挪動；新填之格須塞得進其右界。"""
    i = ln - 1
    old = L[i]
    got = [dw(old[:m.start()]) for m in re.finditer(u"[^ ]+(?: [^ ]+)*", old)]
    assert all(s in starts for s in got), u"L%d 原有欄位 %s 有被挪動者" % (ln, got)
    pairs = [(st, c) for st, c in zip(starts, cells) if c]
    for st, c in pairs:
        if st in got:
            continue                      # 原有之格，其界由 render 統一看
        rig = [g for g in got if g > st]
        assert not rig or st + dw(c) <= rig[0], u"L%d 新欄@%d『%s』擠開原有欄" % (ln, st, c)
    L[i] = render(pairs)
    print(u"  ✓ 圖 L%-5d｜%s" % (ln, L[i][:44]))


# ===== 一、犍度歸屬（衣揵度之三处；皮革揵度之木刺一案仍存）=====
print(u"【一】犍度歸屬")
sub(u"（皮革揵度不為醫立法", u"（衣揵度之一不為醫立法")
sub(u"皮革揵度之餘記此一大事", u"衣揵度之三記此一大事")
sub(u"同一批皮革揵度的文字裡", u"同一批衣揵度的文字裡")
assert u"皮革揵度" in L[4122], u"L4123 木刺一案之皮革揵度須存"

# ===== 二、兩張板塊圖：補漏號、去重號（欄寬不動）=====
print(u"【二】板塊圖")
S14 = [0, 20, 42, 64]
regrid(5049, [u"90～91條）", u"95～98、", u"87～89、92～94、99、", u"嚴禁度孕婦、"], S14)
regrid(5052, [u"手指過限、", u"禁露身裸浴引誘狂徒、", u"惡意咒詛、親近居士、", u"「六法考驗期」"], S14)
regrid(5053, [u"禁拍擊嬉鬧、", u"禁一切時人間遊行、", u"安居中驅他出房、", None], S14)
regrid(5054, [u"禁共被眠", u"禁邊界險境與觀王宮", u"倒賣生穀、誦世俗咒術", None], S14)
S15 = [0, 20, 42, 66]
regrid(5589, [u"148～149、", u"171～175條）", u"176～178條）", u"未著胸衣不得入村、"], S15)
regrid(5590, [u"165～170條）", u"半月必須向男僧", u"嚴禁緊身衣、搖臀行步、", u"禁黃昏落鎖後出門、"], S15)
regrid(5591, [u"嚴禁度逃婚情傷女、", u"請教誡、安居竟", u"嚴禁首飾珠寶、皮草", u"禁不參加結夏安居"], S15)
regrid(5592, [u"禁父母夫主不聽、", u"向男僧行自恣、", u"嚴禁任何人塗香按摩", u"（防暗夜暴徒襲擊）"], S15)
regrid(5593, [u"隔年方准度一人、", u"長老尼禮敬新受戒比丘", u"（粉碎最後的感官享受）", None], S15)
regrid(5594, [u"嚴禁度逃債重病者、", u"（八敬法落實、", None, None], S15)
regrid(5595, [u"禁嫉家與足食後食", u"外部司法監督）", None, None], S15)

# ===== 三、案例二十一補第118條 =====
print(u"【三】第118條")
sub(u"案例二十一：靠什麼活——呪術、紡縷、外道食與親近居士（第99、112、114、117條）",
    u"案例二十一：靠什麼活——呪術、紡縷、外道食與親近居士（第99、112、114、117、118條）", 2)  # 目錄＋正文
v118 = verbatim(u"若比丘尼教人誦習呪術者，波逸提。")
sub(u"「**若比丘尼誦習世俗呪術者，波逸提。**」「**若比丘尼與白衣",
    u"「**若比丘尼誦習世俗呪術者，波逸提。**」「**若比丘尼教人誦習呪術者，波逸提。**」"
    u"（此律無別因緣，即於前條戒文之後隨制而宣）「**若比丘尼與白衣")
sub(u"**四條戒問的是同一個問題：一個出家人靠什麼活？**",
    u"**五條戒問的是同一個問題：一個出家人靠什麼活？**")
sub(u"這四條路都能活", u"這五條路都能活")
sub(u"四條合起來是一張圖", u"五條合起來是一張圖")

# ===== 四、名相隨文註：阿姨、故二 =====
print(u"【四】隨文註")
sub(u"我今隨佛出家。和尚某甲，如來、無所著、等正覺是我世尊。**」第二、第三亦如是說。",
    u"我今隨佛出家。和尚某甲，如來、無所著、等正覺是我世尊。**」第二、第三亦如是說。"
    u"（阿姨乃律中對比丘尼之敬稱：尼眾自陳如是呼，俗人、宮人呼尼亦如是呼，猶言大姐。）")
sub(u"跋闍子比丘愁憂不樂淨行，還家與故二共行不淨",
    u"跋闍子比丘愁憂不樂淨行，還家與故二（律中或作本二，謂出家前之妻子）共行不淨")

txt = u"\r\n".join(L)
assert txt.count(u"\r\n") == len(L) - 1, u"CRLF 變形"
print(u"替换 %d 處｜行數 %d→%d｜%s" % (nsub, len(raw.split(u"\r\n")), len(L), u"寫檔" if GO else u"覆核模式（未寫檔）"))
if GO:
    io.open(BOOK, u"w", encoding="utf-8", newline=u"").write(txt)
