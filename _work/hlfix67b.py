# -*- coding: utf-8 -*-
"""第 67 輪・乙：目錄之撮述補行・款5 之巴利除・指針三處歸位・全書案例自報改約。
法：唯一錨＋命中數斷言＋CRLF 等式＋備份＋SHA；行插入以內容定位（免死行號）。
用法：python -X utf8 _work/hlfix67b.py [--go]
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
BAK = BOOK + ".bak67b"
GO = "--go" in sys.argv

raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert raw.count(u"\r") == raw.count(u"\n") == raw.count(u"\r\n"), u"入口 CRLF 已傷"
L = raw.split(u"\r\n")
N0, sha0 = len(L), hashlib.sha256(raw.encode("utf-8")).hexdigest()

EDITS = [
    (u"甲 目錄補『衛生』一目", u"  * 飲食威儀：征服最原始的獸性衝動",
     u"    * 衛生與敬畏自然：慈護細小有情", 1, u"after"),
    (u"乙 款5 除巴利（本地無從覆核）",
     u"#### 5. 覓罪相（罪處所，Amūlakā-vinaya）：把前後相違寫進公共紀錄",
     u"#### 5. 覓罪相（犍度之羯磨文作『罪處所』）：把前後相違寫進公共紀錄", 1, u"this"),
    (u"丙1 指針：塔下一組今為案例一", u"| 第十章案例六 | 眾學法 | 十次「我不敢」與十次「佛言聽」——",
     u"| 第十章案例一 | 眾學法 | 五次「我不敢」與六次「佛言聽」——", 1, u"this"),
    (u"丙2 指針：同上（十線地圖散文）", u"每一式各結一戒（第十章案例六）",
     u"每一式各結一戒（第十章案例一）", 1, u"this"),
    (u"丙3 指針：飯桌一組今為案例二", u"【第十章案例五（同一飯桌之時限）】",
     u"【第十章案例二（同一飯桌之時限）】", 1, u"this"),
    (u"丁 全書案例自報改約", u"把全書一百三十四則案例", u"把全書一百三十三則案例", 1, u"this"),
]

for tag, old, new, want, mode in EDITS:
    hits = [i for i, l in enumerate(L) if old in l]
    assert len(hits) == want, u"%s｜命中 %d（欲 %d）：%s" % (tag, len(hits), want, old[:30])
    i = hits[0]
    cnt = L[i].count(old)
    assert cnt == 1, u"%s｜行內重出 %d" % (tag, cnt)
    if mode == u"after":
        assert new not in u"\r\n".join(L), u"%s｜已存在，勿兩插" % tag
        L[i + 1:i + 1] = [new]
        print(u"  %s 插於 L%-5d 後 ✓" % (tag, i + 1))
    else:
        L[i] = L[i].replace(old, new)
        print(u"  %s L%-5d ✓×%d" % (tag, i + 1, cnt))

txt = u"\r\n".join(L)
assert txt.count(u"\r") == txt.count(u"\n") == len(L) - 1, u"CRLF 變形"
print(u"行數 %d→%d" % (N0, len(L)))
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
assert not os.path.exists(BAK) or io.open(BAK, encoding="utf-8", newline=u"").read() == raw, u"備份不同本"
if not os.path.exists(BAK):
    shutil.copy2(BOOK, BAK)
with open(BOOK, "wb") as fh:
    fh.write(txt.encode("utf-8"))
chk = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert chk == txt, u"回讀不符"
print(u"已寫檔｜sha %s→%s｜備份 %s" % (
    sha0[:12], hashlib.sha256(chk.encode("utf-8")).hexdigest()[:12], os.path.basename(BAK)))
