# -*- coding: utf-8 -*-
"""第 66 輪・收尾甲：丙組歸真之三處「新句與舊句重出」之除複＋兩枚簡形之歸正。
病（simp_sweep 與目視同逮）：丙5 之替換把「今語轉折句」整段重打一遍，舊句未刪，
    遂成 L2670／L2701／L2720 三處同義重出；且我手打之兩處帶簡形（当→當、条→條）。
治：只刪重出之半句，不動作者一拍之文；簡形以字元本身改，改後印碼位覆讀。
法：唯一錨＋命中數斷言＋行號定位＋CRLF 等式＋備份＋SHA 一步回退；乾跑為預設。
用法：python -X utf8 _work/hlfix66d.py [--go]
"""
import os as _hp_os, sys as _hp_sys
_hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__))))
import hulan_path as HP
import hashlib
import io
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
BAK = BOOK + ".bak66d"
GO = "--go" in sys.argv

raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert raw.count(u"\r") == raw.count(u"\n") == raw.count(u"\r\n"), u"入口 CRLF 已傷"
L = raw.split(u"\r\n")
N0, sha0 = len(L), hashlib.sha256(raw.encode("utf-8")).hexdigest()

# (稿行號, 舊錨, 新文, 命中數)
FIX = [
    (2670,
     u"嘔吐物。佛陀停下腳步，指著地上的娑伽陀，對阿難說出了全律藏最冷酷的一句反問：（旁有溝中",
     u"嘔吐物。（旁有溝中", 1),
    (2701,
     u"拖字訣，企圖以此無限期癱瘓審判。 企圖藉由「質疑法律本身的權威性」來無限期拖延審判。佛陀當場",
     u"拖字訣，企圖以此無限期癱瘓審判。佛陀當場", 1),
    (2701, u"当作", u"當作", 1),
    (2720,
     u"面前，滿臉無辜、裝瘋賣傻地大叫：滿臉無辜、裝瘋賣傻地搶先大叫：",
     u"面前，滿臉無辜、裝瘋賣傻地大叫：", 1),
    (2720, u"戒經裡有這一条", u"戒經裡有這一條", 1),
]

for idx, old, new, want in FIX:
    line = L[idx - 1]
    c = line.count(old)
    assert c == want, u"稿L%d 錨命中 %d（欲 %d）：%s" % (idx, c, want, old[:24])
    assert old != new
    L[idx - 1] = line.replace(old, new)
    print(u"  ✓ L%-5d ×%d  %s → %s" % (idx, want, old[:16], new[:16]))

for idx in (2670, 2701, 2720):
    for ch in (u"當", u"條"):
        if ch in L[idx - 1]:
            print(u"  碼位覆讀 L%-5d %s=U+%04X" % (idx, ch, ord(ch)))

txt = u"\r\n".join(L)
assert txt.count(u"\r") == txt.count(u"\n") == len(L) - 1, u"CRLF 變形"
print(u"行數 %d→%d｜刪複 %d 處｜簡形 %d 枚" % (N0, len(L), 3, 2))
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
assert not os.path.exists(BAK), u"備份已存在：%s" % BAK
shutil.copy2(BOOK, BAK)
io.open(BOOK, "w", encoding="utf-8", newline=u"").write(txt)
chk = io.open(BOOK, "rb").read()
print(u"已寫檔｜sha %s→%s｜備份 %s" % (
    sha0[:12], hashlib.sha256(chk).hexdigest()[:12], os.path.basename(BAK)))
