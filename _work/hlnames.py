# -*- coding: utf-8 -*-
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import hulan_path as HP
GO = "--go" in sys.argv

PAIRS = [
    # 一・名形歸通例（語料核：頻婆娑羅 0 見、目犍連 0 見；書中通例 瓶沙 16・目連 4）
    (u"**故妄語的起源：** 頻婆娑羅王曾向佛陀發願", u"**故妄語的起源：** 瓶沙王曾向佛陀發願"),
    (u"成為與舍利弗、目犍連並駕齊驅的偉大聖者！", u"成為與舍利弗、目連並駕齊驅的偉大聖者！"),
    # 二・第十五章案例七第 5 點與本章第四節『制度妥協』項對齊（去「證明自己不是壓迫」之美化，
    #     轉入律文親留之活口；『除因緣』三名相不掛逐字式樣，免與 L5761 之【重制戒文】重覆自稱）
    (u"**佛陀把這條最難的戒交給最有資格拒絕的人，因為只有她守得住，這條戒才證明自己不是壓迫。**",
     u"**佛陀不把這條戒美化為榮耀：它是一道制度妥協，其代價由被壓住的一方付清（說詳本章第四節第三項）；"
     u"而他在條文裡親手留下的活口，正是戒文那三個字——『除因緣』。**"),
]

raw = io.open(HP.SRC, encoding="utf-8", newline="").read()
NL = u"\r\n" if u"\r\n" in raw else u"\n"
lines = raw.split(NL)
n0, cr0 = len(lines), raw.count(u"\r\n")
star0, bang0 = raw.count(u"**"), raw.count(u"！")
bad = []
for old, new in PAIRS:
    c = raw.count(old)
    print(u"  命中 %d｜%s" % (c, old[:46]))
    if c != 1:
        bad.append(old[:30])
if raw.count(u"頻婆娑羅") != 1 or raw.count(u"目犍連") != 1:
    bad.append(u"名形總數不合（期各 1 枚）")
if bad:
    print(u"預檢未過，一字未寫：" + u"；".join(bad))
    sys.exit(1)
if not GO:
    sys.exit(u"試跑畢；加 --go 方寫")

out = raw
for old, new in PAIRS:
    out = out.replace(old, new, 1)
io.open(HP.SRC, "w", encoding="utf-8", newline="").write(out)

back = io.open(HP.SRC, encoding="utf-8", newline="").read()
errs = []
if len(back.split(NL)) != n0 or back.count(u"\r\n") != cr0:
    errs.append(u"行數或 EOL 走樣：%d/%d（期 %d/%d）" % (len(back.split(NL)), back.count(u"\r\n"), n0, cr0))
for old, new in PAIRS:
    if back.count(new) != 1:
        errs.append(u"新形未立：%s" % new[:26])
    if back.count(old) != 0:
        errs.append(u"舊形猶在：%s" % old[:26])
if back.count(u"**") != star0:
    errs.append(u"粗體對數走樣：%d→%d" % (star0, back.count(u"**")))
if back.count(u"！") > bang0:
    errs.append(u"嘆號增量")
print(u"== 回讀：%s ==" % (u"全中（行 %d・CR %d・粗體 %d 對俱不動）" % (n0, cr0, star0 // 2)) if not errs else u"有失")
for e in errs:
    print(u"  ✗ " + e)
sys.exit(1 if errs else 0)
